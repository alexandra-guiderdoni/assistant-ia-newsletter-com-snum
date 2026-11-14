"""Serveur de prototype local ; le secret peut être saisi temporairement côté navigateur."""
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import os
import threading
from pathlib import Path
from urllib.error import HTTPError
from urllib.parse import urlsplit
from .core import albert_model, collect, rebuild_packet, sources, summarize_selected

APP_HTML = (Path(__file__).parent / "index.html").read_bytes()
APP_JS = (Path(__file__).parent / "app.js").read_bytes()
DSFR_DIR = (Path(__file__).parent / "dsfr").resolve()
DSFR_TYPES = {".css": "text/css; charset=utf-8", ".js": "text/javascript; charset=utf-8", ".woff2": "font/woff2",
              ".woff": "font/woff", ".svg": "image/svg+xml", ".png": "image/png", ".ico": "image/x-icon"}
CSP = ("default-src 'none'; script-src 'self'; style-src 'self' 'unsafe-inline'; font-src 'self'; "
       "img-src 'self' data:; connect-src 'self'; manifest-src 'self'; base-uri 'none'; form-action 'self'; "
       "frame-ancestors 'none'")
HOST = "127.0.0.1"
PORT = int(os.environ.get("SNUM_PORT", "8765"))
COLLECT_LOCK = threading.Lock()
PROGRESS_LOCK = threading.Lock()
LAST_CANDIDATES = {}  # texte des candidats de la dernière collecte, jamais renvoyé au navigateur
MAX_BODY = {"/api/collect": 4096, "/api/summarize": 4096, "/api/packet": 400_000}
PROGRESS = {"phase": "idle", "done": 0, "total": 0, "current": ""}


def update_progress(phase, done, total, current=""):
    """Étape courante, sans donnée sensible : ni clé, ni URL, ni contenu."""
    with PROGRESS_LOCK:
        PROGRESS.update(phase=str(phase), done=int(done), total=int(total), current=str(current)[:120])


class Handler(BaseHTTPRequestHandler):
    server_version = "SNUMPrototype/0.1"

    def _json(self, code, payload):
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _allowed_host(self):
        return self.headers.get("Host") in {f"127.0.0.1:{PORT}", f"localhost:{PORT}"}

    def do_GET(self):
        if not self._allowed_host():
            return self._json(403, {"error": "Hôte interdit"})
        if self.path == "/api/progress":
            with PROGRESS_LOCK:
                return self._json(200, dict(PROGRESS))
        if self.path == "/api/info":
            sanitized = [{"id": s["id"], "label": s["label"], "internal": s["internal"]} for s in sources()]
            return self._json(200, {"sources": sanitized,
                                    "albert_configured": bool(os.environ.get("ALBERT_API_KEY")),
                                    "albert_model": albert_model(),
                                    "secret_persistence_enabled": os.environ.get("SNUM_ALLOW_LOCALSTORAGE") == "1"})
        if self.path.startswith("/dsfr/"):
            return self._dsfr(self.path[len("/dsfr/"):])
        if self.path not in ("/", "/index.html", "/app.js"):
            return self._json(404, {"error": "Chemin inconnu"})
        is_script = self.path == "/app.js"
        body = APP_JS if is_script else APP_HTML
        self.send_response(200)
        self.send_header("Content-Type", "text/javascript; charset=utf-8" if is_script else "text/html; charset=utf-8")
        self.send_header("Content-Security-Policy", CSP)
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _dsfr(self, relative):
        """Fichiers DSFR embarqués : liste fermée d'extensions, jamais hors du dossier."""
        target = (DSFR_DIR / relative).resolve()
        kind = DSFR_TYPES.get(target.suffix.lower())
        if "%" in relative or kind is None or DSFR_DIR not in target.parents or not target.is_file():
            return self._json(404, {"error": "Chemin inconnu"})
        body = target.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", kind)
        self.send_header("Cache-Control", "max-age=3600")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self):
        if not self._allowed_host() or self.path not in MAX_BODY:
            return self._json(403, {"error": "Requête refusée"})
        origin = self.headers.get("Origin", "")
        if origin and origin not in (f"http://127.0.0.1:{PORT}", f"http://localhost:{PORT}"):
            return self._json(403, {"error": "Origine interdite"})
        if not self.headers.get("Content-Type", "").startswith("application/json"):
            return self._json(415, {"error": "JSON requis"})
        try:
            self.connection.settimeout(10)
            size = int(self.headers.get("Content-Length", "0"))
            if not 1 <= size <= MAX_BODY[self.path]:
                raise ValueError("Taille de requête incorrecte")
            payload = json.loads(self.rfile.read(size))
        except (ValueError, json.JSONDecodeError) as exc:
            return self._json(400, {"error": str(exc)})
        if self.path == "/api/packet":
            try:
                return self._json(200, {"packet": rebuild_packet(payload)})
            except (ValueError, TypeError) as exc:
                return self._json(400, {"error": str(exc)})
        if self.path == "/api/summarize":
            return self._summarize(payload)
        return self._collect(payload)

    def _summarize(self, payload):
        if not isinstance(payload, dict):
            return self._json(400, {"error": "Paramètres JSON requis"})
        key = str(payload.get("albert_api_key") or "").strip() or os.environ.get("ALBERT_API_KEY", "")
        model = albert_model(str(payload.get("albert_model") or ""))
        try:
            if not LAST_CANDIDATES.get(payload.get("url")):
                raise ValueError("Candidat inconnu : relancez la collecte avant de repêcher un article.")
            if not (key and model):
                raise ValueError("Albert non configuré : impossible de résumer cet article.")
            article = summarize_selected(payload.get("url"), payload.get("rubric"), LAST_CANDIDATES, key=key, model=model)
        except ValueError as exc:
            return self._json(400, {"error": str(exc)})
        except HTTPError as exc:
            return self._json(502, {"error": f"Albert : HTTP {exc.code}"})
        except Exception as exc:  # noqa: BLE001 -- dernier recours, aucun détail exposé
            print(f"Repêchage échoué : {type(exc).__name__}", flush=True)
            return self._json(502, {"error": f"Albert : {type(exc).__name__}"})
        return self._json(200, {"article": article})

    def _collect(self, payload):
        if not COLLECT_LOCK.acquire(blocking=False):
            return self._json(409, {"error": "Une collecte est déjà en cours sur ce poste"})
        try:
            update_progress("sites", 0, 0)
            result = collect(payload, progress=update_progress, cache=LAST_CANDIDATES)
        except (ValueError, json.JSONDecodeError) as exc:
            return self._json(400, {"error": str(exc)})
        except Exception as exc:
            # Ne jamais exposer les erreurs détaillées du serveur ou les clés.
            print(f"Collecte échouée : {type(exc).__name__}", flush=True)
            return self._json(500, {"error": "Erreur interne, consulter le terminal local"})
        finally:
            update_progress("idle", 0, 0)
            COLLECT_LOCK.release()
        return self._json(200, result)

def main():
    print(f"Veille SNUM : http://{HOST}:{PORT}/ (local uniquement)", flush=True)
    ThreadingHTTPServer((HOST, PORT), Handler).serve_forever()


if __name__ == "__main__":
    main()

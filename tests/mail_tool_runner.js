/* Exerce les scripts réellement inclus dans le fichier distribué, sans navigateur. */
const assert = require("node:assert/strict");
const fs = require("node:fs");
const vm = require("node:vm");

async function main() {
  const {bundle, packets, invalid} = JSON.parse(fs.readFileSync(0, "utf8"));
  const canon = JSON.parse(bundle.match(/<script id="mail-canon" type="application\/json">([\s\S]*?)<\/script>/)[1]);
  const scripts = Array.from(bundle.matchAll(/<script>([\s\S]*?)<\/script>/g), match => match[1]);
  assert.equal(scripts.length, 2);
  const context = vm.createContext({window: {}, URL});
  vm.runInContext(scripts[0], context);
  const api = context.window.SnumMail;
  const rendered = packets.map(packet => {
    const json = JSON.stringify(packet);
    const html = api.build(api.parse(json), canon);
    assert.equal(api.build(api.parse(`SNUM_PAQUET_RENDU_V519_START\n${json}\nSNUM_PAQUET_RENDU_V519_END\nPAQUET_RENDU_PRET`), canon), html);
    return html;
  });
  const sample = JSON.stringify(packets[0]);
  assert.equal(api.build(api.parse(`SNUM_PAQUET_RENDU_V519_START\n${sample}\nSNUM_PAQUET_RENDU_V519_END\nPAQUET_RENDU_PRET`), canon), rendered[0]);
  assert.equal(api.build(api.parse("```json\n" + sample + "\n```"), canon), rendered[0]);
  for (const value of ["", "{", "SNUM_PAQUET_RENDU_V519_START\n" + sample, ...invalid.map(JSON.stringify)]) {
    assert.throws(() => api.parse(value));
  }

  class Element {
    constructor() { this.hidden = true; this.textContent = ""; this.value = ""; this.attributes = {}; this.listeners = {}; }
    addEventListener(name, handler) { this.listeners[name] = handler; }
    removeAttribute(name) { delete this.attributes[name]; delete this[name]; }
    setAttribute(name, value) { this.attributes[name] = value; }
    focus() { this.focused = true; }
  }
  const names = ["mail-canon", "packet-form", "packet-input", "packet-error", "mail-preview", "preview-empty", "mail-download", "render-status", "collection-notes", "collection-notes-text"];
  const elements = Object.fromEntries(names.map(name => [name, new Element()]));
  elements["mail-canon"].textContent = JSON.stringify(canon);
  const blobs = new Map(), revoked = [], windowEvents = {};
  class TestURL extends URL {
    static createObjectURL(blob) { const key = `blob:test/${blobs.size}`; blobs.set(key, blob); return key; }
    static revokeObjectURL(key) { revoked.push(key); }
  }
  const ui = vm.createContext({
    window: {SnumMail: api, addEventListener: (name, fn) => { windowEvents[name] = fn; }},
    document: {getElementById: id => elements[id]}, URL: TestURL, Blob
  });
  vm.runInContext(scripts[1], ui);
  let prevented = false;
  const submit = () => elements["packet-form"].listeners.submit({preventDefault() { prevented = true; }});
  elements["packet-input"].value = sample;
  submit();
  assert.equal(prevented, true);
  assert.equal(elements["mail-preview"].src, elements["mail-download"].href);
  assert.equal(typeof elements["mail-preview"].src, "string");
  assert.equal(elements["mail-preview"].hidden, false);
  assert.equal(elements["mail-download"].hidden, false);
  assert.equal(elements["mail-download"].download, `newsletter-snum-${packets[0].edition_date}.html`);
  const firstURL = elements["mail-download"].href;
  const blob = blobs.get(firstURL);
  assert.equal(blob.type, "text/html;charset=utf-8");
  assert.equal(await blob.text(), rendered[0]);
  assert.equal(elements["collection-notes"].hidden, packets[0].watch.length === 0);
  for (const item of packets[0].watch) {
    assert.equal(elements["collection-notes-text"].textContent.includes(item.title), true);
    assert.equal(elements["collection-notes-text"].textContent.includes(item.summary), true);
  }

  elements["packet-input"].value = "{";
  elements["packet-input"].listeners.input();
  assert.equal(elements["mail-download"].hidden, true);
  assert.equal(elements["mail-download"].href, undefined);
  assert.equal(elements["mail-preview"].src, undefined);
  assert.equal(elements["collection-notes"].hidden, true);
  assert.equal(elements["collection-notes-text"].textContent, "");
  assert.equal(revoked.includes(firstURL), true);
  submit();
  assert.equal(elements["packet-error"].hidden, false);
  assert.equal(elements["packet-error"].focused, true);
  assert.equal(elements["packet-input"].attributes["aria-invalid"], "true");
  assert.equal(elements["mail-download"].hidden, true);
  elements["packet-input"].value = JSON.stringify(packets[1]);
  submit();
  assert.equal(elements["packet-error"].hidden, true);
  assert.equal(elements["mail-download"].hidden, false);
  assert.equal(elements["packet-input"].attributes["aria-invalid"], undefined);
  assert.equal(elements["collection-notes"].hidden, packets[1].watch.length === 0);
  const finalURL = elements["mail-download"].href;
  windowEvents.pagehide();
  assert.equal(revoked.includes(finalURL), true);
  assert.equal(elements["mail-download"].hidden, true);
  assert.equal(elements["mail-download"].href, undefined);
  assert.equal(elements["mail-preview"].hidden, true);
  submit();
  assert.equal(elements["mail-download"].hidden, false);
  assert.notEqual(elements["mail-download"].href, finalURL);
  process.stdout.write(JSON.stringify({rendered, invalidRejected: invalid.length + 3, uiPassed: true}));
}

main().catch(error => {
  // Ne pas imprimer les HTML ou les paquets en cas d'échec.
  process.stderr.write(`Échec de la recette JavaScript : ${error.name}\n${error.stack.split("\n").filter(line => /^\s+at /.test(line)).join("\n")}\n`);
  process.exitCode = 1;
});

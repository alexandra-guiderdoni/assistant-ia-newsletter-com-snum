(() => {
  "use strict";
  const get = id => document.getElementById(id);
  const canon = JSON.parse(get("mail-canon").textContent);
  const form = get("packet-form"), input = get("packet-input"), error = get("packet-error");
  const preview = get("mail-preview"), empty = get("preview-empty");
  const download = get("mail-download"), status = get("render-status");
  const notes = get("collection-notes"), notesText = get("collection-notes-text");
  let objectURL = null;

  function reset() {
    preview.hidden = true;
    preview.removeAttribute("src");
    preview.removeAttribute("srcdoc");
    if (objectURL) URL.revokeObjectURL(objectURL);
    objectURL = null;
    download.hidden = true;
    download.removeAttribute("href");
    empty.hidden = false;
    error.hidden = true;
    notes.hidden = true;
    notesText.textContent = "";
    input.removeAttribute("aria-invalid");
  }

  input.addEventListener("input", () => {
    const wasRendered = objectURL !== null;
    reset();
    status.textContent = wasRendered ? "Le paquet a changé. Prévisualisez à nouveau pour télécharger le mail à jour." : "";
  });

  form.addEventListener("submit", event => {
    event.preventDefault();
    reset();
    status.textContent = "";
    try {
      const packet = window.SnumMail.parse(input.value);
      const html = window.SnumMail.build(packet, canon);
      objectURL = URL.createObjectURL(new Blob([html], {type: "text/html;charset=utf-8"}));
      download.href = objectURL;
      download.download = `newsletter-snum-${packet.edition_date}.html`;
      download.hidden = false;
      preview.src = objectURL;
      preview.hidden = false;
      empty.hidden = true;
      if (packet.watch.length) {
        notesText.textContent = packet.watch.map(item => `${item.title}\n${item.summary}`).join("\n\n");
        notes.hidden = false;
      }
      const count = packet.articles.length;
      status.textContent = `${count} ${count === 1 ? "article" : "articles"}. Le mail est prêt à télécharger.`;
    } catch (cause) {
      reset();
      error.textContent = cause.message;
      error.hidden = false;
      input.setAttribute("aria-invalid", "true");
      error.focus();
    }
  });

  window.addEventListener("pagehide", () => {
    reset();
    status.textContent = "";
  });
})();

/* Imagiter – Webseite: Hell/Dunkel, Laufband, Einblenden, Download.
   Einfaches JavaScript ohne Bibliotheken. Der Modus wird schon im <head> gesetzt (kein Aufblitzen). */
(function () {
  "use strict";
  var html = document.documentElement;
  var SPEICHER = "imagiter-webseite-modus";

  // ---------- Hell/Dunkel ----------
  var knopf = document.getElementById("modus-knopf");
  function knopfBeschriften() {
    var hell = html.dataset.modus !== "dunkel";
    knopf.setAttribute("aria-label", hell ? "Zu dunklem Design wechseln" : "Zu hellem Design wechseln");
    knopf.title = hell ? "Dunkel" : "Hell";
  }
  if (knopf) {
    knopf.addEventListener("click", function () {
      var neu = html.dataset.modus === "dunkel" ? "hell" : "dunkel";
      html.dataset.modus = neu;
      try { localStorage.setItem(SPEICHER, neu); } catch (e) {}
      knopfBeschriften();
    });
    knopfBeschriften();
  }

  // ---------- Laufband mit Jahreszahlen (doppelt, damit es nahtlos läuft) ----------
  var band = document.getElementById("jahrband");
  if (band) {
    var jahre = [];
    for (var j = 1985; j <= 2025; j++) jahre.push("<span>" + j + "</span>");
    band.innerHTML = jahre.join("") + jahre.join("");
  }

  // ---------- Einblenden beim Scrollen ----------
  var teile = document.querySelectorAll(".zeigen");
  if (html.classList.contains("js") && "IntersectionObserver" in window) {
    var beob = new IntersectionObserver(function (eintraege) {
      eintraege.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add("sichtbar"); beob.unobserve(e.target); }
      });
    }, { rootMargin: "0px 0px -8% 0px" });
    teile.forEach(function (t) { beob.observe(t); });
  } else {
    teile.forEach(function (t) { t.classList.add("sichtbar"); });
  }

  // ---------- Bilder vergrößern (ohne JavaScript öffnet der Link einfach das Bild) ----------
  var lupe = document.getElementById("lupe");
  if (lupe && typeof lupe.showModal === "function") {
    var lupeBild = document.getElementById("lupe-bild"), lupeText = document.getElementById("lupe-text");
    document.querySelectorAll(".bild-link").forEach(function (a) {
      a.addEventListener("click", function (e) {
        e.preventDefault();
        var img = a.querySelector("img"), cap = a.parentNode.querySelector("figcaption");
        lupeBild.src = a.getAttribute("href");
        lupeBild.alt = img ? img.alt : "";
        lupeText.textContent = cap ? cap.textContent : "";
        lupe.showModal();
      });
    });
    document.getElementById("lupe-zu").addEventListener("click", function () { lupe.close(); });
    lupe.addEventListener("click", function (e) { if (e.target === lupe) lupe.close(); });
  }

  // ---------- Download ----------
  // Liegt neben der Seite eine download.json, wird der Knopf freigeschaltet (siehe README.md).
  // Fehlt sie oder ist die Seite lokal geöffnet, bleibt „Demnächst“ stehen.
  var dlKnopf = document.getElementById("dl-knopf");
  function setzen(id, text) { var el = document.getElementById(id); if (el && text) el.textContent = text; }
  if (dlKnopf && location.protocol !== "file:" && window.fetch) {
    fetch("download.json", { cache: "no-store" })
      .then(function (r) { return r.ok ? r.json() : null; })
      .then(function (d) {
        if (!d || typeof d.link !== "string" || !/^https:\/\//.test(d.link)) return;
        dlKnopf.href = d.link;
        dlKnopf.removeAttribute("aria-disabled");
        setzen("dl-knopf-text", "Für Windows herunterladen");
        setzen("dl-stand", "Version " + d.version);
        setzen("dl-text", "Die aktuelle Version von Imagiter für Windows.");
        setzen("dl-version", d.version);
        setzen("dl-datum", d.datum);
        setzen("dl-groesse", d.groesse);
        setzen("dl-pruefsumme", d.sha256);
      })
      .catch(function () {});
  }
})();

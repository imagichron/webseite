/* Imagichron – Webseite: Hell/Dunkel schon vor dem Zeichnen setzen (kein Aufblitzen). Eigene Datei statt Skript im
   Seitenkopf, damit die Seite nur Skripte aus eigenen Dateien erlaubt (Content-Security-Policy im <head>). */
(function () { // Modus vor dem Zeichnen setzen: hell voreingestellt, dunkel nur nach eigener Wahl
  var m = null, h = document.documentElement;
  try { m = localStorage.getItem("imagichron-webseite-modus"); } catch (e) {}
  h.dataset.modus = m === "dunkel" ? "dunkel" : "hell";
  if (!window.matchMedia("(prefers-reduced-motion: reduce)").matches) h.classList.add("js");
})();

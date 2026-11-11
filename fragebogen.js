/* Beta-Fragebogen (beta.html): Antworten als Text zusammenstellen und im E-Mail-Programm öffnen.
   Die Seite speichert und sendet nichts selbst. Zu lange Texte (manche E-Mail-Programme kürzen
   mailto-Links ab ca. 2000 Zeichen) werden stattdessen kopiert und zum Einfügen angezeigt. */
(function () {
  "use strict";
  var ADRESSE = "kontakt@imagiter.de", BETREFF = "Imagiter-Beta: Fragebogen", GRENZE = 1800;
  var form = document.getElementById("fragebogen-form");
  if (!form) return;
  var meldung = document.getElementById("fragebogen-meldung");
  var box = document.getElementById("fragebogen-text-box"), feld = document.getElementById("fragebogen-text");

  function text() {
    var zeilen = ["Imagiter-Beta: Fragebogen", ""];
    form.querySelectorAll("fieldset").forEach(function (fs) {
      var titel = fs.querySelector("legend").textContent.trim(), teile = [];
      fs.querySelectorAll("input[type=text], select, textarea").forEach(function (el) {
        var w = el.value.trim();
        if (!w) return;
        var name = el.name || "";
        teile.push(fs.querySelectorAll("input[type=text], select, textarea").length > 1 ? name + ": " + w : w);
      });
      var gewaehlt = fs.querySelector("input[type=radio]:checked");
      if (gewaehlt) teile.push(gewaehlt.value);
      zeilen.push(titel);
      zeilen.push(teile.length ? teile.join("\n") : "–");
      zeilen.push("");
    });
    return zeilen.join("\n").trim() + "\n";
  }

  function zeigen(t) {
    feld.value = t;
    box.hidden = false;
  }

  function kopieren(t) {
    if (navigator.clipboard && window.isSecureContext) return navigator.clipboard.writeText(t);
    zeigen(t); feld.select();
    try { document.execCommand("copy"); return Promise.resolve(); } catch (e) { return Promise.reject(e); }
  }

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    var t = text(), body = encodeURIComponent(t);
    zeigen(t);
    if (body.length <= GRENZE) {
      location.href = "mailto:" + ADRESSE + "?subject=" + encodeURIComponent(BETREFF) + "&body=" + body;
      meldung.textContent = "Dein E-Mail-Programm sollte sich jetzt mit den Antworten öffnen. Bitte dort auf „Senden“ klicken.";
    } else {
      kopieren(t).then(function () {
        meldung.textContent = "Die Antworten sind lang und wurden deshalb kopiert. Im E-Mail-Programm, das sich jetzt öffnet, bitte mit Strg + V einfügen und senden.";
      }, function () {
        meldung.textContent = "Bitte den Text unten kopieren, im E-Mail-Programm einfügen und senden.";
      });
      location.href = "mailto:" + ADRESSE + "?subject=" + encodeURIComponent(BETREFF) + "&body=" + encodeURIComponent("(Antworten hier einfügen: Strg + V)\n");
    }
  });

  document.getElementById("fragebogen-kopieren").addEventListener("click", function () {
    var t = text();
    zeigen(t);
    kopieren(t).then(function () {
      meldung.textContent = "Kopiert. Füge den Text in eine E-Mail an " + ADRESSE + " ein.";
    }, function () {
      meldung.textContent = "Bitte den Text unten markieren und kopieren.";
    });
  });
})();

/*
 * Selector de idioma ES / EN para el sitio.
 *
 * El idioma nativo del sitio es el ESPAÑOL. Al pulsar "EN" se traduce la página
 * al inglés con el widget de traducción de Google (en cliente) y se muestra un
 * aviso de que es una traducción automática, con el correo del autor.
 *
 * Compatible con navigation.instant de Material: el código se re-ejecuta en cada
 * navegación a través del observable global `document$`.
 */
(function () {
  "use strict";

  var EMAIL = "fgg170708@proton.me";

  // --- utilidades de cookie / almacenamiento ---
  function setCookie(n, v) {
    document.cookie = n + "=" + v + ";path=/;SameSite=Lax";
    document.cookie = n + "=" + v + ";path=/;domain=" + location.hostname + ";SameSite=Lax";
  }
  function delCookie(n) {
    var past = ";expires=Thu, 01 Jan 1970 00:00:00 GMT";
    document.cookie = n + "=;path=/" + past;
    document.cookie = n + "=;path=/;domain=" + location.hostname + past;
  }
  function currentLang() {
    try { return localStorage.getItem("site-lang") || "es"; } catch (e) { return "es"; }
  }
  function storeLang(l) { try { localStorage.setItem("site-lang", l); } catch (e) {} }

  // --- widget de Google Translate (oculto; lo gobierna nuestro botón) ---
  function ensureWidget() {
    if (document.getElementById("google_translate_element")) return;
    var d = document.createElement("div");
    d.id = "google_translate_element";
    d.style.display = "none";
    document.body.appendChild(d);
    window.googleTranslateElementInit = function () {
      try {
        new google.translate.TranslateElement(
          { pageLanguage: "es", includedLanguages: "en", autoDisplay: false },
          "google_translate_element"
        );
      } catch (e) {}
    };
    var s = document.createElement("script");
    s.src = "https://translate.google.com/translate_a/element.js?cb=googleTranslateElementInit";
    s.async = true;
    document.body.appendChild(s);
  }
  // Fuerza la traducción manejando el <select> que crea el widget.
  function driveTranslate(to) {
    var tries = 0;
    (function attempt() {
      var sel = document.querySelector("select.goog-te-combo");
      if (sel) {
        sel.value = to === "en" ? "en" : "";
        sel.dispatchEvent(new Event("change"));
      } else if (tries++ < 60) {
        setTimeout(attempt, 150);
      }
    })();
  }

  // --- aviso (popup) de traducción automática ---
  function showDisclaimer() {
    if (document.getElementById("lang-modal")) return;
    var ov = document.createElement("div");
    ov.id = "lang-modal";
    ov.className = "lang-modal__overlay";
    ov.innerHTML =
      '<div class="lang-modal__box" role="dialog" aria-modal="true" aria-labelledby="lang-modal-title">' +
        '<h2 id="lang-modal-title" class="lang-modal__title">🌐 Automatic English translation</h2>' +
        '<p class="lang-modal__text">Sorry if some of the English on this site isn’t perfectly correct — it is an ' +
        '<strong>automatic translation</strong>. The author, <strong>Francisco Gutiérrez García</strong>, ' +
        'is a native <strong>Spanish</strong> speaker, so the original (and most accurate) version is the Spanish one.</p>' +
        '<p class="lang-modal__text">If anything is unclear or you have a question, feel free to email me at ' +
        '<a class="lang-modal__mail" href="mailto:' + EMAIL + '">' + EMAIL + '</a>.</p>' +
        '<button type="button" class="lang-modal__btn">Got it</button>' +
      '</div>';
    document.body.appendChild(ov);
    function close() { if (ov.parentNode) ov.parentNode.removeChild(ov); }
    ov.querySelector(".lang-modal__btn").addEventListener("click", close);
    ov.addEventListener("click", function (e) { if (e.target === ov) close(); });
    document.addEventListener("keydown", function esc(e) {
      if (e.key === "Escape") { close(); document.removeEventListener("keydown", esc); }
    });
  }

  // --- acciones del selector ---
  function goEnglish() {
    storeLang("en");
    setCookie("googtrans", "/es/en");
    showDisclaimer();
    ensureWidget();
    driveTranslate("en");
    syncToggle();
  }
  function goSpanish() {
    storeLang("es");
    delCookie("googtrans");
    location.reload(); // recarga limpia al idioma original
  }

  // --- botón ES/EN en la cabecera ---
  function buildToggle() {
    var header = document.querySelector(".md-header__inner");
    if (!header || header.querySelector(".lang-switch")) return;
    var wrap = document.createElement("div");
    wrap.className = "lang-switch";
    wrap.setAttribute("aria-label", "Idioma / Language");
    wrap.innerHTML =
      '<button type="button" data-lang="es" title="Español">ES</button>' +
      '<button type="button" data-lang="en" title="English">EN</button>';
    var opts = header.querySelector(".md-header__option") || header.querySelector('[data-md-component="palette"]');
    if (opts && opts.parentNode === header) header.insertBefore(wrap, opts);
    else header.appendChild(wrap);
    wrap.querySelector('[data-lang="es"]').addEventListener("click", function () {
      if (currentLang() !== "es") goSpanish();
    });
    wrap.querySelector('[data-lang="en"]').addEventListener("click", goEnglish);
    syncToggle();
  }
  function syncToggle() {
    var l = currentLang();
    var btns = document.querySelectorAll(".lang-switch [data-lang]");
    Array.prototype.forEach.call(btns, function (b) {
      b.classList.toggle("is-active", b.getAttribute("data-lang") === l);
    });
  }

  // --- ejecutar al cargar y en cada navegación instantánea ---
  function onPage() {
    buildToggle();
    if (currentLang() === "en") { ensureWidget(); driveTranslate("en"); }
  }

  if (window.document$ && typeof window.document$.subscribe === "function") {
    window.document$.subscribe(onPage);
  } else if (document.readyState !== "loading") {
    onPage();
  } else {
    document.addEventListener("DOMContentLoaded", onPage);
  }
})();

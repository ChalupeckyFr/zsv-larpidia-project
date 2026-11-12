(() => {
  "use strict";
  const PASSWORD_DIGEST = "04b366dd778be46b1d0be7acc19e13f1288c604b8a4e2d3e52acbe6f5ee82a9b";
  const SESSION_KEY = "larpidia-explorer:access:v1";
  const panel = document.querySelector("#access-panel");
  const form = document.querySelector("#access-form");
  const password = document.querySelector("#access-password");
  const toggle = document.querySelector("#access-toggle");
  const submit = document.querySelector("#access-submit");
  const status = document.querySelector("#access-status");
  const storageWarning = document.querySelector("#access-storage-warning");
  let resolveAccess;
  let checking = false;

  window.LarpidiaExplorerAccess = Object.freeze({
    ready: new Promise((resolve) => { resolveAccess = resolve; }),
  });

  function warnStorage() {
    storageWarning.textContent = "Prohlížeč nedovolil zapamatovat odemknutí. Hrát můžete dál, ale po obnovení stránky zadejte heslo znovu.";
    storageWarning.hidden = false;
  }

  function unlock(focus) {
    password.value = "";
    password.type = "password";
    panel.hidden = true;
    document.querySelector("#explorer-content").hidden = false;
    document.querySelector("#reset-game").hidden = false;
    resolveAccess();
    if (focus) document.querySelector("#intro-title").focus({ preventScroll: true });
  }

  function showError(message) {
    status.textContent = message;
    status.hidden = false;
  }

  toggle.addEventListener("click", () => {
    const visible = password.type === "password";
    password.type = visible ? "text" : "password";
    toggle.textContent = visible ? "Skrýt" : "Zobrazit";
    toggle.setAttribute("aria-pressed", String(visible));
  });
  password.addEventListener("input", () => {
    password.removeAttribute("aria-invalid");
    status.hidden = true;
  });
  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    if (checking) return;
    checking = true;
    submit.disabled = true;
    submit.textContent = "Ověřuji heslo…";
    status.hidden = true;
    password.removeAttribute("aria-invalid");
    try {
      if (!window.crypto?.subtle) {
        showError("Ověření hesla vyžaduje HTTPS nebo místní náhled na localhost. Otevřete zabezpečenou adresu webu.");
        return;
      }
      // The board shows the password in capitals; accept any letter case and stray spaces.
      const normalized = password.value.trim().toUpperCase();
      const digest = await window.crypto.subtle.digest("SHA-256", new TextEncoder().encode(normalized));
      const hex = Array.from(new Uint8Array(digest), (byte) => byte.toString(16).padStart(2, "0")).join("");
      if (hex !== PASSWORD_DIGEST) {
        showError("Heslo nesedí. Zkontrolujte heslo na tabuli a zkuste to znovu.");
        password.setAttribute("aria-invalid", "true");
        password.focus();
        return;
      }
      try { sessionStorage.setItem(SESSION_KEY, PASSWORD_DIGEST); }
      catch { warnStorage(); }
      unlock(true);
    } catch (error) {
      showError("Heslo se nepodařilo ověřit. Obnovte stránku a zkuste to znovu.");
      console.error("Larpidia Explorer access verification failed:", error);
    } finally {
      checking = false;
      submit.disabled = false;
      submit.textContent = "Odemknout expedici →";
    }
  });
  submit.disabled = false;

  try {
    if (sessionStorage.getItem(SESSION_KEY) === PASSWORD_DIGEST) unlock(false);
  } catch {
    warnStorage();
  }
})();

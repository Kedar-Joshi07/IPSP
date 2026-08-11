const STORAGE_KEY = "ipsp.theme";
const VALID_THEMES = new Set(["system", "dark", "light"]);

export function getStoredTheme() {
  try {
    const stored = window.localStorage.getItem(STORAGE_KEY);
    return VALID_THEMES.has(stored) ? stored : "system";
  } catch {
    return "system";
  }
}

export function resolveTheme(preference) {
  if (preference === "dark" || preference === "light") {
    return preference;
  }
  return window.matchMedia("(prefers-color-scheme: light)").matches ? "light" : "dark";
}

export function applyTheme(preference) {
  const resolved = resolveTheme(preference);
  document.documentElement.dataset.theme = resolved;
  const toggle = document.querySelector("#theme-toggle");
  if (toggle) {
    toggle.setAttribute("aria-pressed", String(resolved === "light"));
    toggle.setAttribute("title", `Using ${resolved} theme`);
  }
}

function persistTheme(preference) {
  try {
    window.localStorage.setItem(STORAGE_KEY, preference);
  } catch {
    // The visual theme still works when storage is unavailable.
  }
}

export function initTheme() {
  let preference = getStoredTheme();
  applyTheme(preference);

  const toggle = document.querySelector("#theme-toggle");
  toggle?.addEventListener("click", () => {
    const current = resolveTheme(preference);
    preference = current === "dark" ? "light" : "dark";
    persistTheme(preference);
    applyTheme(preference);
  });

  window.matchMedia("(prefers-color-scheme: light)").addEventListener("change", () => {
    if (preference === "system") {
      applyTheme(preference);
    }
  });
}

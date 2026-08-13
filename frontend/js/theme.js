const STORAGE_KEY = "ipsp.theme";
const VALID_THEMES = new Set(["system", "dark", "light"]);
let preference = "system";
let configuredDefault = "system";
let mediaQuery = null;

function storedPreference() {
  try {
    const stored = window.localStorage.getItem(STORAGE_KEY);
    return VALID_THEMES.has(stored) ? stored : null;
  } catch {
    return null;
  }
}

function resolveTheme(value) {
  if (value === "dark" || value === "light") return value;
  return mediaQuery?.matches ? "light" : "dark";
}

function updateControls() {
  document.querySelectorAll("[data-theme-control], #topbar-theme").forEach((control) => {
    control.value = preference;
  });
}

function apply() {
  document.documentElement.dataset.theme = resolveTheme(preference);
  updateControls();
}

export function getThemePreference() { return preference; }

export function setThemePreference(value) {
  if (!VALID_THEMES.has(value)) return;
  preference = value;
  try { window.localStorage.setItem(STORAGE_KEY, value); } catch { /* Visual selection remains active without storage. */ }
  apply();
}

export function bindThemeControl(control) {
  control.value = preference;
  control.addEventListener("change", () => setThemePreference(control.value));
}

export function initTheme(defaultTheme = "system") {
  configuredDefault = VALID_THEMES.has(defaultTheme) ? defaultTheme : "system";
  mediaQuery = window.matchMedia("(prefers-color-scheme: light)");
  preference = storedPreference() ?? configuredDefault;
  apply();
  mediaQuery.addEventListener("change", () => {
    if (preference === "system") apply();
  });
  const topbar = document.querySelector("#topbar-theme");
  if (topbar) bindThemeControl(topbar);
}

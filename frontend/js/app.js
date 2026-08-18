import { ApiError, getBrowserConfig, getCurrentUser, logout } from "./api.js";
import { permissionState } from "./components.js";
import { clearIdentity, getState, setApiInfo, setFlash, setIdentity, takeFlash } from "./state.js";
import { initTheme } from "./theme.js";
import { navigate, startRouter } from "./router.js";
import { renderJobs } from "./views/jobs.js";
import { renderLogin } from "./views/login.js";
import { renderNotFound } from "./views/not-found.js";
import { renderOverview } from "./views/overview.js";
import { renderProfile, renderRequiredPassword } from "./views/profile.js";
import { renderSystemHealth } from "./views/system-health.js";

const shell = document.querySelector("#app-root");
const main = document.querySelector("#main-content");
const contextLabel = document.querySelector("#page-context");
const identitySummary = document.querySelector("#identity-summary");
const logoutButton = document.querySelector("#logout-button");
const mobileMenu = document.querySelector("#mobile-menu-button");
const navigationScrim = document.querySelector("#navigation-scrim");
let loggingOut = false;
let router = null;

function safeError(error, fallback) {
  if (!(error instanceof ApiError)) return fallback;
  if (error.status >= 500 || error.status === 0) return `${fallback} (${error.code})`;
  return `${error.message} (${error.code})`;
}

function transitionAfterAuth(target) {
  if (!navigate(target)) router?.refresh();
}

function showLogin(message = null) {
  clearIdentity();
  if (message) setFlash("warning", message);
  transitionAfterAuth("#/login");
}

function handleAuthError(error) {
  if (error instanceof ApiError && error.status === 401) {
    showLogin("Your session has expired. Sign in again to continue.");
    return true;
  }
  return false;
}

function closeNavigation() {
  shell.dataset.navigationOpen = "false";
  mobileMenu.setAttribute("aria-expanded", "false");
}

async function performLogout() {
  if (loggingOut) return;
  loggingOut = true;
  logoutButton.disabled = true;
  try { await logout(); }
  catch (error) { if (!(error instanceof ApiError && error.status === 401)) setFlash("warning", "The server could not confirm logout. Local identity was cleared."); }
  finally { loggingOut = false; logoutButton.disabled = false; clearIdentity(); transitionAfterAuth("#/login"); }
}

function viewContext(lifecycle) {
  return {
    identity: getState().identity,
    apiInfo: getState().apiInfo,
    navigate,
    safeError,
    handleAuthError,
    permissionState,
    takeFlash,
    signal: lifecycle.signal,
    isActive: lifecycle.isCurrent,
    isRouteAbort: (error) => lifecycle.signal.aborted || error?.name === "AbortError",
    refresh: () => router?.refresh(),
    onAuthenticated: (identity) => {
      setIdentity(identity);
      identitySummary.textContent = identity.display_name;
      transitionAfterAuth(identity.must_change_password ? "#/profile" : "#/overview");
    },
    onPasswordChanged: () => {
      clearIdentity();
      setFlash("success", "Password changed successfully. Sign in again with your new password.");
      transitionAfterAuth("#/login");
    },
    onLogout: performLogout,
  };
}

function updateShell(route) {
  const identity = getState().identity;
  shell.dataset.mode = identity ? (identity.must_change_password ? "required-password" : "authenticated") : "login";
  identitySummary.textContent = identity?.display_name ?? "";
  contextLabel.textContent = route.title;
  document.title = `${route.title} · IPSP`;
  document.querySelectorAll("[data-route]").forEach((link) => {
    if (link.dataset.route === route.key) link.setAttribute("aria-current", "page");
    else link.removeAttribute("aria-current");
  });
  closeNavigation();
}

async function renderRoute(route, lifecycle) {
  const identity = getState().identity;
  if (!identity && route.key !== "login") { navigate("#/login"); return; }
  let cleanup;
  if (identity?.must_change_password) {
    updateShell({ key: "profile", title: "Password change required" });
    cleanup = renderRequiredPassword(main, viewContext(lifecycle));
  } else if (identity && route.key === "login") {
    navigate("#/overview");
    return;
  } else {
    updateShell(route);
    const context = viewContext(lifecycle);
    if (route.key === "login") cleanup = renderLogin(main, context);
    else if (route.key === "overview") cleanup = await renderOverview(main, context);
    else if (route.key === "jobs") cleanup = await renderJobs(main, context);
    else if (route.key === "profile") cleanup = renderProfile(main, context);
    else if (route.key === "admin-system") cleanup = await renderSystemHealth(main, context);
    else cleanup = renderNotFound(main, context);
  }
  if (!lifecycle.isCurrent()) return cleanup;
  const heading = main.querySelector("h1, h2");
  if (heading) { heading.setAttribute("tabindex", "-1"); heading.focus({ preventScroll: true }); }
  return cleanup;
}

async function bootstrap() {
  try {
    const apiInfo = await getBrowserConfig();
    setApiInfo(apiInfo);
    initTheme(apiInfo.browser.default_theme);
  } catch {
    initTheme("system");
    setFlash("danger", "Application configuration could not be loaded. Sign-in may be unavailable.");
  }
  try { setIdentity(await getCurrentUser()); }
  catch (error) { if (!(error instanceof ApiError && error.status === 401)) setFlash("warning", "The current session could not be checked safely."); }
  router = startRouter(renderRoute);
}

logoutButton.addEventListener("click", performLogout);
mobileMenu.addEventListener("click", () => {
  const open = shell.dataset.navigationOpen !== "true";
  shell.dataset.navigationOpen = String(open);
  mobileMenu.setAttribute("aria-expanded", String(open));
});
navigationScrim.addEventListener("click", closeNavigation);
document.querySelector("#primary-navigation").addEventListener("click", closeNavigation);
void bootstrap();

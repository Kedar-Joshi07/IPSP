import { changePassword } from "../api.js";
import { alertBox, card, pageHeader } from "../components.js";
import { bindThemeControl, getThemePreference } from "../theme.js";
import { button, clear, element, formatDate } from "../dom.js";

function detailList(identity) {
  const list = element("dl", { className: "detail-list" });
  const rows = [
    ["Display name", identity.display_name],
    ["Username", identity.username],
    ["Email", identity.email ?? "Not provided"],
    ["Role", identity.role_name],
    ["Session expires", formatDate(identity.session_expires_at)],
  ];
  for (const [label, value] of rows) list.append(element("dt", { text: label }), element("dd", {}, value));
  return list;
}

function passwordForm(context, required) {
  let active = true;
  const notices = element("div", { attributes: { "aria-live": "polite" } });
  const form = element("form", { className: "form", attributes: { autocomplete: "off" } });
  const current = element("input", { className: "form-control", id: "current-password", attributes: { type: "password", autocomplete: "current-password", required: "" } });
  const next = element("input", { className: "form-control", id: "new-password", attributes: { type: "password", autocomplete: "new-password", required: "" } });
  const confirm = element("input", { className: "form-control", id: "confirm-password", attributes: { type: "password", autocomplete: "new-password", required: "" } });
  const submit = button(required ? "Change password and sign in again" : "Change password", "button button--primary", "submit");
  form.append(
    element("div", { className: "form-group" }, [element("label", { text: "Current password", attributes: { for: "current-password" } }), current]),
    element("div", { className: "form-group" }, [element("label", { text: "New password", attributes: { for: "new-password" } }), next]),
    element("div", { className: "form-group" }, [element("label", { text: "Confirm new password", attributes: { for: "confirm-password" } }), confirm]),
    element("p", { className: "form-hint", text: "Password policy is validated securely by the server." }),
    submit,
  );
  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    notices.replaceChildren();
    if (next.value !== confirm.value) {
      notices.append(alertBox("The new password and confirmation do not match.", "danger"));
      confirm.focus();
      return;
    }
    submit.disabled = true;
    try {
      await changePassword(current.value, next.value, context.signal);
      if (!active || !context.isActive()) return;
      form.reset();
      context.onPasswordChanged();
    } catch (error) {
      if (context.isRouteAbort(error) || !active || !context.isActive()) return;
      if (context.handleAuthError(error)) return;
      notices.append(alertBox(context.safeError(error, "The password could not be changed."), "danger"));
      current.value = "";
      current.focus();
    } finally {
      if (active && context.isActive()) submit.disabled = false;
    }
  });
  return { node: element("div", {}, [notices, form]), cleanup: () => { active = false; form.reset(); }, focus: () => current.focus() };
}

export function renderRequiredPassword(container, context) {
  clear(container);
  container.append(pageHeader("Password change required", "Your account requires a password change before the workspace can be used."));
  const password = passwordForm(context, true);
  const signOut = button("Sign out", "button button--ghost");
  let active = true;
  signOut.addEventListener("click", async () => {
    if (signOut.disabled) return;
    signOut.disabled = true;
    try { await context.onLogout(); }
    finally { if (active && context.isActive()) signOut.disabled = false; }
  });
  container.append(card("Secure your account", element("div", {}, [password.node, element("div", { className: "action-row" }, signOut)]), { kicker: "Required action" }));
  container.setAttribute("aria-busy", "false");
  password.focus();
  return () => { active = false; password.cleanup(); };
}

export function renderProfile(container, context) {
  clear(container);
  const logoutAction = button("Logout", "button button--ghost");
  logoutAction.addEventListener("click", context.onLogout);
  container.append(pageHeader("Profile", "Current identity and session information returned by the authentication service.", [logoutAction]));
  const theme = element("select", { className: "theme-selector", attributes: { "data-theme-control": "", "aria-label": "Profile theme preference" } }, [element("option", { text: "System", attributes: { value: "system" } }), element("option", { text: "Dark", attributes: { value: "dark" } }), element("option", { text: "Light", attributes: { value: "light" } })]);
  theme.value = getThemePreference();
  bindThemeControl(theme);
  container.append(element("div", { className: "grid grid--2" }, [card("Identity and session", detailList(context.identity), { kicker: "Read only" }), card("Theme preference", element("div", { className: "form-group" }, [element("label", { text: "Color theme" }), theme, element("p", { className: "form-hint", text: "Stored locally as a visual preference only." })]), { kicker: "Appearance" })]));
  const password = passwordForm(context, false);
  container.append(card("Change password", password.node, { kicker: "Security" }));
  container.setAttribute("aria-busy", "false");
  return password.cleanup;
}

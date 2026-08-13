import { getReadiness, login } from "../api.js";
import { alertBox } from "../components.js";
import { button, clear, element } from "../dom.js";

export function renderLogin(container, context) {
  clear(container);
  const panel = element("section", { className: "card login-panel", attributes: { "aria-labelledby": "login-title" } });
  panel.append(element("div", { className: "brand" }, [element("span", { className: "brand__mark", text: "◇", attributes: { "aria-hidden": "true" } }), element("span", { text: "CampaignSim" }), element("span", { className: "brand__qualifier", text: "Powered by IPSP" })]));
  panel.append(element("h1", { id: "login-title", text: "Sign in to the platform" }));
  panel.append(element("p", { text: "Access the secure local foundation workspace." }));
  const notices = element("div", { attributes: { "aria-live": "polite" } });
  const flash = context.takeFlash();
  if (flash) notices.append(alertBox(flash.message, flash.kind));
  const form = element("form", { className: "form" });
  const username = element("input", { className: "form-control", id: "login-username", attributes: { name: "username", type: "text", autocomplete: "username", required: "", maxlength: "255" } });
  const password = element("input", { className: "form-control", id: "login-password", attributes: { name: "password", type: "password", autocomplete: "current-password", required: "" } });
  const submit = button("Sign in", "button button--primary", "submit");
  form.append(element("div", { className: "form-group" }, [element("label", { text: "Username", attributes: { for: "login-username" } }), username]));
  form.append(element("div", { className: "form-group" }, [element("label", { text: "Password", attributes: { for: "login-password" } }), password]));
  form.append(submit);
  panel.append(notices, form);
  const readiness = element("div", { className: "login-readiness", attributes: { role: "status" } }, [element("span", { className: "spinner", attributes: { "aria-hidden": "true" } }), element("span", { text: "Checking local readiness" })]);
  panel.append(readiness);
  container.append(panel);
  container.setAttribute("aria-busy", "false");

  let active = true;
  getReadiness(context.signal).then((result) => {
    if (!active || !context.isActive()) return;
    readiness.replaceChildren(element("span", { className: "status-dot", attributes: { "aria-hidden": "true" } }), element("span", { text: result.status === "ready" ? "Local service ready" : "Local service not ready" }));
  }).catch((error) => {
    if (active && context.isActive() && !context.isRouteAbort(error)) readiness.replaceChildren(element("span", { text: "Local readiness unavailable" }));
  });

  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    notices.replaceChildren();
    submit.disabled = true;
    submit.textContent = "Signing in…";
    try {
      const identity = await login(username.value, password.value, context.signal);
      if (!active || !context.isActive()) return;
      form.reset();
      context.onAuthenticated(identity);
    } catch (error) {
      if (context.isRouteAbort(error) || !active || !context.isActive()) return;
      password.value = "";
      notices.append(alertBox(context.safeError(error, "Sign-in failed. Check your credentials and try again."), "danger"));
      password.focus();
    } finally {
      if (active && context.isActive()) {
        submit.disabled = false;
        submit.textContent = "Sign in";
      }
    }
  });
  username.focus();
  return () => { active = false; form.reset(); };
}

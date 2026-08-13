import { emptyState } from "../components.js";
import { button, clear } from "../dom.js";

export function renderNotFound(container, context) {
  clear(container);
  const state = emptyState("Page not found", "The requested workspace route does not exist.", "?");
  const action = button("Return to overview", "button button--primary");
  action.addEventListener("click", () => context.navigate("#/overview"));
  state.append(action);
  container.append(state);
  container.setAttribute("aria-busy", "false");
  return () => {};
}

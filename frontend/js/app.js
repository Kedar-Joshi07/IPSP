import { getReadiness } from "./api.js";
import { initTheme } from "./theme.js";

function renderReady(payload) {
  const status = document.querySelector("#service-status");
  const badge = document.querySelector("#service-badge");
  if (!status || !badge) return;

  const checked = Object.keys(payload.checks ?? {}).length;
  const deferred = (payload.deferred_checks ?? []).length;
  status.innerHTML = `<span>Local API ready · ${checked} checks active · ${deferred} checks deferred honestly</span>`;
  badge.textContent = "Ready";
  badge.className = "badge badge--success";
}

function renderError() {
  const status = document.querySelector("#service-status");
  const badge = document.querySelector("#service-badge");
  if (!status || !badge) return;

  status.textContent = "The local API could not be reached. Start the development server and retry.";
  badge.textContent = "Unavailable";
  badge.className = "badge badge--danger";
}

async function bootstrap() {
  initTheme();
  try {
    renderReady(await getReadiness());
  } catch {
    renderError();
  }
}

void bootstrap();

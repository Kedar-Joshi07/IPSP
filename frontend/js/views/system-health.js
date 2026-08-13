import { getSystemHealth } from "../api.js";
import { badge, card, emptyState, errorState, loadingState, pageHeader } from "../components.js";
import { button, clear, element, formatBytes, formatDate, humanize } from "../dom.js";

const COMPONENT_STATES = new Set(["healthy", "degraded", "unhealthy", "not_configured", "not_implemented", "not_available", "not_initialized", "never_run"]);

function componentState(value) { return COMPONENT_STATES.has(value) ? value : "not_available"; }
function displayValue(value) {
  if (value === null || value === undefined) return "Unavailable";
  if (typeof value === "boolean") return value ? "Yes" : "No";
  return humanize(value);
}
function values(entries) {
  const grid = element("div", { className: "health-values" });
  for (const [label, value] of entries) grid.append(element("div", { className: "health-value" }, [element("span", { className: "health-value__label", text: label }), element("span", { className: "health-value__content" }, value instanceof Node ? value : displayValue(value))]));
  return grid;
}
function healthCard(title, status, entries) { return card(title, values(entries), { className: "health-group", trailing: badge(componentState(status)) }); }

function renderDiagnostics(container, health, refresh) {
  clear(container);
  const refreshButton = button("Refresh diagnostics", "button button--ghost");
  refreshButton.addEventListener("click", refresh);
  container.append(pageHeader("System Health", "Sanitized rich diagnostics returned by the permission-protected system health service.", [refreshButton]));
  container.append(element("section", { className: "grid grid--4", attributes: { "aria-label": "System health summary" } }, [
    healthCard("Overall", health.status, [["State", health.status], ["Checked", formatDate(health.timestamp_utc)]]),
    healthCard("Readiness", health.readiness.ready ? "healthy" : "unhealthy", [["Ready", health.readiness.ready], ["Error code", health.readiness.error_code], ["Active checks", Object.keys(health.readiness.checks).length], ["Deferred checks", health.readiness.deferred_checks.length]]),
    healthCard("SQLite", health.database.status, [["Connectivity", health.database.connectivity], ["Foreign keys", health.database.foreign_keys_enabled], ["Migration at head", health.database.migration_at_head], ["Integrity", health.database.integrity_status], ["Database size", formatBytes(health.database.database_size_bytes)]]),
    healthCard("Job worker", health.job_worker.status, [["Running", health.job_worker.running], ["Accepting jobs", health.job_worker.accepting_jobs], ["Workers", health.job_worker.worker_count], ["Runtime queue", health.job_worker.queue_depth], ["Persisted queued", health.job_worker.persisted_queued_jobs]]),
  ]));
  const storageCards = health.storage.map((item) => healthCard(`${humanize(item.name)} storage`, item.status, [["Display path", item.display_path], ["Required now", item.required_now], ["Exists", item.exists], ["Directory", item.is_directory], ["Readable", item.readable], ["Writable", item.writable], ["Free space", formatBytes(item.free_bytes)]]));
  container.append(element("section", { className: "health-stack" }, [card("Storage", element("div", { className: "health-grid" }, storageCards), { kicker: "Sanitized paths" })]));
  container.append(element("section", { className: "health-grid" }, [
    healthCard("Local LLM", health.local_llm.status, [["Feature enabled", health.local_llm.feature_enabled], ["Configured", health.local_llm.configured], ["Reachable", health.local_llm.reachable]]),
    healthCard("Remote LLM", health.remote_llm.status, [["Feature enabled", health.remote_llm.feature_enabled], ["Internet enabled", health.remote_llm.internet_enabled], ["Policy enabled", health.remote_llm.remote_llm_policy_enabled], ["Allowed providers", health.remote_llm.allowed_provider_count], ["Configured", health.remote_llm.configured], ["Reachability", health.remote_llm.reachability_status]]),
    card("Outbound policy", values([["Internet", health.outbound_policy.internet_enabled], ["Remote LLM", health.outbound_policy.remote_llm_enabled], ["Model downloads", health.outbound_policy.model_download_enabled], ["Update checks", health.outbound_policy.update_check_enabled], ["Default transmission", health.outbound_policy.default_remote_transmission], ["Allowed providers", health.outbound_policy.allowed_remote_provider_count]]), { className: "health-group", trailing: badge("Policy state", "info") }),
    healthCard("Model artifacts", health.model_artifacts.status, [["Storage accessible", health.model_artifacts.storage_accessible], ["Display path", health.model_artifacts.display_path]]),
    healthCard("Backup", health.backup.status === "succeeded" ? "healthy" : health.backup.status === "failed" ? "unhealthy" : health.backup.status === "running" || health.backup.status === "queued" ? "degraded" : "never_run", [["State", health.backup.status], ["Job ID", health.backup.job_id ? element("span", { className: "mono", text: health.backup.job_id }) : "Unavailable"], ["Updated", formatDate(health.backup.updated_at)], ["Finished", formatDate(health.backup.finished_at)], ["Error code", health.backup.error_code]]),
    card("Runtime", values([["Logical CPUs", health.runtime.logical_cpu_count], ["Process memory", formatBytes(health.runtime.process_memory_bytes)], ["Load average (1m)", health.runtime.load_average_1m]]), { className: "health-group", trailing: badge("Portable metrics", "info") }),
  ]));
  let criticalContent;
  if (health.recent_critical_errors.entries.length === 0) {
    criticalContent = emptyState("No recent critical errors", "The bounded critical error summary contains no entries.", "✓");
  } else {
    criticalContent = element("ul", { className: "critical-list" });
    for (const entry of health.recent_critical_errors.entries) criticalContent.append(element("li", {}, [element("strong", { text: `${humanize(entry.component)} · ${humanize(entry.action)}` }), element("div", { className: "mono", text: `${entry.error_code ?? "No code"} · ${entry.event_id}` }), element("div", {}, formatDate(entry.timestamp_utc))]));
  }
  container.append(card("Recent critical errors", criticalContent, { kicker: `Maximum ${health.recent_critical_errors.maximum_entries}`, trailing: badge(componentState(health.recent_critical_errors.status)) }));
}

export async function renderSystemHealth(container, context) {
  let loading = false;
  let disposed = false;
  const isActive = () => !disposed && context.isActive();
  const load = async () => {
    if (loading || !isActive()) return;
    loading = true;
    clear(container); container.append(loadingState("Loading system diagnostics")); container.setAttribute("aria-busy", "true");
    try { const health = await getSystemHealth(context.signal); if (isActive()) renderDiagnostics(container, health, load); }
    catch (error) {
      if (context.isRouteAbort(error) || !isActive()) return;
      if (context.handleAuthError(error)) return;
      clear(container);
      if (error?.status === 403) container.append(context.permissionState());
      else container.append(errorState("System diagnostics unavailable", context.safeError(error, "System diagnostics could not be loaded."), load));
    } finally { loading = false; if (isActive()) container.setAttribute("aria-busy", "false"); }
  };
  await load();
  return () => { disposed = true; };
}

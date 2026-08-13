import { getReadiness, listJobs } from "../api.js";
import { alertBox, badge, card, emptyState, errorState, loadingState, metricCard, pageHeader, progress } from "../components.js";
import { button, clear, element, formatDate, humanize } from "../dom.js";

function recentJobsCard(jobs, context) {
  if (jobs.length === 0) return card("Recent jobs", emptyState("No jobs yet", "No owner-visible jobs have been recorded for this account.", "≋"), { kicker: "Latest five" });
  const list = element("div", { className: "grid" });
  for (const job of jobs) {
    const item = element("article", { className: "card card--compact" }, [
      element("div", { className: "card__header" }, [element("div", {}, [element("h3", { text: humanize(job.job_type) }), element("p", { className: "mono", text: job.job_id })]), badge(job.status)]),
      progress(job.progress.percent, job.progress.message || job.progress.phase),
      element("p", { className: "metric-card__meta" }, ["Updated ", formatDate(job.updated_at)]),
    ]);
    list.append(item);
  }
  const open = button("Open all jobs", "button button--ghost");
  open.addEventListener("click", () => context.navigate("#/jobs"));
  return card("Recent jobs", element("div", {}, [list, element("div", { className: "action-row" }, open)]), { kicker: "Latest five" });
}

function capabilitiesCard() {
  const list = element("ul", { className: "roadmap-list" });
  for (const name of ["Secure server sessions", "Permission-based access", "Structured observability and audit", "Local persistent jobs", "Authorized system health"]) {
    list.append(element("li", {}, [element("span", { text: name }), badge("Implemented", "success")]));
  }
  return card("Implemented foundation capabilities", list, { kicker: "Available now" });
}

function roadmapCard() {
  const list = element("ul", { className: "roadmap-list" });
  for (const name of ["Projects and datasets", "Semantic discovery", "Model capabilities", "Simulation workspace"]) {
    list.append(element("li", {}, [element("span", { text: name }), badge("Not yet implemented", "neutral")]));
  }
  return card("Later milestones", list, { kicker: "Roadmap · disabled" });
}

export async function renderOverview(container, context) {
  let disposed = false;
  const isActive = () => !disposed && context.isActive();
  clear(container);
  container.append(loadingState("Loading platform overview"));
  container.setAttribute("aria-busy", "true");
  try {
    const [readiness, jobResult] = await Promise.all([getReadiness(context.signal), listJobs(5, 0, context.signal)]);
    if (!isActive()) return () => { disposed = true; };
    clear(container);
    const identity = context.identity;
    const activeChecks = Object.keys(readiness.checks ?? {}).length;
    const deferredChecks = (readiness.deferred_checks ?? []).length;
    container.append(pageHeader("Platform workspace", "A truthful view of the implemented IPSP foundation and your current server state."));
    const flash = context.takeFlash();
    if (flash) container.append(alertBox(flash.message, flash.kind));
    container.append(element("section", { className: "grid grid--4", attributes: { "aria-label": "Foundation metrics" } }, [
      metricCard("Platform status", humanize(readiness.status), "GET /health/ready"),
      metricCard("Active checks", String(activeChecks), "Current readiness dependencies"),
      metricCard("Deferred checks", String(deferredChecks), "Reported explicitly by readiness"),
      metricCard("Recent job records", String(jobResult.jobs.length), "Latest bounded list, not total history"),
    ]));
    const readinessBody = element("div", {}, [
      alertBox(readiness.status === "ready" ? "The platform foundation is ready to serve implemented operations." : "The platform reports that it is not ready.", readiness.status === "ready" ? "success" : "warning"),
      element("dl", { className: "detail-list" }, [
        element("dt", { text: "Active checks" }), element("dd", { text: Object.entries(readiness.checks ?? {}).map(([name, value]) => `${humanize(name)}: ${humanize(value)}`).join(" · ") || "None reported" }),
        element("dt", { text: "Deferred checks" }), element("dd", { text: (readiness.deferred_checks ?? []).map(humanize).join(" · ") || "None" }),
      ]),
    ]);
    const sessionBody = element("dl", { className: "detail-list" }, [
      element("dt", { text: "Display name" }), element("dd", { text: identity.display_name }),
      element("dt", { text: "Username" }), element("dd", { className: "mono", text: identity.username }),
      element("dt", { text: "Role" }), element("dd", { text: identity.role_name }),
      element("dt", { text: "Session expires" }), element("dd", {}, formatDate(identity.session_expires_at)),
      element("dt", { text: "Password change" }), element("dd", { text: identity.must_change_password ? "Required" : "Not required" }),
    ]);
    container.append(element("section", { className: "grid grid--2" }, [card("Platform readiness", readinessBody, { kicker: "Live foundation state", trailing: badge(readiness.status) }), card("Session", sessionBody, { kicker: "Current identity" })]));
    container.append(element("section", { className: "grid grid--2" }, [recentJobsCard(jobResult.jobs, context), element("div", { className: "grid" }, [capabilitiesCard(), roadmapCard()])]));
  } catch (error) {
    if (context.isRouteAbort(error) || !isActive()) return () => { disposed = true; };
    if (context.handleAuthError(error)) return;
    clear(container);
    container.append(errorState("Overview unavailable", context.safeError(error, "The platform overview could not be loaded."), () => context.refresh()));
  } finally {
    if (isActive()) container.setAttribute("aria-busy", "false");
  }
  return () => { disposed = true; };
}

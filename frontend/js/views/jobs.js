import { cancelJob, getJob, listJobs, retryJob } from "../api.js";
import { alertBox, badge, emptyState, errorState, loadingState, pageHeader, progress } from "../components.js";
import { button, clear, element, formatDate, humanize } from "../dom.js";

const JOB_STATUSES = new Set(["QUEUED", "RUNNING", "SUCCEEDED", "FAILED", "CANCELLED"]);

function canCancel(job) { return job.status === "QUEUED" || job.status === "RUNNING"; }
function canRetry(job) { return job.retryable === true && (job.status === "FAILED" || job.status === "CANCELLED"); }

function confirmationDialog(job, confirmAction) {
  const dialog = element("dialog", { attributes: { "aria-labelledby": "cancel-dialog-title" } });
  const cancel = button("Keep job", "button button--ghost");
  const confirm = button("Request cancellation", "button button--danger");
  dialog.append(element("div", { className: "dialog__body" }, [element("h2", { id: "cancel-dialog-title", text: "Cancel this job?" }), element("p", { text: "The server will apply its authoritative cancellation rules. Running work may stop cooperatively." }), element("p", { className: "mono", text: job.job_id })]), element("div", { className: "dialog__actions" }, [cancel, confirm]));
  cancel.addEventListener("click", () => dialog.close("keep"));
  confirm.addEventListener("click", () => { dialog.close("confirm"); confirmAction(); });
  dialog.addEventListener("close", () => dialog.remove(), { once: true });
  document.body.append(dialog);
  dialog.showModal();
  cancel.focus();
}

function detailPanel(job) {
  const content = element("dl", { className: "detail-list" });
  const entries = [
    ["Job ID", element("span", { className: "mono", text: job.job_id })],
    ["Type", humanize(job.job_type)], ["Status", badge(job.status)],
    ["Phase", job.progress.phase || "Unavailable"], ["Message", job.progress.message || "Unavailable"],
    ["Attempt", `${job.attempt_count} of ${job.max_attempts}`], ["Retryable", job.retryable ? "Yes" : "No"],
    ["Cancellation requested", job.cancel_requested ? "Yes" : "No"], ["Created", formatDate(job.created_at)],
    ["Queued", formatDate(job.queued_at)], ["Started", formatDate(job.started_at)], ["Finished", formatDate(job.finished_at)],
  ];
  for (const [label, value] of entries) content.append(element("dt", { text: label }), element("dd", {}, value));
  content.append(element("dt", { text: "Progress" }), element("dd", {}, progress(job.progress.percent, job.progress.message || job.progress.phase)));
  if (job.error) content.append(element("dt", { text: "Safe error" }), element("dd", {}, [element("span", { className: "mono", text: job.error.error_code }), document.createTextNode(` · ${job.error.message}`)]));
  const artifacts = element("ul", { className: "artifact-list" });
  for (const reference of job.artifact_refs) artifacts.append(element("li", { text: reference }));
  content.append(element("dt", { text: "Artifact references" }), element("dd", {}, job.artifact_refs.length ? artifacts : "None"));
  return element("section", { className: "card job-detail", attributes: { "aria-label": "Selected job details" } }, [element("div", { className: "card__header" }, [element("h2", { text: "Job details" }), badge(job.status)]), content]);
}

export async function renderJobs(container, context) {
  let jobs = [];
  let selected = null;
  let busyId = null;
  let disposed = false;
  let loading = false;

  const draw = () => {
    if (disposed) return;
    clear(container);
    const refresh = button("Refresh", "button button--ghost");
    refresh.addEventListener("click", load);
    container.append(pageHeader("Jobs", "Current owner-visible job records from the local persistent job service.", [refresh]));
    if (jobs.length === 0) { container.append(emptyState("No jobs found", "There are no owner-visible jobs for this account. Job submission is not available in this phase.", "≋")); return; }
    const table = element("table", { className: "data-table" });
    table.append(element("thead", {}, element("tr", {}, ["Job", "Status", "Progress", "Updated", "Attempt", "Actions"].map((name) => element("th", { text: name, attributes: { scope: "col" } })))));
    const body = element("tbody");
    for (const job of jobs) {
      const status = JOB_STATUSES.has(job.status) ? job.status : "FAILED";
      const actions = element("div", { className: "table-actions" });
      const view = button("View", "button button--ghost");
      view.disabled = busyId === job.job_id;
      view.addEventListener("click", () => loadDetail(job.job_id));
      actions.append(view);
      if (canCancel(job)) { const cancel = button("Cancel", "button button--danger"); cancel.disabled = busyId === job.job_id; cancel.addEventListener("click", () => confirmationDialog(job, () => mutate(job, "cancel"))); actions.append(cancel); }
      if (canRetry(job)) { const retry = button("Retry", "button button--ghost"); retry.disabled = busyId === job.job_id; retry.addEventListener("click", () => mutate(job, "retry")); actions.append(retry); }
      body.append(element("tr", {}, [
        element("td", {}, [element("strong", { text: humanize(job.job_type) }), element("div", { className: "mono", text: job.job_id })]),
        element("td", {}, badge(status)), element("td", {}, progress(job.progress.percent, job.progress.phase || job.progress.message)),
        element("td", {}, formatDate(job.updated_at)), element("td", { text: `${job.attempt_count}/${job.max_attempts}` }), element("td", {}, actions),
      ]));
    }
    table.append(body);
    container.append(element("div", { className: "table-wrapper" }, table));
    if (selected) container.append(detailPanel(selected));
  };

  const load = async () => {
    if (loading) return;
    loading = true;
    clear(container); container.append(loadingState("Loading jobs")); container.setAttribute("aria-busy", "true");
    try { const result = await listJobs(50, 0); jobs = result.jobs; selected = null; draw(); }
    catch (error) { if (context.handleAuthError(error)) return; clear(container); container.append(errorState("Jobs unavailable", context.safeError(error, "Jobs could not be loaded."), load)); }
    finally { loading = false; container.setAttribute("aria-busy", "false"); }
  };
  const loadDetail = async (jobId) => {
    busyId = jobId; draw();
    try { selected = await getJob(jobId); draw(); }
    catch (error) { if (context.handleAuthError(error)) return; selected = null; clear(container); container.append(errorState(error?.status === 404 ? "Job not found" : "Job unavailable", context.safeError(error, "The selected job could not be loaded."), load)); }
    finally { busyId = null; }
  };
  const mutate = async (job, action) => {
    busyId = job.job_id; draw();
    let mutationError = null;
    try { const updated = action === "cancel" ? await cancelJob(job.job_id) : await retryJob(job.job_id); jobs = jobs.map((item) => item.job_id === updated.job_id ? updated : item); selected = updated; }
    catch (error) { if (context.handleAuthError(error)) return; mutationError = error; }
    finally { busyId = null; }
    draw();
    if (mutationError) container.prepend(alertBox(context.safeError(mutationError, `The job ${action} request could not be completed.`), "danger"));
  };
  await load();
  return () => { disposed = true; document.querySelectorAll("dialog").forEach((dialog) => dialog.close()); };
}

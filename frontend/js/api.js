let browserConfig = null;

export class ApiError extends Error {
  constructor(status, code, message, recoverable = false) {
    super(message);
    this.name = "ApiError";
    this.status = status;
    this.code = code;
    this.recoverable = recoverable;
  }
}

function assertRelativePath(path) {
  if (typeof path !== "string" || !path.startsWith("/") || path.startsWith("//")) {
    throw new ApiError(0, "CLIENT-URL-INVALID", "The requested local resource is invalid.");
  }
  return path;
}

function getCookie(name) {
  const prefix = `${encodeURIComponent(name)}=`;
  const entry = document.cookie.split(";").map((item) => item.trim()).find((item) => item.startsWith(prefix));
  return entry ? decodeURIComponent(entry.slice(prefix.length)) : null;
}

async function parseResponse(response, allowedStatuses = []) {
  if (response.status === 204) return null;
  const contentType = response.headers.get("content-type") ?? "";
  if (!contentType.includes("application/json")) {
    if (!response.ok) throw new ApiError(response.status, "SYS-REQUEST-FAILED", "The request could not be completed.");
    return null;
  }
  let payload;
  try {
    payload = await response.json();
  } catch {
    throw new ApiError(response.status, "SYS-RESPONSE-INVALID", "The service returned an invalid response.");
  }
  if (!response.ok && !allowedStatuses.includes(response.status)) {
    const code = typeof payload?.error_code === "string" ? payload.error_code : "SYS-REQUEST-FAILED";
    const message = typeof payload?.message === "string" ? payload.message : "The request could not be completed.";
    throw new ApiError(response.status, code, message, payload?.recoverable === true);
  }
  return payload;
}

async function request(path, options = {}) {
  const method = options.method ?? "GET";
  const headers = { Accept: "application/json" };
  if (options.body !== undefined) headers["Content-Type"] = "application/json";
  if (options.csrf === true) {
    if (!browserConfig) throw new ApiError(0, "CLIENT-CONFIG-MISSING", "Browser security configuration is unavailable.");
    const csrfValue = getCookie(browserConfig.csrf_cookie_name);
    if (!csrfValue) throw new ApiError(403, "AUTHZ-CSRF_INVALID", "The secure request could not be verified.");
    headers[browserConfig.csrf_header_name] = csrfValue;
  }
  const response = await fetch(assertRelativePath(path), {
    method,
    credentials: "same-origin",
    headers,
    body: options.body === undefined ? undefined : JSON.stringify(options.body),
    signal: options.signal,
  });
  return parseResponse(response, options.allowedStatuses);
}

function isReadinessPayload(payload, responseStatus) {
  const expectedStatus = responseStatus === 200 ? "ready" : "not_ready";
  return payload !== null
    && typeof payload === "object"
    && payload.status === expectedStatus
    && typeof payload.timestamp_utc === "string"
    && !Number.isNaN(Date.parse(payload.timestamp_utc))
    && (payload.error_code === null || typeof payload.error_code === "string")
    && payload.checks !== null
    && typeof payload.checks === "object"
    && !Array.isArray(payload.checks)
    && Object.values(payload.checks).every((value) => typeof value === "string")
    && Array.isArray(payload.deferred_checks)
    && payload.deferred_checks.every((value) => typeof value === "string");
}

export async function getBrowserConfig() {
  const payload = await request("/api/v1");
  browserConfig = payload.browser;
  return payload;
}

export async function getReadiness(signal) {
  let response;
  try {
    response = await fetch(assertRelativePath("/health/ready"), {
      method: "GET",
      credentials: "same-origin",
      headers: { Accept: "application/json" },
      signal,
    });
  } catch (error) {
    if (error?.name === "AbortError") throw error;
    throw new ApiError(0, "SYS-REQUEST-FAILED", "Local readiness could not be checked.");
  }
  const payload = await parseResponse(response, [503]);
  if ((response.status !== 200 && response.status !== 503) || !isReadinessPayload(payload, response.status)) {
    throw new ApiError(response.status, "SYS-RESPONSE-INVALID", "The service returned an invalid readiness response.");
  }
  return payload;
}
export function login(username, password, signal) { return request("/api/v1/auth/login", { method: "POST", body: { username, password }, signal }); }
export function getCurrentUser(signal) { return request("/api/v1/auth/me", { signal }); }
export function logout() { return request("/api/v1/auth/logout", { method: "POST", csrf: true }); }
export function changePassword(currentPassword, newPassword, signal) { return request("/api/v1/auth/change-password", { method: "POST", csrf: true, body: { current_password: currentPassword, new_password: newPassword }, signal }); }
export function listJobs(limit = 50, offset = 0, signal) { return request(`/api/v1/jobs?limit=${encodeURIComponent(limit)}&offset=${encodeURIComponent(offset)}`, { signal }); }
export function getJob(jobId, signal) { return request(`/api/v1/jobs/${encodeURIComponent(jobId)}`, { signal }); }
export function cancelJob(jobId, signal) { return request(`/api/v1/jobs/${encodeURIComponent(jobId)}/cancel`, { method: "POST", csrf: true, signal }); }
export function retryJob(jobId, signal) { return request(`/api/v1/jobs/${encodeURIComponent(jobId)}/retry`, { method: "POST", csrf: true, signal }); }
export function getSystemHealth(signal) { return request("/api/v1/admin/system/health", { signal }); }

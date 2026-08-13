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

async function parseResponse(response) {
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
  if (!response.ok) {
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
  });
  return parseResponse(response);
}

export async function getBrowserConfig() {
  const payload = await request("/api/v1");
  browserConfig = payload.browser;
  return payload;
}

export function getReadiness() { return request("/health/ready"); }
export function login(username, password) { return request("/api/v1/auth/login", { method: "POST", body: { username, password } }); }
export function getCurrentUser() { return request("/api/v1/auth/me"); }
export function logout() { return request("/api/v1/auth/logout", { method: "POST", csrf: true }); }
export function changePassword(currentPassword, newPassword) { return request("/api/v1/auth/change-password", { method: "POST", csrf: true, body: { current_password: currentPassword, new_password: newPassword } }); }
export function listJobs(limit = 50, offset = 0) { return request(`/api/v1/jobs?limit=${encodeURIComponent(limit)}&offset=${encodeURIComponent(offset)}`); }
export function getJob(jobId) { return request(`/api/v1/jobs/${encodeURIComponent(jobId)}`); }
export function cancelJob(jobId) { return request(`/api/v1/jobs/${encodeURIComponent(jobId)}/cancel`, { method: "POST", csrf: true }); }
export function retryJob(jobId) { return request(`/api/v1/jobs/${encodeURIComponent(jobId)}/retry`, { method: "POST", csrf: true }); }
export function getSystemHealth() { return request("/api/v1/admin/system/health"); }

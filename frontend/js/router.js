const ROUTES = new Map([
  ["#/login", { key: "login", title: "Sign in" }],
  ["#/overview", { key: "overview", title: "Overview" }],
  ["#/jobs", { key: "jobs", title: "Jobs" }],
  ["#/profile", { key: "profile", title: "Profile" }],
  ["#/admin/system", { key: "admin-system", title: "System Health" }],
]);

function currentRoute() {
  const hash = window.location.hash || "#/overview";
  return ROUTES.get(hash) ?? { key: "not-found", title: "Page not found" };
}

export function navigate(path, replace = false) {
  const target = path.startsWith("#/") ? path : `#/${path}`;
  if (window.location.hash === target) return false;
  if (replace) window.location.replace(target);
  else window.location.hash = target;
  return true;
}

export function startRouter(onRoute) {
  let activeCleanup = null;
  let activeController = null;
  let generation = 0;
  let stopped = false;

  const once = (callback) => {
    let called = false;
    return () => {
      if (called) return;
      called = true;
      callback();
    };
  };

  const cleanupActiveRoute = () => {
    const cleanup = activeCleanup;
    activeCleanup = null;
    if (cleanup) cleanup();
  };

  const dispatch = async () => {
    const routeGeneration = ++generation;
    if (activeController) activeController.abort();
    activeController = new AbortController();
    const controller = activeController;
    cleanupActiveRoute();
    const route = currentRoute();
    let nextCleanup;
    try {
      nextCleanup = await onRoute(route, {
        signal: controller.signal,
        isCurrent: () => !stopped && generation === routeGeneration && !controller.signal.aborted,
      });
    } catch (error) {
      if (controller.signal.aborted || error?.name === "AbortError") return;
      throw error;
    }
    const cleanup = typeof nextCleanup === "function" ? once(nextCleanup) : null;
    if (stopped || generation !== routeGeneration || controller.signal.aborted) {
      if (cleanup) cleanup();
      return;
    }
    activeCleanup = cleanup;
  };
  const onHashChange = () => { void dispatch(); };
  window.addEventListener("hashchange", onHashChange);
  void dispatch();
  return {
    refresh: () => { if (!stopped) void dispatch(); },
    stop: () => {
      if (stopped) return;
      stopped = true;
      generation += 1;
      if (activeController) activeController.abort();
      cleanupActiveRoute();
      window.removeEventListener("hashchange", onHashChange);
    },
  };
}

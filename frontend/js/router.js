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
  if (replace) window.location.replace(target);
  else window.location.hash = target;
}

export function startRouter(onRoute) {
  let cleanup = () => {};
  const dispatch = async () => {
    cleanup();
    cleanup = () => {};
    const route = currentRoute();
    const nextCleanup = await onRoute(route);
    if (typeof nextCleanup === "function") cleanup = nextCleanup;
  };
  window.addEventListener("hashchange", dispatch);
  void dispatch();
  return () => {
    cleanup();
    window.removeEventListener("hashchange", dispatch);
  };
}

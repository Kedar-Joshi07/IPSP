export function element(tag, options = {}, children = []) {
  const node = document.createElement(tag);
  if (options.className) node.className = options.className;
  if (options.text !== undefined) node.textContent = String(options.text);
  if (options.id) node.id = options.id;
  for (const [name, value] of Object.entries(options.attributes ?? {})) {
    if (value !== null && value !== undefined) node.setAttribute(name, String(value));
  }
  const items = Array.isArray(children) ? children : [children];
  for (const child of items) {
    if (child instanceof Node) node.append(child);
    else if (child !== null && child !== undefined) node.append(document.createTextNode(String(child)));
  }
  return node;
}

export function clear(node) { node.replaceChildren(); }
export function button(label, className = "button", type = "button") { return element("button", { className, text: label, attributes: { type } }); }
export function formatDate(value) {
  if (!value) return "Unavailable";
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return "Unavailable";
  const time = element("time", { text: new Intl.DateTimeFormat(undefined, { dateStyle: "medium", timeStyle: "short" }).format(date), attributes: { datetime: date.toISOString(), title: date.toISOString() } });
  return time;
}
export function formatBytes(value) {
  if (!Number.isFinite(value) || value < 0) return "Unavailable";
  const units = ["B", "KiB", "MiB", "GiB", "TiB"];
  let amount = value;
  let index = 0;
  while (amount >= 1024 && index < units.length - 1) { amount /= 1024; index += 1; }
  return `${amount.toFixed(index === 0 ? 0 : 1)} ${units[index]}`;
}
export function humanize(value) { return String(value ?? "Unavailable").replaceAll("_", " ").replace(/\b\w/g, (letter) => letter.toUpperCase()); }

export async function getReadiness() {
  const response = await fetch("/health/ready", {
    headers: { Accept: "application/json" },
  });
  if (!response.ok) {
    throw new Error("The local service is not ready.");
  }
  return response.json();
}

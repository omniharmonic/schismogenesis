// Password gate for the private preview (any username; password in the PREVIEW_PASSWORD env var).
// Remove this file when Benjamin approves the public launch.
export const config = { matcher: "/(.*)" };

export default function middleware(request) {
  const expected = process.env.PREVIEW_PASSWORD;
  const header = request.headers.get("authorization") || "";
  const [scheme, value] = header.split(" ");
  if (expected && scheme === "Basic" && value) {
    const decoded = atob(value);
    if (decoded.slice(decoded.indexOf(":") + 1) === expected) return;
  }
  return new Response("This preview is private.", {
    status: 401,
    headers: { "WWW-Authenticate": 'Basic realm="anti-memes preview"' },
  });
}

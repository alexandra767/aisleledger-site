"""Writes support.html from the apps' shared help text, so the website says
exactly what the iPhone and Android apps say.

python3 scripts/build_support.py [path/to/help.json]   (default: the app repo's shared/help/help.json)
"""
import html, json, os, sys

HEAD = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>AisleLedger — Support</title>
<meta name="description" content="Help and contact for AisleLedger on iPhone and Android." />
<meta name="robots" content="index,follow" />
<style>
  body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", system-ui, sans-serif; margin: 0; padding: 48px 16px; color: #2b2f2c; background: #f7faf8; line-height: 1.6; }
  .container { max-width: 720px; margin: 0 auto; }
  h1 { color: #0f8a4f; }
  h2 { margin-top: 32px; color: #333; }
  h3 { margin-bottom: 4px; }
  a { color: #0f8a4f; }
  .meta { color: #777; font-size: 14px; }
  nav { margin-bottom: 24px; font-size: 15px; }
  nav a { margin-right: 16px; }
  ol li { margin-bottom: 8px; }
  @media (prefers-color-scheme: dark) {
    body { background: #121614; color: #e4e9e6; }
    h2 { color: #f0f3f1; } .meta { color: #9aa39e; }
    h1, a { color: #4fd18f; }
  }
</style>
</head>
<body><div class="container">
<nav><a href="index.html">AisleLedger</a><a href="privacy.html">Privacy</a><a href="terms.html">Terms</a><a href="support.html">Support</a></nav>
"""
PLATFORM = {"ios": "iPhone", "android": "Android"}


def e(s):
    return html.escape(s, quote=True)


def label(item):
    p = item.get("platform")
    return f" (on {PLATFORM[p]})" if p else ""


def render(help):
    c = help["contact"]
    out = [HEAD, "<h1>Support</h1>",
           f'<p>Email <a href="mailto:{e(c["email"])}?subject={e(c["subject"]).replace(" ", "%20")}">{e(c["email"])}</a>. '
           f'Put "AisleLedger" in the subject so we can find it fast. {e(c["note"])}</p>',
           '<p class="meta">The same help is in the app: Settings → Help &amp; Support (iPhone and Android).</p>',
           "<h2>Quick start</h2>", "<ol>"]
    out += [f"<li><strong>{e(s['title'])}.</strong> {e(s['detail'])}</li>" for s in help["quickStart"]]
    out += ["</ol>", "<h2>How it works</h2>"]
    for f in help["features"]:
        out += [f"<h3>{e(f['title'])}</h3>", f"<p>{e(f['body'])}</p>"]
    out += ["<h2>Subscription</h2>"]
    for s in help["subscription"]:
        out += [f"<h3>{e(s['title'])}{e(label(s))}</h3>", f"<p>{e(s['detail'])}</p>"]
    out += ["<h2>Questions</h2>"]
    for q in help["faq"]:
        out += [f"<h3>{e(q['q'])}{e(label(q))}</h3>", f"<p>{e(q['a'])}</p>"]
    out += ["<h2>Links</h2>", "<ul>"]
    out += [f'<li><a href="{e(l["url"])}">{e(l["title"])}</a></li>' for l in help["links"]]
    out += ["</ul>", "</div></body>", "</html>", ""]
    return "\n".join(out)


DEFAULT_HELP = os.path.expanduser("~/CodingProjects/aisleledger/shared/help/help.json")
SITE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    src = sys.argv[1] if len(sys.argv) > 1 else os.environ.get("HELP_JSON", DEFAULT_HELP)
    dest = os.path.join(SITE_DIR, "support.html")
    open(dest, "w").write(render(json.load(open(src))))
    print("wrote", dest)

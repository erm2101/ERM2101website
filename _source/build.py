#!/usr/bin/env python3
"""
Goal:    Compile the Jekyll source in this folder into plain static HTML that GoDaddy
         shared hosting can serve. GoDaddy runs Apache only, it does not run Jekyll,
         so the Liquid templates have to be rendered here rather than on the server.

Output:  Built .html pages plus all assets written to the repository root, which is
         exactly the set of files that gets uploaded to public_html.

Details: Front matter is stripped, the page body is rendered, then wrapped in
         _layouts/default.html. _config.yml becomes `site` and _data/*.yml becomes
         `site.data.*`, matching Jekyll. 404.html is generated from the same layout
         so it can never drift from the rest of the site. .htaccess is left alone.

         Jekyll's `{% include coauthors.html list=p.coauthors %}` is not standard
         Liquid, so the single include in this site is resolved by inlining its body
         with `include.list` rewritten to the caller's argument.

Usage:   pip install python-liquid pyyaml
         python3 _source/build.py
"""
import os, re, shutil, sys
import yaml
from liquid import Environment

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = HERE
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(HERE)

# Jekyll inputs and local clutter. None of this belongs on a public web server.
SKIP_DIRS = {"_layouts", "_includes", "_data", "_archive", ".git", ".stfolder",
             "_site", ".jekyll-cache", ".sass-cache", "__pycache__"}
SKIP_FILES = {"_config.yml", "README.md", ".gitignore", ".DS_Store", ".stignore",
              "CNAME", "Gemfile", "Gemfile.lock", "build.py"}

NOT_FOUND_BODY = '''\t\t\t<h2>Page Not Found</h2>
\t\t\t<p>That page does not exist. Use the links above, or go to the <a href="index.html">home page</a>.</p>
'''

with open(os.path.join(SRC, "_config.yml")) as f:
    site = yaml.safe_load(f) or {}
site["data"] = {
    os.path.splitext(n)[0]: yaml.safe_load(open(os.path.join(SRC, "_data", n)))
    for n in sorted(os.listdir(os.path.join(SRC, "_data")))
    if n.endswith((".yml", ".yaml"))
}

with open(os.path.join(SRC, "_includes", "coauthors.html")) as f:
    COAUTHORS = f.read().rstrip("\n")

INCLUDE_RE = re.compile(r"\{%-?\s*include\s+([\w.\-]+)\s+list=([\w.]+)\s*-?%\}")
FM_RE = re.compile(r"\A---\r?\n(.*?)\r?\n---\r?\n?", re.S)


def resolve_includes(text):
    def sub(m):
        if m.group(1) != "coauthors.html":
            raise SystemExit("unhandled include, add it to build.py: " + m.group(1))
        return COAUTHORS.replace("include.list", m.group(2))
    out = INCLUDE_RE.sub(sub, text)
    if re.search(r"\{%-?\s*include", out):
        raise SystemExit("an include survived resolution")
    return out


env = Environment(autoescape=False)
layouts = {os.path.splitext(n)[0]: open(os.path.join(SRC, "_layouts", n)).read()
           for n in os.listdir(os.path.join(SRC, "_layouts"))}


def render_page(body, layout_name, page):
    ctx = {"site": site, "page": page, "content": ""}
    rendered = env.from_string(resolve_includes(body)).render(**ctx)
    if layout_name:
        ctx["content"] = rendered
        rendered = env.from_string(layouts[layout_name]).render(**ctx)
    return rendered if rendered.endswith("\n") else rendered + "\n"


os.makedirs(OUT, exist_ok=True)
built, copied = [], []

for name in sorted(os.listdir(SRC)):
    path = os.path.join(SRC, name)
    if os.path.isdir(path):
        if name not in SKIP_DIRS:
            raise SystemExit("unexpected directory, decide about it explicitly: " + name)
        continue
    if name in SKIP_FILES:
        continue
    if name.endswith(".html"):
        raw = open(path).read()
        m = FM_RE.match(raw)
        if not m:
            shutil.copy2(path, os.path.join(OUT, name)); copied.append(name); continue
        fm = yaml.safe_load(m.group(1)) or {}
        html = render_page(raw[m.end():], fm.get("layout"), {"title": fm.get("title"), "url": "/" + name})
        open(os.path.join(OUT, name), "w").write(html)
        built.append(name)
    else:
        shutil.copy2(path, os.path.join(OUT, name)); copied.append(name)

# 404.html: same frame as every other page, with root-relative paths because Apache
# serves it while the browser URL stays on the missing (possibly nested) path.
nf = render_page(NOT_FOUND_BODY, "default", {"title": "Page Not Found", "url": "/404.html"})
nf = re.sub(r'(href|src)="([^"]+)"',
            lambda m: m.group(0) if re.match(r'^(https?:)?//|^mailto:|^#|^/', m.group(2))
            else f'{m.group(1)}="/{m.group(2)}"', nf)
open(os.path.join(OUT, "404.html"), "w").write(nf)
built.append("404.html")

print("built:  " + ", ".join(built))
print("copied: " + ", ".join(copied))
print("\nOutput written to " + OUT)
print("Upload everything there EXCEPT _source/ and README.md to public_html.")

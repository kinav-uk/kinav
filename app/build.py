"""Wrap page.html into index.html, the full page served when Kinav is hosted."""
import datetime
import hashlib
import os

HERE = os.path.dirname(os.path.abspath(__file__))
body = open(os.path.join(HERE, "page.html"), encoding="utf-8").read()
head_end = body.index("</style>") + len("</style>")
html = ("<!doctype html>\n<html lang=\"en-GB\">\n<head>\n<meta charset=\"utf-8\">\n"
        "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1, viewport-fit=cover\">\n"
        "<style>:root{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}"
        "body{margin:0}img{max-width:100%}[hidden]{display:none!important}</style>\n"
        + body[:head_end] + "\n</head>\n<body>\n" + body[head_end:] + "\n</body>\n</html>\n")
# The date this version was built; the app shows it, or the weekly care data date if that's newer.
today = datetime.date.today()
html = html.replace("BUILD_DATE_TEXT", today.strftime("%-d %B %Y")).replace("BUILD_DATE", today.isoformat())
# Stamp each script with a hash of its contents, so browsers never mix an old script with a new page.
for name in ("content.js", "app.js"):
    digest = hashlib.sha1(open(os.path.join(HERE, name), "rb").read()).hexdigest()[:10]
    html = html.replace('src="%s"' % name, 'src="%s?v=%s"' % (name, digest))
open(os.path.join(HERE, "index.html"), "w", encoding="utf-8").write(html)
print("Built index.html")

# Export the app's content for the search-friendly guide pages, then rebuild them and the sitemap.
# Needs JavaScriptCore (on every Mac); elsewhere the committed pages are left as they are.
JSC = "/System/Library/Frameworks/JavaScriptCore.framework/Versions/A/Helpers/jsc"
if os.path.exists(JSC):
    import subprocess
    import sys
    out = subprocess.run([JSC, "-e", "var window = {}; load(%r); print(JSON.stringify(window.KC));" % os.path.join(HERE, "content.js")],
                         check=True, capture_output=True, text=True).stdout
    update = os.path.join(os.path.dirname(HERE), "update")
    open(os.path.join(update, "content.json"), "w", encoding="utf-8").write(out)
    sys.path.insert(0, update)
    import build_guides
    import build_pages
    build_guides.main(today.strftime("%-d %B %Y"))
    print("Sitemap pages: %d" % build_pages.write_sitemap(HERE))

"""Wrap page.html into index.html, the full page served when Kinav is hosted."""
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
# Stamp each script with a hash of its contents, so browsers never mix an old script with a new page.
for name in ("content.js", "app.js"):
    digest = hashlib.sha1(open(os.path.join(HERE, name), "rb").read()).hexdigest()[:10]
    html = html.replace('src="%s"' % name, 'src="%s?v=%s"' % (name, digest))
open(os.path.join(HERE, "index.html"), "w", encoding="utf-8").write(html)
print("Built index.html")

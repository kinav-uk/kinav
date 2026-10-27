"""Make a Pinterest image (1000 x 1500, JPEG) for each guide, letter, plan and tool page that doesn't have one yet.

Run on a Mac with Chrome after adding pages: python3 -I update/make_pins.py
The images go in app/pins/, and build_guides lists them in app/pins.xml for Pinterest to pick up.
"""
import html
import os
import re
import subprocess
import tempfile

HOME = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APP = os.path.join(HOME, "app")
CHROME = os.environ.get("CHROME", os.path.expanduser("~/Desktop/Google Chrome.app/Contents/MacOS/Google Chrome"))
KINDS = [("guides", "Step-by-step guide"), ("letters", "Free letter template"), ("plans", "30-day plan for carers"), ("articles", "For carers")]
TOOLS = {"benefits-calculator": "Free tool", "care-cost-calculator": "Free tool", "will-they-have-to-sell-the-house-to-pay-for-care": "Paying for care",
         "ask-a-specialist": "Free helplines"}

TEMPLATE = """<!doctype html><html><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:wght@700;800&family=Inter:wght@500;600&display=block" rel="stylesheet">
<style>html,body{margin:0;width:1000px;height:1500px;overflow:hidden}
body{font-family:Inter,sans-serif;color:#fff;background:radial-gradient(circle at 85%% 10%%,#2a7493 0,#1f5f7a 45%%,#173f52 100%%);box-sizing:border-box;padding:90px 80px;display:flex;flex-direction:column}
.top{display:flex;align-items:center;gap:20px;font-family:"Bricolage Grotesque";font-weight:700;font-size:46px}
.top img{width:76px;height:76px;border-radius:18px}
main{flex:1;display:flex;flex-direction:column;justify-content:center}
.k{font-size:32px;font-weight:600;letter-spacing:3px;text-transform:uppercase;color:#f2c14e}
h1{font-family:"Bricolage Grotesque";font-weight:800;font-size:%(size)dpx;line-height:1.04;margin:28px 0 0;letter-spacing:-1.5px}
p{font-size:40px;line-height:1.35;margin:44px 0 0;opacity:.92}
.foot{display:flex;justify-content:space-between;align-items:center}
.url{background:#f2c14e;color:#18232e;font-family:"Bricolage Grotesque";font-weight:700;font-size:44px;padding:18px 46px;border-radius:999px}
.n{font-size:30px;opacity:.8}</style></head><body>
<div class="top"><img src="file://%(icon)s">Kinav</div><main><div class="k">%(kind)s</div><h1>%(title)s</h1><p>Free for families caring for an older parent in England.</p></main>
<div class="foot"><span class="url">kinav.co.uk</span><span class="n">No sign-up. No ads.</span></div></body></html>"""


def clean(title):
    title = re.sub(r"\s*\|\s*Kinav$", "", title)
    title = re.sub(r":\s*step-by-step checklist$|:\s*a 30-day plan for carers$|\s*\(free template, England\)$|:\s*free template$", "", title)
    return title


def pages():
    for folder, kind in KINDS:
        base = os.path.join(APP, folder)
        for slug in sorted(os.listdir(base)) if os.path.isdir(base) else []:
            if os.path.isfile(os.path.join(base, slug, "index.html")):
                yield slug, kind, os.path.join(base, slug, "index.html")
    for slug, kind in TOOLS.items():
        yield slug, kind, os.path.join(APP, slug, "index.html")


def main():
    made = 0
    for slug, kind, path in pages():
        out = os.path.join(APP, "pins", slug + ".jpg")
        if os.path.exists(out) or not os.path.exists(path):
            continue
        with open(path, encoding="utf-8") as f:
            title = clean(html.unescape(re.search(r"<title>(.*?)</title>", f.read()).group(1)))
        size = 104 if len(title) < 40 else 88 if len(title) < 70 else 74
        doc = TEMPLATE % {"title": html.escape(title), "kind": html.escape(kind), "size": size, "icon": os.path.join(APP, "apple-touch-icon.png")}
        with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8") as t:
            t.write(doc)
        subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=1", "--window-size=1000,1500",
                        "--allow-file-access-from-files", "--virtual-time-budget=5000", "--screenshot=" + out[:-4] + ".png", "file://" + t.name],
                       capture_output=True, timeout=60)
        os.unlink(t.name)
        # JPEG keeps each pin around 100 KB.
        subprocess.run(["sips", "-s", "format", "jpeg", "-s", "formatOptions", "80", out[:-4] + ".png", "--out", out], capture_output=True)
        os.unlink(out[:-4] + ".png")
        made += 1
    print("Pin images made: %d" % made)


if __name__ == "__main__":
    main()

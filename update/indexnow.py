"""Tell Bing and other IndexNow search engines about pages that are new or changed.

Run after each publish. Sends the pages changed in commits from the last 26 hours (the publish runs daily), or
every page in the sitemap if git history isn't available. Nothing is sent on days with no changes, because
re-sending the same pages every day makes search engines take less notice. IndexNow is free; the key file lives
at the site root.
"""
import json
import os
import re
import subprocess

HOME = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KEY = "49ded43f68a200536aa2b27e53028955"


def changed_pages(sitemap):
    """URLs of pages changed in the last 26 hours, or None if git can't tell."""
    out = subprocess.run(["git", "-C", HOME, "log", "--since=26 hours ago", "--name-only", "--pretty=format:"], capture_output=True, text=True)
    shallow = subprocess.run(["git", "-C", HOME, "rev-parse", "--is-shallow-repository"], capture_output=True, text=True).stdout.strip()
    if out.returncode or shallow == "true":
        return None
    paths = {"https://kinav.co.uk/" + f[len("app/"):-len("index.html")] for f in out.stdout.split() if f.startswith("app/") and f.endswith("index.html")}
    return [u for u in sitemap if u in paths]


def main():
    with open(os.path.join(HOME, "app", "sitemap.xml"), encoding="utf-8") as f:
        sitemap = re.findall(r"<loc>([^<]+)</loc>", f.read())
    urls = changed_pages(sitemap)
    if urls is None:
        urls = sitemap
    if not urls:
        print("IndexNow: no new or changed pages today")
        return
    body = json.dumps({"host": "kinav.co.uk", "key": KEY, "keyLocation": "https://kinav.co.uk/%s.txt" % KEY, "urlList": urls[:10000]})
    out = subprocess.run(["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}", "-X", "POST", "https://api.indexnow.org/indexnow",
                          "-H", "Content-Type: application/json; charset=utf-8", "-d", body], capture_output=True, text=True)
    print("IndexNow: %d pages sent, response %s" % (len(urls), out.stdout))


if __name__ == "__main__":
    main()

"""Tell Bing and other IndexNow search engines about every page in the sitemap.

Run after each publish. IndexNow is free; the key file lives at the site root.
"""
import json
import os
import re
import subprocess

HOME = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KEY = "49ded43f68a200536aa2b27e53028955"


def main():
    with open(os.path.join(HOME, "app", "sitemap.xml"), encoding="utf-8") as f:
        urls = re.findall(r"<loc>([^<]+)</loc>", f.read())
    body = json.dumps({"host": "kinav.co.uk", "key": KEY, "keyLocation": "https://kinav.co.uk/%s.txt" % KEY, "urlList": urls[:10000]})
    out = subprocess.run(["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}", "-X", "POST", "https://api.indexnow.org/indexnow",
                          "-H", "Content-Type: application/json; charset=utf-8", "-d", body], capture_output=True, text=True)
    print("IndexNow: %d pages sent, response %s" % (len(urls), out.stdout))


if __name__ == "__main__":
    main()

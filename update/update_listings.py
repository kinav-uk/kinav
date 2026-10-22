"""Weekly refresh of Kinav care listings from CQC open data.

Downloads the latest CQC care directory (weekly) and ratings file (monthly),
keeps every care home, nursing home and home care agency in England (any age
group) that CQC rates Good or Outstanding, and rewrites ~/Kincircle/care-listings-england.csv with CQC's published
fields only.
If anything fails, the existing spreadsheet is left untouched.
"""
import csv
import datetime
import json
import os
import re
import shutil
import sys
import subprocess
import tempfile
import xml.etree.ElementTree as ET
import zipfile

# The Kincircle folder: this script's parent, so it runs the same on a Mac or on GitHub.
HOME = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(HOME, "care-listings-england.csv")
STATE = os.path.join(HOME, "update", "state")
LOG = os.path.join(HOME, "update", "update.log")
PAGE = "https://www.cqc.org.uk/about-us/transparency/using-cqc-data"
UA = {"User-Agent": "Mozilla/5.0 (Kinav listings refresh)"}

SERVICE_TYPES = {"Nursing homes", "Residential homes", "Homecare agencies"}
LISTED = {"Outstanding", "Good"}
DOMAINS = ["Safe", "Effective", "Caring", "Responsive", "Well-led"]
COLUMNS = ["Name", "Also known as", "Address", "Postcode", "Phone number",
           "Service's website (if available)", "Service types", "Specialisms/services",
           "Provider name", "Local authority", "Region", "Date of latest check",
           "Overall rating"] + DOMAINS + ["Key questions below Good", "Rating published",
                                   "Service ratings", "Location URL"]

T = "{urn:oasis:names:tc:opendocument:xmlns:table:1.0}"
X = "{urn:oasis:names:tc:opendocument:xmlns:text:1.0}"


def log(msg):
    line = "%s  %s" % (datetime.datetime.now().strftime("%Y-%m-%d %H:%M"), msg)
    print(line)
    with open(LOG, "a") as f:
        f.write(line + "\n")


def fetch(url, dest=None):
    # curl uses the macOS certificate store; python.org builds of Python often don't.
    cmd = ["/usr/bin/curl", "-sSfL", "--max-time", "600", "-A", UA["User-Agent"], url]
    if dest is None:
        return subprocess.run(cmd, check=True, capture_output=True).stdout.decode("utf-8", "replace")
    subprocess.run(cmd + ["-o", dest], check=True, capture_output=True)


def find_link(page, pattern):
    links = re.findall(r'href="(https://www\.cqc\.org\.uk/system/files/[^"]+)"', page)
    for link in links:
        if re.search(pattern, link):
            return link
    raise RuntimeError("Could not find a link matching %s on the CQC page" % pattern)


def ods_cells(row):
    out = []
    for c in row:
        if c.tag not in (T + "table-cell", T + "covered-table-cell"):
            continue
        rep = int(c.get(T + "number-columns-repeated", "1"))
        txt = "".join("".join(p.itertext()) for p in c.findall(X + "p"))
        out += [txt] * min(rep, 30)
    return out


def parse_ratings(path):
    """Every published rating per CQC location: {location ID: {group: {domain: [rating, date]}}}.

    Group "Overall" holds the location's overall and key-question ratings; other
    groups (e.g. "Homecare", "Supported Living") are service-level ratings.
    """
    ratings, sheet = {}, None
    with zipfile.ZipFile(path) as z, z.open("content.xml") as f:
        for ev, el in ET.iterparse(f, events=("start", "end")):
            if ev == "start" and el.tag == T + "table":
                sheet = el.get(T + "name")
            elif ev == "end" and el.tag == T + "table-row":
                if sheet == "Locations":
                    c = ods_cells(el)
                    if len(c) > 20 and c[0].startswith("1-"):
                        ratings.setdefault(c[0], {}).setdefault(c[17], {})[c[18]] = [c[19], c[20]]
                el.clear()
            elif ev == "end" and el.tag == T + "table":
                el.clear()
                if sheet == "Locations":
                    break
    if len(ratings) < 10000:
        raise RuntimeError("Ratings file looked incomplete (%d locations)" % len(ratings))
    return ratings


def rating_columns(groups):
    overall = groups.get("Overall", {})
    out = [overall.get("Overall", ["", ""])[0]]
    out += [overall.get(d, ["", ""])[0] for d in DOMAINS]
    # Highlight, in CQC's own words, any key question rated below Good.
    out.append("; ".join("%s: %s" % (d, overall[d][0]) for d in DOMAINS
                         if overall.get(d, [""])[0] in ("Requires improvement", "Inadequate")))
    out.append(overall.get("Overall", ["", ""])[1])
    services = ["%s: %s" % (g, v["Overall"][0]) for g, v in sorted(groups.items())
                if g != "Overall" and "Overall" in v]
    out.append("; ".join(services))
    return out


def load_ratings(page, tmp):
    url = find_link(page, r"Latest_ratings\.ods$")
    cache = os.path.join(STATE, "ratings.json")
    if os.path.exists(cache):
        with open(cache) as f:
            saved = json.load(f)
        if saved.get("url") == url and saved.get("format") == 2:
            return saved["ratings"], url
    path = os.path.join(tmp, "ratings.ods")
    fetch(url, path)
    ratings = parse_ratings(path)
    with open(cache, "w") as f:
        json.dump({"url": url, "format": 2, "ratings": ratings}, f)
    log("New ratings file: %s" % url.rsplit("/", 1)[-1])
    return ratings, url


def build(directory_path, ratings):
    with open(directory_path, encoding="utf-8-sig") as f:
        rows = list(csv.reader(f))
    header_at = next(i for i, r in enumerate(rows) if r and r[0] == "Name")
    out = []
    for r in rows[header_at + 1:]:
        if len(r) < 15:
            continue
        name, aka, addr, pc, phone, web, types, check, spec, prov, la, region, url, lid, _ = r[:15]
        if not SERVICE_TYPES & set(types.split("|")):
            continue
        groups = ratings.get(lid, {})
        # Only list services CQC rates Good or Outstanding: the location's overall
        # rating, or, where CQC rates per service instead, every service rating.
        overall = groups.get("Overall", {}).get("Overall", [""])[0]
        services = [v["Overall"][0] for g, v in groups.items() if g != "Overall" and "Overall" in v]
        if overall in LISTED:
            pass
        elif overall == "Not Rated" and services and all(r in LISTED for r in services):
            pass
        else:
            continue
        out.append([name, aka, addr, pc, phone, web, types.replace("|", "; "),
                    spec.replace("|", "; "), prov, la, region,
                    check.replace(" - 00:00", "")] + rating_columns(groups) + [url])
    if len(out) < 12000:
        raise RuntimeError("Only %d listings found; expected about 19,000" % len(out))
    out.sort(key=lambda x: (x[10], x[9], x[0]))
    return out


def main():
    os.makedirs(STATE, exist_ok=True)
    tmp = tempfile.mkdtemp(prefix="kinav-cqc-")
    try:
        page = fetch(PAGE)
        dir_url = find_link(page, r"CQC_directory\.csv$")
        dir_path = os.path.join(tmp, "directory.csv")
        fetch(dir_url, dir_path)
        ratings, _ = load_ratings(page, tmp)
        rows = build(dir_path, ratings)
        part = OUT + ".new"
        with open(part, "w", newline="", encoding="utf-8-sig") as f:
            w = csv.writer(f)
            w.writerow(COLUMNS)
            w.writerows(rows)
        os.replace(part, OUT)
        log("Updated %d listings from %s" % (len(rows), dir_url.rsplit("/", 1)[-1]))
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        import build_app_data
        build_app_data.main()
    except Exception as e:
        log("FAILED, spreadsheet left unchanged: %s" % e)
        sys.exit(1)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    main()

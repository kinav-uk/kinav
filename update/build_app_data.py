"""Turn the CQC listings spreadsheet into small JSON files for the Kinav app.

Writes ~/Kincircle/app/data/index.json (councils + postcode districts) and one
file per council in ~/Kincircle/app/data/la/, so the app only loads the area
the family searches for.
"""
import collections
import csv
import datetime
import json
import os
import re
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import postcodes  # noqa: E402

# The Kincircle folder: this script's parent, so it runs the same on a Mac or on GitHub.
HOME = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(HOME, "care-listings-england.csv")
OUT = os.path.join(HOME, "app", "data")
DOMAINS = ["Safe", "Effective", "Caring", "Responsive", "Well-led"]
CODE = {"Outstanding": "O", "Good": "G", "Requires improvement": "R", "Inadequate": "I"}


def slug(name):
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-") or "unknown"


def phone(p):
    # CQC's file drops the leading zero from UK numbers.
    p = re.sub(r"\D", "", p or "")
    return ("0" + p) if p and not p.startswith("0") else p


def types(s):
    t = ""
    if "Homecare agencies" in s:
        t += "H"
    if "Nursing homes" in s:
        t += "N"
    if "Residential homes" in s:
        t += "R"
    return t


def where(pc, coords, centres):
    # Exact postcode if Code-Point has it, else the district centre, else unknown.
    pc = " ".join((pc or "").upper().split())
    if pc in coords:
        return coords[pc]
    district = centres.get(pc.split(" ")[0]) if pc else None
    return tuple(district) if district else (None, None)


# CQC "Specialisms/services" wording -> one-letter codes used by the app
SPECIALISMS = [
    ("Dementia", "D"), ("Physical disabilities", "P"), ("Sensory impairments", "S"),
    ("Learning disabilities", "L"), ("Mental health conditions", "M"),
    ("Substance misuse problems", "X"), ("Eating disorders", "E"),
    ("Caring for adults over 65 yrs", "O"), ("Caring for adults under 65 yrs", "U"),
    ("Caring for children", "C"), ("Services for everyone", "A"),
]


def main(codepoint_zip=None):
    with open(SRC, encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))
    tmp = OUT + ".new"
    shutil.rmtree(tmp, ignore_errors=True)
    os.makedirs(os.path.join(tmp, "la"))
    # Postcode locations for distance search; if the download fails, keep last week's.
    try:
        coords = postcodes.load(codepoint_zip or postcodes.download())
        centres = postcodes.write(coords, os.path.join(tmp, "pc"))
    except Exception as e:
        print("Postcode locations not updated: %s" % e)
        coords, centres = {}, {}
        if os.path.isdir(os.path.join(OUT, "pc")):
            shutil.copytree(os.path.join(OUT, "pc"), os.path.join(tmp, "pc"))
            try:
                with open(os.path.join(OUT, "index.json")) as f:
                    centres = json.load(f).get("dc", {})
            except (OSError, ValueError):
                pass
    by_la = collections.defaultdict(list)
    districts = collections.defaultdict(collections.Counter)
    for r in rows:
        la = r["Local authority"] or "Unknown"
        spec = r["Specialisms/services"]
        by_la[la].append([
            r["Name"], r["Address"].replace(",", ", "), r["Postcode"], phone(r["Phone number"]),
            r["Service's website (if available)"], types(r["Service types"]),
            1 if "Dementia" in spec else 0, 1 if "Caring for adults over 65 yrs" in spec else 0,
            r["Overall rating"], "".join(CODE.get(r[d], "-") for d in DOMAINS),
            r["Rating published"], r["Service ratings"], r["Location URL"].rsplit("/", 1)[-1],
            "".join(c for name, c in SPECIALISMS if name in spec),
        ] + list(where(r["Postcode"], coords, centres)))
        out_code = r["Postcode"].strip().upper().split(" ")[0]
        if out_code:
            districts[out_code][la] += 1

    councils = []
    for la, items in sorted(by_la.items()):
        s = slug(la)
        items.sort(key=lambda x: ({"Outstanding": 0, "Good": 1}.get(x[8], 2), x[0].lower()))
        with open(os.path.join(tmp, "la", s + ".json"), "w") as f:
            json.dump(items, f, separators=(",", ":"))
        council = {"n": la, "s": s, "c": len(items)}
        placed = [x for x in items if x[14] is not None]
        if placed:
            es, ns = [x[14] for x in placed], [x[15] for x in placed]
            council["b"] = [min(es), min(ns), max(es), max(ns)]
        councils.append(council)
    index = {
        "updated": datetime.date.today().strftime("%-d %B %Y"),
        "councils": councils,
        "districts": {d: slug(c.most_common(1)[0][0]) for d, c in districts.items()},
        "dc": centres,
    }
    with open(os.path.join(tmp, "index.json"), "w") as f:
        json.dump(index, f, separators=(",", ":"))
    shutil.rmtree(OUT, ignore_errors=True)
    os.replace(tmp, OUT)
    print("App data: %d councils, %d listings" % (len(councils), len(rows)))


if __name__ == "__main__":
    main()

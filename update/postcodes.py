"""Postcode locations for distance search, from Ordnance Survey Code-Point Open.

Code-Point Open is free open data (Contains OS data, Royal Mail data and National
Statistics data, Crown copyright and database right). We keep England only and
round each location to the nearest 100 metres, which is plenty for "within 2 miles".

The app looks up a postcode by fetching just that district's file, for example
data/pc/BR1.json, so the postcode a family types never leaves their phone.
"""
import collections
import csv
import io
import json
import os
import subprocess
import tempfile
import zipfile

URL = "https://api.os.uk/downloads/v1/products/CodePointOpen/downloads?area=GB&format=CSV&redirect"
ENGLAND = "E92000001"


def download():
    tmp = tempfile.mkdtemp(prefix="kinav-codepoint-")
    path = os.path.join(tmp, "codepo_gb.zip")
    subprocess.run(["/usr/bin/curl", "-sSfL", "--max-time", "600", "-o", path, URL], check=True)
    return path


def load(zip_path):
    """Return {"BR1 3AA": (east, north)} in hectometres (100 m units)."""
    coords = {}
    with zipfile.ZipFile(zip_path) as z:
        for name in z.namelist():
            if not (name.startswith("Data/CSV/") and name.endswith(".csv")):
                continue
            with z.open(name) as f:
                for row in csv.reader(io.TextIOWrapper(f, encoding="utf-8")):
                    pc, east, north, country = row[0], row[2], row[3], row[4]
                    if country != ENGLAND or east in ("", "0"):
                        continue
                    pc = " ".join(pc.split())
                    if " " not in pc:
                        pc = pc[:-3] + " " + pc[-3:]
                    coords[pc] = (round(int(east) / 100), round(int(north) / 100))
    return coords


def write(coords, out_dir):
    """One file per postcode district, plus district centres for outward-only searches."""
    by_district = collections.defaultdict(dict)
    for pc, en in coords.items():
        outward, inward = pc.split(" ")
        by_district[outward][inward] = en
    os.makedirs(out_dir, exist_ok=True)
    centres = {}
    for outward, items in by_district.items():
        with open(os.path.join(out_dir, outward + ".json"), "w") as f:
            json.dump(dict(sorted(items.items())), f, separators=(",", ":"))
        n = len(items)
        centres[outward] = [round(sum(e for e, _ in items.values()) / n), round(sum(n_ for _, n_ in items.values()) / n)]
    return centres

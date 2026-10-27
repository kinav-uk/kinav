"""Readable web pages for every council area, so search engines can find Kinav.

Writes ~/Kincircle/app/care/ (an England index, then per council an overview and
pages for care at home, nursing homes, residential homes and dementia care),
plus sitemap.xml and robots.txt. Built from the same rows as the app's data.
"""
import collections
import datetime
import html
import os
import re
import shutil

SITE = "https://kinav.co.uk"
TYPES = [  # (code, page slug, plural, singular)
    ("H", "care-at-home", "Care at home services", "Care at home"),
    ("N", "nursing-homes", "Nursing homes", "Nursing home"),
    ("R", "residential-homes", "Residential care homes", "Residential home"),
]
KQ = ["Safe", "Effective", "Caring", "Responsive", "Well-led"]
KQ_WORD = {"O": "Outstanding", "G": "Good", "R": "Requires improvement", "I": "Inadequate", "-": "Not rated"}
SPEC_WORD = {"D": "Dementia", "P": "Physical disabilities", "S": "Sensory impairments", "L": "Learning disabilities",
             "M": "Mental health", "X": "Substance misuse", "E": "Eating disorders"}
AGE_WORD = {"O": "over 65s", "U": "adults under 65", "C": "children", "A": "everyone"}
MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
LOGO = ('<svg viewBox="0 0 512 512" aria-hidden="true"><rect width="512" height="512" rx="112" fill="#1f5f7a"/>'
        '<circle cx="256" cy="256" r="140" fill="none" stroke="#f2c14e" stroke-width="40"/><circle cx="256" cy="116" r="38" fill="#ffffff"/>'
        '<circle cx="377" cy="326" r="38" fill="#ffffff"/><circle cx="135" cy="326" r="38" fill="#ffffff"/></svg>')
CREDIT = ("Contains CQC data. Contains OS data © Crown copyright and database right {y}. "
          "Contains Royal Mail data © Royal Mail copyright and database right {y}.")

CARE_FOOTER = """<p>We only list care services rated Good or Outstanding by CQC. Services rated Requires improvement or Inadequate are left out. Details and ratings are as CQC publishes them, updated every week. Last updated {updated}.</p>
  <p>Kinav gives general information only, not medical, legal or financial advice, and doesn't recommend or inspect care services. A specialism listed by CQC doesn't mean a service suits the person's needs. Always visit, read the full CQC report and ask the council for a needs assessment. For health questions, speak to the GP, a pharmacist or NHS 111. In an emergency, call 999.</p>
  <p>{credit}</p>"""
GUIDE_FOOTER = """<p>Kinav gives general information about care in England. It doesn't give health, medical, legal or financial advice. For health questions, speak to the GP, a pharmacist or NHS 111. In an emergency, call 999. Last updated {updated}.</p>"""

e = html.escape


def rated(d):
    p = (d or "").split("/")
    return "%s %s" % (MONTHS[int(p[1]) - 1], p[2]) if len(p) == 3 else ""


def page(path, title, description, body, updated, kind="care"):
    """A full HTML page. `path` is the URL path, e.g. /care/bromley/."""
    return """<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{site}{path}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{site}{path}">
<meta property="og:image" content="{site}/og-image.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#1f5f7a">
<link rel="icon" href="/icon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="stylesheet" href="/site.css">
</head>
<body>
<div class="page">
<header class="top">
  <a class="brand" href="/" aria-label="Kinav home">{logo}<b>Kinav</b></a>
  <a class="btn btn-ghost" href="/#care">Search by postcode</a>
</header>
{body}
<footer class="tiny muted">
  {footer}
  <p><a href="/">Kinav app</a> · <a href="/care/">Care by area</a> · <a href="/guides/">Guides</a> · <a href="/ask-a-specialist/">Ask a specialist</a> · <a href="/#privacy">Privacy</a> · <a href="/#terms">Terms</a></p>
  <p>Follow us on <a href="https://www.instagram.com/ukkinav/" rel="noopener">Instagram</a> and <a href="https://www.facebook.com/kinavhelp" rel="noopener">Facebook</a></p>
  <p>© {y} Kinav</p>
</footer>
</div>
<script data-goatcounter="https://kinav.goatcounter.com/count" async src="https://gc.zgo.at/count.js"></script>
</body>
</html>
""".format(title=e(title), desc=e(description), site=SITE, path=path, logo=LOGO, body=body,
           footer=(CARE_FOOTER if kind == "care" else GUIDE_FOOTER).format(updated=e(updated), credit=CREDIT.format(y=datetime.date.today().year)),
           y=datetime.date.today().year)


def card(r, show_type):
    name, addr, pc, phone, web, types, overall, kq, date, svc, loc = r[0], r[1], r[2], r[3], r[4], r[5], r[8], r[9], r[10], r[11], r[12]
    spec = r[13] or ""
    lows = ["%s as %s" % (KQ[i], KQ_WORD[k]) for i, k in enumerate(kq) if k in "RI"]
    if overall == "Not Rated":
        badge, pill = "CQC: rated per service", "pill pill-quiet"
        ratings = '<p class="small">%s</p>' % e(svc)
    else:
        badge, pill = "CQC: %s%s" % (overall, " · " + rated(date) if rated(date) else ""), "pill"
        cells = []
        for i, k in enumerate(kq):
            cls = {"O": "o", "G": "", "R": "r", "I": "i", "-": "n"}[k]
            word = "Req. improv." if k == "R" else KQ_WORD[k]
            cells.append('<div class="%s"><span>%s</span><b>%s</b></div>' % (cls, KQ[i], word))
        ratings = '<div class="kq">%s</div>' % "".join(cells)
    tags = "".join('<span class="tag%s">%s</span>' % (" tag-hi" if c == "D" else "", SPEC_WORD[c]) for c in spec if c in SPEC_WORD)
    ages = [AGE_WORD[c] for c in spec if c in AGE_WORD]
    kinds = " · ".join(t[3] for t in TYPES if t[0] in types)
    site = web if web.lower().startswith("http") else ("https://" + web if web else "")
    out = ['<article class="card">',
           '<div class="head"><div><h3>%s</h3>%s</div><span class="%s">%s</span></div>' % (
               e(name), '<p class="small muted">%s</p>' % e(kinds) if show_type else "", pill, e(badge)),
           '<p class="small">%s %s</p>' % (e(addr), e(pc))]
    if lows:
        out.append('<p class="warn">Good overall, but CQC rated %s. Read the CQC report before choosing.</p>' % e(" and ".join(lows)))
    out.append(ratings)
    if tags or ages:
        out.append('<div class="stack-sm"><p class="tiny muted">Specialist care (as listed by CQC)</p>%s%s</div>' % (
            '<div class="spec">%s</div>' % tags if tags else "",
            '<p class="tiny muted">Cares for: %s</p>' % e(", ".join(ages)) if ages else ""))
    links = []
    if phone:
        links.append('<a href="tel:%s">Call %s</a>' % (e(phone), e(phone)))
    if site:
        links.append('<a href="%s" rel="nofollow noopener" target="_blank">Website</a>' % e(site))
    links.append('<a href="https://www.cqc.org.uk/location/%s" rel="noopener" target="_blank">CQC report</a>' % e(loc))
    out.append('<p class="links">%s</p>' % "".join(links))
    out.append("</article>")
    return "".join(out)


def tabs(slug, current, counts):
    items = [("", "Overview")] + [(t[1], t[3]) for t in TYPES] + [("dementia-care", "Dementia care")]
    out = []
    for path, label in items:
        n = counts.get(path)
        text = label + (" (%d)" % n if n is not None else "")
        cur = ' aria-current="page"' if path == current else ""
        out.append('<a href="/care/%s/%s"%s>%s</a>' % (slug, path + "/" if path else "", cur, e(text)))
    return '<nav class="tabs" aria-label="Type of care">%s</nav>' % "".join(out)


def crumbs(region, council=None, slug=None):
    parts = ['<a href="/care/">England</a>', '<a href="/care/#%s">%s</a>' % (e(region_id(region)), e(region))]
    if council:
        parts.append('<a href="/care/%s/">%s</a>' % (slug, e(council)))
    return '<nav class="crumbs" aria-label="Breadcrumb">%s</nav>' % " › ".join(parts)


def region_id(region):
    return "".join(c if c.isalnum() else "-" for c in region.lower()).strip("-")


def cta(council):
    return ('<div class="cta"><p><b>Search by miles from a postcode</b>, filter by specialist care and work out care costs in the free Kinav app for families.</p>'
            '<a class="btn" href="/#care">Open Kinav</a></div>')


def paying(council):
    return ('<section class="panel"><h2>Paying for care in %s</h2>'
            '<p>In England, the council may help pay for care if the person has less than £23,250 in savings and other assets. '
            'Below £14,250, these don\'t count at all. The value of their home is usually ignored for the first 12 weeks in a care home, '
            'and always if a partner or certain relatives still live there.</p>'
            '<p>For free help with the financial assessment or a council charging decision, contact Citizens Advice on 0800 144 8848.</p>'
            '<p class="links"><a href="/#costs">Work out care costs</a><a href="/#benefits">Check benefits</a>'
            '<a href="/#kit-home-choice">Choosing a care home: step by step</a>'
            '<a href="https://www.citizensadvice.org.uk/family/looking-after-people/carers-help-and-support/" rel="noopener" target="_blank">Citizens Advice: help for carers</a></p></section>') % e(council)


def day_centres(council):
    return ('<section class="panel"><h2>Day centres and respite in %s</h2>'
            '<p>Day centres offer company, activities and a meal, often with transport, and give family carers a regular break. '
            'Many, especially those run or funded by the council, only take people referred by a social worker, so ask at the needs assessment. '
            'Others let you book and pay privately. Ask about respite care too: short stays so carers can rest.</p>'
            '<p>Day centres aren\'t usually rated by CQC, so they aren\'t listed on Kinav. Ask %s adult social care, your social worker, '
            'or local charities such as Age UK and Alzheimer\'s Society what\'s available nearby.</p></section>') % (e(council), e(council))


def write(by_la, regions, out_dir, updated):
    """by_la: {council name: [app rows]}; regions: {council name: region}."""
    shutil.rmtree(out_dir, ignore_errors=True)
    os.makedirs(out_dir)
    urls = ["/", "/care/"]
    by_region = collections.defaultdict(list)

    for council, rows in sorted(by_la.items()):
        if council == "Unknown":
            continue
        slug = slugify(council)
        region = regions.get(council, "England")
        by_region[region].append((council, slug, len(rows)))
        groups = {t[1]: [r for r in rows if t[0] in r[5]] for t in TYPES}
        groups["dementia-care"] = [r for r in rows if "D" in (r[13] or "")]
        counts = {k: len(v) for k, v in groups.items()}
        counts[""] = None
        os.makedirs(os.path.join(out_dir, slug))

        # Overview
        outstanding = [r for r in rows if r[8] == "Outstanding"]
        stats = "".join('<a href="/care/%s/%s/"><b>%d</b><span>%s</span></a>' % (slug, t[1], counts[t[1]], e(t[2]))
                        for t in TYPES) + '<a href="/care/%s/dementia-care/"><b>%d</b><span>Offer dementia care</span></a>' % (slug, counts["dementia-care"])
        body = [crumbs(region),
                '<div class="stack-sm"><h1>Care homes and care at home in %s</h1>'
                '<p class="lede">%d care services in %s are rated Good or Outstanding by CQC, including %d rated Outstanding.</p></div>' % (
                    e(council), len(rows), e(council), len(outstanding)),
                tabs(slug, "", counts), '<div class="stats">%s</div>' % stats, cta(council)]
        if outstanding:
            body.append('<section class="stack"><h2>Rated Outstanding in %s</h2><div class="list">%s</div></section>' % (
                e(council), "".join(card(r, True) for r in outstanding[:12])))
        body.append('<section class="panel"><h2>Ask %s for help</h2><p>Anyone who seems to need care can ask the council for a free needs assessment, whatever their savings. '
                    '<a href="/care/%s/needs-assessment/">How to ask, and what happens next ›</a></p></section>' % (e(council), slug))
        body.append(paying(council))
        body.append(day_centres(council))
        title = "Care homes and care at home in %s: Good and Outstanding | Kinav" % council
        desc = "%d care services in %s rated Good or Outstanding by CQC: nursing homes, residential homes, care at home and dementia care. Updated weekly." % (len(rows), council)
        save(out_dir, slug, "", page("/care/%s/" % slug, title, desc, "\n".join(body), updated))
        urls.append("/care/%s/" % slug)

        # One page per type of care, plus dementia
        for code, path, plural, _ in TYPES + [("D", "dementia-care", "Dementia care services", "")]:
            items = groups[path]
            if path == "dementia-care":
                h1 = "Dementia care in %s" % council
                lede = "%d care services in %s rated Good or Outstanding by CQC list dementia as a specialism." % (len(items), council)
            else:
                h1 = "%s in %s" % (plural, council)
                lede = "%d %s in %s are rated Good or Outstanding by CQC, best rated first." % (len(items), plural.lower(), council)
            body = [crumbs(region, council, slug), '<div class="stack-sm"><h1>%s</h1><p class="lede">%s</p></div>' % (e(h1), e(lede)),
                    tabs(slug, path, counts), cta(council)]
            body.append('<div class="list">%s</div>' % "".join(card(r, path == "dementia-care") for r in items) if items
                        else '<p class="panel">No services of this type in %s are currently rated Good or Outstanding. Try a nearby area or search by postcode in the app.</p>' % e(council))
            body.append(paying(council))
            title = "%s rated Good or Outstanding | Kinav" % h1
            desc = "%s Contact details, CQC ratings for each key question and specialisms. Updated weekly." % lede
            save(out_dir, slug, path, page("/care/%s/%s/" % (slug, path), title, desc, "\n".join(body), updated))
            urls.append("/care/%s/%s/" % (slug, path))

    # England index
    sections = []
    for region in sorted(by_region):
        links = "".join('<a href="/care/%s/">%s (%d)</a>' % (s, e(c), n) for c, s, n in sorted(by_region[region]))
        sections.append('<section class="panel" id="%s"><h2>%s</h2><div class="grid">%s</div></section>' % (region_id(region), e(region), links))
    total = sum(len(v) for k, v in by_la.items() if k != "Unknown")
    body = ('<div class="stack-sm"><h1>Care homes and care at home across England</h1>'
            '<p class="lede">%d care services rated Good or Outstanding by CQC, by council area. Choose an area to see nursing homes, residential homes, care at home and dementia care.</p></div>'
            % total) + cta("England") + "".join(sections)
    with open(os.path.join(out_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(page("/care/", "Care homes and care at home in England, rated Good or Outstanding | Kinav",
                     "Find care homes, nursing homes and care at home rated Good or Outstanding by CQC in every council area in England. Updated weekly.",
                     body, updated))
    return urls


def slugify(name):
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-") or "unknown"


def save(out_dir, slug, path, text):
    folder = os.path.join(out_dir, slug, path) if path else os.path.join(out_dir, slug)
    os.makedirs(folder, exist_ok=True)
    with open(os.path.join(folder, "index.html"), "w", encoding="utf-8") as f:
        f.write(text)


def write_sitemap(app_dir, urls=None):
    """List every page under the app folder: the app itself, area pages and guides."""
    found = []
    for root, dirs, files in os.walk(app_dir):
        dirs[:] = sorted(d for d in dirs if d not in ("data", "fonts"))
        if "index.html" in files:
            rel = os.path.relpath(root, app_dir)
            found.append("/" if rel == "." else "/" + rel.replace(os.sep, "/") + "/")
    found.sort(key=lambda u: (u != "/", u.count("/"), u))
    today = datetime.date.today().isoformat()
    lines = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    lines += ["<url><loc>%s%s</loc><lastmod>%s</lastmod></url>" % (SITE, u, today) for u in found]
    lines.append("</urlset>")
    with open(os.path.join(app_dir, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    with open(os.path.join(app_dir, "robots.txt"), "w", encoding="utf-8") as f:
        f.write("User-agent: *\nAllow: /\nSitemap: %s/sitemap.xml\n" % SITE)
    return len(found)

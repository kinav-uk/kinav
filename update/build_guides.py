"""Readable pages for Kinav's guides, so search engines can find them.

Reads update/content.json (the app's content, exported by app/build.py) and writes:
  /guides/                       index of everything
  /guides/<kit page>/            each step-by-step kit
  /plans/<plan page>/            each 30-day plan
  /articles/<article id>/        each monthly article
  /letters/<letter page>/        each letter template, as a sample to fill in
  /care-cost-calculator/, /benefits-calculator/, /ask-a-specialist/
Each page links into the app, where people can tick steps off or use the tools.
"""
import json
import os
import re
import shutil
import subprocess

import build_pages
from build_pages import e

HOME = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APP = os.path.join(HOME, "app")
CONTENT = os.path.join(HOME, "update", "content.json")

KIT_PAGES = {
    "home-choice": "how-to-choose-a-care-home",
    "home-care": "setting-up-care-at-home",
    "live-in": "arranging-live-in-care",
    "safety": "home-safety-and-grants-for-older-people",
    "alarms": "fall-alarms-and-home-cameras",
    "hospital": "leaving-hospital-discharge-checklist",
    "blue-badge": "how-to-apply-for-a-blue-badge",
    "contract": "care-home-contract-checklist",
    "no-lpa": "no-lasting-power-of-attorney-deputyship",
}
PLAN_PAGES = {
    "dementia": "caring-for-someone-with-dementia",
    "parkinsons": "caring-for-someone-with-parkinsons",
    "mobility": "caring-for-someone-with-poor-mobility-and-falls",
    "stroke": "caring-for-someone-after-a-stroke",
    "eol": "end-of-life-care-for-a-parent",
    "heart": "caring-for-someone-with-heart-failure",
    "copd": "caring-for-someone-with-copd",
    "cancer": "supporting-someone-with-cancer",
    "sight": "caring-for-someone-with-sight-or-hearing-loss",
    "continence": "caring-for-someone-with-incontinence",
    "diabetes": "caring-for-someone-with-diabetes-in-older-age",
    "arthritis": "caring-for-someone-with-arthritis",
    "afterfall": "after-a-fall-or-hospital-stay",
    "delirium": "sudden-confusion-delirium-in-older-people",
}
REVIEWED = "24 October 2026"
GOV_CARE = ("NHS: social care and support guide", "https://www.nhs.uk/social-care-and-support/")
KIT_SOURCES = {
    "home-choice": [("Care Quality Commission (CQC)", "https://www.cqc.org.uk/"), ("Age UK: care and support", "https://www.ageuk.org.uk/information-advice/care/")],
    "home-care": [("GOV.UK: apply for a needs assessment", "https://www.gov.uk/apply-needs-assessment-social-services"), ("Care Quality Commission (CQC)", "https://www.cqc.org.uk/")],
    "live-in": [("Care Quality Commission (CQC)", "https://www.cqc.org.uk/"), GOV_CARE],
    "safety": [("GOV.UK: Disabled Facilities Grants", "https://www.gov.uk/disabled-facilities-grants"), ("NHS: falls", "https://www.nhs.uk/conditions/falls/")],
    "alarms": [("Age UK: care and support", "https://www.ageuk.org.uk/information-advice/care/"), ("NHS: falls", "https://www.nhs.uk/conditions/falls/")],
    "hospital": [GOV_CARE, ("Carers UK: help and advice", "https://www.carersuk.org/help-and-advice/")],
    "blue-badge": [("GOV.UK: apply for a Blue Badge", "https://www.gov.uk/apply-blue-badge")],
    "no-lpa": [("GOV.UK: become a deputy", "https://www.gov.uk/become-deputy"), ("GOV.UK: become an appointee", "https://www.gov.uk/become-appointee-for-someone-claiming-benefits"), ("GOV.UK: search the Office of the Public Guardian registers", "https://www.gov.uk/find-someones-attorney-deputy-or-guardian")],
    "contract": [("CMA: care homes consumer law advice", "https://www.gov.uk/government/publications/care-homes-consumer-law-advice-for-providers"), ("Age UK: care and support", "https://www.ageuk.org.uk/information-advice/care/")],
}
PLAN_CHARITY = {
    "dementia": ("Alzheimer's Society", "https://www.alzheimers.org.uk/"), "parkinsons": ("Parkinson's UK", "https://www.parkinsons.org.uk/"),
    "mobility": ("NHS: falls", "https://www.nhs.uk/conditions/falls/"), "stroke": ("Stroke Association", "https://www.stroke.org.uk/"),
    "eol": ("Marie Curie", "https://www.mariecurie.org.uk/"), "heart": ("British Heart Foundation", "https://www.bhf.org.uk/"),
    "copd": ("Asthma + Lung UK", "https://www.asthmaandlung.org.uk/"), "cancer": ("Macmillan Cancer Support", "https://www.macmillan.org.uk/"),
    "sight": ("RNIB", "https://www.rnib.org.uk/"), "continence": ("Bladder & Bowel UK", "https://www.bbuk.org.uk/"),
    "diabetes": ("Diabetes UK", "https://www.diabetes.org.uk/"), "arthritis": ("Versus Arthritis", "https://www.versusarthritis.org/"), "afterfall": ("NHS: falls", "https://www.nhs.uk/conditions/falls/"),
    "delirium": GOV_CARE,
}


TEL = re.compile(r"(^|[^\u00a3\d.,])(0\d{3}(?: ?\d){6,7}|116 123|NHS 111|999)(?![\d,])")


def tel(html_text):
    """Make UK phone numbers in already-escaped text tappable (same rule as the app)."""
    return TEL.sub(lambda m: '%s<a href="tel:%s">%s</a>' % (m.group(1), re.sub(r"\D", "", m.group(2)), m.group(2)), html_text)


def sources_html(items):
    links = " \u00b7 ".join('<a href="%s" rel="noopener" target="_blank">%s</a>' % (e(u), e(n)) for n, u in items)
    return '<p class="small muted">Sources: %s. Last reviewed %s.</p>' % (links, REVIEWED)


NOT_ADVICE = ('<p class="panel small">General information only, not health or medical advice. For health questions, speak to the GP, '
              'a pharmacist or NHS 111. In an emergency, call 999.</p>')

# Free specialist helplines, by condition. Nurses and trained advisers, not a diagnosis service.
SPECIALISTS = [
    ("Dementia", [
        ("Admiral Nurse Dementia Helpline (Dementia UK)", "0800 888 6678", "https://www.dementiauk.org/get-support/dementia-helpline/",
         "Specialist dementia nurses for families: changes in behaviour, coping, planning ahead and care choices."),
        ("Alzheimer's Society Dementia Support Line", "0333 150 3456", "https://www.alzheimers.org.uk/get-support/dementia-support-line",
         "Trained dementia advisers: what support is available locally, and someone to talk to."),
    ]),
    ("Stroke", [
        ("Stroke Association Helpline", "0303 3033 100", "https://www.stroke.org.uk/stroke/support/helpline",
         "For anyone affected by stroke, including family: recovery, fatigue, money, work and driving after a stroke."),
    ]),
    ("Heart and circulation", [
        ("British Heart Foundation Heart Helpline", "0808 802 1234", "https://www.bhf.org.uk/informationsupport/heart-helpline",
         "Cardiac nurses answer questions about heart and circulatory conditions, for patients and families."),
    ]),
    ("Parkinson's", [
        ("Parkinson's UK Helpline", "0808 800 0303", "https://www.parkinsons.org.uk/contact",
         "Parkinson's nurses and advisers: living with Parkinson's, medicines questions to raise with the care team, money and work."),
    ]),
]
FAQS = [
    ("Can I ask a doctor a question online for free?",
     "For health questions about the person you care for, start with their GP practice, which may offer online consultations, or NHS 111 online or by phone. "
     "Pharmacists can answer questions about medicines without an appointment. The charity helplines on this page are staffed by specialist nurses and trained advisers, "
     "who can help you understand a condition and what to ask the doctor."),
    ("Who can I talk to about dementia?",
     "Call the Admiral Nurse Dementia Helpline on 0800 888 6678 to speak to a specialist dementia nurse, or the Alzheimer's Society Dementia Support Line on 0333 150 3456."),
    ("Who can I talk to after someone has had a stroke?",
     "The Stroke Association Helpline on 0303 3033 100 helps survivors and their families. If you think someone is having a stroke now, call 999 immediately."),
    ("Who can I ask about heart conditions?",
     "The British Heart Foundation Heart Helpline on 0808 802 1234 has cardiac nurses who answer questions from patients and families."),
    ("Who can I talk to about Parkinson's?",
     "The Parkinson's UK Helpline on 0808 800 0303 has Parkinson's nurses and advisers."),
    ("What if it's urgent?",
     "Call 999 if someone is seriously ill or injured, or their life is at risk. For urgent advice when it isn't an emergency, call NHS 111 or use 111.nhs.uk."),
    ("Does Kinav give medical advice?",
     "No. Kinav helps carers organise care and find the right people to ask. It doesn't give health or medical advice."),
]


def cta(text, href, label):
    return '<div class="cta"><p>%s</p><a class="btn" href="%s">%s</a></div>' % (text, href, e(label))


def save(rel, html_text):
    folder = os.path.join(APP, rel)
    os.makedirs(folder, exist_ok=True)
    with open(os.path.join(folder, "index.html"), "w", encoding="utf-8") as f:
        f.write(html_text)


def crumbs(*parts):
    links = ['<a href="/guides/">Guides</a>'] + ['<a href="%s">%s</a>' % (h, e(t)) for t, h in parts]
    return '<nav class="crumbs" aria-label="Breadcrumb">%s</nav>' % " › ".join(links)


def kit_page(k, updated):
    path = "/guides/%s/" % KIT_PAGES[k["id"]]
    steps = "".join('<li><b>%s</b><br><span class="muted">%s</span></li>' % (e(s["t"]), tel(e(s["d"]))) for s in k["steps"])
    body = [crumbs(), '<div class="stack-sm"><h1>%s</h1><p class="lede">%s</p></div>' % (e(k["name"]), e(k["what"])),
            cta("Tick off each step as you go in the free Kinav app.", "/#kit-%s" % k["id"], "Open this checklist"),
            '<section class="panel"><h2>Step by step</h2><ol class="steps">%s</ol></section>' % steps,
            sources_html(KIT_SOURCES.get(k["id"], [GOV_CARE])), NOT_ADVICE]
    title = "%s: step-by-step checklist | Kinav" % k["name"]
    desc = "%s A free step-by-step checklist for families caring for an older parent in England." % k["what"]
    return path, build_pages.page(path, title, desc, "\n".join(body), updated, kind="guide")


def plan_page(key, p, updated):
    path = "/plans/%s/" % PLAN_PAGES[key]
    groups = "".join('<section class="panel"><h2>%s</h2><ul class="steps">%s</ul></section>' % (
        e(g["title"]), "".join('<li><b>%s</b>%s%s</li>' % (e(i["text"]), '<br><span class="muted">%s</span>' % tel(e(i["note"])) if i.get("note") else "",
                                                          '<br>%s' % " · ".join('<a href="%s">%s ›</a>' % (l[2], e(l[0])) for l in i["links"]) if i.get("links") else "")
                               for i in g["items"])) for g in p["groups"])
    body = [crumbs(("30-day plans", "/guides/#plans")),
            '<div class="stack-sm"><h1>%s</h1><p class="lede">%s</p></div>' % (e(p["title"]), e(p["lede"])),
            cta("Follow this plan and tick off each step in the free Kinav app.", "/#plan", "Start the plan"), groups,
            sources_html([PLAN_CHARITY.get(key, GOV_CARE), ("Carers UK: help and advice", "https://www.carersuk.org/help-and-advice/")]), NOT_ADVICE]
    title = "%s: a 30-day plan for carers | Kinav" % p["title"]
    desc = "%s Practical steps for family carers: support, money, benefits and who to ask. Not medical advice." % p["lede"]
    return path, build_pages.page(path, title, desc, "\n".join(body), updated, kind="guide")


def article_page(a, plans, updated):
    path = "/articles/%s/" % a["id"]
    secs = "".join('<section class="stack-sm"><h2>%s</h2>%s%s</section>' % (
        e(s["h"]), "".join("<p>%s</p>" % tel(e(t)) for t in s.get("p", [])),
        '<ul>%s</ul>' % "".join("<li>%s</li>" % tel(e(t)) for t in s["list"]) if s.get("list") else "") for s in a["sections"])
    plan = plans.get(a.get("plan"))
    body = [crumbs(("Articles", "/guides/#articles")),
            '<div class="stack-sm"><p class="tiny muted">%s · %s</p><h1>%s</h1><p class="lede">%s</p></div>' % (
                e(a["month"]), e(a["topic"]), e(a["title"]), e(a["intro"])), secs]
    if plan:
        body.append(cta("A step-by-step plan for families: %s." % e(plan["title"]), "/plans/%s/" % PLAN_PAGES[a["plan"]], "See the 30-day plan"))
    body.append('<section class="stack-sm"><h2>Sources</h2><ul>%s</ul></section>' % "".join(
        '<li><a href="%s" rel="noopener" target="_blank">%s</a></li>' % (e(s["url"]), e(s["name"])) for s in a["sources"]))
    body.append(NOT_ADVICE)
    return path, build_pages.page(path, "%s | Kinav" % a["title"], a["intro"][:155], "\n".join(body), updated, kind="guide")


def costs_page(updated):
    path = "/care-cost-calculator/"
    body = [crumbs(), '<div class="stack-sm"><h1>Care cost calculator: how long will their savings last?</h1>'
            '<p class="lede">Work out what care might cost, how long savings could last, and when the council may start to help pay, using England\'s rules.</p></div>',
            cta("Enter the weekly fee and their savings to see the result in seconds. Nothing you enter leaves your phone.", "/#costs", "Use the calculator"),
            '<section class="panel"><h2>When does the council help pay for care?</h2>'
            '<p>The council looks at the savings and income of the person who needs care, not yours.</p>'
            '<ul><li><b>Over £23,250:</b> they usually pay the full cost of their care.</li>'
            '<li><b>£14,250 to £23,250:</b> they pay from their income, plus £1 a week for every £250 of savings over £14,250. The council pays the rest.</li>'
            '<li><b>Under £14,250:</b> savings are ignored, and they pay from their income only.</li></ul></section>',
            '<section class="panel"><h2>Is the house counted?</h2><ul>'
            '<li>Their home is never counted for care at home.</li>'
            '<li>For a care home, it is counted, but not for the first 12 weeks, and not at all if a partner, or a relative who is 60 or over or disabled, still lives there.</li>'
            '<li>If it does count, ask the council for a deferred payment agreement, so it doesn\'t have to be sold straight away.</li></ul></section>',
            '<section class="panel"><h2>Needs come first</h2><p>The council\'s free needs assessment decides whether they qualify for care. Anyone can ask for one, whatever their savings. '
            'A financial assessment then works out who pays. Citizens Advice (0800 144 8848) can help with the financial assessment or a charging decision.</p></section>',
            '<p class="panel small">These are estimates and general information about England\'s rules, not financial advice. Wales, Scotland and Northern Ireland have different limits.</p>']
    return path, build_pages.page(path, "Care cost calculator: how long will savings last? (England) | Kinav",
                                  "Free care cost calculator for England: see how long savings last in a care home or with care at home, and when the council helps pay (£23,250 and £14,250 limits).",
                                  "\n".join(body), updated, kind="guide")


def benefits_page(updated):
    path = "/benefits-calculator/"
    items = [("Attendance Allowance", "For people over State Pension age who need help with personal care or supervision. Not means-tested."),
             ("Personal Independence Payment (PIP)", "For people under State Pension age with a long-term condition or disability."),
             ("Carer's Allowance", "For carers who spend 35 hours or more a week caring and earn under the limit."),
             ("Carer's Credit", "Protects your State Pension if you care for 20 hours or more a week."),
             ("Pension Credit", "Tops up a low income in retirement, and can unlock other help."),
             ("Council tax discounts", "Discounts or exemptions for people living alone, people with a severe mental impairment such as dementia, and some carers."),
             ("Blue Badge", "Parking closer to where they need to go. See the step-by-step Blue Badge guide.")]
    body = [crumbs(), '<div class="stack-sm"><h1>Benefits calculator for carers and older people</h1>'
            '<p class="lede">Six quick questions to see which benefits the person you care for, and you, could claim.</p></div>',
            cta("Answer six questions. Your answers are used once on your phone, then forgotten.", "/#benefits", "Check what you could claim"),
            '<section class="panel"><h2>Benefits they may be eligible for</h2><ul>%s</ul></section>' % "".join(
                "<li><b>%s:</b> %s</li>" % (e(n), e(d)) for n, d in items),
            '<section class="panel"><h2>Free help to claim</h2><p>Citizens Advice can check entitlement, help fill in forms such as Attendance Allowance and challenge decisions. '
            'Adviceline (England): 0800 144 8848. Age UK Advice Line: 0800 678 1602.</p></section>',
            '<p class="panel small">A guide to what they may be eligible for, not benefits or financial advice. The Department for Work and Pensions and the council decide what someone gets.</p>']
    return path, build_pages.page(path, "Benefits calculator for carers and older people (UK) | Kinav",
                                  "Free benefits calculator: check Attendance Allowance, PIP, Carer's Allowance, Carer's Credit, Pension Credit, council tax discounts and Blue Badge in six questions.",
                                  "\n".join(body), updated, kind="guide")


def specialist_page(updated):
    path = "/ask-a-specialist/"
    groups = "".join('<section class="panel"><h2>%s</h2>%s</section>' % (e(cond), "".join(
        '<div class="stack-sm"><h3><a href="%s" rel="noopener" target="_blank">%s</a></h3><p><b>%s</b></p><p class="small muted">%s</p></div>' % (
            e(url), e(name), tel(e(num)), e(note)) for name, num, url, note in lines)) for cond, lines in SPECIALISTS)
    faq = "".join('<details class="panel"><summary><b>%s</b></summary><p>%s</p></details>' % (e(q), e(a)) for q, a in FAQS)
    schema = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQS]}
    body = [crumbs(), '<div class="stack-sm"><h1>Ask a nurse or specialist: dementia, stroke, heart and Parkinson\'s</h1>'
            '<p class="lede">Free UK helplines where family carers can ask specialist nurses and trained advisers about a condition, and what to ask the doctor.</p></div>',
            '<p class="panel"><b>Urgent?</b> Call 999 if someone is seriously ill or injured, or their life is at risk. For urgent advice, call NHS 111. '
            'For questions about their health and medicines, speak to their GP or a pharmacist.</p>',
            groups, '<section class="stack"><h2>Common questions</h2>%s</section>' % faq,
            '<p class="panel small">Kinav lists these services so you know where to ask. It doesn\'t run them or give health or medical advice. Opening times vary: check each website.</p>',
            '<script type="application/ld+json">%s</script>' % json.dumps(schema)]
    return path, build_pages.page(path, "Ask a nurse or specialist: dementia, stroke, heart and Parkinson's helplines | Kinav",
                                  "Free UK helplines for family carers: Admiral Nurses for dementia, Stroke Association, British Heart Foundation cardiac nurses and Parkinson's UK nurses.",
                                  "\n".join(body), updated, kind="guide")


HOUSE_FAQS = [
    ("Will Mum have to sell her house to pay for care at home?", "No. In England, the home is never counted when someone gets care in their own home."),
    ("Is the house counted if they move into a care home?", "It can be, but not if their partner, a relative aged 60 or over, a relative who is disabled, or a child under 18 they support still lives there."),
    ("Does the house have to be sold straight away?", "No. If the home is counted, it's ignored for the first 12 weeks of a permanent stay, and a deferred payment agreement with the council means it doesn't have to be sold in their lifetime."),
    ("When does the council start to help pay?", "When savings and other assets fall below \u00a323,250. Below \u00a314,250, they're ignored."),
    ("Can we give the house away to avoid care fees?", "Giving the home away to avoid care fees can be treated as if they still own it."),
]


def house_page(updated):
    path = "/will-they-have-to-sell-the-house-to-pay-for-care/"
    faq = "".join('<details class="panel"><summary><b>%s</b></summary><p>%s</p></details>' % (e(q), e(a)) for q, a in HOUSE_FAQS)
    schema = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in HOUSE_FAQS]}
    body = [crumbs(), '<div class="stack-sm"><h1>Will they have to sell the house to pay for care?</h1>'
            '<p class="lede">Often not, and never straight away. England\'s rules in plain English for families.</p></div>',
            cta("Work out what care could cost and how long savings would last, privately on your phone.", "/#costs", "Use the cost calculator"),
            '<section class="stack"><h2>Common questions</h2>%s</section>' % faq,
            '<section class="panel"><h2>Good to know</h2><ul><li>If the NHS agrees they qualify for NHS continuing healthcare, the NHS pays for their care.</li>'
            '<li>The council\'s financial assessment decides, so ask for the result in writing.</li>'
            '<li>Free help: Citizens Advice 0800 144 8848 and Age UK 0800 678 1602. For regulated financial advice, the Society of Later Life Advisers.</li></ul></section>',
            '<p class="panel small">General information about England\'s rules, not legal or financial advice.</p>',
            '<script type="application/ld+json">%s</script>' % json.dumps(schema)]
    return path, build_pages.page(path, "Will they have to sell the house to pay for care? (England) | Kinav",
                                  "Does the house have to be sold to pay for care? England's rules explained: care at home, the 12-week disregard, who still lives there, deferred payments and the \u00a323,250 limit.",
                                  "\n".join(body), updated, kind="guide")


# Letter templates live in app.js; these pages show each one as a sample, filled with [gaps].
LETTER_PAGES = {
    "needs": ("letter-asking-the-council-for-a-care-needs-assessment", "Letter asking the council for a care needs assessment"),
    "carer": ("carers-assessment-request-letter", "Carer's assessment request letter"),
    "discharge": ("hospital-discharge-planning-letter", "Letter to plan for leaving hospital"),
    "review": ("letter-to-challenge-a-council-care-decision", "Letter to challenge a council care decision"),
    "complaint": ("adult-social-care-complaint-letter", "Adult social care complaint letter"),
}
LETTER_SOURCES = {
    "needs": [("GOV.UK: apply for a needs assessment", "https://www.gov.uk/apply-needs-assessment-social-services"), GOV_CARE],
    "carer": [("NHS: carer's assessments", "https://www.nhs.uk/social-care-and-support/support-and-benefits-for-carers/carer-assessments/"),
              ("Carers UK: help and advice", "https://www.carersuk.org/help-and-advice/")],
    "discharge": [("NHS: going into hospital and leaving", "https://www.nhs.uk/nhs-services/hospitals/going-into-hospital/"), GOV_CARE],
    "review": [("GOV.UK: apply for a needs assessment", "https://www.gov.uk/apply-needs-assessment-social-services"),
               ("Citizens Advice", "https://www.citizensadvice.org.uk/")],
    "complaint": [("Local Government and Social Care Ombudsman", "https://www.lgo.org.uk/"), ("Citizens Advice", "https://www.citizensadvice.org.uk/")],
}
APP_JS = os.path.join(APP, "app.js")
JSC = "/System/Library/Frameworks/JavaScriptCore.framework/Versions/A/Helpers/jsc"
SAMPLE_JS = r"""
var out = LETTERS.map(function (l) {
  var v = {}, t = {};
  Object.keys(LT_FIELDS).forEach(function (k) { v[k] = "[" + LT_FIELDS[k][0].replace(/ \(optional\)/, "").toLowerCase() + "]"; });
  v.hours = "[number]"; v.rel = "[daughter or son]";
  l.ticks.forEach(function (k) { t[k] = true; });
  var to = l.to === "hospital" ? ["The ward manager and discharge team", v.hospital] : [l.to === "complaints" ? "Complaints team, Adult Social Care" : "Adult Social Care", v.council];
  var dear = l.to === "hospital" ? "Dear ward manager," : l.to === "complaints" ? "Dear complaints team," : "Dear Adult Social Care team,";
  var text = [v.you, v.contact, "[date]", "", to.join("\n"), "", dear, "", l.subject + ": " + v.them, ""].join("\n") + "\n" +
    l.body(v, t).filter(Boolean).join("\n\n") + "\n\nYours sincerely,\n\n" + v.you;
  return { id: l.id, name: l.name, when: l.when, ticks: l.ticks.map(function (k) { return LT_TICKS[k]; }), text: text };
});
print(JSON.stringify(out));
"""


def letter_samples():
    with open(APP_JS, encoding="utf-8") as f:
        js = f.read()
    start, end = js.index("  var LT_FIELDS = {"), js.index("\n  function ltState")
    out = subprocess.run([JSC, "-e", js[start:end] + SAMPLE_JS], check=True, capture_output=True, text=True).stdout
    return json.loads(out)


def letter_page(l, updated):
    slug, title = LETTER_PAGES[l["id"]]
    path = "/letters/%s/" % slug
    ticks = "".join("<li>%s</li>" % e(t) for t in l["ticks"])
    body = [crumbs(("Letters", "/letters/")),
            '<div class="stack-sm"><h1>%s: free template</h1><p class="lede">%s</p></div>' % (e(title), e(l["when"])),
            cta("Fill in the gaps on your phone and Kinav writes the letter for you, ready to email, copy or print. Nothing you type leaves your phone.",
                "/#letter-" + l["id"], "Write this letter"),
            '<section class="stack-sm"><h2>The letter</h2><pre class="letter">%s</pre></section>' % e(l["text"]),
            ('<section class="panel"><h2>Lines you can switch on or off in the app</h2><ul>%s</ul></section>' % ticks) if ticks else "",
            '<section class="panel"><h2>Good to know</h2><ul>'
            '<li>Email or post it, and keep a copy with the date you sent it.</li>'
            '<li>If you haven\'t heard back in a couple of weeks, phone and ask who is dealing with it.</li>'
            '<li>Free help: Carers UK on 0808 808 7777 and Age UK on 0800 678 1602. Citizens Advice: 0800 144 8848.</li></ul></section>',
            sources_html(LETTER_SOURCES[l["id"]]),
            '<p class="panel small">A template to help you write, not legal advice.</p>']
    return path, build_pages.page(path, "%s (free template, England) | Kinav" % title,
                                  "%s for families in England. %s Free, and fill it in on your phone." % (title, l["when"]),
                                  tel("\n".join(b for b in body if b)), updated, kind="guide")


def letters_index(samples, updated):
    items = "".join('<a href="/letters/%s/">%s</a>' % (LETTER_PAGES[l["id"]][0], e(LETTER_PAGES[l["id"]][1])) for l in samples if l["id"] in LETTER_PAGES)
    body = [crumbs(), '<div class="stack-sm"><h1>Free letter templates for family carers</h1>'
            '<p class="lede">Letters to the council and the hospital, in plain English, for families in England.</p></div>',
            cta("Fill in the gaps on your phone and Kinav writes the letter for you. Nothing you type leaves your phone.", "/#letters", "Write a letter"),
            '<section class="panel"><h2>Letters</h2><div class="grid">%s</div></section>' % items,
            '<p class="panel small">Templates to help you write, not legal advice.</p>']
    return "/letters/", build_pages.page("/letters/", "Free letter templates for family carers in England | Kinav",
                                         "Free letter templates for carers in England: ask for a needs assessment or carer's assessment, plan for leaving hospital, challenge a decision or complain.",
                                         "\n".join(body), updated, kind="guide")


def main(updated):
    with open(CONTENT, encoding="utf-8") as f:
        kc = json.load(f)
    for folder in ("guides", "plans", "articles", "care-cost-calculator", "benefits-calculator", "ask-a-specialist", "will-they-have-to-sell-the-house-to-pay-for-care", "letters"):
        shutil.rmtree(os.path.join(APP, folder), ignore_errors=True)
    pages = [kit_page(k, updated) for k in kc["kits"] if k["id"] in KIT_PAGES]
    pages += [plan_page(key, p, updated) for key, p in kc["plans"].items() if key in PLAN_PAGES]
    import datetime as _dt
    today = _dt.date.today().isoformat()
    kc["articles"] = [a for a in kc["articles"] if not a.get("from") or a["from"] <= today]
    pages += [article_page(a, kc["plans"], updated) for a in kc["articles"]]
    pages += [costs_page(updated), benefits_page(updated), specialist_page(updated), house_page(updated)]
    samples = letter_samples()
    pages += [letter_page(l, updated) for l in samples if l["id"] in LETTER_PAGES] + [letters_index(samples, updated)]
    for path, text in pages:
        save(path.strip("/"), text)

    # Guides index
    def links(prefix, names):
        return '<div class="grid">%s</div>' % "".join('<a href="%s">%s</a>' % (p, e(n)) for p, n in names if p.startswith(prefix))
    kits = [("/guides/%s/" % KIT_PAGES[k["id"]], k["name"]) for k in kc["kits"] if k["id"] in KIT_PAGES]
    plans = [("/plans/%s/" % PLAN_PAGES[k], p["title"]) for k, p in kc["plans"].items() if k in PLAN_PAGES]
    arts = [("/articles/%s/" % a["id"], a["title"]) for a in kc["articles"]]
    body = ['<div class="stack-sm"><h1>Guides for families caring for an older parent</h1>'
            '<p class="lede">Free step-by-step guides, 30-day plans and tools for carers in England.</p></div>',
            '<section class="panel"><h2>Tools</h2><div class="grid"><a href="/care-cost-calculator/">Care cost calculator</a>'
            '<a href="/benefits-calculator/">Benefits calculator</a><a href="/care/">Care homes and care at home by area</a>'
            '<a href="/ask-a-specialist/">Ask a nurse or specialist</a><a href="/will-they-have-to-sell-the-house-to-pay-for-care/">Will they have to sell the house?</a>'
            '<a href="/letters/">Free letter templates</a></div></section>',
            '<section class="panel" id="kits"><h2>Step-by-step guides</h2>%s</section>' % links("/guides/", kits),
            '<section class="panel" id="plans"><h2>30-day plans</h2>%s</section>' % links("/plans/", plans),
            '<section class="panel" id="articles"><h2>Articles for carers</h2>%s</section>' % links("/articles/", arts), NOT_ADVICE]
    save("guides", build_pages.page("/guides/", "Guides for family carers: care homes, costs, benefits and plans | Kinav",
                                    "Free guides for families caring for an older parent in England: choosing a care home, care costs, benefits, Blue Badge, hospital discharge and 30-day plans.",
                                    "\n".join(body), updated, kind="guide"))
    print("Guide pages: %d" % (len(pages) + 1))


if __name__ == "__main__":
    import datetime
    main(datetime.date.today().strftime("%-d %B %Y"))

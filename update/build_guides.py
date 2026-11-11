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
import urllib.parse

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
    "needs-assessment": "care-needs-assessment-how-to-prepare",
    "aa": "how-to-claim-attendance-allowance",
    "carers-allowance": "how-to-claim-carers-allowance",
    "lpa": "how-to-make-a-lasting-power-of-attorney",
    "chc": "nhs-continuing-healthcare-checklist-and-assessment",
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
    "needs-assessment": [("GOV.UK: apply for a needs assessment", "https://www.gov.uk/apply-needs-assessment-social-services"), ("Age UK: care and support", "https://www.ageuk.org.uk/information-advice/care/")],
    "aa": [("GOV.UK: Attendance Allowance", "https://www.gov.uk/attendance-allowance"), ("Citizens Advice: Attendance Allowance", "https://www.citizensadvice.org.uk/benefits/sick-or-disabled-people-and-carers/attendance-allowance/")],
    "carers-allowance": [("GOV.UK: Carer's Allowance", "https://www.gov.uk/carers-allowance"), ("Carers UK: help and advice", "https://www.carersuk.org/help-and-advice/")],
    "lpa": [("GOV.UK: make a lasting power of attorney", "https://www.gov.uk/power-of-attorney"), ("GOV.UK: register a lasting power of attorney", "https://www.gov.uk/power-of-attorney/register")],
    "chc": [("NHS: NHS continuing healthcare", "https://www.nhs.uk/social-care-and-support/money-work-and-benefits/nhs-continuing-healthcare/"), ("Age UK: care and support", "https://www.ageuk.org.uk/information-advice/care/")],
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
    ("Cancer", [
        ("Macmillan Support Line", "0808 808 00 00", "https://www.macmillan.org.uk/about-us/contact-us",
         "Cancer information nurses and advisers, 8am to 8pm every day: treatment questions to raise, money, work and emotional support."),
    ]),
    ("Lungs and breathing", [
        ("Asthma + Lung UK Helpline", "0300 222 5800", "https://www.asthmaandlung.org.uk/helpline",
         "Respiratory nurses for COPD and other lung conditions, weekdays 9am to 5pm."),
    ]),
    ("Terminal illness and end of life", [
        ("Marie Curie Support Line", "0800 090 2309", "https://www.mariecurie.org.uk/help/support",
         "Practical and emotional support for people with a terminal illness, their families and carers, including bereavement."),
    ]),
    ("Arthritis", [
        ("Arthritis UK Helpline", "0800 5200 520", "https://www.arthritis-uk.org/",
         "Formerly Versus Arthritis. Advice on living with arthritis and joint pain, weekdays 9am to 6pm."),
    ]),
    ("Diabetes", [
        ("Diabetes UK Helpline", "0345 123 2399", "https://www.diabetes.org.uk/how_we_help/helpline",
         "For anyone affected by diabetes, including family, weekdays 9am to 6pm."),
    ]),
    ("Sight and hearing", [
        ("RNIB Helpline", "0303 123 9999", "https://www.rnib.org.uk/helpline", "Living with sight loss: equipment, benefits, rights and emotional support."),
        ("RNID Helpline", "0808 808 0123", "https://rnid.org.uk/about-us/contact-rnid/", "Hearing loss and tinnitus: hearing aids, equipment and support."),
    ]),
    ("Bladder and bowel", [
        ("Bladder & Bowel UK Helpline", "0161 214 4591", "https://www.bbuk.org.uk/",
         "Specialist continence nurses and product advice."),
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
            cta(e(k["print"][1]), k["print"][2], k["print"][0]) if k.get("print") else "",
            '<section class="panel"><h2>Step by step</h2><ol class="steps">%s</ol>'
            '<p class="noprint"><button class="btn btn-ghost" type="button" onclick="print()">Print this checklist</button></p></section>' % steps,
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
    if a.get("cta"):
        body.append(cta(e(a["cta"][0]), a["cta"][1], a["cta"][2]))
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
    body = [crumbs(), '<div class="stack-sm"><h1>Ask a nurse or specialist: free helplines by condition</h1>'
            '<p class="lede">Free UK helplines where family carers can ask specialist nurses and trained advisers about a condition, and what to ask the doctor.</p></div>',
            '<p class="panel"><b>Urgent?</b> Call 999 if someone is seriously ill or injured, or their life is at risk. For urgent advice, call NHS 111. '
            'For questions about their health and medicines, speak to their GP or a pharmacist.</p>',
            groups, '<section class="stack"><h2>Common questions</h2>%s</section>' % faq,
            '<p class="panel small">Kinav lists these services so you know where to ask. It doesn\'t run them or give health or medical advice. Opening times vary: check each website.</p>',
            '<script type="application/ld+json">%s</script>' % json.dumps(schema)]
    return path, build_pages.page(path, "Ask a nurse or specialist: free UK helplines by condition | Kinav",
                                  "Free UK helplines for family carers: dementia, stroke, heart, Parkinson's, cancer, lungs, arthritis, diabetes, sight and hearing. Specialist nurses and advisers.",
                                  "\n".join(body), updated, kind="guide")


def door_sign_page(updated):
    """A printable Halloween door sign. Kept all year so it's found again each October."""
    path = "/printables/no-trick-or-treaters-door-sign/"
    body = ['<style>.sign{border:8px solid #e8772e;border-radius:32px;background:#fff;color:#18232e;text-align:center;padding:48px 20px;margin:0 auto;max-width:560px;box-sizing:border-box}'
            '.sign .pk{font-size:96px;line-height:1}.sign b{display:block;font-size:clamp(32px,9vw,52px);line-height:1.05;margin:24px 0 0}.sign span{display:block;font-size:24px;margin-top:20px}'
            '@media print{.sign{max-width:none;padding:120px 40px;border-width:12px}.sign .pk{font-size:160px}.sign b{font-size:96px}.sign span{font-size:36px}}</style>',
            '<div class="stack-sm noprint"><h1>Free printable "No trick or treaters" door sign</h1>'
            '<p class="lede">For an older parent, relative or neighbour who would rather not have knocks at the door after dark on Halloween. '
            'Print it, then tape it to the front door or a window.</p>'
            '<p><button class="btn" type="button" onclick="print()">Print the sign</button></p></div>',
            '<div class="sign"><div class="pk">\U0001F383</div><b>No trick or treaters, please</b><span>Thank you, and have a lovely Halloween</span></div>',
            '<section class="panel noprint"><h2>A few other things that help</h2><ul>'
            '<li>Remind them they don\'t have to answer the door after dark, to anyone they aren\'t expecting.</li>'
            '<li>Leave the porch light off if they don\'t want callers. Many families take that as a sign to skip the house.</li>'
            '<li>Give them a quick call in the evening, or ask a neighbour to look in.</li>'
            '<li>If a stranger calls about work on the house or money, they can say no and close the door. Real callers won\'t mind.</li></ul>'
            '<p>More free help for families caring for an older parent: <a href="/guides/">guides</a>, <a href="/letters/">letters</a> and <a href="/">care near them</a>.</p></section>']
    return path, build_pages.page(path, "Free printable \"No trick or treaters\" door sign for older parents | Kinav",
                                  "A free Halloween door sign to print for an older parent or neighbour who would rather not have knocks at the door after dark.",
                                  "\n".join(body), updated, kind="guide")


DISCHARGE_SHEET = [
    ("The plan", ["When is the planned discharge date and time?", "Can we have the written discharge plan, and a copy for the family?",
                  "Who is our named contact for the discharge, and their number?"]),
    ("Support at home", ["What care and support will be in place at home, and from which day?", "Is reablement being arranged? It's free, usually for up to 6 weeks.",
                         "Who is arranging the care, and how do we contact them?", "Has a care needs assessment been done or asked for?"]),
    ("Equipment and the home", ["What equipment is needed, and when will it be delivered?", "Does someone need to check the home before they come back, such as an occupational therapist?"]),
    ("Medicines", ["What medicines are they going home with, and who will explain any changes?"]),
    ("Getting home", ["Who is arranging transport, and what time?", "Will the GP get a discharge letter, and can we have a copy?",
                      "Has the NHS continuing healthcare checklist been considered?", "Who do we call if something agreed doesn't happen?"]),
]


def discharge_sheet_page(updated):
    """A printable sheet of questions for the ward before an older parent leaves hospital."""
    path = "/printables/before-discharge-questions-for-the-ward/"
    rows = "".join('<h2>%s</h2>%s' % (e(h), "".join('<div class="ds-q"><span class="ds-box"></span><span>%s<span class="ds-line"></span></span></div>' % e(q) for q in qs))
                   for h, qs in DISCHARGE_SHEET)
    body = ['<style>.ds{background:#fff;color:#18232e;border:1.5px solid var(--line);border-radius:18px;padding:24px 20px;max-width:720px}'
            '.ds h2{font-size:17px;margin:18px 0 6px}.ds-q{display:flex;gap:10px;align-items:flex-start;margin:8px 0;font-size:15px}.ds-q>span:last-child{flex:1}'
            '.ds-box{flex:none;width:16px;height:16px;border:1.5px solid #18232e;border-radius:3px;margin-top:3px}'
            '.ds-line{display:block;border-bottom:1px solid #9aa5ad;height:26px}.ds-top{display:grid;grid-template-columns:1fr 1fr;gap:10px 16px;font-size:14px}'
            '.ds-top span{border-bottom:1px solid #9aa5ad;padding-bottom:16px}.ds-fam{border:2px solid #e8772e;border-radius:12px;padding:12px 14px;margin-top:18px;font-size:15px}'
            '@media print{@page{margin:12mm}.ds{border:0;padding:0;max-width:none}.ds h1{font-size:20px!important;margin-bottom:6px!important}.ds h2{font-size:14px;margin:8px 0 2px}.ds-q{font-size:12.5px;margin:2px 0}.ds-line{height:15px}.ds-top span{padding-bottom:10px}.ds-fam{margin-top:10px;padding:8px 12px;font-size:13px}}</style>',
            '<div class="stack-sm noprint"><h1>Before they leave hospital: questions for the ward</h1>'
            '<p class="lede">A one-page sheet to print and take to the ward, or to have by the phone. Write the answers as you go, '
            'so nothing is missed and everyone in the family knows the plan.</p>'
            '<p><button class="btn" type="button" onclick="print()">Print the sheet</button></p></div>',
            '<div class="ds"><h1 style="font-size:24px;margin:0 0 12px">Before they leave hospital</h1>'
            '<div class="ds-top"><span>Name:</span><span>Ward:</span><span>Hospital:</span><span>Date:</span></div>' + rows +
            '<div class="ds-fam"><b>Please don\'t assume family can provide the care.</b><br>We can help with: <span class="ds-line"></span>We can\'t: <span class="ds-line"></span></div>'
            '<p class="tiny" style="margin:6px 0 0">Free from kinav.co.uk · General information, not medical advice: ask the ward team about their health and medicines.</p></div>',
            '<section class="panel noprint"><h2>More help when someone leaves hospital</h2>'
            '<p><a href="/guides/leaving-hospital-discharge-checklist/">Leaving hospital: step-by-step checklist ›</a></p>'
            '<p><a href="/letters/">Write to the ward or the council: free letter templates ›</a></p>'
            '<p>If you can\'t give the care that\'s needed, say so clearly before the discharge date. The plan shouldn\'t rely on family who can\'t provide it.</p></section>']
    return path, build_pages.page(path, "Before they leave hospital: printable questions for the ward | Kinav",
                                  "A free printable sheet of questions to ask the ward before an older parent is discharged from hospital: the plan, care at home, equipment, medicines and transport.",
                                  "\n".join(body), updated, kind="guide")


def cold_callers_page(updated):
    """A printable "No cold callers" door sign, with tips on doorstep scams."""
    path = "/printables/no-cold-callers-door-sign/"
    body = ['<style>.sign{border:8px solid #1f5f7a;border-radius:32px;background:#fff;color:#18232e;text-align:center;padding:48px 20px;margin:0 auto;max-width:560px;box-sizing:border-box}'
            '.sign .pk{width:96px;height:96px}.sign b{display:block;font-size:clamp(34px,10vw,60px);line-height:1.05;margin:20px 0 0}.sign span{display:block;font-size:22px;margin-top:18px;line-height:1.35}'
            '@media print{.sign{max-width:none;padding:110px 40px;border-width:12px}.sign .pk{width:170px;height:170px}.sign b{font-size:110px}.sign span{font-size:34px}}</style>',
            '<div class="stack-sm noprint"><h1>Free printable "No cold callers" door sign</h1>'
            '<p class="lede">Doorstep sellers and scammers often target older people. A clear sign on the door helps them say no. Print it, then tape it to the door or a window by the door.</p>'
            '<p><button class="btn" type="button" onclick="print()">Print the sign</button></p></div>',
            '<div class="sign"><svg class="pk" viewBox="0 0 100 100" aria-hidden="true"><circle cx="50" cy="50" r="46" fill="#c8102e"/><rect x="18" y="41" width="64" height="18" rx="3" fill="#fff"/></svg><b>No cold callers</b><span>We don\'t buy or sign up to anything at the door.<br>Please respect this notice and leave.</span></div>',
            '<section class="panel noprint"><h2>Help them stay safe at the door</h2><ul>'
            '<li>They never have to open the door to someone they aren\'t expecting. A door chain or a video doorbell helps them check first.</li>'
            '<li>Genuine callers from gas, electricity and water companies carry ID and won\'t mind waiting while they phone the company on a number from a bill, not one the caller gives them.</li>'
            '<li>No genuine bank, police officer or council will ask for their PIN, or send someone to collect cash or their bank card.</li>'
            '<li>Be wary of anyone who knocks offering roof, driveway or garden work, especially if they want cash or to start today.</li>'
            '<li>If it happens, report it to Citizens Advice on 0808 223 1133, who pass it to Trading Standards. If someone won\'t leave or they feel unsafe, call 999.</li></ul>'
            '<p>More free help for families caring for an older parent: <a href="/guides/">guides</a>, <a href="/letters/">letters</a> and <a href="/">care near them</a>.</p></section>']
    return path, build_pages.page(path, "Free printable \"No cold callers\" door sign for older people | Kinav",
                                  "A free door sign to print for an older parent or neighbour, to stop doorstep sellers and scammers, with simple tips to stay safe at the door.",
                                  tel("\n".join(body)), updated, kind="guide")


PHONE_ROWS = [("Family", "", ""), ("Family", "", ""), ("Neighbour with a key", "", ""), ("GP surgery", "", ""), ("Pharmacy", "", ""),
              ("Care agency or carer", "", ""), ("Their council's adult social care", "", ""),
              ("NHS 111", "Urgent medical help when it isn't an emergency", "111"), ("Power cut", "Any electricity network", "105"),
              ("Gas emergency", "If they smell gas", "0800 111 999"), ("Age UK Advice Line", "Free, for older people and families", "0800 678 1602"),
              ("Samaritans", "Any time, if things feel too much", "116 123")]


def phone_list_page(updated):
    """A large-print list of important numbers to fill in on screen and print for beside the phone."""
    path = "/printables/important-phone-numbers-list/"
    rows = "".join('<div class="pl-row"><input class="pl-who" value="%s" aria-label="Who"><input class="pl-num" value="%s" placeholder="Number" aria-label="Number">%s</div>'
                   % (e(w), e(n), '<small>%s</small>' % e(note) if note else "") for w, note, n in PHONE_ROWS)
    body = ['<style>.pl{background:#fff;color:#18232e;border:1.5px solid var(--line);border-radius:18px;padding:20px;max-width:720px}'
            '.pl h2{font-size:30px;margin:0 0 4px}.pl-999{font-size:26px;font-weight:800;color:#b42318;margin:6px 0 12px}'
            '.pl-row{display:grid;grid-template-columns:1fr 1fr;gap:4px 12px;border-bottom:1.5px solid #c9d1d6;padding:8px 0}'
            '.pl-row input{font:inherit;font-size:20px;border:0;border-bottom:1px dashed #c9d1d6;border-radius:0;padding:4px 2px;min-height:0;background:transparent;width:100%}'
            '.pl-who{font-weight:700}.pl-row small{grid-column:1/-1;color:#5b6770;font-size:14px}'
            '@media print{@page{margin:12mm}.pl{border:0;padding:0;max-width:none}.pl h2{font-size:34px}.pl-999{font-size:30px}'
            '.pl-row{padding:5px 0}.pl-row input{font-size:22px;border-bottom:0}.pl-row input:placeholder-shown{border-bottom:1px solid #9aa5ad}.pl-row input::placeholder{color:transparent}.pl-row small{font-size:12px}}</style>',
            '<div class="stack-sm noprint"><h1>Important phone numbers: a large-print list for by the phone</h1>'
            '<p class="lede">Type the names and numbers in the boxes, then print. Big, clear and easy to find in a hurry. '
            'What you type stays on this page: it isn\'t saved or sent anywhere.</p>'
            '<p><button class="btn" type="button" onclick="print()">Print the list</button></p></div>',
            '<div class="pl"><h2>Important numbers</h2><p class="pl-999">Emergency: 999</p>' + rows +
            '<p class="tiny" style="margin:10px 0 0">Free from kinav.co.uk</p></div>',
            '<section class="panel noprint"><h2>Tips</h2><ul><li>Put a copy by the phone, and another on the fridge.</li>'
            '<li>Save the same numbers in their mobile, and yours.</li><li>Leave a row blank to write a number in by hand after printing.</li></ul>'
            '<p>More free help for families caring for an older parent: <a href="/guides/">guides</a>, <a href="/letters/">letters</a> and <a href="/">care near them</a>.</p></section>']
    return path, build_pages.page(path, "Important phone numbers list for an older parent: free large-print printable | Kinav",
                                  "A free large-print list of important phone numbers to fill in and print for an older parent: family, GP, pharmacy, carers, NHS 111, power cut and gas emergency.",
                                  "\n".join(body), updated, kind="guide")


EMERGENCY_ROWS = ["Full name", "Date of birth", "Address", "Call first (name and number)", "Call next (name and number)",
                  "GP surgery and number", "NHS number", "Where their medicines list is kept", "Allergies",
                  "Glasses, hearing aid or walking aid", "Lasting Power of Attorney (who)", "Spare key is with",
                  "Care agency or carer", "Pets to look after"]


def emergency_sheet_page(updated):
    """A one-page emergency information sheet to fill in on screen and print for the fridge. Nothing is saved."""
    path = "/printables/emergency-information-sheet/"
    rows = "".join('<label class="es-row"><span>%s</span><input aria-label="%s"></label>' % (e(r), e(r)) for r in EMERGENCY_ROWS)
    body = ['<style>.es{background:#fff;color:#18232e;border:1.5px solid var(--line);border-radius:18px;padding:20px;max-width:720px}'
            '.es h2{font-size:28px;margin:0 0 2px}.es-999{font-size:22px;font-weight:800;color:#b42318;margin:4px 0 10px}'
            '.es-row{display:grid;grid-template-columns:minmax(150px,40%) 1fr;gap:10px;align-items:end;border-bottom:1.5px solid #c9d1d6;padding:9px 0;font-weight:700;font-size:16px}'
            '.es-row input{font:inherit;font-weight:400;font-size:18px;border:0;border-radius:0;padding:2px;min-height:0;background:transparent;width:100%}'
            '@media(max-width:520px){.es-row{grid-template-columns:1fr}}'
            '@media print{@page{margin:12mm}.es{border:0;padding:0;max-width:none}.es h2{font-size:30px}.es-row{padding:7px 0;font-size:15px;grid-template-columns:40% 1fr}.es-row input{font-size:17px}}</style>',
            '<div class="stack-sm noprint"><h1>Emergency information sheet for an older parent: free printable</h1>'
            '<p class="lede">One page with what paramedics, carers or a neighbour need to know in a hurry. Type in the details, print it, and keep it on the fridge. '
            'What you type stays on this page: it isn\'t saved or sent anywhere.</p>'
            '<p><button class="btn" type="button" onclick="print()">Print the sheet</button></p></div>',
            '<div class="es"><h2>In an emergency</h2><p class="es-999">Call 999</p>' + rows +
            '<p class="tiny" style="margin:10px 0 0">Free from kinav.co.uk · Check and update it every few months.</p></div>',
            '<section class="panel noprint"><h2>Tips</h2><ul>'
            '<li>Keep it on the fridge door, where paramedics are used to looking, and give a copy to whoever has a spare key.</li>'
            '<li>Leave a box blank to fill in by hand after printing.</li>'
            '<li>For medicines, write where the list is kept rather than copying it out, so there\'s only one list to keep up to date. The pharmacy can print one.</li>'
            '<li>Some areas give out free "Message in a Bottle" kits from the Lions Clubs, with stickers that tell paramedics to look in the fridge.</li></ul>'
            '<p>More free printables: <a href="/printables/important-phone-numbers-list/">important numbers for by the phone</a> and '
            '<a href="/printables/before-discharge-questions-for-the-ward/">questions before they leave hospital</a>.</p></section>']
    return path, build_pages.page(path, "Emergency information sheet for an older parent: free printable for the fridge | Kinav",
                                  "A free one-page emergency information sheet to fill in and print for an older parent: who to call, GP, NHS number, where medicines are listed, allergies and spare keys.",
                                  "\n".join(body), updated, kind="guide")


SHOP = "https://kinavuk.etsy.com"
# Kinav's printables on Etsy: picture name in app/shop-img, name, one line, and the words that find it in the shop's search.
PLANNERS = [
    ("Christmas games, activities and gifts", "christmas", [
        ("christmas-bundle", "The Kinav Christmas Bundle", "Retro Christmas games, Let's Talk Christmas cards and the gift planner, together. Save over 30%.", "christmas bundle"),
        ("christmas-gift-planner", "Christmas Gift Planner for carers", "Budgets, bought, wrapped and given, and gifts from the person you care for. An app plus a printable planner.", "christmas gift planner"),
        ("christmas-activity-programme", "24 Days of December, for care homes", "A ready-to-run Christmas activity for every day of Advent, with three ways for every resident to join in.", "24 day december"),
        ("christmas-cards", "Let's Talk Christmas pack", "Christmas reminiscence cards, a quiz and word search to share Christmas memories.", "christmas reminiscence"),
        ("christmas-cards-care-home", "Let's Talk Christmas pack: care home edition", "Christmas memory cards and activities, licensed for a care home.", "care home christmas activity pack"),
        ("retro-christmas-games", "Retro Christmas games", "Christmas quizzes from the 1950s to the 1980s, so everyone plays their decade. Bingo, carols, charades and an easy mode.", "retro christmas games"),
        ("retro-christmas-games-care-home", "Retro Christmas games: care home edition", "Four decades of Christmas quizzes, with an easy mode, licensed for a care home or day centre.", "care home retro christmas")]),
    ("Planners and calendars", "planners", [
        ("calendar-2027", "2027 large-print calendar", "Big, clear months for appointments, visits and bin days. Print it or fill it in on screen.", "2027 calendar"),
        ("care-binder", "Elderly parent care binder (UK)", "174 pages: every Kinav planner and kit in one binder, in three colour styles.", "care binder"),
        ("care-planner", "Elderly parent care planner", "Contacts, medicines list, appointments and who does what.", "care planner"),
        ("carers-budget-planner", "Carer's budget planner", "Monthly budget, caring costs and who pays what. Printable, plus an Excel spreadsheet.", "budget planner"),
        ("care-spreadsheet", "Care organiser spreadsheet", "Medicines chart, health log, appointments and care costs that add themselves up. For Excel and Google Sheets.", "care organiser spreadsheet"),
        ("daily-log", "Caregiver daily log", "Daily notes and handover sheets for the family or carers.", "daily log"),
        ("dementia-planner", "Dementia care planner", "Routines, what helps, and planning ahead, for families caring for someone with dementia.", "dementia care planner"),
        ("adhd-carer-planner", "ADHD-friendly carer's planner", "Less writing, more ticking: a Today page with just 3 things, phone call scripts and reminders. Plus a spreadsheet.", "adhd carer planner"),
        ("adhd-digital-planner", "ADHD-friendly digital planner", "The ADHD planner for iPad and tablets: tap-to-go tabs, a page for every day, and stickers. For GoodNotes and Notability.", "adhd digital planner"),
        ("adhd-fridge-cards", "Fridge dashboard and grab cards", "The week at a glance on the fridge, key numbers by the phone, and checklist cards for the door, visits and the hospital bag.", "fridge dashboard"),
        ("life-admin-binder", "Just-in-case binder", "Where everything is, who to call, accounts and wishes, in one place.", "just in case binder"),
        ("bundle", "Complete carer's bundle", "The main planners and checklists together, for less.", "bundle")]),
    ("Checklists and kits", "kits", [
        ("attendance-allowance", "Attendance Allowance claim kit", "A care diary and prompts for the form, so you don't miss what matters.", "attendance allowance"),
        ("needs-assessment", "Care needs assessment kit", "Get ready for the council's assessment, with a diary and letters.", "needs assessment"),
        ("hospital-discharge", "Leaving hospital checklist", "Questions for the ward and getting the home ready.", "hospital discharge"),
        ("care-home-visit-pack", "Care home visit checklist", "Questions to ask, a scorecard and a side-by-side comparison.", "care home visit"),
        ("moving-into-a-care-home", "Moving into a care home", "Packing list, an 'About me' profile and the first weeks.", "moving into a care home"),
        ("lpa-organiser", "Lasting Power of Attorney kit", "Step by step, with a record book for attorneys.", "power of attorney"),
        ("household-paperwork", "Bills and paperwork kit", "Accounts, direct debits and paperwork, all in one place.", "bills and paperwork"),
        ("carers-emergency-plan", "Carer's emergency plan", "An 'if I can't be there' plan and a wallet card.", "emergency plan"),
        ("planning-ahead", "Planning ahead pack", "Wishes, will and power of attorney checklists.", "planning ahead"),
        ("after-a-death", "After a death checklist", "What to do, who to tell, and funeral planning.", "after a death"),
        ("later-life-divorce", "Divorce planner, over 60", "Money, pensions and the home, step by step.", "divorce planner"),
        ("letter-pack", "Carer letter templates", "Editable letters for the council, employers and more.", "letter templates")]),
    ("Activities", "activities", [
        ("reminiscence-cards", "Let's Talk reminiscence cards", "120 cards to spark memories and conversation, at home or in a care home.", "reminiscence cards")]),
]

# Each product's own Etsy listing link (Share & Save links are best). Products not listed here open a search
# inside the Kinav shop for that product, so only Kinav listings ever show.
LISTING_LINKS = {
    "christmas-bundle": "https://kinavuk.etsy.com/uk/listing/4612582895/christmas-bundle-for-older-relatives",
    "christmas-gift-planner": "https://kinavuk.etsy.com/uk/listing/4611384577/christmas-gift-planner-app-for-carers",
    "christmas-activity-programme": "https://kinavuk.etsy.com/uk/listing/4611376412/christmas-activities-for-care-homes-24",
    "christmas-cards": "https://kinavuk.etsy.com/uk/listing/4610679958/christmas-activity-reminiscence-cards",
    "care-spreadsheet": "https://kinavuk.etsy.com/uk/listing/4611241685/care-organiser-spreadsheet-uk-medication",
    "carers-budget-planner": "https://kinavuk.etsy.com/uk/listing/4611074567/carers-budget-planner-uk-printable-pdf",
    "retro-christmas-games-care-home": "https://kinavuk.etsy.com/uk/listing/4610697448/care-home-christmas-activities-retro",
    "retro-christmas-games": "https://kinavuk.etsy.com/uk/listing/4610674187/printable-party-games-grandparent-gift",
    "christmas-cards-care-home": "https://kinavuk.etsy.com/uk/listing/4610619702/care-home-christmas-activity-pack",
    "attendance-allowance": "https://kinavuk.etsy.com/uk/listing/4610570617/attendance-allowance-claim-kit-uk",
    "needs-assessment": "https://kinavuk.etsy.com/uk/listing/4611923791/care-needs-assessment-kit-uk-pdf-and",
    "moving-into-a-care-home": "https://kinavuk.etsy.com/uk/listing/4611943646/moving-into-a-care-home-checklist-pdf",
    "lpa-organiser": "https://kinavuk.etsy.com/uk/listing/4611932219/lasting-power-of-attorney-kit-pdf-and",
    "reminiscence-cards": "https://kinavuk.etsy.com/uk/listing/4611935151/reminiscence-cards-for-elderly-128",
    "care-home-visit-pack": "https://kinavuk.etsy.com/uk/listing/4610539380/care-home-visit-checklist-printable-and",
    "calendar-2027": "https://kinavuk.etsy.com/uk/listing/4610543809/2027-large-print-calendar-printable",
    "daily-log": "https://kinavuk.etsy.com/uk/listing/4610530561/caregiver-daily-log-printable-fillable",
    "life-admin-binder": "https://kinavuk.etsy.com/uk/listing/4610527265/just-in-case-binder-uk-life-admin",
    "care-binder": "https://kinavuk.etsy.com/uk/listing/4610544522/elderly-parent-care-binder-125-page",
    "dementia-planner": "https://kinavuk.etsy.com/uk/listing/4610524094/dementia-care-planner-uk-printable",
    "adhd-carer-planner": "https://kinavuk.etsy.com/uk/listing/4612708355/adhd-friendly-carer-planner-uk-printable",
    "adhd-digital-planner": "https://kinavuk.etsy.com/uk/listing/4613210920/adhd-digital-planner-for-carers",
    "adhd-fridge-cards": "https://kinavuk.etsy.com/uk/listing/4613198171/adhd-fridge-dashboard-and-checklist",
    "letter-pack": "https://kinavuk.etsy.com/uk/listing/4610484887/carer-letter-templates-editable-word-and",
    "bundle": "https://kinavuk.etsy.com/uk/listing/4610501544/elderly-parent-care-bundle-care-planner",
    "after-a-death": "https://kinavuk.etsy.com/uk/listing/4610477309/after-a-death-checklist-printable",
    "hospital-discharge": "https://kinavuk.etsy.com/uk/listing/4610469119/hospital-discharge-checklist-printable",
    "planning-ahead": "https://kinavuk.etsy.com/uk/listing/4605940380/planning-ahead-pack-end-of-life-planner",
    "care-planner": "https://kinavuk.etsy.com/uk/listing/4606518980/care-planning",
}
SHOP_SEARCH = "https://kinavuk.etsy.com?search_query=%s"

def adhd_page(updated):
    """Practical tips for carers who have ADHD. Organising tips only: no advice about ADHD itself or anyone's health."""
    path = "/articles/caring-with-adhd/"
    tips = [
        ("Put everything in one place", "One list, one notebook or one app, not sticky notes everywhere. Write each job down the moment you think of it, "
         "even half a thought. Then you can stop holding it in your head."),
        ("Let your phone do the remembering", "Set alarms for the times medicines are due, as on the pharmacy label, and a reminder a week before repeat "
         "prescriptions run out. Name each alarm with the action, like \"Mum's evening tablets\", not just a time. Put every appointment in your "
         "calendar with two alerts: the day before and two hours before. A shared family calendar means you're not the only one who knows."),
        ("Make phone calls easier", "Have their name, date of birth and any reference number ready before you dial. Write down what you want to say "
         "in a sentence or two. It's fine to tell people you're reading from notes. Afterwards, write down who you spoke to, the date and what happens next. "
         "If phoning is hard, many councils and surgeries accept emails or letters too, and our free letter templates can help."),
        ("Tame the paperwork pile", "Pick up one thing at a time and decide straight away: do it, file it or bin it. Keep one box for anything to keep. "
         "Put a 10-minute paperwork slot in your calendar once a week, and stop when the timer goes."),
        ("Shrink big jobs", "\"Fill in the Attendance Allowance form\" is hard to start. \"Find the form and put it on the table\" isn't. "
         "Write down a tiny first step, do just that, then decide whether to carry on."),
        ("Keep one page of the key facts", "Their NHS number, GP, pharmacy, social worker and who holds Power of Attorney, on one page by the phone. "
         "Every form and phone call gets quicker."),
        ("Share the load", "Write each job down once with a name next to it, and send the list to the family. You don't have to hold it all. "
         "Kinav's free 'Share out the jobs' tool sends one clear list to your family group."),
        ("Look after yourself too", "Ask the council for a free carer's assessment. It can lead to breaks and support. If you work, you can take a week "
         "of unpaid carer's leave a year and ask for flexible working, from your first day in a job. And keep a 'done' list: on hard days it shows how much "
         "you're already doing."),
    ]
    body = [crumbs(), '<div class="stack-sm"><h1>Caring for a parent when you have ADHD: practical tips</h1>'
            '<p class="lede">Caring is full of the things ADHD can make hardest: remembering appointments, chasing paperwork, starting phone calls, '
            'and juggling someone else\'s needs with your own. You\'re not failing. It\'s a lot. These tips make it easier to keep on top of.</p></div>']
    for i, (h, t) in enumerate(tips, 1):
        body.append('<section class="stack-sm"><h2>%d. %s</h2><p>%s</p></section>' % (i, e(h), e(t)))
    body.append('<section class="panel"><h2>Support for you</h2><ul>'
                '<li><b>Carers UK Helpline:</b> 0808 808 7777, for advice on benefits, work and support</li>'
                '<li><b>Your local carers\' centre:</b> search carers.org for carer services near you</li>'
                '<li><b>ADHD UK:</b> information about ADHD for adults at adhduk.co.uk</li>'
                '<li><b>Your GP:</b> if you think you might have ADHD, or need support with it</li>'
                '<li><b>Samaritans:</b> 116 123, free, any time, if things feel too much</li></ul></section>')
    body.append('<div class="cta"><p><b>Want it all on paper?</b> Our ADHD-friendly carer\'s planner has a Today page with just 3 things, '
                'phone call scripts, a reminders checklist and a reset card, plus a spreadsheet that shows what\'s urgent. '
                'Prefer your iPad? There\'s a <a href="/shop/adhd-digital-planner/">digital version</a> with tap-to-go tabs and stickers.</p>'
                '<a class="btn" href="/planners/#planners">See the planner</a> <a class="btn btn-ghost" href="/#plan">Free Kinav tools</a></div>')
    body.append(NOT_ADVICE)
    return path, build_pages.page(path, "Caring for a parent when you have ADHD: practical tips (UK) | Kinav",
                                  "Practical tips for carers with ADHD: one list, phone reminders, call scripts, the paperwork pile, tiny first steps and sharing the load.",
                                  "\n".join(body), updated, kind="guide")


def about_page(updated):
    """Why Kinav exists, in the founder's words. The founder stays anonymous: no name, place or other details about their father."""
    path = "/about/"
    body = ['<div class="stack-sm"><h1>Why I built Kinav</h1>'
            '<p class="lede">Kinav was built by a family carer whose father has dementia.</p></div>',
            '<section class="stack-sm">'
            '<p>When my father was diagnosed with dementia, I didn\'t know where to start.</p>'
            '<p>I was working full time. Overnight I was also learning a new language: needs assessments, Attendance Allowance, Lasting Power of Attorney, '
            'CQC ratings, care home fees. Every answer seemed to lead to three more questions, and each one was on a different website, behind a phone queue, '
            'or in a leaflet I couldn\'t find when I needed it.</p>'
            '<p>The hardest part wasn\'t the forms. It was the feeling that I was always one step behind, and that one wrong decision could cost my father '
            'his home, his savings or his dignity.</p>'
            '<p>So I started writing things down: the questions to ask, the letters that worked, which care homes near us were actually rated well, '
            'what the council had to do and what it didn\'t.</p>'
            '<p>Kinav is those notes, made into something anyone can use.</p></section>',
            '<section class="panel"><h2>What I promised myself when I built it</h2><ul>'
            '<li><b>Free where it matters.</b> Finding care, working out costs, checking benefits and writing to the council will always be free.</li>'
            '<li><b>Only good care.</b> We only list care rated Good or Outstanding by CQC, and care homes can\'t pay to be listed.</li>'
            '<li><b>Nothing about your family is stored.</b> No sign-up, no selling your details.</li>'
            '<li><b>Plain English.</b> Written for a tired person at 11pm, not for a professional.</li></ul></section>',
            '<section class="stack-sm"><p>Kinav doesn\'t give medical or legal advice. It points you to the people who can, like your GP, Citizens Advice, '
            'Carers UK and Age UK. What it does is help you feel less alone, and a little more in control.</p>'
            '<p>If you\'re caring for someone right now: you\'re doing better than you think.</p>'
            '<p><b>The Kinav team</b></p></section>',
            '<div class="cta"><p><b>Where do I start?</b> Answer 3 quick questions in the free Kinav app and get your first steps.</p>'
            '<a class="btn" href="/#start">Open Kinav</a></div>']
    return path, build_pages.page(path, "About Kinav: built by a family carer | Kinav",
                                  "Why Kinav exists: free, independent help for families caring for an older parent in England, built by a carer whose father has dementia.",
                                  "\n".join(body), updated, kind="guide")


def planners_page(updated):
    """Kinav's printable planners and calendars, with links to the Etsy shop. Free tools on kinav.co.uk stay free."""
    path = "/planners/"
    def card(k, name, line, q):
        # Straight to the listing when we have its link, otherwise a search for it inside the Kinav shop.
        link = LISTING_LINKS.get(k) or SHOP_SEARCH % urllib.parse.quote_plus(q)
        return ('<a class="pp" href="%s" rel="noopener"><img src="/shop-img/%s.jpg" alt="" loading="lazy" width="420" height="420">'
                '<span><b>%s</b><small>%s</small><em>See it in the Kinav Etsy shop ›</em></span></a>' % (e(link), k, e(name), e(line)))
    jump = " · ".join('<a href="#%s">%s</a>' % (anchor, e(title)) for title, anchor, _ in PLANNERS)
    body = ['<style>.pp-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:14px}'
            '.pp{display:flex;flex-direction:column;background:var(--surface,#fff);border:1.5px solid var(--line);border-radius:16px;overflow:hidden;text-decoration:none;color:inherit}'
            '.pp img{width:100%;height:auto;aspect-ratio:1;object-fit:cover;display:block;background:#eee}'
            '.pp span{display:flex;flex-direction:column;gap:4px;padding:12px 14px 14px}.pp b{font-size:17px;line-height:1.25}.pp small{font-size:14px;color:var(--muted,#5b6770)}'
            '.pp em{font-style:normal;font-weight:700;color:var(--accent,#1f5f7a);font-size:14px;margin-top:4px}.pp:hover{border-color:var(--accent,#1f5f7a)}'
            '@media(max-width:560px){.pp-grid{gap:10px}.pp{flex-direction:row;align-items:center}.pp img{width:104px;height:104px;flex:none}.pp span{padding:10px 12px}.pp b{font-size:16px}}</style>',
            crumbs(), '<div class="stack-sm"><h1>Printable planners and calendars for carers</h1>'
            '<p class="lede">Planners, checklists and calendars to print or fill in on screen, made in the UK by Kinav for families caring for an older parent.</p>'
            '<p class="small">%s</p></div>' % jump,
            '<p class="panel small">Everything free on kinav.co.uk stays free. These printables are sold in the Kinav shop on Etsy, which helps keep Kinav running. '
            'Links open Etsy. To come back to Kinav, use your back button or swipe back.</p>']
    for title, anchor, items in PLANNERS:
        free = ('<div class="panel"><p><b>Free:</b> <a href="/activities/christmas/">24 Christmas activities for care homes and older relatives</a>, '
                'one for every day of December, with lists to print.</p></div>') if anchor == "christmas" else ""
        body.append('<section class="stack-sm" id="%s"><h2>%s</h2>%s<div class="pp-grid">%s</div></section>' % (anchor, e(title), free, "".join(card(*it) for it in items)))
    body.append('<section class="panel"><h2>Free printables</h2><div class="grid">'
                '<a href="/printables/emergency-information-sheet/">Emergency information sheet for the fridge</a>'
                '<a href="/printables/important-phone-numbers-list/">Large-print phone numbers list</a>'
                '<a href="/printables/before-discharge-questions-for-the-ward/">Questions before they leave hospital</a>'
                '<a href="/printables/no-cold-callers-door-sign/">No cold callers door sign</a>'
                '<a href="/activities/christmas/">24 free Christmas activities</a>'
                '<a href="/letters/">Free letter templates</a></div></section>')
    body.append('<p class="small"><a href="%s" rel="noopener">See everything in the Kinav shop on Etsy ›</a></p>' % SHOP)
    return path, build_pages.page(path, "Printable planners and calendars for carers of older parents (UK) | Kinav",
                                  "Printable planners, checklists and calendars for families caring for an older parent in the UK: care binder, budget planner, 2027 large-print calendar, Christmas gift planner and more.",
                                  "\n".join(body), updated, kind="guide")


def shop_pages(updated):
    """One short page per Etsy product, so Pinterest pins can link to kinav.co.uk (Pinterest only auto-publishes links on
    the claimed domain). Each page shows the product and a big button to its Etsy listing."""
    try:
        with open(os.path.join(HOME, "update", "shop_pins.json"), encoding="utf-8") as f:
            about = {}
            for p in json.load(f):
                if p["slug"].endswith("-a") or p["key"] not in about:
                    about[p["key"]] = p["description"].replace(" Instant download from Kinav on Etsy. Made in the UK.", "")
    except OSError:
        about = {}
    names = {k: (n, l) for _, _, items in PLANNERS for k, n, l, _ in items}
    pages = []
    for k, link in LISTING_LINKS.items():
        if k not in names:
            continue
        name, line = names[k]
        path = "/shop/%s/" % k
        body = ['<style>.shop-hero{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:24px;align-items:center}'
                '.shop-hero img{width:100%;height:auto;border-radius:16px;display:block}'
                '.btn-etsy{display:inline-block;font-size:19px;padding:14px 26px}'
                '@media(max-width:640px){.shop-hero{grid-template-columns:1fr}}</style>',
                '<nav class="crumbs" aria-label="Breadcrumb"><a href="/planners/">Printable planners</a></nav>',
                '<div class="shop-hero"><img src="/shop-img/%s.jpg" alt="%s" width="420" height="420">'
                '<div class="stack-sm"><h1>%s</h1><p class="lede">%s</p>%s'
                '<p><a class="btn btn-etsy" href="%s" rel="noopener">See it on Etsy ›</a></p>'
                '<p class="small muted">Instant download from the Kinav shop on Etsy. Made in the UK. To come back here, use your back button.</p></div></div>'
                % (k, e(name), e(name), e(line), ('<p>%s</p>' % e(about[k])) if about.get(k) else "", e(link)),
                '<section class="panel"><h2>Free help from Kinav</h2><div class="grid">'
                '<a href="/planners/">All printable planners and calendars</a><a href="/guides/">Free step-by-step guides</a>'
                '<a href="/letters/">Free letter templates</a><a href="/benefits-calculator/">Benefits calculator</a></div></section>']
        pages.append((path, build_pages.page(path, "%s: printable for carers (UK) | Kinav" % name, "%s %s" % (name + ".", line),
                                             "\n".join(body), updated, kind="guide")))
    return pages


# Each free page points to the Kinav product that helps with the same job (exact paths first, then by section).
CROSS_SELL = {
    "/guides/how-to-claim-attendance-allowance/": "attendance-allowance", "/benefits-calculator/": "attendance-allowance",
    "/guides/how-to-choose-a-care-home/": "care-home-visit-pack", "/guides/care-home-contract-checklist/": "moving-into-a-care-home",
    "/guides/leaving-hospital-discharge-checklist/": "hospital-discharge", "/printables/before-discharge-questions-for-the-ward/": "hospital-discharge",
    "/letters/hospital-discharge-planning-letter/": "hospital-discharge", "/plans/after-a-fall-or-hospital-stay/": "hospital-discharge",
    "/guides/how-to-make-a-lasting-power-of-attorney/": "lpa-organiser", "/guides/no-lasting-power-of-attorney-deputyship/": "lpa-organiser",
    "/guides/care-needs-assessment-how-to-prepare/": "needs-assessment", "/letters/letter-asking-the-council-for-a-care-needs-assessment/": "needs-assessment",
    "/plans/caring-for-someone-with-dementia/": "dementia-planner", "/plans/end-of-life-care-for-a-parent/": "planning-ahead",
    "/guides/how-to-claim-carers-allowance/": "carers-budget-planner", "/care-cost-calculator/": "carers-budget-planner",
    "/will-they-have-to-sell-the-house-to-pay-for-care/": "bundle", "/articles/christmas-signs-parent-needs-help/": "bundle",
    "/guides/how-to-apply-for-a-blue-badge/": "bundle", "/guides/nhs-continuing-healthcare-checklist-and-assessment/": "letter-pack",
    "/printables/emergency-information-sheet/": "life-admin-binder", "/printables/important-phone-numbers-list/": "adhd-fridge-cards",
    "/printables/no-cold-callers-door-sign/": "life-admin-binder", "/printables/large-print-calendar-2027/": "calendar-2027", "/printables/day-and-date-clock/": "calendar-2027", "/printables/reminiscence-questions/": "reminiscence-cards", "/printables/daily-routine-chart/": "dementia-planner", "/printables/family-care-handover-sheet/": "daily-log", "/printables/monthly-caring-costs-sheet/": "carers-budget-planner", "/printables/what-to-talk-about-in-a-care-home-visit/": "reminiscence-cards", "/articles/day-centres/": "reminiscence-cards",
}
CROSS_SECTIONS = [("/letters/", "letter-pack"), ("/plans/", "care-planner"), ("/guides/", "care-planner"), ("/articles/", "bundle")]
IN_BUNDLE = {"care-home-visit-pack", "care-planner", "letter-pack", "hospital-discharge"}


def cross_sell(path, html_text):
    """Adds a 'from the Kinav shop' card for the matching product, above the footer."""
    k = CROSS_SELL.get(path) or next((v for pre, v in CROSS_SECTIONS if path.startswith(pre)), None)
    names = {key: (n, l) for _, _, items in PLANNERS for key, n, l, _ in items}
    if not k or k not in LISTING_LINKS or k not in names or "/shop/" in path or path in ("/planners/", "/about/"):
        return html_text
    name, line = names[k]
    extra = ""
    if k in IN_BUNDLE:
        extra = '<p class="small">Or get it in the <a href="%s" rel="noopener">Elderly Parent Care Bundle</a>, with the care planner, letters and checklists, for less.</p>' % e(LISTING_LINKS["bundle"])
    card = ('<section class="panel stack-sm"><h2>Make it easier</h2>'
            '<a class="pp" href="%s" rel="noopener" style="display:flex;gap:14px;align-items:center;text-decoration:none;color:inherit">'
            '<img src="/shop-img/%s.jpg" alt="" loading="lazy" width="110" height="110" style="width:110px;height:110px;border-radius:12px;flex:none">'
            '<span><b>%s</b><br><small>%s</small><br><em style="font-style:normal;font-weight:700">See it in the Kinav shop on Etsy ›</em></span></a>%s'
            '<p class="small muted">Everything on kinav.co.uk stays free. The shop helps keep Kinav running.</p></section>\n'
            % (e(LISTING_LINKS[k]), k, e(name), e(line), extra))
    return html_text.replace('<footer class="tiny muted">', card + '<footer class="tiny muted">', 1)


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
    "short": ("complaint-letter-home-care-visits-cut-short-or-missed", "Complaint letter: home care visits cut short or missed"),
    "provider": ("complaint-letter-to-a-care-home-or-care-agency", "Complaint letter to a care home or care agency"),
    "fee": ("letter-to-question-a-care-home-fee-increase", "Letter to question a care home fee increase"),
    "nhs": ("nhs-complaint-letter-gp-or-hospital", "NHS complaint letter (GP or hospital)"),
    "cqc": ("how-to-tell-cqc-about-poor-care", "Tell CQC about poor care: letter template"),
    "safeguard": ("report-a-safeguarding-concern-letter", "Letter to report a safeguarding concern"),
    "sar": ("subject-access-request-for-care-records", "Subject access request for care records"),
}
LETTER_SOURCES = {
    "needs": [("GOV.UK: apply for a needs assessment", "https://www.gov.uk/apply-needs-assessment-social-services"), GOV_CARE],
    "carer": [("NHS: carer's assessments", "https://www.nhs.uk/social-care-and-support/support-and-benefits-for-carers/carer-assessments/"),
              ("Carers UK: help and advice", "https://www.carersuk.org/help-and-advice/")],
    "discharge": [("NHS: going into hospital and leaving", "https://www.nhs.uk/nhs-services/hospitals/going-into-hospital/"), GOV_CARE],
    "review": [("GOV.UK: apply for a needs assessment", "https://www.gov.uk/apply-needs-assessment-social-services"),
               ("Citizens Advice", "https://www.citizensadvice.org.uk/")],
    "complaint": [("Local Government and Social Care Ombudsman", "https://www.lgo.org.uk/"), ("Citizens Advice", "https://www.citizensadvice.org.uk/")],
    "short": [("Local Government and Social Care Ombudsman", "https://www.lgo.org.uk/"), ("CQC: give feedback on care", "https://www.cqc.org.uk/give-feedback-on-care")],
    "provider": [("Local Government and Social Care Ombudsman", "https://www.lgo.org.uk/"), ("CQC: give feedback on care", "https://www.cqc.org.uk/give-feedback-on-care")],
    "fee": [("CMA: care homes consumer law advice", "https://www.gov.uk/government/publications/care-homes-consumer-law-advice-for-providers"), ("Age UK: care and support", "https://www.ageuk.org.uk/information-advice/care/")],
    "nhs": [("NHS: how to complain to the NHS", "https://www.nhs.uk/using-the-nhs/about-the-nhs/how-to-complain-to-the-nhs/"), ("Parliamentary and Health Service Ombudsman", "https://www.ombudsman.org.uk/")],
    "cqc": [("CQC: give feedback on care", "https://www.cqc.org.uk/give-feedback-on-care")],
    "safeguard": [("NHS: abuse and neglect of adults at risk", "https://www.nhs.uk/social-care-and-support/help-from-social-services-and-charities/abuse-and-neglect-adults-at-risk/"), GOV_CARE],
    "sar": [("ICO: your right of access", "https://ico.org.uk/for-the-public/your-right-to-get-copies-of-your-data/")],
}
APP_JS = os.path.join(APP, "app.js")
JSC = "/System/Library/Frameworks/JavaScriptCore.framework/Versions/A/Helpers/jsc"
LETTER_CACHE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "letter_samples.json")
SAMPLE_JS = r"""
var out = LETTERS.map(function (l) {
  var v = {}, t = {};
  Object.keys(LT_FIELDS).forEach(function (k) { v[k] = "[" + LT_FIELDS[k][0].replace(/ \(optional\)/, "").toLowerCase() + "]"; });
  v.hours = "[number]"; v.rel = "[daughter or son]";
  l.ticks.forEach(function (k) { t[k] = true; });
  var hd = ltHead(l, v), to = hd.to, dear = hd.dear;
  var text = [v.you, v.contact, "[date]", "", to.join("\n"), "", dear, "", l.subject + ": " + v.them, ""].join("\n") + "\n" +
    l.body(v, t).filter(Boolean).join("\n\n") + "\n\nYours sincerely,\n\n" + v.you;
  return { id: l.id, name: l.name, when: l.when, ticks: l.ticks.map(function (k) { return LT_TICKS[k]; }), text: text };
});
print(JSON.stringify(out));
"""


def letter_samples():
    """The letter texts, worked out from app.js with JavaScriptCore on a Mac and saved, so the weekly
    update on GitHub (not a Mac) can rebuild the letter pages from the saved copy."""
    if not os.path.exists(JSC):
        with open(LETTER_CACHE, encoding="utf-8") as f:
            return json.load(f)
    with open(APP_JS, encoding="utf-8") as f:
        js = f.read()
    start, end = js.index("  var LT_FIELDS = {"), js.index("\n  function ltState")
    out = subprocess.run([JSC, "-e", js[start:end] + SAMPLE_JS], check=True, capture_output=True, text=True).stdout
    samples = json.loads(out)
    with open(LETTER_CACHE, "w", encoding="utf-8") as f:
        json.dump(samples, f, ensure_ascii=False, indent=1)
    return samples


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
    for folder in ("guides", "plans", "articles", "care-cost-calculator", "benefits-calculator", "ask-a-specialist", "will-they-have-to-sell-the-house-to-pay-for-care", "letters", "printables", "planners", "about", "shop", "activities"):
        shutil.rmtree(os.path.join(APP, folder), ignore_errors=True)
    pages = [kit_page(k, updated) for k in kc["kits"] if k["id"] in KIT_PAGES]
    pages += [plan_page(key, p, updated) for key, p in kc["plans"].items() if key in PLAN_PAGES]
    import datetime as _dt
    today = _dt.date.today().isoformat()
    kc["articles"] = [a for a in kc["articles"] if not a.get("from") or a["from"] <= today]
    pages += [article_page(a, kc["plans"], updated) for a in kc["articles"]]
    pages += [costs_page(updated), benefits_page(updated), specialist_page(updated), house_page(updated), door_sign_page(updated), discharge_sheet_page(updated), cold_callers_page(updated), phone_list_page(updated), emergency_sheet_page(updated), planners_page(updated), about_page(updated), adhd_page(updated)]
    pages += shop_pages(updated)
    import build_activities
    import build_free
    import build_months
    pages += build_activities.pages(updated) + build_months.pages(updated) + build_free.pages(updated)
    samples = letter_samples()
    pages += [letter_page(l, updated) for l in samples if l["id"] in LETTER_PAGES] + [letters_index(samples, updated)]
    pages = [(path, cross_sell(path, text)) for path, text in pages]
    for path, text in pages:
        save(path.strip("/"), text)

    # Guides index
    def links(prefix, names):
        return '<div class="grid">%s</div>' % "".join('<a href="%s">%s</a>' % (p, e(n)) for p, n in names if p.startswith(prefix))
    kits = [("/guides/%s/" % KIT_PAGES[k["id"]], k["name"]) for k in kc["kits"] if k["id"] in KIT_PAGES]
    plans = [("/plans/%s/" % PLAN_PAGES[k], p["title"]) for k, p in kc["plans"].items() if k in PLAN_PAGES]
    arts = [("/articles/%s/" % a["id"], a["title"]) for a in kc["articles"]] + [("/articles/caring-with-adhd/", "Caring for a parent when you have ADHD")]
    body = ['<div class="stack-sm"><h1>Guides for families caring for an older parent</h1>'
            '<p class="lede">Free step-by-step guides, 30-day plans and tools for carers in England.</p></div>',
            '<section class="panel"><h2>Tools</h2><div class="grid"><a href="/care-cost-calculator/">Care cost calculator</a>'
            '<a href="/benefits-calculator/">Benefits calculator</a><a href="/care/">Care homes and care at home by area</a>'
            '<a href="/ask-a-specialist/">Ask a nurse or specialist</a><a href="/will-they-have-to-sell-the-house-to-pay-for-care/">Will they have to sell the house?</a>'
            '<a href="/letters/">Free letter templates</a><a href="/planners/">Printable planners and calendars</a></div></section>',
            '<section class="panel" id="kits"><h2>Step-by-step guides</h2>%s</section>' % links("/guides/", kits),
            '<section class="panel" id="plans"><h2>30-day plans</h2>%s</section>' % links("/plans/", plans),
            '<section class="panel" id="articles"><h2>Articles for carers</h2>%s</section>' % links("/articles/", arts), NOT_ADVICE]
    save("guides", build_pages.page("/guides/", "Guides for family carers: care homes, costs, benefits and plans | Kinav",
                                    "Free guides for families caring for an older parent in England: choosing a care home, care costs, benefits, Blue Badge, hospital discharge and 30-day plans.",
                                    "\n".join(body), updated, kind="guide"))
    council_pages(kc, updated)
    print("Guide pages: %d" % (len(pages) + 1))
    write_llms(pages)
    write_pins(pages)


def council_pages(kc, updated):
    """One page per council: how to ask that council for a care needs assessment. Rebuilt with the weekly data."""
    try:
        with open(os.path.join(APP, "data", "index.json"), encoding="utf-8") as f:
            idx = json.load(f)
    except OSError:
        return
    names = kc.get("councils", {})
    for c in idx["councils"]:
        info = names.get(c["s"])
        if not info or not os.path.isdir(os.path.join(APP, "care", c["s"])):
            continue
        full, area, slug = info[0], c["n"].replace(", City of", "").replace(", County of", ""), c["s"]
        gov = "https://www.gov.uk/apply-needs-assessment-social-services/%s" % (info[1] if len(info) > 1 else slug)
        path = "/care/%s/needs-assessment/" % slug
        body = ['<nav class="crumbs" aria-label="Breadcrumb"><a href="/care/">England</a> › <a href="/care/%s/">%s</a></nav>' % (slug, e(area)),
                '<div class="stack-sm"><h1>Ask %s for a care needs assessment</h1><p class="lede">Anyone in %s who seems to need care or support can ask '
                '%s for an assessment. It\'s free, whatever their savings, and it\'s how the council decides what help it can arrange.</p></div>' % (e(full), e(area), e(full)),
                '<div class="cta"><p>Ask online on %s\'s website, or let Kinav write the letter for you, ready to email.</p>'
                '<a class="btn" href="%s" rel="noopener" target="_blank">Go to %s</a> <a class="btn btn-ghost" href="/#letter-needs">Write the letter</a></div>' % (e(full), gov, e(full)),
                '<section class="panel"><h2>How it works</h2><ol class="steps">'
                '<li><b>Ask adult social care</b><br><span class="muted">Contact %s online, by phone or with a letter. You can ask on their behalf.</span></li>'
                '<li><b>Prepare</b><br><span class="muted">Keep a diary for a week of what they need help with, day and night, and write down what family do now and can\'t keep doing.</span></li>'
                '<li><b>The assessment</b><br><span class="muted">At home, by phone or by video. Family can be there. If they\'d struggle to take part and have no one to help, the council must offer an advocate.</span></li>'
                '<li><b>The decision</b><br><span class="muted">The council tells you in writing whether they meet the national eligibility criteria. If they do, it writes a care and support plan with you.</span></li>'
                '<li><b>Paying for care</b><br><span class="muted">A separate financial assessment works out what they pay. With savings over £23,250 they usually pay the full cost at first; below £14,250, savings aren\'t counted.</span></li>'
                '<li><b>If you disagree</b><br><span class="muted">Ask for a review, then complain if needed. After that, the Local Government and Social Care Ombudsman can look into it, free.</span></li>'
                '</ol><p><a href="/guides/care-needs-assessment-how-to-prepare/">How to prepare: full checklist ›</a></p></section>' % e(full),
                '<section class="panel"><h2>Ask for a carer\'s assessment too</h2><p>If you help look after them, you have the right to your own assessment from %s, '
                'free, whatever your income. <a href="/letters/carers-assessment-request-letter/">Carer\'s assessment letter ›</a></p></section>' % e(full),
                '<section class="panel"><h2>Care in %s</h2><p>%d care services in %s are rated Good or Outstanding by CQC. '
                '<a href="/care/%s/">See care homes and care at home in %s ›</a></p></section>' % (e(area), c.get("c", 0), e(area), slug, e(area)),
                sources_html([("GOV.UK: apply for a needs assessment", "https://www.gov.uk/apply-needs-assessment-social-services"), GOV_CARE]),
                '<p class="panel small">General information about care in England, not legal advice. Kinav isn\'t part of %s.</p>' % e(full)]
        save(path.strip("/"), build_pages.page(path, "How to ask %s for a care needs assessment | Kinav" % full,
                                               "Ask %s for a free care needs assessment: how to ask, how to prepare, what happens next and how paying for care works in %s." % (full, area),
                                               tel("\n".join(body)), updated, kind="guide"))


def write_pins(pages):
    """RSS feed for Pinterest: one item per page that has a picture in app/pins (made by make_pins.py).
    Each item keeps the date it first appeared (update/pin_dates.json), so Pinterest can tell what's new."""
    import html
    import datetime
    from email.utils import formatdate
    dates_file = os.path.join(HOME, "update", "pin_dates.json")
    try:
        with open(dates_file, encoding="utf-8") as f:
            dates = json.load(f)
    except OSError:
        dates = {}
    now = datetime.datetime.now(datetime.timezone.utc)
    items = []
    for path, text in sorted(pages):
        slug = path.strip("/").split("/")[-1]
        img = os.path.join(APP, "pins", slug + ".jpg")
        if not os.path.exists(img):
            continue
        # Spread first-time dates a minute apart, so a batch of new pins doesn't share one timestamp.
        if slug not in dates:
            dates[slug] = (now - datetime.timedelta(minutes=len(items))).timestamp()
        title = html.unescape(re.search(r"<title>(.*?)</title>", text).group(1)).replace(" | Kinav", "")
        desc = html.unescape(re.search(r'<meta name="description" content="(.*?)"', text).group(1))
        url = "https://kinav.co.uk" + path
        pic = "https://kinav.co.uk/pins/%s.jpg" % slug
        items.append((dates[slug], "<item><title>%s</title><link>%s</link><guid isPermaLink=\"true\">%s</guid><pubDate>%s</pubDate><description>%s</description>"
                     '<enclosure url="%s" length="%d" type="image/jpeg"/><media:content url="%s" medium="image" type="image/jpeg" width="1000" height="1500"/></item>'
                     % (e(title), url, url, formatdate(dates[slug], usegmt=True), e(desc), pic, os.path.getsize(img), pic)))
    items.sort(key=lambda x: -x[0])
    with open(dates_file, "w", encoding="utf-8") as f:
        json.dump(dates, f, indent=0, sort_keys=True)
    with open(os.path.join(APP, "pins.xml"), "w", encoding="utf-8") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n<rss version="2.0" xmlns:media="http://search.yahoo.com/mrss/"><channel><title>Kinav: guides and letters for family carers</title>'
                "<link>https://kinav.co.uk/</link><description>Free step-by-step guides, letters and plans for families caring for an older parent in England.</description>"
                "<language>en-gb</language><lastBuildDate>%s</lastBuildDate>%s</channel></rss>\n" % (formatdate(usegmt=True), "".join(x[1] for x in items)))

def write_llms(pages):
    """A plain summary for AI assistants (llmstxt.org), listing every guide page."""
    import html
    title = {path: html.unescape(re.search(r"<title>(.*?)</title>", text).group(1)).replace(" | Kinav", "") for path, text in pages}
    def section(head, prefix):
        return "## %s\n\n%s\n" % (head, "\n".join("- [%s](https://kinav.co.uk%s)" % (t, p) for p, t in sorted(title.items()) if p.startswith(prefix)))
    tools = [p for p in title if not p.startswith(("/guides/", "/letters/", "/plans/", "/articles/"))]
    out = ["# Kinav", "",
           "> Kinav is a free website and app for families arranging care for an older parent or relative in England. "
           "It lists care homes and home care providers with their latest CQC ratings, and has step-by-step guides, "
           "30-day plans for common conditions, a benefits calculator, a care cost calculator and free letter templates. "
           "No sign-up, no ads, and nothing about the family is stored. Kinav gives general information only, not health, "
           "medical, legal or financial advice.", "",
           "Useful for people in England who want to know how to arrange or pay for care for an older relative, what benefits "
           "they or their parent can claim, or how to deal with the council, the NHS or a care home.", "",
           "## Tools\n\n- [Kinav app: find care by postcode](https://kinav.co.uk/)\n- [Care homes and home care by council area](https://kinav.co.uk/care/)\n%s\n"
           % "\n".join("- [%s](https://kinav.co.uk%s)" % (title[p], p) for p in sorted(tools)),
           section("Step-by-step guides", "/guides/"), section("Letter templates", "/letters/"),
           section("30-day plans for carers", "/plans/"), section("Articles", "/articles/")]
    with open(os.path.join(APP, "llms.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(out))


if __name__ == "__main__":
    import datetime
    main(datetime.date.today().strftime("%-d %B %Y"))

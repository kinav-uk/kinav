"""Free Christmas printables that people search for, each a taster of a £1.99 Kinav pack: one large-print word search
(with answers), 2 large-print bingo cards with calling words, a Christmas dinner cooking timetable and a Christmas
card list. Print from the page; nothing is saved or sent. build_guides adds the shop card for each (CROSS_SELL).
"""
import random

import build_pages
from build_free import SHEET_CSS, sheet

WS = "/printables/large-print-christmas-word-search/"
BINGO = "/printables/large-print-christmas-bingo/"
DINNER = "/printables/christmas-dinner-cooking-timetable/"
CARDS = "/printables/christmas-card-list/"
XMAS_CSS = ('<style>.xm{background:#fff;color:#18232e;border:3px solid #1e5b3f;border-radius:18px;padding:18px;max-width:760px}'
            '.xm h2{font-size:28px;margin:0 0 6px;color:#a3262a}.xm .note{font-size:12px;margin:10px 0 0}'
            '.shopnote{border:2px solid #e9c46a;background:#fdf6e3;border-radius:16px;padding:16px}'
            '@media print{@page{margin:10mm}.xm{border:0;padding:0;max-width:none}.xm h2{color:#000}}</style>')
SHOP_IMG = '<img src="/shop-img/%s.jpg" alt="" width="110" height="110" style="width:110px;height:110px;border-radius:12px;flex:none">'


def shop(k, head, line, links):
    """The 'want the full pack?' box, straight under the free printable."""
    if k not in links:
        return ""
    return ('<section class="shopnote noprint stack-sm"><h2>%s</h2>'
            '<a href="%s" rel="noopener" style="display:flex;gap:14px;align-items:center;text-decoration:none;color:inherit">%s'
            '<span>%s<br><b style="color:#a3262a">See the full pack in the Kinav shop on Etsy ›</b></span></a>'
            '<p class="small muted">An instant download to print at home. Everything on kinav.co.uk stays free.</p></section>' % (head, links[k], SHOP_IMG % k, line))


def grid(words, seed, n=10):
    """Words across and down only, never backwards, as in the paid pack."""
    rnd = random.Random(seed)
    for _ in range(2000):
        g = [[None] * n for _ in range(n)]; pos = {}; ok = True
        for wd in sorted(words, key=len, reverse=True):
            for _ in range(300):
                d = rnd.choice([(0, 1), (1, 0)])
                r = rnd.randrange(n - (len(wd) - 1) * d[0]); c = rnd.randrange(n - (len(wd) - 1) * d[1])
                cells = [(r + i * d[0], c + i * d[1]) for i in range(len(wd))]
                if all(g[a][b] in (None, ch) for (a, b), ch in zip(cells, wd)):
                    for (a, b), ch in zip(cells, wd):
                        g[a][b] = ch
                    pos[wd] = cells; break
            else:
                ok = False; break
        if ok:
            for a in range(n):
                for b in range(n):
                    g[a][b] = g[a][b] or rnd.choice("ABCDEFGHIKLMNOPRSTUWY")
            return g, {cell for cells in pos.values() for cell in cells}
    raise RuntimeError("couldn't place " + str(words))


def ws_page(updated, links):
    words = "WRAPPING RIBBON PAPER CARDS STAMPS TAGS LIST SHOPS BAGS POSTMAN".split()
    g, ans = grid(words, 1225)
    rows = "".join("<tr>%s</tr>" % "".join('<td%s>%s</td>' % (' class="a"' if (a, b) in ans else "", g[a][b]) for b in range(10)) for a in range(10))
    ticks = "".join("<li>%s</li>" % w.title() for w in sorted(words))
    body = [XMAS_CSS, '<style>.ws{border-collapse:collapse;margin:8px auto;width:100%;max-width:560px;table-layout:fixed}'
            '.ws td{text-align:center;font:700 clamp(20px,6vw,34px)/1 Arial,sans-serif;padding:0;height:clamp(32px,9vw,54px);border:1px solid #e6dccb}'
            '.ws.show td.a{background:#e9c46a}.wl{columns:2;font-size:20px;list-style:none;padding:0;margin:12px 0 0}.wl li:before{content:"\\2610  "}'
            '@media print{.ws td{font-size:30px;height:50px}.ws.show td.a{background:none}}</style>',
            '<div class="stack-sm noprint"><h1>Free large-print Christmas word search</h1>'
            '<p class="lede">A Christmas shopping word search in big, clear letters, for older relatives, family and care homes. '
            'Words go across and down only, never backwards, so they\'re easier to find.</p>'
            '<p><button class="btn" type="button" onclick="print()">Print the word search</button> '
            '<button class="btn btn-ghost" type="button" onclick="document.querySelector(\'.ws\').classList.toggle(\'show\')">Show or hide the answers</button></p></div>',
            '<div class="xm"><h2>Christmas shopping</h2><table class="ws" aria-label="Word search grid">%s</table>'
            '<p style="font-weight:700;margin:12px 0 0">Find these 10 words</p><ul class="wl">%s</ul>'
            '<p class="note">Large-print Christmas word search · Free from kinav.co.uk</p></div>' % (rows, ticks),
            shop("christmas-word-search", "Want 12 more?", "<b>Large-print Christmas word searches</b><br>12 puzzles: Christmas dinner, the Nativity, "
                 "Santa's reindeer, pantomime, Boxing Day and more, with the answers at the back.", links),
            '<section class="panel noprint"><h2>Tips</h2><ul><li>Print one for each person, or do it together on a big screen.</li>'
            '<li>Use a highlighter instead of a pen, if that\'s easier to hold.</li><li>Talk about the words as you find them: who did the Christmas shopping when they were young?</li></ul>'
            '<p>More free ideas: <a href="/activities/christmas/">24 free Christmas activities</a> and <a href="%s">free large-print Christmas bingo</a>.</p></section>' % BINGO]
    return WS, build_pages.page(WS, "Free large-print Christmas word search for seniors: printable, with answers | Kinav",
                                "A free large-print Christmas word search to print, for older people, family and care homes. Big letters, across and down only, with the answers.",
                                "\n".join(body), updated, kind="guide")


BINGO_WORDS = ["Robin", "Holly", "Cracker", "Stocking", "Snowman", "Pudding", "Star", "Bell", "Candle", "Reindeer", "Mince pie", "Present",
               "Turkey", "Angel", "Sleigh", "Snowflake", "Tinsel", "Santa", "Carol", "Wreath", "Bauble", "Chimney", "Sprouts", "Elf"]


def bingo_page(updated, links):
    rnd = random.Random(2412)
    cards = [rnd.sample(BINGO_WORDS, 16) for _ in range(2)]
    def card(n, ws):
        return ('<div class="xm bc"><h2>Christmas bingo: card %d</h2><table class="bg">%s</table><p class="note">Large-print Christmas bingo · Free from kinav.co.uk</p></div>'
                % (n, "".join("<tr>%s</tr>" % "".join("<td>%s</td>" % w for w in ws[r * 4:r * 4 + 4]) for r in range(4))))
    body = [XMAS_CSS, '<style>.bg{border-collapse:collapse;width:100%;table-layout:fixed}.bg td{border:2px solid #a3262a;text-align:center;'
            'font:700 clamp(12px,3.5vw,26px)/1.15 Arial,sans-serif;height:clamp(64px,17vw,110px);padding:3px;background:#fbf5ec;overflow-wrap:anywhere}'
            '.bc{margin:14px 0}.calls{columns:3;font-size:19px;list-style:none;padding:0}@media(max-width:560px){.calls{columns:2}}@media print{.bc{break-after:page}.bg td{height:150px;font-size:30px}}</style>',
            '<div class="stack-sm noprint"><h1>Free large-print Christmas bingo for seniors</h1>'
            '<p class="lede">Two Christmas word bingo cards in big, clear letters, plus the calling words. For older relatives, family gatherings and care homes.</p>'
            '<p><button class="btn" type="button" onclick="print()">Print the cards</button></p></div>',
            card(1, cards[0]), card(2, cards[1]),
            '<div class="xm"><h2>Calling words</h2><p>Print this page, cut the words out and pull them from a bowl. Cross off the words as they\'re called: '
            'first to get a line wins, then play on for a full house.</p><ul class="calls">%s</ul></div>' % "".join("<li>%s</li>" % w for w in BINGO_WORDS),
            shop("christmas-bingo", "Playing with more people?", "<b>Large-print Christmas bingo</b><br>20 different cards, calling cards to cut out "
                 "and a caller's checklist, for up to 20 players.", links),
            '<section class="panel noprint"><h2>Tips</h2><ul><li>Play for chocolate coins or small wrapped prizes.</li>'
            '<li>Pair up anyone who finds it hard to see or hold a pen: one calls, one crosses off.</li><li>Say a word about each one as it\'s called: "Who had a real tree?"</li></ul>'
            '<p>More free ideas: <a href="/activities/christmas/">24 free Christmas activities</a> and a <a href="%s">free large-print Christmas word search</a>.</p></section>' % WS]
    return BINGO, build_pages.page(BINGO, "Free large-print Christmas bingo for seniors: printable cards | Kinav",
                                   "Free large-print Christmas bingo cards to print, with calling words. For older people, family Christmas and care homes.",
                                   "\n".join(body), updated, kind="guide")


def dinner_page(updated, links):
    times = ["Night before", "Morning", "", "", "2 hours to go", "", "1 hour to go", "", "30 minutes to go", "Dinner time", "Afternoon"]
    rows = [t or "Row %d" % i for i, t in enumerate(times, 1)]
    html = sheet("Christmas Day cooking timetable", ["Time", "Job", "Who"], rows, "Write each job against its time, working back from dinner")
    for i, t in enumerate(times, 1):
        if not t:
            html = html.replace('<td class="l">Row %d</td>' % i, '<td><input aria-label="Time"></td>')
    body = ['<style>.sh th:nth-child(2){width:46%}</style>']
    return DINNER, build_pages.page(DINNER, "Free Christmas dinner cooking timetable: printable planner | Kinav",
                                    "A free Christmas Day cooking timetable to print or fill in: work back from dinner time, so everything is ready together. With tips for hosting older relatives.",
                                    "\n".join(body + _free(html, "Free Christmas dinner cooking timetable",
                                              "Work back from the time you want to eat, so the turkey, potatoes and veg are ready together. Print it, or type into it here and then print.",
                                              ["Write dinner time first, then work back: when the turkey goes in, when it comes out to rest, when the potatoes go in.",
                                               "Give jobs away: someone on drinks, someone on the table, someone keeping an older guest company.",
                                               "Ask older guests what helps: a chair with arms, softer food, a quiet corner after dinner."],
                                              shop("christmas-dinner-planner", "Planning the whole day?", "<b>Christmas dinner planner</b><br>Who's coming and what they need, "
                                                   "the menu, shopping list, cooking timetable, seating plan and a Christmas week countdown.", links))),
                                    updated, kind="guide")


def cards_page(updated, links):
    html = sheet("Christmas card list", ["Name", "Address", "Sent", "Got one"], ["Row %d" % i for i in range(1, 15)], "Keep it for next year", label_first=False)
    html = html.replace("<th>Name</th>", '<th style="width:28%">Name</th>').replace("<th>Address</th>", '<th style="width:44%">Address</th>')
    return CARDS, build_pages.page(CARDS, "Free Christmas card list printable: track cards sent and received | Kinav",
                                   "A free Christmas card list to print or fill in: names, addresses, sent and received. Keep it for next year.",
                                   "\n".join(_free(html, "Free Christmas card list",
                                                   "Who you've sent cards to, and who sent one back. Print it, or type into it here and then print.",
                                                   ["Start from last year's cards, if you kept them.", "Write cards together with an older relative: they say it, you write it.",
                                                    "Keep the list in the Christmas decorations box for next year."],
                                                   shop("christmas-card-list-tags", "Gift tags too?", "<b>Christmas card list and gift tags</b><br>A fillable card list, "
                                                        "plus 16 large-print gift tags with a big To and From.", links))),
                                   updated, kind="guide")


def _free(html, h1, lede, tips, shopbox):
    return [SHEET_CSS, '<div class="stack-sm noprint"><h1>%s</h1><p class="lede">%s What you type stays on this page: it isn\'t saved or sent anywhere.</p>'
            '<p><button class="btn" type="button" onclick="print()">Print it</button></p></div>' % (h1, lede), html, shopbox,
            '<section class="panel noprint"><h2>Tips</h2><ul>%s</ul><p>More free ideas: <a href="/activities/christmas/">24 free Christmas activities</a>.</p></section>'
            % "".join("<li>%s</li>" % t for t in tips)]


def pages(updated):
    import build_guides as bg
    links = bg.LISTING_LINKS
    return [ws_page(updated, links), bingo_page(updated, links), dinner_page(updated, links), cards_page(updated, links)]

"""Pinterest product feeds: one RSS feed per Pinterest board (app/shop-<board>.xml), linking each pin to its product page on kinav.co.uk (Pinterest
only auto-publishes links on the claimed domain), which has a button to the Etsy listing.
The schedule is update/shop_pins.json (3 a day); a pin joins its feed once its publish time has passed, so Pinterest
picks up a few new pins each day. Run by the publish job every day, and by app/build.py.
Run: python3 update/shop_feeds.py"""
import datetime
import json
import os
from email.utils import formatdate
from xml.sax.saxutils import escape as e

HOME = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APP = os.path.join(HOME, "app")
BOARDS = {"christmas": "Christmas activities for older people and care homes", "planners": "Printable planners for carers",
          "kits": "Caring for an elderly parent (UK)", "dementia": "Dementia activities and support"}


def main(now=None):
    now = now or datetime.datetime.now(datetime.timezone.utc)
    with open(os.path.join(HOME, "update", "shop_pins.json"), encoding="utf-8") as f:
        pins = json.load(f)
    for feed, board in BOARDS.items():
        items = []
        for p in pins:
            when = datetime.datetime.fromisoformat(p["publish"].replace("Z", "+00:00"))
            img = os.path.join(APP, "shop-pins", p["slug"] + ".jpg")
            if p["feed"] != feed or when > now or not os.path.exists(img):
                continue
            pic = "https://kinav.co.uk/shop-pins/%s.jpg" % p["slug"]
            guid = "https://kinav.co.uk/shop-pins/%s" % p["slug"]
            items.append((when, "<item><title>%s</title><link>%s</link><guid isPermaLink=\"false\">%s</guid><pubDate>%s</pubDate><description>%s</description>"
                          '<enclosure url="%s" length="%d" type="image/jpeg"/><media:content url="%s" medium="image" type="image/jpeg" width="1000" height="1500"/></item>'
                          % (e(p["title"]), "https://kinav.co.uk/shop/%s/" % p["key"], guid, formatdate(when.timestamp(), usegmt=True), e(p["description"]), pic, os.path.getsize(img), pic)))
        items.sort(key=lambda x: x[0], reverse=True)
        items = items[:100]   # Pinterest only needs the newest; keeps the feed small
        with open(os.path.join(APP, "shop-%s.xml" % feed), "w", encoding="utf-8") as f:
            f.write('<?xml version="1.0" encoding="UTF-8"?>\n<rss version="2.0" xmlns:media="http://search.yahoo.com/mrss/"><channel>'
                    "<title>Kinav on Etsy: %s</title><link>https://kinav.co.uk/planners/</link><description>Printables for families caring for an older parent, from Kinav's Etsy shop.</description>"
                    "<language>en-gb</language><lastBuildDate>%s</lastBuildDate>%s</channel></rss>\n" % (e(board), formatdate(usegmt=True), "".join(x[1] for x in items)))
        print("shop-%s.xml: %d pins" % (feed, len(items)))


if __name__ == "__main__":
    main()

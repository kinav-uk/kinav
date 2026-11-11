"""Care home activity ideas for every month: /activities/ plus /activities/<month>/. Each month has its dates to plan
around (checked for 2027) and 8 easy activity ideas, with the matching Kinav packs. December points to the 24 free
Christmas activities. Pins: ~/Kinav-Etsy/tools/activity_pins.py.
"""
import html

import build_pages
from build_activities import HUB as XMAS, card, names

e = html.escape
ROOT = "/activities/"

# (slug, month, one line, dates in 2027, 8 ideas: (name, how))
MONTHS = [
 ("january", "January", "A fresh start: cosy afternoons, Burns Night and planning the year ahead.",
  [("1 January", "New Year's Day"), ("25 January", "Burns Night")],
  [("New Year memories", "How did you see the New Year in? Talk about first-footing, Auld Lang Syne and resolutions."),
   ("A Burns Night afternoon", "Shortbread, a poem read aloud, Scottish songs and a tartan to pass round."),
   ("Winter warmers taste test", "Try three soups or hot drinks and vote for a favourite."),
   ("The year ahead calendar", "Make a big wall calendar together and fill in birthdays and outings."),
   ("Snow memories", "Sledging, snowmen and the worst winters people remember."),
   ("Indoor bowls", "Soft balls and a target on the floor. Play seated or standing."),
   ("Seed catalogue browsing", "Look through seed catalogues and choose what to grow this spring."),
   ("Old toys and games", "Bring out marbles, jacks, cards and dominoes, and talk about childhood games.")]),
 ("february", "February", "Valentine's Day, pancakes and the first signs of spring.",
  [("9 February", "Pancake Day (Shrove Tuesday)"), ("14 February", "Valentine's Day")],
  [("Pancake party", "Make or warm pancakes and choose toppings. A pancake race with a frying pan and a beanbag."),
   ("Love stories", "How did people meet their sweethearts? Dances, letters and first dates."),
   ("Valentine's cards", "Make cards for family, staff or each other."),
   ("Love songs sing-along", "Songs from the 1950s and 1960s, with a dance for anyone who wants one."),
   ("Snowdrop spotting", "A short walk or a look out of the window, then press or draw the flowers."),
   ("Wedding photos afternoon", "Ask family to send wedding photos and talk about the day."),
   ("Heart crafts", "Paper hearts, a heart garland or a heart-shaped wreath for the door."),
   ("A sweet shop quiz", "Old sweets and chocolate bars: who remembers them?")]),
 ("march", "March", "Mother's Day, St David's Day, St Patrick's Day and Easter.",
  [("1 March", "St David's Day"), ("7 March", "Mother's Day"), ("17 March", "St Patrick's Day"), ("28 March", "Easter Sunday (clocks go forward 1 hour)")],
  [("Mother's Day memories", "Talk about mums and grandmas: their sayings, recipes and the things they made."),
   ("Daffodil crafts", "Paper or egg-box daffodils for St David's Day."),
   ("A St Patrick's Day afternoon", "Irish songs, a green quiz and soda bread."),
   ("Easter bonnets", "Decorate paper or straw hats and hold a gentle parade."),
   ("Egg decorating", "Hard-boiled or paper eggs, with pens, paint and stickers."),
   ("Spring planting", "Sow cress or bulbs in pots for the windowsill."),
   ("Easter memories", "Hot cross buns, egg rolling and Easter bonnets in years gone by."),
   ("An Easter egg hunt", "A simple hunt indoors or in the garden, with prizes for everyone.")]),
 ("april", "April", "Spring, St George's Day and a little April foolery.",
  [("1 April", "April Fools' Day"), ("23 April", "St George's Day")],
  [("April Fools' stories", "Famous April Fools' jokes and the best tricks people played."),
   ("A St George's Day tea", "Cucumber sandwiches, a cuppa and English songs."),
   ("Spring flower arranging", "Arrange spring flowers in jars for the tables."),
   ("Bird watching", "Put out a feeder and keep a list of the birds that visit."),
   ("Spring cleaning memories", "Beating rugs, whitening the step and other jobs from years ago."),
   ("Garden centre trip or catalogue", "Visit one, or choose plants from a catalogue."),
   ("Rain songs", "Singin' in the Rain and other songs about the weather."),
   ("Lambs and farm memories", "Talk about farms, holidays in the country and animals people kept.")]),
 ("may", "May", "Bank holidays, maypoles and getting out into the garden.",
  [("3 May", "Early May bank holiday"), ("31 May", "Spring bank holiday")],
  [("A May Day ribbon dance", "A small maypole or ribbons on sticks, with music."),
   ("Garden afternoon", "Sit out, pot up plants or deadhead flowers together."),
   ("Seaside day trip memories", "Bank holiday trips, the coach, the beach and fish and chips."),
   ("Flower crowns", "Paper or real flowers threaded into crowns."),
   ("Cream tea", "Scones, jam and cream. Jam first or cream first?"),
   ("Old adverts quiz", "Slogans and jingles from old TV and radio adverts."),
   ("Nature table", "Collect leaves, flowers and stones and make a display."),
   ("Bank holiday sing-along", "Music hall and wartime songs everyone knows.")]),
 ("june", "June", "Summer, Father's Day and Armed Forces Day.",
  [("20 June", "Father's Day"), ("21 June", "Longest day of the year"), ("26 June", "Armed Forces Day")],
  [("Father's Day memories", "Talk about dads and grandads: their jobs, sayings and hobbies."),
   ("A garden party", "Bunting, squash, sandwiches and music outside."),
   ("Strawberries and cream", "Taste strawberries and talk about tennis and summer sport."),
   ("Armed Forces Day", "Share service memories and family stories, and make bunting."),
   ("Summer holidays then", "Holiday camps, caravans and seaside boarding houses."),
   ("Garden games", "Skittles, hoopla and bean bags, played seated or standing."),
   ("Pressed flowers", "Press flowers from the garden and make cards."),
   ("Picnic indoors or out", "Pack a picnic, spread a blanket and enjoy it together.")]),
 ("july", "July", "Summer fun, the seaside and sports days.",
  [],
  [("Seaside afternoon", "Sand in a tray, shells, ice lollies and seaside songs."),
   ("Sports day games", "Egg and spoon, beanbag throwing and a gentle obstacle course."),
   ("Ice cream tasting", "Try three flavours and talk about ice cream vans and wafers."),
   ("School days memories", "School milk, slates, teachers and the last day of term."),
   ("Summer songs", "Songs about summer and holidays, with shakers."),
   ("Outdoor painting", "Paint flowers or the view from the garden."),
   ("Holiday postcards", "Write postcards to family, or look at old ones."),
   ("Fruit kebabs", "Make and share fruit kebabs, after checking dietary needs.")]),
 ("august", "August", "Long days, holidays and the summer bank holiday.",
  [("30 August", "Summer bank holiday")],
  [("A beach in a box", "Shells, sand and seaside smells to pass round."),
   ("Holiday camp memories", "Butlins, Pontins, knobbly knees and talent shows."),
   ("A talent show", "Sing, tell a joke, recite a poem or share a skill."),
   ("Summer fete", "Tombola, guess the weight of the cake and a raffle."),
   ("Cricket afternoon", "Watch a match or play soft-ball cricket indoors."),
   ("Lavender bags", "Fill small bags with dried lavender, and talk about gardens."),
   ("Summer reading", "Read a short story or poem aloud in the garden."),
   ("Barbecue", "Sausages, salads and music outside.")]),
 ("september", "September", "Back to school, harvest and the Battle of Britain.",
  [("15 September", "Battle of Britain Day")],
  [("Harvest festival", "Collect tins for a food bank and sing harvest hymns."),
   ("Back to school memories", "Uniforms, satchels and the walk to school."),
   ("Blackberry picking", "Pick or buy blackberries and talk about crumbles and jam."),
   ("Battle of Britain memories", "Share wartime stories and look at pictures of the planes."),
   ("Apple tasting", "Try different apples and vote for a favourite."),
   ("Autumn leaf art", "Collect leaves and make pictures or prints."),
   ("Handwriting afternoon", "Copybooks, fountain pens and best handwriting."),
   ("Radio favourites", "Old radio shows and the songs people listened to.")]),
 ("october", "October", "Autumn colours, Halloween and the clocks going back.",
  [("31 October", "Halloween (clocks go back 1 hour)")],
  [("Pumpkin decorating", "Decorate pumpkins with paint or stickers, no carving needed."),
   ("Halloween memories", "Apple bobbing, turnip lanterns and old Halloween games."),
   ("Autumn walk", "A short walk to collect conkers, leaves and acorns."),
   ("Conkers", "Talk about conker fights and play a gentle game."),
   ("Soup making", "Make a simple autumn soup together."),
   ("Spooky stories", "Gentle ghost stories, read aloud with a torch."),
   ("Autumn wreath", "Make a door wreath with leaves, pine cones and ribbon."),
   ("Harvest of memories quiz", "Questions about food, farms and the countryside.")]),
 ("november", "November", "Bonfire Night, Remembrance and the start of Christmas planning.",
  [("5 November", "Bonfire Night"), ("11 November", "Armistice Day"), ("14 November", "Remembrance Sunday"), ("30 November", "St Andrew's Day")],
  [("Bonfire Night memories", "Guy Fawkes, sparklers, toffee apples and treacle toffee."),
   ("Firework pictures", "Paint or glitter firework pictures on dark paper."),
   ("Remembrance", "A two-minute silence, poppies, and family stories of service."),
   ("Poppy crafts", "Paper or felt poppies for a display."),
   ("Christmas card making", "Start early: make Christmas cards for families."),
   ("A St Andrew's Day afternoon", "Scottish songs, shortbread and a tartan quiz."),
   ("Winter knitting circle", "Knit, crochet or just chat while others do."),
   ("Plan the Christmas activities", "Choose favourites from our 24 free Christmas activities.")]),
 ("december", "December", "Christmas: one free activity for every day of Advent.",
  [("25 December", "Christmas Day"), ("26 December", "Boxing Day"), ("31 December", "New Year's Eve")],
  []),
]


def month_page(i, m, updated, nm, links):
    slug, name, line, dates, ideas = m
    path = "%s%s/" % (ROOT, slug)
    prev, nxt = MONTHS[i - 1], MONTHS[(i + 1) % 12]
    body = ['<nav class="crumbs" aria-label="Breadcrumb"><a href="%s">Activity ideas by month</a> › %s</nav>' % (ROOT, name),
            '<div class="stack-sm"><h1>Care home activity ideas for %s</h1><p class="lede">%s Easy ideas for care homes, day centres and families with older relatives.</p></div>' % (name, e(line))]
    if dates:
        body.append('<section class="panel"><h2>Dates to plan around in %s 2027</h2><ul>%s</ul></section>'
                    % (name, "".join("<li><b>%s:</b> %s</li>" % (e(d), e(t)) for d, t in dates)))
    if slug == "december":
        body.append('<section class="panel"><h2>24 free Christmas activities</h2><p>One easy activity for every day from 1 to 24 December, '
                    'with what you need, how to run it and lists to print.</p><p><a class="btn" href="%s">See all 24 activities</a></p></section>' % XMAS)
    else:
        body.append('<section class="panel"><h2>%d activity ideas</h2><ol class="steps">%s</ol>'
                    '<p class="small muted">Check dietary needs before anything is eaten, and adapt each idea so everyone can join in.</p></section>'
                    % (len(ideas), "".join("<li><b>%s</b><br><span class=\"muted\">%s</span></li>" % (e(a), e(b)) for a, b in ideas)))
    cards = card("christmas-activity-programme", "For care homes: every day of Advent planned", nm, links) + card("christmas-cards-care-home", "Christmas memory cards for groups", nm, links) \
        if slug in ("november", "december") else card("reminiscence-cards", "For memory and conversation sessions, all year", nm, links)
    body.append('<section class="panel stack-sm noprint"><h2>Ready-made activities</h2>%s'
                '<p class="small muted">Everything on kinav.co.uk stays free. The shop helps keep Kinav running.</p></section>' % cards)
    body.append('<nav class="panel noprint grid" aria-label="More months"><a href="%s%s/">‹ %s</a><a href="%s">All months</a><a href="%s%s/">%s ›</a></nav>'
                % (ROOT, prev[0], prev[1], ROOT, ROOT, nxt[0], nxt[1]))
    return path, build_pages.page(path, "Care home activity ideas for %s: free ideas and dates | Kinav" % name,
                                  "Free care home activity ideas for %s, with the dates to plan around in 2027. Easy activities for care homes, day centres and older relatives." % name,
                                  "\n".join(body), updated, kind="guide")


def root_page(updated, nm, links):
    grid = "".join('<a href="%s%s/"><b>%s</b><br><small class="muted">%s</small></a>' % (ROOT, m[0], m[1], e(m[2])) for m in MONTHS)
    body = ['<div class="stack-sm"><h1>Care home activity ideas for every month</h1>'
            '<p class="lede">Free activity ideas for care homes, day centres and families with older relatives, month by month, '
            'with the special dates to plan around in 2027.</p><p id="now" class="small" hidden></p></div>',
            '<section class="panel"><h2>Choose a month</h2><div class="grid">%s</div></section>' % grid,
            '<section class="panel"><h2>Christmas</h2><p><a href="%s">24 free Christmas activities</a>: one for every day of December.</p></section>' % XMAS,
            '<section class="panel stack-sm"><h2>Ready-made activities</h2>%s%s'
            '<p class="small muted">Everything on kinav.co.uk stays free. The shop helps keep Kinav running.</p></section>'
            % (card("reminiscence-cards", "For memory and conversation sessions, all year", nm, links),
               card("christmas-activity-programme", "For care homes: every day of Advent planned", nm, links)),
            '<script>(function(){var m=["january","february","march","april","may","june","july","august","september","october","november","december"],'
            'N=["January","February","March","April","May","June","July","August","September","October","November","December"],i=new Date().getMonth(),p=document.getElementById("now");'
            'p.hidden=false;p.innerHTML="<b>This month:</b> <a href=\\"/activities/"+m[i]+"/\\">"+N[i]+" activity ideas ›</a>"})();</script>']
    return ROOT, build_pages.page(ROOT, "Care home activity ideas for every month: free calendar of ideas | Kinav",
                                  "Free care home activity ideas for every month of the year, with dates to plan around in 2027: easy activities for care homes, day centres and older relatives.",
                                  "\n".join(body), updated, kind="guide")


def pages(updated):
    nm, links = names()
    return [root_page(updated, nm, links)] + [month_page(i, m, updated, nm, links) for i, m in enumerate(MONTHS)]

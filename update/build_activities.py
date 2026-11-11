"""24 free Christmas activities for care homes and older relatives: one page each, plus /activities/christmas/.
All pages are live from the start, so search engines find them before December; Pinterest gets one a day, 1 to 24 December
(pins made by ~/Kinav-Etsy/tools/activity_pins.py). Each page points to the matching Kinav Christmas packs.
"""
import html
import json

import build_pages

e = html.escape
HUB = "/activities/christmas/"

# (slug, name, one line, what you need, how to run it, make it easier, optional (heading, items) to print, family product, care home product)
DAYS = [
 ("christmas-memory-tree", "A Christmas memory tree", "Everyone adds a Christmas memory to a paper tree, and by the end of the month it's full of stories.",
  ["A big paper tree shape on the wall, or a small real tree", "Paper baubles or stars, cut out ready", "Pens and something to stick them up with"],
  ["Put the tree up somewhere everyone passes.", "Ask one question a day, such as \"What was your best ever Christmas present?\"", "Write each answer on a bauble with the person's first name, or help them write it.", "Read a few out each day, and let people add more whenever they like."],
  ["Offer to write for anyone who would rather talk than write.", "A photo of a bauble with a memory makes a lovely thing to send to family."],
  None, "christmas-cards", "christmas-cards-care-home"),
 ("finish-the-carol", "Finish the carol", "Read the start of a carol line and everyone sings or says the rest. Easy, quick and always gets people joining in.",
  ["This page, printed", "Words for a few carols, if you want to sing on"],
  ["Read the first half of a line slowly and clearly.", "Pause, and let the group finish it, sung or spoken.", "Carry on singing that carol if people want to.", "Ask \"Where did you sing this when you were young?\""],
  ["Start with the best-known lines.", "Hum the tune first if words are hard to find."],
  ("Carol lines to finish", ["Silent night, holy night … all is calm, all is bright", "Hark! the herald angels sing … glory to the newborn King",
   "O come, all ye faithful … joyful and triumphant", "Away in a manger … no crib for a bed", "Once in royal David's city … stood a lowly cattle shed",
   "While shepherds watched their flocks by night … all seated on the ground", "Ding dong merrily on high … in heaven the bells are ringing",
   "God rest ye merry, gentlemen … let nothing you dismay", "Good King Wenceslas looked out … on the feast of Stephen",
   "O little town of Bethlehem … how still we see thee lie", "Jingle bells, jingle bells … jingle all the way", "We wish you a merry Christmas … and a happy New Year"]),
  "retro-christmas-games", "retro-christmas-games-care-home"),
 ("christmas-dinner-memories", "What was on your Christmas table?", "A conversation about Christmas dinners past: who cooked, what was served, and who got the wishbone.",
  ["A cup of tea and a comfortable spot", "Optional: a few pictures of Christmas food to pass round"],
  ["Sit in a small group or one to one.", "Ask one question at a time and give plenty of time to answer.", "Share your own memories too, so it feels like a chat.", "Note any lovely stories to share with family."],
  ["Pictures help people who find words harder.", "There are no wrong answers: every Christmas was different."],
  ("Questions to ask", ["Who did the cooking on Christmas Day?", "Did you have turkey, goose, chicken or something else?", "What did you have for pudding?",
   "Was there a sixpence in the Christmas pudding?", "Who sat where around the table?", "What did you drink with Christmas dinner?", "Who got the wishbone?", "What did you eat for tea on Boxing Day?"]),
  "christmas-cards", "christmas-cards-care-home"),
 ("paper-chains", "Make paper chains", "The simplest Christmas craft there is, and the decorations go straight up on the walls.",
  ["Strips of coloured paper, about 2cm by 20cm, cut ready", "Glue sticks or sticky tape"],
  ["Give everyone a pile of strips.", "Make the first loop and show how the next one links through it.", "Join everyone's chains into one long chain.", "Hang it up together, and count the loops."],
  ["Pre-cut and pre-taped loops make it easy for anyone with less grip.", "People can choose colours and pass loops along the table instead."],
  None, "christmas-bundle", "christmas-activity-programme"),
 ("christmas-smell-box", "A Christmas smell and touch box", "Pass round the smells and textures of Christmas, and see what memories they bring back.",
  ["A box or basket", "An orange, a few cloves, cinnamon sticks, a sprig of pine or holly, tinsel, a Christmas card, a wrapped sweet"],
  ["Take out one thing at a time and pass it round.", "Ask: \"What does this remind you of?\"", "Talk about where people smelt it at Christmas: the kitchen, church, the market.", "Finish with an orange cut into pieces to share, if everyone can have it."],
  ["Check for allergies and dietary needs before anything is eaten.", "Keep small items in sight, and pass them round in a little dish."],
  None, "christmas-cards", "christmas-activity-programme"),
 ("christmas-word-game", "How many words in CHRISTMAS?", "A gentle team word game: how many words can you make from the letters in CHRISTMAS?",
  ["A big sheet of paper or a whiteboard", "A pen"],
  ["Write CHRISTMAS in big letters.", "Ask for any word made from those letters, and write each one up.", "Count the words at the end.", "Try another word next time: SNOWFLAKE, REINDEER or DECORATION."],
  ["Play as one big team, so nobody is put on the spot.", "Give a clue if it goes quiet, such as \"the shiny thing on top of the tree\" (star)."],
  ("Words to get you started", ["it, is, his, him, mist, mast, mash, star, stir, this", "chat, chair, charm, march, smart, trash, stair, smash", "Christmas has 9 letters, so there are lots more"]),
  "retro-christmas-games", "retro-christmas-games-care-home"),
 ("write-christmas-cards", "Write Christmas cards together", "A cosy afternoon writing cards to family, friends or a local school.",
  ["Christmas cards and envelopes", "Pens, and big pens for anyone who prefers them", "Addresses, if sending to family"],
  ["Set out cards, pens and a cup of tea.", "Help each person choose who to write to.", "Write together: they say it, you write it, if that's easier.", "Post them together, or ask a local school or nursery to swap cards."],
  ["A card with just a signature still means a lot.", "Ready-written phrases help: \"Thinking of you this Christmas.\""],
  None, "christmas-gift-planner", "christmas-cards-care-home"),
 ("christmas-picture-bingo", "Make your own Christmas bingo", "Draw or write 9 Christmas things on a card, then play bingo with the list below.",
  ["Paper with a 3 by 3 grid for each player", "Pens", "This list, printed and cut up into calling slips"],
  ["Everyone picks 9 things from the list and writes or draws one in each square.", "Pull slips out of a hat and call them out.", "Cross them off. First to get a line, then a full card, wins.", "Have small prizes ready, like a chocolate coin."],
  ["Fill in the cards in advance for anyone who'd rather not.", "Call each one twice, and hold the slip up."],
  ("Things to call", ["Robin", "Holly", "Cracker", "Stocking", "Snowman", "Christmas pudding", "Star", "Bell", "Candle", "Reindeer", "Mince pie", "Present", "Turkey", "Angel", "Sleigh", "Snowflake"]),
  "retro-christmas-games", "retro-christmas-games-care-home"),
 ("classic-christmas-films", "A classic Christmas film afternoon", "Old favourites, a blanket and a mince pie. Then a chat about the films people loved.",
  ["A TV or projector, and one of the films below", "Blankets, tea and mince pies"],
  ["Choose the film together from the list.", "Show it in two halves, with a break for tea.", "Afterwards ask: \"Where did you first see it?\"", "Ask about going to the pictures when they were young."],
  ["Turn the subtitles on.", "A short film like The Snowman (about half an hour) suits a shorter afternoon."],
  ("Classic Christmas films", ["It's a Wonderful Life (1946)", "Miracle on 34th Street (1947)", "Scrooge, with Alastair Sim (1951)", "White Christmas (1954)", "The Snowman (1982)", "The Muppet Christmas Carol (1992)"]),
  "christmas-cards", "christmas-cards-care-home"),
 ("decorate-christmas-biscuits", "Decorate Christmas biscuits", "Plain biscuits, icing and sprinkles: quick to set up, and everyone gets to eat their work.",
  ["Plain biscuits", "Ready-made icing in tubes, or icing sugar and water", "Sprinkles and small sweets", "Plates and napkins"],
  ["Check everyone's dietary needs first.", "Give each person a plate with two or three biscuits.", "Ice, decorate and admire.", "Eat them with a cup of tea, or wrap them as gifts for visitors."],
  ["Icing tubes are easier to hold than knives.", "Pre-iced biscuits just need sprinkles on top."],
  None, "christmas-bundle", "christmas-activity-programme"),
 ("easy-christmas-quiz", "An easy Christmas quiz", "Ten Christmas questions, each with just two answers to choose from. Everyone can have a go.",
  ["This page, printed", "Small prizes, if you like"],
  ["Read each question and both answers slowly.", "Let people call out, or hold up a hand for each answer.", "Give the answer and chat about it.", "Play as one team, or two halves of the room."],
  ["Two answers make it easy to join in.", "Repeat the question and answers twice."],
  ("Questions (answer first)", ["Who wrote A Christmas Carol? Charles Dickens, or Thomas Hardy", "What colour is Rudolph's nose? Red, or blue",
   "How many days of Christmas are in the song? Twelve, or ten", "Which bird is on lots of Christmas cards? The robin, or the blackbird",
   "What do you pull at Christmas dinner? A cracker, or a ribbon", "What is Scrooge's first name? Ebenezer, or Jacob",
   "What is given on the first day of Christmas in the song? A partridge in a pear tree, or two turtle doves", "Which plant do people kiss under? Mistletoe, or ivy",
   "Sprouts are named after which city? Brussels, or Paris", "In the Christmas story, which town was Jesus born in? Bethlehem, or Nazareth"]),
  "retro-christmas-games", "retro-christmas-games-care-home"),
 ("christmas-memory-questions", "Christmas memory questions", "Twenty easy questions to start Christmas conversations, at home or in a group.",
  ["This list, printed and cut up", "A bowl or a hat"],
  ["Put the questions in a bowl.", "Take turns picking one, and answer it if you like.", "Everyone else can add their own story.", "Write down the best answers for the family."],
  ["Pick one for them and read it out.", "\"Pass\" is always allowed."],
  ("Questions", ["What's your first Christmas memory?", "Did you hang up a stocking or a pillowcase?", "What was the best present you ever had?", "Did you go to church at Christmas?",
   "Who came for Christmas Day?", "Did you make paper chains?", "What was in your stocking?", "Did it ever snow at Christmas?", "Which carol do you love most?",
   "What games did you play on Christmas Day?", "Did you watch the King's or Queen's Christmas message?", "What was Boxing Day like?", "Did you go carol singing?",
   "What did you do on Christmas Eve?", "Who made the Christmas cake?", "What's the funniest thing that happened one Christmas?", "What did your mum always do at Christmas?",
   "Did you have a real tree?", "What did you buy with Christmas money?", "What does Christmas mean to you?"]),
  "christmas-cards", "christmas-cards-care-home"),
 ("paper-snowflakes", "Cut paper snowflakes", "Fold, snip and open: every snowflake comes out different, and they look lovely in the windows.",
  ["Squares of white paper", "Safe scissors", "Sticky tack for the windows"],
  ["Fold a square in half, then in half again, then into a triangle.", "Snip small shapes out of the edges.", "Open it up, and see what you made.", "Stick them on windows or string them up."],
  ["Pre-fold the paper for anyone with less grip.", "Some people enjoy just opening them up and choosing where they go."],
  None, "christmas-bundle", "christmas-activity-programme"),
 ("christmas-sing-along", "A Christmas sing-along", "Old Christmas songs everyone knows. Print the song list, pick favourites and sing.",
  ["Music on a speaker, or a piano if you have one", "Song words printed in large print"],
  ["Let the group choose the songs.", "Start with the best-known, and sing along with the recording.", "Add shakers, bells or clapping.", "Ask: \"Where were you when you first heard this one?\""],
  ["Seated is fine: humming and clapping count.", "Large-print words help people join in."],
  ("Songs to sing", ["Jingle Bells", "White Christmas", "Rudolph the Red-Nosed Reindeer", "Let It Snow! Let It Snow! Let It Snow!", "Winter Wonderland", "Frosty the Snowman", "We Wish You a Merry Christmas", "Silent Night"]),
  "retro-christmas-games", "retro-christmas-games-care-home"),
 ("guess-the-parcel", "Guess the parcel", "Wrap everyday things and pass them round: who can guess what's inside by feel?",
  ["8 to 10 everyday things, like a wooden spoon, a tennis ball, a hairbrush or a cup", "Wrapping paper and tape"],
  ["Wrap each thing before the session.", "Pass one parcel round and let everyone feel it.", "Take guesses, then unwrap it together.", "Talk about the thing: \"When did you last use one of these?\""],
  ["Make the shapes easy to start with.", "Don't use anything sharp, fragile or small enough to swallow."],
  None, "christmas-bundle", "christmas-activity-programme"),
 ("christmas-around-the-world", "Christmas around the world", "A tour of Christmas traditions from other countries, with a chat about the ones people know.",
  ["This page, printed", "A map or globe, if you have one"],
  ["Read out one tradition at a time and find the country on the map.", "Ask: \"Have you ever been there?\" and \"Would you like this one here?\"", "Ask about anyone's family traditions from other countries.", "Pick a favourite to try, like lighting a candle for St Lucia."],
  ["Pictures of each country help.", "Do two or three countries a day instead of all six."],
  ("Traditions", ["Germany: Advent calendars and Christmas markets", "Sweden: St Lucia's Day on 13 December, with candles and singing",
   "The Netherlands: Sinterklaas brings presents on 5 December", "Italy: La Befana brings sweets on 6 January", "Australia: Christmas Day is in summer, often at the beach",
   "Mexico: Las Posadas processions, and piñatas to break"]),
  "christmas-cards", "christmas-activity-programme"),
 ("christmas-table-decorations", "Make a Christmas table decoration", "Pine cones, ribbon and greenery: a simple centrepiece for the Christmas table.",
  ["Pine cones", "Ribbon, and sprigs of greenery", "A small dish or jar for each person", "Battery tea lights (not real candles)"],
  ["Collect pine cones and greenery together, or bring them in.", "Arrange them in a dish with a battery tea light.", "Tie a ribbon round the dish.", "Use them on the tables for Christmas dinner."],
  ["Lay everything out on a tray so it's in easy reach.", "People can choose and pass, and someone else can arrange."],
  None, "christmas-bundle", "christmas-activity-programme"),
 ("christmas-pass-the-parcel", "Pass the parcel, with jokes", "Old-fashioned pass the parcel, with a cracker joke in every layer.",
  ["One parcel with a layer for each person, and a small treat in the middle", "These jokes, cut up, one in each layer", "Music to stop and start"],
  ["Pass the parcel while the music plays.", "When it stops, that person unwraps a layer.", "They read out the joke, or you do.", "The last layer wins the treat."],
  ["Help anyone who finds unwrapping fiddly.", "Pass it on a tray, so it doesn't have to be held."],
  ("Cracker jokes", ["What do snowmen eat for breakfast? Snowflakes!", "What do you call a man who claps at Christmas? Santa Claps!", "Why did the turkey join the band? It had the drumsticks!",
   "What's a snowman's favourite drink? An iced tea!", "Who hides in the bakery at Christmas? A mince spy!", "What do you call an elf who sings? A wrapper!",
   "What did one snowman say to the other? Can you smell carrots?", "Why is Santa so good at gardening? He loves to hoe, hoe, hoe!"]),
  "retro-christmas-games", "retro-christmas-games-care-home"),
 ("christmas-photo-afternoon", "An old Christmas photos afternoon", "Bring out old Christmas photos and cards, and let the stories come.",
  ["Old family photos or Christmas cards", "Or pictures of old Christmases from a library book"],
  ["Ask family to send in a few Christmas photos beforehand.", "Look at one photo at a time.", "Ask: \"Who's this? Where was this taken?\"", "Write a caption with them, to keep with the photo."],
  ["Bigger copies are easier to see: a phone or tablet can zoom in.", "Old Christmas cards work just as well as photos."],
  None, "christmas-cards", "christmas-cards-care-home"),
 ("christmas-charades", "Easy Christmas charades", "Mime a Christmas job, and everyone guesses. Lots of laughs and no reading needed.",
  ["These mimes, written on slips of paper", "A bowl"],
  ["Pick a slip and mime it, with no talking.", "Everyone guesses.", "Staff or family can go first to break the ice.", "Swap so everyone who wants a turn gets one."],
  ["Seated mimes are just as fun.", "Whisper the mime to anyone who can't read the slip."],
  ("Mimes", ["Wrapping a present", "Stirring the Christmas pudding", "Pulling a cracker", "Building a snowman", "Putting the star on the tree", "Carving the turkey",
   "Singing a carol", "Opening a stocking", "Ice skating", "Hanging up a stocking", "Writing a Christmas card", "Eating a mince pie"]),
  "retro-christmas-games", "retro-christmas-games-care-home"),
 ("christmas-carol-concert", "Hold a little carol concert", "Invite a local choir, school or family to sing, or put on your own concert.",
  ["Carol words in large print", "A few chairs set out like a concert", "Mince pies for afterwards"],
  ["Ask a local school, church choir or brownies a few weeks ahead.", "Or make it your own concert, with everyone singing.", "Print a simple programme of carols.", "Finish with mince pies and a chat with the singers."],
  ["Keep it to about 30 minutes.", "Put people who love singing near the front."],
  None, "christmas-cards", "christmas-activity-programme"),
 ("christmas-story-reading", "A Christmas story read aloud", "Read 'Twas the Night Before Christmas or part of A Christmas Carol, slowly, with feeling.",
  ["A copy of the story: both are free online", "A cosy, quiet room"],
  ["Choose a short story or one chapter.", "Read slowly and clearly, with pauses.", "Stop to ask: \"Who remembers this one?\"", "Let anyone who'd like to read a few lines."],
  ["Short is better than long.", "Pictures from the book help people follow."],
  None, "christmas-cards", "christmas-cards-care-home"),
 ("christmas-thank-you-cards", "Thank-you cards for the helpers", "Make cards to thank the people who help all year: staff, carers, neighbours and volunteers.",
  ["Card and envelopes", "Pens, stickers and glitter glue", "A list of names"],
  ["Explain the idea and write the names up.", "Make and decorate a card for each person.", "Write a message together.", "Hand them out on Christmas Eve."],
  ["One message from the whole group works well.", "Stickers are easier than glue."],
  None, "christmas-gift-planner", "christmas-cards-care-home"),
 ("calm-christmas-eve", "A calm Christmas Eve", "A gentle evening after a busy month: soft music, a story and a warm drink.",
  ["Soft Christmas music", "Battery candles or fairy lights", "Hot chocolate or tea", "A blanket"],
  ["Dim the main lights and switch on the fairy lights.", "Play quiet carols.", "Read a short story, or share a Christmas Eve memory.", "Say goodnight with \"Happy Christmas\"."],
  ["Keep the room calm and not too busy.", "Some people prefer to spend it one to one."],
  None, "christmas-bundle", "christmas-activity-programme"),
]
assert len(DAYS) == 24


def names():
    import build_guides as bg
    return {k: n for _, _, items in bg.PLANNERS for k, n, _, _ in items}, bg.LISTING_LINKS


def card(k, why, nm, links):
    return ('<a class="pp" href="%s" rel="noopener" style="display:flex;gap:14px;align-items:center;text-decoration:none;color:inherit;margin:8px 0">'
            '<img src="/shop-img/%s.jpg" alt="" loading="lazy" width="96" height="96" style="width:96px;height:96px;border-radius:12px;flex:none">'
            '<span><small class="muted">%s</small><br><b>%s</b><br><em style="font-style:normal;font-weight:700">See it in the Kinav shop on Etsy ›</em></span></a>'
            % (e(links[k]), k, e(why), e(nm[k])))


def day_page(i, d, updated, nm, links):
    slug, name, line, need, steps, easier, extra, fam, home = d
    n = i + 1
    path = "%s%s/" % (HUB, slug)
    prev = DAYS[i - 1] if i else None
    nxt = DAYS[i + 1] if i < 23 else None
    body = ['<nav class="crumbs" aria-label="Breadcrumb"><a href="%s">24 free Christmas activities</a> › Day %d</nav>' % (HUB, n),
            '<div class="stack-sm"><p class="small muted">Day %d of 24</p><h1>%s</h1><p class="lede">%s</p>'
            '<p class="small muted">For care homes, day centres and families with older relatives. Takes about 30 to 45 minutes.</p></div>' % (n, e(name), e(line)),
            '<section class="panel"><h2>You\'ll need</h2><ul>%s</ul></section>' % "".join("<li>%s</li>" % e(x) for x in need),
            '<section class="panel"><h2>How to run it</h2><ol class="steps">%s</ol></section>' % "".join("<li>%s</li>" % e(x) for x in steps),
            '<section class="panel"><h2>Make it easier</h2><ul>%s</ul></section>' % "".join("<li>%s</li>" % e(x) for x in easier)]
    if extra:
        body.append('<section class="panel"><h2>%s</h2><ol class="big-list">%s</ol>'
                    '<p class="noprint"><button class="btn btn-ghost" type="button" onclick="print()">Print this page</button></p></section>'
                    % (e(extra[0]), "".join("<li>%s</li>" % e(x) for x in extra[1])))
    body.append('<section class="panel stack-sm noprint"><h2>Want all of December planned?</h2>%s%s'
                '<p class="small muted">Everything on kinav.co.uk stays free. The shop helps keep Kinav running.</p></section>'
                % (card(home, "For care homes and day centres", nm, links), card(fam, "For families", nm, links)))
    nav = []
    if prev:
        nav.append('<a href="%s%s/">‹ Day %d: %s</a>' % (HUB, prev[0], n - 1, e(prev[1])))
    nav.append('<a href="%s">All 24 activities</a>' % HUB)
    if nxt:
        nav.append('<a href="%s%s/">Day %d: %s ›</a>' % (HUB, nxt[0], n + 1, e(nxt[1])))
    body.append('<nav class="panel noprint grid" aria-label="More activities">%s</nav>' % "".join(nav))
    body.insert(0, '<style>.big-list li{font-size:19px;margin:6px 0}@media print{.big-list li{font-size:22px}}</style>')
    title = "%s: free Christmas activity for older people | Kinav" % name
    desc = "%s Free Christmas activity idea for care homes, day centres and families with older relatives, with what you need and how to run it." % line
    return path, build_pages.page(path, title, desc, "\n".join(body), updated, kind="guide")


def hub_page(updated, nm, links):
    cards = "".join('<a href="%s%s/" data-day="%d"><small class="muted">Day %d</small><br>%s</a>' % (HUB, d[0], i + 1, i + 1, e(d[1])) for i, d in enumerate(DAYS))
    body = ['<style>.today{outline:3px solid var(--sun,#f2b705);border-radius:12px}</style>',
            '<div class="stack-sm"><h1>24 free Christmas activities for care homes and older relatives</h1>'
            '<p class="lede">One easy activity for every day from 1 to 24 December. Each has what you need, how to run it and how to make it easier, '
            'with lists to print. For care homes, day centres and families.</p>'
            '<p id="today" class="small" hidden></p></div>',
            '<section class="panel"><h2>The activities</h2><div class="grid">%s</div></section>' % cards,
            '<section class="panel stack-sm"><h2>Want it all done for you?</h2>%s%s%s'
            '<p class="small muted">Everything on kinav.co.uk stays free. The shop helps keep Kinav running.</p></section>'
            % (card("christmas-activity-programme", "For care homes: a ready-to-run plan for every day of Advent", nm, links),
               card("retro-christmas-games-care-home", "For care homes and day centres", nm, links),
               card("christmas-bundle", "For families: games, memory cards and a gift planner", nm, links)),
            '<script>(function(){var d=new Date();if(d.getMonth()!==11||d.getDate()>24)return;var a=document.querySelector(\'[data-day="\'+d.getDate()+\'"]\');'
            'if(!a)return;a.classList.add("today");var p=document.getElementById("today");p.hidden=false;'
            'p.innerHTML=\'<b>Today, day \'+d.getDate()+\':</b> <a href="\'+a.getAttribute("href")+\'">\'+a.lastChild.textContent+\' ›</a>\';})();</script>']
    return HUB, build_pages.page(HUB, "24 free Christmas activities for care homes and older relatives | Kinav",
                                 "Free Christmas activity ideas for every day of December: easy games, crafts, quizzes and memory activities for care homes, day centres and older relatives.",
                                 "\n".join(body), updated, kind="guide")


def pages(updated):
    nm, links = names()
    return [hub_page(updated, nm, links)] + [day_page(i, d, updated, nm, links) for i, d in enumerate(DAYS)]


def pin_data():
    """For the pin maker: (slug, day, name, line, path)."""
    return [(d[0], i + 1, d[1], d[2], "%s%s/" % (HUB, d[0])) for i, d in enumerate(DAYS)]


if __name__ == "__main__":
    print(json.dumps(pin_data(), indent=1))

"""Free tools that bring searchers in and lead to the Kinav shop: a large-print 2027 month calendar (print any month)
and a big "Today is" day and date clock for an old tablet, with a sign to print. Nothing is saved or sent.
"""
import build_pages

CAL = "/printables/large-print-calendar-2027/"
CLOCK = "/printables/day-and-date-clock/"
# England and Wales bank holidays 2027 (GOV.UK) and clock changes. Shown on the calendar.
MARKS = {"2027-01-01": "New Year's Day (bank holiday)", "2027-03-26": "Good Friday (bank holiday)", "2027-03-28": "Clocks go forward 1 hour",
         "2027-03-29": "Easter Monday (bank holiday)", "2027-05-03": "Early May bank holiday", "2027-05-31": "Spring bank holiday",
         "2027-08-30": "Summer bank holiday", "2027-10-31": "Clocks go back 1 hour", "2027-12-25": "Christmas Day", "2027-12-26": "Boxing Day",
         "2027-12-27": "Bank holiday (for Christmas Day)", "2027-12-28": "Bank holiday (for Boxing Day)"}


def calendar_page(updated):
    import json
    body = ['<style>.cal-pick{display:flex;flex-wrap:wrap;gap:6px}.cal-pick button{font:inherit;font-weight:700;border:1.5px solid var(--line);background:var(--surface,#fff);'
            'border-radius:999px;padding:6px 12px;cursor:pointer;color:inherit}.cal-pick button[aria-pressed=true]{background:#1f5f7a;color:#fff;border-color:#1f5f7a}'
            '.cal{background:#fff;color:#18232e;border:1.5px solid var(--line);border-radius:18px;padding:16px;margin-top:12px}'
            '.cal h2{font-size:clamp(30px,7vw,48px);margin:0 0 10px;text-align:center}'
            '.cal table{width:100%;border-collapse:collapse;table-layout:fixed}.cal th{font-size:clamp(12px,2.6vw,20px);padding:6px 2px;border-bottom:3px solid #18232e}'
            '.cal td{border:1.5px solid #9aa5ad;height:clamp(54px,11vw,104px);vertical-align:top;padding:4px 6px}'
            '.cal td b{font-size:clamp(20px,5vw,40px);line-height:1}.cal td small{display:block;font-size:clamp(9px,1.8vw,13px);line-height:1.2;margin-top:2px;color:#b42318;font-weight:700}'
            '.cal th .s{display:none}@media(max-width:640px){.cal th .l{display:none}.cal th .s{display:inline}}.cal td.x{background:#f2f4f5}.cal .foot{font-size:12px;margin:8px 0 0;text-align:right}'
            '@media print{@page{size:A4 landscape;margin:9mm}.cal th .l{display:inline!important}.cal th .s{display:none!important}.cal{border:0;padding:0;margin:0}.cal h2{font-size:44px}.cal th{font-size:18px}'
            '.cal td{height:27mm}.cal td b{font-size:34px}.cal td small{font-size:12px}}</style>',
            '<div class="stack-sm noprint"><h1>Free large-print calendar for 2027: print any month</h1>'
            '<p class="lede">Big, clear dates with room to write appointments, visits and bin days. Pick a month, then print it on A4. '
            'England and Wales bank holidays and the clock changes are marked.</p>'
            '<div class="cal-pick" role="group" aria-label="Choose a month"></div>'
            '<p><button class="btn" type="button" onclick="print()">Print this month</button></p></div>',
            '<div class="cal" id="cal" aria-live="polite"></div>',
            '<section class="panel noprint"><h2>Tips</h2><ul>'
            '<li>Print next month as well, and keep it behind this one on the wall or fridge.</li>'
            '<li>Cross off each day at bedtime, so the next morning it\'s easy to see what day it is.</li>'
            '<li>Use one colour for visits from family, and another for appointments.</li></ul>'
            '<p>More free printables: <a href="%s">a big day and date clock</a>, <a href="/printables/important-phone-numbers-list/">important phone numbers</a> '
            'and <a href="/printables/emergency-information-sheet/">an emergency information sheet</a>.</p></section>' % CLOCK,
            '<script>(function(){var M=%s,N=["January","February","March","April","May","June","July","August","September","October","November","December"],'
            'D=["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"],pick=document.querySelector(".cal-pick"),cal=document.getElementById("cal");'
            'function p(n){return(n<10?"0":"")+n}'
            'function show(m){var first=new Date(2027,m,1),start=(first.getDay()+6)%%7,days=new Date(2027,m+1,0).getDate(),h="<h2>"+N[m]+" 2027</h2><table><tr>";'
            'D.forEach(function(d){h+="<th><span class=l>"+d+"</span><span class=s>"+d.slice(0,3)+"</span></th>"});h+="</tr><tr>";for(var i=0;i<start;i++)h+="<td class=x></td>";'
            'for(var d=1;d<=days;d++){var k="2027-"+p(m+1)+"-"+p(d),c=(start+d-1)%%7;h+="<td"+(c>4?" class=x":"")+"><b>"+d+"</b>"+(M[k]?"<small>"+M[k]+"</small>":"")+"</td>";'
            'if(c==6&&d<days)h+="</tr><tr>"}var end=(start+days)%%7;if(end)for(i=end;i<7;i++)h+="<td class=x></td>";'
            'cal.innerHTML=h+"</tr></table><p class=foot>Free from kinav.co.uk</p>";'
            'pick.querySelectorAll("button").forEach(function(b,i){b.setAttribute("aria-pressed",i==m)})}'
            'N.forEach(function(n,i){var b=document.createElement("button");b.type="button";b.textContent=n.slice(0,3);b.setAttribute("aria-label",n+" 2027");'
            'b.onclick=function(){show(i)};pick.appendChild(b)});var now=new Date();show(now.getFullYear()==2027?now.getMonth():0)})();</script>'
            % json.dumps(MARKS)]
    return CAL, build_pages.page(CAL, "Free large-print calendar 2027: printable monthly calendar for older people | Kinav",
                                 "Free large-print 2027 calendar to print any month on A4: big dates, room to write appointments and visits, with UK bank holidays and clock changes marked.",
                                 "\n".join(body), updated, kind="guide")


def clock_page(updated):
    body = ['<style>.clk{background:#fff;color:#18232e;border:1.5px solid var(--line);border-radius:22px;padding:28px 16px;text-align:center}'
            '.clk .d{font-size:clamp(40px,12vw,128px);overflow-wrap:anywhere;font-weight:800;line-height:1.05}.clk .p{font-size:clamp(28px,7vw,72px);margin-top:6px}'
            '.clk .dt{font-size:clamp(28px,7vw,72px);font-weight:700;margin-top:14px}.clk .t{font-size:clamp(24px,5vw,56px);margin-top:8px;color:#1f5f7a;font-weight:700}'
            '.clk.full{position:fixed;inset:0;z-index:50;border-radius:0;border:0;display:flex;flex-direction:column;justify-content:center}'
            '.sign{display:none}@media print{@page{size:A4;margin:12mm}.clk{display:none}.sign{display:block;text-align:center;color:#18232e}'
            '.sign h2{font-size:64px;margin:0 0 30px}.sign p{font-size:34px;border-bottom:3px solid #18232e;padding:28px 0 6px;text-align:left;margin:0 0 18px}}</style>',
            '<div class="stack-sm noprint"><h1>Big day and date clock for older people</h1>'
            '<p class="lede">Shows the day, morning or afternoon, the date and the time in very large letters. Open this page on an old tablet or phone, '
            'tap "Full screen" and leave it on a stand where they can see it. There\'s also a "Today is" sign to print and fill in by hand.</p>'
            '<p><button class="btn" type="button" id="fs">Full screen</button> <button class="btn btn-ghost" type="button" onclick="print()">Print the sign</button></p></div>',
            '<div class="clk" id="clk" aria-live="polite"><div class="d" id="d"></div><div class="p" id="p"></div><div class="dt" id="dt"></div><div class="t" id="t"></div></div>',
            '<div class="sign" aria-hidden="true"><h2>Today is</h2><p>Day:</p><p>Date:</p><p>The weather is:</p><p>Who is coming:</p><p>What\'s happening:</p></div>',
            '<section class="panel noprint"><h2>Tips</h2><ul>'
            '<li>Set the tablet so the screen doesn\'t switch off: Settings, Display, Auto-Lock (iPad) or Screen timeout (Android), then Never, and keep it plugged in.</li>'
            '<li>Tap the clock to leave full screen.</li>'
            '<li>Everything happens on the tablet itself. Nothing is saved or sent.</li></ul>'
            '<p>More free printables: <a href="%s">a large-print 2027 calendar</a> and <a href="/printables/important-phone-numbers-list/">important phone numbers</a>.</p></section>' % CAL,
            '<script>(function(){var D=["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"],'
            'M=["January","February","March","April","May","June","July","August","September","October","November","December"];'
            'function part(h){return h<12?"Morning":h<17?"Afternoon":h<21?"Evening":"Night"}'
            'function tick(){var n=new Date(),h=n.getHours(),m=n.getMinutes();document.getElementById("d").textContent=D[n.getDay()];'
            'document.getElementById("p").textContent=part(h);document.getElementById("dt").textContent=n.getDate()+" "+M[n.getMonth()]+" "+n.getFullYear();'
            'document.getElementById("t").textContent=((h%12)||12)+":"+(m<10?"0":"")+m+(h<12?" am":" pm")}tick();setInterval(tick,10000);'
            'var c=document.getElementById("clk");document.getElementById("fs").onclick=function(){c.classList.add("full");'
            'if(c.requestFullscreen)c.requestFullscreen().catch(function(){})};c.onclick=function(){if(!c.classList.contains("full"))return;'
            'c.classList.remove("full");if(document.fullscreenElement)document.exitFullscreen()}})();</script>']
    return CLOCK, build_pages.page(CLOCK, "Big day and date clock for older people: free, for any tablet | Kinav",
                                   "A free large day and date clock for an older parent: shows the day, morning or afternoon, the date and time in big letters on an old tablet. Plus a 'Today is' sign to print.",
                                   "\n".join(body), updated, kind="guide")


REMI = "/printables/reminiscence-questions/"
VISIT = "/printables/what-to-talk-about-in-a-care-home-visit/"
REMI_Q = ["Where did you grow up, and what was the house like?", "What games did you play outside as a child?", "Who was your favourite teacher?",
          "What was your first job, and what did you spend your first wage on?", "How did you meet someone special?", "What was the first record you bought?",
          "Where did you go on holiday as a child?", "What was Christmas like when you were young?", "What's the biggest change you've seen in your lifetime?",
          "What's the best advice you've ever been given?"]


def remi_page(updated):
    groups = '<section class="panel rq"><h2>10 questions to start with</h2><ol>%s</ol></section>' % "".join("<li>%s</li>" % q for q in REMI_Q)
    body = ['<style>.rq li{font-size:19px;margin:6px 0}@media print{.rq{break-inside:avoid}.rq li{font-size:18px}}</style>',
            '<div class="stack-sm"><h1>10 reminiscence questions for older people</h1>'
            '<p class="lede">Gentle questions to start conversations about a long life: growing up, work, love, music, holidays and more. '
            'For visits, care home groups or a cup of tea at home. Free to print.</p>'
            '<p class="noprint"><button class="btn" type="button" onclick="print()">Print the questions</button></p></div>',
            '<section class="panel noprint"><h2>How to use them</h2><ul><li>Pick one question, not a list. Let the answer lead where it wants to go.</li>'
            '<li>Share a memory of your own, so it feels like a chat, not a quiz.</li><li>Photos, music and old objects help memories come.</li>'
            '<li>If a question doesn\'t feel right, move on. "Pass" is always fine.</li><li>Write down or record the best stories for the family.</li></ul></section>',
            groups,
            '<section class="panel noprint"><p class="small">More free ideas: <a href="%s">what to talk about on a care home visit</a> and <a href="/activities/">activity ideas for every month</a>.</p></section>' % VISIT]
    return REMI, build_pages.page(REMI, "10 reminiscence questions for older people: free printable conversation starters | Kinav",
                                  "10 free reminiscence questions for older people and people in care homes: easy conversation starters about childhood, work, love, music, holidays and Christmas.",
                                  "\n".join(body), updated, kind="guide")


VISIT_TIPS = [("Bring something to look at", "Photos, a magazine, post from home, a newspaper or something from the garden. Things to look at make it easy to start talking."),
              ("Talk about now, too", "What the family are up to, what's on TV, the weather, the football. Everyday news matters."),
              ("Ask open questions", "\"Tell me about…\" works better than questions with a yes or no answer."),
              ("Do something together", "A crossword, a card game, a jigsaw, nails or hair, a walk round the garden. Talking is easier side by side."),
              ("Play music", "Their favourite songs on your phone. Sing along if they want to."),
              ("Silence is fine", "Sitting together quietly, holding hands or watching the birds still counts as a good visit."),
              ("Keep it short and regular", "Shorter, more frequent visits often go better than long ones."),
              ("Say when you'll be back", "Write it on their calendar, so they can look forward to it.")]
VISIT_Q = ["What have you been up to this week?", "Who's been in to see you?", "What was lunch like today?", "What's the best thing about living here?", "Is there anything you'd like me to bring next time?",
           "What did you think of the weather this week?", "Which of the staff makes you laugh?", "What's on the telly that you're enjoying?", "Shall we look at some photos?", "What were you doing at my age?",
           "Can you tell me again how you met Grandad (or Grandma)?", "What was your favourite holiday?", "What should I cook this weekend? How did you make it?", "Which song shall we put on?", "What would you like to do next time I come?"]


def visit_page(updated):
    tips = "".join("<li><b>%s</b><br><span class=\"muted\">%s</span></li>" % (a, b) for a, b in VISIT_TIPS)
    qs = "".join("<li>%s</li>" % q for q in VISIT_Q)
    body = ['<style>.vq li{font-size:19px;margin:6px 0}</style>',
            '<div class="stack-sm"><h1>What to talk about when visiting someone in a care home</h1>'
            '<p class="lede">Easy ideas and 15 conversation starters for visiting a parent or grandparent in a care home, so visits feel less awkward and more like time together.</p></div>',
            '<section class="panel"><h2>8 ideas that help</h2><ol class="steps">%s</ol></section>' % tips,
            '<section class="panel vq"><h2>15 conversation starters</h2><ol>%s</ol>'
            '<p class="noprint"><button class="btn btn-ghost" type="button" onclick="print()">Print this page</button></p></section>' % qs,
            '<section class="panel noprint"><p class="small">More free help: <a href="%s">10 reminiscence questions</a>, <a href="/activities/">activity ideas for every month</a> '
            'and <a href="/guides/how-to-choose-a-care-home/">how to choose a care home</a>.</p></section>' % REMI]
    return VISIT, build_pages.page(VISIT, "What to talk about when visiting someone in a care home: 15 conversation starters | Kinav",
                                   "What to talk about when you visit a parent or grandparent in a care home: 8 ideas that help, and 15 free conversation starters to print.",
                                   "\n".join(body), updated, kind="guide")


def pages(updated):
    return [calendar_page(updated), clock_page(updated), remi_page(updated), visit_page(updated)]

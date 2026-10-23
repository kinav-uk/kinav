(function () {
  "use strict";
  var KC = window.KC;
  var $ = function (id) { return document.getElementById(id); };
  var esc = function (s) {
    return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  };
  var gbp = function (n) { return "£" + Math.round(n).toLocaleString("en-GB"); };
  var MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];

  // Everything personal stays in this browser. Storage can be blocked, so never rely on it.
  // A memory copy keeps choices working for this visit even when storage is blocked.
  var mem = {};
  var store = {
    get: function (k, d) {
      if (k in mem) return mem[k];
      try { var v = localStorage.getItem("kc." + k); return v == null ? d : JSON.parse(v); } catch (e) { return d; }
    },
    set: function (k, v) { mem[k] = v; try { localStorage.setItem("kc." + k, JSON.stringify(v)); } catch (e) {} }
  };

  /* ---------- Screens ---------- */
  var SCREENS = ["home", "plan", "appts", "care", "costs", "benefits", "help", "kit", "privacy", "terms", "articles", "article", "questions", "stayhome", "start", "house"];
  var TAB_FOR = { stayhome: "home", start: "home", house: "home", costs: "home", benefits: "home", kit: "help", questions: "help", privacy: "home", terms: "home", articles: "home", article: "home" };

  function show() {
    var hash = (location.hash || "#home").slice(1);
    var name = hash.indexOf("kit-") === 0 ? "kit" : hash.indexOf("article-") === 0 ? "article" : hash;
    if (SCREENS.indexOf(name) < 0) name = "home";
    SCREENS.forEach(function (s) { $("s-" + s).hidden = s !== name; });
    var tab = TAB_FOR[name] || name;
    document.querySelectorAll(".tabbar a").forEach(function (a) {
      if (a.dataset.tab === tab) a.setAttribute("aria-current", "page"); else a.removeAttribute("aria-current");
    });
    if (name === "kit") renderKit(hash.slice(4));
    if (name === "article") renderArticle(hash.slice(8));
    if (name === "home") renderHome();
    if (name === "care") initCare();
    if (name === "questions") renderQuestions();
    if (name === "appts") suggestQuestions();
    window.scrollTo(0, 0);
    track(hash);
  }
  window.addEventListener("hashchange", show);

  // Visit counts with GoatCounter: no cookies, no personal details, only which screen was opened.
  var pendingVisit = null;
  function track(screen) {
    if (location.hostname !== "kinav.co.uk") return;
    var gc = window.goatcounter;
    if (gc && gc.count) gc.count({ path: "/" + screen }); else pendingVisit = screen;
  }
  function countEvent(name) {
    if (location.hostname !== "kinav.co.uk") return;
    var gc = window.goatcounter;
    if (gc && gc.count) gc.count({ path: name, title: name, event: true });
  }
  var gcScript = document.getElementById("gcScript");
  if (gcScript) gcScript.addEventListener("load", function () { if (pendingVisit) track(pendingVisit); });

  // "Last updated" on Home: whichever is newer, this version of the app or the weekly care data.
  (function () {
    var el = $("lastUpdated"), built = el.dataset.built;
    if (!/^\d{4}-\d\d-\d\d$/.test(built)) { el.hidden = true; return; }
    var full = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
    var words = function (iso) { var p = iso.split("-"); return parseInt(p[2], 10) + " " + full[parseInt(p[1], 10) - 1] + " " + p[0]; };
    el.textContent = "Last updated " + words(built);
    fetch("data/index.json").then(function (r) { return r.json(); }).then(function (idx) {
      if (idx.iso && idx.iso > built) el.textContent = "Last updated " + words(idx.iso);
    }).catch(function () {});
  })();

  /* ---------- 30-day plans ---------- */
  function planDone() { return store.get("plan", {}); }
  // No plan until the carer picks one, so nobody is shown dementia steps they don't need.
  function planKey() { var k = store.get("guide", ""); return KC.plans[k] ? k : ""; }

  function planStats(key) {
    var done = planDone(), total = 0, count = 0, next = null;
    KC.plans[key].groups.forEach(function (g) {
      g.items.forEach(function (it) {
        total++;
        if (done[it.id]) count++; else if (!next) next = it;
      });
    });
    return { total: total, count: count, next: next };
  }

  function renderPlan() {
    var key = planKey(), plan = KC.plans[key], done = planDone();
    fillPick($("planPick"), key);
    $("planProgress").hidden = !key;
    if (!key) {
      $("planTitle").textContent = "Your 30-day plan";
      $("planLede").textContent = "Choose the condition or situation below to see clear steps for your first 30 days.";
      $("planList").innerHTML = "";
      return;
    }
    $("planTitle").textContent = plan.title;
    $("planLede").textContent = plan.lede + " Ticks are saved on this phone only.";
    $("planList").innerHTML = plan.groups.map(function (g) {
      return '<div class="stack-sm"><h2 style="color:var(--accent);font-size:16px">' + esc(g.title) + "</h2>" +
        g.items.map(function (it) {
          var d = !!done[it.id];
          return '<button class="task" type="button" data-id="' + it.id + '" aria-pressed="' + d + '">' +
            '<span class="box" aria-hidden="true">' + (d ? tick() : "") + "</span>" +
            '<span class="stack-sm" style="gap:2px"><span class="tt">' + esc(it.text) + "</span>" +
            (it.note ? '<span class="small muted">' + esc(it.note) + "</span>" : "") + "</span></button>";
        }).join("") + "</div>";
    }).join("");
    var st = planStats(key);
    $("planCount").textContent = st.count + " of " + st.total + " done";
    $("planBar").style.width = Math.round(st.count / st.total * 100) + "%";
  }

  // One menu of plans, grouped into conditions and situations.
  function fillPick(sel, key) {
    var group = function (kind, label) {
      return '<optgroup label="' + label + '">' + Object.keys(KC.plans).filter(function (k) { return KC.plans[k].kind === kind; }).map(function (k) {
        return '<option value="' + k + '"' + (k === key ? " selected" : "") + ">" + esc(KC.plans[k].name) + "</option>";
      }).join("") + "</optgroup>";
    };
    sel.innerHTML = '<option value=""' + (key ? "" : " selected") + ">Choose a plan…</option>" + group("condition", "Conditions") + group("situation", "Situations");
  }

  $("planPick").addEventListener("change", function (e) {
    store.set("guide", e.target.value);
    renderPlan();
  });

  function tick() {
    return '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12l5 5 9-10"/></svg>';
  }

  $("planList").addEventListener("click", function (e) {
    var b = e.target.closest(".task");
    if (!b) return;
    var done = planDone();
    done[b.dataset.id] = !done[b.dataset.id];
    store.set("plan", done);
    renderPlan();
  });

  /* ---------- Home ---------- */
  function renderHome() {
    var key = planKey();
    $("homePlanTitle").textContent = "Your 30-day plan";
    $("homePlanOpen").hidden = !key;
    $("homePlanBar").parentNode.hidden = !key;
    if (!key) {
      $("homePlanCount").textContent = "";
      $("homePlanNext").textContent = "Choose a condition or situation to get clear steps for your first 30 days.";
      fillPick($("homePick"), key);
      var pc0 = store.get("area", "");
      if (pc0 && !$("homePostcode").value) $("homePostcode").value = pc0;
      return;
    }
    var st = planStats(key);
    $("homePlanCount").textContent = st.count + " of " + st.total + " done";
    $("homePlanBar").style.width = Math.round(st.count / st.total * 100) + "%";
    $("homePlanNext").textContent = st.next ? "Next: " + st.next.text + "." : "All " + st.total + " steps done. Well done.";
    fillPick($("homePick"), key);
    var pc = store.get("area", "");
    if (pc && !$("homePostcode").value) $("homePostcode").value = pc;
  }

  $("homePick").addEventListener("change", function (e) {
    store.set("guide", e.target.value);
    renderPlan();
    renderHome();
  });

  $("saveArea").addEventListener("click", function () {
    var v = $("homePostcode").value.trim();
    if (!v) { $("homePostcode").focus(); return; }
    store.set("area", v);
    $("careQ").value = v;
    location.hash = "care";
    searchCare();
  });

  /* ---------- Appointments ---------- */
  function pad(n) { return (n < 10 ? "0" : "") + n; }

  function apptEvent() {
    var date = $("apDate").value, time = $("apTime").value || "10:00";
    if (!date) return null;
    var start = new Date(date + "T" + time), end = new Date(start.getTime() + 60 * 60 * 1000);
    var title = $("apType").value + ($("apWith").value.trim() ? " with " + $("apWith").value.trim() : "");
    var details = [];
    if ($("apWho").value.trim()) details.push("Going: " + $("apWho").value.trim());
    if ($("apAsk").value.trim()) details.push("Questions to ask: " + $("apAsk").value.trim());
    if ($("apNotes").value.trim()) details.push("Notes: " + $("apNotes").value.trim());
    var stamp = function (d) { return d.getFullYear() + pad(d.getMonth() + 1) + pad(d.getDate()) + "T" + pad(d.getHours()) + pad(d.getMinutes()) + "00"; };
    return { title: title, where: $("apWhere").value.trim(), details: details.join("\n"), start: stamp(start), end: stamp(end) };
  }

  function icsText(ev) {
    var clean = function (s) { return s.replace(/\\/g, "\\\\").replace(/\n/g, "\\n").replace(/,/g, "\\,").replace(/;/g, "\\;"); };
    return ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//Kinav//EN", "BEGIN:VEVENT",
      "UID:" + Date.now() + "@kinav", "DTSTAMP:" + new Date().toISOString().replace(/[-:]/g, "").slice(0, 15) + "Z",
      "DTSTART:" + ev.start, "DTEND:" + ev.end, "SUMMARY:" + clean(ev.title),
      ev.where ? "LOCATION:" + clean(ev.where) : "", ev.details ? "DESCRIPTION:" + clean(ev.details) : "",
      "BEGIN:VALARM", "TRIGGER:-P1D", "ACTION:DISPLAY", "DESCRIPTION:Appointment tomorrow", "END:VALARM",
      "END:VEVENT", "END:VCALENDAR"].filter(Boolean).join("\r\n");
  }

  var icsUrl = null;
  function updateAppt() {
    var ev = apptEvent();
    $("apError").hidden = true;
    if (!ev) { $("apGoogle").href = "#appts"; $("apIcs").href = "#appts"; return; }
    $("apGoogle").href = "https://calendar.google.com/calendar/render?action=TEMPLATE" +
      "&text=" + encodeURIComponent(ev.title) + "&dates=" + ev.start + "/" + ev.end +
      "&details=" + encodeURIComponent(ev.details) + "&location=" + encodeURIComponent(ev.where);
    if (icsUrl) URL.revokeObjectURL(icsUrl);
    icsUrl = URL.createObjectURL(new Blob([icsText(ev)], { type: "text/calendar" }));
    $("apIcs").href = icsUrl;
  }
  // Suggested questions: general ones, two for their plan, and any they picked in Questions to ask.
  // Filled in only while the box is empty or still holds our suggestion, so their own words are never replaced.
  function suggestQuestions() {
    var box = $("apAsk");
    if (box.value.trim() && box.dataset.auto !== "1") return;
    var general = KC.questions.filter(function (t) { return t.id === "appointment"; })[0];
    var picked = store.get("q.appointment", { picked: [] }).picked.map(function (i) { return general.items[i]; });
    var list = general.items.slice(0, 3).concat(KC.planQuestions[planKey()] || [], picked);
    list = list.filter(function (q, i) { return q && list.indexOf(q) === i; });
    box.value = list.join("\n");
    box.dataset.auto = "1";
    $("apAskHint").hidden = false;
    updateAppt();
  }
  $("apAsk").addEventListener("input", function () { $("apAsk").dataset.auto = "0"; $("apAskHint").hidden = true; });
  $("apptForm").addEventListener("input", updateAppt);
  $("apptForm").addEventListener("submit", function (e) { e.preventDefault(); });
  ["apGoogle", "apIcs"].forEach(function (id) {
    $(id).addEventListener("click", function (e) {
      if (!$("apDate").value) { e.preventDefault(); $("apError").hidden = false; $("apDate").focus(); }
    });
  });

  /* ---------- Reminders ---------- */
  $("remType").innerHTML = KC.reminders.map(function (r) { return '<option value="' + r.id + '">' + esc(r.label) + "</option>"; }).join("");

  function remPreset() { var id = $("remType").value; return KC.reminders.filter(function (r) { return r.id === id; })[0]; }

  function remPick() {
    var r = remPreset();
    $("remDueLabel").textContent = r.due;
    $("remWeeks").value = String(r.weeks);
    $("remRepeat").value = r.repeat;
    $("remTitleField").hidden = r.id !== "other";
    $("remWhat").textContent = r.details;
    updateRem();
  }

  function ymd(d) { return d.getFullYear() + pad(d.getMonth() + 1) + pad(d.getDate()); }

  function remEvent() {
    var r = remPreset(), due = $("remDate").value;
    if (!due) return null;
    var day = new Date(due + "T12:00"), weeks = parseInt($("remWeeks").value, 10) || 0;
    day.setDate(day.getDate() - weeks * 7);
    var next = new Date(day.getTime()); next.setDate(next.getDate() + 1);
    var title = r.id === "other" ? ($("remTitle").value.trim() || "Reminder") : r.title;
    var details = (r.details ? r.details + "\n\n" : "") + "Due: " + new Date(due + "T12:00").toLocaleDateString("en-GB", { day: "numeric", month: "long", year: "numeric" }) + ". Added with Kinav.";
    return { title: title, details: details, start: ymd(day), end: ymd(next), repeat: $("remRepeat").value };
  }

  var remUrl = null;
  function updateRem() {
    var ev = remEvent();
    $("remError").hidden = true;
    if (!ev) { $("remGoogle").href = "#appts"; $("remIcs").href = "#appts"; return; }
    var rule = ev.repeat ? "RRULE:FREQ=" + ev.repeat.toUpperCase() : "";
    $("remGoogle").href = "https://calendar.google.com/calendar/render?action=TEMPLATE" +
      "&text=" + encodeURIComponent(ev.title) + "&dates=" + ev.start + "/" + ev.end +
      "&details=" + encodeURIComponent(ev.details) + (rule ? "&recur=" + encodeURIComponent(rule) : "");
    var clean = function (t) { return t.replace(/\\/g, "\\\\").replace(/\n/g, "\\n").replace(/,/g, "\\,").replace(/;/g, "\\;"); };
    var ics = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//Kinav//EN", "BEGIN:VEVENT",
      "UID:" + Date.now() + "-rem@kinav", "DTSTAMP:" + new Date().toISOString().replace(/[-:]/g, "").slice(0, 15) + "Z",
      "DTSTART;VALUE=DATE:" + ev.start, "DTEND;VALUE=DATE:" + ev.end, "SUMMARY:" + clean(ev.title), "DESCRIPTION:" + clean(ev.details),
      rule, "BEGIN:VALARM", "TRIGGER:PT9H", "ACTION:DISPLAY", "DESCRIPTION:" + clean(ev.title), "END:VALARM",
      "END:VEVENT", "END:VCALENDAR"].filter(Boolean).join("\r\n");
    if (remUrl) URL.revokeObjectURL(remUrl);
    remUrl = URL.createObjectURL(new Blob([ics], { type: "text/calendar" }));
    $("remIcs").href = remUrl;
  }

  $("remType").addEventListener("change", remPick);
  $("remForm").addEventListener("input", function (e) { if (e.target.id !== "remType") updateRem(); });
  $("remForm").addEventListener("submit", function (e) { e.preventDefault(); });
  ["remGoogle", "remIcs"].forEach(function (id) {
    $(id).addEventListener("click", function (e) {
      if (!$("remDate").value) { e.preventDefault(); $("remError").hidden = false; $("remDate").focus(); }
    });
  });
  remPick();

  function calMode(rem) {
    $("apptForm").hidden = rem; $("remForm").hidden = !rem;
    if (rem) { $("segRem").setAttribute("aria-current", "page"); $("segAppt").removeAttribute("aria-current"); }
    else { $("segAppt").setAttribute("aria-current", "page"); $("segRem").removeAttribute("aria-current"); }
  }
  $("segAppt").addEventListener("click", function (e) { e.preventDefault(); calMode(false); });
  $("segRem").addEventListener("click", function (e) { e.preventDefault(); calMode(true); });

  /* ---------- Questions to ask ---------- */
  // One list: tapping a question adds it and opens a note box underneath; a switch hides the rest.
  $("qTopic").innerHTML = KC.questions.map(function (t) { return '<option value="' + t.id + '">' + esc(t.name) + "</option>"; }).join("");
  $("qTopic").value = store.get("qtopic", KC.questions[0].id);
  function qTopic() { var id = $("qTopic").value; return KC.questions.filter(function (t) { return t.id === id; })[0] || KC.questions[0]; }
  function qState() {
    var n = qTopic().items.length, st = store.get("q." + qTopic().id, { picked: [], notes: {} });
    st.picked = st.picked.filter(function (i) { return i < n; });
    return st;
  }
  function qSave(st) { store.set("q." + qTopic().id, st); }

  function renderQuestions(focusIndex) {
    var t = qTopic(), st = qState(), only = $("qOnly").checked;
    $("qOnlyLabel").textContent = "Show only my questions (" + st.picked.length + ")";
    $("qCopied").hidden = true;
    var shown = t.items.map(function (q, i) { return { q: q, i: i, on: st.picked.indexOf(i) >= 0 }; }).filter(function (x) { return !only || x.on; });
    $("qList").innerHTML = shown.map(function (x) {
      var note = st.notes[x.i] || "";
      return '<div class="qitem' + (x.on ? " on" : "") + (note.trim() ? " done" : "") + '"><button class="qpick" type="button" data-i="' + x.i + '" aria-pressed="' + x.on + '">' +
        '<span class="mark" aria-hidden="true">' + (x.on ? "✓" : "+") + "</span><span>" + esc(x.q) + "</span></button>" +
        (x.on ? '<div class="qanswer"><label class="qlabel" for="qn' + x.i + '">Answer</label><textarea class="qnote" id="qn' + x.i + '" data-i="' + x.i + '" rows="2" placeholder="Type the answer here">' + esc(note) + '</textarea>' +
          '<button class="linkbtn tiny qremove" type="button" data-i="' + x.i + '">Remove this question</button></div>' : "") + "</div>";
    }).join("");
    $("qEmpty").hidden = shown.length > 0;
    document.querySelectorAll("#qList .qnote").forEach(grow);
    if (focusIndex != null && $("qn" + focusIndex)) $("qn" + focusIndex).focus();
  }

  $("qTopic").addEventListener("change", function () { store.set("qtopic", $("qTopic").value); renderQuestions(); });
  $("qOnly").addEventListener("change", function () { renderQuestions(); });
  // Answer boxes grow with the text, so nothing is hidden behind a scroll bar.
  function grow(ta) { ta.style.height = "auto"; ta.style.height = (ta.scrollHeight + 2) + "px"; }

  $("qList").addEventListener("click", function (e) {
    var rm = e.target.closest(".qremove"), b = e.target.closest(".qpick"), st = qState();
    if (rm) {
      var r = parseInt(rm.dataset.i, 10);
      st.picked = st.picked.filter(function (x) { return x !== r; });
      qSave(st); renderQuestions();
      return;
    }
    if (!b) return;
    var i = parseInt(b.dataset.i, 10);
    // Tapping a chosen question just jumps to its answer box, so nothing is removed by accident.
    if (st.picked.indexOf(i) >= 0) { $("qn" + i).focus(); return; }
    st.picked.push(i);
    st.picked.sort(function (a, c) { return a - c; });
    qSave(st);
    renderQuestions(i);
  });
  $("qList").addEventListener("input", function (e) {
    var ta = e.target.closest("textarea");
    if (!ta) return;
    grow(ta);
    ta.closest(".qitem").classList.toggle("done", ta.value.trim().length > 0);
    var st = qState(); st.notes[ta.dataset.i] = ta.value; qSave(st);
  });
  function qText() {
    var t = qTopic(), st = qState();
    return t.name + "\n\n" + st.picked.map(function (i) {
      var n = (st.notes[i] || "").trim();
      return "- " + t.items[i] + (n ? "\n  " + n : "");
    }).join("\n");
  }
  $("qCopy").addEventListener("click", function () {
    var done = function () { $("qCopied").hidden = false; };
    try { navigator.clipboard.writeText(qText()).then(done, done); } catch (e) { done(); }
  });
  $("qToAppt").addEventListener("click", function () {
    var st = qState(), t = qTopic();
    $("apAsk").value = st.picked.map(function (i) { return t.items[i]; }).join("\n");
    $("apAsk").dataset.auto = "0"; $("apAskHint").hidden = true;
    location.hash = "appts";
    updateAppt();
  });
  $("qQuick").addEventListener("click", function () {
    var st = qState(); st.picked = qTopic().items.map(function (q, i) { return i; });
    qSave(st); $("qOnly").checked = true; renderQuestions();
  });
  $("qClear").addEventListener("click", function () { qSave({ picked: [], notes: {} }); $("qOnly").checked = false; renderQuestions(); });

  /* ---------- Find care ---------- */
  var care = { index: null, rows: [], pool: [], council: null, point: null, place: "", files: {}, type: "H", shown: 0 };
  var HM_PER_MILE = 16.0934; // locations are stored in 100 m units
  var KQ = ["Safe", "Effective", "Caring", "Responsive", "Well-led"];
  var KQ_WORD = { O: "Outstanding", G: "Good", R: "Requires improvement", I: "Inadequate", "-": "Not rated" };
  var TYPE_WORD = { H: "Care at home", N: "Nursing home", R: "Residential home" };

  function initCare() {
    if (care.index) return;
    fetch("data/index.json").then(function (r) { return r.json(); }).then(function (idx) {
      care.index = idx;
      $("councilList").innerHTML = idx.councils.map(function (c) { return '<option value="' + esc(c.n) + '">'; }).join("");
      $("careNote").textContent += " Updated " + idx.updated + ".";
      var saved = store.get("area", "");
      if (saved && !$("careQ").value) $("careQ").value = saved;
      if ($("careQ").value) searchCare();
    }).catch(function () {
      $("careStatus").textContent = "Care listings couldn't load. Check your connection and try again.";
    });
  }

  function findCouncil(q) {
    var idx = care.index, raw = q.trim().toUpperCase(), compact = raw.replace(/\s+/g, "");
    if (!raw) return null;
    // Postcode: use the district (outward code), e.g. BR1 from "BR1 3AA".
    var outward = raw.indexOf(" ") > 0 ? raw.split(/\s+/)[0] : (compact.length > 4 ? compact.slice(0, -3) : compact);
    if (/^[A-Z]{1,2}\d[A-Z\d]?$/.test(outward) && idx.districts[outward]) {
      return idx.councils.filter(function (c) { return c.s === idx.districts[outward]; })[0] || null;
    }
    var low = q.trim().toLowerCase();
    var exact = idx.councils.filter(function (c) { return c.n.toLowerCase() === low; });
    if (exact.length) return exact[0];
    var starts = idx.councils.filter(function (c) { return c.n.toLowerCase().indexOf(low) === 0; });
    if (starts.length) return starts[0];
    return idx.councils.filter(function (c) { return c.n.toLowerCase().indexOf(low) >= 0; })[0] || null;
  }

  function searchCare() {
    if (!care.index) { initCare(); return; }
    var c = findCouncil($("careQ").value);
    if (!c) {
      care.rows = []; care.council = null; $("careList").innerHTML = ""; $("careMore").hidden = true;
      $("careStatus").textContent = "We couldn't find that area. Try a postcode, like BR1 3AA, or a council name, like Bromley.";
      return;
    }
    store.set("area", $("careQ").value.trim());
    $("careStatus").textContent = "Loading care in " + c.n + "…";
    Promise.all([councilRows(c), locate($("careQ").value)]).then(function (got) {
      care.rows = got[0]; care.council = c; care.point = got[1] ? got[1].en : null; care.place = got[1] ? got[1].label : "";
      var dist = $("fDist");
      dist.disabled = !care.point;
      dist.options[0].text = care.point ? "Whole of " + c.n : "Enter a postcode to search by miles";
      if (!care.point) dist.value = "";
      if (care.point && $("fSort").value === "best" && !care.sortChosen) $("fSort").value = "near";
      if (!care.point && $("fSort").value === "near") $("fSort").value = "best";
      return refreshPool();
    }).then(function () { renderCare(true); }).catch(function () {
      $("careStatus").textContent = "Care listings couldn't load. Check your connection and try again.";
    });
  }

  function councilRows(c) {
    if (care.files[c.s]) return Promise.resolve(care.files[c.s]);
    return fetch("data/la/" + c.s + ".json").then(function (r) { return r.json(); }).then(function (rows) {
      care.files[c.s] = rows; return rows;
    });
  }

  // Find a postcode's location from this phone's own copy of the district file,
  // so the postcode is never sent to anyone else.
  function locate(q) {
    var compact = (q || "").toUpperCase().replace(/\s+/g, "");
    var full = /^([A-Z]{1,2}\d[A-Z\d]?)(\d[A-Z]{2})$/.exec(compact);
    var outward = full ? full[1] : (/^[A-Z]{1,2}\d[A-Z\d]?$/.test(compact) ? compact : "");
    if (!outward) return Promise.resolve(null);
    var centre = care.index.dc && care.index.dc[outward];
    var district = centre ? { en: centre, label: outward } : null;
    if (!full) return Promise.resolve(district);
    return fetch("data/pc/" + outward + ".json").then(function (r) { return r.ok ? r.json() : {}; }).then(function (pcs) {
      var en = pcs[full[2]];
      return en ? { en: en, label: outward + " " + full[2] } : district;
    }).catch(function () { return district; });
  }

  function miles(r) {
    if (!care.point || r[14] == null) return null;
    return Math.sqrt(Math.pow(r[14] - care.point[0], 2) + Math.pow(r[15] - care.point[1], 2)) / HM_PER_MILE;
  }

  // Searching by miles can cross council borders, so load every council the circle touches.
  function refreshPool() {
    var m = parseFloat($("fDist").value);
    if (!care.point || !m) { care.pool = care.rows; return Promise.resolve(); }
    var p = care.point, reach = m * HM_PER_MILE;
    var near = care.index.councils.filter(function (c) {
      var b = c.b;
      return c.s === care.council.s || (b && p[0] >= b[0] - reach && p[0] <= b[2] + reach && p[1] >= b[1] - reach && p[1] <= b[3] + reach);
    });
    $("careStatus").textContent = "Finding care within " + m + " miles…";
    return Promise.all(near.map(councilRows)).then(function (lists) {
      care.pool = [].concat.apply([], lists).filter(function (r) { var d = miles(r); return d !== null && d <= m; });
    });
  }

  function dateKey(d) { var p = (d || "").split("/"); return p.length === 3 ? p[2] + p[1] + p[0] : ""; }

  function filtered() {
    var who = $("fWho").value, want = $("fSpec").value, rate = $("fRate").value;
    var list = care.pool.filter(function (r) {
      var spec = specOf(r);
      if (r[5].indexOf(care.type) < 0) return false;
      if (who && spec.indexOf(who) < 0 && spec.indexOf("A") < 0 && !(who === "O" && r[7])) return false;
      if (want && spec.indexOf(want) < 0) return false;
      if (rate === "O" && r[8] !== "Outstanding") return false;
      if (rate === "G" && (r[8] === "Not Rated" || /[RI]/.test(r[9]))) return false;
      return true;
    });
    var sort = $("fSort").value;
    if (sort === "az") list.sort(function (a, b) { return a[0].localeCompare(b[0]); });
    if (sort === "near" && care.point) list.sort(function (a, b) { return (miles(a) == null ? 1e9 : miles(a)) - (miles(b) == null ? 1e9 : miles(b)); });
    if (sort === "recent") list.sort(function (a, b) { return dateKey(b[10]).localeCompare(dateKey(a[10])); });
    return list;
  }

  var SPEC_WORD = { D: "Dementia", P: "Physical disabilities", S: "Sensory impairments", L: "Learning disabilities", M: "Mental health", X: "Substance misuse", E: "Eating disorders" };
  var AGE_WORD = { O: "over 65s", U: "adults under 65", C: "children", A: "everyone" };

  // Older cached data has no specialism codes, only the dementia flag
  function specOf(r) { return r[13] != null ? r[13] : (r[6] ? "D" : ""); }

  function specLine(r) {
    var codes = specOf(r).split(""), want = $("fSpec").value;
    var tags = codes.filter(function (c) { return SPEC_WORD[c]; }).map(function (c) {
      return '<span class="tag' + (c === "D" || c === want ? " tag-hi" : "") + '">' + SPEC_WORD[c] + "</span>";
    }).join("");
    var ages = codes.filter(function (c) { return AGE_WORD[c]; }).map(function (c) { return AGE_WORD[c]; });
    if (!tags && !ages.length) return "";
    return '<div class="stack-sm"><p class="tiny muted">Specialist care (as listed by CQC)</p>' +
      (tags ? '<div class="spec">' + tags + "</div>" : "") +
      (ages.length ? '<p class="tiny muted">Cares for: ' + ages.join(", ") + "</p>" : "") + "</div>";
  }

  function milesText(d) {
    return d < 0.1 ? "Under 0.1 miles" : (d < 10 ? d.toFixed(1) : Math.round(d)) + (d >= 0.95 && d < 1.05 ? " mile" : " miles");
  }

  function rated(d) {
    var p = (d || "").split("/");
    return p.length === 3 ? MONTHS[parseInt(p[1], 10) - 1] + " " + p[2] : "";
  }

  function careCard(r) {
    var name = r[0], addr = r[1], pc = r[2], phone = r[3], web = r[4], overall = r[8], kq = r[9], date = r[10], svc = r[11], id = r[12];
    var lows = [];
    var cells = kq.split("").map(function (k, i) {
      if (k === "R" || k === "I") lows.push(KQ[i] + " as " + KQ_WORD[k]);
      var cls = { O: "o", G: "", R: "r", I: "i", "-": "n" }[k];
      var word = k === "R" ? "Req. improv." : KQ_WORD[k];
      return '<div class="' + cls + '"><span>' + KQ[i] + "</span><b>" + word + "</b></div>";
    }).join("");
    var badge = overall === "Not Rated" ? "CQC: rated per service" : "CQC: " + overall + (date ? " · " + rated(date) : "");
    var types = r[5].split("").map(function (t) { return TYPE_WORD[t]; }).join(" · ");
    var site = web ? (/^https?:/i.test(web) ? web : "https://" + web) : "";
    return '<article class="card">' +
      '<div class="head"><div><h3>' + esc(name) + '</h3><p class="small muted">' + esc(types) + "</p></div>" +
      '<span class="pill ' + (overall === "Outstanding" ? "pill-good" : overall === "Good" ? "pill-good" : "pill-quiet") + '">' + esc(badge) + "</span></div>" +
      '<p class="small">' + esc(addr) + " " + esc(pc) + "</p>" +
      (miles(r) !== null ? '<p class="small"><b>' + milesText(miles(r)) + "</b> from " + esc(care.place) + "</p>" : "") +
      (lows.length ? '<div class="warn"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3l9 16H3z"/><path d="M12 10v4M12 17v.5"/></svg><span>Good overall, but CQC rated ' + esc(lows.join(" and ")) + ". Read the CQC report before choosing.</span></div>" : "") +
      (overall === "Not Rated" ? '<p class="small">' + esc(svc) + "</p>" : '<div class="kq">' + cells + "</div>") +
      specLine(r) +
      (phone ? '<p class="small">Phone: <span class="phone">' + esc(phone) + "</span></p>" : "") +
      '<div class="actions">' +
      (phone ? '<a class="btn btn-primary btn-sm" href="tel:' + esc(phone) + '">Call</a>' : "") +
      (site ? '<a class="btn btn-ghost btn-sm" href="' + esc(site) + '" target="_blank" rel="noopener">Website</a>' : "") +
      '<a class="btn btn-ghost btn-sm" href="https://www.cqc.org.uk/location/' + esc(id) + '" target="_blank" rel="noopener">CQC report</a>' +
      "</div></article>";
  }

  function where() {
    var m = $("fDist").value;
    return m && care.point ? "within " + m + (m === "1" ? " mile" : " miles") + " of " + care.place : "in " + care.council.n;
  }

  function renderCare(reset) {
    if (!care.council) return;
    var list = filtered();
    if (reset) { care.shown = 0; $("careList").innerHTML = ""; }
    var next = list.slice(care.shown, care.shown + 25);
    $("careList").insertAdjacentHTML("beforeend", next.map(careCard).join(""));
    care.shown += next.length;
    $("careMore").hidden = care.shown >= list.length;
    $("careStatus").textContent = list.length
      ? list.length + " " + { H: "care at home services", N: "nursing homes", R: "residential homes" }[care.type] + " " + where() + ", " +
        { best: "best rated first.", near: "nearest first.", recent: "most recently rated first.", az: "A to Z." }[$("fSort").value]
      : "No matches " + where() + ". Try another type of care, a wider distance or change a filter.";
  }

  $("careForm").addEventListener("submit", function (e) { e.preventDefault(); searchCare(); });
  $("careTypes").addEventListener("click", function (e) {
    var b = e.target.closest(".chip");
    if (!b) return;
    care.type = b.dataset.t;
    document.querySelectorAll("#careTypes .chip").forEach(function (c) { c.setAttribute("aria-pressed", String(c === b)); });
    renderCare(true);
  });
  ["fWho", "fSpec", "fRate"].forEach(function (id) {
    $(id).addEventListener("change", function () { renderCare(true); });
  });
  $("fSort").addEventListener("change", function () { care.sortChosen = true; renderCare(true); });
  $("fDist").addEventListener("change", function () {
    if (care.council) refreshPool().then(function () { renderCare(true); });
  });
  $("careMore").addEventListener("click", function () { renderCare(false); });

  /* ---------- Care costs ---------- */
  var UPPER = 23250, LOWER = 14250, DISREGARD_WEEKS = 12, YEARS = 10;
  var touched = false;
  var num = function (id) { var v = parseFloat($(id).value); return isFinite(v) && v > 0 ? v : 0; };
  var careType = function () { return document.querySelector('input[name="type"]:checked').value; };

  $("area").innerHTML = Object.keys(KC.areas).map(function (k) { return '<option value="' + k + '">' + esc(KC.areas[k].name) + "</option>"; }).join("");

  function fillDefaults() {
    var a = KC.areas[$("area").value], t = careType();
    $("areaNote").textContent = a.note;
    $("rate").value = a.hourly.toFixed(2);
    if (t !== "home") $("weekly").value = a[t];
  }

  function capitalAt(week, gap, homeCounts) {
    var c = num("savings") - gap * week;
    if (homeCounts && week >= DISREGARD_WEEKS) c += num("homeValue");
    return c;
  }
  function tariff(c) { return c > LOWER ? Math.ceil((Math.min(c, UPPER) - LOWER) / 250) : 0; }
  function duration(weeks) {
    var months = Math.round(weeks / 4.345), y = Math.floor(months / 12), m = months % 12;
    if (y === 0) return m + (m === 1 ? " month" : " months");
    return y + (y === 1 ? " yr" : " yrs") + (m ? " " + m + " mo" : "");
  }

  function renderCosts() {
    var t = careType(), cost = t === "home" ? num("hours") * num("rate") : num("weekly"), income = num("income");
    var owns = $("owns").checked, homeCounts = t !== "home" && owns && !$("disregard").checked, gap = cost - income;
    $("homeCareRow").hidden = t !== "home";
    $("weeklyRow").hidden = t === "home";
    $("ownsRow").hidden = t === "home";
    $("homeValueRow").hidden = !owns || t === "home";
    $("disregardRow").hidden = !owns || t === "home";

    $("weeklyOut").textContent = gbp(cost);
    var hourly = t === "home" ? num("rate") : cost / 168;
    $("periodOut").textContent = "a week · £" + hourly.toFixed(2) + " an hour" + (t === "home" ? "" : " (round the clock)") +
      " · " + gbp(cost * 52 / 12) + " a month · " + gbp(cost * 52) + " a year";

    var longRunCap = capitalAt(DISREGARD_WEEKS, 0, homeCounts);
    $("capOut").textContent = gbp(Math.max(longRunCap, 0));
    $("gapOut").textContent = gap > 0 ? gbp(gap) : "None";

    // First week counted savings reach the upper limit. When the home counts, start after the
    // 12-week disregard so a temporary dip doesn't read as long-term help.
    var hit = null;
    for (var w = homeCounts ? DISREGARD_WEEKS : 0; w <= YEARS * 52; w++) {
      if (capitalAt(w, Math.max(gap, 0), homeCounts) <= UPPER) { hit = w; break; }
    }
    var chip = $("chip"), text;
    if (hit === 0 && longRunCap <= UPPER) {
      chip.className = "status help";
      chip.textContent = longRunCap > LOWER ? "Council may help now" : "Council may help now, from income only";
      text = longRunCap > LOWER
        ? "Counted savings are under £23,250. They would pay from their income plus about " + gbp(tariff(longRunCap)) + " a week from savings."
        : "Counted savings are under £14,250, so they are ignored. They would pay a contribution from income only.";
      $("runOut").textContent = "Now";
    } else if (hit === null) {
      chip.className = "status self";
      chip.textContent = "Self-funding";
      text = gap <= 0 ? "Income covers the weekly cost, so savings aren't drawn down." : "Savings should last more than " + YEARS + " years at this cost.";
      $("runOut").textContent = YEARS + "+ yrs";
    } else {
      chip.className = "status self";
      chip.textContent = "Self-funding for now";
      text = "Savings may last about " + duration(hit) + " before the council could start to help.";
      if (homeCounts) text += " This includes the home, which counts after the first 12 weeks.";
      else if (t === "home") text += " A home they own isn't counted for care at home.";
      $("runOut").textContent = duration(hit);
    }
    $("statusText").textContent = text;
    drawChart(gap, homeCounts);

    var s = ["Ask the council for a free care needs assessment, whatever their savings."];
    if (hit === 0 && longRunCap <= UPPER) s.push("Ask the council for a financial assessment to confirm what they would pay.");
    if (homeCounts) s.push("Ask the council about a deferred payment agreement, so the home doesn't have to be sold straight away.");
    if (t === "nurs") s.push("Ask whether the NHS will pay towards nursing costs, and about an NHS Continuing Healthcare check.");
    s.push("Check whether they can claim Attendance Allowance. It isn't means-tested.");
    s.push("Get written quotes from 2 or 3 local providers and put the real fee in above.");
    $("steps").innerHTML = s.map(function (x) { return "<li>" + esc(x) + "</li>"; }).join("");
  }

  function drawChart(gap, homeCounts) {
    var W = 520, H = 220, L = 58, R = 12, T = 12, B = 28, weeks = YEARS * 52, pts = [], max = UPPER * 1.6;
    for (var w = 0; w <= weeks; w += 4) {
      var c = Math.max(capitalAt(w, Math.max(gap, 0), homeCounts), 0);
      pts.push([w, c]); if (c > max) max = c;
    }
    var raw = max / 4, p10 = Math.pow(10, Math.floor(Math.log10(raw))), n = raw / p10;
    var step = (n <= 1 ? 1 : n <= 2 ? 2 : n <= 2.5 ? 2.5 : n <= 5 ? 5 : 10) * p10;
    max = Math.ceil(max / step) * step;
    var x = function (w) { return L + (w / weeks) * (W - L - R); };
    var y = function (v) { return T + (1 - v / max) * (H - T - B); };
    var short = function (v) { return v >= 1e6 ? "£" + (v / 1e6).toFixed(v % 1e6 ? 1 : 0) + "m" : v >= 1e3 ? "£" + Math.round(v / 1e3) + "k" : "£" + v; };
    var s = "";
    for (var v = 0; v <= max + 1; v += step) {
      s += '<line x1="' + L + '" x2="' + (W - R) + '" y1="' + y(v) + '" y2="' + y(v) + '" stroke="var(--line)" stroke-width="1"/>';
      s += '<text x="' + (L - 6) + '" y="' + (y(v) + 4) + '" text-anchor="end">' + short(v) + "</text>";
    }
    for (var yr = 0; yr <= YEARS; yr += 2) s += '<text x="' + x(yr * 52) + '" y="' + (H - 8) + '" text-anchor="middle">' + (yr === 0 ? "Now" : yr + "y") + "</text>";
    s += '<line x1="' + L + '" x2="' + (W - R) + '" y1="' + y(UPPER) + '" y2="' + y(UPPER) + '" stroke="var(--sun-fg)" stroke-width="1.5" stroke-dasharray="4 3"/>' +
      '<text x="' + (W - R) + '" y="' + (y(UPPER) - 5) + '" text-anchor="end" style="fill:var(--sun-fg)">£23,250: council may help</text>';
    var d = pts.map(function (p, i) { return (i ? "L" : "M") + x(p[0]).toFixed(1) + " " + y(p[1]).toFixed(1); }).join(" ");
    s += '<path d="' + d + " L" + x(weeks).toFixed(1) + " " + y(0) + " L" + x(0) + " " + y(0) + ' Z" fill="var(--sunk)"/>';
    s += '<path d="' + d + '" fill="none" stroke="var(--accent)" stroke-width="2.25" stroke-linejoin="round"/>';
    var last = pts[pts.length - 1];
    s += '<circle cx="' + x(last[0]) + '" cy="' + y(last[1]) + '" r="3.5" fill="var(--accent)"/>';
    $("chart").innerHTML = s;
  }

  $("area").addEventListener("change", function () { fillDefaults(); renderCosts(); });
  document.querySelectorAll('input[name="type"]').forEach(function (r) {
    r.addEventListener("change", function () { fillDefaults(); renderCosts(); });
  });
  $("calc").addEventListener("input", function (e) {
    if (e.target.id !== "area" && e.target.name !== "type" && !touched) { touched = true; $("exampleTag").hidden = true; }
    renderCosts();
  });
  $("calc").addEventListener("submit", function (e) { e.preventDefault(); });

  /* ---------- Where do I start? ---------- */
  fillPick($("stPlan"), "");
  $("stPlan").options[0].text = "None, or not sure";
  var ST_STEPS = {
    diagnosed: [["#benefits", "Check the money they could be missing", "Attendance Allowance isn't means-tested."], ["#questions", "Pick questions for the next appointment", "So nothing is forgotten on the day.", "appointment"]],
    hospital: [["#kit-hospital", "Use the Leaving hospital checklist", "Make sure help is in place before they come home."], ["#questions", "Questions to ask before they come home", "Discharge date, support, equipment and contacts.", "discharge"], ["#stayhome", "Help them stay at home", "Grants, equipment, alarms and home care."]],
    struggling: [["#stayhome", "Help them stay at home", "A plan with grants, equipment, alarms and home care."], ["#kit-home-care", "Ask the council for a needs assessment", "Free, whatever their savings."], ["#benefits", "Check the money they could be missing", "Benefits and discounts in six questions."]],
    carehome: [["#care", "Find care homes near them", "Only homes rated Good or Outstanding by CQC."], ["#kit-home-choice", "Use the Choosing a care home checklist", "Shortlist, visit and ask the right questions."], ["#house", "Will they have to sell the house?", "The rules in plain English."], ["#costs", "Work out the costs", "And how long savings could last."]],
    money: [["#benefits", "Check the money they could be missing", "Benefits and discounts in six questions."], ["#house", "Will they have to sell the house?", "The rules in plain English."], ["#costs", "Work out care costs", "Home or care home, and how long savings last."]]
  };
  function renderStart() {
    var now = $("stNow").value, plan = $("stPlan").value, alone = $("stAlone").value;
    if (!now) { $("stOut").innerHTML = ""; return; }
    var steps = [];
    if (plan) steps.push(["#plan", "Start the 30-day plan: " + KC.plans[plan].name, "Clear steps for the first weeks, one at a time.", null, plan]);
    steps = steps.concat(ST_STEPS[now] || []);
    if (alone === "yes" && now !== "carehome") steps.push(["#kit-alarms", "Think about a fall alarm", "Help at the press of a button when they live alone."]);
    steps = steps.slice(0, 4);
    store.set("start", { steps: steps.map(function (st) { return [st[0], st[1]]; }), done: [] });
    countEvent("start-" + now);
    renderNext();
    $("stOut").innerHTML = "<h2>Your first " + steps.length + " steps</h2>" + steps.map(function (st, i) {
      return '<a class="card shstep" style="text-decoration:none;color:inherit" href="' + st[0] + '"' + (st[3] ? ' data-qtopic="' + st[3] + '"' : "") + (st[4] ? ' data-setplan="' + st[4] + '"' : "") +
        '><h3>' + (i + 1) + ". " + esc(st[1]) + ' ›</h3><p class="small muted">' + esc(st[2]) + "</p></a>";
    }).join("") + '<button class="btn btn-ghost" type="button" data-share="start">Send these steps to family</button>';
  }
  $("stForm").addEventListener("change", renderStart);
  $("stForm").addEventListener("submit", function (e) { e.preventDefault(); });
  $("stOut").addEventListener("click", function (e) {
    var a = e.target.closest("a");
    if (!a) return;
    if (a.dataset.setplan) { store.set("guide", a.dataset.setplan); renderPlan(); renderHome(); countEvent("plan-" + a.dataset.setplan); }
    var st = store.get("start", null), title = a.querySelector("h3") ? a.querySelector("h3").textContent.replace(/^\d+\. /, "").replace(/ ›$/, "") : "";
    if (st) { st.steps.forEach(function (x, i) { if (x[1] === title && st.done.indexOf(i) < 0) st.done.push(i); }); store.set("start", st); renderNext(); }
    if (a.dataset.qtopic) { store.set("qtopic", a.dataset.qtopic); $("qTopic").value = a.dataset.qtopic; }
  });

  /* ---------- Your next step (Home) ---------- */
  function renderNext() {
    var st = store.get("start", null), card = $("nextStep");
    var i = st ? st.steps.findIndex(function (x, k) { return st.done.indexOf(k) < 0; }) : -1;
    if (!st || i < 0) { card.hidden = true; return; }
    $("nextTitle").textContent = st.steps[i][1];
    $("nextGo").setAttribute("href", st.steps[i][0]);
    $("nextGo").dataset.i = i;
    $("nextCount").textContent = "Step " + (st.done.length + 1) + " of " + st.steps.length;
    card.hidden = false;
  }
  $("nextGo").addEventListener("click", function () { markNext(); });
  $("nextDone").addEventListener("click", function () { markNext(); });
  function markNext() {
    var st = store.get("start", null), i = parseInt($("nextGo").dataset.i, 10);
    if (st && st.done.indexOf(i) < 0) { st.done.push(i); store.set("start", st); }
    setTimeout(renderNext, 50);
  }
  $("nextReset").addEventListener("click", function () { store.set("start", null); renderNext(); location.hash = "start"; });
  renderNext();

  /* ---------- Was this helpful? ---------- */
  document.addEventListener("click", function (e) {
    var b = e.target.closest(".fb button");
    if (!b) return;
    var box = b.closest(".fb");
    countEvent("helpful-" + box.dataset.fb + "-" + b.dataset.v);
    box.innerHTML = '<p class="small muted">Thank you. This helps us improve Kinav.</p>';
  });

  /* ---------- Send to family ---------- */
  // Shares a short summary through the phone's share sheet, or WhatsApp where that isn't available.
  function shareSummary(kind) {
    var lines = [];
    var pick = function (sel) { return Array.prototype.map.call(document.querySelectorAll(sel), function (n) { return n.textContent.replace(/ ›$/, "").trim(); }); };
    if (kind === "stayhome") lines = ["Steps to help them stay at home:"].concat(pick("#shPlan h3"));
    if (kind === "start") lines = ["Our first steps:"].concat(pick("#stOut h3"));
    if (kind === "costs") lines = ["Care costs (estimate):"].concat(pick("#cmpOut .cmp-box").map(function (t) { return t.replace(/\s+/g, " "); }));
    if (kind === "benefits") lines = ["Benefits worth checking:"].concat(pick("#benResults .card h3"));
    if (kind === "house") lines = ["Will they have to sell the house to pay for care? Often not. The rules explained:"];
    var text = lines.join("\n") + "\n\nFrom Kinav, free help for families: https://kinav.co.uk";
    if (navigator.share) { navigator.share({ title: "Kinav", text: text }).catch(function () {}); return; }
    window.open("https://wa.me/?text=" + encodeURIComponent(text), "_blank", "noopener");
  }
  document.addEventListener("click", function (e) {
    var b = e.target.closest("[data-share]");
    if (b) { shareSummary(b.dataset.share); countEvent("share-" + b.dataset.share); }
  });

  /* ---------- Add to home screen ---------- */
  // One clear button: installs in one tap where the browser allows it, otherwise shows simple steps.
  var installEvent = null;
  var SHARE_ICON = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-label="Share"><path d="M12 3v12M7 8l5-5 5 5"/><path d="M5 12v7a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2v-7"/></svg>';
  function installSteps() {
    var ua = navigator.userAgent;
    if (/iphone|ipad|ipod/i.test(ua)) return [
      "Tap the Share button " + SHARE_ICON + " at the bottom of the screen (at the top on iPad).",
      "Scroll down and tap <b>Add to Home Screen</b>.",
      "Tap <b>Add</b>. Kinav now opens like an app from your home screen."];
    return [
      "Tap the browser menu <b>⋮</b> at the top right.",
      "Tap <b>Add to Home screen</b> or <b>Install app</b>.",
      "Tap <b>Add</b> or <b>Install</b>. Kinav now opens like an app from your home screen."];
  }
  function showInstall() {
    var standalone = (window.matchMedia && window.matchMedia("(display-mode: standalone)").matches) || navigator.standalone;
    if (standalone) { $("installCard").hidden = true; return; }
    $("installHow").textContent = "Open Kinav like an app, straight from your phone. It takes 10 seconds.";
  }
  window.addEventListener("beforeinstallprompt", function (e) { e.preventDefault(); installEvent = e; showInstall(); });
  window.addEventListener("appinstalled", function () { $("installCard").hidden = true; });
  $("installBtn").addEventListener("click", function () {
    countEvent("install-tap");
    if (installEvent) { installEvent.prompt(); installEvent = null; return; }
    var list = $("installSteps");
    list.innerHTML = installSteps().map(function (t) { return "<li><span>" + t + "</span></li>"; }).join("");
    list.hidden = !list.hidden;
  });
  showInstall();

  // Header button: "Get the app" until Kinav is on the home screen, then a text-size switch.
  function isStandalone() { return (window.matchMedia && window.matchMedia("(display-mode: standalone)").matches) || navigator.standalone; }
  function setHdr() { $("hdrBtn").textContent = isStandalone() ? (store.get("bigtext", false) ? "Normal text" : "Larger text") : "Get the app"; }
  $("hdrBtn").addEventListener("click", function () {
    if (isStandalone()) { $("bigText").click(); setHdr(); return; }
    if (installEvent) { installEvent.prompt(); installEvent = null; return; }
    location.hash = "home";
    setTimeout(function () {
      var list = $("installSteps");
      list.innerHTML = installSteps().map(function (t) { return "<li><span>" + t + "</span></li>"; }).join("");
      list.hidden = false;
      $("installCard").hidden = false;
      $("installCard").scrollIntoView({ behavior: "smooth", block: "center" });
    }, 150);
  });

  /* ---------- Larger text ---------- */
  function applyBig(on) { document.documentElement.classList.toggle("big", on); $("bigText").setAttribute("aria-pressed", String(on)); $("bigText").textContent = on ? "Normal text" : "Larger text"; }
  applyBig(store.get("bigtext", false));
  $("bigText").addEventListener("click", function () { var on = !store.get("bigtext", false); store.set("bigtext", on); applyBig(on); setHdr(); });
  setHdr();

  /* ---------- Stay at home plan ---------- */
  // Five yes/no questions build a list of practical next steps. Nothing is saved.
  var SH_Q = [
    { id: "alone", q: "Do they live alone?" },
    { id: "move", q: "Are stairs or getting around the home getting harder?" },
    { id: "wash", q: "Do they need help washing or bathing?" },
    { id: "fall", q: "Have they had a fall in the last year, or are they worried about falling?" },
    { id: "meals", q: "Do they need help with meals or shopping?" }
  ];
  var shAns = {};
  $("shForm").innerHTML = SH_Q.map(function (q) {
    return '<fieldset class="card" style="border:0;margin:0"><legend class="label" style="padding:0;margin-bottom:8px">' + esc(q.q) + "</legend>" +
      '<div class="seg" style="grid-template-columns:repeat(2,minmax(0,1fr))">' +
      ["Yes", "No"].map(function (o) {
        var id = "sh-" + q.id + "-" + o;
        return '<input type="radio" name="' + q.id + '" id="' + id + '" value="' + o + '"><label for="' + id + '">' + o + "</label>";
      }).join("") + "</div></fieldset>";
  }).join("");
  $("shForm").addEventListener("change", function (e) { shAns[e.target.name] = e.target.value === "Yes"; renderStayHome(); });
  $("shForm").addEventListener("submit", function (e) { e.preventDefault(); });

  function renderStayHome() {
    var a = shAns, left = SH_Q.length - Object.keys(a).length;
    if (left > 0) { $("shPlan").innerHTML = '<p class="small muted">' + left + " more to answer.</p>"; return; }
    var steps = [];
    var add = function (tag, title, why, href, link) { steps.push({ tag: tag, title: title, why: why, href: href, link: link }); };
    // Steps in priority order, so the free top five mix practical help and money.
    add("Free", "Ask the council for a needs assessment", "Anyone can ask, whatever their savings. Ask for a carer's assessment for yourself too.", "#kit-home-care", "How to ask");
    if (a.move || a.wash || a.fall) add("Free", "Ask for an occupational therapy (OT) assessment", "An OT visits the home and recommends changes. Equipment and small changes under £1,000 are then free.", "#kit-safety", "Home safety and grants guide");
    if (a.move || a.wash || a.fall || a.meals) add("Money", "Check Attendance Allowance", "If they're over State Pension age and need help, it's £76.70 or £114.60 a week and isn't means-tested.", "#benefits", "Check what they could get");
    if (a.wash || a.meals) add("Care", "Help at home, rated Good or Outstanding", "Home care can help with washing, dressing and meals.", "#care", "Find care at home near them");
    if (a.fall || a.alone) add("Help", "A fall alarm", "A pendant or watch that calls for help at the press of a button.", "#kit-alarms", "Fall alarms guide");
    if (a.move || a.wash) add("Grant", "Disabled Facilities Grant, up to £30,000", "For bigger changes such as a stairlift or level-access shower. Means-tested; the council decides.", "https://www.gov.uk/disabled-facilities-grants", "GOV.UK guide");
    if (a.alone) add("Money", "Council tax discount for living alone", "Usually 25% off the bill. More off is possible in some situations, such as dementia.", "https://www.gov.uk/council-tax/discounts-for-people-living-alone", "GOV.UK guide");
    if (a.alone) add("Free", "A free fire safety visit", "Your local fire and rescue service can check the home and fit smoke alarms.", "#kit-safety", "Home safety guide");
    if (a.meals) add("Help", "Meals and shopping support", "Ask the council or Age UK about meal deliveries, shopping help and lunch clubs.", "https://www.ageuk.org.uk/services/in-your-area/", "Find local Age UK");
    add("Plan", "Home or care home: the real cost", "See what staying at home with help costs compared with a care home.", "#costs", "Compare costs");
    // Free version: the five most important steps, in order of priority.
    steps = steps.slice(0, 5);
    $("shShare").hidden = false;
    var pill = { Free: "pill-good", Grant: "pill-sun", Money: "pill-sun", Help: "pill-quiet", Care: "pill-good", Plan: "pill-quiet" };
    $("shPlan").innerHTML = "<h2>Their top " + steps.length + " steps</h2>" + steps.map(function (st, i) {
      var ext = /^https?:/.test(st.href);
      return '<div class="card shstep"><div class="head"><h3>' + (i + 1) + ". " + esc(st.title) + '</h3><span class="pill ' + pill[st.tag] + '">' + st.tag + "</span></div>" +
        '<p class="small">' + esc(st.why) + '</p><a class="small" style="font-weight:600" href="' + st.href + '"' + (ext ? ' target="_blank" rel="noopener"' : "") + ">" + esc(st.link) + " ›</a></div>";
    }).join("");
  }

  /* ---------- Home or care home ---------- */
  var SAVINGS_LIMIT = 23250;
  function cmpLasts(weeklyCost, income, savings) {
    var fromSavings = weeklyCost - income, usable = Math.max(0, savings - SAVINGS_LIMIT);
    if (fromSavings <= 0) return "Income covers it";
    if (!usable) return "Council help now";
    var weeks = usable / fromSavings;
    if (weeks < 104) return "About " + Math.max(1, Math.round(weeks / 4.33)) + " months";
    return weeks / 52 >= 20 ? "Over 20 years" : "About " + Math.round(weeks / 52) + " years";
  }
  function renderCompare() {
    var num = function (id) { var v = parseFloat($(id).value); return isNaN(v) || v < 0 ? 0 : v; };
    var home = num("cmpHours") * num("cmpRate"), ch = num("cmpHome"), inc = num("cmpIncome"), sav = num("cmpSavings");
    var gbp = function (v) { return "£" + Math.round(v).toLocaleString("en-GB"); };
    $("cmpOut").innerHTML =
      '<div class="cmp-box home"><span>At home with care</span><b>' + gbp(home) + '</b><span>a week</span><span>Savings: ' + cmpLasts(home, inc, sav) + "</span></div>" +
      '<div class="cmp-box"><span>Care home</span><b>' + gbp(ch) + '</b><span>a week</span><span>Savings: ' + cmpLasts(ch, inc, sav) + "</span></div>";
  }
  $("cmp").addEventListener("input", renderCompare);
  $("cmp").addEventListener("submit", function (e) { e.preventDefault(); });
  renderCompare();

  /* ---------- Benefits calculator ---------- */
  var answers = {};
  $("benForm").innerHTML = KC.benefits.questions.map(function (q) {
    return '<fieldset class="card" style="border:0;margin:0"><legend class="label" style="padding:0;margin-bottom:8px">' + esc(q.q) + "</legend>" +
      '<div class="seg" style="grid-template-columns:repeat(' + q.options.length + ',minmax(0,1fr))">' +
      q.options.map(function (o, i) {
        var id = "b-" + q.id + "-" + i;
        return '<input type="radio" name="' + q.id + '" id="' + id + '" value="' + esc(o) + '"><label for="' + id + '">' + esc(o) + "</label>";
      }).join("") + "</div></fieldset>";
  }).join("");
  $("benForm").addEventListener("change", function (e) { answers[e.target.name] = e.target.value; renderBenefits(); });
  $("benForm").addEventListener("submit", function (e) { e.preventDefault(); });

  function renderBenefits() {
    var a = answers, out = [];
    var need = KC.benefits.questions.length - Object.keys(a).length;
    if (need > 0) { $("benResults").innerHTML = '<p class="small muted">' + need + " more to answer.</p>"; return; }
    var spa = a.age === "Yes";
    if (spa && a.help === "Yes") out.push(["Attendance Allowance", "Them", "Likely", "They're over State Pension age and have needed help for 6 months. £76.70 or £114.60 a week, and not means-tested.", "https://www.gov.uk/attendance-allowance"]);
    else if (spa && a.help === "Not yet") out.push(["Attendance Allowance", "Them", "Worth checking", "They can usually claim once they've needed help for 6 months, or straight away if terminally ill.", "https://www.gov.uk/attendance-allowance"]);
    else if (!spa) out.push(["Personal Independence Payment", "Them", "Worth checking", "Under State Pension age, PIP is the benefit for extra daily living or mobility needs.", "https://www.gov.uk/pip"]);
    if (a.income !== "No" && spa) out.push(["Pension Credit", "Them", "Worth checking", "Tops up a low income. Getting Attendance Allowance can increase it.", "https://www.gov.uk/pension-credit"]);
    out.push(["Council tax discount", "Their household", "Worth checking",
      a.alone === "Yes" ? "If they live alone with dementia or another condition affecting memory, council tax can be cut by up to 100%." : "There are discounts and disregards for people with severe mental impairment, such as dementia.",
      "https://www.gov.uk/council-tax/discounts-for-disabled-people"]);
    if (a.hours !== "Under 20") out.push(["Carer's Credit", "You", "Likely", "You care 20 or more hours a week. It protects your State Pension.", "https://www.gov.uk/carers-credit"]);
    if (a.hours === "35 or more" && a.earn === "No") out.push(["Carer's Allowance", "You", "Worth checking", "You care 35+ hours a week and earn £204 a week or less. The person you care for must get a qualifying benefit, such as Attendance Allowance.", "https://www.gov.uk/carers-allowance"]);
    else out.push(["Carer's Allowance", "You", "Unlikely", "Needs 35+ hours caring a week and earnings of £204 a week or less.", "https://www.gov.uk/carers-allowance/eligibility"]);
    out.push(["Blue Badge", "Them", "Worth checking", "Some non-visible conditions, including dementia, can qualify. See the step-by-step Blue Badge kit in Help.", "https://www.gov.uk/apply-blue-badge"]);
    out.push(["Carer's assessment", "You", "Likely", "Free from the council for anyone who cares. It can lead to support for you.", "https://www.nhs.uk/social-care-and-support/support-and-benefits-for-carers/carer-assessments/"]);
    var pill = { Likely: "pill-good", "Worth checking": "pill-sun", Unlikely: "pill-quiet" };
    var order = { Likely: 0, "Worth checking": 1, Unlikely: 2 };
    out.sort(function (x, y) { return order[x[2]] - order[y[2]]; });
    var likely = out.filter(function (o) { return o[2] === "Likely"; }).length;
    // A yearly "could be missing" figure from the two benefits with fixed rates (2026 to 2027 rates).
    var yearly = 0, maybe = function (name) { return out.some(function (o) { return o[0] === name && o[2] !== "Unlikely"; }); };
    if (maybe("Attendance Allowance")) yearly += 114.60 * 52;
    if (maybe("Carer's Allowance")) yearly += 86.45 * 52;
    var headline = yearly ? '<div class="money-head"><span class="small">Your family could be missing up to</span><b>£' + Math.round(yearly / 100) * 100 + ' a year</b><span class="tiny">From Attendance Allowance and Carer\'s Allowance at 2026 to 2027 rates, plus any council tax or Pension Credit. The Department for Work and Pensions decides.</span></div>' : "";
    $("benShare").hidden = false;
    $("benResults").innerHTML = headline + '<h2>' + likely + " likely, " + out.filter(function (o) { return o[2] === "Worth checking"; }).length + " worth checking</h2>" +
      out.map(function (o) {
        return '<div class="card"><div class="head"><h3>' + esc(o[0]) + '</h3><span class="pill ' + pill[o[2]] + '">' + esc(o[2]) + "</span></div>" +
          '<p class="tiny muted">For ' + esc(o[1].toLowerCase()) + "</p><p class=\"small\">" + esc(o[3]) + "</p>" +
          '<a class="small" style="font-weight:600" href="' + o[4] + '" target="_blank" rel="noopener">' + (o[4].indexOf("nhs.uk") >= 0 ? "See NHS" : "See GOV.UK") + ' ›</a></div>';
      }).join("");
  }

  /* ---------- Help and kits ---------- */
  $("helplines").innerHTML = KC.helplines.map(function (h) {
    return '<div><p style="font-weight:600">' + esc(h.name) + '</p><p><a class="phone" style="font-size:18px;font-weight:700;text-decoration:none" href="tel:' + h.number.replace(/\s/g, "") + '">' + esc(h.number) + '</a></p><p class="tiny muted">' + esc(h.note) + "</p></div>";
  }).join("");

  function kitDone(id) { return store.get("kit." + id, {}); }

  $("kitList").innerHTML = KC.kits.map(function (k) {
    return '<a class="card" style="text-decoration:none;color:inherit" href="#kit-' + k.id + '"><div class="head"><h3>' + esc(k.name) + '</h3><span class="tiny" style="color:var(--accent);font-weight:600;white-space:nowrap">' + k.steps.length + " steps ›</span></div>" +
      '<p class="small muted">' + esc(k.what) + "</p></a>";
  }).join("");

  function renderKit(id) {
    var k = KC.kits.filter(function (x) { return x.id === id; })[0];
    if (!k) { location.hash = "help"; return; }
    var done = kitDone(id);
    $("kitTitle").textContent = k.name;
    $("kitWhat").textContent = k.what;
    $("kitSteps").innerHTML = k.steps.map(function (s, i) {
      var d = !!done[i];
      return '<button class="task kitstep" type="button" data-i="' + i + '" data-done="' + d + '" aria-pressed="' + d + '">' +
        '<span class="n" aria-hidden="true">' + (d ? tick() : i + 1) + '</span><span class="stack-sm" style="gap:2px"><span class="tt">' + esc(s.t) + '</span><span class="small muted">' + esc(s.d) + "</span></span></button>";
    }).join("");
    $("kitSteps").dataset.kit = id;
  }
  $("kitSteps").addEventListener("click", function (e) {
    var b = e.target.closest(".kitstep");
    if (!b) return;
    var id = $("kitSteps").dataset.kit, done = kitDone(id);
    done[b.dataset.i] = !done[b.dataset.i];
    store.set("kit." + id, done);
    renderKit(id);
  });

  /* ---------- Articles ---------- */
  var todayIso = new Date().toISOString().slice(0, 10);
  KC.articles = KC.articles.filter(function (a) { return !a.from || a.from <= todayIso; });
  var latest = KC.articles[0];
  $("homeArticleMonth").textContent = latest.month + " · " + latest.topic;
  $("homeArticleTitle").textContent = latest.title;
  $("homeArticle").href = "#article-" + latest.id;
  $("articleList").innerHTML = KC.articles.map(function (a) {
    return '<a class="card" style="text-decoration:none;color:inherit" href="#article-' + a.id + '"><span class="eyebrow">' + esc(a.month + " · " + a.topic) + "</span><h3>" + esc(a.title) + "</h3></a>";
  }).join("");

  function renderArticle(id) {
    var a = KC.articles.filter(function (x) { return x.id === id; })[0];
    if (!a) { location.hash = "articles"; return; }
    $("articleBody").innerHTML =
      '<div class="stack-sm"><span class="eyebrow">' + esc(a.month + " · " + a.topic) + "</span><h1>" + esc(a.title) + '</h1><p class="lede">' + esc(a.intro) + "</p></div>" +
      a.sections.map(function (sec) {
        return '<div class="stack-sm"><h2>' + esc(sec.h) + "</h2>" +
          (sec.p || []).map(function (t) { return "<p>" + esc(t) + "</p>"; }).join("") +
          (sec.list ? '<ul class="plain">' + sec.list.map(function (t) { return "<li>" + esc(t) + "</li>"; }).join("") + "</ul>" : "") + "</div>";
      }).join("") +
      (a.plan && KC.plans[a.plan] ? '<a class="btn btn-primary" href="#plan" data-plan="' + a.plan + '">Open the ' + esc(KC.plans[a.plan].name) + " 30-day plan</a>" : "") +
      '<div class="stack-sm"><h3>Sources</h3><ul class="plain tiny">' + a.sources.map(function (src) {
        return '<li><a href="' + esc(src.url) + '" target="_blank" rel="noopener">' + esc(src.name) + "</a></li>";
      }).join("") + '</ul><p class="tiny muted">Kinav does not give health advice. For health questions, speak to the GP, a pharmacist or NHS 111, and call 999 in an emergency.</p></div>';
  }
  $("articleBody").addEventListener("click", function (e) {
    var b = e.target.closest("[data-plan]");
    if (b) { store.set("guide", b.dataset.plan); renderPlan(); }
  });

  /* ---------- Privacy ---------- */
  $("wipe").addEventListener("click", function () {
    try {
      mem = {};
      Object.keys(localStorage).forEach(function (k) { if (k.indexOf("kc.") === 0) localStorage.removeItem(k); });
    } catch (e) {}
    $("homePostcode").value = ""; $("careQ").value = "";
    renderPlan();
    $("wipeDone").hidden = false;
  });

  /* ---------- Start ---------- */
  renderPlan();
  fillDefaults();
  renderCosts();
  show();
  if ("serviceWorker" in navigator && location.protocol === "https:") {
    try { navigator.serviceWorker.register("sw.js", { updateViaCache: "none" }).catch(function () {}); } catch (e) {}
  }
})();

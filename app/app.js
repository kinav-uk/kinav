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
  var SCREENS = ["home", "plan", "appts", "care", "costs", "benefits", "help", "kit", "privacy", "terms", "articles", "article"];
  var TAB_FOR = { costs: "home", benefits: "home", kit: "help", privacy: "home", terms: "home", articles: "home", article: "home" };

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
    window.scrollTo(0, 0);
  }
  window.addEventListener("hashchange", show);

  /* ---------- 30-day plans ---------- */
  function planDone() { return store.get("plan", {}); }
  function planKey() { var k = store.get("guide", "dementia"); return KC.plans[k] ? k : "dementia"; }

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
    $("planTitle").textContent = plan.title;
    $("planLede").textContent = plan.lede + " Ticks are saved on this phone only.";
    fillPick($("planPick"), key);
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
    sel.innerHTML = group("condition", "Conditions") + group("situation", "Situations");
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
    var key = planKey(), st = planStats(key);
    $("homePlanTitle").textContent = "Your 30-day plan";
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
  $("apptForm").addEventListener("input", updateAppt);
  $("apptForm").addEventListener("submit", function (e) { e.preventDefault(); });
  ["apGoogle", "apIcs"].forEach(function (id) {
    $(id).addEventListener("click", function (e) {
      if (!$("apDate").value) { e.preventDefault(); $("apError").hidden = false; $("apDate").focus(); }
    });
  });

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

  /* ---------- Benefits check ---------- */
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
    if (spa && a.help === "Yes") out.push(["Attendance Allowance", "Them", "Likely", "They're over State Pension age and have needed help for 6 months. Not means-tested.", "https://www.gov.uk/attendance-allowance"]);
    else if (spa && a.help === "Not yet") out.push(["Attendance Allowance", "Them", "Worth checking", "They can usually claim once they've needed help for 6 months, or straight away if terminally ill.", "https://www.gov.uk/attendance-allowance"]);
    else if (!spa) out.push(["Personal Independence Payment", "Them", "Worth checking", "Under State Pension age, PIP is the benefit for extra daily living or mobility needs.", "https://www.gov.uk/pip"]);
    if (a.income !== "No" && spa) out.push(["Pension Credit", "Them", "Worth checking", "Tops up a low income. Getting Attendance Allowance can increase it.", "https://www.gov.uk/pension-credit"]);
    out.push(["Council tax discount", "Their household", "Worth checking",
      a.alone === "Yes" ? "If they live alone with dementia or another condition affecting memory, council tax can be cut by up to 100%." : "There are discounts and disregards for people with severe mental impairment, such as dementia.",
      "https://www.gov.uk/council-tax/discounts-for-disabled-people"]);
    if (a.hours !== "Under 20") out.push(["Carer's Credit", "You", "Likely", "You care 20 or more hours a week. It protects your State Pension.", "https://www.gov.uk/carers-credit"]);
    if (a.hours === "35 or more" && a.earn === "No") out.push(["Carer's Allowance", "You", "Worth checking", "You care 35+ hours a week and earn £204 a week or less. The person you care for must get a qualifying benefit, such as Attendance Allowance.", "https://www.gov.uk/carers-allowance"]);
    else out.push(["Carer's Allowance", "You", "Unlikely", "Needs 35+ hours caring a week and earnings of £204 a week or less.", "https://www.gov.uk/carers-allowance/eligibility"]);
    out.push(["Blue Badge", "Them", "Worth checking", "Some non-visible conditions, including dementia, can qualify.", "https://www.gov.uk/apply-blue-badge"]);
    out.push(["Carer's assessment", "You", "Likely", "Free from the council for anyone who cares. It can lead to support for you.", "https://www.gov.uk/carers-assessment"]);
    var pill = { Likely: "pill-good", "Worth checking": "pill-sun", Unlikely: "pill-quiet" };
    var order = { Likely: 0, "Worth checking": 1, Unlikely: 2 };
    out.sort(function (x, y) { return order[x[2]] - order[y[2]]; });
    var likely = out.filter(function (o) { return o[2] === "Likely"; }).length;
    $("benResults").innerHTML = '<h2>' + likely + " likely, " + out.filter(function (o) { return o[2] === "Worth checking"; }).length + " worth checking</h2>" +
      out.map(function (o) {
        return '<div class="card"><div class="head"><h3>' + esc(o[0]) + '</h3><span class="pill ' + pill[o[2]] + '">' + esc(o[2]) + "</span></div>" +
          '<p class="tiny muted">For ' + esc(o[1].toLowerCase()) + "</p><p class=\"small\">" + esc(o[3]) + "</p>" +
          '<a class="small" style="font-weight:600" href="' + o[4] + '" target="_blank" rel="noopener">See GOV.UK ›</a></div>';
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

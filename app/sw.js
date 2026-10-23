// Offline support: keep the app shell cached; care data is fetched fresh, falling back to the cache.
var SHELL = "kinav-shell-v37";
var FILES = ["./", "index.html", "content.js", "app.js", "manifest.webmanifest", "icon.svg", "data/index.json"];
self.addEventListener("install", function (e) {
  self.skipWaiting(); // a new version takes over straight away instead of waiting for every tab to close
  e.waitUntil(caches.open(SHELL).then(function (c) { return c.addAll(FILES); }));
});
self.addEventListener("activate", function (e) {
  e.waitUntil(caches.keys().then(function (keys) {
    return Promise.all(keys.filter(function (k) { return k !== SHELL && k !== "kinav-data"; }).map(function (k) { return caches.delete(k); }));
  }).then(function () { return self.clients.claim(); }));
});
self.addEventListener("fetch", function (e) {
  var url = new URL(e.request.url);
  if (e.request.method !== "GET" || url.origin !== location.origin) return;
  e.respondWith(fetch(e.request, { cache: "no-cache" }).then(function (res) {
    var copy = res.clone();
    caches.open(url.pathname.indexOf("/data/") >= 0 ? "kinav-data" : SHELL).then(function (c) { c.put(e.request, copy); });
    return res;
  }).catch(function () { return caches.match(e.request); }));
});

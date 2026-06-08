// Camp Raad Dojo — Service Worker v4
// Forces fresh HTML on every navigation → no more stale cached pages

const SW_VERSION = 'camp-raad-v4';

self.addEventListener('install', e => {
  e.waitUntil(self.skipWaiting());
});

self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys().then(keys =>
      Promise.all(keys.filter(k => k !== SW_VERSION).map(k => caches.delete(k)))
    ).then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', event => {
  const req = event.request;
  const url = new URL(req.url);

  // HTML pages: always fetch fresh from network (bypass cache completely)
  if(req.mode === 'navigate' || url.pathname.endsWith('.html')){
    event.respondWith(
      fetch(req, { cache: 'no-store' })
        .catch(() => caches.match(req)) // fallback if offline
    );
    return;
  }
  // Everything else (images, fonts, JS data files): normal caching
});

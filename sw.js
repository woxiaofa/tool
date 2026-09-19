/* =====================================================================
 *  文本格式化工具箱 — Service Worker
 *  作用：把整个工具缓存到本地，实现「离线可用」，契合纯本地运行的定位。
 *  注意：file:// 直接打开时不会注册 SW，不影响使用。
 * ===================================================================== */

const CACHE = 'text-formatter-v1';

/* 需要预缓存的核心资源（全部为静态文件） */
const PRECACHE = [
  './',
  './index.html',
  './en/',
  './manifest.webmanifest',
  './favicon.svg',
  './icon-192.png',
  './icon-512.png',
  './llms.txt',
  './assets/alipay-qr.jpg'
];

self.addEventListener('install', event => {
  self.skipWaiting();
  event.waitUntil(
    caches.open(CACHE)
      .then(cache => cache.addAll(PRECACHE).catch(() => undefined))
  );
});

self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(keys =>
      Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k)))
    ).then(() => self.clients.claim())
  );
});

/* 缓存优先 + 后台更新：断网时依然秒开 */
self.addEventListener('fetch', event => {
  const req = event.request;
  if (req.method !== 'GET') return;
  const url = new URL(req.url);
  if (url.origin !== self.location.origin) return;

  event.respondWith(
    caches.match(req).then(cached => {
      const network = fetch(req)
        .then(res => {
          if (res && res.status === 200 && res.type === 'basic') {
            const copy = res.clone();
            caches.open(CACHE).then(c => c.put(req, copy));
          }
          return res;
        })
        .catch(() => cached);
      return cached || network;
    })
  );
});

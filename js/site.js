/* Afro Code Academy — site behaviour (no dependencies) */
(function () {
  var doc = document.documentElement;
  doc.classList.add('js');

  // Sticky header shadow + mobile navigation
  var header = document.querySelector('.site-header');
  var toggle = document.querySelector('.nav-toggle');
  if (header) {
    var onScroll = function () { header.classList.toggle('is-scrolled', window.scrollY > 8); };
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });
  }
  if (header && toggle) {
    toggle.addEventListener('click', function () {
      var open = header.classList.toggle('nav-open');
      toggle.setAttribute('aria-expanded', String(open));
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && header.classList.contains('nav-open')) {
        header.classList.remove('nav-open');
        toggle.setAttribute('aria-expanded', 'false');
        toggle.focus();
      }
    });
  }

  // Email links are assembled here so the address isn't a plain mailto in the HTML
  document.querySelectorAll('[data-mail]').forEach(function (el) {
    var addr = el.getAttribute('data-mail').replace('(at)', '@');
    var query = ['subject', 'body']
      .filter(function (k) { return el.hasAttribute('data-' + k); })
      .map(function (k) { return k + '=' + encodeURIComponent(el.getAttribute('data-' + k)); });
    el.setAttribute('href', 'mailto:' + addr + (query.length ? '?' + query.join('&') : ''));
  });

  // Reveal-on-scroll
  var reveals = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window && reveals.length) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) { entry.target.classList.add('is-in'); io.unobserve(entry.target); }
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
    reveals.forEach(function (el) { io.observe(el); });
  } else {
    reveals.forEach(function (el) { el.classList.add('is-in'); });
  }

  // Lightbox for [data-lightbox] links
  var items = Array.prototype.slice.call(document.querySelectorAll('a[data-lightbox]'));
  if (!items.length) return;

  var de = doc.lang === 'de';
  var t = de
    ? { close: 'Schließen', prev: 'Vorheriges Foto', next: 'Nächstes Foto', of: 'von' }
    : { close: 'Close', prev: 'Previous photo', next: 'Next photo', of: 'of' };
  var icon = function (d) {
    return '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="' + d + '"/></svg>';
  };

  var box = document.createElement('div');
  box.className = 'lightbox';
  box.hidden = true;
  box.setAttribute('role', 'dialog');
  box.setAttribute('aria-modal', 'true');
  box.innerHTML =
    '<div class="lb-top"><span class="lb-count" aria-live="polite"></span>' +
    '<button class="lb-btn lb-close" type="button" aria-label="' + t.close + '">' + icon('M6 6l12 12M18 6L6 18') + '</button></div>' +
    '<div class="lb-stage">' +
    '<button class="lb-btn lb-prev" type="button" aria-label="' + t.prev + '">' + icon('M15 5l-7 7 7 7') + '</button>' +
    '<img alt="">' +
    '<button class="lb-btn lb-next" type="button" aria-label="' + t.next + '">' + icon('M9 5l7 7-7 7') + '</button>' +
    '</div><div class="lb-caption"></div>';
  document.body.appendChild(box);

  var img = box.querySelector('img');
  var cap = box.querySelector('.lb-caption');
  var count = box.querySelector('.lb-count');
  var closeBtn = box.querySelector('.lb-close');
  var index = 0;
  var lastFocus = null;

  function show(i) {
    index = (i + items.length) % items.length;
    var a = items[index];
    var thumb = a.querySelector('img');
    img.src = a.getAttribute('href');
    img.alt = thumb ? thumb.alt : '';
    cap.textContent = a.getAttribute('data-caption') || (thumb ? thumb.alt : '');
    count.textContent = (index + 1) + ' ' + t.of + ' ' + items.length;
    // Preload neighbours
    [index + 1, index - 1].forEach(function (n) {
      var p = new Image();
      p.src = items[(n + items.length) % items.length].getAttribute('href');
    });
  }
  function open(i) {
    lastFocus = document.activeElement;
    show(i);
    box.hidden = false;
    document.body.style.overflow = 'hidden';
    closeBtn.focus();
  }
  function close() {
    box.hidden = true;
    document.body.style.overflow = '';
    img.removeAttribute('src');
    if (lastFocus) lastFocus.focus();
  }

  items.forEach(function (a, i) {
    a.addEventListener('click', function (e) { e.preventDefault(); open(i); });
  });
  closeBtn.addEventListener('click', close);
  box.querySelector('.lb-prev').addEventListener('click', function () { show(index - 1); });
  box.querySelector('.lb-next').addEventListener('click', function () { show(index + 1); });
  box.addEventListener('click', function (e) {
    if (e.target === box || e.target.classList.contains('lb-stage')) close();
  });
  document.addEventListener('keydown', function (e) {
    if (box.hidden) return;
    if (e.key === 'Escape') close();
    else if (e.key === 'ArrowLeft') show(index - 1);
    else if (e.key === 'ArrowRight') show(index + 1);
    else if (e.key === 'Tab') {
      var f = box.querySelectorAll('button');
      var first = f[0], last = f[f.length - 1];
      if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
      else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
    }
  });

  // Swipe on touch screens
  var x0 = null;
  box.addEventListener('touchstart', function (e) { x0 = e.touches[0].clientX; }, { passive: true });
  box.addEventListener('touchend', function (e) {
    if (x0 === null) return;
    var dx = e.changedTouches[0].clientX - x0;
    if (Math.abs(dx) > 50) show(index + (dx < 0 ? 1 : -1));
    x0 = null;
  });
})();

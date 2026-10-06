document.addEventListener('DOMContentLoaded', function () {
  var track = document.getElementById('csTrack');
  var prevBtn = document.getElementById('csPrev');
  var nextBtn = document.getElementById('csNext');
  var panelWrap = document.getElementById('csPanelWrap');
  var panelInner = document.getElementById('csPanelInner');
  if (!track || !panelWrap) return;

  var cards = Array.from(track.querySelectorAll('.cs-card'));
  var GAP = 18;

  function cardW() {
    return (cards[0] ? cards[0].getBoundingClientRect().width : 290) + GAP;
  }

  function updateNav() {
    if (prevBtn) prevBtn.disabled = track.scrollLeft <= 1;
    if (nextBtn) nextBtn.disabled = track.scrollLeft >= track.scrollWidth - track.clientWidth - 2;
  }

  track.addEventListener('scroll', updateNav, { passive: true });

  if (prevBtn) {
    prevBtn.addEventListener('click', function () {
      track.scrollBy({ left: -cardW(), behavior: 'smooth' });
    });
  }
  if (nextBtn) {
    nextBtn.addEventListener('click', function () {
      track.scrollBy({ left: cardW(), behavior: 'smooth' });
    });
  }

  /* Open / close panel */
  function openPanel(card) {
    var tpl = card.querySelector('template');
    if (!tpl) return;

    /* Deactivate all, activate clicked */
    cards.forEach(function (c) { c.classList.remove('cs-active'); });
    card.classList.add('cs-active');

    /* Stamp template into panel */
    panelInner.innerHTML = '';
    panelInner.appendChild(document.importNode(tpl.content, true));

    /* Wire close button */
    var closeBtn = panelInner.querySelector('.cs-close-btn');
    if (closeBtn) closeBtn.addEventListener('click', closePanel);

    /* Open */
    panelWrap.classList.add('open');

    /* Scroll to panel */
    requestAnimationFrame(function () {
      var headerEl = document.getElementById('app-header');
      var headerH = headerEl ? headerEl.getBoundingClientRect().bottom : 80;
      var el = panelWrap, docTop = 0;
      while (el) { docTop += el.offsetTop; el = el.offsetParent; }
      window.scrollTo({ top: docTop - headerH - 16, behavior: 'smooth' });
    });
  }

  function closePanel() {
    panelWrap.classList.remove('open');
    cards.forEach(function (c) { c.classList.remove('cs-active'); });
    setTimeout(function () {
      if (!panelWrap.classList.contains('open')) panelInner.innerHTML = '';
    }, 350);
  }

  cards.forEach(function (card) {
    card.addEventListener('click', function (e) {
      // If clicked on a link inside the panel, don't close it
      if (e.target.closest('.cs-panel-body a')) return;

      if (card.classList.contains('cs-active')) {
        closePanel();
        return;
      }
      openPanel(card);
    });
  });

  updateNav();
});
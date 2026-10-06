/**
 * our-webinars.js
 * Swiper slider for the Our webinars section.
 */
document.addEventListener('DOMContentLoaded', function () {
  new Swiper('.webinar-swiper', {
    slidesPerView: 1,
    spaceBetween: 30,
    breakpoints: {
      768: { slidesPerView: 2 },
      1200: { slidesPerView: 3 }
    },
    pagination: { el: '.swiper-pagination', clickable: true },
    navigation: { nextEl: '.webinars-button-next', prevEl: '.webinars-button-prev' },
  });
});
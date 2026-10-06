document.addEventListener('DOMContentLoaded', function () {
  const gallerySlider = document.querySelector('.gallery-slider');

  if (typeof Swiper !== 'undefined' && gallerySlider) {
    new Swiper(gallerySlider, {
      slidesPerView: 1,
      spaceBetween: 20,
      navigation: {
        nextEl: '.swiper-button-next-assist',
        prevEl: '.swiper-button-prev-assist',
      },
      pagination: {
        el: '.gallery-slider-pagination',
        clickable: true,
      },
      breakpoints: {
        768: { slidesPerView: 2, spaceBetween: 20 },
        1024: { slidesPerView: 3, spaceBetween: 20 }
      }
    })
  }

  Fancybox.bind("[data-fancybox='gallery-group']", {
    Hash: false,
  });
});
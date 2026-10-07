document.addEventListener('DOMContentLoaded', function () {
  const mediaSliderBlog = document.querySelector('.media-slider-blog');

  if (typeof Swiper !== 'undefined' && mediaSliderBlog) {
    new Swiper(mediaSliderBlog, {
      slidesPerView: 1,
      spaceBetween: 20,
      navigation: {
        nextEl: '.webinars-button-next',
        prevEl: '.webinars-button-prev',
      },
      pagination: {
        el: '.media-slider-pagination',
        clickable: true,
      },
      breakpoints: {
        768: { slidesPerView: 2, spaceBetween: 20 },
        1024: { slidesPerView: 3, spaceBetween: 20 }
      }
    })
  }
});
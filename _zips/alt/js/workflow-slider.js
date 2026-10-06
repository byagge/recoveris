document.addEventListener('DOMContentLoaded', function () {
  const workflowSlider = document.querySelector('.workflow-slider');

  if (typeof Swiper !== 'undefined' && workflowSlider) {
    new Swiper(workflowSlider, {
      slidesPerView: 1.2,
      spaceBetween: 20,
      pagination: {
        el: '.workflow-pagination',
        clickable: true,
      },
      breakpoints: {
        768: {
          enabled: false,
          slidesPerView: 5,
          spaceBetween: 50,
        }
      }
    })
  }
});
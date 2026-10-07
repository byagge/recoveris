document.addEventListener('DOMContentLoaded', function () {
  const partnersSwiper = new Swiper('.partners-swiper', {
    slidesPerView: 'auto',
    spaceBetween: 0,
    loop: true,
    loopedSlides: 20,
    speed: 8000,

    autoplay: {
      delay: 0,
      disableOnInteraction: false, // Не зупиняти після кліку
      pauseOnMouseEnter: false,    // Не зупиняти при наведенні
    },

    freeMode: {
      enabled: true,
      momentum: false,
    },

    on: {
      // Гарантований старт при завантаженні та після будь-яких подій
      init: function () {
        this.autoplay.start();
      },
      touchEnd: function () {
        setTimeout(() => {
          this.autoplay.start();
        }, 100);
      },
      click: function () {
        setTimeout(() => {
          this.autoplay.start();
        }, 100);
      }
    }
  });
});
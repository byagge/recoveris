document.addEventListener('DOMContentLoaded', function () {
  const newSliderElement = document.querySelector('.team-slider');

  if (typeof Swiper !== 'undefined' && newSliderElement) {
    new Swiper(newSliderElement, {
      direction: 'horizontal',
      loop: false,
      slidesPerView: 1,
      spaceBetween: 15,
      pagination: {
        el: '.team-slider .swiper-pagination',
        clickable: true,
      },
      navigation: {
        nextEl: "#teamSliderNext",
        prevEl: "#teamSliderPrev",
      },
      breakpoints: {
        768: {
          slidesPerView: 2,
          spaceBetween: 15,
        },
        1244: {
          slidesPerView: 3,
          spaceBetween: 30,
        },
        1400: {
          slidesPerView: 3,
          spaceBetween: 30,
        },
        1920: {
          slidesPerView: 4,
          spaceBetween: 30,
        },
      },
    });
  }

  const newSliderElement2 = document.querySelector('.team-slider-2');

  if (typeof Swiper !== 'undefined' && newSliderElement2) {
    new Swiper(newSliderElement2, {
      direction: 'horizontal',
      loop: false,
      slidesPerView: 1,
      spaceBetween: 15,
      pagination: {
        el: '.team-slider-2 .swiper-pagination',
        clickable: true,
      },
      breakpoints: {
        414: {
          slidesPerView: 2,
          spaceBetween: 15,
        },
        1244: {
          slidesPerView: 3,
          spaceBetween: 30,
        },
        1480: {
          slidesPerView: 3,
          spaceBetween: 30,
        },
      },
    });
  }

  const leadershipSlider = document.querySelector('.leadership-slider');

  if (typeof Swiper !== 'undefined' && leadershipSlider) {
    new Swiper(leadershipSlider, {
      navigation: {
        nextEl: "#leadershipSliderNext",
        prevEl: "#leadershipSliderPrev",
      },
      loop: false,
      slidesPerView: 2,
      spaceBetween: 15,
      grid: {
        rows: 1,
        fill: 'row',
      },
      breakpoints: {
        768: {
          slidesPerView: 2,
          spaceBetween: 15,
          grid: {
            rows: 1,
            fill: 'row',
          },
        },
        1024: {
          slidesPerView: 2,
          spaceBetween: 30,
          grid: {
            rows: 2,
            fill: 'row',
          },
        },
        1400: {
          slidesPerView: 2,
          spaceBetween: 30,
          grid: {
            rows: 2,
            fill: 'row',
          },
        },
        1920: {
          slidesPerView: 2,
          spaceBetween: 30,
          grid: {
            rows: 2,
            fill: 'row',
          },
        },
      },
    });
  }
  const intelligenceSlider = document.querySelector('.intelligence-slider');

  if (typeof Swiper !== 'undefined' && intelligenceSlider) {
    new Swiper(intelligenceSlider, {
      navigation: {
        nextEl: "#intelligenceSliderNext",
        prevEl: "#intelligenceSliderPrev",
      },
      loop: false,
      slidesPerView: 2,
      spaceBetween: 15,
      grid: {
        rows: 1,
        fill: 'row',
      },
      breakpoints: {
        768: {
          slidesPerView: 2,
          spaceBetween: 15,
          grid: {
            rows: 1,
            fill: 'row',
          },
        },
        1024: {
          slidesPerView: 2,
          spaceBetween: 30,
          grid: {
            rows: 5,
            fill: 'row',
          },
        },
        1400: {
          slidesPerView: 2,
          spaceBetween: 30,
          grid: {
            rows: 5,
            fill: 'row',
          },
        },
        1920: {
          slidesPerView: 2,
          spaceBetween: 30,
          grid: {
            rows: 5,
            fill: 'row',
          },
        },
      },
    });
  }
  const operationsSlider = document.querySelector('.operations-slider');

  if (typeof Swiper !== 'undefined' && operationsSlider) {
    new Swiper(operationsSlider, {
      navigation: {
        nextEl: "#operationsSliderNext",
        prevEl: "#operationsSliderPrev",
      },
      loop: false,
      slidesPerView: 2,
      spaceBetween: 15,
      grid: {
        rows: 1,
        fill: 'row',
      },
      breakpoints: {
        768: {
          slidesPerView: 2,
          spaceBetween: 15,
          grid: {
            rows: 1,
            fill: 'row',
          },
        },
        1024: {
          slidesPerView: 2,
          spaceBetween: 30,
          grid: {
            rows: 2,
            fill: 'row',
          },
        },
        1400: {
          slidesPerView: 2,
          spaceBetween: 30,
          grid: {
            rows: 2,
            fill: 'row',
          },
        },
        1920: {
          slidesPerView: 2,
          spaceBetween: 30,
          grid: {
            rows: 2,
            fill: 'row',
          },
        },
      },
    });
  }

  const techteamSlider = document.querySelector('.tech-team-slider');

  if (typeof Swiper !== 'undefined' && techteamSlider) {
    new Swiper(techteamSlider, {
      navigation: {
        nextEl: "#techteamSliderNext",
        prevEl: "#techteamSliderPrev",
      },
      loop: false,
      slidesPerView: 2,
      spaceBetween: 15,
      grid: {
        rows: 1,
        fill: 'row',
      },
      breakpoints: {
        768: {
          slidesPerView: 2,
          spaceBetween: 15,
          grid: {
            rows: 1,
            fill: 'row',
          },
        },
        1024: {
          slidesPerView: 2,
          spaceBetween: 30,
          grid: {
            rows: 5,
            fill: 'row',
          },
        },
        1400: {
          slidesPerView: 2,
          spaceBetween: 30,
          grid: {
            rows: 5,
            fill: 'row',
          },
        },
        1920: {
          slidesPerView: 2,
          spaceBetween: 30,
          grid: {
            rows: 5,
            fill: 'row',
          },
        },
      },
    });
  }

  const instructorsSlider = document.querySelector('.instructors-slider');

  if (typeof Swiper !== 'undefined' && instructorsSlider) {
    new Swiper(instructorsSlider, {
      navigation: {
        nextEl: "#techteamSliderNext",
        prevEl: "#techteamSliderPrev",
      },
      loop: false,
      slidesPerView: 2,
      spaceBetween: 15,
      grid: {
        rows: 1,
        fill: 'row',
      },
      breakpoints: {
        768: {
          slidesPerView: 2,
          spaceBetween: 15,
          grid: {
            rows: 1,
            fill: 'row',
          },
        },
        1024: {
          slidesPerView: 2,
          spaceBetween: 30,
          grid: {
            rows: 3,
            fill: 'row',
          },
        },
        1400: {
          slidesPerView: 2,
          spaceBetween: 30,
          grid: {
            rows: 3,
            fill: 'row',
          },
        },
        1920: {
          slidesPerView: 2,
          spaceBetween: 30,
          grid: {
            rows: 3,
            fill: 'row',
          },
        },
      },
    });
  }
});
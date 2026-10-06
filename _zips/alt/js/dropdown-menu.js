document.addEventListener('DOMContentLoaded', () => {
  const menuItems = document.querySelectorAll('.dropdown-menu');
  const HIDE_DELAY = 300;

  // Елементи зовнішнього скрипта
  const headerTrigger = document.querySelector('.header-trigger');
  const header = document.querySelector('.header');

  // ФУНКЦІЯ ПРИМУСОВОГО ЗАКРИТТЯ ВСІХ СТАНІВ МЕНЮ
  const closeAllMenuStates = () => {
    document.querySelectorAll('.submenu.show').forEach(openSubmenu => {
      openSubmenu.classList.remove('show');
    });
    if (headerTrigger) headerTrigger.classList.remove('active');
    if (header) header.classList.remove('active');
  };

  // Хелпер-функція для перевірки мобільного режиму (ширина менше 640px)
  const isMobile = () => window.matchMedia('(max-width: 640px)').matches;

  // ФУНКЦІЯ ДЛЯ ВИЗНАЧЕННЯ, ЧИ ЗНАХОДИМОСЯ МИ НА СТОРІНЦІ, КУДИ ВЕДЕ ЯКІР
  const isTargettingCurrentPage = (targetHref) => {
    const currentPath = window.location.pathname.replace(/\/$/, '');
    const isRoot = currentPath === '' || currentPath === '/';

    if (targetHref.includes('#')) {
      const targetPath = targetHref.split('#')[0].replace(/\/$/, '');
      if (targetPath === '' || targetPath === '/' || targetPath === currentPath) {
        return true;
      }
    }
    return false;
  };

  // Хелпер-функція для примусової зупинки спливання подій
  const stopAllPropagation = (element) => {
    ['click', 'mousedown', 'mouseup', 'touchstart', 'touchend'].forEach(event => {
      element.addEventListener(event, (e) => {
        e.stopImmediatePropagation();
      }, true);
    });
  };


  // === ОСНОВНА ЛОГІКА ОБРОБКИ МЕНЮ ===
  menuItems.forEach(item => {
    const submenu = item.querySelector('.submenu');
    const toggleLink = item.querySelector('a');
    let hideTimeout = null;

    if (submenu && toggleLink) {

      const showSubmenu = () => {
        document.querySelectorAll('.submenu.show').forEach(openSubmenu => {
          if (openSubmenu !== submenu) openSubmenu.classList.remove('show');
        });
        if (hideTimeout) clearTimeout(hideTimeout);
        submenu.classList.add('show');
      };

      const hideSubmenu = () => {
        hideTimeout = setTimeout(() => {
          submenu.classList.remove('show');
          hideTimeout = null;
        }, HIDE_DELAY);
      };

      const toggleSubmenu = () => {
        if (submenu.classList.contains('show')) {
          submenu.classList.remove('show');
        } else {
          showSubmenu();
        }
      };


      // 1. Обробка ховеру (для десктопу)
      item.addEventListener('mouseenter', showSubmenu);
      item.addEventListener('mouseleave', hideSubmenu);


      // 2. ФІКС МОБІЛЬНОГО КОНФЛІКТУ: Керування кліком на <a>

      // А. ФІКС 'TOUCHSTART' для усунення проблеми "подвійного кліка"
      toggleLink.addEventListener('touchstart', (event) => {
        if (isMobile()) {
          event.stopImmediatePropagation();
          event.preventDefault();
          toggleSubmenu(); // Викликаємо toggle одразу
        }
      }, { passive: false });


      // Б. Обробка кліку
      toggleLink.addEventListener('click', (event) => {

        if (isMobile()) {
          // На мобільному клік ігнорується, оскільки ми обробляємо touchstart
          // Але на випадок, якщо touchstart не спрацював, ми повторюємо логіку:
          event.preventDefault();
          event.stopImmediatePropagation();
          toggleSubmenu();
        } else {
          // На десктопі
          event.preventDefault();
          event.stopImmediatePropagation();
        }
      });

      // Блокування спливання для самого сабменю (щоб уникнути закриття меню)
      stopAllPropagation(submenu);


      // 3. ГЛОБАЛЬНИЙ ХАК: Перехоплення кліків на якірні посилання
      document.body.addEventListener('click', (event) => {
        const targetLink = event.target.closest('a');

        if (targetLink && targetLink.closest('.submenu')) {
          const href = targetLink.getAttribute('href');

          if (href && isTargettingCurrentPage(href)) {
            closeAllMenuStates();
            event.preventDefault();
            event.stopImmediatePropagation();

            // Ручна прокрутка (щоб уникнути тригера scroll)
            const targetId = href.split('#')[1];
            const targetElement = document.getElementById(targetId);

            if (targetElement) {
              targetElement.scrollIntoView({ behavior: 'instant' });
            } else if (href.includes('/')) {
              window.location.href = href;
            }
          } else {
            closeAllMenuStates();
          }
        }
      }, true);


      // 4. Обробник для закриття по кліку поза меню
      document.addEventListener('click', (event) => {
        if (!item.contains(event.target)) {
          if (hideTimeout) clearTimeout(hideTimeout);
          submenu.classList.remove('show');
        }
      });
    }
  });
});
document.addEventListener('DOMContentLoaded', function () {
    const triggers = document.querySelectorAll('.accordion-trigger');

    triggers.forEach(trigger => {
        trigger.addEventListener('click', function () {
            const currentSection = this.closest('.accordion-section');
            // Знаходимо саме той акордеон, у якому ми зараз знаходимось
            const parentAccordion = this.closest('.accordion-container');
            const content = currentSection.querySelector('.accordion-content');
            const isActive = currentSection.classList.contains('active');

            // 1. Закриваємо секції ТІЛЬКИ в межах поточного акордеона
            if (parentAccordion) {
                parentAccordion.querySelectorAll('.accordion-section').forEach(section => {
                    section.classList.remove('active');
                    const sectionContent = section.querySelector('.accordion-content');
                    if (sectionContent) {
                        sectionContent.style.maxHeight = null;
                    }
                });
            }

            // 2. Якщо клікнута секція не була активною — відкриваємо її
            if (!isActive) {
                currentSection.classList.add('active');
                content.style.maxHeight = content.scrollHeight + "px";

                setTimeout(() => {
                    const swiperEl = currentSection.querySelector('.swiper');
                    if (swiperEl && swiperEl.swiper) {
                        swiperEl.swiper.update();
                    }
                }, 300);
            }
        });
    });

    // Оновлюємо висоту для всіх дефолтних відкритих секцій на сторінці
    document.querySelectorAll('.accordion-section.active .accordion-content').forEach(activeSection => {
        activeSection.style.maxHeight = activeSection.scrollHeight + "px";
    });
});
/**
 * char-counter.js
 * Chars counter for Contact Form 7.
 */

// Функція для скидання лічильників після успішної відправки форми
document.addEventListener('wpcf7mailsent', function (event) {
  document.querySelectorAll('.count-chars').forEach(function (field) {
    const counterId = field.getAttribute('id') + '-counter';
    const counterElement = document.getElementById(counterId);
    if (counterElement) {
      const maxLength = parseInt(field.getAttribute('maxlength'));
      counterElement.textContent = maxLength;
      counterElement.classList.remove('maxed');
    }
  });
}, false);

// Ініціалізація лічильників після завантаження DOM
document.addEventListener('DOMContentLoaded', function () {
  document.querySelectorAll('.count-chars').forEach(function (field) {
    const maxLength = parseInt(field.getAttribute('maxlength'));
    if (!maxLength) return; // Вихід, якщо немає maxlength

    const counter = document.createElement('span');

    // Генеруємо та встановлюємо ID для поля, якщо його немає, для унікальності лічильника
    const fieldId = field.getAttribute('id') || 'cf7-field-' + Math.random().toString(36).substring(2, 9);
    field.setAttribute('id', fieldId);

    const counterId = fieldId + '-counter';
    counter.setAttribute('id', counterId);
    counter.classList.add('char-counter');

    // Вставляємо лічильник після поля у DOM
    field.parentNode.insertBefore(counter, field.nextSibling);

    function updateCounter() {
      const currentLength = field.value.length;
      const remaining = maxLength - currentLength;

      counter.textContent = remaining;

      if (remaining <= 0) {
        counter.classList.add('maxed');
      } else {
        counter.classList.remove('maxed');
      }
    }

    // Ініціалізація та прив'язка обробників подій
    updateCounter();
    field.addEventListener('input', updateCounter);
    field.addEventListener('propertychange', updateCounter);
    field.addEventListener('keyup', updateCounter);
  });
});

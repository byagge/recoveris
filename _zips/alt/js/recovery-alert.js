/**
 * recovery-alert.js
 * Handler for Contact Form 7
 */
(function () {
  const setupAlertLogic = () => {
    const topicSelect = document.querySelector('select.wpcf7-select');

    const alertDiv = document.getElementById('recovery-alert');

    if (!topicSelect || !alertDiv) {
      return;
    }

    const toggleAlert = () => {
      const currentValue = topicSelect.value ? topicSelect.value.trim() : "";

      if (currentValue === 'Recovery') {
        alertDiv.style.display = 'block';
      } else {
        alertDiv.style.display = 'none';
      }
    };

    topicSelect.addEventListener('change', toggleAlert);
    toggleAlert();
  };

  setupAlertLogic();
})();
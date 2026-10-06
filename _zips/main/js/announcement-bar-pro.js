/**
 * Announcement Bar Pro Features
 *
 * Advanced features for pro version: coupon auto-apply, advanced countdown,
 * A/B testing integration, and analytics tracking.
 */

(function() {
  'use strict';

  /**
   * Initialize pro features
   */
  document.addEventListener('DOMContentLoaded', function() {
    initializeProFeatures();
  });

  /**
   * Main initialization for pro features
   */
  function initializeProFeatures() {
    const bars = document.querySelectorAll('.hashbar-announcement-bar');

    if (bars.length === 0) {
      return;
    }

    bars.forEach(function(bar) {
      const barId = bar.getAttribute('data-bar-id');

      // Initialize coupon auto-apply for WooCommerce
      if (bar.getAttribute('data-coupon-enabled') === 'true') {
        initializeCouponAutoApply(bar, barId);
      }

      // Note: Countdown is already initialized in announcement-bar-frontend.js
      // Do not initialize it here to avoid double intervals

      // Initialize A/B test tracking
      if (bar.getAttribute('data-ab-test-enabled') === 'true') {
        initializeABTestTracking(bar, barId);
      }
    });
  }

  /**
   * Initialize coupon auto-apply for WooCommerce
   */
  function initializeCouponAutoApply(bar, barId) {
    const couponCode = bar.getAttribute('data-coupon-code');
    const couponDisplay = bar.querySelector('.hashbar-coupon-display');

    if (!couponCode || !couponDisplay) {
      return;
    }

    // Check if WooCommerce is active
    if (typeof wc === 'undefined' || !wc.blocksCheckout) {
      // Not using new WooCommerce Blocks, skip auto-apply
      return;
    }

    // Add auto-apply button
    const applyBtn = document.createElement('button');
    applyBtn.className = 'hashbar-coupon-apply-btn';
    applyBtn.textContent = 'Apply';
    applyBtn.style.cssText = 'margin-left: 8px; cursor: pointer; padding: 4px 12px; background: #0073aa; color: white; border: none; border-radius: 3px; font-size: 12px; font-weight: 600;';

    applyBtn.addEventListener('click', function(e) {
      e.preventDefault();
      applyCouponToCart(couponCode, applyBtn);
    });

    couponDisplay.appendChild(applyBtn);
  }

  /**
   * Apply coupon to WooCommerce cart
   */
  function applyCouponToCart(couponCode, button) {
    if (!couponCode || typeof jQuery === 'undefined') {
      return;
    }

    button.disabled = true;
    button.textContent = 'Applying...';

    // Use WooCommerce REST API to apply coupon
    fetch(window.HashbarAnnouncementData.restUrl + 'apply-coupon', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-WP-Nonce': window.HashbarAnnouncementData.nonce,
      },
      body: JSON.stringify({
        coupon_code: couponCode,
      }),
    })
      .then(function(response) {
        return response.json();
      })
      .then(function(data) {
        if (data.success) {
          button.textContent = 'Applied!';
          button.style.background = '#008000';

          // Notify user
          if (typeof wc !== 'undefined' && wc.store && wc.store.dispatch) {
            // Show success notice in new WooCommerce blocks
          }

          setTimeout(function() {
            button.textContent = 'Apply';
            button.style.background = '#0073aa';
            button.disabled = false;
          }, 3000);
        } else {
          button.textContent = 'Error';
          button.style.background = '#dc3545';

          setTimeout(function() {
            button.textContent = 'Apply';
            button.style.background = '#0073aa';
            button.disabled = false;
          }, 3000);
        }
      })
      .catch(function(error) {
        button.textContent = 'Error';
        button.style.background = '#dc3545';
        button.disabled = false;
      });
  }

  /**
   * Update timer display based on style (simple, digital, circular, or box)
   */
  function updateTimerDisplay(timerElement, displayText) {
    const style = timerElement.getAttribute('data-countdown-style') || 'simple';

    if (style === 'simple' || style === 'digital') {
      // Simple and digital styles: update text content directly only if changed
      if (timerElement.textContent !== displayText) {
        timerElement.textContent = displayText;
      }
    } else if (style === 'circular' || style === 'box') {
      // Circular and box styles: update individual countdown-number elements
      // displayText should be in format "1d 2h 3m 4s" or "Expired"
      if (displayText === 'Expired') {
        if (timerElement.textContent !== displayText) {
          timerElement.textContent = displayText;
        }
        return;
      }

      // Parse the display text to extract days, hours, minutes, seconds
      // Format: "1d 2h 3m 4s" or variations like "1d 2h" or "2h 3m 4s"
      const parts = displayText.split(/\s+/);
      const values = {};

      parts.forEach(part => {
        if (part.endsWith('d')) {
          values.days = part.slice(0, -1);
        } else if (part.endsWith('h')) {
          values.hours = part.slice(0, -1);
        } else if (part.endsWith('m')) {
          values.minutes = part.slice(0, -1);
        } else if (part.endsWith('s')) {
          values.seconds = part.slice(0, -1);
        }
      });

      // Update the countdown-number divs in the correct units - only if changed
      const daysUnit = timerElement.querySelector('.hb-countdown-days');
      if (daysUnit) {
        const dayNumber = daysUnit.querySelector('.countdown-number');
        const newDayText = String(values.days || 0).padStart(2, '0');
        if (dayNumber && dayNumber.textContent !== newDayText) {
          dayNumber.textContent = newDayText;
        }
      }

      const hoursUnit = timerElement.querySelector('.hb-countdown-hours');
      if (hoursUnit) {
        const hourNumber = hoursUnit.querySelector('.countdown-number');
        const newHourText = String(values.hours || 0).padStart(2, '0');
        if (hourNumber && hourNumber.textContent !== newHourText) {
          hourNumber.textContent = newHourText;
        }
      }

      const minutesUnit = timerElement.querySelector('.hb-countdown-minutes');
      if (minutesUnit) {
        const minuteNumber = minutesUnit.querySelector('.countdown-number');
        const newMinuteText = String(values.minutes || 0).padStart(2, '0');
        if (minuteNumber && minuteNumber.textContent !== newMinuteText) {
          minuteNumber.textContent = newMinuteText;
        }
      }

      const secondsUnit = timerElement.querySelector('.hb-countdown-seconds');
      if (secondsUnit) {
        const secondNumber = secondsUnit.querySelector('.countdown-number');
        const newSecondText = String(values.seconds || 0).padStart(2, '0');
        if (secondNumber && secondNumber.textContent !== newSecondText) {
          secondNumber.textContent = newSecondText;
        }
      }
    }
  }

  /**
   * Initialize advanced countdown with percentage display
   */
  function initializeAdvancedCountdown(bar, barId) {
    const countdownType = bar.getAttribute('data-countdown-type');
    const countdownDate = bar.getAttribute('data-countdown-date');
    const resetTimeStr = bar.getAttribute('data-countdown-reset-time');
    const resetDaysJson = bar.getAttribute('data-countdown-reset-days');
    const durationHours = bar.getAttribute('data-countdown-duration');
    const timezoneStr = bar.getAttribute('data-countdown-timezone');
    const timerElement = bar.querySelector('.hashbar-countdown-timer-wrapper, .hashbar-countdown-timer-text');

    if (!timerElement) {
      return;
    }


    if (countdownType === 'fixed') {
      if (!countdownDate) return;
      // Calculate remaining time and display in days/hours/minutes/seconds format
      let lastDisplayedText = '';

      function updateIfChanged() {
        const timezoneOffset = getTimezoneOffset(timezoneStr || 'UTC');
        const now = new Date();
        const utcMs = now.getTime();

        // Parse the countdown date
        const endDateParts = countdownDate.split('T')[0].split('-');
        const endYear = parseInt(endDateParts[0], 10);
        const endMonth = parseInt(endDateParts[1], 10) - 1;
        const endDate = parseInt(endDateParts[2], 10);

        const timeParts = countdownDate.split('T')[1] || '00:00:00';
        const [endHours, endMinutes] = timeParts.split(':').map(Number);

        const localOffsetMs = now.getTimezoneOffset() * 60 * 1000;
        const targetOffsetMs = timezoneOffset * 60 * 60 * 1000;

        const endTimeUtc = new Date(Date.UTC(endYear, endMonth, endDate, endHours, endMinutes, 0, 0));
        const endTimeMs = endTimeUtc.getTime();
        const endTimeInTargetTz = endTimeMs + localOffsetMs - targetOffsetMs;

        const remaining = endTimeInTargetTz - utcMs;

        let displayText;
        if (remaining < 0) {
          displayText = 'Expired';
        } else {
          const days = Math.floor(remaining / (1000 * 60 * 60 * 24));
          const hours = Math.floor((remaining % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
          const minutes = Math.floor((remaining % (1000 * 60 * 60)) / (1000 * 60));
          const seconds = Math.floor((remaining % (1000 * 60)) / 1000);
          displayText = days + 'd ' + hours + 'h ' + minutes + 'm ' + seconds + 's';
        }

        if (displayText !== lastDisplayedText) {
          updateTimerDisplay(timerElement, displayText);
          lastDisplayedText = displayText;
        }
      }

      updateIfChanged();
      setInterval(updateIfChanged, 1000);
    } else if (countdownType === 'recurring') {
      // Parse reset days array
      let resetDays = [];
      if (resetDaysJson) {
        try {
          resetDays = JSON.parse(resetDaysJson);
        } catch (e) {
          resetDays = [];
        }
      }

      // Recurring countdown - use resetTimeStr (not countdownDate)
      // resetTimeStr should always be available for recurring type
      const resetTime = resetTimeStr && resetTimeStr !== '' ? resetTimeStr : '00:00';
      let lastDisplayedText = '';
      let lastDisplayState = null;

      function updateIfChangedRecurring() {
        const timerText = getRecurringCountdownText(resetTime, resetDays, timezoneStr);
        if (timerText !== lastDisplayedText) {
          updateTimerDisplay(timerElement, timerText);
          lastDisplayedText = timerText;
        }
        // Update display state separately
        const displayState = shouldShowRecurringCountdown(resetDays);
        if (displayState !== lastDisplayState) {
          timerElement.style.display = displayState ? '' : 'none';
          lastDisplayState = displayState;
        }
      }

      updateIfChangedRecurring();
      setInterval(updateIfChangedRecurring, 1000);
    } else if (countdownType === 'evergreen') {
      // Evergreen countdown - per-visitor personalized timer based on duration
      const duration = parseInt(durationHours, 10) || 24;
      let lastDisplayedText = '';

      function updateIfChangedEvergreen() {
        const timerText = getEvergreenCountdownText(barId, duration);
        if (timerText !== lastDisplayedText) {
          if (timerText === '') {
            timerElement.textContent = '';
            timerElement.style.display = 'none';
          } else {
            timerElement.style.display = '';
            updateTimerDisplay(timerElement, timerText);
          }
          lastDisplayedText = timerText;
        }
      }

      updateIfChangedEvergreen();
      setInterval(updateIfChangedEvergreen, 1000);
    }
  }

  /**
   * Calculate fixed countdown percentage
   */
  function getFixedCountdownPercentage(countdownDate, timezoneStr) {
    // Get timezone offset in hours
    const timezoneOffset = getTimezoneOffset(timezoneStr || 'UTC');
    const now = new Date();
    const utcMs = now.getTime();

    // Parse the countdown date as provided by the input
    // countdownDate is in format "YYYY-MM-DDTHH:MM"
    const endDateParts = countdownDate.split('T')[0].split('-');
    const endYear = parseInt(endDateParts[0], 10);
    const endMonth = parseInt(endDateParts[1], 10) - 1;
    const endDate = parseInt(endDateParts[2], 10);

    // Parse time from countdown date (HH:MM or HH:MM:SS)
    const timeParts = countdownDate.split('T')[1] || '00:00:00';
    const [endHours, endMinutes] = timeParts.split(':').map(Number);

    // Get browser's local offset in milliseconds
    const localOffsetMs = now.getTimezoneOffset() * 60 * 1000;

    // Get target timezone offset in milliseconds
    const targetOffsetMs = timezoneOffset * 60 * 60 * 1000;

    // Create a UTC timestamp representing the input date/time interpreted as the target timezone
    // The datetime-local input gives us a value like "2025-12-31T14:00"
    // This value is interpreted by the browser as being in the browser's local timezone
    // But the user intended it to represent the selected timezone
    //
    // Example: Browser is in EST (UTC-5), user is in CET (UTC+1)
    // User enters "2025-12-31 14:00" intending "14:00 CET"
    // We need to calculate what UTC time corresponds to "14:00 CET"
    // Answer: 13:00 UTC (because CET is +1, so 14:00 CET = 13:00 UTC)
    const endTimeUtc = new Date(Date.UTC(endYear, endMonth, endDate, endHours, endMinutes, 0, 0));
    const endTimeMs = endTimeUtc.getTime();

    // Use the same formula as recurring: adjust for both local and target timezones
    const endTimeInTargetTz = endTimeMs + localOffsetMs - targetOffsetMs;

    // Start date is 7 days before end date
    const startTimeMs = endTimeInTargetTz - (7 * 24 * 60 * 60 * 1000);

    const totalDuration = endTimeInTargetTz - startTimeMs;
    const remaining = endTimeInTargetTz - utcMs;

    // Return percentage (or negative if expired)
    return remaining < 0 ? -1 : Math.round((remaining / totalDuration) * 100);
  }

  /**
   * Update countdown with percentage display and timezone support (initial update only)
   */
  function updatePercentageCountdown(timerElement, countdownDate, timezoneStr) {
    const percentage = getFixedCountdownPercentage(countdownDate, timezoneStr);
    if (percentage < 0) {
      timerElement.textContent = 'Expired';
    } else {
      timerElement.textContent = percentage + '% left';
    }
  }

  /**
   * Check if recurring countdown should be shown based on reset days
   */
  function shouldShowRecurringCountdown(resetDays) {
    if (!Array.isArray(resetDays)) {
      return true; // Show if no day restrictions
    }

    if (resetDays.length === 0) {
      return false; // Hide if no days selected
    }

    // Get timezone-adjusted today's day
    const now = new Date();
    const utcMs = now.getTime();
    const localOffsetMs = now.getTimezoneOffset() * 60 * 1000;
    const targetOffsetMs = 0; // Using UTC for day calculation
    const targetTimeMs = utcMs + (targetOffsetMs - localOffsetMs);
    const targetTime = new Date(targetTimeMs);
    const today = targetTime.getUTCDay();

    return resetDays.includes(today);
  }

  /**
   * Get recurring countdown text without updating DOM
   */
  function getRecurringCountdownText(resetTimeStr, resetDays, timezoneStr) {
    // Check if should show
    if (!shouldShowRecurringCountdown(resetDays)) {
      return ''; // Empty means hidden
    }

    const nowMs = new Date().getTime();
    const nextOccurrence = getNextRecurringDate(resetTimeStr, timezoneStr);
    const distance = nextOccurrence - nowMs;

    if (distance < 0) {
      return 'Expired';
    }

    const days = Math.floor(distance / (1000 * 60 * 60 * 24));
    const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
    const seconds = Math.floor((distance % (1000 * 60)) / 1000);

    return days + 'd ' + hours + 'h ' + minutes + 'm ' + seconds + 's';
  }

  /**
   * Get next recurring countdown date based on reset time with timezone support
   */
  function getNextRecurringDate(resetTimeStr, timezoneStr) {
    // Get timezone offset in hours
    const timezoneOffset = getTimezoneOffset(timezoneStr || 'UTC');
    const now = new Date();

    // Get current UTC time
    const utcMs = now.getTime();

    // Convert UTC to target timezone time (in milliseconds)
    // targetTimeMs is a millisecond value that represents what time it is in the target timezone
    const targetOffsetMs = timezoneOffset * 60 * 60 * 1000;
    const targetTimeMs = utcMs + targetOffsetMs;

    // Parse reset time (HH:MM format)
    const [resetHours, resetMinutes] = (resetTimeStr || '00:00').split(':').map(Number);

    // Get today's date/time in target timezone
    // We need to extract year/month/date from the target timezone, not UTC
    const targetTime = new Date(targetTimeMs);
    const year = targetTime.getUTCFullYear();
    const month = targetTime.getUTCMonth();
    const date = targetTime.getUTCDate();

    // Create a UTC timestamp for "today at reset time in the target timezone"
    // If timezone is UTC+1 and reset time is 14:00:
    //   UTC 14:00 in +1 timezone is actually 13:00 UTC
    //   So we create Date.UTC(year, month, date, 14, 0) then subtract 1 hour
    const resetTimeUtc = new Date(Date.UTC(year, month, date, resetHours, resetMinutes, 0, 0));
    const resetTimeMs = resetTimeUtc.getTime() - targetOffsetMs;

    // If reset time has already passed today, use tomorrow's reset time
    if (resetTimeMs <= utcMs) {
      const tomorrow = new Date(Date.UTC(year, month, date + 1, resetHours, resetMinutes, 0, 0));
      const tomorrowResetMs = tomorrow.getTime() - targetOffsetMs;
      return tomorrowResetMs;
    }

    return resetTimeMs;
  }

  /**
   * Get timezone offset in hours from timezone abbreviation
   */
  function getTimezoneOffset(timezone) {
    // Handle new simplified timezone options
    if (timezone === 'site') {
      // Use the site timezone offset passed from PHP
      return typeof HashbarAnnouncementData !== 'undefined' && HashbarAnnouncementData.siteTimezoneOffset !== undefined
        ? parseFloat(HashbarAnnouncementData.siteTimezoneOffset)
        : 0;
    }

    if (timezone === 'visitor') {
      // Use visitor's local timezone (browser timezone)
      // getTimezoneOffset() returns minutes with reversed sign, so we negate and convert to hours
      return -(new Date().getTimezoneOffset() / 60);
    }

    // Legacy timezone abbreviations (for backward compatibility)
    const timezoneMap = {
      // UTC & GMT
      'UTC': 0,
      'GMT': 0,

      // North America
      'EST': -5,
      'EDT': -4,
      'CST': -6,
      'CDT': -5,
      'MST': -7,
      'MDT': -6,
      'PST': -8,
      'PDT': -7,
      'AKST': -9,
      'AKDT': -8,
      'HST': -10,
      'HADT': -9,

      // Europe
      'CET': 1,
      'CEST': 2,
      'EET': 2,
      'EEST': 3,
      'WET': 0,
      'WEST': 1,

      // Asia
      'IST': 5.5,
      'IDT': 6.5,
      'JST': 9,
      'HKT': 8,
      'MYT': 8,
      'PHT': 8,
      'KST': 9,
      'WITA': 8,
      'WIB': 7,
      'ICT': 7,
      'BDT': 6,
      'PKT': 5,

      // Middle East & Africa
      'GST': 4,
      'EAT': 3,
      'CAT': 2,
      'WAT': 1,
      'SAST': 2,

      // Oceania
      'AEST': 10,
      'AEDT': 11,
      'ACST': 9.5,
      'ACDT': 10.5,
      'AWST': 8,
      'NZST': 12,
      'NZDT': 13,

      // South America
      'ART': -3,
      'BRT': -3,
      'VET': -4,
      'CLT': -3,
      'PET': -5,
    };

    return timezoneMap[timezone] !== undefined ? timezoneMap[timezone] : 0;
  }

  /**
   * Get evergreen countdown text without updating DOM
   */
  function getEvergreenCountdownText(barId, durationHours) {
    const storageKey = 'hashbar_evergreen_start_' + barId;
    const now = new Date();
    const utcMs = now.getTime();
    let startTime;

    // Try to use localStorage if available (real frontend)
    try {
      startTime = localStorage.getItem(storageKey);
      if (!startTime) {
        startTime = utcMs;
        localStorage.setItem(storageKey, startTime);
      } else {
        startTime = parseInt(startTime, 10);
      }
    } catch (e) {
      // localStorage not available (admin preview) - use demo timer
      // Show 1/3 of the duration as demo
      startTime = utcMs - (durationHours * 60 * 60 * 1000 * 0.666);
    }

    // Calculate deadline (start time + duration in hours)
    const durationMs = durationHours * 60 * 60 * 1000;
    const deadline = startTime + durationMs;
    const distance = deadline - utcMs;

    // If countdown has expired, clear localStorage and return empty
    if (distance <= 0) {
      try {
        localStorage.removeItem(storageKey);
      } catch (e) {
        // Ignore errors when trying to remove from localStorage
      }
      return ''; // Empty means hidden
    }

    // Calculate time units
    const days = Math.floor(distance / (1000 * 60 * 60 * 24));
    const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
    const seconds = Math.floor((distance % (1000 * 60)) / 1000);

    return days + 'd ' + hours + 'h ' + minutes + 'm ' + seconds + 's';
  }

  /**
   * Initialize A/B test tracking with analytics
   */
  function initializeABTestTracking(bar, barId) {
    const variantCookieName = 'hashbar_ab_variant_' + barId;
    let variant = getCookie(variantCookieName);

    if (!variant) {
      // Get A/B test variants from data attribute or fetch from API
      fetchABTestVariants(barId, function(variants) {
        if (variants && variants.length > 0) {
          // Weighted random selection based on traffic split
          variant = selectWeightedVariant(variants);
          setCookie(variantCookieName, variant, 30);
          trackABTestEvent('view', barId, variant);
        }
      });
    } else {
      trackABTestEvent('view', barId, variant);
    }

    // Track interaction events
    bar.addEventListener('click', function() {
      if (variant) {
        trackABTestEvent('click', barId, variant);
      }
    });

    // Track close events
    const closeButtons = bar.querySelectorAll('.hashbar-announcement-close');
    closeButtons.forEach(function(button) {
      button.addEventListener('click', function() {
        if (variant) {
          trackABTestEvent('close', barId, variant);
        }
      });
    });

    // Track CTA click
    const ctaButton = bar.querySelector('.hashbar-announcement-cta');
    if (ctaButton) {
      ctaButton.addEventListener('click', function() {
        if (variant) {
          trackABTestEvent('cta_click', barId, variant);
        }
      });
    }
  }

  /**
   * Fetch A/B test variants from API
   * NOTE: This endpoint is deprecated. A/B testing is now handled by the main
   * announcement-bar-frontend.js using the data-messages attribute from PHP backend.
   * This function is kept for backwards compatibility but doesn't do anything.
   */
  function fetchABTestVariants(barId, callback) {
    // A/B testing variants are now provided via data-messages attribute
    // No need to fetch from API anymore
    return;
  }

  /**
   * Select weighted random variant
   */
  function selectWeightedVariant(variants) {
    const random = Math.random() * 100;
    let accumulated = 0;

    for (let i = 0; i < variants.length; i++) {
      accumulated += variants[i].traffic;

      if (random <= accumulated) {
        return variants[i].id;
      }
    }

    return variants[0].id;
  }

  /**
   * Track A/B test event
   */
  function trackABTestEvent(eventType, barId, variant) {
    if (!window.HashbarAnnouncementData) {
      return;
    }

    // Track in Google Analytics if available
    if (typeof gtag !== 'undefined') {
      gtag('event', 'announcement_bar_' + eventType, {
        'bar_id': barId,
        'variant': variant,
        'event_category': 'announcement_bar',
        'event_label': eventType,
      });
    }

    // Send to custom analytics endpoint
    fetch(window.HashbarAnnouncementData.restUrl + 'announcement-bars/' + barId + '/track', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-WP-Nonce': window.HashbarAnnouncementData.nonce,
      },
      body: JSON.stringify({
        event: eventType,
        variant: variant,
        timestamp: new Date().toISOString(),
      }),
    }).catch(function(error) {
      // Silently fail, don't disrupt user experience
    });
  }

  /**
   * Cookie utilities
   */
  function setCookie(name, value, days) {
    let expires = '';

    if (days) {
      const date = new Date();
      date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
      expires = '; expires=' + date.toUTCString();
    }

    document.cookie = name + '=' + (value || '') + expires + '; path=/';
  }

  function getCookie(name) {
    const nameEQ = name + '=';
    const cookies = document.cookie.split(';');

    for (let i = 0; i < cookies.length; i++) {
      let cookie = cookies[i].trim();

      if (cookie.indexOf(nameEQ) === 0) {
        return cookie.substring(nameEQ.length);
      }
    }

    return null;
  }

})();

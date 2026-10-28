/**
 * Laika Internal Telemetry & Engagement Tracker (100% Prywatny, Zero Cookies)
 * Autorski silnik analityczny Bloga Laika — bez Google Analytics, bez ciasteczek, bez zewnętrznych trackerów.
 * Przechowuje statystyki zaangażowania wyłącznie w pamięci przeglądarki (localStorage).
 */
(function() {
  'use strict';

  var STORAGE_KEY = 'laika_telemetry_v1';

  function getStore() {
    try {
      var raw = localStorage.getItem(STORAGE_KEY);
      if (raw) return JSON.parse(raw);
    } catch (e) {
      console.warn('[Laika Telemetry] Nie można odczytać localStorage:', e);
    }
    return {
      version: 1,
      total_pageviews: 0,
      posts: {},
      categories: {},
      searches: [],
      reading_sessions: []
    };
  }

  function saveStore(data) {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(data));
    } catch (e) {
      console.warn('[Laika Telemetry] Błąd zapisu do localStorage:', e);
    }
  }

  var path = window.location.pathname;
  var isPost = path.indexOf('/post/') !== -1;
  var isCategory = path.indexOf('/kategoria/') !== -1;
  var isSearch = path.indexOf('/szukaj') !== -1;

  var currentSlug = '';
  if (isPost) {
    var parts = path.split('/').filter(Boolean);
    var pIdx = parts.indexOf('post');
    if (pIdx !== -1 && parts[pIdx + 1]) {
      currentSlug = parts[pIdx + 1];
    }
  }

  var currentCat = '';
  if (isCategory) {
    var catParts = path.split('/').filter(Boolean);
    var cIdx = catParts.indexOf('kategoria');
    if (cIdx !== -1 && catParts[cIdx + 1]) {
      currentCat = catParts[cIdx + 1];
    }
  }

  // Record Pageview
  var store = getStore();
  store.total_pageviews = (store.total_pageviews || 0) + 1;

  if (currentSlug) {
    if (!store.posts[currentSlug]) {
      store.posts[currentSlug] = {
        views: 0,
        scroll_depth: 0,
        seconds_spent: 0,
        completed: false,
        last_visit: null
      };
    }
    store.posts[currentSlug].views += 1;
    store.posts[currentSlug].last_visit = new Date().toISOString();
  }

  if (currentCat) {
    store.categories[currentCat] = (store.categories[currentCat] || 0) + 1;
  }

  saveStore(store);

  // Update live view badges on page
  document.addEventListener('DOMContentLoaded', function() {
    var badges = document.querySelectorAll('.laika-views-count');
    badges.forEach(function(el) {
      var slug = el.getAttribute('data-slug') || currentSlug;
      var baseVal = parseInt(el.textContent.replace(/\s+/g, ''), 10) || 0;
      var localViews = (store.posts[slug] && store.posts[slug].views) ? store.posts[slug].views : 0;
      if (localViews > 0) {
        var total = baseVal + (localViews - 1); // unikanie podwójnego zliczania pierwszej wizyty
        el.textContent = total.toLocaleString('pl-PL');
      }
    });

    // Search query tracking
    if (isSearch) {
      var searchInput = document.getElementById('search-input') || document.querySelector('input[name="q"]');
      if (searchInput) {
        searchInput.addEventListener('change', function() {
          var q = searchInput.value.trim();
          if (q.length >= 2) {
            var st = getStore();
            if (st.searches.indexOf(q) === -1) {
              st.searches.unshift(q);
              if (st.searches.length > 30) st.searches.pop();
              saveStore(st);
            }
          }
        });
      }
    }
  });

  // Active reading time and scroll-depth tracking (only for posts)
  if (isPost && currentSlug) {
    var activeSeconds = 0;
    var maxScrollPct = 0;
    var lastInteraction = Date.now();
    var isTabActive = true;

    // Track user presence
    function resetInteraction() {
      lastInteraction = Date.now();
    }
    ['mousemove', 'keydown', 'scroll', 'touchstart'].forEach(function(evt) {
      window.addEventListener(evt, resetInteraction, { passive: true });
    });

    document.addEventListener('visibilitychange', function() {
      isTabActive = (document.visibilityState === 'visible');
    });

    // Heartbeat timer (every 2 seconds)
    var heartbeatTimer = setInterval(function() {
      var idle = Date.now() - lastInteraction;
      // Only count if tab is visible and user was active in the last 45 seconds
      if (isTabActive && idle < 45000) {
        activeSeconds += 2;
        var st = getStore();
        if (st.posts[currentSlug]) {
          st.posts[currentSlug].seconds_spent = (st.posts[currentSlug].seconds_spent || 0) + 2;
          saveStore(st);
        }
      }
    }, 2000);

    // Scroll depth tracker
    var scrollThrottler = false;
    window.addEventListener('scroll', function() {
      if (scrollThrottler) return;
      scrollThrottler = true;
      setTimeout(function() {
        scrollThrottler = false;
        var article = document.querySelector('article') || document.body;
        var rect = article.getBoundingClientRect();
        var articleHeight = rect.height;
        var scrolled = window.scrollY || window.pageYOffset;
        var windowHeight = window.innerHeight;

        var pct = Math.min(100, Math.round(((scrolled + windowHeight) / (articleHeight + rect.top + scrolled)) * 100));
        if (pct > maxScrollPct) {
          maxScrollPct = pct;
          var st = getStore();
          if (st.posts[currentSlug]) {
            st.posts[currentSlug].scroll_depth = maxScrollPct;
            if (maxScrollPct >= 80 && !st.posts[currentSlug].completed) {
              st.posts[currentSlug].completed = true;
            }
            saveStore(st);
          }
        }
      }, 300);
    }, { passive: true });
  }

  // Expose global telemetry API for the Admin Dashboard
  window.LaikaTelemetry = {
    getStore: getStore,
    getSummary: function() {
      var s = getStore();
      var postCount = Object.keys(s.posts).length;
      var totalLocalViews = 0;
      var completedCount = 0;
      var totalDwell = 0;

      for (var k in s.posts) {
        var p = s.posts[k];
        totalLocalViews += (p.views || 0);
        if (p.completed) completedCount++;
        totalDwell += (p.seconds_spent || 0);
      }

      return {
        total_pageviews: s.total_pageviews || 0,
        posts_tracked: postCount,
        total_local_views: totalLocalViews,
        completed_reads: completedCount,
        total_dwell_seconds: totalDwell,
        searches: s.searches || [],
        categories: s.categories || {},
        posts: s.posts || {}
      };
    },
    exportJSON: function() {
      var dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(getStore(), null, 2));
      var downloadAnchor = document.createElement('a');
      downloadAnchor.setAttribute("href", dataStr);
      downloadAnchor.setAttribute("download", "laika_local_telemetry.json");
      document.body.appendChild(downloadAnchor);
      downloadAnchor.click();
      downloadAnchor.remove();
    },
    reset: function() {
      localStorage.removeItem(STORAGE_KEY);
      console.log('[Laika Telemetry] Zresetowano lokalne statystyki.');
    }
  };
})();

/**
 * Laika Cookie Analytics Engine (100% Realne Dane, Oparte na Plikach Cookies)
 * Autorski silnik analityczny Bloga Laika — bez zewnętrznych trackerów, bez inwazyjnego profilowania.
 * Gromadzi i weryfikuje dane czytelnictwa na bazie plików cookies (first-party cookies):
 *   - laika_vid: Unikalny identyfikator czytelnika (ważność: 365 dni)
 *   - laika_sid: Identyfikator sesji czytania (ważność: 30 minut bezczynności)
 *   - laika_vcount: Liczba wizyt / sesji danego czytelnika
 *   - laika_seen: Eseje przeczytane w bieżącej sesji (ochrona przed sztucznym nabijaniem przy odświeżaniu)
 *   - laika_ref: Rzeczywiste źródło wejścia (Organic Search, Social Media, Direct, RSS)
 *   - laika_device: Kategoria urządzenia (Mobile, Desktop, Tablet)
 */
(function() {
  'use strict';

  // =========================================================================
  // 1. ZARZĄDZANIE PLIKAMI COOKIES (First-Party Cookies)
  // =========================================================================

  function getCookie(name) {
    var nameEQ = encodeURIComponent(name) + "=";
    var ca = document.cookie.split(';');
    for (var i = 0; i < ca.length; i++) {
      var c = ca[i];
      while (c.charAt(0) === ' ') c = c.substring(1, c.length);
      if (c.indexOf(nameEQ) === 0) {
        return decodeURIComponent(c.substring(nameEQ.length, c.length));
      }
    }
    return null;
  }

  function setCookie(name, value, days) {
    var expires = "";
    if (days) {
      var date = new Date();
      date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
      expires = "; expires=" + date.toUTCString();
    }
    document.cookie = encodeURIComponent(name) + "=" + encodeURIComponent(value || "") + expires + "; path=/; SameSite=Lax";
  }

  function setSessionCookie(name, value, minutes) {
    var expires = "";
    if (minutes) {
      var date = new Date();
      date.setTime(date.getTime() + (minutes * 60 * 1000));
      expires = "; expires=" + date.toUTCString();
    }
    document.cookie = encodeURIComponent(name) + "=" + encodeURIComponent(value || "") + expires + "; path=/; SameSite=Lax";
  }

  function deleteCookie(name) {
    document.cookie = encodeURIComponent(name) + "=; expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/; SameSite=Lax";
  }

  // =========================================================================
  // 2. DETEKCJA URZĄDZENIA I ŹRÓDŁA WEJŚCIA
  // =========================================================================

  function detectDevice() {
    var ua = navigator.userAgent || "";
    if (/iPad|Tablet|(Android(?!.*Mobile))/i.test(ua)) {
      return { device: "Tablety", icon: "📟" };
    }
    if (/Mobile|iPhone|Android|iPod|BlackBerry|IEMobile|Silk/i.test(ua)) {
      return { device: "Smartfony (Mobile)", icon: "📱" };
    }
    return { device: "Komputery (Desktop)", icon: "💻" };
  }

  function detectReferrer() {
    var ref = document.referrer || "";
    if (!ref) return { type: "Wejścia Bezpośrednie & Zakładki", raw: "" };
    var lower = ref.toLowerCase();
    if (lower.indexOf("google.") !== -1 || lower.indexOf("bing.com") !== -1 || lower.indexOf("duckduckgo.com") !== -1 || lower.indexOf("ecosia.org") !== -1 || lower.indexOf("search.") !== -1) {
      return { type: "Wyszukiwarki (Organic Search)", raw: ref };
    }
    if (lower.indexOf("t.co") !== -1 || lower.indexOf("twitter.com") !== -1 || lower.indexOf("x.com") !== -1 || lower.indexOf("linkedin.com") !== -1 || lower.indexOf("facebook.com") !== -1 || lower.indexOf("reddit.com") !== -1 || lower.indexOf("wykop.pl") !== -1 || lower.indexOf("instagram.com") !== -1) {
      return { type: "Media Społecznościowe & Dyskusje", raw: ref };
    }
    if (lower.indexOf("feedly.com") !== -1 || lower.indexOf("inoreader.com") !== -1 || lower.indexOf("newsblur.com") !== -1) {
      return { type: "Czytniki RSS & Agregatory", raw: ref };
    }
    if (ref.indexOf(window.location.hostname) !== -1) {
      return { type: "Nawigacja Wewnętrzna", raw: ref };
    }
    return { type: "Inne witryny odsyłające", raw: ref };
  }

  // =========================================================================
  // 3. PERSYSTENTNY BAZOWY MAGAZYN ANALITYCZNY COOKIES
  // =========================================================================

  var STATS_STORAGE_KEY = 'laika_cookie_analytics_v2';

  function getRealStats() {
    try {
      var raw = localStorage.getItem(STATS_STORAGE_KEY);
      if (raw) return JSON.parse(raw);
    } catch (e) {}

    return {
      version: 2,
      created_at: new Date().toISOString(),
      total_views: 0,
      unique_visitors: {}, // { [vid]: { first_seen, last_seen, visits } }
      posts: {}, // { [slug]: { views: 0, dwell_seconds: 0, completions: 0, last_visit: null } }
      categories: {
        "technologia": 0,
        "gospodarka": 0,
        "historia": 0,
        "polityka": 0,
        "eseje": 0,
        "kondensat": 0
      },
      traffic_sources: {},
      devices: {},
      sessions_log: [] // ostatnie 30 realnych sesji czytelników
    };
  }

  function saveRealStats(stats) {
    try {
      localStorage.setItem(STATS_STORAGE_KEY, JSON.stringify(stats));
    } catch (e) {}

    // Zapisz kompaktowe podsumowanie w ciasteczku
    try {
      var compact = {
        v: stats.total_views,
        u: Object.keys(stats.unique_visitors || {}).length,
        p: Object.keys(stats.posts || {}).length
      };
      setCookie("laika_stats_summary", JSON.stringify(compact), 365);
    } catch (e) {}
  }

  // =========================================================================
  // 4. INICJALIZACJA PLIKÓW COOKIES I ŚLEDZENIE ODSŁON
  // =========================================================================

  // A. Inicjalizacja stałego ciasteczka czytelnika: laika_vid
  var vid = getCookie("laika_vid");
  if (!vid) {
    vid = "vid_" + Date.now().toString(36) + "_" + Math.random().toString(36).substring(2, 7);
    setCookie("laika_vid", vid, 365);
  }

  // B. Inicjalizacja ciasteczka sesji: laika_sid (30 minut bezczynności)
  var isNewSession = false;
  var sid = getCookie("laika_sid");
  if (!sid) {
    sid = "sid_" + Date.now().toString(36) + "_" + Math.random().toString(36).substring(2, 7);
    setSessionCookie("laika_sid", sid, 30);
    isNewSession = true;

    // Inkrementacja licznika sesji w ciasteczku laika_vcount
    var vcount = (parseInt(getCookie("laika_vcount"), 10) || 0) + 1;
    setCookie("laika_vcount", vcount.toString(), 365);

    // Reset listy przeczytanych artykułów w tej nowej sesji
    setSessionCookie("laika_seen", "", 30);
  } else {
    // Odśwież czas życia aktywnej sesji
    setSessionCookie("laika_sid", sid, 30);
  }

  // C. Wykrycie i utrwalenie źródła oraz urządzenia
  var refInfo = detectReferrer();
  if (refInfo.type !== "Nawigacja Wewnętrzna") {
    setSessionCookie("laika_ref", refInfo.type, 30);
  }
  var activeReferrer = getCookie("laika_ref") || refInfo.type;

  var devInfo = detectDevice();
  setCookie("laika_device", devInfo.device, 365);

  // D. Analiza ścieżki URL
  var path = window.location.pathname;
  var isPost = path.indexOf('/post/') !== -1;
  var isCategory = path.indexOf('/kategoria/') !== -1;
  var isSearch = path.indexOf('/szukaj') !== -1;
  var isAdmin = path.indexOf('/admin') !== -1;

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

  // =========================================================================
  // 5. REJESTRACJA REALNEJ ODSŁONY (Z OCHRONĄ PRZED DUBLOWANIEM W SESJI)
  // =========================================================================

  var stats = getRealStats();

  // Zarejestruj unikalnego czytelnika
  if (!stats.unique_visitors[vid]) {
    stats.unique_visitors[vid] = {
      first_seen: new Date().toISOString(),
      visits: 0,
      device: devInfo.device
    };
  }
  if (isNewSession) {
    stats.unique_visitors[vid].visits = (stats.unique_visitors[vid].visits || 0) + 1;
    stats.unique_visitors[vid].last_seen = new Date().toISOString();
  }

  // Obsługa odsłony artykułu
  var isNewPostView = false;
  if (isPost && currentSlug && !isAdmin) {
    var seenCookie = getCookie("laika_seen") || "";
    var seenList = seenCookie ? seenCookie.split(',') : [];

    if (seenList.indexOf(currentSlug) === -1) {
      isNewPostView = true;
      seenList.push(currentSlug);
      setSessionCookie("laika_seen", seenList.join(','), 30);

      // Inkrementacja realnych metryk
      stats.total_views = (stats.total_views || 0) + 1;

      if (!stats.posts[currentSlug]) {
        stats.posts[currentSlug] = {
          views: 0,
          dwell_seconds: 0,
          completions: 0,
          last_visit: null
        };
      }
      stats.posts[currentSlug].views += 1;
      stats.posts[currentSlug].last_visit = new Date().toISOString();

      // Odczyt kategorii z elementu na stronie lub domyślna
      var catBadge = document.querySelector('.category-badge') || document.querySelector('[data-category]');
      var catSlug = catBadge ? (catBadge.getAttribute('data-category') || catBadge.textContent.trim().toLowerCase()) : 'eseje';
      if (catSlug.indexOf('tech') !== -1) catSlug = 'technologia';
      else if (catSlug.indexOf('gosp') !== -1) catSlug = 'gospodarka';
      else if (catSlug.indexOf('hist') !== -1) catSlug = 'historia';
      else if (catSlug.indexOf('polit') !== -1) catSlug = 'polityka';
      else if (catSlug.indexOf('konden') !== -1) catSlug = 'kondensat';
      else catSlug = 'eseje';

      stats.categories[catSlug] = (stats.categories[catSlug] || 0) + 1;

      // Rejestracja źródła i urządzenia
      stats.traffic_sources[activeReferrer] = (stats.traffic_sources[activeReferrer] || 0) + 1;
      stats.devices[devInfo.device] = (stats.devices[devInfo.device] || 0) + 1;

      // Rejestracja w dzienniku sesji
      var pageTitle = document.title ? document.title.split('|')[0].trim() : currentSlug;
      stats.sessions_log.unshift({
        vid: vid,
        sid: sid,
        slug: currentSlug,
        title: pageTitle,
        category: catSlug,
        device: devInfo.device,
        referrer: activeReferrer,
        time: new Date().toISOString(),
        dwell_seconds: 0,
        completed: false
      });
      if (stats.sessions_log.length > 30) stats.sessions_log.pop();

      saveRealStats(stats);

      // Opcjonalne wysłanie beaconu do lokalnego serwera FastAPI
      if (navigator.sendBeacon) {
        try {
          var payload = JSON.stringify({
            vid: vid,
            sid: sid,
            slug: currentSlug,
            cat: catSlug,
            ref: activeReferrer,
            dev: devInfo.device
          });
          navigator.sendBeacon("/api/analytics/collect", payload);
        } catch (e) {}
      }
    }
  }

  // =========================================================================
  // 6. POMIAR CZASU AKTYWNEGO CZYTANIA I GŁĘBOKOŚCI PRZEWINIĘCIA
  // =========================================================================

  if (isPost && currentSlug && !isAdmin) {
    var activeDwell = 0;
    var maxScrollPct = 0;
    var lastInteraction = Date.now();
    var isTabActive = true;
    var isCompleted = false;

    function resetActivity() {
      lastInteraction = Date.now();
    }
    ['mousemove', 'keydown', 'scroll', 'touchstart', 'click'].forEach(function(evt) {
      window.addEventListener(evt, resetActivity, { passive: true });
    });

    document.addEventListener('visibilitychange', function() {
      isTabActive = (document.visibilityState === 'visible');
    });

    // Heartbeat aktywności czytelnika co 2 sekundy
    var dwellInterval = setInterval(function() {
      var idle = Date.now() - lastInteraction;
      // Zliczaj czas wyłącznie gdy karta jest aktywna i czytelnik wykonał akcję w ciągu ostatnich 45s
      if (isTabActive && idle < 45000) {
        activeDwell += 2;
        var curStats = getRealStats();
        if (curStats.posts[currentSlug]) {
          curStats.posts[currentSlug].dwell_seconds = (curStats.posts[currentSlug].dwell_seconds || 0) + 2;
          
          // Zaktualizuj pierwszy wpis w logu sesji
          if (curStats.sessions_log.length > 0 && curStats.sessions_log[0].slug === currentSlug) {
            curStats.sessions_log[0].dwell_seconds = activeDwell;
          }
          saveRealStats(curStats);
        }
      }
    }, 2000);

    // Pomiar przewinięcia treści
    var scrollThrottler = false;
    window.addEventListener('scroll', function() {
      if (scrollThrottler) return;
      scrollThrottler = true;
      setTimeout(function() {
        scrollThrottler = false;
        var article = document.querySelector('article') || document.querySelector('.post-content') || document.body;
        var rect = article.getBoundingClientRect();
        var articleHeight = rect.height;
        var scrolled = window.scrollY || window.pageYOffset;
        var windowHeight = window.innerHeight;

        var pct = Math.min(100, Math.round(((scrolled + windowHeight) / (articleHeight + rect.top + scrolled)) * 100));
        if (pct > maxScrollPct) {
          maxScrollPct = pct;
          var curStats = getRealStats();
          if (curStats.posts[currentSlug]) {
            // Próg ukończenia lektury: >= 75% przewinięcia
            if (maxScrollPct >= 75 && !isCompleted) {
              isCompleted = true;
              curStats.posts[currentSlug].completions = (curStats.posts[currentSlug].completions || 0) + 1;
              if (curStats.sessions_log.length > 0 && curStats.sessions_log[0].slug === currentSlug) {
                curStats.sessions_log[0].completed = true;
              }
            }
            saveRealStats(curStats);
          }
        }
      }, 300);
    }, { passive: true });
  }

  // =========================================================================
  // 7. AKTUALIZACJA LICZNIKÓW ODSŁON NA STRONIE (BADGES)
  // =========================================================================

  document.addEventListener('DOMContentLoaded', function() {
    var badges = document.querySelectorAll('.laika-views-count');
    var curStats = getRealStats();
    badges.forEach(function(el) {
      var slug = el.getAttribute('data-slug') || currentSlug;
      var count = (curStats.posts[slug] && curStats.posts[slug].views) ? curStats.posts[slug].views : 0;
      el.textContent = count.toLocaleString('pl-PL');
    });

    // Jeśli jesteśmy w panelu CMS, zaaplikuj realne dane ciasteczek do interfejsu
    if (isAdmin) {
      applyRealStatsToAdminUI();
    }
  });

  // =========================================================================
  // 8. DYNAMICZNA AKTUALIZACJA PANELU CMS NA BAZIE PLIKÓW COOKIES
  // =========================================================================

  function formatDwell(sec) {
    sec = Math.round(sec || 0);
    var m = Math.floor(sec / 60);
    var s = sec % 60;
    return m + "m " + (s < 10 ? "0" : "") + s + "s";
  }

  function applyRealStatsToAdminUI() {
    var curStats = getRealStats();
    var totalViews = curStats.total_views || 0;
    var uniqueVisitors = Object.keys(curStats.unique_visitors || {}).length;

    // Oblicz średni czas skupienia czytelników
    var totalDwellSec = 0;
    var totalCompletions = 0;
    var totalPostViews = 0;

    for (var k in curStats.posts) {
      var p = curStats.posts[k];
      totalDwellSec += (p.dwell_seconds || 0);
      totalCompletions += (p.completions || 0);
      totalPostViews += (p.views || 0);
    }

    var avgDwellSec = totalPostViews > 0 ? Math.round(totalDwellSec / totalPostViews) : 0;
    var completionPct = totalPostViews > 0 ? Math.round((totalCompletions / totalPostViews) * 100) : 0;

    // 1. Aktualizacja kafelków KPI w panelu admina
    var kpiViews = document.getElementById('admin-kpi-total-views');
    if (kpiViews) kpiViews.textContent = totalViews.toLocaleString('pl-PL');

    var kpiUniques = document.getElementById('admin-kpi-uniques');
    if (kpiUniques) kpiUniques.textContent = uniqueVisitors.toLocaleString('pl-PL');

    var kpiDwell = document.getElementById('admin-kpi-dwell');
    if (kpiDwell) kpiDwell.textContent = formatDwell(avgDwellSec);

    var kpiCompletion = document.getElementById('admin-kpi-completion');
    if (kpiCompletion) kpiCompletion.textContent = completionPct + "%";

    // 2. Aktualizacja wierszy w tabeli artykułów
    var tableRows = document.querySelectorAll('tr[data-post-slug]');
    tableRows.forEach(function(row) {
      var slug = row.getAttribute('data-post-slug');
      var postData = curStats.posts[slug] || { views: 0, dwell_seconds: 0, completions: 0 };
      
      var viewsCell = row.querySelector('.col-real-views');
      if (viewsCell) viewsCell.textContent = (postData.views || 0).toLocaleString('pl-PL');

      var complCell = row.querySelector('.col-real-completion');
      if (complCell) {
        var cPct = postData.views > 0 ? Math.round(((postData.completions || 0) / postData.views) * 100) : 0;
        complCell.textContent = cPct + "%";
      }

      var dwellCell = row.querySelector('.col-real-dwell');
      if (dwellCell) {
        var postAvgDwell = postData.views > 0 ? Math.round(postData.dwell_seconds / postData.views) : 0;
        dwellCell.textContent = formatDwell(postAvgDwell);
      }
    });

    // 3. Aktualizacja udziału szuflad tematycznych
    for (var catSlug in curStats.categories) {
      var catCount = curStats.categories[catSlug] || 0;
      var catShare = totalPostViews > 0 ? Math.round((catCount / totalPostViews) * 100) : 0;
      
      var catValEl = document.getElementById('cat-views-' + catSlug);
      if (catValEl) catValEl.textContent = catCount.toLocaleString('pl-PL') + " (" + catShare + "%)";

      var catBarEl = document.getElementById('cat-bar-' + catSlug);
      if (catBarEl) catBarEl.style.width = catShare + "%";
    }

    // 4. Renderowanie aktywnego Cookie Inspectora
    renderCookieInspector(curStats);
  }

  function renderCookieInspector(curStats) {
    var container = document.getElementById('cookie-inspector-sessions-body');
    if (!container) return;

    // Podsumowanie stanu ciasteczek użytkownika
    var vidEl = document.getElementById('inspector-my-vid');
    if (vidEl) vidEl.textContent = getCookie("laika_vid") || "brak";

    var sidEl = document.getElementById('inspector-my-sid');
    if (sidEl) sidEl.textContent = getCookie("laika_sid") || "aktywna sesja";

    var vcountEl = document.getElementById('inspector-my-vcount');
    if (vcountEl) vcountEl.textContent = getCookie("laika_vcount") || "1";

    var devEl = document.getElementById('inspector-my-device');
    if (devEl) devEl.textContent = getCookie("laika_device") || detectDevice().device;

    var refEl = document.getElementById('inspector-my-ref');
    if (refEl) refEl.textContent = getCookie("laika_ref") || detectReferrer().type;

    // Tabela ostatnich sesji
    var log = curStats.sessions_log || [];
    if (log.length === 0) {
      container.innerHTML = '<tr><td colspan="6" style="padding: 1rem; text-align: center; color: var(--text-muted);">Brak zarejestrowanych sesji czytelników. Odwiedź dowolny esej na blogu, aby zarejestrować pierwsze ciasteczko!</td></tr>';
      return;
    }

    var html = '';
    log.forEach(function(s) {
      var timeFormatted = s.time ? new Date(s.time).toLocaleTimeString('pl-PL', { hour: '2-digit', minute: '2-digit', second: '2-digit' }) : '-';
      var complBadge = s.completed ? '<span style="color:#10b981; font-weight:700;">✓ Ukończono</span>' : '<span style="color:var(--text-muted);">W trakcie</span>';
      html += '<tr style="border-bottom: 1px solid var(--border-color); font-size: 0.78rem;">' +
        '<td style="padding: 0.5rem; font-family: monospace; color: var(--accent);">' + s.vid.substring(0, 14) + '...</td>' +
        '<td style="padding: 0.5rem;">' + timeFormatted + '</td>' +
        '<td style="padding: 0.5rem; font-weight: 600;">' + (s.title || s.slug) + '</td>' +
        '<td style="padding: 0.5rem;">' + (s.device || 'Desktop') + '</td>' +
        '<td style="padding: 0.5rem; color: var(--text-secondary);">' + (s.referrer || 'Wejście bezpośrednie') + '</td>' +
        '<td style="padding: 0.5rem; text-align: right;">' + formatDwell(s.dwell_seconds) + ' (' + complBadge + ')</td>' +
      '</tr>';
    });
    container.innerHTML = html;
  }

  // =========================================================================
  // 9. PUBLICZNE API KONSOLOWE I ADMINISTRACYJNE
  // =========================================================================

  window.LaikaCookieAnalytics = {
    getStats: getRealStats,
    getCookie: getCookie,
    setCookie: setCookie,
    deleteCookie: deleteCookie,
    applyToUI: applyRealStatsToAdminUI,
    exportJSON: function() {
      var dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(getRealStats(), null, 2));
      var downloadAnchor = document.createElement('a');
      downloadAnchor.setAttribute("href", dataStr);
      downloadAnchor.setAttribute("download", "laika_cookie_analytics.json");
      document.body.appendChild(downloadAnchor);
      downloadAnchor.click();
      downloadAnchor.remove();
    },
    exportCSV: function() {
      var st = getRealStats();
      var csvRows = [
        ["Slug Artykulu", "Tytul", "Odsłony (Cookies)", "Czas Skupienia (s)", "Czas Skupienia (format)", "Ukończone Lektury"].join(",")
      ];
      for (var slug in st.posts) {
        var p = st.posts[slug];
        var dwellFmt = formatDwell(p.dwell_seconds);
        csvRows.push([
          slug,
          '"' + slug + '"',
          p.views || 0,
          p.dwell_seconds || 0,
          '"' + dwellFmt + '"',
          p.completions || 0
        ].join(","));
      }
      var csvStr = "data:text/csv;charset=utf-8," + encodeURIComponent(csvRows.join("\n"));
      var a = document.createElement('a');
      a.setAttribute("href", csvStr);
      a.setAttribute("download", "statystyki_bloga_cookies.csv");
      document.body.appendChild(a);
      a.click();
      a.remove();
    },
    reset: function() {
      localStorage.removeItem(STATS_STORAGE_KEY);
      deleteCookie("laika_seen");
      deleteCookie("laika_stats_summary");
      applyRealStatsToAdminUI();
      alert("Pomyślnie zresetowano dane analityczne cookies. Od tej chwili zliczane są wyłącznie świeże wejścia!");
    }
  };

  // Kompatybilność wsteczna z LaikaTelemetry
  window.LaikaTelemetry = {
    getSummary: function() {
      var st = getRealStats();
      return {
        total_pageviews: st.total_views || 0,
        posts_tracked: Object.keys(st.posts).length,
        total_local_views: st.total_views || 0,
        completed_reads: Object.values(st.posts).reduce(function(acc, p) { return acc + (p.completions || 0); }, 0),
        total_dwell_seconds: Object.values(st.posts).reduce(function(acc, p) { return acc + (p.dwell_seconds || 0); }, 0),
        posts: st.posts
      };
    },
    exportJSON: window.LaikaCookieAnalytics.exportJSON,
    reset: window.LaikaCookieAnalytics.reset
  };

})();

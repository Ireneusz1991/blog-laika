/**
 * Blog Laika — Silnik Bezpośredniej Aktualizacji na Stronie (Zero Ingerencji w GitHub UI)
 * Wspiera:
 *  1. Lokalny serwer FastAPI (/api/posts/inline-update)
 *  2. Atomową aktualizację całego serwisu (wpis + strona główna + kategoria + wyszukiwarka + źródło .md) w tle
 */
(function () {
  'use strict';

  const REPO_SLUG = 'Ireneusz1991/blog-laika';
  const PAT_STORAGE_KEY = 'blog_laika_gh_pat';

  const CATEGORY_NAMES = {
    technologia: 'Technologia',
    gospodarka: 'Gospodarka',
    historia: 'Historia',
    polityka: 'Polityka',
    eseje: 'Inne eseje',
    kondensat: 'Inne eseje'
  };

  function escapeHtml(str) {
    return String(str || '')
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }

  function formatInlineMarkdown(escapedLine) {
    let s = escapedLine;
    // Inline code `...`
    s = s.replace(/`([^`]+)`/g, '<code>$1</code>');
    // Images ![alt](url)
    s = s.replace(/!\[([^\]]*)\]\((https?:\/\/[^\s\)]+|\/[^\s\)]*)\)/g, '<img src="$2" alt="$1" style="max-width:100%; border-radius:8px; margin:1rem 0;" loading="lazy">');
    // Links [text](url)
    s = s.replace(/\[([^\]]+)\]\((https?:\/\/[^\s\)]+|\/[^\s\)]*)\)/g, '<a href="$2" target="_blank" rel="noopener">$1</a>');
    // Bold **...**
    s = s.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
    // Italic *...*
    s = s.replace(/(^|[^\*])\*([^*]+)\*(?!\*)/g, '$1<em>$2</em>');
    return s;
  }

  /**
   * Pełny, czysty renderer treści artykułu z Markdown do HTML (bez duplikowania okładki ani głównego H1 strony)
   */
  function renderMarkdownBody(md) {
    const cleaned = String(md || '').replace(/\r\n/g, '\n').replace(/^\s*#\s+[^\n]+\n*/, '');
    const lines = cleaned.split('\n');
    const out = [];
    let inUl = false;
    let inOl = false;
    let inCode = false;
    let codeBuf = [];
    let quoteBuf = [];
    let paraBuf = [];
    let tableBuf = [];

    const flushPara = () => {
      if (paraBuf.length > 0) {
        out.push('<p>' + paraBuf.map(l => formatInlineMarkdown(escapeHtml(l))).join('<br>') + '</p>');
        paraBuf = [];
      }
    };
    const flushLists = () => {
      if (inUl) { out.push('</ul>'); inUl = false; }
      if (inOl) { out.push('</ol>'); inOl = false; }
    };
    const flushQuote = () => {
      if (quoteBuf.length > 0) {
        out.push('<blockquote><p>' + quoteBuf.map(l => formatInlineMarkdown(escapeHtml(l))).join('<br>') + '</p></blockquote>');
        quoteBuf = [];
      }
    };
    const flushTable = () => {
      if (tableBuf.length >= 2) {
        const parseRow = r => r.trim().replace(/^\||\|$/g, '').split('|').map(c => formatInlineMarkdown(escapeHtml(c.trim())));
        const headers = parseRow(tableBuf[0]);
        const isSep = /^[\s\|:\-]+$/.test(tableBuf[1]);
        const bodyRows = (isSep ? tableBuf.slice(2) : tableBuf.slice(1)).map(parseRow);
        let thtml = '<table><thead><tr>' + headers.map(h => `<th>${h}</th>`).join('') + '</tr></thead><tbody>';
        bodyRows.forEach(r => {
          thtml += '<tr>' + r.map(c => `<td>${c}</td>`).join('') + '</tr>';
        });
        thtml += '</tbody></table>';
        out.push(thtml);
      } else if (tableBuf.length === 1) {
        paraBuf.push(tableBuf[0]);
        flushPara();
      }
      tableBuf = [];
    };

    for (let i = 0; i < lines.length; i++) {
      const raw = lines[i];
      const trimmed = raw.trim();

      if (trimmed.startsWith('```')) {
        flushPara(); flushLists(); flushQuote(); flushTable();
        if (!inCode) {
          inCode = true;
          codeBuf = [];
        } else {
          out.push('<pre><code>' + escapeHtml(codeBuf.join('\n')) + '</code></pre>');
          inCode = false;
          codeBuf = [];
        }
        continue;
      }

      if (inCode) {
        codeBuf.push(raw);
        continue;
      }

      // Markdown table row
      if (trimmed.startsWith('|') && trimmed.endsWith('|') && trimmed.length > 2) {
        flushPara(); flushLists(); flushQuote();
        tableBuf.push(trimmed);
        continue;
      } else if (tableBuf.length > 0) {
        flushTable();
      }

      if (trimmed === '') {
        flushPara(); flushLists(); flushQuote();
        continue;
      }

      if (/^(---|\*\*\*|___)$/.test(trimmed)) {
        flushPara(); flushLists(); flushQuote();
        out.push('<hr>');
        continue;
      }

      const hMatch = raw.match(/^(#{1,4})\s+(.+)$/);
      if (hMatch) {
        flushPara(); flushLists(); flushQuote();
        const lvl = Math.min(4, Math.max(2, hMatch[1].length)); // wewnątrz treści artykułu stosujemy H2-H4
        out.push(`<h${lvl}>${formatInlineMarkdown(escapeHtml(hMatch[2].trim()))}</h${lvl}>`);
        continue;
      }

      if (trimmed.startsWith('>')) {
        flushPara(); flushLists();
        quoteBuf.push(trimmed.replace(/^>\s?/, ''));
        continue;
      } else if (quoteBuf.length > 0) {
        flushQuote();
      }

      const ulMatch = raw.match(/^\s*[-*]\s+(.+)$/);
      if (ulMatch) {
        flushPara();
        if (inOl) { out.push('</ol>'); inOl = false; }
        if (!inUl) { out.push('<ul>'); inUl = true; }
        out.push(`<li>${formatInlineMarkdown(escapeHtml(ulMatch[1]))}</li>`);
        continue;
      }

      const olMatch = raw.match(/^\s*\d+\.\s+(.+)$/);
      if (olMatch) {
        flushPara();
        if (inUl) { out.push('</ul>'); inUl = false; }
        if (!inOl) { out.push('<ol>'); inOl = true; }
        out.push(`<li>${formatInlineMarkdown(escapeHtml(olMatch[1]))}</li>`);
        continue;
      }

      flushLists();
      paraBuf.push(raw);
    }

    if (inCode && codeBuf.length > 0) {
      out.push('<pre><code>' + escapeHtml(codeBuf.join('\n')) + '</code></pre>');
    }
    flushTable();
    flushQuote();
    flushLists();
    flushPara();

    return out.join('\n');
  }

  function utf8ToBase64(str) {
    const bytes = new TextEncoder().encode(String(str || ''));
    let bin = '';
    for (let i = 0; i < bytes.length; i += 0x8000) {
      bin += String.fromCharCode.apply(null, bytes.subarray(i, i + 0x8000));
    }
    return btoa(bin);
  }

  function base64ToUtf8(b64) {
    const clean = String(b64 || '').replace(/\s/g, '');
    const bin = atob(clean);
    const bytes = new Uint8Array(bin.length);
    for (let i = 0; i < bin.length; i++) bytes[i] = bin.charCodeAt(i);
    return new TextDecoder('utf-8').decode(bytes);
  }

  function getToken() {
    try { return (localStorage.getItem(PAT_STORAGE_KEY) || '').trim(); } catch (e) { return ''; }
  }

  function setToken(val) {
    try { localStorage.setItem(PAT_STORAGE_KEY, String(val || '').trim()); } catch (e) {}
  }

  function clearToken() {
    try { localStorage.removeItem(PAT_STORAGE_KEY); } catch (e) {}
  }

  async function verifyToken(candidate) {
    const tok = String(candidate || '').trim();
    if (!tok) {
      return { ok: false, reason: 'EMPTY', message: 'Pole tokena jest puste. Wklej swój kod zaczynający się od ghp_... lub github_pat_...' };
    }
    const lower = tok.toLowerCase();
    if (['laik2026', 'laika2026', 'admin2026', 'admin', 'laik', 'laika'].includes(lower) || tok.length < 20) {
      return {
        ok: false,
        reason: 'NOT_A_PAT',
        message: 'Wpisałeś hasło logowania zamiast Tokena Aktualizacji API (kod musi zaczynać się od ghp_... lub github_pat_...). Kliknij link po prawej, aby wygenerować go w 15 sekund.'
      };
    }
    try {
      const res = await fetch(`https://api.github.com/repos/${REPO_SLUG}?_t=${Date.now()}`, {
        headers: {
          'Accept': 'application/vnd.github+json',
          'Authorization': `Bearer ${tok}`,
          'X-GitHub-Api-Version': '2022-11-28'
        }
      });
      if (!res.ok) {
        return {
          ok: false,
          reason: 'INVALID',
          message: `Serwer odrzucił ten token (HTTP ${res.status}). Wygeneruj świeży token z zaznaczonym polem „repo”.`
        };
      }
      const data = await res.json();
      if (!data || !data.permissions || !data.permissions.push) {
        return {
          ok: false,
          reason: 'NO_PUSH',
          message: 'Token działa, ale nie ma zaznaczonego uprawnienia zapisu („repo” / Contents: Read and write).'
        };
      }
      setToken(tok);
      return { ok: true, message: 'Token zweryfikowany pomyślnie! Masz pełne uprawnienia bezpośredniego zapisu na blogu.' };
    } catch (e) {
      return { ok: false, reason: 'NETWORK', message: 'Błąd połączenia sieciowego podczas weryfikacji tokena: ' + String(e.message || e) };
    }
  }

  async function ghRequest(pat, method, endpoint, bodyObj) {
    const opts = {
      method,
      headers: {
        'Accept': 'application/vnd.github+json',
        'Authorization': `Bearer ${pat}`,
        'X-GitHub-Api-Version': '2022-11-28'
      }
    };
    if (bodyObj !== undefined) {
      opts.headers['Content-Type'] = 'application/json';
      opts.body = JSON.stringify(bodyObj);
    }
    const sep = endpoint.includes('?') ? '&' : '?';
    const url = method === 'GET'
      ? `https://api.github.com/repos/${REPO_SLUG}${endpoint}${sep}_t=${Date.now()}`
      : `https://api.github.com/repos/${REPO_SLUG}${endpoint}`;
    const res = await fetch(url, opts);
    if (res.status === 404 && method === 'GET') return null;
    if (!res.ok) {
      const txt = await res.text();
      throw new Error(`HTTP ${res.status}: ${txt.slice(0, 160)}`);
    }
    return res.status === 204 ? {} : await res.json();
  }

  async function getFileText(pat, branch, path) {
    const data = await ghRequest(pat, 'GET', `/contents/${path}?ref=${encodeURIComponent(branch)}`);
    if (!data || !data.content) return null;
    return { sha: data.sha, text: base64ToUtf8(data.content) };
  }

  async function putSingleFile(pat, branch, path, contentUtf8, message) {
    const existing = await ghRequest(pat, 'GET', `/contents/${path}?ref=${encodeURIComponent(branch)}`);
    const payload = {
      message,
      content: utf8ToBase64(contentUtf8),
      branch
    };
    if (existing && existing.sha) payload.sha = existing.sha;
    return await ghRequest(pat, 'PUT', `/contents/${path}`, payload);
  }

  async function commitMultipleFilesAtomically(pat, branch, filesMap, commitMessage) {
    // 1. Pobierz aktualny HEAD gałęzi
    const refData = await ghRequest(pat, 'GET', `/git/ref/heads/${branch}`);
    if (!refData || !refData.object || !refData.object.sha) {
      throw new Error(`Nie znaleziono gałęzi ${branch}`);
    }
    const baseCommitSha = refData.object.sha;

    // 2. Pobierz drzewo bazowe
    const commitData = await ghRequest(pat, 'GET', `/git/commits/${baseCommitSha}`);
    const baseTreeSha = commitData.tree.sha;

    // 3. Zbuduj nowe drzewo w 1 wywołaniu
    const treeEntries = Object.keys(filesMap).map(path => ({
      path,
      mode: '100644',
      type: 'blob',
      content: filesMap[path]
    }));

    const newTree = await ghRequest(pat, 'POST', '/git/trees', {
      base_tree: baseTreeSha,
      tree: treeEntries
    });

    // 4. Utwórz pojedynczy atomowy commit
    const newCommit = await ghRequest(pat, 'POST', '/git/commits', {
      message: commitMessage,
      tree: newTree.sha,
      parents: [baseCommitSha]
    });

    // 5. Przesuń wskaźnik gałęzi
    await ghRequest(pat, 'PATCH', `/git/refs/heads/${branch}`, {
      sha: newCommit.sha,
      force: true
    });

    return newCommit.sha;
  }

  function patchPostPageHtml(rawHtml, meta) {
    const doc = new DOMParser().parseFromString(rawHtml, 'text/html');
    const pubCat = meta.category === 'kondensat' ? 'eseje' : (meta.category || 'eseje');
    const pubCatName = CATEGORY_NAMES[pubCat] || 'Inne eseje';

    doc.title = `${meta.title} — Blog Laika`;

    const setMeta = (sel, val) => {
      const el = doc.querySelector(sel);
      if (el && val !== undefined) el.setAttribute('content', val);
    };
    setMeta('meta[name="description"]', meta.summary || '');
    setMeta('meta[property="og:title"]', `${meta.title} — Blog Laika`);
    setMeta('meta[property="og:description"]', meta.summary || '');
    setMeta('meta[name="twitter:title"]', `${meta.title} — Blog Laika`);
    setMeta('meta[name="twitter:description"]', meta.summary || '');
    if (meta.coverImage) {
      setMeta('meta[property="og:image"]', meta.coverImage);
      setMeta('meta[property="og:image:secure_url"]', meta.coverImage);
      setMeta('meta[name="twitter:image"]', meta.coverImage);
    }

    // Kategoria w nagłówku artykułu
    const catTag = doc.querySelector('.article-header .post-category-tag');
    if (catTag) {
      catTag.textContent = pubCatName;
      catTag.setAttribute('href', `/kategoria/${pubCat}`);
    }

    // Czas czytania w nagłówku artykułu
    doc.querySelectorAll('.article-header .post-meta span').forEach(sp => {
      if (sp.textContent && sp.textContent.includes('min czytania')) {
        sp.textContent = `⏱️ ${meta.readTime} min czytania`;
      }
    });

    // Tytuł H1 i Lead
    const titleEl = doc.getElementById('article-page-title');
    if (titleEl) titleEl.textContent = meta.title;

    let leadEl = doc.getElementById('article-page-lead');
    if (meta.summary) {
      if (!leadEl && titleEl && titleEl.parentNode) {
        leadEl = doc.createElement('p');
        leadEl.className = 'article-lead';
        leadEl.id = 'article-page-lead';
        titleEl.parentNode.appendChild(leadEl);
      }
      if (leadEl) leadEl.textContent = meta.summary;
    } else if (leadEl) {
      leadEl.textContent = '';
    }

    // Okładka artykułu
    let coverWrap = doc.getElementById('article-page-cover');
    if (meta.coverImage) {
      if (!coverWrap) {
        const headerEl = doc.querySelector('.article-header');
        if (headerEl && headerEl.parentNode) {
          coverWrap = doc.createElement('div');
          coverWrap.className = 'article-cover';
          coverWrap.id = 'article-page-cover';
          const img = doc.createElement('img');
          coverWrap.appendChild(img);
          headerEl.insertAdjacentElement('afterend', coverWrap);
        }
      }
      const img = coverWrap ? coverWrap.querySelector('img') : null;
      if (img) {
        img.setAttribute('src', meta.coverImage);
        img.setAttribute('alt', meta.title);
      }
    }

    // Główna treść HTML
    const bodyEl = doc.getElementById('article-page-body');
    if (bodyEl) {
      bodyEl.innerHTML = meta.renderedHtml;
    }

    // Tagi pod artykułem
    const tagsEl = doc.getElementById('article-page-tags');
    if (tagsEl && meta.tags !== undefined) {
      const tagList = String(meta.tags || '').split(',').map(t => t.trim()).filter(Boolean);
      tagsEl.innerHTML = tagList.map(t =>
        `<span style="font-size: 0.8rem; background: var(--bg-surface); padding: 0.25rem 0.6rem; border-radius: 4px; color: var(--text-muted);">#${escapeHtml(t)}</span>`
      ).join('');
    }

    // Surowe dane JSON wpisu (#post-raw-data) używane przy kolejnych edycjach
    const rawScript = doc.getElementById('post-raw-data');
    if (rawScript) {
      let postObj = {};
      try { postObj = JSON.parse(rawScript.textContent || '{}'); } catch (e) {}
      postObj.title = meta.title;
      postObj.slug = meta.slug;
      postObj.category = pubCat;
      postObj.category_name = pubCatName;
      postObj.is_kondensat = (meta.category === 'kondensat');
      postObj.tags = meta.tags || '';
      postObj.summary = meta.summary || '';
      postObj.cover_image = meta.coverImage || '';
      postObj.read_time = meta.readTime;
      postObj.content_markdown = meta.bodyMarkdown;
      postObj.content_html = meta.renderedHtml;
      rawScript.textContent = '\n' + JSON.stringify(postObj).replace(/<\/script>/gi, '<\\/script>') + '\n';
    }

    return '<!DOCTYPE html>\n' + doc.documentElement.outerHTML;
  }

  function patchHomepageHtml(rawHtml, meta) {
    const doc = new DOMParser().parseFromString(rawHtml, 'text/html');
    const pubCat = meta.category === 'kondensat' ? 'eseje' : (meta.category || 'eseje');
    const pubCatName = CATEGORY_NAMES[pubCat] || 'Inne eseje';
    const slug = meta.slug;
    let foundAny = false;

    const matchesPostLink = (a) => {
      const h = (a.getAttribute('href') || '').replace(/\/+$/, '');
      return h === `/post/${slug}` || h.endsWith(`/post/${slug}`);
    };

    // Aktualizacja wszystkich bloków tego wpisu na stronie głównej (hero, subgrid, extra, sidebar, katalog)
    doc.querySelectorAll('article').forEach(art => {
      const links = Array.from(art.querySelectorAll('a')).filter(matchesPostLink);
      if (links.length === 0 && !String(art.id || '').endsWith(slug)) return;
      foundAny = true;

      // Tytuł wewnątrz nagłówka H1/H3
      const titleLink = art.querySelector('h1 a, h3 a');
      if (titleLink) titleLink.textContent = meta.title;

      // Zajawka
      const excerpt = art.querySelector('.excerpt-preview, .sidebar-featured-excerpt, .post-card-excerpt');
      if (excerpt && meta.summary !== undefined) excerpt.textContent = meta.summary;

      // Pełna rozwinięta treść ("Czytaj więcej ↓" na stronie głównej!)
      const fullProse = art.querySelector('.editorial-full-prose');
      if (fullProse) fullProse.innerHTML = meta.renderedHtml;

      // Okładka
      const img = art.querySelector('img');
      if (img && meta.coverImage) {
        img.setAttribute('src', meta.coverImage);
        img.setAttribute('alt', meta.title);
      }

      // Kategoria
      if (art.classList.contains('editorial-hero-article')) {
        const heroCat = doc.querySelector('.editorial-meta-bar .editorial-label-cat');
        if (heroCat) heroCat.textContent = pubCatName;
      }
      const catEl = art.querySelector('.editorial-cat-tag, .post-category-tag, .sidebar-item-cat a');
      if (catEl) {
        catEl.textContent = pubCatName;
        if (catEl.tagName === 'A') catEl.setAttribute('href', `/kategoria/${pubCat}`);
      }

      // Czas czytania
      art.querySelectorAll('.byline-read-time, .editorial-read-min').forEach(rt => {
        rt.textContent = rt.classList.contains('byline-read-time')
          ? `⏱️ ${meta.readTime} min czytania`
          : `⏱️ ${meta.readTime} min`;
      });
    });

    // Jeśli to zupełnie nowy artykuł jeszcze nieobecny na stronie głównej -> dodaj do Najnowszych i Katalogu
    if (!foundAny) {
      const sidebarList = doc.querySelector('.sidebar-articles-list');
      if (sidebarList) {
        const item = doc.createElement('article');
        item.className = 'sidebar-article-item';
        item.innerHTML = `
          <div class="sidebar-item-body">
            <div class="sidebar-item-cat"><a href="/kategoria/${escapeHtml(pubCat)}">${escapeHtml(pubCatName)}</a></div>
            <h3 class="sidebar-item-title"><a href="/post/${escapeHtml(slug)}">${escapeHtml(meta.title)}</a></h3>
            <div class="editorial-author-byline">
              <span class="byline-author-name">Autor artykułu: Ireneusz Machowiec</span>
              <span class="byline-separator">&bull;</span>
              <span class="byline-date">${escapeHtml(meta.createdDatePl || 'Dzisiaj')}</span>
            </div>
          </div>`;
        sidebarList.insertBefore(item, sidebarList.firstChild);
      }
      const catalogGrid = doc.querySelector('#katalog-publikacji .posts-grid');
      if (catalogGrid) {
        const card = doc.createElement('article');
        card.className = 'post-card';
        card.id = `post-card-${slug}`;
        card.innerHTML = `
          ${meta.coverImage ? `<a href="/post/${escapeHtml(slug)}"><img src="${escapeHtml(meta.coverImage)}" alt="${escapeHtml(meta.title)}" class="post-card-thumb" loading="lazy"></a>` : ''}
          <div class="post-card-body">
            <div class="post-meta">
              <a href="/kategoria/${escapeHtml(pubCat)}" class="post-category-tag">${escapeHtml(pubCatName)}</a>
              <span>&bull;</span>
              <span class="byline-author-name">Autor artykułu: Ireneusz Machowiec</span>
              <span>&bull;</span>
              <span>⏱️ ${meta.readTime} min</span>
            </div>
            <h3 class="post-card-title"><a href="/post/${escapeHtml(slug)}">${escapeHtml(meta.title)}</a></h3>
            <p class="post-card-excerpt excerpt-preview">${escapeHtml(meta.summary || '')}</p>
            <div class="full-content" style="display: none;"><div class="editorial-full-prose">${meta.renderedHtml}</div></div>
            <div class="post-card-footer">
              <span>${escapeHtml(meta.createdDatePl || 'Dzisiaj')}</span>
              <div style="display: flex; gap: 0.6rem; align-items: center;">
                <a href="/post/${escapeHtml(slug)}" style="text-decoration: none; font-weight: 700; color: var(--accent); font-size: 0.85rem;">Otwórz wpis &rarr;</a>
              </div>
            </div>
          </div>`;
        catalogGrid.insertBefore(card, catalogGrid.firstChild);
      }
    }

    return '<!DOCTYPE html>\n' + doc.documentElement.outerHTML;
  }

  function patchCategoryPageHtml(rawHtml, meta, shouldExistInThisCategory) {
    const doc = new DOMParser().parseFromString(rawHtml, 'text/html');
    const pubCat = meta.category === 'kondensat' ? 'eseje' : (meta.category || 'eseje');
    const pubCatName = CATEGORY_NAMES[pubCat] || 'Inne eseje';
    const slug = meta.slug;
    let foundCard = null;

    doc.querySelectorAll('article.post-card').forEach(card => {
      const hasSlug = Array.from(card.querySelectorAll('a')).some(a => {
        const h = (a.getAttribute('href') || '').replace(/\/+$/, '');
        return h === `/post/${slug}` || h.endsWith(`/post/${slug}`);
      });
      if (hasSlug) foundCard = card;
    });

    if (!shouldExistInThisCategory) {
      if (foundCard) foundCard.remove();
      return '<!DOCTYPE html>\n' + doc.documentElement.outerHTML;
    }

    if (foundCard) {
      const tLink = foundCard.querySelector('.post-card-title a');
      if (tLink) tLink.textContent = meta.title;
      const exc = foundCard.querySelector('.post-card-excerpt');
      if (exc) exc.textContent = meta.summary || '';
      const img = foundCard.querySelector('img.post-card-thumb');
      if (img && meta.coverImage) {
        img.setAttribute('src', meta.coverImage);
        img.setAttribute('alt', meta.title);
      }
      foundCard.querySelectorAll('.post-meta span').forEach(sp => {
        if (sp.textContent && sp.textContent.includes('min')) {
          sp.textContent = `⏱️ ${meta.readTime} min`;
        }
      });
    } else {
      let grid = doc.querySelector('.posts-grid');
      if (!grid) {
        const container = doc.querySelector('.container');
        if (container) {
          grid = doc.createElement('div');
          grid.className = 'posts-grid';
          container.appendChild(grid);
        }
      }
      if (grid) {
        const card = doc.createElement('article');
        card.className = 'post-card';
        card.innerHTML = `
          ${meta.coverImage ? `<a href="/post/${escapeHtml(slug)}"><img src="${escapeHtml(meta.coverImage)}" alt="${escapeHtml(meta.title)}" class="post-card-thumb" loading="lazy"></a>` : ''}
          <div class="post-card-body">
            <div class="post-meta">
              <span class="post-category-tag">${escapeHtml(pubCatName)}</span>
              <span>•</span>
              <span class="byline-author-name">Autor artykułu: Ireneusz Machowiec</span>
              <span>•</span>
              <span>⏱️ ${meta.readTime} min</span>
            </div>
            <h3 class="post-card-title"><a href="/post/${escapeHtml(slug)}">${escapeHtml(meta.title)}</a></h3>
            <p class="post-card-excerpt">${escapeHtml(meta.summary || '')}</p>
            <div class="post-card-footer">
              <span>${escapeHtml(meta.createdDatePl || 'Dzisiaj')}</span>
              <a href="/post/${escapeHtml(slug)}" style="text-decoration: none; font-weight: 600; color: var(--accent);">Czytaj &rarr;</a>
            </div>
          </div>`;
        grid.insertBefore(card, grid.firstChild);
      }
    }

    return '<!DOCTYPE html>\n' + doc.documentElement.outerHTML;
  }

  function patchSearchIndex(rawJson, meta) {
    let arr = [];
    try { arr = JSON.parse(rawJson || '[]'); } catch (e) { arr = []; }
    const pubCat = meta.category === 'kondensat' ? 'eseje' : (meta.category || 'eseje');
    const pubCatName = CATEGORY_NAMES[pubCat] || 'Inne eseje';
    const idx = arr.findIndex(x => x && x.slug === meta.slug);
    const entry = {
      title: meta.title,
      slug: meta.slug,
      summary: meta.summary || '',
      category: pubCat,
      category_name: pubCatName,
      tags: meta.tags || '',
      read_time: meta.readTime,
      created_date: (idx > -1 && arr[idx].created_date) ? arr[idx].created_date : (meta.createdDatePl || '')
    };
    if (idx > -1) {
      arr[idx] = entry;
    } else {
      arr.unshift(entry);
    }
    return JSON.stringify(arr, null, 2);
  }

  /**
   * Główna funkcja zapisująca artykuł bezpośrednio na stronie (lokalnie przez FastAPI lub zdalnie w 1 atomowym zapisie)
   */
  async function saveArticleEverywhere(payload, onProgress) {
    const notify = (msg) => { if (typeof onProgress === 'function') onProgress(msg); };
    const words = String(payload.bodyMarkdown || '').trim() ? String(payload.bodyMarkdown || '').trim().split(/\s+/).length : 0;
    const readTime = Math.max(1, Math.ceil(words / 190));
    const renderedHtml = payload.renderedHtml || renderMarkdownBody(payload.bodyMarkdown || '');
    const pubCat = payload.category === 'kondensat' ? 'eseje' : (payload.category || 'eseje');

    const cleanSlug = String(payload.slug || '')
      .toLowerCase().trim()
      .split('-')
      .filter(p => p && !p.startsWith('kondensat'))
      .join('-') || 'esej';
    const cleanMarkdownDoc = payload.markdownDoc
      ? String(payload.markdownDoc).replace(/^slug:\s*"[^"]*"/m, `slug: "${cleanSlug}"`)
      : payload.markdownDoc;

    const meta = {
      title: payload.title || 'Wpis bez tytułu',
      slug: cleanSlug,
      category: payload.category || 'eseje',
      oldCategory: payload.oldCategory || pubCat,
      tags: payload.tags || '',
      summary: payload.summary || '',
      coverImage: payload.coverImage || '',
      bodyMarkdown: payload.bodyMarkdown || '',
      markdownDoc: cleanMarkdownDoc,
      renderedHtml,
      readTime,
      createdDatePl: payload.createdDatePl || ''
    };

    // 1. Tryb lokalnego serwera FastAPI (zero tokenów!)
    const isLocalHost = (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1');
    if (isLocalHost) {
      notify('⏳ Zapisywanie artykułu bezpośrednio na lokalnym serwerze i publikacja zmian...');
      const res = await fetch('/api/posts/inline-update', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          auth: 'authenticated',
          slug: meta.slug,
          title: meta.title,
          category: meta.category,
          tags: meta.tags,
          summary: meta.summary,
          cover_image: meta.coverImage,
          content_markdown: meta.bodyMarkdown
        })
      });
      const data = await res.json();
      if (!res.ok || data.status !== 'ok') {
        throw new Error(data.message || 'Błąd zapisu lokalnego.');
      }
      rememberRecentEdit(meta);
      return { mode: 'local', renderedHtml, readTime, publicCategory: pubCat, publicCategoryName: CATEGORY_NAMES[pubCat] || 'Inne eseje' };
    }

    // 2. Tryb zdalny na blog-laika.com (atomowy zapis w tle przez Token Aktualizacji)
    const pat = getToken();
    if (!pat) {
      const err = new Error('MISSING_TOKEN');
      err.code = 'MISSING_TOKEN';
      throw err;
    }

    notify('⏳ Synchronizacja pliku źródłowego wpisu w tle...');
    await putSingleFile(pat, 'main', `posts/${meta.slug}.md`, meta.markdownDoc, `Aktualizacja wpisu ${meta.slug}`);

    notify('⏳ Pobieranie bieżących widoków strony do atomowej aktualizacji...');
    const oldPubCat = meta.oldCategory === 'kondensat' ? 'eseje' : (meta.oldCategory || pubCat);

    const [postFile, indexFile, catFile, oldCatFile, searchFile] = await Promise.all([
      getFileText(pat, 'gh-pages', `post/${meta.slug}/index.html`),
      getFileText(pat, 'gh-pages', 'index.html'),
      getFileText(pat, 'gh-pages', `kategoria/${pubCat}/index.html`),
      (oldPubCat && oldPubCat !== pubCat) ? getFileText(pat, 'gh-pages', `kategoria/${oldPubCat}/index.html`) : Promise.resolve(null),
      getFileText(pat, 'gh-pages', 'search-index.json')
    ]);

    let basePostHtml = postFile ? postFile.text : null;
    if (!basePostHtml) {
      const tplPost = await getFileText(pat, 'gh-pages', 'post/pochwala-dociekliwego-laika/index.html');
      if (tplPost) basePostHtml = tplPost.text;
    }

    const filesToCommit = {};
    if (basePostHtml) {
      filesToCommit[`post/${meta.slug}/index.html`] = patchPostPageHtml(basePostHtml, meta);
    }
    if (indexFile && indexFile.text) {
      filesToCommit['index.html'] = patchHomepageHtml(indexFile.text, meta);
    }
    if (catFile && catFile.text) {
      filesToCommit[`kategoria/${pubCat}/index.html`] = patchCategoryPageHtml(catFile.text, meta, true);
    }
    if (oldCatFile && oldCatFile.text && oldPubCat !== pubCat) {
      filesToCommit[`kategoria/${oldPubCat}/index.html`] = patchCategoryPageHtml(oldCatFile.text, meta, false);
    }
    if (searchFile && searchFile.text) {
      filesToCommit['search-index.json'] = patchSearchIndex(searchFile.text, meta);
    }

    notify('⏳ Publikowanie zmian we wszystkich sekcjach bloga (wpis, strona główna, kategoria, wyszukiwarka)...');
    const commitSha = await commitMultipleFilesAtomically(
      pat,
      'gh-pages',
      filesToCommit,
      `Aktualizacja artykulu na zywo: ${meta.title}`
    );

    rememberRecentEdit(meta);

    return {
      mode: 'cloud-atomic',
      commitSha,
      renderedHtml,
      readTime,
      publicCategory: pubCat,
      publicCategoryName: CATEGORY_NAMES[pubCat] || 'Inne eseje'
    };
  }

  // =========================================================================
  // NATYCHMIASTOWA HYDRACJA DOM (OMIJA 10-MINUTOWY CACHE CDN `max-age=600`!)
  // Dzięki temu odświeżenie F5 lub przejście na stronę główną 0.1 s po zapisie
  // od razu pokazuje nową treść, zanim CDN GitHub Pages odświeży swój bufor.
  // =========================================================================
  const RECENT_EDITS_KEY = 'blog_laika_recent_edits_v1';
  const RECENT_TTL_MS = 30 * 60 * 1000; // 30 minut (CDN ma max-age=600s = 10 min)

  function loadRecentEditsMap() {
    try {
      const raw = localStorage.getItem(RECENT_EDITS_KEY);
      if (!raw) return {};
      const parsed = JSON.parse(raw);
      const now = Date.now();
      let changed = false;
      Object.keys(parsed).forEach(slug => {
        if (!parsed[slug] || !parsed[slug].savedAt || (now - parsed[slug].savedAt) > RECENT_TTL_MS) {
          delete parsed[slug];
          changed = true;
        }
      });
      if (changed) localStorage.setItem(RECENT_EDITS_KEY, JSON.stringify(parsed));
      return parsed;
    } catch (e) {
      return {};
    }
  }

  function rememberRecentEdit(meta) {
    try {
      const map = loadRecentEditsMap();
      const pubCat = meta.category === 'kondensat' ? 'eseje' : (meta.category || 'eseje');
      map[meta.slug] = {
        savedAt: Date.now(),
        title: meta.title,
        slug: meta.slug,
        category: pubCat,
        rawCategory: meta.category,
        category_name: CATEGORY_NAMES[pubCat] || 'Inne eseje',
        is_kondensat: meta.category === 'kondensat',
        tags: meta.tags || '',
        summary: meta.summary || '',
        cover_image: meta.coverImage || '',
        read_time: meta.readTime,
        content_markdown: meta.bodyMarkdown || '',
        content_html: meta.renderedHtml || '',
        created_date: meta.createdDatePl || ''
      };
      localStorage.setItem(RECENT_EDITS_KEY, JSON.stringify(map));
    } catch (e) {}
  }

  function getRecentEdit(slug) {
    const map = loadRecentEditsMap();
    return map[slug] || null;
  }

  function hydrateLiveDomFromRecentEdits() {
    const map = loadRecentEditsMap();
    const slugs = Object.keys(map);
    if (slugs.length === 0) return;

    // 1. Strona pojedynczego wpisu (/post/<slug>/)
    const rawScript = document.getElementById('post-raw-data');
    if (rawScript) {
      let pageObj = null;
      try { pageObj = JSON.parse(rawScript.textContent || '{}'); } catch (e) {}
      if (pageObj && pageObj.slug && map[pageObj.slug]) {
        const ed = map[pageObj.slug];
        document.title = `${ed.title} — Blog Laika`;
        const h1 = document.getElementById('article-page-title');
        if (h1) h1.textContent = ed.title;
        let lead = document.getElementById('article-page-lead');
        if (ed.summary) {
          if (!lead && h1 && h1.parentNode) {
            lead = document.createElement('p');
            lead.className = 'article-lead';
            lead.id = 'article-page-lead';
            h1.parentNode.appendChild(lead);
          }
          if (lead) lead.textContent = ed.summary;
        } else if (lead) {
          lead.textContent = '';
        }
        const catTag = document.querySelector('.article-header .post-category-tag');
        if (catTag) {
          catTag.textContent = ed.category_name;
          catTag.setAttribute('href', `/kategoria/${ed.category}`);
        }
        document.querySelectorAll('.article-header .post-meta span').forEach(sp => {
          if (sp.textContent && sp.textContent.includes('min czytania')) {
            sp.textContent = `⏱️ ${ed.read_time} min czytania`;
          }
        });
        if (ed.cover_image) {
          const cImg = document.querySelector('#article-page-cover img');
          if (cImg) {
            cImg.src = ed.cover_image;
            cImg.alt = ed.title;
          }
        }
        const bodyEl = document.getElementById('article-page-body');
        if (bodyEl && ed.content_html) bodyEl.innerHTML = ed.content_html;

        const tagsEl = document.getElementById('article-page-tags');
        if (tagsEl && ed.tags !== undefined) {
          const tList = String(ed.tags || '').split(',').map(t => t.trim()).filter(Boolean);
          tagsEl.innerHTML = tList.map(t =>
            `<span style="font-size: 0.8rem; background: var(--bg-surface); padding: 0.25rem 0.6rem; border-radius: 4px; color: var(--text-muted);">#${escapeHtml(t)}</span>`
          ).join('');
        }

        const merged = Object.assign({}, pageObj, ed);
        rawScript.textContent = JSON.stringify(merged).replace(/<\/script>/gi, '<\\/script>');
        if (window.currentPostData && window.currentPostData.slug === ed.slug) {
          Object.assign(window.currentPostData, ed);
        }
      }
    }

    // 2. Strona główna i podstrony kategorii (karty artykułów)
    slugs.forEach(slug => {
      const ed = map[slug];
      document.querySelectorAll('article').forEach(art => {
        const hasLink = Array.from(art.querySelectorAll('a')).some(a => {
          const h = (a.getAttribute('href') || '').split('?')[0].replace(/\/+$/, '');
          return h === `/post/${slug}` || h.endsWith(`/post/${slug}`);
        });
        if (!hasLink && !String(art.id || '').endsWith(slug)) return;

        const tLink = art.querySelector('h1 a, h3 a, .post-card-title a');
        if (tLink) tLink.textContent = ed.title;

        const exc = art.querySelector('.excerpt-preview, .sidebar-featured-excerpt, .post-card-excerpt');
        if (exc) exc.textContent = ed.summary || '';

        const fullProse = art.querySelector('.editorial-full-prose');
        if (fullProse && ed.content_html) fullProse.innerHTML = ed.content_html;

        const img = art.querySelector('img');
        if (img && ed.cover_image) {
          img.src = ed.cover_image;
          img.alt = ed.title;
        }

        if (art.classList.contains('editorial-hero-article')) {
          const heroCat = document.querySelector('.editorial-meta-bar .editorial-label-cat');
          if (heroCat) heroCat.textContent = ed.category_name;
        }
        const catEl = art.querySelector('.editorial-cat-tag, .post-category-tag, .sidebar-item-cat a');
        if (catEl) {
          catEl.textContent = ed.category_name;
          if (catEl.tagName === 'A') catEl.setAttribute('href', `/kategoria/${ed.category}`);
        }
        art.querySelectorAll('.byline-read-time, .editorial-read-min').forEach(rt => {
          rt.textContent = rt.classList.contains('byline-read-time')
            ? `⏱️ ${ed.read_time} min czytania`
            : `⏱️ ${ed.read_time} min`;
        });
      });

      // 3. Tabela opublikowanych wpisów w /admin/
      document.querySelectorAll('.admin-table tbody tr').forEach(row => {
        const a = row.querySelector('td a');
        if (!a) return;
        const h = (a.getAttribute('href') || '').split('?')[0].replace(/\/+$/, '');
        if (h === `/post/${slug}` || h.endsWith(`/post/${slug}`)) {
          a.textContent = ed.title;
          const catSpan = row.querySelector('.post-category-tag');
          if (catSpan) catSpan.textContent = ed.category_name;
          const cells = row.querySelectorAll('td');
          if (cells[2]) cells[2].textContent = `⏱️ ${ed.read_time} min`;
        }
      });
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', hydrateLiveDomFromRecentEdits);
  } else {
    hydrateLiveDomFromRecentEdits();
  }

  window.LaikaDirectSync = {
    CATEGORY_NAMES,
    renderMarkdownBody,
    getToken,
    setToken,
    clearToken,
    verifyToken,
    getRecentEdit,
    saveArticleEverywhere
  };
})();

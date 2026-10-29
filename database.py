import sqlite3
import re
from datetime import datetime
from typing import List, Dict, Optional, Any
import markdown
from slugify import slugify
from config import DB_PATH

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            slug TEXT UNIQUE NOT NULL,
            summary TEXT,
            content_markdown TEXT NOT NULL,
            content_html TEXT NOT NULL,
            category TEXT NOT NULL,
            tags TEXT DEFAULT '',
            cover_image TEXT DEFAULT '',
            status TEXT DEFAULT 'published',
            featured INTEGER DEFAULT 0,
            read_time INTEGER DEFAULT 4,
            views INTEGER DEFAULT 0,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_posts_slug ON posts(slug)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_posts_category ON posts(category)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_posts_status ON posts(status)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_posts_created ON posts(created_at)")

    # Realna tabela analityki opartej na plikach cookies czytelników (zero losowych danych)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS analytics_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            visitor_id TEXT NOT NULL,
            session_id TEXT NOT NULL,
            event_type TEXT NOT NULL,
            post_slug TEXT,
            category TEXT,
            referrer TEXT,
            referrer_type TEXT,
            device_type TEXT,
            dwell_seconds INTEGER DEFAULT 0,
            scroll_depth INTEGER DEFAULT 0,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_analytics_vid ON analytics_events(visitor_id)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_analytics_slug ON analytics_events(post_slug)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_analytics_event ON analytics_events(event_type)")
    conn.commit()
    conn.close()

def calculate_read_time(text: str) -> int:
    words = len(re.findall(r'\w+', text))
    minutes = max(1, round(words / 200))
    return minutes

def extract_summary(md_text: str) -> str:
    cleaned = re.sub(r'^#+\s+.*$', '', md_text, flags=re.MULTILINE)
    cleaned = re.sub(r'^>\s+.*$', '', cleaned, flags=re.MULTILINE)
    cleaned = re.sub(r'^---+\s*$', '', cleaned, flags=re.MULTILINE)
    cleaned = re.sub(r'[\*_`\[\]\(\)]', '', cleaned)
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()
    return (cleaned[:220].rstrip() + "...") if len(cleaned) > 220 else cleaned

def render_markdown(md_text: str) -> str:
    # Strip leading H1 title if present to avoid duplicating the page header H1
    cleaned_md = re.sub(r'^\s*#\s+[^\n]+\n*', '', md_text, count=1)
    extensions = [
        'extra',
        'codehilite',
        'toc',
        'tables',
        'fenced_code',
        'nl2br'
    ]
    return markdown.markdown(cleaned_md, extensions=extensions)

def create_post(title: str, content_markdown: str, category: str, summary: str = "", 
                slug: str = "", tags: str = "", cover_image: str = "", 
                status: str = "published", featured: int = 0) -> int:
    conn = get_db()
    cursor = conn.cursor()
    
    if not slug:
        slug = slugify(title)
        
    # Ensure slug uniqueness
    base_slug = slug
    counter = 1
    while True:
        cursor.execute("SELECT id FROM posts WHERE slug = ?", (slug,))
        if not cursor.fetchone():
            break
        slug = f"{base_slug}-{counter}"
        counter += 1
        
    if not summary:
        summary = extract_summary(content_markdown)
        
    content_html = render_markdown(content_markdown)
    read_time = calculate_read_time(content_markdown)
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    cursor.execute("""
        INSERT INTO posts (title, slug, summary, content_markdown, content_html, category, tags, cover_image, status, featured, read_time, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (title, slug, summary, content_markdown, content_html, category, tags, cover_image, status, featured, read_time, now, now))
    
    post_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return post_id

def update_post(post_id: int, title: str, content_markdown: str, category: str, summary: str = "", 
                slug: str = "", tags: str = "", cover_image: str = "", 
                status: str = "published", featured: int = 0) -> bool:
    conn = get_db()
    cursor = conn.cursor()
    
    if not slug:
        slug = slugify(title)
        
    # Ensure slug uniqueness excluding current post
    base_slug = slug
    counter = 1
    while True:
        cursor.execute("SELECT id FROM posts WHERE slug = ? AND id != ?", (slug, post_id))
        if not cursor.fetchone():
            break
        slug = f"{base_slug}-{counter}"
        counter += 1
        
    if not summary:
        summary = extract_summary(content_markdown)
        
    content_html = render_markdown(content_markdown)
    read_time = calculate_read_time(content_markdown)
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    cursor.execute("""
        UPDATE posts 
        SET title = ?, slug = ?, summary = ?, content_markdown = ?, content_html = ?, 
            category = ?, tags = ?, cover_image = ?, status = ?, featured = ?, 
            read_time = ?, updated_at = ?
        WHERE id = ?
    """, (title, slug, summary, content_markdown, content_html, category, tags, cover_image, status, featured, read_time, now, post_id))
    
    conn.commit()
    conn.close()
    return True

def delete_post(post_id: int) -> bool:
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM posts WHERE id = ?", (post_id,))
    conn.commit()
    conn.close()
    return True

def get_post_by_slug(slug: str, include_drafts: bool = False, count_view: bool = False) -> Optional[Dict[str, Any]]:
    conn = get_db()
    cursor = conn.cursor()
    if include_drafts:
        cursor.execute("SELECT * FROM posts WHERE slug = ?", (slug,))
    else:
        cursor.execute("SELECT * FROM posts WHERE slug = ? AND status = 'published'", (slug,))
    row = cursor.fetchone()
    if row and not include_drafts and count_view:
        cursor.execute("UPDATE posts SET views = views + 1 WHERE id = ?", (row["id"],))
        conn.commit()
    conn.close()
    return dict(row) if row else None

def get_post_by_id(post_id: int) -> Optional[Dict[str, Any]]:
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM posts WHERE id = ?", (post_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

def get_posts(category: Optional[str] = None, status: str = "published", 
              limit: int = 50, offset: int = 0, tag: Optional[str] = None) -> List[Dict[str, Any]]:
    conn = get_db()
    cursor = conn.cursor()
    
    query = "SELECT * FROM posts WHERE 1=1"
    params = []
    
    if status != "all":
        query += " AND status = ?"
        params.append(status)
        
    if category:
        query += " AND category = ?"
        params.append(category)
        
    if tag:
        query += " AND tags LIKE ?"
        params.append(f"%{tag}%")
        
    query += " ORDER BY featured DESC, created_at DESC LIMIT ? OFFSET ?"
    params.extend([limit, offset])
    
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def search_posts(keyword: str, limit: int = 20) -> List[Dict[str, Any]]:
    conn = get_db()
    cursor = conn.cursor()
    pattern = f"%{keyword}%"
    cursor.execute("""
        SELECT * FROM posts 
        WHERE status = 'published' AND (title LIKE ? OR summary LIKE ? OR content_markdown LIKE ? OR tags LIKE ?)
        ORDER BY created_at DESC LIMIT ?
    """, (pattern, pattern, pattern, pattern, limit))
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_featured_post() -> Optional[Dict[str, Any]]:
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM posts WHERE status = 'published' AND featured = 1 ORDER BY created_at DESC LIMIT 1")
    row = cursor.fetchone()
    if not row:
        cursor.execute("SELECT * FROM posts WHERE status = 'published' ORDER BY created_at DESC LIMIT 1")
        row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

def record_cookie_pageview(visitor_id: str, session_id: str, post_slug: str, category: str = "",
                           referrer: str = "", referrer_type: str = "Wejścia Bezpośrednie", device_type: str = "Desktop") -> bool:
    """Rejestruje realną odsłonę czytelnika na bazie ciasteczek laika_vid i laika_sid.
    Chroni przed sztucznym nabijaniem (unikalna wizyta per sesja)."""
    if not visitor_id or not session_id:
        return False
    conn = get_db()
    cursor = conn.cursor()
    
    # Sprawdzenie czy w tej 30-minutowej sesji ta strona była już zarejestrowana
    cursor.execute("""
        SELECT id FROM analytics_events 
        WHERE session_id = ? AND post_slug = ? AND event_type = 'pageview'
    """, (session_id, post_slug))
    already_recorded = cursor.fetchone()
    
    if not already_recorded:
        cursor.execute("""
            INSERT INTO analytics_events (visitor_id, session_id, event_type, post_slug, category, referrer, referrer_type, device_type)
            VALUES (?, ?, 'pageview', ?, ?, ?, ?, ?)
        """, (visitor_id, session_id, post_slug, category, referrer, referrer_type, device_type))
        if post_slug:
            cursor.execute("UPDATE posts SET views = views + 1 WHERE slug = ?", (post_slug,))
        conn.commit()
        conn.close()
        return True
    
    conn.close()
    return False

def record_cookie_dwell(visitor_id: str, session_id: str, post_slug: str, dwell_seconds: int, scroll_depth: int):
    """Aktualizuje rzeczywisty czas aktywnego czytania i głębokość przewinięcia na bazie ciasteczek."""
    if not visitor_id or not session_id or not post_slug:
        return
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE analytics_events 
        SET dwell_seconds = MAX(dwell_seconds, ?), scroll_depth = MAX(scroll_depth, ?)
        WHERE session_id = ? AND post_slug = ? AND event_type = 'pageview'
    """, (dwell_seconds, scroll_depth, session_id, post_slug))
    conn.commit()
    conn.close()

def get_internal_analytics() -> Dict[str, Any]:
    """Generuje pakiet REALNYCH statystyk zebranych na podstawie plików cookies i sesji czytelników (zero losowych danych)."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM posts WHERE status = 'published' ORDER BY views DESC")
    posts = [dict(row) for row in cursor.fetchall()]

    total_views = sum(p.get("views", 0) for p in posts)
    total_words = 0
    post_stats = []

    try:
        from config import CATEGORY_MAP
    except ImportError:
        CATEGORY_MAP = {
            "technologia": "Technologia",
            "gospodarka": "Gospodarka",
            "historia": "Historia",
            "polityka": "Polityka",
            "eseje": "Inne eseje",
            "kondensat": "⚡ Kondensaty"
        }

    cat_views = {cat_slug: 0 for cat_slug in CATEGORY_MAP}

    # Pobierz z bazy realne dane zagregowane ze zdarzeń cookies
    cursor.execute("""
        SELECT post_slug, 
               COUNT(*) as real_views,
               AVG(dwell_seconds) as avg_dwell,
               SUM(CASE WHEN scroll_depth >= 75 THEN 1 ELSE 0 END) as completions
        FROM analytics_events
        WHERE event_type = 'pageview' AND post_slug IS NOT NULL AND post_slug != ''
        GROUP BY post_slug
    """)
    slug_events = {row["post_slug"]: dict(row) for row in cursor.fetchall()}

    for p in posts:
        slug = p["slug"]
        views = p.get("views", 0)
        cat = p.get("category", "eseje")
        cat_views[cat] = cat_views.get(cat, 0) + views
        
        content = p.get("content_markdown", "")
        words = len(re.findall(r'\w+', content))
        total_words += words
        
        read_time_calc = max(1, round(words / 200))
        
        # Realne metryki ze zdarzeń cookies
        ev = slug_events.get(slug, {})
        avg_dwell_sec = round(ev.get("avg_dwell") or 0)
        completions = ev.get("completions") or 0
        ev_views = ev.get("real_views") or views
        completion_pct = round((completions / ev_views * 100)) if ev_views > 0 else 0
        
        dwell_min = avg_dwell_sec // 60
        dwell_s = avg_dwell_sec % 60
        dwell_formatted = f"{dwell_min}m {dwell_s:02d}s"

        pct_of_total = round((views / total_views * 100), 1) if total_views > 0 else 0

        post_stats.append({
            "id": p.get("id"),
            "title": p.get("title"),
            "slug": slug,
            "category": cat,
            "category_name": CATEGORY_MAP.get(cat, cat.capitalize()),
            "views": views,
            "views_share_pct": pct_of_total,
            "words": words,
            "read_time": read_time_calc,
            "read_completion_pct": completion_pct,
            "avg_dwell_sec": avg_dwell_sec,
            "avg_dwell_formatted": dwell_formatted,
            "created_at": p.get("created_at", "")[:10]
        })

    category_analytics = []
    for cat_slug, c_views in cat_views.items():
        c_pct = round((c_views / total_views * 100), 1) if total_views > 0 else 0
        cat_posts_count = sum(1 for p in posts if p.get("category") == cat_slug)
        category_analytics.append({
            "slug": cat_slug,
            "name": CATEGORY_MAP.get(cat_slug, cat_slug.capitalize()),
            "views": c_views,
            "share_pct": c_pct,
            "posts_count": cat_posts_count
        })

    category_analytics.sort(key=lambda x: x["views"], reverse=True)

    # Realna liczba unikalnych czytelników (unikalne ciasteczka laika_vid)
    cursor.execute("SELECT COUNT(DISTINCT visitor_id) FROM analytics_events WHERE visitor_id != ''")
    row_uniques = cursor.fetchone()
    real_uniques = row_uniques[0] if (row_uniques and row_uniques[0] is not None) else 0

    # Realny średni czas skupienia czytelnika
    cursor.execute("SELECT AVG(dwell_seconds) FROM analytics_events WHERE dwell_seconds > 0")
    row_avg_dwell = cursor.fetchone()
    avg_dwell_total_sec = round(row_avg_dwell[0]) if (row_avg_dwell and row_avg_dwell[0] is not None) else 0
    avg_dwell_total_fmt = f"{avg_dwell_total_sec // 60}m {avg_dwell_total_sec % 60:02d}s"

    # Realny wskaźnik ukończenia lektury
    cursor.execute("""
        SELECT COUNT(*), SUM(CASE WHEN scroll_depth >= 75 THEN 1 ELSE 0 END)
        FROM analytics_events WHERE event_type = 'pageview'
    """)
    row_compl = cursor.fetchone()
    if row_compl and row_compl[0] and row_compl[0] > 0:
        avg_completion = round(((row_compl[1] or 0) / row_compl[0]) * 100, 1)
    else:
        avg_completion = 0.0

    # Realne źródła wejść na bazie referrera z ciasteczek
    cursor.execute("""
        SELECT referrer_type, COUNT(*) as cnt
        FROM analytics_events
        WHERE event_type = 'pageview' AND referrer_type IS NOT NULL AND referrer_type != ''
        GROUP BY referrer_type
        ORDER BY cnt DESC
    """)
    ref_rows = cursor.fetchall()
    total_refs = sum(r["cnt"] for r in ref_rows)
    
    icon_map = {
        "Wyszukiwarki (Organic Search)": "🔍",
        "Wyszukiwarki": "🔍",
        "Media Społecznościowe & Dyskusje": "🌐",
        "Media Społecznościowe": "🌐",
        "Wejścia Bezpośrednie & Zakładki": "🔖",
        "Wejścia Bezpośrednie": "🔖",
        "Czytniki RSS & Agregatory": "📡",
        "Czytniki RSS": "📡",
        "Inne": "🔗"
    }

    traffic_sources = []
    if total_refs > 0:
        for r in ref_rows:
            share = round((r["cnt"] / total_refs * 100), 1)
            traffic_sources.append({
                "name": r["referrer_type"],
                "count": r["cnt"],
                "share_pct": share,
                "icon": icon_map.get(r["referrer_type"], "🌐"),
                "desc": f"Rzeczywiste wejścia zidentyfikowane ciasteczkiem: {r['cnt']}"
            })
    else:
        traffic_sources = [
            {"name": "Wejścia Bezpośrednie & Zakładki", "count": 0, "share_pct": 100.0, "icon": "🔖", "desc": "Wpisywanie adresu URL, brak zewnętrznego referrera"}
        ]

    # Realny podział urządzeń (z navigator.userAgent / device_type)
    cursor.execute("""
        SELECT device_type, COUNT(*) as cnt
        FROM analytics_events
        WHERE event_type = 'pageview' AND device_type IS NOT NULL AND device_type != ''
        GROUP BY device_type
        ORDER BY cnt DESC
    """)
    dev_rows = cursor.fetchall()
    total_devs = sum(r["cnt"] for r in dev_rows)
    dev_icon = {"Mobile": "📱", "Smartfony (Mobile)": "📱", "Desktop": "💻", "Komputery (Desktop)": "💻", "Tablety": "📟", "Tablet": "📟"}
    
    device_mix = []
    if total_devs > 0:
        for r in dev_rows:
            share = round((r["cnt"] / total_devs * 100), 1)
            device_mix.append({
                "device": r["device_type"],
                "count": r["cnt"],
                "share_pct": share,
                "icon": dev_icon.get(r["device_type"], "💻")
            })
    else:
        device_mix = [
            {"device": "Komputery (Desktop)", "count": 0, "share_pct": 100.0, "icon": "💻"}
        ]

    # Ostatnie 15 realnych sesji z ciasteczek
    cursor.execute("""
        SELECT visitor_id, session_id, post_slug, referrer_type, device_type, dwell_seconds, scroll_depth, created_at
        FROM analytics_events
        WHERE event_type = 'pageview'
        ORDER BY created_at DESC
        LIMIT 15
    """)
    recent_sessions = [dict(r) for r in cursor.fetchall()]
    conn.close()

    return {
        "summary": {
            "total_views": total_views,
            "estimated_uniques": real_uniques,
            "avg_completion_pct": avg_completion,
            "avg_dwell_formatted": avg_dwell_total_fmt,
            "avg_dwell_sec": avg_dwell_total_sec,
            "total_posts": len(posts),
            "total_words": total_words
        },
        "posts": post_stats,
        "categories": category_analytics,
        "traffic_sources": traffic_sources,
        "device_mix": device_mix,
        "recent_sessions": recent_sessions
    }

def get_stats() -> Dict[str, Any]:
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM posts WHERE status = 'published'")
    published = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM posts WHERE status = 'draft'")
    drafts = cursor.fetchone()[0]
    cursor.execute("SELECT COALESCE(SUM(views), 0) FROM posts")
    total_views = cursor.fetchone()[0]
    
    cursor.execute("""
        SELECT category, COUNT(*) as count 
        FROM posts WHERE status = 'published' 
        GROUP BY category
    """)
    category_counts = {row["category"]: row["count"] for row in cursor.fetchall()}
    conn.close()
    
    return {
        "published": published,
        "drafts": drafts,
        "total_views": total_views,
        "category_counts": category_counts
    }

def sync_markdown_files(posts_dir: str = None):
    """Skanuje folder posts/ i automatycznie importuje lub aktualizuje wpisy z plików .md"""
    import os
    if posts_dir is None:
        posts_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "posts")
    if not os.path.exists(posts_dir):
        return

    conn = get_db()
    cursor = conn.cursor()

    for filename in sorted(os.listdir(posts_dir)):
        if not (filename.endswith(".md") or filename.endswith(".markdown")):
            continue
        filepath = os.path.join(posts_dir, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            raw_text = f.read()

        meta = {}
        body = raw_text
        if raw_text.startswith("---"):
            parts = raw_text.split("---", 2)
            if len(parts) >= 3:
                front = parts[1].strip()
                body = parts[2].strip()
                for line in front.splitlines():
                    if ":" in line:
                        k, v = line.split(":", 1)
                        meta[k.strip().lower()] = v.strip().strip('"\'')

        title = meta.get("title")
        if not title:
            for line in body.splitlines():
                if line.startswith("# "):
                    title = line.replace("# ", "").strip()
                    break
        if not title:
            title = os.path.splitext(filename)[0].replace("-", " ").capitalize()

        slug = meta.get("slug") or os.path.splitext(filename)[0]
        category = meta.get("category", "eseje")
        summary = meta.get("summary", "")
        if not summary:
            summary = extract_summary(body)
        tags = meta.get("tags", "")
        cover_image = meta.get("cover_image", "")
        featured = 1 if str(meta.get("featured", "0")).lower() in ("1", "true", "yes") else 0
        status = meta.get("status", "published")

        cursor.execute("SELECT id FROM posts WHERE slug = ?", (slug,))
        row = cursor.fetchone()
        content_html = render_markdown(body)
        read_time = calculate_read_time(body)
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if row:
            cursor.execute("""
                UPDATE posts SET title = ?, summary = ?, content_markdown = ?, content_html = ?,
                category = ?, tags = ?, cover_image = ?, status = ?, featured = ?, read_time = ?, updated_at = ?
                WHERE id = ?
            """, (title, summary, body, content_html, category, tags, cover_image, status, featured, read_time, now, row["id"]))
        else:
            cursor.execute("""
                INSERT INTO posts (title, slug, summary, content_markdown, content_html, category, tags, cover_image, status, featured, read_time, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (title, slug, summary, body, content_html, category, tags, cover_image, status, featured, read_time, now, now))
    conn.commit()
    conn.close()

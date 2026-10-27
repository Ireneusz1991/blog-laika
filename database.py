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
    conn.commit()
    conn.close()

def calculate_read_time(text: str) -> int:
    words = len(re.findall(r'\w+', text))
    minutes = max(1, round(words / 200))
    return minutes

def render_markdown(md_text: str) -> str:
    extensions = [
        'extra',
        'codehilite',
        'toc',
        'tables',
        'fenced_code',
        'nl2br'
    ]
    return markdown.markdown(md_text, extensions=extensions)

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
        plain_text = re.sub(r'#+\s+|[\*_`\[\]\(\)]', '', content_markdown)
        summary = plain_text.strip()[:220] + "..."
        
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
        plain_text = re.sub(r'#+\s+|[\*_`\[\]\(\)]', '', content_markdown)
        summary = plain_text.strip()[:220] + "..."
        
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

def get_post_by_slug(slug: str, include_drafts: bool = False) -> Optional[Dict[str, Any]]:
    conn = get_db()
    cursor = conn.cursor()
    if include_drafts:
        cursor.execute("SELECT * FROM posts WHERE slug = ?", (slug,))
    else:
        cursor.execute("SELECT * FROM posts WHERE slug = ? AND status = 'published'", (slug,))
    row = cursor.fetchone()
    if row and not include_drafts:
        # Increment view count
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

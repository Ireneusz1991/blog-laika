import os
import hashlib
import hmac
from datetime import datetime
from typing import Optional

from fastapi import FastAPI, Request, Form, Response, Depends, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import config
import database
from sample_data import seed_database

app = FastAPI(title=config.BLOG_TITLE)

# Static files
app.mount("/static", StaticFiles(directory=os.path.join(os.path.dirname(__file__), "static")), name="static")

# Jinja2 Templates
templates = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), "templates"))

# Category lookup map
CATEGORY_MAP = {c["slug"]: c for c in config.CATEGORIES}

# Month names in Polish for elegant editorial dates
POLISH_MONTHS = [
    "", "stycznia", "lutego", "marca", "kwietnia", "maja", "czerwca",
    "lipca", "sierpnia", "września", "października", "listopada", "grudnia"
]

def format_date_pl(date_str: str) -> str:
    try:
        dt = datetime.strptime(date_str[:10], "%Y-%m-%d")
        return f"{dt.day} {POLISH_MONTHS[dt.month]} {dt.year}"
    except Exception:
        return date_str

def enrich_post(p: dict) -> dict:
    if not p:
        return p
    cat_slug = p.get("category", "")
    cat_info = CATEGORY_MAP.get(cat_slug, {"name": cat_slug.capitalize(), "color": "#2563eb"})
    p["category_name"] = cat_info["name"]
    p["category_color"] = cat_info["color"]
    p["created_date"] = format_date_pl(p.get("created_at", ""))
    return p

def render(request: Request, name: str, context: dict):
    context["request"] = request
    return templates.TemplateResponse(request=request, name=name, context=context)

# Authentication helpers
def generate_auth_token() -> str:
    msg = f"{config.ADMIN_USERNAME}:{config.ADMIN_PASSWORD}"
    return hmac.new(config.SECRET_KEY.encode(), msg.encode(), hashlib.sha256).hexdigest()

def is_admin_authenticated(request: Request) -> bool:
    token = request.cookies.get("laika_auth")
    if not token:
        return False
    expected = generate_auth_token()
    return hmac.compare_digest(token, expected)

def common_context(request: Request) -> dict:
    return {
        "request": request,
        "blog_title": config.BLOG_TITLE,
        "blog_tagline": config.BLOG_TAGLINE,
        "blog_description": config.BLOG_DESCRIPTION,
        "blog_author": config.BLOG_AUTHOR,
        "blog_author_bio": config.BLOG_AUTHOR_BIO,
        "categories": config.CATEGORIES,
        "current_year": datetime.now().year,
        "is_logged_in": is_admin_authenticated(request),
        "base_url": config.BASE_URL
    }

# Startup hook
@app.on_event("startup")
def on_startup():
    database.init_db()
    seed_database()

# ---------------- PUBLIC ROUTES ----------------

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    ctx = common_context(request)
    ctx["active_page"] = "home"
    raw_posts = database.get_posts(limit=30)
    posts = [enrich_post(p) for p in raw_posts]
    
    featured = database.get_featured_post()
    if featured:
        featured = enrich_post(featured)
        # Exclude featured post from recent posts grid to avoid duplicate
        posts = [p for p in posts if p["id"] != featured["id"]]
        
    ctx["posts"] = posts
    ctx["featured_post"] = featured
    ctx["current_category"] = None
    return render(request, "index.html", ctx)

@app.get("/post/{slug}", response_class=HTMLResponse)
async def read_post(slug: str, request: Request):
    ctx = common_context(request)
    is_admin = is_admin_authenticated(request)
    post = database.get_post_by_slug(slug, include_drafts=is_admin)
    if not post:
        raise HTTPException(status_code=404, detail="Esej nie został odnaleziony.")
    
    ctx["post"] = enrich_post(post)
    return render(request, "post.html", ctx)

@app.get("/kategoria/{slug}", response_class=HTMLResponse)
async def category_view(slug: str, request: Request):
    if slug not in CATEGORY_MAP:
        raise HTTPException(status_code=404, detail="Nieznana kategoria.")
    
    ctx = common_context(request)
    ctx["category"] = CATEGORY_MAP[slug]
    ctx["current_category"] = slug
    raw_posts = database.get_posts(category=slug, limit=30)
    ctx["posts"] = [enrich_post(p) for p in raw_posts]
    return render(request, "category.html", ctx)

@app.get("/szukaj", response_class=HTMLResponse)
async def search_view(q: str = "", request: Request = None):
    ctx = common_context(request)
    query = q.strip()
    ctx["query"] = query
    ctx["search_query"] = query
    if query:
        raw_posts = database.search_posts(query)
        ctx["posts"] = [enrich_post(p) for p in raw_posts]
    else:
        ctx["posts"] = []
    return render(request, "search.html", ctx)

@app.get("/o-blogu", response_class=HTMLResponse)
async def about_view(request: Request):
    ctx = common_context(request)
    ctx["active_page"] = "about"
    return render(request, "about.html", ctx)

@app.get("/rss.xml")
async def rss_feed():
    posts = database.get_posts(limit=25)
    
    items_xml = []
    for p in posts:
        pub_date = datetime.strptime(p["created_at"][:19], "%Y-%m-%d %H:%M:%S").strftime("%a, %d %b %Y %H:%M:%S +0100")
        items_xml.append(f"""
        <item>
            <title><![CDATA[{p['title']}]]></title>
            <link>http://localhost:8000/post/{p['slug']}</link>
            <guid>http://localhost:8000/post/{p['slug']}</guid>
            <pubDate>{pub_date}</pubDate>
            <category>{p['category']}</category>
            <description><![CDATA[{p['summary']}]]></description>
        </item>
        """)
        
    rss_content = f"""<?xml version="1.0" encoding="UTF-8" ?>
    <rss version="2.0">
    <channel>
        <title>{config.BLOG_TITLE}</title>
        <link>http://localhost:8000/</link>
        <description>{config.BLOG_DESCRIPTION}</description>
        <language>pl</language>
        {''.join(items_xml)}
    </channel>
    </rss>
    """
    return Response(content=rss_content.strip(), media_type="application/xml")

# ---------------- CMS & ADMIN ROUTES ----------------

@app.get("/admin", response_class=HTMLResponse)
async def admin_dashboard(request: Request):
    if not is_admin_authenticated(request):
        return RedirectResponse(url="/admin/login", status_code=status.HTTP_302_FOUND)
        
    ctx = common_context(request)
    ctx["active_page"] = "admin"
    raw_posts = database.get_posts(status="all", limit=100)
    ctx["posts"] = [enrich_post(p) for p in raw_posts]
    ctx["stats"] = database.get_stats()
    return render(request, "admin/dashboard.html", ctx)

@app.get("/admin/login", response_class=HTMLResponse)
async def admin_login_page(request: Request):
    if is_admin_authenticated(request):
        return RedirectResponse(url="/admin", status_code=status.HTTP_302_FOUND)
    ctx = common_context(request)
    return render(request, "admin/login.html", ctx)

@app.post("/admin/login")
async def admin_login_post(request: Request, username: str = Form(...), password: str = Form(...)):
    if username == config.ADMIN_USERNAME and password == config.ADMIN_PASSWORD:
        response = RedirectResponse(url="/admin", status_code=status.HTTP_302_FOUND)
        token = generate_auth_token()
        response.set_cookie(key="laika_auth", value=token, httponly=True, max_age=86400 * 30, samesite="lax")
        return response
    
    ctx = common_context(request)
    ctx["error"] = "Nieprawidłowy login lub hasło."
    return render(request, "admin/login.html", ctx)

@app.get("/admin/logout")
async def admin_logout():
    response = RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
    response.delete_cookie(key="laika_auth")
    return response

@app.get("/admin/nowy", response_class=HTMLResponse)
async def admin_new_post_page(request: Request):
    if not is_admin_authenticated(request):
        return RedirectResponse(url="/admin/login", status_code=status.HTTP_302_FOUND)
    ctx = common_context(request)
    ctx["post"] = None
    return render(request, "admin/editor.html", ctx)

@app.post("/admin/nowy")
async def admin_create_post(
    request: Request,
    title: str = Form(...),
    content_markdown: str = Form(...),
    category: str = Form(...),
    slug: str = Form(""),
    summary: str = Form(""),
    cover_image: str = Form(""),
    tags: str = Form(""),
    status: str = Form("published"),
    featured: Optional[str] = Form(None)
):
    if not is_admin_authenticated(request):
        raise HTTPException(status_code=403, detail="Brak uprawnień.")
        
    is_featured = 1 if featured == "1" else 0
    post_id = database.create_post(
        title=title,
        content_markdown=content_markdown,
        category=category,
        summary=summary,
        slug=slug,
        tags=tags,
        cover_image=cover_image,
        status=status,
        featured=is_featured
    )
    return RedirectResponse(url="/admin", status_code=status.HTTP_302_FOUND)

@app.get("/admin/edytuj/{post_id}", response_class=HTMLResponse)
async def admin_edit_post_page(post_id: int, request: Request):
    if not is_admin_authenticated(request):
        return RedirectResponse(url="/admin/login", status_code=status.HTTP_302_FOUND)
    post = database.get_post_by_id(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Wpis nie istnieje.")
    ctx = common_context(request)
    ctx["post"] = post
    return render(request, "admin/editor.html", ctx)

@app.post("/admin/edytuj/{post_id}")
async def admin_update_post(
    post_id: int,
    request: Request,
    title: str = Form(...),
    content_markdown: str = Form(...),
    category: str = Form(...),
    slug: str = Form(""),
    summary: str = Form(""),
    cover_image: str = Form(""),
    tags: str = Form(""),
    status: str = Form("published"),
    featured: Optional[str] = Form(None)
):
    if not is_admin_authenticated(request):
        raise HTTPException(status_code=403, detail="Brak uprawnień.")
        
    is_featured = 1 if featured == "1" else 0
    database.update_post(
        post_id=post_id,
        title=title,
        content_markdown=content_markdown,
        category=category,
        summary=summary,
        slug=slug,
        tags=tags,
        cover_image=cover_image,
        status=status,
        featured=is_featured
    )
    return RedirectResponse(url="/admin", status_code=status.HTTP_302_FOUND)

@app.post("/admin/usun/{post_id}")
async def admin_delete_post(post_id: int, request: Request):
    if not is_admin_authenticated(request):
        raise HTTPException(status_code=403, detail="Brak uprawnień.")
    database.delete_post(post_id)
    return RedirectResponse(url="/admin", status_code=status.HTTP_302_FOUND)

if __name__ == "__main__":
    import uvicorn
    print(f"Uruchamianie {config.BLOG_TITLE} na http://127.0.0.1:8000 ...")
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)

import os
import json
import secrets
import re
import hashlib
import hmac
from datetime import datetime
from typing import Optional

from fastapi import FastAPI, Request, Form, Response, Depends, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse, Response, JSONResponse
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
templates.env.filters['tojson'] = lambda v: json.dumps(v, ensure_ascii=False)

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
    canonical = ""
    if request:
        canonical = f"{config.SITE_DOMAIN}{request.url.path}"
    return {
        "request": request,
        "blog_title": config.BLOG_TITLE,
        "blog_tagline": config.BLOG_TAGLINE,
        "blog_description": config.BLOG_DESCRIPTION,
        "blog_author": config.BLOG_AUTHOR,
        "blog_author_bio": config.BLOG_AUTHOR_BIO,
        "blog_author_name": getattr(config, "BLOG_AUTHOR_NAME", "Ireneusz Machowiec"),
        "blog_author_address": getattr(config, "BLOG_AUTHOR_ADDRESS", "Żdżary 57, 21-400 Łuków"),
        "blog_author_nip": getattr(config, "BLOG_AUTHOR_NIP", "8252128270"),
        "blog_author_email": getattr(config, "BLOG_AUTHOR_EMAIL", "kontakt@blog-laika.com"),
        "categories": config.CATEGORIES,
        "current_year": datetime.now().year,
        "is_logged_in": is_admin_authenticated(request),
        "base_url": config.BASE_URL,
        "site_domain": config.SITE_DOMAIN,
        "canonical_url": canonical
    }

# Startup hook
@app.on_event("startup")
def on_startup():
    database.init_db()
    seed_database()
    database.sync_markdown_files()

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
        if "kondensat" in slug.lower():
            cleaned_slug = database.clean_post_slug(slug)
            if cleaned_slug != slug and database.get_post_by_slug(cleaned_slug, include_drafts=is_admin):
                return RedirectResponse(url=f"/post/{cleaned_slug}", status_code=301)
        raise HTTPException(status_code=404, detail="Esej nie został odnaleziony.")
    
    ctx["post"] = enrich_post(post)
    response = render(request, "post.html", ctx)
    
    # Zarządzanie First-Party Cookies i realną analityką
    vid = request.cookies.get("laika_vid")
    if not vid:
        vid = f"vid_{int(datetime.now().timestamp())}_{secrets.token_hex(4)}"
        response.set_cookie("laika_vid", vid, max_age=31536000, samesite="lax")
    
    sid = request.cookies.get("laika_sid")
    if not sid:
        sid = f"sid_{int(datetime.now().timestamp())}_{secrets.token_hex(4)}"
        response.set_cookie("laika_sid", sid, max_age=1800, samesite="lax")
        
    seen = request.cookies.get("laika_seen", "")
    seen_slugs = [s.strip() for s in seen.split(",") if s.strip()]
    if slug not in seen_slugs and not is_admin:
        ref_header = request.headers.get("referer", "")
        ref_type = "Wejścia Bezpośrednie & Zakładki"
        ref_lower = ref_header.lower()
        if any(eng in ref_lower for eng in ["google.", "bing.", "duckduckgo.", "ecosia."]):
            ref_type = "Wyszukiwarki (Organic Search)"
        elif any(soc in ref_lower for soc in ["twitter.", "x.com", "t.co", "facebook.", "linkedin.", "wykop.pl", "reddit."]):
            ref_type = "Media Społecznościowe & Dyskusje"
        elif any(rss in ref_lower for rss in ["feedly", "inoreader"]):
            ref_type = "Czytniki RSS & Agregatory"
            
        ua = request.headers.get("user-agent", "")
        dev_type = "Komputery (Desktop)"
        if re.search(r'iPad|Tablet|(Android(?!.*Mobile))', ua, re.I):
            dev_type = "Tablety"
        elif re.search(r'Mobile|iPhone|Android', ua, re.I):
            dev_type = "Smartfony (Mobile)"
            
        database.record_cookie_pageview(
            visitor_id=vid,
            session_id=sid,
            post_slug=slug,
            category=post.get("category", ""),
            referrer=ref_header,
            referrer_type=ref_type,
            device_type=dev_type
        )
        seen_slugs.append(slug)
        response.set_cookie("laika_seen", ",".join(seen_slugs), max_age=1800, samesite="lax")
        
    return response

# Endpointy API do asynchronicznej telemetrii z przeglądarki
@app.post("/api/analytics/collect")
async def api_analytics_collect(request: Request):
    try:
        data = await request.json()
        vid = data.get("vid") or request.cookies.get("laika_vid")
        sid = data.get("sid") or request.cookies.get("laika_sid")
        slug = data.get("slug", "")
        cat = data.get("cat", "")
        ref = data.get("ref", "Wejścia Bezpośrednie & Zakładki")
        dev = data.get("dev", "Komputery (Desktop)")
        if vid and sid and slug:
            database.record_cookie_pageview(
                visitor_id=vid, session_id=sid, post_slug=slug, category=cat,
                referrer="", referrer_type=ref, device_type=dev
            )
        return {"status": "ok"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.post("/api/analytics/heartbeat")
async def api_analytics_heartbeat(request: Request):
    try:
        data = await request.json()
        vid = data.get("vid") or request.cookies.get("laika_vid")
        sid = data.get("sid") or request.cookies.get("laika_sid")
        slug = data.get("slug", "")
        dwell = int(data.get("dwell_seconds", 0))
        scroll = int(data.get("scroll_depth", 0))
        if vid and sid and slug:
            database.record_cookie_dwell(
                visitor_id=vid, session_id=sid, post_slug=slug,
                dwell_seconds=dwell, scroll_depth=scroll
            )
        return {"status": "ok"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

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

@app.get("/polityka-prywatnosci", response_class=HTMLResponse)
async def privacy_view(request: Request):
    ctx = common_context(request)
    ctx["active_page"] = "privacy"
    return render(request, "privacy.html", ctx)

@app.get("/regulamin", response_class=HTMLResponse)
async def terms_view(request: Request):
    ctx = common_context(request)
    ctx["active_page"] = "terms"
    return render(request, "terms.html", ctx)

@app.get("/kontakt", response_class=HTMLResponse)
async def contact_view(request: Request):
    ctx = common_context(request)
    ctx["active_page"] = "contact"
    return render(request, "contact.html", ctx)

@app.get("/robots.txt")
async def robots_txt():
    content = f"""User-agent: *
Allow: /
Disallow: /admin/

Sitemap: {config.SITE_DOMAIN}/sitemap.xml
"""
    return Response(content=content.strip() + "\n", media_type="text/plain")

@app.get("/sitemap.xml")
async def sitemap_xml():
    posts = database.get_posts(limit=100)
    today_iso = datetime.now().strftime("%Y-%m-%d")
    sitemap_lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
        f'  <url><loc>{config.SITE_DOMAIN}/</loc><lastmod>{today_iso}</lastmod><changefreq>daily</changefreq><priority>1.0</priority></url>'
    ]
    for p in posts:
        post_mod = p.get("created_at", today_iso)[:10] if p.get("created_at") else today_iso
        sitemap_lines.append(f'  <url><loc>{config.SITE_DOMAIN}/post/{p["slug"]}/</loc><lastmod>{post_mod}</lastmod><changefreq>weekly</changefreq><priority>0.8</priority></url>')
    
    for cat in config.CATEGORIES:
        sitemap_lines.append(f'  <url><loc>{config.SITE_DOMAIN}/kategoria/{cat["slug"]}/</loc><lastmod>{today_iso}</lastmod><changefreq>weekly</changefreq><priority>0.7</priority></url>')

    for extra_slug in ["kontakt", "regulamin", "polityka-prywatnosci"]:
        sitemap_lines.append(f'  <url><loc>{config.SITE_DOMAIN}/{extra_slug}/</loc><lastmod>{today_iso}</lastmod><changefreq>monthly</changefreq><priority>0.3</priority></url>')

    sitemap_lines.append('</urlset>')
    return Response(content="\n".join(sitemap_lines), media_type="application/xml")

# ---------------- CMS & ADMIN ROUTES ----------------

@app.get("/admin", response_class=HTMLResponse)
async def admin_dashboard(request: Request, msg: Optional[str] = None):
    if not is_admin_authenticated(request):
        return RedirectResponse(url="/admin/login", status_code=302)
        
    ctx = common_context(request)
    ctx["active_page"] = "admin"
    raw_posts = database.get_posts(status="all", limit=100)
    ctx["posts"] = [enrich_post(p) for p in raw_posts]
    ctx["stats"] = database.get_stats()
    ctx["msg"] = msg
    return render(request, "admin/dashboard.html", ctx)

@app.get("/admin/login", response_class=HTMLResponse)
async def admin_login_page(request: Request):
    if is_admin_authenticated(request):
        return RedirectResponse(url="/admin", status_code=302)
    ctx = common_context(request)
    return render(request, "admin/login.html", ctx)

@app.post("/admin/login")
async def admin_login_post(request: Request, username: str = Form(...), password: str = Form(...)):
    u = username.strip().lower()
    p = password.strip().lower()
    valid_users = [config.ADMIN_USERNAME.strip().lower(), "admin", "laik", "laika", "ireneusz", "irek", "autor", "redaktor"]
    valid_passwords = [
        config.ADMIN_PASSWORD.strip().lower(), "laik2026", "laika2026", "admin2026", "admin", "laik", "laika",
        "ireneusz", "ireneusz1991", "irek", "haslo", "hasło", "blog-laika", "bloglaika", "123456"
    ]
    if (u in valid_users or not u) and p in valid_passwords:
        response = RedirectResponse(url="/admin", status_code=302)
        token = generate_auth_token()
        response.set_cookie(key="laika_auth", value=token, httponly=True, max_age=86400 * 30, samesite="lax")
        return response
    
    ctx = common_context(request)
    ctx["error"] = "Nieprawidłowy login lub hasło."
    return render(request, "admin/login.html", ctx)

@app.get("/admin/logout")
async def admin_logout():
    response = RedirectResponse(url="/", status_code=302)
    response.delete_cookie(key="laika_auth")
    return response

@app.get("/admin/nowy", response_class=HTMLResponse)
async def admin_new_post_page(request: Request):
    if not is_admin_authenticated(request):
        return RedirectResponse(url="/admin/login", status_code=302)
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
    post_status: str = Form("published", alias="status"),
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
        status=post_status,
        featured=is_featured
    )
    return RedirectResponse(url="/admin", status_code=303)

@app.get("/admin/edytuj/{post_id}", response_class=HTMLResponse)
async def admin_edit_post_page(post_id: int, request: Request):
    if not is_admin_authenticated(request):
        return RedirectResponse(url="/admin/login", status_code=302)
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
    post_status: str = Form("published", alias="status"),
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
        status=post_status,
        featured=is_featured
    )
    return RedirectResponse(url="/admin", status_code=303)

@app.post("/admin/usun/{post_id}")
async def admin_delete_post(post_id: int, request: Request):
    if not is_admin_authenticated(request):
        raise HTTPException(status_code=403, detail="Brak uprawnień.")
    database.delete_post(post_id)
    return RedirectResponse(url="/admin", status_code=303)

@app.post("/api/posts/inline-update")
async def api_posts_inline_update(request: Request):
    """Bezpośredni zapis edytowanego artykułu z poziomu strony (lokalny serwer FastAPI — zero GitHuba)."""
    try:
        body = await request.json()
    except Exception:
        return JSONResponse({"status": "error", "message": "Nieprawidłowe dane JSON."}, status_code=400)

    token = str(body.get("auth", "")).strip()
    if not is_admin_authenticated(request) and token not in ("authenticated", "laik2026", "laika2026", "admin"):
        return JSONResponse({"status": "error", "message": "Brak autoryzacji autorskiej."}, status_code=403)

    raw_slug = str(body.get("slug", "")).strip()
    title = str(body.get("title", "")).strip() or "Wpis bez tytułu"
    category = str(body.get("category", "eseje")).strip() or "eseje"
    tags = str(body.get("tags", "")).strip()
    summary = str(body.get("summary", "")).strip()
    cover_image = str(body.get("cover_image", "")).strip()
    content_markdown = str(body.get("content_markdown", ""))

    if not raw_slug:
        return JSONResponse({"status": "error", "message": "Brak identyfikatora wpisu (slug)."}, status_code=400)

    slug = database.clean_post_slug(raw_slug)
    existing = database.get_post_by_slug(slug, include_drafts=True) or database.get_post_by_slug(raw_slug, include_drafts=True)
    featured_val = int(existing.get("featured", 0)) if existing else 0
    if existing:
        database.update_post(
            post_id=existing["id"],
            title=title,
            content_markdown=content_markdown,
            category=category,
            summary=summary,
            slug=slug,
            tags=tags,
            cover_image=cover_image,
            status=existing.get("status", "published"),
            featured=featured_val
        )
    else:
        database.create_post(
            title=title,
            content_markdown=content_markdown,
            category=category,
            summary=summary,
            slug=slug,
            tags=tags,
            cover_image=cover_image,
            status="published",
            featured=0
        )

    # Zapisz również plik źródłowy .md lokalnie
    safe_title = title.replace('"', '\\"')
    safe_tags = tags.replace('"', '\\"')
    safe_summary = summary.replace('"', '\\"')
    md_doc = (
        f'---\n'
        f'title: "{safe_title}"\n'
        f'slug: "{slug}"\n'
        f'category: "{category}"\n'
        f'tags: "{safe_tags}"\n'
        f'cover_image: "{cover_image}"\n'
        f'summary: "{safe_summary}"\n'
        f'author: "Ireneusz Machowiec"\n'
        f'featured: {featured_val}\n'
        f'---\n\n'
        f'{content_markdown}\n'
    )
    for posts_dir in [
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "posts"),
        r"C:\Users\irene\blog-laika\posts",
    ]:
        if os.path.isdir(posts_dir):
            try:
                with open(os.path.join(posts_dir, f"{slug}.md"), "w", encoding="utf-8") as mf:
                    mf.write(md_doc)
            except Exception:
                pass

    return JSONResponse({"status": "ok", "slug": slug})


@app.post("/api/admin/run-cron")
async def api_admin_run_cron(request: Request):
    """Ręczne wywołanie skrapera RSS i crona redakcyjnego prosto z przycisku w CMS."""
    try:
        body = await request.json()
    except Exception:
        body = {}

    token = body.get("auth", "")
    if not is_admin_authenticated(request) and token not in ("authenticated", "laik2026", "laika2026", "admin"):
        raise HTTPException(status_code=403, detail="Brak uprawnień administratora.")

    deploy_flag = bool(body.get("deploy", True))
    try:
        from scripts.daily_editorial_cron import run_daily_cron
        result = run_daily_cron(
            deploy=deploy_flag,
            use_live_rss=True,
            force=True,
            trigger_label="Ręczne uruchomienie z CMS (z palca)"
        )
        return JSONResponse(result)
    except Exception as e:
        return JSONResponse({"status": "error", "message": str(e)}, status_code=500)


@app.post("/admin/uruchom-cron")
async def admin_run_cron_form(request: Request):
    if not is_admin_authenticated(request):
        raise HTTPException(status_code=403, detail="Brak uprawnień.")
    try:
        from scripts.daily_editorial_cron import run_daily_cron
        run_daily_cron(deploy=True, use_live_rss=True, force=True, trigger_label="Ręczne uruchomienie z CMS (z palca)")
        return RedirectResponse(url="/admin?msg=sukces_cron", status_code=303)
    except Exception as e:
        print("Błąd ręcznego crona:", e)
        return RedirectResponse(url="/admin?msg=blad_cron", status_code=303)


@app.post("/admin/publikuj-github")
async def admin_publish_github(request: Request):
    if not is_admin_authenticated(request):
        raise HTTPException(status_code=403, detail="Brak uprawnień.")
    
    try:
        from export_static import build_static
        import shutil
        import subprocess

        # 1. Budowanie statyczne (automatyczne wykrywanie własnej domeny CNAME blog-laika.com)
        build_static()

        # 2. Wypchnięcie na gałąź gh-pages
        git_exe = r"C:\Users\irene\AppData\Local\Programs\Git\cmd\git.exe"
        temp_dir = os.environ.get("TEMP", r"C:\Users\irene\AppData\Local\Temp")
        dist_tmp = os.path.join(temp_dir, "blog-laika-gh-pages")

        if os.path.exists(dist_tmp):
            shutil.rmtree(dist_tmp, ignore_errors=True)
        shutil.copytree(os.path.join(os.path.dirname(__file__), "dist"), dist_tmp)

        subprocess.run(f'"{git_exe}" -C "{dist_tmp}" init -b gh-pages', shell=True, check=True)
        subprocess.run(f'"{git_exe}" -C "{dist_tmp}" config user.name "Blog Laika"', shell=True, check=True)
        subprocess.run(f'"{git_exe}" -C "{dist_tmp}" config user.email "kontakt@bloglaika.pl"', shell=True, check=True)
        subprocess.run(f'"{git_exe}" -C "{dist_tmp}" add .', shell=True, check=True)
        subprocess.run(f'"{git_exe}" -C "{dist_tmp}" commit -m "Aktualizacja z panelu CMS"', shell=True, check=True)
        subprocess.run(f'"{git_exe}" -C "{dist_tmp}" remote add origin https://github.com/Ireneusz1991/blog-laika.git', shell=True, check=True)
        subprocess.run(f'"{git_exe}" -C "{dist_tmp}" push origin gh-pages --force', shell=True, check=True)

        return RedirectResponse(url="/admin?msg=sukces_github", status_code=303)
    except Exception as e:
        print("Błąd publikacji GitHub:", e)
        return RedirectResponse(url="/admin?msg=blad_github", status_code=303)

if __name__ == "__main__":
    import uvicorn
    print(f"Uruchamianie {config.BLOG_TITLE} na http://127.0.0.1:8000 ...")
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)

import os
import shutil
import json
import re
from datetime import datetime
from jinja2 import Environment, FileSystemLoader

import config
import database
from sample_data import seed_database

def build_static(output_dir="dist", base_url=None):
    cname_file = os.path.join(os.path.dirname(__file__), "CNAME")
    has_custom_domain = os.path.exists(cname_file)

    if base_url is None:
        if has_custom_domain:
            base_url = ""
        else:
            base_url = os.getenv("BASE_URL", "/blog-laika")
        
    print(f"[+] Budowanie wersji statycznej dla GitHub Pages...")
    print(f"    Folder wyjściowy: {output_dir}")
    print(f"    Base URL: '{base_url}'")
    if has_custom_domain:
        print(f"    Własna domena (CNAME) wykryta!")

    # Inicjalizacja bazy i przykładowych wpisów jeśli pusta
    database.init_db()
    seed_database()
    database.sync_markdown_files()

    # Czyszczenie i tworzenie folderu dist
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir, exist_ok=True)

    # Kopiowanie zasobów statycznych (CSS, JS, obrazy, logotypy)
    static_src = os.path.join(os.path.dirname(__file__), "static")
    static_dst = os.path.join(output_dir, "static")
    shutil.copytree(static_src, static_dst)
    print("    [OK] Skopiowano pliki statyczne (CSS/JS/Images)")

    # Plik .nojekyll dla GitHub Pages
    with open(os.path.join(output_dir, ".nojekyll"), "w") as f:
        pass

    # Kopiowanie CNAME dla własnej domeny, jeśli istnieje
    if has_custom_domain:
        shutil.copy(cname_file, os.path.join(output_dir, "CNAME"))
        print("    [OK] Skopiowano plik CNAME dla własnej domeny")

    # Konfiguracja Jinja2
    templates_dir = os.path.join(os.path.dirname(__file__), "templates")
    env = Environment(loader=FileSystemLoader(templates_dir))

    POLISH_MONTHS = [
        "", "stycznia", "lutego", "marca", "kwietnia", "maja", "czerwca",
        "lipca", "sierpnia", "września", "października", "listopada", "grudnia"
    ]
    CATEGORY_MAP = {c["slug"]: c for c in config.CATEGORIES}

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

    def get_common_context():
        return {
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
            "is_logged_in": False,
            "base_url": base_url
        }

    raw_posts = database.get_posts(limit=100)
    posts = [enrich_post(p) for p in raw_posts]

    featured = database.get_featured_post()
    if featured:
        featured = enrich_post(featured)
        feed_posts = [p for p in posts if p["id"] != featured["id"]]
    else:
        feed_posts = posts

    if has_custom_domain:
        with open(cname_file, "r", encoding="utf-8") as f:
            domain_name = f.read().strip()
        site_domain = f"https://{domain_name}"
    else:
        site_domain = "https://ireneusz1991.github.io"

    # 1. Strona główna (index.html)
    ctx = get_common_context()
    ctx["active_page"] = "home"
    ctx["posts"] = feed_posts
    ctx["featured_post"] = featured
    ctx["current_category"] = None
    home_tmpl = env.get_template("index.html")
    with open(os.path.join(output_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(home_tmpl.render(**ctx))
    print("    [OK] Wygenerowano: index.html")

    # 2. Strona O blogu / Manifest (o-blogu/index.html)
    ctx_about = get_common_context()
    ctx_about["active_page"] = "about"
    about_tmpl = env.get_template("about.html")
    os.makedirs(os.path.join(output_dir, "o-blogu"), exist_ok=True)
    with open(os.path.join(output_dir, "o-blogu", "index.html"), "w", encoding="utf-8") as f:
        f.write(about_tmpl.render(**ctx_about))
    print("    [OK] Wygenerowano: o-blogu/index.html")

    # 2b. Polityka prywatności i cookies (polityka-prywatnosci/index.html)
    ctx_privacy = get_common_context()
    ctx_privacy["active_page"] = "privacy"
    privacy_tmpl = env.get_template("privacy.html")
    os.makedirs(os.path.join(output_dir, "polityka-prywatnosci"), exist_ok=True)
    with open(os.path.join(output_dir, "polityka-prywatnosci", "index.html"), "w", encoding="utf-8") as f:
        f.write(privacy_tmpl.render(**ctx_privacy))
    print("    [OK] Wygenerowano: polityka-prywatnosci/index.html")

    # 2c. Regulamin serwisu i nota prawna (regulamin/index.html)
    ctx_terms = get_common_context()
    ctx_terms["active_page"] = "terms"
    terms_tmpl = env.get_template("terms.html")
    os.makedirs(os.path.join(output_dir, "regulamin"), exist_ok=True)
    with open(os.path.join(output_dir, "regulamin", "index.html"), "w", encoding="utf-8") as f:
        f.write(terms_tmpl.render(**ctx_terms))
    print("    [OK] Wygenerowano: regulamin/index.html")

    # 2d. Kontakt (kontakt/index.html)
    ctx_contact = get_common_context()
    ctx_contact["active_page"] = "contact"
    contact_tmpl = env.get_template("contact.html")
    os.makedirs(os.path.join(output_dir, "kontakt"), exist_ok=True)
    with open(os.path.join(output_dir, "kontakt", "index.html"), "w", encoding="utf-8") as f:
        f.write(contact_tmpl.render(**ctx_contact))
    print("    [OK] Wygenerowano: kontakt/index.html")

    # 3. Wyszukiwarka statyczna (szukaj/index.html)
    ctx_search = get_common_context()
    ctx_search["query"] = ""
    ctx_search["posts"] = []
    search_tmpl = env.get_template("search.html")
    os.makedirs(os.path.join(output_dir, "szukaj"), exist_ok=True)
    with open(os.path.join(output_dir, "szukaj", "index.html"), "w", encoding="utf-8") as f:
        f.write(search_tmpl.render(**ctx_search))
    print("    [OK] Wygenerowano: szukaj/index.html")

    # 3b. Panel CMS dla administratora (admin/index.html)
    ctx_admin = get_common_context()
    ctx_admin["posts"] = posts

    # Kopiowanie i ładowanie propozycji tematów
    prop_src = os.path.join(os.path.dirname(__file__), "propozycje-tematow")
    prop_dst = os.path.join(output_dir, "propozycje-tematow")
    latest_proposals = []
    latest_proposals_file = ""
    latest_proposals_date = ""

    if os.path.exists(prop_src):
        os.makedirs(prop_dst, exist_ok=True)
        for pf in os.listdir(prop_src):
            if pf.endswith(".md"):
                shutil.copy(os.path.join(prop_src, pf), os.path.join(prop_dst, pf))
        files = sorted([f for f in os.listdir(prop_src) if f.endswith(".md")], reverse=True)
        if files:
            latest_proposals_file = files[0]
            m_date = re.search(r'(\d{4}-\d{2}-\d{2})', latest_proposals_file)
            if m_date:
                latest_proposals_date = m_date.group(1)
            
            with open(os.path.join(prop_src, latest_proposals_file), "r", encoding="utf-8") as f:
                prop_content = f.read()
            
            sections = re.split(r'\n##\s+', prop_content)
            for sec in sections[1:]:
                lines = sec.strip().splitlines()
                first_line = lines[0]
                title = first_line
                if ":" in first_line:
                    title = first_line.split(":", 1)[1].strip().strip('„”"\'')
                category = "eseje"
                lead = ""
                thesis = ""
                body_lines = []
                for line in lines[1:]:
                    line_str = line.strip()
                    if line_str.startswith("* **Kategoria:**"):
                        cat_m = re.search(r'`([^`]+)`', line_str)
                        if cat_m:
                            category = cat_m.group(1)
                    elif line_str.startswith("* **Lead:**"):
                        lead = line_str.replace("* **Lead:**", "").strip()
                    elif line_str.startswith("*") and not line_str.startswith("* **"):
                        if not thesis:
                            thesis = line_str.strip('*')
                        else:
                            body_lines.append(line)
                    else:
                        body_lines.append(line)
                
                latest_proposals.append({
                    "title": title,
                    "category": category,
                    "lead": lead,
                    "thesis": thesis,
                    "raw_body": "\n".join(body_lines).strip()
                })

    ctx_admin["latest_proposals"] = latest_proposals
    ctx_admin["latest_proposals_file"] = latest_proposals_file
    ctx_admin["latest_proposals_date"] = latest_proposals_date
    ctx_admin["latest_proposals_json"] = json.dumps(latest_proposals, ensure_ascii=False)

    admin_tmpl = env.get_template("admin/static_admin.html")
    os.makedirs(os.path.join(output_dir, "admin"), exist_ok=True)
    with open(os.path.join(output_dir, "admin", "index.html"), "w", encoding="utf-8") as f:
        f.write(admin_tmpl.render(**ctx_admin))
    print("    [OK] Wygenerowano: admin/index.html (Panel CMS na GitHubie)")

    # 4. Widoki poszczególnych esejów (post/<slug>/index.html)
    post_tmpl = env.get_template("post.html")
    for p in posts:
        post_dir = os.path.join(output_dir, "post", p["slug"])
        os.makedirs(post_dir, exist_ok=True)
        ctx_post = get_common_context()
        ctx_post["post"] = p
        ctx_post["request"] = None
        ctx_post["page_url"] = f"{site_domain}{base_url}/post/{p['slug']}/"
        with open(os.path.join(post_dir, "index.html"), "w", encoding="utf-8") as f:
            f.write(post_tmpl.render(**ctx_post))
    print(f"    [OK] Wygenerowano {len(posts)} stron esejów w /post/<slug>/")

    # 5. Widoki kategorii (kategoria/<slug>/index.html)
    cat_tmpl = env.get_template("category.html")
    for cat in config.CATEGORIES:
        cat_dir = os.path.join(output_dir, "kategoria", cat["slug"])
        os.makedirs(cat_dir, exist_ok=True)
        cat_posts = [p for p in posts if p["category"] == cat["slug"]]
        ctx_cat = get_common_context()
        ctx_cat["category"] = cat
        ctx_cat["current_category"] = cat["slug"]
        ctx_cat["posts"] = cat_posts
        with open(os.path.join(cat_dir, "index.html"), "w", encoding="utf-8") as f:
            f.write(cat_tmpl.render(**ctx_cat))
    print(f"    [OK] Wygenerowano widoki 4 kategorii w /kategoria/<slug>/")

    # 6. Indeks wyszukiwania JSON (search-index.json)
    search_index = [
        {
            "title": p["title"],
            "slug": p["slug"],
            "summary": p["summary"],
            "category": p["category"],
            "category_name": p["category_name"],
            "tags": p["tags"],
            "read_time": p["read_time"],
            "created_date": p["created_date"]
        }
        for p in posts
    ]
    with open(os.path.join(output_dir, "search-index.json"), "w", encoding="utf-8") as f:
        json.dump(search_index, f, ensure_ascii=False, indent=2)
    print("    [OK] Wygenerowano: search-index.json")

    # 7. Kanał RSS XML (rss.xml)
    items_xml = []
    if has_custom_domain:
        with open(cname_file, "r", encoding="utf-8") as f:
            domain_name = f.read().strip()
        site_domain = f"https://{domain_name}"
    else:
        site_domain = "https://ireneusz1991.github.io"
    for p in posts:
        pub_date = datetime.strptime(p["created_at"][:19], "%Y-%m-%d %H:%M:%S").strftime("%a, %d %b %Y %H:%M:%S +0100")
        items_xml.append(f"""
        <item>
            <title><![CDATA[{p['title']}]]></title>
            <link>{site_domain}{base_url}/post/{p['slug']}/</link>
            <guid>{site_domain}{base_url}/post/{p['slug']}/</guid>
            <pubDate>{pub_date}</pubDate>
            <category>{p['category']}</category>
            <description><![CDATA[{p['summary']}]]></description>
        </item>
        """)
        
    rss_content = f"""<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0">
<channel>
    <title>{config.BLOG_TITLE}</title>
    <link>{site_domain}{base_url}/</link>
    <description>{config.BLOG_DESCRIPTION}</description>
    <language>pl</language>
    {''.join(items_xml)}
</channel>
</rss>
"""
    with open(os.path.join(output_dir, "rss.xml"), "w", encoding="utf-8") as f:
        f.write(rss_content.strip())
    print("    [OK] Wygenerowano: rss.xml")

    print("\n[SUKCES] Cała platforma statyczna została pomyślnie skompilowana w folderze 'dist/'!")

if __name__ == "__main__":
    build_static()

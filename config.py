import os

BLOG_TITLE = "Blog Laika"
BLOG_TAGLINE = "Technologia, Gospodarka, Polityka i inne eseje"
BLOG_DESCRIPTION = "Niezależne spojrzenie dociekliwego laika na mechanizmy rządzące technologią, gospodarką i współczesną polityką."
BLOG_AUTHOR = "Laik"
BLOG_AUTHOR_BIO = "Obserwator procesów technologicznych, rynkowych i społecznych. Piszę bez akademickiego żargonu, szukając istoty rzeczy i logiki zdarzeń."

CATEGORIES = [
    {"slug": "technologia", "name": "Technologia", "color": "#2563eb", "icon": "cpu", "desc": "Sztuczna inteligencja, cyfryzacja, przyszłość sieci i technologii"},
    {"slug": "gospodarka", "name": "Gospodarka", "color": "#059669", "icon": "trending-up", "desc": "Makroekonomia, rynki finansowe, energetyka i trendy globalne"},
    {"slug": "polityka", "name": "Polityka", "color": "#dc2626", "icon": "landmark", "desc": "Geopolityka, mechanizmy władzy, instytucje i przemiany społeczne"},
    {"slug": "eseje", "name": "Inne eseje", "color": "#7c3aed", "icon": "book-open", "desc": "Filozofia codzienności, kultura, książki i refleksje o świecie"}
]

ADMIN_USERNAME = os.getenv("BLOG_ADMIN_USER", "admin")
ADMIN_PASSWORD = os.getenv("BLOG_ADMIN_PASS", "laik2026")  # Do zmiany w panelu lub zmiennej środowiskowej
SECRET_KEY = os.getenv("BLOG_SECRET_KEY", "blog-laika-super-secret-key-change-in-prod-2026")
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "blog.db")

import os

BLOG_TITLE = "Blog Laika"
BLOG_TAGLINE = "Technologia, Gospodarka, Historia, Polityka"
BLOG_DESCRIPTION = "Niezależne spojrzenie dociekliwego laika na mechanizmy rządzące technologią, gospodarką, historią i współczesną polityką."
BLOG_AUTHOR = "Ireneusz Machowiec"
BLOG_AUTHOR_BIO = "Autor Bloga Laika. Obserwator procesów technologicznych, rynkowych, historycznych i geopolitycznych. Prowadzi niezależną publicystykę bez akademickiego żargonu."
BLOG_AUTHOR_NAME = "Ireneusz Machowiec"
BLOG_AUTHOR_ADDRESS = "Żdżary 57, 21-400 Łuków"
BLOG_AUTHOR_NIP = "8252128270"
BLOG_AUTHOR_EMAIL = "kontakt@blog-laika.com"

CATEGORIES = [
    {"slug": "technologia", "name": "Technologia", "color": "#2563eb", "icon": "cpu", "desc": "Sztuczna inteligencja, cyfryzacja, przyszłość sieci i technologii"},
    {"slug": "gospodarka", "name": "Gospodarka", "color": "#059669", "icon": "trending-up", "desc": "Makroekonomia, rynki finansowe, energetyka i trendy globalne"},
    {"slug": "historia", "name": "Historia", "color": "#d97706", "icon": "landmark", "desc": "Węzłowe punkty dziejów, mechanizmy upadku imperiów, historia gospodarcza i lekcje dla teraźniejszości"},
    {"slug": "polityka", "name": "Polityka", "color": "#dc2626", "icon": "shield", "desc": "Geopolityka, mechanizmy władzy, instytucje i przemiany społeczne"},
    {"slug": "eseje", "name": "Inne eseje", "color": "#7c3aed", "icon": "book-open", "desc": "Filozofia codzienności, kultura, książki i refleksje o świecie"}
]

ADMIN_USERNAME = os.getenv("BLOG_ADMIN_USER", "admin")
ADMIN_PASSWORD = os.getenv("BLOG_ADMIN_PASS", "laik2026")  # Do zmiany w panelu lub zmiennej środowiskowej
SECRET_KEY = os.getenv("BLOG_SECRET_KEY", "blog-laika-super-secret-key-change-in-prod-2026")
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "blog.db")
BASE_URL = os.getenv("BASE_URL", "")
SITE_DOMAIN = os.getenv("SITE_DOMAIN", "https://blog-laika.com")


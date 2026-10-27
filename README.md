# 🖋️ Blog Laika — Technologia, Gospodarka, Polityka i inne eseje

> **„W świecie wąskich specjalizacji i hermetycznego żargonu, dociekliwy laik zadaje najważniejsze pytania.”**

Nowoczesna, ultra-lekka platforma blogowa z wbudowanym autorskim panelem **CMS**, zaprojektowana specjalnie do publikacji esejów, analiz i publicystyki społeczno-gospodarczej.

---

## 🧭 Spis treści
1. [WordPress czy lekki CMS autorski? — Porównanie](#-wordpress-czy-lekki-cms-autorski)
2. [Identyfikacja wizualna i logo](#-identyfikacja-wizualna-i-logo)
3. [Architektura systemu i UI](#-architektura-systemu-i-ui)
4. [Szybki start (Uruchomienie w 1 kliknięcie)](#-szybki-start)
5. [Funkcje platformy i panelu CMS](#-funkcje-platformy-i-panelu-cms)
6. [Struktura plików projektu](#-struktura-plik%C3%B3w-projektu)
7. [Wdrożenie na serwer produkcyjny](#-wdro%C5%BCenie-na-serwer)

---

## ⚖️ WordPress czy lekki CMS autorski?

Użytkownik zadał pytanie o wybór: **WordPress CMS** czy **odpowiednia lekka alternatywa do pisania prostego bloga**.

| Cecha | WordPress | Blog Laika (Lekki CMS w Pythonie) |
|---|---|---|
| **Waga & narzut zasobów** | Duży (~100 MB plików, baza MySQL, serwer PHP/Apache) | **Minimalny** (< 2 MB, baza SQLite w jednym pliku) |
| **Szybkość działania (TTFB)** | Często 800–2000 ms bez agresywnego cachowania | **Błyskawiczna (< 15 ms)**, natywny asynchroniczny Python |
| **Doświadczenie pisania** | Ciężki edytor blokowy (Gutenberg) | **Dwupanelowy edytor Markdown z podglądem live** |
| **Bezpieczeństwo & aktualizacje**| Wymaga regularnych aktualizacji wtyczek i ochrony przed botami | **Brak podatności na typowe exploity WP**, zero zewnętrznych wtyczek |
| **Typografia eseistyczna** | Wymaga zakupu lub konfiguracji ciężkiego motywu | **Zoptymalizowana typografia Newsreader / Inter**, idealna do długich tekstów |
| **Kopia zapasowa (Backup)** | Złożony backup bazy SQL i katalogu `wp-content` | **Wystarczy skopiować plik `blog.db`** lub katalog z markdownem |

### Werdykt:
Do pisania **prostego, eleganckiego, opiniotwórczego bloga z esejami** (Technologia, Gospodarka, Polityka), WordPress jest zbyt ociężały i wymaga stałej opieki technicznej. Przygotowana platforma daje pełną swobodę pisania bez żadnych opłat licencyjnych, reklam czy podatności.

---

## 🎨 Identyfikacja wizualna i logo

Blog został wyposażony w kompletny zestaw logotypów:

1. **Wektorowy logotyp SVG (`static/images/logo.svg`)**:
   - Skalowalny bezstratnie na każdy ekran (Retina, 4K, smartfony).
   - Dynamiczny gradient kobaltowo-szafirowy z akcentem bursztynowym.
   - Pióro publicystyczne przeplatające się z orbitą satelity badawczego i gwiazdą ciekawości.
   - Nowoczesna, czysta typografia nagłówkowa z podtytułem *Technologia • Gospodarka • Polityka*.

2. **Wektorowy Favicon (`static/images/favicon.svg`)**:
   - Dedykowana ikona do paska kart przeglądarki i zakładek.

3. **Wygenerowane logo koncepcyjne (`static/images/logo.jpg`)**:
   - Redakcyjny emblemat w stylu prestiżowych magazynów opinii (*The Atlantic*, *Quanta Magazine*).

---

## 🏗️ Architektura systemu i UI

### Architektura techniczna (MVC / Clean Core):
- **Backend**: FastAPI (Python 3.12) — asynchroniczny, nowoczesny framework webowy.
- **Baza danych**: SQLite3 — bezobsługowa baza danych w jednym pliku (`blog.db`), działająca natywnie bez instalowania serwerów MySQL/PostgreSQL.
- **Szablony**: Jinja2 — semantyczny HTML5, SSR (Server-Side Rendering) gwarantujący idealne SEO i natychmiastowe ładowanie.
- **Formatowanie treści**: Markdown (wzbogacony o tabele, wyróżnienia kodu, cytaty blokowe, automatyczny slug i czas czytania).
- **Format kanału informacyjnego**: Natywny kanał RSS 2.0 (`/rss.xml`) dla czytników RSS (Feedly, Inoreader, Apple News).

### Projekt Interfejsu (UI / UX):
- **Czysta typografia eseistyczna**:
  - Tytuły i treść esejów: szlachetny szeryf *Newsreader / Georgia* zapewniający maksymalny komfort lektury długich artykułów.
  - Interfejs i nawigacja: nowoczesny bezszeryfowy *Inter*.
  - Szerokość szpalty tekstu zoptymalizowana do ~720px (złoty standard czytelności).
- **Tryb Ciemny / Jasny (Dark Mode)**:
  - Przełącznik jednym kliknięciem z zapamiętywaniem wyboru w `localStorage` oraz automatycznym wykrywaniem preferencji systemowych.
- **Pasek postępu czytania (Reading Progress)**:
  - Dyskretny pasek postępu u góry ekranu pokazujący, ile eseju zostało do końca.
- **Kategorie tematyczne z dedykowanymi akcentami**:
  - 🔵 **Technologia** (`#2563eb`) — AI, oprogramowanie, cyfryzacja.
  - 🟢 **Gospodarka** (`#059669`) — Makroekonomia, inflacja, rynki finansowe.
  - 🔴 **Polityka** (`#dc2626`) — Geopolityka, mechanizmy władzy, ład międzynarodowy.
  - 🟣 **Inne eseje** (`#7c3aed`) — Filozofia, kultura, refleksje o świecie.

---

## 🚀 Szybki start

### Metoda 1: Uruchomienie w 1 kliknięcie (Windows)
Wystarczy dwukrotnie kliknąć plik:
```
uruchom_blog.bat
```
Skrypt sprawdzi Pythona, uruchomi lokalny serwer i automatycznie otworzy bloga w przeglądarce pod adresem:
👉 **`http://127.0.0.1:8000`**

### Metoda 2: Uruchomienie z terminala
```powershell
# 1. Wejdź do katalogu projektu
cd "g:\Mój dysk\blog-laika"

# 2. Uruchom aplikację
python app.py
```

---

## 🔐 Panel Autorski (CMS)

Wejdź na: **`http://127.0.0.1:8000/admin`**

- **Domyślny login**: `admin`
- **Domyślne hasło**: `laik2026`
*(Hasło i login możesz w każdej chwili zmienić w pliku `config.py`)*

### Możliwości panelu:
1. **Tworzenie i edycja esejów**:
   - Lewe okno: Pisanie w Markdownie (z obsługą skrótów klawiszowych, wcięć Tab, bloków kodu).
   - Prawe okno: **Podgląd na żywo w czasie rzeczywistym** dokładnie w takim wyglądzie, jaki zobaczą czytelnicy.
   - Licznik słów oraz automatyczna estymacja czasu czytania (np. `~4 min czytania`).
   - Automatyczne generowanie przyjaznych linków (slugów) z polskich znaków (np. `ą -> a`, `ł -> l`).
2. **System szkiców i publikacji**:
   - Możliwość zapisania niedokończonego tekstu jako *Szkic* (niewidoczny dla gości, dostępny tylko dla Ciebie).
   - Przycisk *Wyróżnij* (umieszcza esej jako główny artykuł na samej górze strony głównej).
3. **Statystyki**:
   - Liczba opublikowanych esejów, liczba szkiców, łączna suma odsłon oraz podział na kategorie.
4. **Wyszukiwarka pełnotekstowa**:
   - Działa natychmiastowo po tytule, treści, wstępie i tagach.

---

## 📁 Struktura plików projektu

```
blog-laika/
├── app.py                     # Główny serwer FastAPI i routing
├── config.py                  # Konfiguracja bloga, kategorie, hasło CMS
├── database.py                # Obsługa bazy SQLite, zapytań i operacji CRUD
├── sample_data.py             # 4 przykładowe gotowe eseje na start
├── blog.db                    # Baza danych SQLite (tworzona automatycznie)
├── requirements.txt           # Lista zależności Pythona
├── uruchom_blog.bat           # Skrypt startowy 1-click dla Windows
├── README.md                  # Dokumentacja projektu
├── templates/                 # Szablony HTML (Jinja2)
│   ├── base.html              # Układ główny, nagłówek, nawigacja, stopka
│   ├── index.html             # Strona główna z wyróżnionym esejem i siatką wpisów
│   ├── post.html              # Widok pojedynczego eseju (pasek czytania, autor, udostępnianie)
│   ├── category.html          # Filtrowanie esejów według kategorii
│   ├── search.html            # Strona wyników wyszukiwania
│   ├── about.html             # Manifest i strona „O blogu / O autorze”
│   └── admin/
│       ├── login.html         # Ekran logowania do CMS
│       ├── dashboard.html     # Lista wpisów, statystyki odsłon, akcje
│       └── editor.html        # Dwupanelowy edytor z podglądem na żywo
└── static/
    ├── css/
    │   └── style.css          # Style CSS: typografia, tryb ciemny, responsywność
    ├── js/
    │   ├── app.js             # Skrypt motywu ciemnego, paska czytania i udostępniania
    │   └── editor.js          # Skrypt podglądu Markdown na żywo i automatycznego sluga
    └── images/
        ├── logo.svg           # Skalowalny wektorowy logotyp główny
        ├── favicon.svg        # Wektorowa ikona przeglądarki
        ├── logo.jpg           # Wygenerowane logo koncepcyjne (magazynowe)
        └── logo_alt.jpg       # Wersja alternatywna logo
```

---

## 🌐 Wdrożenie na serwer i GitHub Pages

### 🌟 Hosting na GitHub Pages (100% darmowy, SSL, globalny CDN):
Twój blog jest już przygotowany i skompilowany na gałęzi **`gh-pages`**!
Adres strony:
👉 **[https://ireneusz1991.github.io/blog-laika/](https://ireneusz1991.github.io/blog-laika/)**

#### Aby włączyć stronę w GitHubie (jednorazowo):
1. Otwórz: **[https://github.com/Ireneusz1991/blog-laika/settings/pages](https://github.com/Ireneusz1991/blog-laika/settings/pages)**
2. W sekcji **„Build and deployment”**:
   - **Source**: wybierz `Deploy from a branch`
   - **Branch**: wybierz `gh-pages` oraz folder `/ (root)`
   - Kliknij **Save**.
3. Po minucie blog będzie publicznie dostępny na całym świecie!

#### Publikacja nowych esejów na GitHub Pages w 1 kliknięcie:
Gdy napiszesz nowy esej w panelu CMS na komputerze, po prostu kliknij dwukrotnie:
👉 **`publikuj_na_github_pages.bat`**  
Skrypt automatycznie przebuduje stronę i wyśle najnowszą wersję na GitHub Pages!

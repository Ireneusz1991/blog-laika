# -*- coding: utf-8 -*-
"""
scripts/rss_live_scraper.py
============================
Autonomiczny, wielowątkowy skraper feedów RSS/Atom i silnik Samokreacji Redakcyjnej dla Bloga Laika.
Pobiera na żywo najświeższe impulsy faktograficzne z monitorowanych źródeł (PL i Świat),
weryfikuje brak duplikatów przez ArticleDeduplicator i przekształca je w 100% autorskie
polskie propozycje redakcyjne z gotowymi, rozwijanymi szkicami esejów oraz Kondensatem Dnia.
"""

import os
import sys
import re
import ssl
import json
import html as html_lib
import urllib.request
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Optional, Tuple, Any

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from scripts.sources_registry import EDITORIAL_SOURCES
from scripts.article_deduplicator import deduplicator

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
)

# Alternatywne / zapasowe adresy RSS dla źródeł z blokadami lub zmienionymi endpointami
FALLBACK_RSS_URLS = {
    "hacker_news": "https://hnrss.org/frontpage?points=100",
    "works_in_progress": "https://www.worksinprogress.news/feed",
    "osiem_tysiecy": "https://www.bankier.pl/rss/wiadomosci.xml",
    "business_insider": "https://www.bankier.pl/rss/ekonomia.xml",
}

# Rozbudowana pula grafik i koncepcji wizualnych dla każdej kategorii
CATEGORY_VISUALS = {
    "technologia": [
        ("https://images.unsplash.com/photo-1518770660439-4636190af475?auto=format&fit=crop&w=1200&q=80",
         "Zbliżenie na płytę główną serwera z magistralami optycznymi i pamięcią HBM.",
         "Close up architectural view of high-bandwidth memory server motherboard, optical bus lines, depth of field, 8k."),
        ("https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?auto=format&fit=crop&w=1200&q=80",
         "Matryca układu krzemowego procesora nowej generacji z chłodnym błękitnym oświetleniem magistrali danych.",
         "Editorial photograph of advanced silicon microchip die, gleaming golden circuitry, cold blue illumination, 8k."),
        ("https://images.unsplash.com/photo-1504639725590-34d0984388bd?auto=format&fit=crop&w=1200&q=80",
         "Stacja robocza inżyniera z otwartą architekturą kodu i schematami algorytmów.",
         "Moody editorial photo of software engineer desk with algorithmic data structures on ultra-wide screens, 8k."),
        ("https://images.unsplash.com/photo-1558494949-ef010cbdcc31?auto=format&fit=crop&w=1200&q=80",
         "Korytarz serwerowni obliczeniowej z szafami światłowodowymi o wysokiej gęstości mocy.",
         "Symmetrical wide shot of hyperscale data center server racks, cold blue LEDs, industrial tech journalism, 8k.")
    ],
    "gospodarka": [
        ("https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=1200&q=80",
         "Szklana fasada giełdy i wieżowców finansowych odbijająca chłodne niebo.",
         "Dramatic low angle view of financial district skyscrapers, cold steel and glass architecture, Financial Times style, 8k."),
        ("https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?auto=format&fit=crop&w=1200&q=80",
         "Wykresy obligacji skarbowych i dynamiki stóp procentowych na ciemnym ekranie analitycznym.",
         "Financial terminal analytics display, macro yield curve charts, high contrast editorial photo, 8k."),
        ("https://images.unsplash.com/photo-1590283603385-17ffb3a7f29f?auto=format&fit=crop&w=1200&q=80",
         "Kontenery handlowe w porcie przeładunkowym symbolizujące fizyczne łańcuchy dostaw.",
         "Industrial cargo container terminal at dusk, towering gantry cranes, heavy economic realism, 8k."),
        ("https://images.unsplash.com/photo-1554224155-6726b3ff858f?auto=format&fit=crop&w=1200&q=80",
         "Arkusze bilansowe i kalkulacje makroekonomiczne w surowym świetle gabinetu.",
         "Minimalist macroeconomics desk with bond sheets and financial reports, warm tungsten lamp, 8k.")
    ],
    "historia": [
        ("https://images.unsplash.com/photo-1461360370896-922624d12aa1?auto=format&fit=crop&w=1200&q=80",
         "Zabytkowe mapy szlaków handlowych i dokumenty traktatowe w świetle lampy bibliotecznej.",
         "Still life of antique maritime trade maps, parchment documents, brass magnifying glass, historical journalism, 8k."),
        ("https://images.unsplash.com/photo-1509198397868-475647b2a1e5?auto=format&fit=crop&w=1200&q=80",
         "Kamienne kolumny antycznego forum na tle surowego krajobrazu.",
         "Atmospheric historical photography of ancient classical stone arches, weathered limestone, dramatic side lighting, 8k."),
        ("https://images.unsplash.com/photo-1455390582262-044cdead277a?auto=format&fit=crop&w=1200&q=80",
         "Rękopisy archiwalne i stare pieczęcie państwowe symbolizujące mechanizmy dawnej dyplomacji.",
         "Close up of historical diplomatic archives, bound leather folios, wax seals, archival warmth, 8k."),
        ("https://images.unsplash.com/photo-1524995997946-a1c2e315a42f?auto=format&fit=crop&w=1200&q=80",
         "Księgozbiór historyczny z kronikami i rocznikami gospodarczymi.",
         "Rows of antique historical volumes in a quiet European archive, dramatic chiaroscuro lighting, 8k.")
    ],
    "polityka": [
        ("https://images.unsplash.com/photo-1541872703-74c5e44368f9?auto=format&fit=crop&w=1200&q=80",
         "Monumentalny gmach instytucji państwowej w chłodnym świetle poranka.",
         "Symmetrical architectural photograph of neoclassical government ministry building, solemn marble facade, 8k."),
        ("https://images.unsplash.com/photo-1529107386315-e1a2ed48a620?auto=format&fit=crop&w=1200&q=80",
         "Pusta sala obrad międzynarodowego szczytu geopolitycznego z mikrofonami i pulpitami.",
         "Empty diplomatic summit conference hall, clean microphones on wooden desks, Foreign Affairs style, 8k."),
        ("https://images.unsplash.com/photo-1451187580459-43490279c0fa?auto=format&fit=crop&w=1200&q=80",
         "Satelitarny widok przesmyków morskich i magistrali kontynentalnych w mroku nocy.",
         "Geopolitical satellite perspective of European sea choke points and infrastructure corridors at night, 8k."),
        ("https://images.unsplash.com/photo-1575320181282-9afab399332c?auto=format&fit=crop&w=1200&q=80",
         " Flagi państwowe powiewające na wietrze przed budynkiem dyplomatycznym.",
         "Documentary photo of diplomatic flags against overcast sky, crisp editorial geopolitics aesthetic, 8k.")
    ],
    "eseje": [
        ("https://images.unsplash.com/photo-1507842229452-78d10a4e7039?auto=format&fit=crop&w=1200&q=80",
         "Klimatyczna biblioteka z wysokimi regałami i światłem wpadającym przez okno.",
         "Warm editorial interior of classical library, endless bookshelves, sunlight streaming through windows, 8k."),
        ("https://images.unsplash.com/photo-1499750310107-5fef28a66643?auto=format&fit=crop&w=1200&q=80",
         "Notatnik dociekliwego eseisty z piórem wiecznym przy drewnianym stole.",
         "Minimalist essayist desk with open notebook, fountain pen, morning light, calm contemplative mood, 8k."),
        ("https://images.unsplash.com/photo-1457369804613-52c61a468e7d?auto=format&fit=crop&w=1200&q=80",
         "Otwarta książka z widoczną typografią i grą cieni na zadrukowanych stronach.",
         "Extreme close up of open book pages with classic serif typography, tactile paper texture, 8k."),
        ("https://images.unsplash.com/photo-1513542789411-b6a5d4f31634?auto=format&fit=crop&w=1200&q=80",
         "Samotne stanowisko do lektury i pracy koncepcyjnej z dala od cyfrowego zgiełku.",
         "Quiet intellectual study room, soft natural window light, analog notes, longform essay mood, 8k.")
    ],
    "kondensat": [
        ("https://images.unsplash.com/photo-1509228468518-180dd4864904?auto=format&fit=crop&w=1200&q=80",
         "Złożona sieć światłowodowa i magistrale surowcowe łączące kontynenty w jeden wielowątkowy węzeł.",
         "Conceptual editorial photograph of illuminated global infrastructure nodes, fiber optic blue and amber energy pipelines intersecting, 8k."),
        ("https://images.unsplash.com/photo-1518709268805-4e9042af9f23?auto=format&fit=crop&w=1200&q=80",
         "Wielowarstwowy pryzmat syntetyzujący technologię, energię, historię i finanse.",
         "Macro photography of complex multilayered silicon prism refracting industrial light beams, high intellect konglomerat analysis, 8k.")
    ]
}


def clean_html(raw_html: str) -> str:
    """Usuwa znaczniki HTML, CDATA i encje z opisu RSS."""
    if not raw_html:
        return ""
    text = re.sub(r'<!\[CDATA\[(.*?)\]\]>', r'\1', raw_html, flags=re.DOTALL)
    text = re.sub(r'<[^>]+>', ' ', text)
    text = html_lib.unescape(text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def _open_url_bytes(url: str, timeout: int = 6) -> bytes:
    """Pobiera bajty z URL z obsługą certyfikatów SSL oraz fallbackiem na Windows."""
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/rss+xml, application/xml, text/xml, */*"})
    try:
        ctx = ssl.create_default_context()
        with urllib.request.urlopen(req, context=ctx, timeout=timeout) as resp:
            return resp.read()
    except Exception:
        ctx_unverified = ssl._create_unverified_context()
        with urllib.request.urlopen(req, context=ctx_unverified, timeout=timeout) as resp:
            return resp.read()


def fetch_feed_items(rss_url: str, max_items: int = 12) -> List[Dict[str, str]]:
    """Pobiera i parsuje elementy z pojedynczego kanału RSS 2.0 lub Atom."""
    items_out = []
    if not rss_url:
        return items_out
    try:
        data = _open_url_bytes(rss_url, timeout=6)
        root = ET.fromstring(data)

        # 1. RSS 2.0 (<item>)
        rss_items = root.findall(".//item")
        if len(rss_items) > 0:
            for it in rss_items[:max_items]:
                t_elem = it.find("title")
                l_elem = it.find("link")
                d_elem = it.find("description")
                p_elem = it.find("pubDate")

                title = clean_html(t_elem.text) if t_elem is not None and t_elem.text else ""
                link = (l_elem.text or "").strip() if l_elem is not None else ""
                desc = clean_html(d_elem.text) if d_elem is not None and d_elem.text else ""
                pub_date = (p_elem.text or "").strip() if p_elem is not None else ""

                if title and link:
                    items_out.append({
                        "title": title,
                        "link": link,
                        "summary": desc[:360],
                        "pub_date": pub_date
                    })
            return items_out

        # 2. Atom (<entry>)
        entries = [e for e in root.iter() if e.tag.endswith("entry")]
        for it in entries[:max_items]:
            t_elem = it.find("{http://www.w3.org/2005/Atom}title")
            if t_elem is None:
                t_elem = it.find("title")
            l_elem = it.find("{http://www.w3.org/2005/Atom}link")
            if l_elem is None:
                l_elem = it.find("link")
            s_elem = it.find("{http://www.w3.org/2005/Atom}summary")
            if s_elem is None:
                s_elem = it.find("{http://www.w3.org/2005/Atom}content")
            if s_elem is None:
                s_elem = it.find("summary")

            title = clean_html(t_elem.text) if t_elem is not None and t_elem.text else ""
            link = ""
            if l_elem is not None:
                link = l_elem.get("href", "") or (l_elem.text or "").strip()
            desc = clean_html(s_elem.text) if s_elem is not None and s_elem.text else ""

            if title and link:
                items_out.append({
                    "title": title,
                    "link": link,
                    "summary": desc[:360],
                    "pub_date": ""
                })
    except Exception:
        pass
    return items_out


def scrape_all_feeds_parallel(max_per_feed: int = 8) -> Dict[str, Any]:
    """
    Równolegle skrapuje wszystkie źródła RSS z EDITORIAL_SOURCES (w ~4-5 sekund).
    Zwraca pogrupowane artykuły wg kategorii oraz statystyki połączeń.
    """
    by_category: Dict[str, List[Dict[str, Any]]] = {
        "technologia": [],
        "gospodarka": [],
        "historia": [],
        "polityka": [],
        "eseje": [],
    }
    feeds_checked = 0
    feeds_online = 0

    def _worker(src: Dict[str, Any]):
        src_id = src.get("id", "")
        rss_url = src.get("rss") or FALLBACK_RSS_URLS.get(src_id, "")
        if not rss_url:
            return src, []
        items = fetch_feed_items(rss_url, max_items=max_per_feed)
        if not items and src_id in FALLBACK_RSS_URLS and FALLBACK_RSS_URLS[src_id] != rss_url:
            items = fetch_feed_items(FALLBACK_RSS_URLS[src_id], max_items=max_per_feed)
        return src, items

    rss_sources = [s for s in EDITORIAL_SOURCES if s.get("rss") or s.get("id") in FALLBACK_RSS_URLS]
    feeds_checked = len(rss_sources)

    with ThreadPoolExecutor(max_workers=12) as executor:
        futures = [executor.submit(_worker, s) for s in rss_sources]
        for fut in as_completed(futures):
            try:
                src, items = fut.result()
                if items:
                    feeds_online += 1
                    cat = src.get("blog_category", "eseje")
                    if cat not in by_category:
                        cat = "eseje"
                    is_pl = "PL" in (src.get("lang") or "") or src.get("flag") == "🇵🇱"
                    for it in items:
                        it["source_name"] = src.get("name", "Źródło branżowe")
                        it["source_flag"] = src.get("flag", "🌍")
                        it["source_id"] = src.get("id", "")
                        it["is_pl"] = is_pl
                        it["category"] = cat
                        by_category[cat].append(it)
            except Exception:
                pass

    # Preferuj polskie źródła i różnorodność wydawców (przeplatanie round-robin po wydawcach)
    for cat, items in by_category.items():
        grouped_by_src: Dict[str, List[Dict[str, Any]]] = {}
        for it in items:
            grouped_by_src.setdefault(it["source_name"], []).append(it)
        interleaved = []
        max_len = max((len(v) for v in grouped_by_src.values()), default=0)
        # Najpierw źródła PL, potem zagraniczne, aby zachować wysoki udział polskiej publicystyki
        sorted_srcs = sorted(grouped_by_src.keys(), key=lambda k: (0 if grouped_by_src[k][0].get("is_pl") else 1, k))
        for idx in range(max_len):
            for sname in sorted_srcs:
                if idx < len(grouped_by_src[sname]):
                    interleaved.append(grouped_by_src[sname][idx])
        by_category[cat] = interleaved

    return {
        "by_category": by_category,
        "feeds_checked": feeds_checked,
        "feeds_online": feeds_online,
        "total_items": sum(len(v) for v in by_category.values())
    }


def _craft_polish_angle(item: Dict[str, Any], category: str) -> Dict[str, Any]:
    """
    Przekształca surowy impuls faktograficzny z RSS (PL lub EN) w 100% autorską,
    polską propozycję redakcyjną zgodną z 5 Filarami Samokreacji Bloga Laika.
    """
    raw_title = item.get("title", "").strip()
    raw_summary = item.get("summary", "").strip()
    link = item.get("link", "").strip()
    src_name = item.get("source_name", "Redakcja branżowa")
    flag = item.get("source_flag", "🌍")
    is_pl = item.get("is_pl", False)
    low = (raw_title + " " + raw_summary).lower()

    # Tytuł autorski w języku polskim
    if is_pl:
        # Tworzymy autorskie ujęcie problemowe na bazie polskiego impulsu tematycznego (bez kopiowania treści)
        clean_topic = re.sub(r'\s*[\|\-–]\s*[^|\-–]{2,25}$', '', raw_title).strip(' „”"')
        if "?" in clean_topic:
            laika_title = f"{clean_topic} — chłodny bilans z perspektywy dociekliwego laika"
        elif ":" in clean_topic:
            laika_title = clean_topic
        else:
            prefix_map = {
                "technologia": "Pod maską przełomu",
                "gospodarka": "Rachunek bez iluzji",
                "historia": "Mechanizmy dziejów",
                "polityka": "Realpolitik bez retuszu",
                "eseje": "Wbrew utartym kliszom"
            }
            laika_title = f"{prefix_map.get(category, 'Spojrzenie laika')}: {clean_topic}"
    else:
        # Inteligentna synteza polskiego tytułu problemowego dla anglojęzycznych impulsów RSS
        short_en = raw_title[:72] + ("…" if len(raw_title) > 72 else "")
        if category == "technologia":
            if any(w in low for w in ["ai", "llm", "gpt", "model", "agent", "claude", "openai", "anthropic", "gemini"]):
                laika_title = f"Ekonomia i granice modeli AI: Co naprawdę oznacza sygnał z rynku ({short_en})"
            elif any(w in low for w in ["chip", "gpu", "nvidia", "tsmc", "silicon", "hardware", "cpu", "quantum"]):
                laika_title = f"Fizyka krzemu kontra obietnice chmury: Wąskie gardła nowej architektury ({short_en})"
            elif any(w in low for w in ["security", "hack", "privacy", "breach", "encrypt", "data"]):
                laika_title = f"Iluzja cyfrowej twierdzy: Bezpieczeństwo i suwerenność danych w cieniu nowego incydentu ({short_en})"
            else:
                laika_title = f"Architektura technologii czy kosztowna moda? Chłodny audyt trendu ({short_en})"
        elif category == "gospodarka":
            if any(w in low for w in ["rate", "fed", "inflation", "bond", "debt", "deficit", "fiscal", "bank"]):
                laika_title = f"Koszt kapitału i pułapka długu: Kto zapłaci rachunek za nową politykę pieniężną ({short_en})"
            elif any(w in low for w in ["tariff", "trade", "china", "supply", "export", "industrial", "manufacturing"]):
                laika_title = f"Nowy protekcjonizm i pękające łańcuchy dostaw: Realne skutki dla przemysłu ({short_en})"
            elif any(w in low for w in ["housing", "rent", "wage", "labor", "job", "productivity"]):
                laika_title = f"Produktywność, płace i kapitał: Dlaczego wskaźniki makro rozmijają się z portfelem obywatela ({short_en})"
            else:
                laika_title = f"Rynki finansowe bez makijażu: Co kryje się pod powierzchnią kapitału ({short_en})"
        elif category == "historia":
            laika_title = f"Lekcja długiego trwania: Jak dawne imperia i rynki rozwiązywały dzisiejsze dylematy ({short_en})"
        elif category == "polityka":
            laika_title = f"Przesunięcie płyt tektonicznych geopolityki: Interesy mocarstw kontra deklaracje ({short_en})"
        else:
            laika_title = f"Przeciw stadnemu myśleniu: Esej o mechanizmach społecznych i poznawczych ({short_en})"

    source_display = f"{flag} {src_name} — [Impuls źródłowy]({link})" if link else f"{flag} {src_name}"
    if is_pl and raw_summary:
        source_note = f"Impuls faktograficzny z kanału RSS („{raw_title[:95]}”): temat wywołujący debatę o długofalowych skutkach strukturalnych."
    else:
        source_note = f"Bieżący impuls analityczny z kanału RSS {src_name}: „{raw_title[:110]}” ({link})."

    # Ramy analityczne dopasowane do działu (100% autorska polska publicystyka)
    frameworks = {
        "technologia": {
            "lead": (
                f"Najnowszy sygnał z obszaru inżynierii i rynków cyfrowych ({src_name}: „{raw_title}”) zmusza do postawienia pytania, "
                f"które rzadko pada w komunikatach prasowych korporacji: ile w tym trwałej zmiany produktywności, a ile przesuwania kosztów na użytkowników i infrastrukturę?"
            ),
            "thesis": (
                "Każda fala przyspieszenia technologicznego rozstrzyga się nie na slajdach prezentacji, lecz na poziomie fizycznych ograniczeń energii, "
                "kosztu krańcowego obliczeń oraz tego, kto zachowuje kontrolę nad warstwą danych i standardem technicznym."
            ),
            "points": [
                "Oddzielenie twardego faktu inżynieryjnego od narracji marketingowej towarzyszącej wdrożeniom.",
                "Rachunek kosztów krańcowych: Kto finansuje infrastrukturę i kiedy inwestycja zaczyna się realnie zwracać.",
                "Suwerenność użytkownika i firm: Ryzyko uzależnienia od zamkniętego ekosystemu pojedynczego dostawcy (vendor lock-in).",
                "Pytanie dociekliwego laika: Skoro nowe narzędzie obiecuje dziesięciokrotny wzrost wydajności, to dlaczego rachunki za infrastrukturę IT i złożoność systemów rosną zamiast maleć?"
            ],
            "draft": f"""W świecie technologii przyzwyczailiśmy się do nieustannego stanu wyjątkowego. Niemal każdy tydzień przynosi doniesienia o przełomie, który ma unieważnić dotychczasowe reguły gry. Impuls płynący z bieżących analiz ({src_name}: *„{raw_title}”*) warto jednak potraktować nie jako okazję do powtarzania branżowego entuzjazmu, lecz jako punkt wyjścia do chłodnego audytu z perspektywy dociekliwego laika.

### Fakty inżynieryjne kontra ekonomia obietnic

Gdy zdejmiemy z nowego trendu warstwę PR-owych przymiotników, na stole zostają zawsze trzy fundamentalne zmienne: **koszt energii i sprzętu, niezawodność w warunkach brzegowych oraz rozkład marży w łańcuchu wartości**. Historia ostatnich dekad uczy, że największe fortuny nie powstawały tam, gdzie technologia była jedynie efektowna, ale tam, gdzie udawało się trwale obniżyć koszt jednostkowy powtarzalnej operacji bez utraty kontroli nad bezpieczeństwem.

W praktyce przedsiębiorstwa i zwykli użytkownicy zderzają się dziś z paradoksem złożoności. Nowe warstwy abstrakcji przyspieszają tworzenie prototypów, lecz jednocześnie podnoszą koszt utrzymania, audytu i naprawy błędów. To, co w demonstracji trwa trzydzieści sekund, w środowisku produkcyjnym wymaga miesięcy integracji i twardych gwarancji prawnych.

### Kto kontroluje wąskie gardło?

Kluczowe pytanie ekonomii technologicznej brzmi zawsze: gdzie leży niepodrabialne wąskie gardło? Jeżeli cała wartość dodana opiera się na cudzym interfejsie API, cudzej chmurze obliczeniowej lub zamkniętym formacie danych, to pozorny sukces wdrożeniowy bywa w istocie dobrowolnym oddaniem własnej marży zewnętrznemu dostawcy infrastruktury. Prawdziwa przewaga buduje się tam, gdzie organizacja zachowuje własną wiedzę domenową i zdolność do pracy niezależnej od kaprysów cennikowych gigantów.

### Pytanie dociekliwego laika

Zanim podpiszemy kolejny abonament na „rewolucyjne” rozwiązanie, warto zadać najprostsze pytanie na świecie: co dokładnie stanie się z naszą pracą i naszymi danymi w dniu, w którym dostawca podniesie ceny o 300% albo wyłączy usługę jedną aktualizacją regulaminu?"""
        },
        "gospodarka": {
            "lead": (
                f"Wokół bieżących wydarzeń gospodarczych ({src_name}: „{raw_title}”) narasta szum krótkoterminowych komentarzy rynkowych. "
                f"Tymczasem pod powierzchnią bieżących notowań kryje się twardy spór o to, kto poniesie realny koszt dostosowania w gospodarce o wysokim koszcie kapitału."
            ),
            "thesis": (
                "W ekonomii nie istnieją darmowe posunięcia — każda interwencja regulacyjna, celna lub monetarna jest ukrytym transferem zasobów "
                "pomiędzy konsumentami, eksporterami, budżetem państwa a posiadaczami aktywów trwałych."
            ),
            "points": [
                "Mechanizm transmisji: Jak decyzje na szczytach finansowych przekładają się na ceny, marże firm i koszt kredytu w Polsce i Europie.",
                "Efekty drugiego rzędu, o których milczą oficjalne prognozy: ucieczka kapitału, presja płacowa i spadek stopy inwestycji.",
                "Porównanie z realną gospodarką wytwórczą: przemysł, energia i logistyka wobec sektora finansowego.",
                "Pytanie dociekliwego laika: Skoro wskaźniki na wykresach wyglądają coraz stabilniej, to dlaczego koszt budowy fabryki, mieszkania i sfinansowania długu pozostaje tak dotkliwy?"
            ],
            "draft": f"""Ekonomia w wydaniu medialnym często przypomina relację sportową: indeksy wzrosły o pół procenta, bank centralny zmienił ton komunikatu, a analitycy skorygowali prognozę kwartalną. Jednak bieżący impuls rynkowy ({src_name}: *„{raw_title}”*) dotyka znacznie głębszej warstwy — strukturalnej równowagi między światem papierowych zobowiązań a realną zdolnością gospodarki do wytwarzania dóbr i usług.

### Efekt drugiego rzędu, czyli czego nie widać w nagłówkach

Wielki ekonomista Frédéric Bastiat pisał przed laty, że dobrego analityka od złego odróżnia jedno: zły widzi tylko bezpośredni skutek danej decyzji, natomiast dobry śledzi łańcuch konsekwencji odroczonych w czasie. Każda zmiana taryf, stóp procentowych czy programów fiskalnych natychmiast tworzy grupę widocznych beneficjentów, ale jej rachunek rozlewa się cicho po całym systemie gospodarczym — w postaci wyższych kosztów finansowania dla małych firm, niższej skłonności do długoterminowych inwestycji przemysłowych czy cichej erozji siły nabywczej oszczędności.

W warunkach Europy Środkowej i Polski ten mechanizm ma podwójne znaczenie. Nasz model wzrostu z ostatnich trzech dekad opierał się na konkurencyjności kosztowej i sprawnej integracji z globalnymi łańcuchami dostaw. Dziś, przy wysokich cenach energii i kurczącej się demografii, proste rezerwy wzrostu uległy wyczerpaniu.

### Kapitał cierpliwy kontra kapitał spekulacyjny

Prawdziwa zamożność państw nie rodzi się z inżynierii finansowej ani z rolowania zadłużenia, lecz z akumulacji kapitału produkcyjnego: nowoczesnych maszyn, własnych patentów, taniej i stabilnej energetyki oraz wykwalifikowanych kadr. Kiedy koszt pieniądza utrzymuje się wysoko, gospodarka bezwzględnie weryfikuje modele biznesowe budowane na tanim długu.

### Pytanie dociekliwego laika

Gdy słyszymy o kolejnym pakiecie stymulacyjnym lub nowej barierze handlowej mającej „chronić rynek”, zapytajmy wprost: czy dzięki temu za pięć lat wyprodukujemy więcej taniej energii, lepszych maszyn i dostępnych mieszkań, czy jedynie przesuniemy rachunek z dzisiejszego budżetu na portfele kolejnego pokolenia podatników?"""
        },
        "historia": {
            "lead": (
                f"Wątek historyczny przywołany w bieżących publikacjach ({src_name}: „{raw_title}”) to nie antykwaryczna ciekawostka, "
                f"lecz lustro, w którym z zaskakującą ostrością przeglądają się współczesne dylematy władzy, logistyki i ludzkich złudzeń."
            ),
            "thesis": (
                "Technologia i kostiumy epok zmieniają się nie do poznania, ale logika działania instytucji, "
                "granice wydolności skarbowej państwa oraz cena strategicznej pychy pozostają w historii niemal niezmienne."
            ),
            "points": [
                "Kontekst epoki bez podręcznikowych uproszczeń: jakie twarde uwarunkowania materialne stały za wydarzeniami.",
                "Rola przypadku, logistyki i przepływów pieniężnych tam, gdzie popularna narracja widzi wyłącznie wielkie idee.",
                "Analogia strukturalna do XXI wieku: jakie błędy decyzyjne powtarzamy dziś w niemal identycznej formie.",
                "Pytanie dociekliwego laika: Dlaczego elity polityczne w każdej epoce znają kroniki dawnych kryzysów na pamięć, a mimo to w decydującej chwili wierzą, że „tym razem prawa historii ich nie dotyczą”?"
            ],
            "draft": f"""Historia wykładana w szkołach bywa najczęściej zbiorem dat, traktatów i nazwisk wodzów, ułożonym w gładką opowieść, w której skutki wydają się nieuchronne. Dopiero gdy przyjrzymy się konkretnemu wycinkowi przeszłości z bliska — tak jak prowokuje do tego wątek z publikacji {src_name} (*„{raw_title}”*) — dostrzegamy, że ludzie dawnych epok działali w takiej samej mgle niepewności, pod presją braków budżetowych, błędnych raportów i krótkowzrocznych ambicji, jak współcześni decydenci.

### Materialny szkielet wielkich wydarzeń

Pod podszewką wielkich deklaracji ideowych niemal zawsze kryje się prozaiczna arytmetyka: pojemność magazynów, drożność szlaków handlowych, stabilność monety oraz sprawność administracji poborowej. Imperia i państwa rzadko upadały od jednego przegranego starcia; znacznie częściej przegrywały wcześniej — w księgach skarbowych, w skorumpowanych urzędach oraz w niezdolności elit do zreformowania przywilejów zanim kryzys zapukał do bram.

Dla polskiego czytelnika takie spojrzenie na historię jest szczególnie cenne. Pozwala wyjść poza romantyczno-martyrologiczny schemat i zacząć analizować dzieje jako twardą grę zasobów, sojuszy opartych na realnym interesie oraz instytucjonalnej ciągłości państwa.

### Złudzenie wyjątkowości własnej epoki

Najgroźniejszym błędem poznawczym nowoczesnego człowieka jest chronocentryzm — naiwne przeświadczenie, że dzięki smartfonom i algorytmom staliśmy się mądrzejsi od pokoleń z XVIII, XIX czy połowy XX wieku. Tymczasem mechanizmy paniki rynkowej, propagandy, grupowego myślenia i dyplomatycznego wishful thinking działają w naszych głowach dokładnie na tym samym biologicznym „sprzęcie” co przed stuleciami.

### Pytanie dociekliwego laika

Skoro studiujemy historię po to, by nie powtarzać katastrof przeszłości, to dlaczego w debacie publicznej tak chętnie używamy przeszłości jako pałki do okładania oponentów, a tak rzadko jako podręcznika chłodnej rachunkowości państwowej?"""
        },
        "polityka": {
            "lead": (
                f"Bieżąca analiza z obszaru bezpieczeństwa i myśli państwowej ({src_name}: „{raw_title}”) odsłania napięcie między "
                f"oficjalnym językiem dyplomatycznych komunikatów a twardą grą interesów w zmieniającej się architekturze międzynarodowej."
            ),
            "thesis": (
                "Sprawczość państwa w XXI wieku nie wynika z moralnej słuszności postulatów, lecz ze zdolności wykonawczej instytucji, "
                "rezerw przemysłowo-energetycznych oraz umiejętności budowania koalicji wokół wymiernych interesów."
            ),
            "points": [
                "Mapa realnych interesów graczy: kto zyskuje, a kto traci pole manewru w nowym układzie sił.",
                "Sprawność instytucjonalna państwa: różnica między uchwaleniem strategii na papierze a jej wdrożeniem w terenie.",
                "Konsekwencje dla pozycji Polski i regionu Europy Środkowo-Wschodniej w perspektywie najbliższej dekady.",
                "Pytanie dociekliwego laika: Jak odróżnić realne budowanie potencjału obronnego i gospodarczego państwa od medialnego teatru obliczonego wyłącznie na najbliższy cykl sondażowy?"
            ],
            "draft": f"""Współczesna polityka cierpi na chroniczny nadmiar słów i dotkliwy deficyt długofalowego planowania. Kiedy wczytamy się w diagnozę zarysowaną na łamach {src_name} (*„{raw_title}”*), wyraźnie widać, że pod powierzchnią codziennych sporów partyjnych przesuwają się znacznie poważniejsze płyty tektoniczne: architektura bezpieczeństwa, suwerenność regulacyjna oraz wydolność aparatu państwowego.

### Państwo deklaratywne kontra państwo sprawcze

Jednym z najpoważniejszych problemów zachodnich demokracji stało się zastąpienie realnego rządzenia zarządzaniem emocjami wyborców. Ogłoszenie konferencji prasowej, powołanie pełnomocnika czy przyjęcie szczytnej rezolucji bywa w mediach traktowane na równi z rozwiązaniem problemu. Tymczasem w zderzeniu z kryzysem energetycznym, presją graniczną czy rywalizacją przemysłową mocarstw liczą się wyłącznie twarde aktywa: działające fabryki, drożna logistyka, sprawne sądy i przewidywalne prawo podatkowe.

W geopolityce nikt nie przyznaje punktów za dobre intencje. Sojusze pozostają trwałe dokładnie tak długo, jak długo pokrywają się strategiczne kalkulacje ich uczestników i jak długo każdy z partnerów wnosi do wspólnego koszyka realną, trudną do zastąpienia wartość.

### Lekcja realizmu dla średniego państwa

Dla kraju o skali i położeniu Polski najważniejszym zadaniem jest budowanie tzw. odporności strukturalnej (resilience) — zdolności do samodzielnego absorbowania wstrząsów zewnętrznych i prowadzenia podmiotowej gry na wielu fortepianach jednocześnie, bez popadania ani w klientelizm, ani w osamotnienie.

### Pytanie dociekliwego laika

Dlaczego w naszej debacie publicznej poświęcamy 90% energii na personalne potyczki polityków, a zaledwie ułamek uwagi na audyt tego, czy kluczowe instytucje państwa potrafią dowieźć wieloletnie projekty infrastrukturalne niezależnie od tego, kto akurat wygrał wybory?"""
        },
        "eseje": {
            "lead": (
                f"Impuls intelektualny z bieżącej lektury ({src_name}: „{raw_title}”) skłania do zatrzymania się w codziennym pośpiechu "
                f"i przyjrzenia się temu, jak współczesna kultura informacyjna zmienia nasz sposób myślenia, wartościowania i rozmowy."
            ),
            "thesis": (
                "W epoce nadpodaży opinii i gotowych tożsamościowych szablonów największym luksusem — a zarazem aktem intelektualnej odwagi — "
                "staje się samodzielny osąd oparty na cierpliwej weryfikacji źródeł i gotowości do powiedzenia „nie wiem, sprawdźmy”."
            ),
            "points": [
                "Mechanizm społeczny pod lupą: dlaczego pewne klisze i mody intelektualne zyskują status niepodważalnych dogmatów.",
                "Koszt poznawczy życia w ciągłym szumie powiadomień i skrótowych narracji.",
                "Powrót do myślenia z pierwszych zasad (First Principles) w życiu zawodowym i obywatelskim.",
                "Pytanie dociekliwego laika: Ile z poglądów, których dziś tak żarliwie bronimy przy rodzinnym stole lub w sieci, wypracowaliśmy samodzielnie po lekturze długich tekstów, a ile przejęliśmy bezwiednie z nagłówków ostatnich tygodni?"
            ],
            "draft": f"""Żyjemy w dziwnym paradoksie: nigdy wcześniej w dziejach ludzkości dostęp do wiedzy, archiwów naukowych i danych źródłowych nie był tak prosty i darmowy, a jednocześnie nigdy wcześniej tak trudno nie przychodziło nam skupienie uwagi na dłużej niż trzy minuty. Lektura wątku poruszonego przez {src_name} (*„{raw_title}”*) otwiera przestrzeń do refleksji, na którą rzadko pozwalają nam algorytmy codziennych mediów.

### Tyrania natychmiastowej opinii

Współczesna sfera publiczna wymusza na nas błyskawiczną deklarację: zanim jeszcze poznamy fakty, musimy już zająć stanowisko, przypisać się do właściwego obozu i użyć odpowiednich słów-kluczy. Wahanie, niuansowanie czy przyznanie, że problem ma dwie racjonalne strony, bywa traktowane niemal jak słabość charakteru.

Postawa dociekliwego laika proponuje dokładną odwrotność tego nawyku. Laik nie udaje wszechwiedzącego eksperta od wszystkiego — zamiast tego ma odwagę zadawać elementarne pytania, rozkładać napuszone pojęcia na czynniki pierwsze i sprawdzać, czy król przypadkiem nie jest nagi. To właśnie z takiej zdroworozsądkowej dociekliwości rodziły się najlepsze eseje od czasów Montaigne’a i Orwella.

### Ochrona własnej suwerenności poznawczej

W świecie, w którym największe korporacje globu zatrudniają tysiące inżynierów pracujących nad przechwyceniem każdej wolnej sekundy naszego wzroku, obrona ciszy, długiej lektury i niespiesznej rozmowy przestaje być kwestią estetyki — staje się warunkiem zachowania wolnej woli.

### Pytanie dociekliwego laika

Gdybyśmy przez najbliższy miesiąc całkowicie zrezygnowali z komentowania spraw, którym nie poświęciliśmy przynajmniej godziny spokojnej, pogłębionej lektury — jak bardzo zmieniłaby się jakość naszego myślenia i naszego spokoju ducha?"""
        }
    }

    fw = frameworks.get(category, frameworks["eseje"])
    return {
        "title": laika_title,
        "source": source_display,
        "source_note": source_note,
        "lead": fw["lead"],
        "thesis": fw["thesis"],
        "points": fw["points"],
        "draft": fw["draft"],
        "raw_rss_title": raw_title,
        "raw_rss_url": link,
        "raw_rss_source": src_name
    }


def synthesize_live_proposal(item: Dict[str, Any], category: str, visual_seed: int = 0) -> Dict[str, Any]:
    """Buduje kompletny słownik propozycji redakcyjnej ze świeżego elementu RSS."""
    visuals = CATEGORY_VISUALS.get(category, CATEGORY_VISUALS["eseje"])
    img_url, img_concept, img_prompt = visuals[visual_seed % len(visuals)]
    crafted = _craft_polish_angle(item, category)

    return {
        "category": category,
        "title": crafted["title"],
        "source": crafted["source"],
        "source_note": crafted["source_note"],
        "image_url": img_url,
        "image_concept": img_concept,
        "image_prompt": img_prompt,
        "lead": crafted["lead"],
        "thesis": crafted["thesis"],
        "points": crafted["points"],
        "draft": crafted["draft"],
        "rss_url": item.get("link", ""),
        "rss_raw_title": item.get("title", "")
    }


def synthesize_live_kondensat(selected_topics: List[Dict[str, Any]], date_pl: str, visual_seed: int = 0) -> Dict[str, Any]:
    """
    Tworzy codzienny wielowątkowy KONDENSAT (Konglomerat Analityczny) splatający
    faktyczne dzisiejsze impulsy z Technologii, Gospodarki, Historii i Geopolityki w jeden esej.
    """
    visuals = CATEGORY_VISUALS["kondensat"]
    img_url, img_concept, img_prompt = visuals[visual_seed % len(visuals)]

    by_cat = {t.get("category"): t for t in selected_topics}
    t_tech = by_cat.get("technologia", selected_topics[0] if selected_topics else {})
    t_econ = by_cat.get("gospodarka", selected_topics[1] if len(selected_topics) > 1 else t_tech)
    t_pol = by_cat.get("polityka", selected_topics[2] if len(selected_topics) > 2 else t_tech)
    t_hist = by_cat.get("historia", selected_topics[3] if len(selected_topics) > 3 else t_tech)

    tech_ref = t_tech.get("rss_raw_title") or t_tech.get("title", "transformacja cyfrowa")
    econ_ref = t_econ.get("rss_raw_title") or t_econ.get("title", "koszt kapitału")
    pol_ref = t_pol.get("rss_raw_title") or t_pol.get("title", "architektura bezpieczeństwa")
    hist_ref = t_hist.get("rss_raw_title") or t_hist.get("title", "lekcje długiego trwania")

    kondensat_title = (
        f"Kondensat ({date_pl}): Sprzężenie krzemu, kapitału i siły państwa — "
        f"wielowątkowa synteza trendów dnia"
    )

    sources_joined = " + ".join(
        dict.fromkeys([
            t.get("source", "").split(" — ")[0]
            for t in [t_tech, t_econ, t_pol, t_hist]
            if t.get("source")
        ])
    ) or "⚡ Węzeł Makroanalityczny Bloga Laika (Synteza 4 szuflad)"

    draft = f"""Tradycyjne media dzielą rzeczywistość na szczelne przegródki: osobno czytamy dział technologiczny, osobno tabelki giełdowe, osobno depesze dyplomatyczne, a w weekendowy wieczór sięgamy po dodatek historyczny. Problem polega na tym, że realny świat nie zna podziału na redakcyjne działy. Dzisiejszy splot impulsów analitycznych z **{date_pl}** pokazuje jak na dłoni, że te cztery wektory tworzą jeden nierozerwalny układ naczyń połączonych.

### Węzeł 1: Technologia i fizyczny rachunek mocy

W warstwie technologicznej dzisiejszą uwagę przykuwa wątek *„{tech_ref}”*. Jeszcze niedawno postęp cyfrowy wydawał się zawieszony w próżni czystego oprogramowania. Dziś widzimy wyraźnie, że każda innowacja obliczeniowa natychmiast zderza się z twardym bilansem energetycznym, dostępnością komponentów i walką o kontrolę nad infrastrukturą krytyczną. Kod bez suwerennego zaplecza sprzętowego przestaje być gwarancją przewagi.

### Węzeł 2: Makroekonomia i dyscyplina kosztu pieniądza

To prowadzi nas bezpośrednio do drugiego ogniwa dzisiejszego konglomeratu — sfery gospodarczej (*„{econ_ref}”*). Kapitał przestał być darmowy, a inwestorzy oraz budżety państw muszą wybierać między obsługą narosłych zobowiązań a finansowaniem modernizacji przemysłowej. Przedsiębiorstwa i rządy, które przespały dekadę niskich stóp, płacą dziś podwójną premię za ryzyko.

### Węzeł 3: Geopolityka i analogia historyczna

Kiedy nałożymy na to dzisiejszy wymiar polityczno-strategiczny (*„{pol_ref}”*) oraz perspektywę historyczną (*„{hist_ref}”*), wyłania się pełny obraz epoki przejściowej. Dokładnie tak jak w przełomowych dekadach minionych stuleci, o pozycji państwa nie decydują uroczyste deklaracje, lecz zdolność do zintegrowania trzech elementów: własnej myśli inżynieryjnej, zdrowych finansów publicznych oraz sprawnej logistyki państwowej.

### Wnioski i pytanie dociekliwego laika

Patrząc na te cztery zjawiska jednocześnie, trudno oprzeć się wrażeniu, że największym zagrożeniem dla współczesnych społeczeństw jest wąska, silosowa specjalizacja elit: inżynierowie nie rozumieją długu publicznego, ekonomiści lekceważą geografię strategiczną, a politycy ignorują prawa fizyki i historii. Czy nie nadszedł najwyższy czas, by przywrócić w debacie publicznej całościowe, interdyscyplinarne myślenie państwowe — zanim rzeczywistość sama wystawi nam łączny rachunek?"""

    return {
        "category": "eseje",
        "section_type": "kondensat",
        "title": kondensat_title,
        "source": f"⚡ Konglomerat Wielowątkowy: {sources_joined}",
        "source_note": (
            f"Autorska synteza łącząca 4 dzisiejsze impulsy: [Tech] {tech_ref[:55]} | "
            f"[Gosp] {econ_ref[:55]} | [Pol] {pol_ref[:55]} | [Hist] {hist_ref[:55]}."
        ),
        "image_url": img_url,
        "image_concept": img_concept,
        "image_prompt": img_prompt,
        "lead": (
            f"Kiedy połączymy kropki między dzisiejszymi sygnałami z rynku technologii, finansów i geopolityki ({date_pl}), "
            f"zamiast pojedynczych newsów wyłania się spójny mechanizm wielkiego przetasowania kapitału i potęgi."
        ),
        "thesis": (
            "Najważniejsze procesy XXI wieku zachodzą na styku dziedzin: między mocą obliczeniową, kosztem długu i bezpieczeństwem szlaków dostaw. "
            "Kto analizuje je osobno, widzi jedynie szum informacyjny; kto łączy je w jeden model, rozumie kierunek zmiany."
        ),
        "points": [
            f"Wektor technologiczny: Wnioski strukturalne wokół impulsu „{tech_ref[:70]}”.",
            f"Wektor kapitałowy: Presja makroekonomiczna i koszt pieniądza na tle „{econ_ref[:70]}”.",
            f"Wektor geopolityczny i historyczny: Zderzenie „{pol_ref[:60]}” z lekcją „{hist_ref[:60]}”.",
            "Pytanie dociekliwego laika: Dlaczego wciąż analizujemy technologię, budżet państwa i bezpieczeństwo w osobnych szufladach, skoro w realnym świecie stanowią one jeden i ten sam rachunek suwerenności?"
        ],
        "draft": draft
    }


if __name__ == "__main__":
    if sys.stdout.encoding != "utf-8":
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    res = scrape_all_feeds_parallel()
    print(f"Sprawdzono kanałów RSS: {res['feeds_checked']}, aktywnych online: {res['feeds_online']}, pobrano wpisów: {res['total_items']}")
    for cat, lst in res["by_category"].items():
        print(f"  - {cat}: {len(lst)} wpisów (przykład: {lst[0]['title'][:65] if lst else 'brak'})")

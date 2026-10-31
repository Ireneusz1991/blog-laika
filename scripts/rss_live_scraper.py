# -*- coding: utf-8 -*-
"""
scripts/rss_live_scraper.py
============================
Autonomiczny skraper feedów RSS i silnik samokreacji redakcyjnej dla Bloga Laika.
Pobiera na żywo najświeższe impulsy faktograficzne z 34 monitorowanych źródeł,
weryfikuje brak duplikatów przez ArticleDeduplicator i przekształca je
w autorskie propozycje redakcyjne z gotowymi szkicami esejów.
"""

import os
import sys
import re
import json
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Optional, Tuple, Any

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from scripts.sources_registry import EDITORIAL_SOURCES
from scripts.article_deduplicator import deduplicator

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"

# Zdjęcia i koncepcje wizualne dla poszczególnych kategorii
CATEGORY_VISUALS = {
    "technologia": [
        ("https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?auto=format&fit=crop&w=1200&q=80",
         "Matryca układu krzemowego procesora nowej generacji z chłodnym błękitnym oświetleniem magistrali danych.",
         "Editorial photograph of advanced silicon microchip die, gleaming golden circuitry, cold blue illumination, macroeconomic technology journalism style, 8k."),
        ("https://images.unsplash.com/photo-1518770660439-4636190af475?auto=format&fit=crop&w=1200&q=80",
         "Zbliżenie na płytę główną serwera z magistralami optycznymi i pamięcią HBM.",
         "Close up architectural view of high-bandwidth memory server motherboard, optical bus lines, depth of field, 8k."),
        ("https://images.unsplash.com/photo-1504639725590-34d0984388bd?auto=format&fit=crop&w=1200&q=80",
         "Stacja robocza inżyniera z otwartą architekturą kodu i schematami algorytmów.",
         "Moody editorial photo of software engineer desk with algorithmic data structures on ultra-wide screens, natural shadows, 8k.")
    ],
    "gospodarka": [
        ("https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=1200&q=80",
         "Szklana fasada giełdy i wieżowców finansowych odbijająca dynamiczne niebo.",
         "Dramatic low angle view of financial district skyscrapers, cold steel and glass architecture, Financial Times photography style, 8k."),
        ("https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?auto=format&fit=crop&w=1200&q=80",
         "Wykresy obligacji skarbowych i dynamiki stóp procentowych na surowym, ciemnym ekranie analitycznym.",
         "Financial terminal analytics display, macro yield curve charts, high contrast editorial photo, 8k."),
        ("https://images.unsplash.com/photo-1590283603385-17ffb3a7f29f?auto=format&fit=crop&w=1200&q=80",
         "Kontenery handlowe w porcie przeładunkowym symbolizujące fizyczne łańcuchy dostaw.",
         "Industrial cargo container terminal at dusk, towering gantry cranes, heavy economic realism, 8k.")
    ],
    "historia": [
        ("https://images.unsplash.com/photo-1461360370896-922624d12aa1?auto=format&fit=crop&w=1200&q=80",
         "Zabytkowe mapy szlaków handlowych i dokumenty traktatowe w świetle lampy bibliotecznej.",
         "Still life of antique maritime trade maps, parchment documents, brass magnifying glass, historical investigative journalism, 8k."),
        ("https://images.unsplash.com/photo-1509198397868-475647b2a1e5?auto=format&fit=crop&w=1200&q=80",
         "Kamienne kolumny starożytnego akweduktu lub forum na tle surowego krajobrazu.",
         "Atmospheric historical photography of ancient Roman aqueduct arches, weathered limestone, dramatic side lighting, 8k."),
        ("https://images.unsplash.com/photo-1455390582262-044cdead277a?auto=format&fit=crop&w=1200&q=80",
         "Rękopisy archiwalne i stare pieczęcie państwowe symbolizujące mechanizmy dawnej dyplomacji.",
         "Close up of historical diplomatic archives, bound leather folios, wax seals, archival warmth, 8k.")
    ],
    "polityka": [
        ("https://images.unsplash.com/photo-1541872703-74c5e44368f9?auto=format&fit=crop&w=1200&q=80",
         "Monumentalny gmach parlamentu lub instytucji państwowej z flagami w chłodnym świetle o poranku.",
         "Symmetrical architectural photograph of neoclassical government ministry building, solemn marble facade, 8k."),
        ("https://images.unsplash.com/photo-1529107386315-e1a2ed48a620?auto=format&fit=crop&w=1200&q=80",
         "Pusta sala obrad międzynarodowego szczytu geopolitycznego z mikrofonami i pulpitami.",
         "Empty diplomatic summit conference hall, clean microphones on wooden desks, cool ambient light, Foreign Affairs magazine style, 8k."),
        ("https://images.unsplash.com/photo-1451187580459-43490279c0fa?auto=format&fit=crop&w=1200&q=80",
         "Satelitarny widok przesmyków morskich i granic kontynentalnych w mroku nocy.",
         "Geopolitical satellite perspective of Baltic sea choke points and maritime borders, glowing infrastructure, 8k.")
    ],
    "eseje": [
        ("https://images.unsplash.com/photo-1507842229452-78d10a4e7039?auto=format&fit=crop&w=1200&q=80",
         "Klimatyczna, przestronna biblioteka z wysokimi regałami i światłem wpadającym przez wielkie okno.",
         "Warm editorial interior of classical library, endless bookshelves, sunlight streaming through towering windows, intellectual curiosity, 8k."),
        ("https://images.unsplash.com/photo-1499750310107-5fef28a66643?auto=format&fit=crop&w=1200&q=80",
         "Notatnik dociekliwego eseisty z piórem wiecznym i filiżanką czarnej kawy przy drewnianym stole.",
         "Minimalist essayist desk with open notebook, fountain pen, morning light, calm contemplative mood, 8k."),
        ("https://images.unsplash.com/photo-1457369804613-52c61a468e7d?auto=format&fit=crop&w=1200&q=80",
         "Otwarta książka z widoczną typografią i grą cieni na zadrukowanych stronach.",
         "Extreme close up of open book pages with classic serif typography, tactile paper texture, intellectual prose, 8k.")
    ],
    "kondensat": [
        ("https://images.unsplash.com/photo-1509228468518-180dd4864904?auto=format&fit=crop&w=1200&q=80",
         "Złożona sieć światłowodowa i magistrale surowcowe łączące kontynenty w jeden wielowątkowy węzeł.",
         "Conceptual editorial photograph of illuminated global infrastructure nodes, deep fiber optic blue and amber energy pipelines intersecting, 8k."),
        ("https://images.unsplash.com/photo-1518709268805-4e9042af9f23?auto=format&fit=crop&w=1200&q=80",
         "Abstrakcyjna geometria węzła wielowątkowego syntetyzująca technologię, energię i finanse.",
         "Futuristic macro photography of complex multilayered silicon prism refracting industrial light beams, high intellect konglomerat analysis, 8k.")
    ]
}

def clean_html(raw_html: str) -> str:
    """Usuwa znaczniki HTML i encje z tekstu opisu RSS."""
    if not raw_html:
        return ""
    text = re.sub(r'<[^>]+>', ' ', raw_html)
    text = text.replace('&amp;', '&').replace('&quot;', '"').replace('&#39;', "'").replace('&lt;', '<').replace('&gt;', '>')
    return re.sub(r'\s+', ' ', text).strip()

def fetch_feed_items(rss_url: str, max_items: int = 15) -> List[Dict[str, str]]:
    """Pobiera i parsuje elementy z pojedynczego kanału RSS/Atom."""
    items_out = []
    try:
        req = urllib.request.Request(rss_url, headers={"User-Agent": USER_AGENT})
        with urllib.request.urlopen(req, timeout=4) as resp:
            data = resp.read()
            root = ET.fromstring(data)
            
            # RSS 2.0
            items = root.findall(".//item")
            if items:
                for it in items[:max_items]:
                    t_elem = it.find("title")
                    l_elem = it.find("link")
                    d_elem = it.find("description")
                    title = t_elem.text.strip() if t_elem is not None and t_elem.text else ""
                    link = l_elem.text.strip() if l_elem is not None and l_elem.text else ""
                    desc = clean_html(d_elem.text) if d_elem is not None and d_elem.text else ""
                    if title and link:
                        items_out.append({"title": title, "link": link, "summary": desc})
                return items_out

            # Atom
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
                    s_elem = it.find("summary")
                
                title = t_elem.text.strip() if t_elem is not None and t_elem.text else ""
                link = ""
                if l_elem is not None:
                    link = l_elem.get("href", "") or (l_elem.text or "").strip()
                desc = clean_html(s_elem.text) if s_elem is not None and s_elem.text else ""
                if title and link:
                    items_out.append({"title": title, "link": link, "summary": desc})
    except Exception:
        pass
    return items_out

def scrape_category_feeds(category: str) -> List[Dict[str, Any]]:
    """Pobiera wszystkie świeże elementy ze źródeł przypisanych do danej kategorii."""
    cat_sources = [s for s in EDITORIAL_SOURCES if s.get("blog_category") == category and s.get("rss")]
    collected = []
    for src in cat_sources:
        rss = src.get("rss")
        src_name = src.get("name", "Źródło branżowe")
        items = fetch_feed_items(rss, max_items=10)
        for it in items:
            it["source_name"] = src_name
            it["source_id"] = src.get("id", "")
            it["category"] = category
            collected.append(it)
    return collected

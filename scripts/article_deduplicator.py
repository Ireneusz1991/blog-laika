# -*- coding: utf-8 -*-
"""
scripts/article_deduplicator.py
================================
Silnik deduplikacji i rejestr historii pobranych/zaproponowanych/opublikowanych artykułów.
Gwarantuje, że:
1. Żaden artykuł opublikowany już na blogu nie zostanie ponownie zaproponowany.
2. Żaden temat zaproponowany w ciągu ostatnich 45 dni nie zostanie zduplikowany.
3. Żaden artykuł z feedów RSS o tym samym URL lub tożsamym tytule/tezie nie pojawi się ponownie.
"""

import os
import re
import sys
import json
import glob
from datetime import datetime, timedelta

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REGISTRY_FILE = os.path.join(ROOT_DIR, "data", "seen_articles_registry.json")

# Polskie i angielskie słowa pospolite (stopwords) do usuwania przy analizie podobieństwa
STOPWORDS = {
    "i", "w", "z", "na", "do", "o", "to", "jak", "dla", "czy", "nie", "się", "ze", "za",
    "po", "od", "że", "co", "a", "oraz", "jest", "są", "być", "ten", "ta", "te", "tym",
    "tych", "też", "już", "ale", "jej", "jego", "ich", "przez", "przy", "we", "the", "a",
    "an", "in", "on", "at", "to", "for", "of", "and", "or", "is", "are", "why", "how", "what"
}

def normalize_text(text: str) -> str:
    """Normalizuje tekst: małe litery, usunięcie cudzysłowów, znaków interpunkcyjnych i spacji."""
    if not text:
        return ""
    text = text.lower()
    # Usuwanie znaków specjalnych
    text = re.sub(r'[„”"\'`«»\(\)\[\]\{\}\:\;\.\,\?\!\—\-\–\/]', ' ', text)
    # Usuwanie wielokrotnych spacji
    tokens = [w.strip() for w in text.split() if len(w.strip()) > 1 and w.strip() not in STOPWORDS]
    return " ".join(tokens)

def get_tokens(text: str) -> set:
    norm = normalize_text(text)
    return set(norm.split())

def token_similarity(text1: str, text2: str) -> float:
    """Oblicza indeks Jaccarda dla dwóch tytułów."""
    tokens1 = get_tokens(text1)
    tokens2 = get_tokens(text2)
    if not tokens1 or not tokens2:
        return 0.0
    intersection = tokens1.intersection(tokens2)
    union = tokens1.union(tokens2)
    return len(intersection) / len(union)

class ArticleDeduplicator:
    def __init__(self, registry_path: str = REGISTRY_FILE):
        self.registry_path = registry_path
        self.registry = {
            "published_articles": [],    # [{"id": 1, "title": "...", "slug": "..."}]
            "proposed_history": [],      # [{"date": "2026-10-31", "category": "technologia", "title": "...", "url": "..."}]
            "seen_rss_urls": {},         # {"url": {"title": "...", "seen_date": "2026-10-31"}}
            "last_updated": ""
        }
        self.load()
        self.sync_with_database()
        self.sync_with_proposals_folder()

    def load(self):
        if os.path.exists(self.registry_path):
            try:
                with open(self.registry_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.registry.update(data)
            except Exception as e:
                print(f"[Deduplicator] Błąd odczytu rejestru ({e}), tworzenie nowego.")

    def save(self):
        os.makedirs(os.path.dirname(self.registry_path), exist_ok=True)
        self.registry["last_updated"] = datetime.now().isoformat()
        try:
            with open(self.registry_path, "w", encoding="utf-8") as f:
                json.dump(self.registry, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"[Deduplicator] Błąd zapisu rejestru: {e}")

    def sync_with_database(self):
        """Pobiera wszystkie opublikowane artykuły z bazy SQLite."""
        try:
            if ROOT_DIR not in sys.path:
                sys.path.insert(0, ROOT_DIR)
            import database
            raw_posts = database.get_posts(limit=200)
            published = []
            for p in raw_posts:
                published.append({
                    "id": p.get("id"),
                    "title": p.get("title", ""),
                    "slug": p.get("slug", ""),
                    "category": p.get("category", "")
                })
            self.registry["published_articles"] = published
        except Exception as e:
            print(f"[Deduplicator] Uwaga: nie udało się zsynchronizować z bazą danych: {e}")

    def sync_with_proposals_folder(self):
        """Skanuje wszystkie istniejące pliki w propozycje-tematow/ i rejestruje ich tytuły."""
        prop_dir = os.path.join(ROOT_DIR, "propozycje-tematow")
        if not os.path.exists(prop_dir):
            return

        existing_titles = {item.get("title").strip().lower() for item in self.registry["proposed_history"] if item.get("title")}

        for fpath in glob.glob(os.path.join(prop_dir, "propozycje-*.md")):
            fname = os.path.basename(fpath)
            # data z nazwy pliku
            date_match = re.search(r'propozycje-(\d{4}-\d{2}-\d{2})\.md', fname)
            f_date = date_match.group(1) if date_match else ""

            try:
                with open(fpath, "r", encoding="utf-8") as f:
                    content = f.read()
                
                # Wyciągnij nagłówki ##
                for line in content.splitlines():
                    line = line.strip()
                    if line.startswith("## ") and not line.startswith("### "):
                        title = line[3:].strip()
                        if ":" in title:
                            title = title.split(":", 1)[1].strip().strip('„”"\'')
                        
                        if title and title.lower() not in existing_titles:
                            self.registry["proposed_history"].append({
                                "date": f_date,
                                "category": "unknown",
                                "title": title,
                                "url": ""
                            })
                            existing_titles.add(title.lower())
            except Exception as e:
                print(f"[Deduplicator] Błąd czytania {fname}: {e}")

        self.save()

    def is_duplicate(self, candidate_title: str, candidate_url: str = None, category: str = None, similarity_threshold: float = 0.45, ignore_date: str = None) -> tuple[bool, str]:
        """
        Główna funkcja weryfikująca, czy dany artykuł jest duplikatem.
        Zwraca: (is_dup: bool, reason: str)
        """
        if not candidate_title or not candidate_title.strip():
            return True, "Pusty tytuł"

        cand_norm = normalize_text(candidate_title)
        cand_tokens = get_tokens(candidate_title)

        # 1. Sprawdź URL (jeśli podano z RSS)
        if candidate_url and candidate_url in self.registry.get("seen_rss_urls", {}):
            seen_info = self.registry["seen_rss_urls"][candidate_url]
            return True, f"Identyczny URL RSS był już pobrany ({seen_info.get('seen_date')}: {seen_info.get('title')})"

        # 2. Sprawdź czy to nie jest artykuł JUŻ OPUBLIKOWANY na blogu
        for pub in self.registry.get("published_articles", []):
            pub_title = pub.get("title", "")
            sim = token_similarity(candidate_title, pub_title)
            if sim >= similarity_threshold or cand_norm in normalize_text(pub_title) or normalize_text(pub_title) in cand_norm:
                return True, f"DUPLIKAT OPUBLIKOWANEGO WPISU: Artykuł o tożsamej treści jest już na blogu! (ID {pub.get('id')}: \"{pub_title}\", podobieństwo: {sim:.0%})"

        # 3. Sprawdź historię propozycji z ostatnich 45 dni
        for prop in self.registry.get("proposed_history", []):
            prop_date = prop.get("date", "")
            if ignore_date and prop_date == ignore_date:
                continue
            prop_title = prop.get("title", "")
            sim = token_similarity(candidate_title, prop_title)
            if sim >= similarity_threshold or cand_norm in normalize_text(prop_title) or normalize_text(prop_title) in cand_norm:
                return True, f"DUPLIKAT NIEDAWNEJ PROPOZYCJI: Temat był już proponowany ({prop_date}: \"{prop_title}\", podobieństwo: {sim:.0%})"

        return False, "Unikalny artykuł"

    def register_seen(self, title: str, category: str, url: str = None, date_str: str = None):
        """Rejestruje zaakceptowany, unikalny artykuł w historii."""
        if not date_str:
            date_str = datetime.now().strftime("%Y-%m-%d")

        if url:
            self.registry.setdefault("seen_rss_urls", {})[url] = {
                "title": title,
                "seen_date": date_str,
                "category": category
            }

        self.registry.setdefault("proposed_history", []).append({
            "date": date_str,
            "category": category,
            "title": title,
            "url": url or ""
        })
        self.save()

# Globalny singleton
deduplicator = ArticleDeduplicator()

if __name__ == "__main__":
    print("=== DEDUPLICATOR STATUS ===")
    print(f"Published articles: {len(deduplicator.registry['published_articles'])}")
    print(f"Proposed history items: {len(deduplicator.registry['proposed_history'])}")
    print(f"Seen RSS URLs: {len(deduplicator.registry['seen_rss_urls'])}")

    # Test duplicate checks
    test_cases = [
        "Anatomia kryzysu sueskiego 1956",
        "Kondensat: Wielkie sprzężenie zwrotne — jak kryzys energetyczny",
        "Pochwała dociekliwego laika: Dlaczego w epoce wąskich specjalizacji",
        "Koniec dyktatu gigantycznych chmur? Dlaczego małe modele (SLM)",
        "Zupełnie nowy, unikalny esej o neurobiologii sztucznej inteligencji"
    ]
    print("\nTesty detekcji duplikatów:")
    for tc in test_cases:
        is_dup, reason = deduplicator.is_duplicate(tc)
        print(f"  [{'DUPLIKAT' if is_dup else 'UNIKALNY'}] \"{tc}\" -> {reason}")

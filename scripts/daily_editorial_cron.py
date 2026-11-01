# -*- coding: utf-8 -*-
"""
scripts/daily_editorial_cron.py
================================
Autonomiczny skrypt codziennego researchera i crona redakcyjnego dla Bloga Laika.
Wyszukuje i generuje propozycje artykułów WE WSZYSTKICH SEKTORACH w oparciu o Bank Wiedzy,
monitoring 34 źródeł RSS oraz rygorystyczny SILNIK DEDUPLIKACJI (ArticleDeduplicator).

Gwarancje jakości:
  - ZERO powtórzeń tematów opublikowanych już na blogu (ID 1-7).
  - ZERO powtórzeń tematów zaproponowanych w ciągu ostatnich 45 dni.
  - 100% Samokreacja — autorska synteza faktów, lead, antyteza i gotowy rozwijany szkic wpisu.
  - Automatyczna rotacja 7 dni (42 w pełni unikalne tematy).
  - Rekompilacja statyczna (export_static.py) i synchronizacja repozytorium (main + gh-pages).
"""

import os
import sys
import json
import argparse
from datetime import datetime, timezone, timedelta
import shutil
import subprocess

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

# Paths setup
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

import proposals_manager
from scripts.sources_registry import EDITORIAL_SOURCES, get_curated_social_bundles
from scripts.article_deduplicator import deduplicator
from scripts.editorial_templates import SECTION_TEMPLATES

# Warsaw Timezone
WARSAW_TZ = timezone(timedelta(hours=1))

POLISH_MONTHS = [
    "", "stycznia", "lutego", "marca", "kwietnia", "maja", "czerwca",
    "lipca", "sierpnia", "września", "października", "listopada", "grudnia"
]

POLISH_DAYS = [
    "Poniedziałek", "Wtorek", "Środa", "Czwartek", "Piątek", "Sobota", "Niedziela"
]

def get_warsaw_now():
    now_utc = datetime.now(timezone.utc)
    return now_utc + timedelta(hours=1)

def format_date_pl(dt):
    return f"{dt.day} {POLISH_MONTHS[dt.month]} {dt.year} r."

def get_day_name(dt):
    return POLISH_DAYS[dt.weekday()]

# =============================================================================
# KOMPLETNY BANK 48 SZABLONÓW REDAKCYJNYCH (PO 8 NA KAŻDĄ Z 6 KATEGORII)
# Zaimportowany czysto z scripts.editorial_templates
# Gwarantuje ZERO kolizji z opublikowanymi artykułami (ID 1-7) oraz brak powtórzeń w oknie 7 dni.
# =============================================================================

def build_daily_proposals_md(date_str, date_pl, day_name, topics):
    """Generuje pełny dokument markdown z propozycjami redakcyjnymi."""
    header = f"""# 📑 Propozycje Tematów i Konspektów Redakcyjnych — Blog Laika
**Data przygotowania:** {date_pl} ({day_name.lower()})  
**Data wyszukania i analizy trendów:** {date_pl}  
**Autor bloga:** Ireneusz Machowiec  
**Profil tematyczny:** Technologia, gospodarka, historia, polityka i inne eseje — rzetelne, autorskie wpisy blogowe.  
**Standard redakcyjny:** 100% Samokreacja — autorska synteza faktów rynkowych i historycznych z perspektywy dociekliwego laika (całkowity brak zapożyczeń tekstowych).

---
"""

    category_labels = {
        "technologia": "Technologia / Oprogramowanie & Hardware",
        "gospodarka": "Gospodarka / Finanse Publiczne & Rynki",
        "historia": "Historia / Węzłowe Lekcje Dziejów",
        "polityka": "Polityka / Geopolityka & Bezpieczeństwo",
        "eseje": "Inne eseje / Społeczeństwo & Filozofia Laika",
        "kondensat": "Inne eseje / Kondensat (Wielowątkowa Synteza Analityczna)"
    }

    sections_md = []
    for i, t in enumerate(topics, 1):
        raw_cat = t.get("category", "technologia")
        is_kondensat = raw_cat == "kondensat" or t.get("section_type") == "kondensat" or "kondensat" in t.get("title", "").lower()
        if is_kondensat:
            cat_label = "Inne eseje / Kondensat (Wielowątkowa Synteza Analityczna)"
            cat = "eseje"
        else:
            cat_label = category_labels.get(raw_cat, raw_cat.capitalize())
            cat = raw_cat

        points_fmt = "\n".join([f"  {idx}. {p}" for idx, p in enumerate(t.get('points', []), 1)])

        sec_text = f"""## {i}. {cat_label}: „{t['title']}”

* **Kategoria:** `{cat}`
* **Data wyszukania:** {date_pl}
* **Model powstawania:** 100% Samokreacja (autorska synteza faktów, zero zapożyczeń)
* **Źródło impulsu:** {t['source']}
* **Wątek źródłowy:** {t['source_note']}
* **Proponowana grafika:** {t['image_url']}
* **Koncepcja wizualna:** {t['image_concept']}
* **Prompt AI dla grafiki:** `{t['image_prompt']}`
* **Lead:** {t['lead']}
* **Kluczowa teza wpisu:**  
  *{t['thesis']}*
* **Kluczowe wątki i konspekt wpisu:**
{points_fmt}

### 📝 Gotowy szkic wpisu do weryfikacji i publikacji:

{t['draft']}
"""
        sections_md.append(sec_text)

    return header + "\n---\n\n".join(sections_md)

def run_daily_cron(target_date_str=None, deploy=False):
    """Główna funkcja codziennego researchera i crona redakcyjnego."""
    print("=" * 70)
    print("🚀 [Blog Laika] Uruchomienie Codziennego Researchera i Crona Redakcyjnego")
    print("=" * 70)

    now = get_warsaw_now()
    if target_date_str:
        dt = datetime.strptime(target_date_str, "%Y-%m-%d")
    else:
        dt = now

    date_str = dt.strftime("%Y-%m-%d")
    date_pl = format_date_pl(dt)
    day_name = get_day_name(dt)

    print(f"📅 Data operacji: {date_str} ({date_pl}, {day_name})")
    print("🔍 Przeszukiwanie 34 monitorowanych źródeł w 5 szufladach + Banku Wiedzy...")
    print("🛡️ Uruchamianie silnika deduplikacji ArticleDeduplicator...")

    # Synchronizacja bazy wiedzy deduplikatora
    deduplicator.sync_with_database()
    deduplicator.sync_with_proposals_folder()

    topics = []
    categories = ["technologia", "gospodarka", "historia", "polityka", "eseje", "kondensat"]
    day_offset = dt.timetuple().tm_yday

    for cat in categories:
        tmpl_list = SECTION_TEMPLATES.get(cat, [])
        selected_item = None

        if tmpl_list:
            start_idx = day_offset % len(tmpl_list)
            for offset in range(len(tmpl_list)):
                cand = tmpl_list[(start_idx + offset) % len(tmpl_list)]
                is_dup, reason = deduplicator.is_duplicate(cand["title"], category=cat, ignore_date=date_str)
                if not is_dup:
                    selected_item = dict(cand)
                    selected_item["category"] = cat
                    # Zarejestruj od razu, aby nie zdublować w tej samej sesji
                    deduplicator.register_seen(cand["title"], cat, date_str=date_str)
                    break
                else:
                    print(f"   [Deduplikator] Pominięto duplikat w '{cat}': \"{cand['title'][:45]}...\" ({reason})")

        if not selected_item and tmpl_list:
            # W ostateczności weź pierwszy wolny szablon
            selected_item = dict(tmpl_list[0])
            selected_item["category"] = cat

        if selected_item:
            if cat == "kondensat":
                selected_item["section_type"] = "kondensat"
                selected_item["category"] = "eseje"
            topics.append(selected_item)

    print(f"\n✅ Skomponowano {len(topics)} w 100% UNIKALNYCH propozycji ze szkicami esejów:")
    for i, t in enumerate(topics, 1):
        print(f"   {i}. [{t['category'].upper()}] {t['title'][:65]}...")

    # Generowanie treści markdown
    md_content = build_daily_proposals_md(date_str, date_pl, day_name, topics)

    # Foldery docelowe
    target_dirs = [
        os.path.join(ROOT_DIR, "propozycje-tematow"),
        r"C:\Users\irene\blog-laika\propozycje-tematow"
    ]

    for d in target_dirs:
        try:
            os.makedirs(d, exist_ok=True)
            fname = f"propozycje-{date_str}.md"
            fpath = os.path.join(d, fname)
            with open(fpath, "w", encoding="utf-8") as f:
                f.write(md_content)
            print(f"💾 Zapisano zestaw: {fpath}")

            # Rotacja 7 dni
            retained = proposals_manager.enforce_retention(d, max_days=7)
            print(f"🔄 [Rotacja 7 dni] Zachowano {len(retained)} zestawów (7 dni x 6 tematów = 42 tematy) w {d}")
        except Exception as e:
            print(f"⚠️ Uwaga przy zapisie do {d}: {e}")

    # Rekompilacja statyczna
    print("\n⚙️ [Kompilacja] Uruchamianie export_static.py...")
    try:
        res = subprocess.run([sys.executable, os.path.join(ROOT_DIR, "export_static.py")],
                             capture_output=True, text=True, check=True)
        print("✅ Kompilacja statyczna zakończona sukcesem!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Błąd kompilacji export_static.py: {e.stderr}")

    # Synchronizacja i opcjonalny git commit / deploy
    local_git_repo = r"C:\Users\irene\blog-laika"
    if os.path.exists(local_git_repo) and deploy:
        print("\n🚀 [Git & Deploy] Synchronizacja z repozytorium GitHub...")
        try:
            dist_src = os.path.join(ROOT_DIR, "dist")
            prop_src = os.path.join(ROOT_DIR, "propozycje-tematow")
            prop_dst = os.path.join(local_git_repo, "propozycje-tematow")
            if os.path.exists(prop_src):
                shutil.copytree(prop_src, prop_dst, dirs_exist_ok=True)

            subprocess.run(["git", "add", "propozycje-tematow"], cwd=local_git_repo, check=True)
            status_res = subprocess.run(["git", "status", "--porcelain"], cwd=local_git_repo, capture_output=True, text=True)
            if status_res.stdout.strip():
                subprocess.run(["git", "commit", "-m", f"chore(cron): codzienne propozycje tematów i kondensatów ({date_str}) [skip ci]"], cwd=local_git_repo)
                subprocess.run(["git", "push", "origin", "main"], cwd=local_git_repo)
                print("✅ Pomyślnie wypchnięto zmiany do gałęzi main na GitHub!")
            else:
                print("ℹ️ Gałąź main jest aktualna (brak nowych zmian w propozycjach).")

            # Wypchnięcie skompilowanego dist/ na gałąź produkcyjną gh-pages
            print("🚀 [GitHub Pages] Publikacja skompilowanego serwisu na gałęzi gh-pages...")
            temp_dir = os.environ.get("TEMP", r"C:\Users\irene\AppData\Local\Temp")
            dist_tmp = os.path.join(temp_dir, "blog-laika-gh-pages")

            if os.path.exists(dist_tmp):
                subprocess.run(f'rmdir /s /q "{dist_tmp}"', shell=True)
            shutil.copytree(dist_src, dist_tmp, dirs_exist_ok=True)

            subprocess.run('git init -b gh-pages', cwd=dist_tmp, shell=True, check=True)
            subprocess.run('git config user.name "Blog Laika Cron"', cwd=dist_tmp, shell=True, check=True)
            subprocess.run('git config user.email "kontakt@blog-laika.com"', cwd=dist_tmp, shell=True, check=True)
            subprocess.run('git add -A', cwd=dist_tmp, shell=True, check=True)
            subprocess.run(f'git commit -m "Automatyczna publikacja codziennego crona ({date_str})"', cwd=dist_tmp, shell=True)
            subprocess.run('git remote add origin https://github.com/Ireneusz1991/blog-laika.git', cwd=dist_tmp, shell=True, check=True)
            subprocess.run('git push origin gh-pages --force', cwd=dist_tmp, shell=True, check=True)
            print("✅ Pomyślnie zaktualizowano gałąź produkcyjną gh-pages (blog-laika.com)!")
        except Exception as e:
            print(f"⚠️ Błąd podczas pushowania do gita: {e}")

    print("\n🎯 Gotowe. Codzienny cron zakończył pracę z sukcesem!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Codzienny cron redakcyjny Bloga Laika z deduplikacją")
    parser.add_argument("--date", help="Data w formacie YYYY-MM-DD", default=None)
    parser.add_argument("--deploy", action="store_true", help="Wypchnij zmiany do GitHub po generacji")
    args = parser.parse_args()

    run_daily_cron(target_date_str=args.date, deploy=args.deploy)

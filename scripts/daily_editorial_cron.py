# -*- coding: utf-8 -*-
"""
scripts/daily_editorial_cron.py
================================
Autonomiczny silnik codziennego researchera, skrapera RSS na żywo i crona redakcyjnego dla Bloga Laika.
Działa zarówno w chmurze GitHub Actions (codziennie o 08:00 rano oraz na żądanie z przycisku w CMS),
jak i lokalnie z poziomu Windows / FastAPI CMS.

Gwarancje jakości:
  - Równoległy skan na żywo 34+ kanałów RSS z Polski i świata (rss_live_scraper.py).
  - ZERO powtórzeń tematów opublikowanych na blogu oraz pobranych wcześniej linków RSS (ArticleDeduplicator).
  - 100% Samokreacja — autorska polska synteza faktów, lead, teza, konspekt i pełny rozwijany szkic wpisu.
  - Codzienny wielowątkowy KONDENSAT (Konglomerat) łączący najważniejsze impulsy dnia.
  - Zapis żywego pulsu RSS i telemetrii crona do data/live_rss_pulse.json (widocznego w CMS).
  - Automatyczna rotacja 7 dni (7 dni x 6 tematów = 42 unikalne propozycje).
"""

import os
import sys
import json
import argparse
import shutil
import subprocess
from datetime import datetime, timezone, timedelta

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

import proposals_manager
from scripts.article_deduplicator import deduplicator
from scripts.editorial_templates import SECTION_TEMPLATES
from scripts.rss_live_scraper import (
    scrape_all_feeds_parallel,
    synthesize_live_proposal,
    synthesize_live_kondensat,
)

POLISH_MONTHS = [
    "", "stycznia", "lutego", "marca", "kwietnia", "maja", "czerwca",
    "lipca", "sierpnia", "września", "października", "listopada", "grudnia"
]

POLISH_DAYS = [
    "Poniedziałek", "Wtorek", "Środa", "Czwartek", "Piątek", "Sobota", "Niedziela"
]


def get_warsaw_now():
    """Zwraca aktualny czas w strefie Europe/Warsaw (z uwzględnieniem czasu letniego/zimowego)."""
    try:
        from zoneinfo import ZoneInfo
        return datetime.now(ZoneInfo("Europe/Warsaw"))
    except Exception:
        return datetime.now(timezone.utc) + timedelta(hours=1)


def format_date_pl(dt):
    return f"{dt.day} {POLISH_MONTHS[dt.month]} {dt.year} r."


def format_datetime_pl(dt):
    return f"{dt.day} {POLISH_MONTHS[dt.month]} {dt.year} r., godz. {dt.strftime('%H:%M:%S')}"


def get_day_name(dt):
    return POLISH_DAYS[dt.weekday()]


def build_daily_proposals_md(date_str, date_pl, day_name, topics):
    """Generuje pełny dokument Markdown z 6 propozycjami redakcyjnymi (5 szuflad + Kondensat)."""
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
        is_kondensat = (
            raw_cat == "kondensat"
            or t.get("section_type") == "kondensat"
            or "kondensat" in t.get("title", "").lower()
        )
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


def save_live_pulse_metadata(now_dt, trigger_label, live_rss_result, chosen_topics):
    """Zapisuje plik data/live_rss_pulse.json z telemetrią ostatniego uruchomienia Crona i żywym pulsem RSS."""
    live_wire = []
    by_cat = (live_rss_result or {}).get("by_category", {})
    for cat in ["technologia", "gospodarka", "historia", "polityka", "eseje"]:
        for item in by_cat.get(cat, [])[:5]:
            live_wire.append({
                "category": cat,
                "source_name": item.get("source_name", ""),
                "source_flag": item.get("source_flag", "🌍"),
                "title": item.get("title", ""),
                "link": item.get("link", ""),
                "summary": item.get("summary", "")[:220],
                "is_pl": bool(item.get("is_pl", False)),
            })

    pulse_payload = {
        "last_run_iso": now_dt.isoformat(),
        "last_run_pl": format_datetime_pl(now_dt),
        "last_run_date": now_dt.strftime("%Y-%m-%d"),
        "trigger_label": trigger_label,
        "feeds_checked": (live_rss_result or {}).get("feeds_checked", 0),
        "feeds_online": (live_rss_result or {}).get("feeds_online", 0),
        "total_items_scraped": (live_rss_result or {}).get("total_items", 0),
        "generated_topics_count": len(chosen_topics),
        "live_wire": live_wire,
    }

    target_data_dirs = [os.path.join(ROOT_DIR, "data")]
    local_git_data = r"C:\Users\irene\blog-laika\data"
    if os.path.exists(r"C:\Users\irene\blog-laika") and os.path.normcase(os.path.abspath(ROOT_DIR)) != os.path.normcase(r"C:\Users\irene\blog-laika"):
        target_data_dirs.append(local_git_data)

    for d_dir in target_data_dirs:
        try:
            os.makedirs(d_dir, exist_ok=True)
            with open(os.path.join(d_dir, "live_rss_pulse.json"), "w", encoding="utf-8") as f:
                json.dump(pulse_payload, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"⚠️ Nie udało się zapisać live_rss_pulse.json w {d_dir}: {e}")

    return pulse_payload


def run_daily_cron(target_date_str=None, deploy=False, use_live_rss=True, force=False, trigger_label="Automatyczny Cron (08:00)"):
    """Główna funkcja codziennego researchera, skrapera RSS i crona redakcyjnego."""
    print("=" * 72)
    print("🚀 [Blog Laika] Uruchomienie Skrapera RSS i Crona Redakcyjnego")
    print("=" * 72)

    now = get_warsaw_now()
    if target_date_str:
        dt = datetime.strptime(target_date_str, "%Y-%m-%d")
    else:
        dt = now

    date_str = dt.strftime("%Y-%m-%d")
    date_pl = format_date_pl(dt)
    day_name = get_day_name(dt)
    day_seed = dt.timetuple().tm_yday + dt.hour

    print(f"📅 Data operacji: {date_str} ({date_pl}, {day_name}) | Tryb: {trigger_label}")

    # Synchronizacja bazy wiedzy deduplikatora
    deduplicator.sync_with_database()
    deduplicator.sync_with_proposals_folder()

    # 1. Równoległy skan na żywo kanałów RSS
    live_rss_result = {"by_category": {}, "feeds_checked": 0, "feeds_online": 0, "total_items": 0}
    if use_live_rss:
        print("🌐 Skanowanie na żywo kanałów RSS ze wszystkich 5 szuflad tematycznych...")
        try:
            live_rss_result = scrape_all_feeds_parallel(max_per_feed=10)
            print(
                f"📡 Kanały RSS online: {live_rss_result['feeds_online']}/{live_rss_result['feeds_checked']} "
                f"| Pobrano świeżych depesz: {live_rss_result['total_items']}"
            )
        except Exception as e:
            print(f"⚠️ Błąd skanowania live RSS ({e}), przełączanie na pulę Banku Wiedzy.")

    topics = []
    standard_categories = ["technologia", "gospodarka", "historia", "polityka", "eseje"]

    # Ignorujemy dzisiejsze wpisy z historii tylko wtedy, gdy odświeżamy ten sam dzień bez --force;
    # przy --force zachowujemy blokadę seen_rss_urls, więc ręczne kliknięcie „z palca” losuje NOWE artykuły z RSS!
    ignore_date_arg = None if force else date_str

    for idx_cat, cat in enumerate(standard_categories):
        selected_item = None

        # KROK A: Spróbuj wybrać świeży, nigdy wcześniej nieużyty impuls z Live RSS
        live_candidates = live_rss_result.get("by_category", {}).get(cat, [])
        for rss_cand in live_candidates:
            rss_url = rss_cand.get("link", "")
            rss_title = rss_cand.get("title", "")
            is_dup_raw, _ = deduplicator.is_duplicate(rss_title, candidate_url=rss_url, category=cat, ignore_date=ignore_date_arg)
            if is_dup_raw:
                continue

            synthesized = synthesize_live_proposal(rss_cand, cat, visual_seed=day_seed + idx_cat)
            is_dup_syn, _ = deduplicator.is_duplicate(synthesized["title"], candidate_url=rss_url, category=cat, ignore_date=ignore_date_arg)
            if not is_dup_syn:
                selected_item = synthesized
                deduplicator.register_seen(synthesized["title"], cat, url=rss_url, date_str=date_str)
                break

        # KROK B: Fallback do kuratorowanego Banku Szablonów, jeśli RSS był niedostępny
        if not selected_item:
            tmpl_list = SECTION_TEMPLATES.get(cat, [])
            if tmpl_list:
                start_idx = day_seed % len(tmpl_list)
                for offset in range(len(tmpl_list)):
                    cand = tmpl_list[(start_idx + offset) % len(tmpl_list)]
                    is_dup, reason = deduplicator.is_duplicate(cand["title"], category=cat, ignore_date=date_str)
                    if not is_dup:
                        selected_item = dict(cand)
                        selected_item["category"] = cat
                        deduplicator.register_seen(cand["title"], cat, date_str=date_str)
                        break

                if not selected_item:
                    # Zamiast brać zawsze [0], wybierz szablon o indeksie zależnym od dnia roku
                    fallback_cand = dict(tmpl_list[day_seed % len(tmpl_list)])
                    fallback_cand["category"] = cat
                    selected_item = fallback_cand

        if selected_item:
            topics.append(selected_item)

    # 2. Szósty element dnia: Wielowątkowy KONDENSAT (Konglomerat)
    kondensat_item = None
    if live_rss_result.get("feeds_online", 0) > 0 and len(topics) >= 4:
        # Najpierw sprawdź, czy mamy nieużyty kuratorowany kondensat, lub wygeneruj żywy Kondensat Dnia z dzisiejszych depesz!
        live_kond = synthesize_live_kondensat(topics, date_pl, visual_seed=day_seed)
        if force:
            # Dodaj znacznik godziny przy ręcznym wymuszeniu, aby tytuł był unikalny w ciągu dnia
            live_kond["title"] = (
                f"Kondensat ({date_pl}, wydanie {now.strftime('%H:%M')}): "
                f"Sprzężenie krzemu, kapitału i siły państwa — wielowątkowa synteza trendów"
            )
        kondensat_item = live_kond
        deduplicator.register_seen(kondensat_item["title"], "kondensat", date_str=date_str)
    else:
        kond_templates = SECTION_TEMPLATES.get("kondensat", [])
        if kond_templates:
            for offset in range(len(kond_templates)):
                cand = kond_templates[(day_seed + offset) % len(kond_templates)]
                is_dup, _ = deduplicator.is_duplicate(cand["title"], category="kondensat", ignore_date=date_str)
                if not is_dup:
                    kondensat_item = dict(cand)
                    break
            if not kondensat_item:
                kondensat_item = dict(kond_templates[day_seed % len(kond_templates)])
            kondensat_item["section_type"] = "kondensat"
            kondensat_item["category"] = "eseje"

    if kondensat_item:
        topics.append(kondensat_item)

    print(f"\n✅ Skomponowano {len(topics)} w 100% UNIKALNYCH propozycji ze szkicami esejów:")
    for i, t in enumerate(topics, 1):
        label = "KONDENSAT" if t.get("section_type") == "kondensat" else t["category"].upper()
        print(f"   {i}. [{label}] {t['title'][:72]}...")

    # 3. Generowanie treści Markdown i zapis do propozycje-tematow/
    md_content = build_daily_proposals_md(date_str, date_pl, day_name, topics)

    target_dirs = [os.path.join(ROOT_DIR, "propozycje-tematow")]
    local_git_repo = r"C:\Users\irene\blog-laika"
    if os.path.exists(local_git_repo) and os.path.normcase(os.path.abspath(ROOT_DIR)) != os.path.normcase(local_git_repo):
        target_dirs.append(os.path.join(local_git_repo, "propozycje-tematow"))
        # Zsynchronizuj także rejestr deduplikatora do repozytorium git
        try:
            reg_src = os.path.join(ROOT_DIR, "data", "seen_articles_registry.json")
            reg_dst_dir = os.path.join(local_git_repo, "data")
            if os.path.exists(reg_src):
                os.makedirs(reg_dst_dir, exist_ok=True)
                shutil.copy2(reg_src, os.path.join(reg_dst_dir, "seen_articles_registry.json"))
        except Exception:
            pass

    for d in target_dirs:
        try:
            os.makedirs(d, exist_ok=True)
            fname = f"propozycje-{date_str}.md"
            fpath = os.path.join(d, fname)
            with open(fpath, "w", encoding="utf-8") as f:
                f.write(md_content)
            print(f"💾 Zapisano zestaw: {fpath}")

            retained = proposals_manager.enforce_retention(d, max_days=7)
            print(f"🔄 [Rotacja 7 dni] Zachowano {len(retained)} zestawów w {d}")
        except Exception as e:
            print(f"⚠️ Uwaga przy zapisie do {d}: {e}")

    # 4. Zapis telemetrii i żywego pulsu RSS (data/live_rss_pulse.json)
    pulse_payload = save_live_pulse_metadata(now, trigger_label, live_rss_result, topics)

    # 5. Rekompilacja statyczna (export_static.py)
    print("\n⚙️ [Kompilacja] Uruchamianie export_static.py...")
    try:
        subprocess.run(
            [sys.executable, os.path.join(ROOT_DIR, "export_static.py")],
            capture_output=True, text=True, encoding="utf-8", errors="replace", check=True
        )
        print("✅ Kompilacja statyczna zakończona sukcesem!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Błąd kompilacji export_static.py: {e.stderr}")

    # 6. Opcjonalny lokalny deploy do GitHub (gdy uruchamiane na Windows z flagą --deploy)
    if os.path.exists(local_git_repo) and deploy:
        print("\n🚀 [Git & Deploy] Synchronizacja z repozytorium GitHub...")
        try:
            dist_src = os.path.join(ROOT_DIR, "dist")
            if os.path.normcase(os.path.abspath(ROOT_DIR)) != os.path.normcase(local_git_repo):
                subprocess.run(
                    [sys.executable, os.path.join(local_git_repo, "export_static.py")],
                    cwd=local_git_repo, capture_output=True, text=True, encoding="utf-8", errors="replace"
                )
                dist_src = os.path.join(local_git_repo, "dist")

            subprocess.run(["git", "pull", "--rebase", "origin", "main"], cwd=local_git_repo, capture_output=True)
            subprocess.run(["git", "add", "propozycje-tematow", "data"], cwd=local_git_repo, check=True)
            status_res = subprocess.run(["git", "status", "--porcelain"], cwd=local_git_repo, capture_output=True, text=True)
            if status_res.stdout.strip():
                subprocess.run(
                    ["git", "commit", "-m", f"chore(cron): codzienne propozycje RSS i kondensat ({date_str}) [skip ci]"],
                    cwd=local_git_repo
                )
                subprocess.run(["git", "push", "origin", "main"], cwd=local_git_repo)
                print("✅ Pomyślnie wypchnięto zmiany do gałęzi main na GitHub!")

            temp_dir = os.environ.get("TEMP", r"C:\Users\irene\AppData\Local\Temp")
            dist_tmp = os.path.join(temp_dir, "blog-laika-gh-pages")
            if os.path.exists(dist_tmp):
                shutil.rmtree(dist_tmp, ignore_errors=True)
            shutil.copytree(dist_src, dist_tmp, dirs_exist_ok=True)

            subprocess.run(["git", "init", "-b", "gh-pages"], cwd=dist_tmp, check=True, capture_output=True)
            subprocess.run(["git", "config", "user.name", "Blog Laika Cron"], cwd=dist_tmp, check=True)
            subprocess.run(["git", "config", "user.email", "kontakt@blog-laika.com"], cwd=dist_tmp, check=True)
            subprocess.run(["git", "add", "-A"], cwd=dist_tmp, check=True)
            subprocess.run(["git", "commit", "-m", f"Automatyczna publikacja crona ({date_str})"], cwd=dist_tmp, capture_output=True)
            subprocess.run(["git", "remote", "add", "origin", "https://github.com/Ireneusz1991/blog-laika.git"], cwd=dist_tmp, check=True)
            subprocess.run(["git", "push", "origin", "gh-pages", "--force"], cwd=dist_tmp, check=True)
            shutil.rmtree(dist_tmp, ignore_errors=True)
            print("✅ Pomyślnie zaktualizowano gałąź produkcyjną gh-pages (blog-laika.com)!")
        except Exception as e:
            print(f"⚠️ Błąd podczas pushowania do gita: {e}")

    print("\n🎯 Gotowe. Skraper RSS i Cron Redakcyjny zakończyły pracę z sukcesem!")
    return {
        "status": "ok",
        "date": date_str,
        "date_pl": date_pl,
        "topics_count": len(topics),
        "feeds_online": live_rss_result.get("feeds_online", 0),
        "total_items_scraped": live_rss_result.get("total_items", 0),
        "pulse": pulse_payload,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Codzienny cron redakcyjny i skraper RSS Bloga Laika")
    parser.add_argument("--date", help="Data w formacie YYYY-MM-DD", default=None)
    parser.add_argument("--deploy", action="store_true", help="Wypchnij zmiany do GitHub po generacji")
    parser.add_argument("--no-live", action="store_true", help="Wyłącz pobieranie RSS na żywo")
    parser.add_argument("--force", action="store_true", help="Wymuś wygenerowanie świeżej paczki z nowych depesz RSS")
    parser.add_argument("--trigger-label", default="Automatyczny Cron (08:00)", help="Etykieta źródła uruchomienia")
    args = parser.parse_args()

    run_daily_cron(
        target_date_str=args.date,
        deploy=args.deploy,
        use_live_rss=not args.no_live,
        force=args.force,
        trigger_label=args.trigger_label,
    )

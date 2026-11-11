import os
import re
import shutil
from datetime import datetime
import markdown

try:
    from scripts.rss_live_scraper import synthesize_bielik_draft
except Exception:
    def synthesize_bielik_draft(title, raw_title, src_name, src_flag, category, summary="", link=""):
        clean_raw = raw_title or title
        bielik_title = f"{title} (Wersja Bielik AI — Polski kontekst)"
        lead = (
            f"Analiza tematu podjętego przez {src_flag} **{src_name}** (*„{clean_raw}”*) z perspektywy polskich uwarunkowań rynkowych i suwerenności regulacyjnej. "
            f"Odrzucamy korporacyjny żargon i zachodnie kalki — skupiamy się na twardym rachunku zysków, kosztów i ryzyk dla polskiego przedsiębiorcy i obywatela."
        )
        return f"""# {bielik_title}

> 🦅 **Wersja Bielik AI:** Zredagowana przez polski model językowy — nacisk na polski kontekst gospodarczy, suwerenność cyfrową i kondensację treści.  
> 📡 **Impuls źródłowy:** {src_flag} [{src_name} — „{clean_raw}”]({link if link else '#'})

{lead}

---

### 1. Twardy bilans faktów (kondensacja redakcyjna)

{summary if summary else 'Wokół tematu narosło wiele narracji, ale kluczowe fakty dają się sprowadzić do mierzalnych wskaźników.'}
Sprawa sprowadza się do prostej zależności: kto kontroluje technologię i reguły gry, ten dyktuje warunki marżowe i prawne.

### 2. Odniesienie do realiów Polski i Europy Środkowej

Dla polskiego rynku kluczowe jest zachowanie elastyczności decyzyjnej, ochrona rodzimego kapitału oraz unikanie jednostronnych uzależnień technologicznych i surowcowych.

### 🦅 Kąt widzenia Bielik AI: Co z tego wynika dla Polski?

1. **Pragmatyzm zamiast kalki językowej:** Weryfikujmy zewnętrzne trendy w lokalnych warunkach gospodarczych.
2. **Ochrona suwerenności i danych:** Zachowujmy własne kompetencje i scenariusze awaryjne w kluczowych sektorach.
3. **Konkretny zysk dla obywatela:** Sprawdzajmy, czy proponowane zmiany trwale obniżają koszty i podnoszą bezpieczeństwo.

---
*Redakcja i kondensacja: Polski model językowy Bielik AI & Blog Laika*"""

POLISH_MONTHS = [
    "", "stycznia", "lutego", "marca", "kwietnia", "maja", "czerwca",
    "lipca", "sierpnia", "września", "października", "listopada", "grudnia"
]

POLISH_DAYS = [
    "Poniedziałek", "Wtorek", "Środa", "Czwartek", "Piątek", "Sobota", "Niedziela"
]

def format_date_pl(date_str: str) -> str:
    try:
        dt = datetime.strptime(date_str[:10], "%Y-%m-%d")
        return f"{dt.day} {POLISH_MONTHS[dt.month]} {dt.year}"
    except Exception:
        return date_str

def get_day_name_pl(date_str: str) -> str:
    try:
        dt = datetime.strptime(date_str[:10], "%Y-%m-%d")
        return POLISH_DAYS[dt.weekday()]
    except Exception:
        return ""

def enforce_retention(proposals_dir: str, max_days: int = 7):
    """Zachowuje wyłącznie najnowsze `max_days` zestawów propozycji (np. 7 dni x 5 tematów = 35 tematów).
    Starsze pliki są automatycznie usuwane (rotacja tygodniowa)."""
    if not os.path.exists(proposals_dir):
        return []

    files = [f for f in os.listdir(proposals_dir) if f.startswith("propozycje-") and f.endswith(".md")]
    
    # Sortowanie po dacie w nazwie pliku (np. propozycje-2026-10-27.md) malejąco
    def extract_date(fn):
        m = re.search(r'(\d{4}-\d{2}-\d{2})', fn)
        return m.group(1) if m else "1970-01-01"

    sorted_files = sorted(files, key=extract_date, reverse=True)

    # Zachowaj do max_days plików, resztę usuń
    retained_files = sorted_files[:max_days]
    pruned_files = sorted_files[max_days:]

    for pf in pruned_files:
        try:
            os.remove(os.path.join(proposals_dir, pf))
            print(f"[Rotacja] Usunięto przestarzały zestaw propozycji (> 7 dni): {pf}")
        except Exception as e:
            print(f"[Błąd rotacji] Nie udało się usunąć {pf}: {e}")

    return retained_files

def parse_proposals_file(filepath: str) -> list:
    """Parsuje plik markdown z propozycjami tematów i zwraca listę ustrukturyzowanych tematów."""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    proposals = []
    sections = re.split(r'\n##\s+', content)
    for sec in sections[1:]:
        lines = sec.strip().splitlines()
        first_line = lines[0]
        title = first_line
        if ":" in first_line:
            title = first_line.split(":", 1)[1].strip().strip('„”"\'')

        # Oczyszczenie sztucznych, naciąganych formułek ze starszych plików archiwalnych
        title = re.sub(r'\s*[—–-]\s*chłodny bilans z perspektywy dociekliwego laika.*$', '', title, flags=re.IGNORECASE).strip()
        title = re.sub(r'\s*[—–-]\s*analiza przyczyn i konsekwencji z pierwszych zasad.*$', '', title, flags=re.IGNORECASE).strip()
        title = re.sub(r'^(?:Pod maską [^:]+|Rachunek [^:]+|Geopolityka [^:]+|Długie echo [^:]+|Anatomia [^:]+|Spojrzenie [^:]+):\s*co sygnał z [^:]+ mówi o ukrytej architekturze rynku:?\s*', '', title, flags=re.IGNORECASE).strip()
        title = re.sub(r'^[^:]+:\s*co sygnał z [^:]+ mówi o ukrytej architekturze rynku:?\s*', '', title, flags=re.IGNORECASE).strip()
        if "?" in title and ("serbscy studenci" in title.lower() or "zwyciężyli" in title.lower()):
            title = "Serbscy studenci zwyciężyli: Pomiędzy siłą buntu a bezwładem instytucji"

        category = "technologia"
        lead = ""
        thesis = ""
        search_date = ""
        image_url = ""
        image_concept = ""
        image_prompt = ""
        samokreacja = "100% Samokreacja (autorska synteza faktów)"
        source_name = ""
        source_flag = "🇵🇱"
        source_note = ""
        body_lines = []
        draft_lines = []
        bielik_lines = []
        is_in_draft = False
        is_in_bielik = False

        for line in lines[1:]:
            line_str = line.strip()
            if line_str.startswith("### 🦅 Alternatywny szkic Bielik") or line_str.startswith("### Alternatywny szkic Bielik") or line_str.startswith("### Szkic Bielik"):
                is_in_draft = False
                is_in_bielik = True
                continue

            if line_str.startswith("### 📝 Gotowy szkic") or line_str.startswith("### Gotowy szkic") or line_str.startswith("### Gotowy artykuł"):
                is_in_draft = True
                is_in_bielik = False
                continue
            
            if is_in_draft:
                draft_lines.append(line)
                continue

            if is_in_bielik:
                bielik_lines.append(line)
                continue

            if line_str.startswith("* **Kategoria:**"):
                cat_m = re.search(r'`([^`]+)`', line_str)
                if cat_m:
                    category = cat_m.group(1)
            elif line_str.startswith("* **Data wyszukania:**"):
                search_date = line_str.replace("* **Data wyszukania:**", "").strip()
            elif line_str.startswith("* **Model powstawania:**") or line_str.startswith("* **Format:**"):
                samokreacja = re.sub(r'^\*\s*\*\*(?:Model powstawania|Format):\*\*', '', line_str).strip()
            elif line_str.startswith("* **Źródło impulsu:**") or line_str.startswith("* **Źródło:**"):
                source_raw = re.sub(r'^\*\s*\*\*(?:Źródło impulsu|Źródło):\*\*', '', line_str).strip()
                if "🇬🇧" in source_raw: source_flag = "🇬🇧"
                elif "🇺🇸" in source_raw: source_flag = "🇺🇸"
                elif "🇪🇺" in source_raw: source_flag = "🇪🇺"
                elif "🌍" in source_raw: source_flag = "🌍"
                elif "🇵🇱" in source_raw: source_flag = "🇵🇱"
                source_name = source_raw.replace("🇬🇧", "").replace("🇺🇸", "").replace("🇪🇺", "").replace("🌍", "").replace("🇵🇱", "").strip()
            elif line_str.startswith("* **Wątek źródłowy:**") or line_str.startswith("* **Raport źródłowy:**"):
                source_note = re.sub(r'^\*\s*\*\*(?:Wątek|Raport)\s+źródłowy:\*\*', '', line_str).strip()
            elif line_str.startswith("* **Proponowana grafika:**") or line_str.startswith("* **Grafika:**"):
                image_url = re.sub(r'^\*\s*\*\*(?:Proponowana grafika|Grafika):\*\*', '', line_str).strip().strip('<>')
            elif line_str.startswith("* **Koncepcja wizualna:**"):
                image_concept = line_str.replace("* **Koncepcja wizualna:**", "").strip()
            elif line_str.startswith("* **Prompt AI dla grafiki:**") or line_str.startswith("* **Prompt AI:**"):
                image_prompt = re.sub(r'^\*\s*\*\*Prompt AI(?:\s+dla grafiki)?:\*\*', '', line_str).strip().strip('`')
            elif line_str.startswith("* **Lead:**"):
                lead = line_str.replace("* **Lead:**", "").strip()
            elif line_str.startswith("* **Kluczowa teza") or line_str.startswith("* **Główna teza") or (line_str.startswith("*") and not line_str.startswith("* **")):
                clean_thesis = re.sub(r'^\*\s*\*\*(?:Kluczowa|Główna)\s+teza(?:\s+(?:wpisu|eseju))?:\*\*', '', line_str).strip().strip('*')
                if clean_thesis and not thesis:
                    thesis = clean_thesis
                else:
                    body_lines.append(line)
            else:
                body_lines.append(line)

        # Build full ready-to-verify-and-publish draft (Wersja A - Autorska)
        if draft_lines:
            full_draft = "\n".join(draft_lines).strip()
        else:
            draft_parts = [f"# {title}\n"]
            if lead:
                draft_parts.append(f"{lead}\n")
            draft_parts.append("---\n")
            if source_name:
                draft_parts.append(f"> 📡 **Źródło impulsu i inspiracji:** {source_flag} **{source_name}**" + (f" — *{source_note}*" if source_note else "") + "\n")
            if thesis:
                draft_parts.append(f"> 💡 **Kluczowa teza wpisu:** *{thesis}*\n")
            if body_lines:
                draft_parts.append("## Węzłowe punkty argumentacji i analiza faktów\n")
                draft_parts.append("\n".join(body_lines).strip())
            draft_parts.append("\n\n---\n\n*Autorski wpis Bloga Laika. 100% Samokreacja — synteza faktów z perspektywy dociekliwego laika.*")
            full_draft = "\n".join(draft_parts)

        # Build Bielik AI alternative draft (Wersja B - Polski kontekst & kondensacja)
        bielik_title = f"{title} (Wersja Bielik AI — Polski kontekst)"
        if bielik_lines:
            bielik_draft = "\n".join(bielik_lines).strip()
        else:
            bielik_draft = synthesize_bielik_draft(
                title=title,
                raw_title=title,
                src_name=source_name or "Źródło branżowe",
                src_flag=source_flag,
                category=category,
                summary=lead or thesis,
                link="#"
            )

        # Convert drafts to HTML for inline reading accordion tabs
        full_draft_html = markdown.markdown(full_draft, extensions=['extra', 'tables', 'fenced_code', 'nl2br'])
        bielik_draft_html = markdown.markdown(bielik_draft, extensions=['extra', 'tables', 'fenced_code', 'nl2br'])

        # W panelu admina kierujemy kondensaty jako osobną kategorię 'kondensat'
        is_kond = "kondensat" in title.lower() or "kondensat" in first_line.lower() or category == "kondensat"
        admin_cat = "kondensat" if is_kond else category

        # Wykrywanie propozycji AI, Bielik AI oraz polskiego kontekstu
        scan_text = f"{title} {lead} {thesis} {' '.join(body_lines)} {' '.join(draft_lines)} {' '.join(bielik_lines)} {source_name} {source_note}".lower()
        ai_terms = [
            'bielik', 'speakleash', 'cyfronet', 'sztuczn', 'model językow', 'modele językow',
            'llm', 'transformer', 'sieci neuronow', 'uczenie maszynow', 'deep learning',
            'chatgpt', 'openai', 'anthropic', 'suwerenność cyfrowa', ' ai ', ' ai:', ' ai,', ' ai.',
            '(ai)', 'sztucznej inteligencji'
        ]
        is_ai_topic = any(term in scan_text for term in ai_terms) or 'bielik' in title.lower() or ' ai' in title.lower() or 'ai:' in title.lower()
        is_bielik_rec = is_ai_topic or (source_flag == '🇵🇱')
        bielik_badge = "🦅 Bielik AI: Rekomendacja AI" if is_ai_topic else ("🦅 Bielik AI: Polski kontekst" if is_bielik_rec else "")

        proposals.append({
            "title": title,
            "category": admin_cat,
            "is_kondensat": is_kond,
            "bielik_recommended": is_bielik_rec,
            "is_bielik_ai": is_ai_topic,
            "bielik_badge": bielik_badge,
            "search_date": search_date,
            "image_url": image_url,
            "image_concept": image_concept,
            "image_prompt": image_prompt,
            "samokreacja": samokreacja,
            "source_name": source_name,
            "source_flag": source_flag,
            "source_note": source_note,
            "lead": lead,
            "thesis": thesis,
            "raw_body": "\n".join(body_lines).strip(),
            "full_draft": full_draft,
            "full_draft_html": full_draft_html,
            "bielik_title": bielik_title,
            "bielik_draft": bielik_draft,
            "bielik_draft_html": bielik_draft_html
        })

    return proposals

def load_all_weekly_proposals(proposals_dir: str, max_days: int = 7) -> list:
    """Ładuje do 7 zestawów dziennych (4 tematy na dzień = 28 tematów łącznie) wraz z datami wyszukania."""
    retained_files = enforce_retention(proposals_dir, max_days=max_days)
    
    daily_packages = []
    total_count = 0
    total_bielik = 0

    for fn in retained_files:
        filepath = os.path.join(proposals_dir, fn)
        m_date = re.search(r'(\d{4}-\d{2}-\d{2})', fn)
        date_str = m_date.group(1) if m_date else ""
        formatted_date = format_date_pl(date_str)
        day_name = get_day_name_pl(date_str)
        
        props = parse_proposals_file(filepath)
        total_count += len(props)
        bielik_in_pkg = sum(1 for p in props if p.get('bielik_recommended') or p.get('is_bielik_ai'))
        total_bielik += bielik_in_pkg

        daily_packages.append({
            "filename": fn,
            "date": date_str,
            "formatted_date": formatted_date,
            "day_name": day_name,
            "proposals": props,
            "count": len(props),
            "bielik_count": bielik_in_pkg
        })

    return {
        "packages": daily_packages,
        "total_proposals": total_count,
        "total_bielik_proposals": total_bielik,
        "total_days": len(daily_packages)
    }

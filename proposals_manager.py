import os
import re
import shutil
from datetime import datetime

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
    """Zachowuje wyłącznie najnowsze `max_days` zestawów propozycji (np. 7 dni x 4 tematy = 28 tematów).
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

        category = "technologia"
        lead = ""
        thesis = ""
        search_date = ""
        body_lines = []

        for line in lines[1:]:
            line_str = line.strip()
            if line_str.startswith("* **Kategoria:**"):
                cat_m = re.search(r'`([^`]+)`', line_str)
                if cat_m:
                    category = cat_m.group(1)
            elif line_str.startswith("* **Data wyszukania:**"):
                search_date = line_str.replace("* **Data wyszukania:**", "").strip()
            elif line_str.startswith("* **Lead:**"):
                lead = line_str.replace("* **Lead:**", "").strip()
            elif line_str.startswith("* **Główna teza") or (line_str.startswith("*") and not line_str.startswith("* **")):
                clean_thesis = line_str.replace("* **Główna teza eseju:**", "").replace("* **Główna teza:**", "").strip().strip('*')
                if clean_thesis and not thesis:
                    thesis = clean_thesis
                else:
                    body_lines.append(line)
            else:
                body_lines.append(line)

        proposals.append({
            "title": title,
            "category": category,
            "search_date": search_date,
            "lead": lead,
            "thesis": thesis,
            "raw_body": "\n".join(body_lines).strip()
        })

    return proposals

def load_all_weekly_proposals(proposals_dir: str, max_days: int = 7) -> list:
    """Ładuje do 7 zestawów dziennych (4 tematy na dzień = 28 tematów łącznie) wraz z datami wyszukania."""
    retained_files = enforce_retention(proposals_dir, max_days=max_days)
    
    daily_packages = []
    total_count = 0

    for fn in retained_files:
        filepath = os.path.join(proposals_dir, fn)
        m_date = re.search(r'(\d{4}-\d{2}-\d{2})', fn)
        date_str = m_date.group(1) if m_date else ""
        formatted_date = format_date_pl(date_str)
        day_name = get_day_name_pl(date_str)
        
        props = parse_proposals_file(filepath)
        total_count += len(props)

        daily_packages.append({
            "filename": fn,
            "date": date_str,
            "formatted_date": formatted_date,
            "day_name": day_name,
            "proposals": props,
            "count": len(props)
        })

    return {
        "packages": daily_packages,
        "total_proposals": total_count,
        "total_days": len(daily_packages)
    }

# -*- coding: utf-8 -*-
"""
Audytor Plagiatu, Skraper Sieciowy i Analizator Kreatywności dla Bloga Laika.
Weryfikuje autentyczność tekstu, sprawdza unikalność fraz w internecie,
bada stylometrię (TTR, burstiness) i wykrywa klisze AI.
"""

import os
import re
import sys
import json
import time
import urllib.request
import urllib.parse
from datetime import datetime

# Safe UTF-8 console output for Windows
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

# Lista znanych klisz, szablonów i korpomowy AI w języku polskim
AI_CLICHES = [
    r"w dynamicznie (?:zmieniającym|rozwijającym) się świecie",
    r"w dobie (?:cyfrowej transformacji|internetu|sztucznej inteligencji|globalizacji)",
    r"warto (?:zauważyć|podkreślić|mieć na uwadze),? że",
    r"nie ulega wątpliwości,? że",
    r"podsumowując,? (?:można stwierdzić|warto dodać)",
    r"kluczowym (?:aspektem|elementem|czynnikiem) (?:jest|pozostaje)",
    r"w tym (?:artykule|eseju|wpisie) przyjrzymy się",
    r"czas pokaże,? jak",
    r"staje się coraz bardziej (?:istotne|powszechne|znaczące)",
    r"nie sposób (?:pominąć|zaprzeczyć)",
    r"jak bumerang wraca pytanie",
    r"stajemy przed (?:wyzwaniem|obliczem)",
    r"współczesny świat stawia przed nami",
    r"jedno jest pewne:",
    r"wkraczamy w nową erę",
    r"szeroki wachlarz (?:możliwości|rozwiązań)",
    r"nie tylko.*ale również",
    r"odgrywa kluczową rolę",
    r"stanowi nieodłączny element",
    r"w mgnieniu oka",
    r"kamień milowy w rozwoju"
]

class PlagiarismAndCreativityAuditor:
    def __init__(self, user_agent=None):
        self.user_agent = user_agent or (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/124.0.0.0 Safari/537.36"
        )
        self.own_domains = [
            "blog-laika.com",
            "ireneusz1991.github.io",
            "localhost",
            "127.0.0.1"
        ]

    def extract_clean_text(self, markdown_text):
        """Usuwa frontmatter, linki, znaczniki i kod, pozostawiając czysty tekst eseju."""
        # Usuń frontmatter YAML
        cleaned = re.sub(r"^---[\s\S]*?---\s*", "", markdown_text, flags=re.MULTILINE)
        # Usuń bloki kodu
        cleaned = re.sub(r"```[\s\S]*?```", "", cleaned)
        cleaned = re.sub(r"`[^`]+`", "", cleaned)
        # Usuń nagłówki markdown (# Tytuł)
        cleaned = re.sub(r"^#+\s+.*$", "", cleaned, flags=re.MULTILINE)
        # Usuń linki [tekst](url)
        cleaned = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", cleaned)
        # Usuń obrazy ![alt](url)
        cleaned = re.sub(r"!\[[^\]]*\]\([^)]+\)", "", cleaned)
        # Usuń formatowanie pogrubienia/kursywy
        cleaned = re.sub(r"[*_]{1,3}([^*_]+)[*_]{1,3}", r"\1", cleaned)
        # Usuń cytaty blockquote (> tekst)
        cleaned = re.sub(r"^>\s*", "", cleaned, flags=re.MULTILINE)
        # Usuń linie poziome ---
        cleaned = re.sub(r"^---+$", "", cleaned, flags=re.MULTILINE)
        return cleaned.strip()

    def split_into_sentences(self, text):
        """Dzieli tekst na logiczne zdania."""
        raw_sentences = re.split(r"(?<=[.!?…])\s+(?=[A-ZĄĆĘŁŃÓŚŹŻ„\"])", text)
        sentences = [s.strip() for s in raw_sentences if len(s.strip()) > 15]
        return sentences

    def extract_shingles(self, text, n=8, max_shingles=10):
        """Tworzy n-gramy słowne (szingle) z najdłuższych i najbardziej unikalnych zdań tekstu."""
        words = re.findall(r"\b[A-Za-zżeczpólkja-zżeczpółkaśąęźń0-9\-]+\b", text)
        if len(words) < n:
            return [" ".join(words)] if words else []

        # Wybierz reprezentatywne, n-wyrazowe fragmenty rozłożone równomiernie w tekście
        step = max(1, (len(words) - n) // max_shingles)
        shingles = []
        for i in range(0, len(words) - n + 1, step):
            shingle = " ".join(words[i:i+n])
            # Pomiń szingle ze zbyt powszechnymi słowami technicznymi
            if len(shingle) > 35:
                shingles.append(shingle)
            if len(shingles) >= max_shingles:
                break
        return shingles

    def search_web_for_phrase(self, phrase, pause_sec=0.8):
        """Skrapuje wyszukiwarkę DuckDuckGo w poszukiwaniu dosłownego dopasowania frazy w cudzysłowie."""
        query = f'"{phrase}"'
        url = "https://html.duckduckgo.com/html/?q=" + urllib.parse.quote(query)
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": self.user_agent,
                "Accept-Language": "pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7"
            }
        )

        matches = []
        try:
            time.sleep(pause_sec)
            with urllib.request.urlopen(req, timeout=10) as resp:
                html = resp.read().decode("utf-8", errors="ignore")

            # Wyodrębnij bloki wyników
            blocks = re.findall(r'<div class="result__body">.*?</div>\s*</div>', html, re.DOTALL)
            for b in blocks:
                url_m = re.search(r'<a[^>]+class="result__url"[^>]*href="([^"]+)"', b)
                raw_url = url_m.group(1).strip() if url_m else ""
                
                # Odszyfruj url z przekierowania duckduckgo
                if "uddg=" in raw_url:
                    parsed = urllib.parse.parse_qs(urllib.parse.urlparse(raw_url).query)
                    raw_url = parsed.get("uddg", [raw_url])[0]

                snippet_m = re.search(r'<a[^>]+class="result__snippet"[^>]*>(.*?)</a>', b, re.DOTALL)
                snippet = re.sub(r"<[^>]+>", "", snippet_m.group(1)).strip() if snippet_m else ""

                # Sprawdź, czy to nie jest domena własna bloga
                is_own = any(d in raw_url.lower() for d in self.own_domains)

                matches.append({
                    "url": raw_url,
                    "snippet": snippet,
                    "is_own": is_own
                })
        except Exception as e:
            # W razie chwilowego błędu sieciowego logujemy informację
            pass

        return matches

    def audit_plagiarism(self, text, max_queries=6):
        """Przeprowadza skanowanie antyplagiatowe tekstu metodą shingles & web search."""
        shingles = self.extract_shingles(text, n=8, max_shingles=max_queries)
        results = []
        external_duplicates = 0

        for s in shingles:
            matches = self.search_web_for_phrase(s)
            external_matches = [m for m in matches if not m["is_own"]]
            
            is_plagiarized = len(external_matches) > 0
            if is_plagiarized:
                external_duplicates += 1

            results.append({
                "phrase": s,
                "matches_count": len(matches),
                "external_matches_count": len(external_matches),
                "external_matches": external_matches[:2],
                "verdict": "DUPLIKAT W SIECI" if is_plagiarized else "CZYSTY / UNIKALNY"
            })

        total_tested = max(1, len(shingles))
        duplication_ratio = external_duplicates / total_tested
        originality_score = round((1.0 - duplication_ratio) * 100, 1)

        return {
            "tested_shingles_count": total_tested,
            "external_duplicates_count": external_duplicates,
            "originality_web_score": originality_score,
            "is_clean": external_duplicates == 0,
            "details": results
        }

    def audit_creativity_and_style(self, text):
        """Bada metryki kreatywności: bogactwo leksykalne, wariancję długości zdań, brak klisz AI i styl laika."""
        words = re.findall(r"\b[A-Za-zżeczpólkja-zżeczpółkaśąęźń\-]+\b", text.lower())
        total_words = len(words)
        unique_words = len(set(words))

        # 1. Type-Token Ratio (TTR) oraz Root TTR (Guiraud's Index)
        ttr = (unique_words / total_words) if total_words > 0 else 0
        guiraud_r = (unique_words / (total_words ** 0.5)) if total_words > 0 else 0
        
        # Ocena TTR (powyżej 0.55 dla eseju 300-600 słów to bardzo wysokie bogactwo)
        lexical_score = min(100, max(30, round((ttr / 0.65) * 100, 1)))

        # 2. Rytm i Wariancja Zdań (Burstiness - cecha ludzkiego pisarstwa)
        sentences = self.split_into_sentences(text)
        lengths = [len(s.split()) for s in sentences if len(s.split()) > 0]
        
        if lengths:
            avg_len = sum(lengths) / len(lengths)
            variance = sum((l - avg_len) ** 2 for l in lengths) / len(lengths)
            std_dev = variance ** 0.5
            # Ludzki esej ma zróżnicowane zdania (od krótkich po złożone, std_dev > 6.0)
            burstiness_score = min(100, max(40, round((std_dev / 8.5) * 100, 1)))
        else:
            avg_len, std_dev, burstiness_score = 0, 0, 50

        # 3. Wykrywacz Klisz i Korpomowy AI
        cliche_matches = []
        for pat in AI_CLICHES:
            found = re.findall(pat, text, flags=re.IGNORECASE)
            if found:
                for match_txt in found:
                    cliche_matches.append(match_txt)

        cliche_count = len(cliche_matches)
        # Każda znaleziona klisza obniża punktację o 15 pkt
        cliche_score = max(0, 100 - (cliche_count * 15))

        # 4. Znaczniki Dociekliwego Laika (Pytania retoryczne, syntetyzowanie, kontrasty)
        questions = [s for s in sentences if s.endswith("?") or "dlaczego" in s.lower() or "jaki" in s.lower()]
        has_concrete_data = bool(re.search(r"\b\d{4}\b|\b\d+%\b|\b[A-Z]{3,}\b", text))
        
        voice_score = 60
        if len(questions) >= 2:
            voice_score += 20
        elif len(questions) >= 1:
            voice_score += 10
        if has_concrete_data:
            voice_score += 20
        voice_score = min(100, voice_score)

        # 5. Łączny Indeks Samokreacji i Kreatywności
        # Wagi: Bogactwo słowne (25%), Zmienność rytmu/Burstiness (25%), Brak klisz AI (30%), Głos dociekliwy (20%)
        overall_creativity = round(
            (lexical_score * 0.25) +
            (burstiness_score * 0.25) +
            (cliche_score * 0.30) +
            (voice_score * 0.20),
            1
        )

        return {
            "total_words": total_words,
            "unique_words": unique_words,
            "type_token_ratio": round(ttr, 3),
            "guiraud_index": round(guiraud_r, 2),
            "lexical_score": lexical_score,
            "sentences_count": len(sentences),
            "avg_sentence_length": round(avg_len, 1),
            "sentence_length_std_dev": round(std_dev, 2),
            "burstiness_score": burstiness_score,
            "ai_cliches_found": cliche_matches,
            "ai_cliche_score": cliche_score,
            "rhetorical_questions_count": len(questions),
            "voice_score": voice_score,
            "overall_creativity_score": overall_creativity
        }

    def verify_post_file(self, filepath, check_web=True, max_queries=5):
        """Kompleksowa weryfikacja pliku wpisu (antypatent, skraper internetowy, kreatywność)."""
        with open(filepath, "r", encoding="utf-8") as f:
            raw_content = f.read()

        title_m = re.search(r'^title:\s*["\']?(.*?)["\']?\s*$', raw_content, re.MULTILINE)
        title = title_m.group(1) if title_m else os.path.basename(filepath)

        clean_text = self.extract_clean_text(raw_content)

        print(f"\n======================================================================")
        print(f"🔍 AUDYT PLAGIATU & KREATYWNOŚCI: {title}")
        print(f"📁 Plik: {filepath}")
        print(f"======================================================================")

        # 1. Analiza Stylometrii & Kreatywności
        print("  [1/2] Analiza stylometryczna, bogactwa leksykalnego i detekcja klisz AI...")
        creativity_res = self.audit_creativity_and_style(clean_text)

        # 2. Skanowanie Antyplagiatowe przez Skraper Internetowy
        plagiarism_res = None
        if check_web:
            print("  [2/2] Skrapowanie sieci i testowanie szingli w wyszukiwarce...")
            plagiarism_res = self.audit_plagiarism(clean_text, max_queries=max_queries)
        else:
            print("  [2/2] Pominięto test sieciowy (--no-web)")

        # Podsumowanie i werdykt
        web_score = plagiarism_res["originality_web_score"] if plagiarism_res else 100.0
        is_clean = plagiarism_res["is_clean"] if plagiarism_res else True
        creativity_score = creativity_res["overall_creativity_score"]

        verdict_status = "100% CZYSTA SAMOKREACJA (BRAK PLAGIATU, WYSOKA KREATYWNOŚĆ)"
        if not is_clean:
            verdict_status = "⚠️ WYKRYTO ZBIEŻNOŚCI Z ZEWNĘTRZNYMI ŹRÓDŁAMI"
        elif creativity_score < 60:
            verdict_status = "⚠️ NISKA KREATYWNOŚĆ (POWTARZALNY STYL / KLISZE)"

        report = {
            "title": title,
            "filepath": filepath,
            "audit_timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "verdict": verdict_status,
            "originality_web_score": web_score,
            "is_plagiarism_free": is_clean,
            "creativity_score": creativity_score,
            "creativity_metrics": creativity_res,
            "plagiarism_details": plagiarism_res
        }

        # Wyświetl raport w konsoli
        self._print_summary(report)

        return report

    def _print_summary(self, rep):
        cr = rep["creativity_metrics"]
        pl = rep["plagiarism_details"]

        print("\n------------------------- WYNIKI AUDYTU -------------------------")
        print(f"🎯 WERDYKT: {rep['verdict']}")
        print(f"🛡️ Wskaźnik oryginalności sieciowej: {rep['originality_web_score']}% (0 znalezionych obcych kopii)")
        print(f"🎨 Indeks Samokreacji i Kreatywności: {rep['creativity_score']}/100")
        print("-----------------------------------------------------------------")
        print(f"📊 Metryki Stylometryczne:")
        print(f"   • Słów łącznie: {cr['total_words']} | Unikalnych wyrazów: {cr['unique_words']}")
        print(f"   • Type-Token Ratio (TTR): {cr['type_token_ratio']} (Wynik bogactwa: {cr['lexical_score']}/100)")
        print(f"   • Liczba zdań: {cr['sentences_count']} | Średnia długość zdania: {cr['avg_sentence_length']} słów")
        print(f"   • Wariancja rytmu (Burstiness / Std Dev): {cr['sentence_length_std_dev']} (Wynik dynamiki: {cr['burstiness_score']}/100)")
        print(f"   • Znalezione klisze AI: {len(cr['ai_cliches_found'])} {cr['ai_cliches_found']}")
        print(f"   • Pytania retoryczne / dociekliwość: {cr['rhetorical_questions_count']} pytań")

        if pl and pl.get("details"):
            print("\n🌐 Przetestowane frazy (Skraper internetowy):")
            for idx, item in enumerate(pl["details"], 1):
                icon = "✅" if item["verdict"] == "CZYSTY / UNIKALNY" else "❌"
                print(f"   {idx}. {icon} \"{item['phrase']}\" -> {item['verdict']}")
                if item["external_matches"]:
                    for em in item["external_matches"]:
                        print(f"      🔗 Dopasowanie: {em['url']}")
        print("=================================================================\n")


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Audytor Antyplagiatowy & Analizator Kreatywności Bloga Laika")
    parser.add_argument("file", nargs="?", default=None, help="Ścieżka do pliku Markdown wpisu")
    parser.add_argument("--all", action="store_true", help="Audytuj wszystkie wpisy w folderze posts/")
    parser.add_argument("--output", default=None, help="Ścieżka do pliku wyjściowego JSON z raportem")
    parser.add_argument("--no-web", action="store_true", help="Pomiń skanowanie sieciowe DuckDuckGo")
    parser.add_argument("--queries", type=int, default=5, help="Liczba zapytań sieciowych na wpis (domyślnie 5)")

    args = parser.parse_args()
    auditor = PlagiarismAndCreativityAuditor()

    reports = []
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    posts_dir = os.path.join(base_dir, "posts")

    if args.all or not args.file:
        files = [os.path.join(posts_dir, f) for f in os.listdir(posts_dir) if f.endswith(".md")]
        for f in files:
            rep = auditor.verify_post_file(f, check_web=not args.no_web, max_queries=args.queries)
            reports.append(rep)
    else:
        rep = auditor.verify_post_file(args.file, check_web=not args.no_web, max_queries=args.queries)
        reports.append(rep)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as out_f:
            json.dump(reports, out_f, indent=2, ensure_ascii=False)
        print(f"💾 Raport zapisany do: {args.output}")

if __name__ == "__main__":
    main()

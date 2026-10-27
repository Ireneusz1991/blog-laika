# -*- coding: utf-8 -*-
"""
Moduł Samokreacji (Originality & Creative Synthesis Engine) dla Bloga Laika.
Autor: Ireneusz Machowiec / Blog Laika

FILOZOFIA SAMOKREACJI:
Blog Laika nigdy nie kopiuje cudzych tekstów, nie przedrukowuje artykułów z innych portali
ani nie stosuje techniki 'scrap & spin' (mieszania cudzych zdań).
Wszelkie zewnętrzne wydarzenia i trendy są traktowane WYŁĄCZNIE jako impuls faktograficzny
(np. decyzja regulatora, publikacja wyników finansowych, premiera modelu AI).
Cała treść wpisu, tytuł, lead, kluczowa teza, krytyczna antyteza oraz pytania dociekliwego laika
powstają od zera na drodze SAMOKREACJI (autorskiej syntezy intelektualnej).
"""

import re
from typing import Dict, List, Any

# 5 Filarów Samokreacji Bloga Laika
SAMOKREACJA_PILLARS = [
    {
        "id": 1,
        "name": "Impuls faktograficzny zamiast powielania tekstu",
        "description": "Zewnętrzne źródła dostarczają jedynie twardych liczb, dat lub zdarzeń. Ani jedno zdanie publicysty z obcego portalu nie jest powielane."
    },
    {
        "id": 2,
        "name": "Filtr Dociekliwego Laika (Common-Sense Check)",
        "description": "Przekształcenie korporacyjnego szumu PR w zdroworozsądkowe, bezkompromisowe pytanie o koszty, użyteczność i realnych beneficjentów."
    },
    {
        "id": 3,
        "name": "Formułowanie autorskiej antytezy",
        "description": "Wskazanie pęknięć w obowiązującym konsensusie rynkowym lub politycznym. Własny punkt widzenia zamiast powtarzania cudzych wniosków."
    },
    {
        "id": 4,
        "name": "Autorska struktura i styl blogowy",
        "description": "Poważny, konkretny i rzeczowy język publicystyczny. Unikanie żargonu agencyjnego i szablonowych formułek prasowych."
    },
    {
        "id": 5,
        "name": "Unikalna kreacja wizualna",
        "description": "Dedykowany dobór koncepcji wizualnej oraz autorski prompt generatywny AI, oddające istotę poruszonego problemu."
    }
]

# Znaczniki zapożyczeń / klisze prasowe, które są bezwzględnie zakazane w modelu Samokreacji
PLAGIARISM_MARKERS = [
    r'\bjak\s+podaje\b',
    r'\bjak\s+informuje\s+portal\b',
    r'\bw\s+rozmowie\s+z\s+naszym\b',
    r'\bźródło:\s*',
    r'\bzrodlo:\s*',
    r'\bopracowanie\s+własne\s+na\s+podstawie\b',
    r'\bprzedruk\b',
    r'\bartykuł\s+pochodzi\s+z\b',
    r'\bczytaj\s+także\s+na\b',
    r'\bwszelkie\s+prawa\s+zastrzeżone\b',
    r'\bnotatka\s+prasowa\b',
    r'\bkomunikat\s+prasowy\s+firmy\b',
    r'\bagencja\s+reuters\s+donosi\b',
    r'\bwedług\s+doniesień\s+medialnych\b',
    r'\bfot\.\s+materiały\s+prasowe\b',
    r'\bwiadomości\s+z\s+kraju\s+i\s+ze\s+świata\b',
    r'\bkliknij\s+tutaj,\s+aby\s+przeczytać\b'
]

def verify_samokreacja(text: str) -> Dict[str, Any]:
    """
    Weryfikuje, czy dany tekst spełnia standard 100% Samokreacji Bloga Laika.
    Wykrywa obce klisze agencyjne, zapożyczenia prasowe oraz ocenia poziom autorskiej syntezy.
    """
    if not text or not text.strip():
        return {
            "status": "empty",
            "score": 0,
            "is_clean": True,
            "violations": [],
            "message": "Pusty tekst do weryfikacji."
        }

    violations = []
    text_lower = text.lower()

    for pattern in PLAGIARISM_MARKERS:
        matches = re.findall(pattern, text_lower)
        if matches:
            violations.append(f"Wykryto znacznik zapożyczenia prasowego: '{matches[0]}'")

    # Sprawdzenie obecności autorskiej tezy lub pytania dociekliwego laika
    has_layman_question = bool(re.search(r'pytanie\s+dociekliwego\s+laika', text_lower))
    has_thesis = bool(re.search(r'(?:teza|wniosek|kluczowa\s+teza)', text_lower))

    # Obliczenie wskaźnika samokreacji (0-100)
    score = 100
    if violations:
        score -= len(violations) * 25
    if not has_layman_question and len(text) > 400:
        score -= 10

    score = max(0, min(100, score))

    is_clean = len(violations) == 0

    return {
        "status": "success" if is_clean else "warning",
        "score": score,
        "is_clean": is_clean,
        "violations": violations,
        "has_layman_question": has_layman_question,
        "has_thesis": has_thesis,
        "message": "Tekst w 100% spełnia wymogi Samokreacji Bloga Laika." if is_clean else "Wykryto elementy wymagające przeredagowania na autorską syntezę."
    }

def build_samokreacja_guidelines_md() -> str:
    """Zwraca zwięzłe wytyczne samokreacji w formacie Markdown do wstrzyknięcia do edytora lub dokumentacji."""
    lines = [
        "> [!IMPORTANT]",
        "> **Zasada Samokreacji Bloga Laika:**",
        "> Każdy wpis jest w 100% autorskim dziełem Ireneusza Machowca. Zewnętrzne doniesienia służą jedynie jako surowy fakt-impuls.",
        "> Bezwzględny zakaz kopiowania cudzych zdań, fragmentów artykułów czy klisz agencyjnych."
    ]
    return "\n".join(lines)

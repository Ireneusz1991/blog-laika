"""
Sanitizer usuwający z treści artykułów:
1. Dopiski sugerujące użycie AI (np. „Wersja Bielik AI”, „Zredagowana przez polski model językowy”).
2. Teksty techniczne i wewnętrzne etykiety algorytmu tworzącego treść
   (np. „Impuls źródłowy”, „Model Samokreacji”, „Data skanowania z palca”,
   „Źródła z monitoringu RSS”, „kondensacja redakcyjna”, „Sygnał spod powierzchni...”,
   „w strumieniu wiadomości”, „First Principles Thinking”).

Oznaczenia robocze (wersja A/B, źródło RSS) mogą istnieć wyłącznie w interfejsie
panelu administratora — nigdy w samej treści ani w tytule publikacji.
"""
import re

_TITLE_SUFFIX_RX = re.compile(r'\s*\((?:Wersja|Redakcja)\s+Bielik\s+AI[^)]*\)', re.IGNORECASE)

_BLOCKQUOTE_AI_RX = re.compile(
    r'^[ \t]*>[ \t]*(?:🦅[ \t]*)?\*\*Wersja Bielik AI:?\*\*:?[^\n]*\n?',
    re.MULTILINE | re.IGNORECASE
)
_BLOCKQUOTE_TECH_RX = re.compile(
    r'^[ \t]*>[ \t]*(?:📡|🛡️|⚡|🦅|📚)?[ \t]*\*\*(?:'
    r'Impuls źródłowy(?:\s*\([^)]*\))?|'
    r'Źródło impulsu(?:\s+i inspiracji(?:\s+rynkowej)?)?|'
    r'Źródło inspiracji(?:\s+z Banku Wiedzy(?:\s+Bloga Laika)?)?|'
    r'Model Samokreacji(?:\s+Bloga Laika)?|'
    r'KONDENSAT REDAKCYJNY(?:\s*\([^)]*\))?|'
    r'Źródła syntezy'
    r'):?\*\*:?[^\n]*\n?',
    re.MULTILINE | re.IGNORECASE
)
_META_ITALIC_LINE_RX = re.compile(
    r'^[ \t]*\*?(?:Data skanowania z palca|Data syntezy na żywo|Data wyszukania i analizy tematu|Autorski wpis Bloga Laika\.\s*100%\s*Samokreacja)[^\n]*\*?[ \t]*\n?',
    re.MULTILINE | re.IGNORECASE
)
_MODEL_LINE_RX = re.compile(
    r'^[ \t]*>?[ \t]*[^\n]*Zredagowan[aey] przez (?:polski )?model językowy[^\n]*\n?',
    re.MULTILINE | re.IGNORECASE
)
_HEADING_BIELIK_RX = re.compile(
    r'^(#{1,6})[ \t]*(?:🦅[ \t]*)?Kąt widzenia Bielik AI:?[ \t]*',
    re.MULTILINE | re.IGNORECASE
)
_FOOTER_RX = re.compile(
    r'(?:\n[ \t]*---[ \t]*\n+)?[ \t]*\*?Redakcja i kondensacja:[^\n]*(?:Bielik|model językowy)[^\n]*\*?[ \t]*\n?',
    re.IGNORECASE
)
_ALT_SZKIC_RX = re.compile(r'Alternatywny szkic Bielik AI', re.IGNORECASE)

# Wewnętrzne sformułowania algorytmu pojawiające się w nagłówkach i zdaniach treści:
_TECH_REPLACEMENTS = [
    (re.compile(r'\s*\(kondensacja redakcyjna\)', re.IGNORECASE), ''),
    (re.compile(r'\s*\(First Principles Thinking\)', re.IGNORECASE), ''),
    (re.compile(r'\s*\(RSS Live\)', re.IGNORECASE), ''),
    (re.compile(r'\s*\(Konglomerat Wielowątkowy[^)]*\)', re.IGNORECASE), ''),
    (re.compile(r'^(#{1,6}[ \t]*(?:\d+\.[ \t]*)?)Źródła z monitoringu RSS[ \t]*$', re.MULTILINE | re.IGNORECASE), r'\1Analizy i źródła prasowe'),
    (re.compile(r'^(#{1,6}[ \t]*(?:\d+\.[ \t]*)?)Impuls rynkowy i analizy[ \t]*$', re.MULTILINE | re.IGNORECASE), r'\1Bieżące analizy rynkowe'),
    (re.compile(r'^(#{1,6}[ \t]*(?:\d+\.[ \t]*)?)Sygnał spod powierzchni codziennych nagłówków[ \t]*$', re.MULTILINE | re.IGNORECASE), r'\1Co kryje się pod powierzchnią codziennych nagłówków'),
    (re.compile(r'^(#{1,6}[ \t]*)Węzeł[ \t]+(\d+)[ \t]*:[ \t]*', re.MULTILINE | re.IGNORECASE), r'\1\2. '),
    (re.compile(r'^(#{1,6}[ \t]*)Węzeł[ \t]+(\d+)[ \t]*\([^)\n]*—[ \t]*sygnał z[^)\n]*\)', re.MULTILINE | re.IGNORECASE), r'\1Część \2.'),
    (re.compile(r'\bJednak bieżący impuls rynkowy\b', re.IGNORECASE), 'Jednak bieżąca debata rynkowa'),
    (re.compile(r'\bKiedy w strumieniu wiadomości pojawia się wątek\b', re.IGNORECASE), 'Kiedy w debacie publicznej pojawia się temat'),
    (re.compile(r'\bImpuls płynący z bieżących analiz\b', re.IGNORECASE), 'Wątek podjęty w bieżących analizach'),
    (re.compile(r'\bImpuls intelektualny z bieżącej lektury\b', re.IGNORECASE), 'Wątek z bieżącej lektury'),
    (re.compile(r'\bNajnowszy sygnał z obszaru\b', re.IGNORECASE), 'Najnowsze doniesienia z obszaru'),
    (re.compile(r'\bŚwieży sygnał ze źródła\b', re.IGNORECASE), 'Publikacja ze źródła'),
    (re.compile(r'\bDzisiejszy splot impulsów analitycznych\b', re.IGNORECASE), 'Zestawienie najważniejszych tematów'),
    (re.compile(r'\bAutorska synteza 4 węzłowych impulsów dnia\b', re.IGNORECASE), 'Przekrojowe spojrzenie na cztery kluczowe zjawiska dnia'),
    (re.compile(r'\bAutorska supersynteza łącząca 4 świeżo zeskanowane impulsy\b', re.IGNORECASE), 'Przekrojowe spojrzenie łączące cztery ważne wątki'),
    (re.compile(r'\bPunktem wyjścia w tym segmencie jest impuls:\s*', re.IGNORECASE), 'Punktem wyjścia jest tu wątek: '),
    (re.compile(r'\bLekcja płynąca z tego impulsu\b', re.IGNORECASE), 'Lekcja płynąca z tej analizy'),
    (re.compile(r'\bdrugiego ogniwa dzisiejszego konglomeratu\b', re.IGNORECASE), 'drugiego wymiaru obecnej sytuacji'),
    (re.compile(r'\*\*Kondensacja priorytetów państwa:\*\*', re.IGNORECASE), '**Koncentracja priorytetów państwa:**'),
    (re.compile(r'\*\*Teza spajająca konglomerat:\*\*', re.IGNORECASE), '**Teza przewodnia:**'),
]


def clean_title(title: str) -> str:
    if not title:
        return title
    return _TITLE_SUFFIX_RX.sub('', title).strip()


def strip_ai_attribution(text: str) -> str:
    """Usuwa dopiski o AI oraz wewnętrzne sformułowania algorytmu z Markdownu."""
    if not text:
        return text
    out = _TITLE_SUFFIX_RX.sub('', text)
    out = _BLOCKQUOTE_AI_RX.sub('', out)
    out = _BLOCKQUOTE_TECH_RX.sub('', out)
    out = _META_ITALIC_LINE_RX.sub('', out)
    out = _MODEL_LINE_RX.sub('', out)
    out = _HEADING_BIELIK_RX.sub(lambda m: m.group(1) + ' ', out)
    out = _FOOTER_RX.sub('\n', out)
    out = _ALT_SZKIC_RX.sub('Alternatywny szkic', out)
    for rx, repl in _TECH_REPLACEMENTS:
        out = rx.sub(repl, out)
    out = re.sub(r'\n{3,}', '\n\n', out)
    return out.rstrip() + ('\n' if text.endswith('\n') else '')

"""
Sanitizer usuwający z treści artykułów wszelkie dopiski sugerujące, że tekst
został napisany / zredagowany przez sztuczną inteligencję (np. „Wersja Bielik AI”,
„Zredagowana przez polski model językowy”, „Kąt widzenia Bielik AI”,
„Redakcja i kondensacja: Polski model językowy Bielik AI & Blog Laika”).

Oznaczenia wersji (A/B, Bielik) mogą istnieć wyłącznie jako metadane w panelu
administratora — nigdy w samej treści, tytule ani w opublikowanym wpisie.
"""
import re

_TITLE_SUFFIX_RX = re.compile(r'\s*\((?:Wersja|Redakcja)\s+Bielik\s+AI[^)]*\)', re.IGNORECASE)
_BLOCKQUOTE_RX = re.compile(r'^[ \t]*>[ \t]*(?:🦅[ \t]*)?\*\*Wersja Bielik AI:?\*\*:?[^\n]*\n?', re.MULTILINE | re.IGNORECASE)
_MODEL_LINE_RX = re.compile(r'^[ \t]*>?[ \t]*[^\n]*Zredagowan[aey] przez (?:polski )?model językowy[^\n]*\n?', re.MULTILINE | re.IGNORECASE)
_HEADING_RX = re.compile(r'^(#{1,6})[ \t]*(?:🦅[ \t]*)?Kąt widzenia Bielik AI:?[ \t]*', re.MULTILINE | re.IGNORECASE)
_FOOTER_RX = re.compile(r'(?:\n[ \t]*---[ \t]*\n+)?[ \t]*\*?Redakcja i kondensacja:[^\n]*(?:Bielik|model językowy)[^\n]*\*?[ \t]*\n?', re.IGNORECASE)
_ALT_SZKIC_RX = re.compile(r'Alternatywny szkic Bielik AI', re.IGNORECASE)


def clean_title(title: str) -> str:
    if not title:
        return title
    return _TITLE_SUFFIX_RX.sub('', title).strip()


def strip_ai_attribution(text: str) -> str:
    """Usuwa dopiski o AI z Markdownu, zachowując merytoryczną treść."""
    if not text:
        return text
    out = _TITLE_SUFFIX_RX.sub('', text)
    out = _BLOCKQUOTE_RX.sub('', out)
    out = _MODEL_LINE_RX.sub('', out)
    out = _HEADING_RX.sub(lambda m: m.group(1) + ' ', out)
    out = _FOOTER_RX.sub('\n', out)
    out = _ALT_SZKIC_RX.sub('Alternatywny szkic', out)
    out = re.sub(r'\n{3,}', '\n\n', out)
    return out.rstrip() + ('\n' if text.endswith('\n') else '')

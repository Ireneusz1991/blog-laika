# -*- coding: utf-8 -*-
"""
Rejestr Źródeł Redakcyjnych i Analitycznych dla Bloga Laika.
Zawiera polskie i międzynarodowe media, think-tanki, serwisy finansowe i kanały debaty publicznej,
z których pobierane są impulsy faktograficzne i tematy do autorskiej Samokreacji.
"""

EDITORIAL_SOURCES = [
    # -------------------------------------------------------------
    # 1. POLSKA PUBLICYSTYKA, SPOŁECZEŃSTWO I POLITYKA
    # -------------------------------------------------------------
    {
        "id": "kultura_liberalna",
        "name": "Kultura Liberalna",
        "scope": "Polska / Europa",
        "lang": "PL",
        "flag": "🇵🇱",
        "type": "Tygodnik opinii / Think tank",
        "url": "https://kulturaliberalna.pl",
        "topics": ["Polityka", "Instytucje demokratyczne", "Kultura", "Filozofia społeczna", "Europa"],
        "desc": "Liberalny namysł nad państwem, prawem, kulturą i przemianami cywilizacyjnymi. Unika taniego populizmu."
    },
    {
        "id": "klub_jagiellonski",
        "name": "Klub Jagielloński",
        "scope": "Polska",
        "lang": "PL",
        "flag": "🇵🇱",
        "type": "Centrum analityczne / Pismo opinii",
        "url": "https://klubjagiellonski.pl",
        "topics": ["Wydolność państwa", "Demografia", "Deglomeracja", "Gospodarka", "Suwerenność"],
        "desc": "Republikańska i propaństwowa analiza instytucji, 'państwa z kartonu', polityki regionalnej i demografii."
    },
    {
        "id": "kanal_zero",
        "name": "Kanał Zero (Publicystyka & Debaty)",
        "scope": "Polska / Świat",
        "lang": "PL",
        "flag": "🇵🇱",
        "type": "Media internetowe / Format debat",
        "url": "https://www.youtube.com/@KanalZeroPL",
        "topics": ["Debaty polityczne", "Gospodarka", "Geopolityka", "Spory społeczne", "Media"],
        "desc": "Szeroka dyskusja społeczna bez poprawności politycznej. Zderzenie różnych perspektyw w kluczowych sporach Polaków."
    },
    {
        "id": "osw",
        "name": "Ośrodek Studiów Wschodnich (OSW)",
        "scope": "Europa Środkowa / Wschód / Świat",
        "lang": "PL / EN",
        "flag": "🇵🇱",
        "type": "Rządowy instytut analityczny",
        "url": "https://www.osw.waw.pl",
        "topics": ["Geopolityka", "Bezpieczeństwo", "Energetyka", "Niemcy", "Ukraina", "Rosja"],
        "desc": "Niezrównany, chłodny i precyzyjny aparat analityczny w sprawach bezpieczeństwa, surowców i równowagi sił."
    },
    {
        "id": "interia",
        "name": "Interia (Wydarzenia & Biznes)",
        "scope": "Polska",
        "lang": "PL",
        "flag": "🇵🇱",
        "type": "Portal ogólnoinformacyjny",
        "url": "https://wydarzenia.interia.pl",
        "topics": ["Wiadomości krajowe", "Gospodarka codzienna", "Nastroje społeczne", "Prawo"],
        "desc": "Puls codziennego życia gospodarczego i politycznego w Polsce. Weryfikacja twardych decyzji rządu i nastrojów."
    },
    {
        "id": "nowa_konfederacja",
        "name": "Nowa Konfederacja",
        "scope": "Polska / Geopolityka",
        "lang": "PL",
        "flag": "🇵🇱",
        "type": "Thinkzine",
        "url": "https://nowakonfederacja.pl",
        "topics": ["Bezpieczeństwo narodowe", "Konstytucjonalizm", "Dyplomacja", "Przemysł obronny"],
        "desc": "Eksperckie spojrzenie na strategiczne interesy Polski, relacje transatlantyckie i stan sił zbrojnych."
    },

    # -------------------------------------------------------------
    # 2. GOSPODARKA, RYNKI I MAKROEKONOMIA
    # -------------------------------------------------------------
    {
        "id": "financial_times",
        "name": "The Financial Times (FT)",
        "scope": "Globalny",
        "lang": "EN (do translacji)",
        "flag": "🇬🇧",
        "type": "Dziennik finansowy / Global benchmark",
        "url": "https://www.ft.com",
        "topics": ["Makroekonomia", "Banki centralne (FED/EBC)", "Dług publiczny", "Handel globalny", "Geonomia"],
        "desc": "Światowy punkt odniesienia w analityce rynkowej. Wyjaśnia głębokie przepływy kapitałowe i politykę stóp procentowych."
    },
    {
        "id": "investing",
        "name": "Investing.com",
        "scope": "Globalny / Rynki",
        "lang": "EN / PL",
        "flag": "🌍",
        "type": "Platforma rynkowa i surowcowa",
        "url": "https://pl.investing.com",
        "topics": ["Ropa i gaz", "Obligacje skarbowe", "Waluty", "Kruszce", "Wskaźniki PMI/CPI"],
        "desc": "Dane rynkowe w czasie rzeczywistym, spready rentowności obligacji i twarde wskaźniki makro."
    },
    {
        "id": "bankier",
        "name": "Bankier.pl / Forsal",
        "scope": "Polska",
        "lang": "PL",
        "flag": "🇵🇱",
        "type": "Portal finansowo-ekonomiczny",
        "url": "https://www.bankier.pl",
        "topics": ["Stopy NBP", "Rynek nieruchomości", "Kredyty hipoteczne", "Podatki", "Budżet państwa"],
        "desc": "Kluczowe źródło danych o kondycji portfela polskiego obywatela, rynku mieszkań i polityce monetarnej RPP."
    },
    {
        "id": "bloomberg",
        "name": "Bloomberg Markets",
        "scope": "Globalny",
        "lang": "EN (do translacji)",
        "flag": "🇺🇸",
        "type": "Agencja analityczno-finansowa",
        "url": "https://www.bloomberg.com",
        "topics": ["Finanse korporacyjne", "Rynek surowców", "Łańcuchy dostaw", "Energetyka"],
        "desc": "Twarde dane z terminali rynkowych dotyczące fuzji, długu, sankcji oraz kondycji największych korporacji świata."
    },

    # -------------------------------------------------------------
    # 3. POLITYKA MIĘDZYNARODOWA I GEOPOLITYKA
    # -------------------------------------------------------------
    {
        "id": "foreign_affairs",
        "name": "Foreign Affairs",
        "scope": "Globalny",
        "lang": "EN (do translacji)",
        "flag": "🇺🇸",
        "type": "Kwartalnik stosunków międzynarodowych",
        "url": "https://www.foreignaffairs.com",
        "topics": ["Wielka strategia", "Rywalizacja mocarstw", "Przyszłość NATO", "Ład postliberalny"],
        "desc": "Najbardziej wpływowy magazyn politologiczny świata. Kształtuje debaty o równowadze sił i doktrynach obronnych."
    },
    {
        "id": "politico_eu",
        "name": "Politico Europe",
        "scope": "Unia Europejska",
        "lang": "EN (do translacji)",
        "flag": "🇪🇺",
        "type": "Dziennikarstwo śledcze i unijne",
        "url": "https://www.politico.eu",
        "topics": ["Bruksela", "Komisja Europejska", "Regulacje handlowe", "Polityka klimatyczna", "Lobbying"],
        "desc": "Kulisy unijnych instytucji, targi między Berlinem, Paryżem i Warszawą oraz mechanizmy unijnego prawa."
    },

    # -------------------------------------------------------------
    # 4. TECHNOLOGIA, CYFRYZACJA I SUWERENNOŚĆ
    # -------------------------------------------------------------
    {
        "id": "ars_technica",
        "name": "Ars Technica",
        "scope": "Globalny",
        "lang": "EN (do translacji)",
        "flag": "🇺🇸",
        "type": "Publicystyka technologiczna",
        "url": "https://arstechnica.com",
        "topics": ["Cyberbezpieczeństwo", "Hardware", "Polityka cyfrowa", "Kryptografia", "Prawa cyfrowe"],
        "desc": "Rzetelne dziennikarstwo technologiczne bez bezkrytycznego zachwytu nad nowościami. Twarda ocena kodu i sprzętu."
    },
    {
        "id": "mit_tech_review",
        "name": "MIT Technology Review",
        "scope": "Globalny",
        "lang": "EN (do translacji)",
        "flag": "🇺🇸",
        "type": "Magazyn naukowo-technologiczny",
        "url": "https://www.technologyreview.com",
        "topics": ["Etyka technologii", "Przełomy laboratoryjne", "Klimatotech", "Biotechnologia"],
        "desc": "Krytyczny namysł nad wpływem inżynierii na społeczeństwo, rynek pracy i przyszłość człowieka."
    }
]

def get_source_by_id(source_id: str) -> dict:
    for s in EDITORIAL_SOURCES:
        if s["id"] == source_id:
            return s
    return {
        "id": source_id,
        "name": source_id.replace("_", " ").title(),
        "flag": "🌐",
        "scope": "Ogólne",
        "lang": "PL"
    }

def get_sources_by_category(category: str) -> list:
    mapping = {
        "technologia": ["ars_technica", "mit_tech_review", "bloomberg"],
        "gospodarka": ["financial_times", "investing", "bankier", "bloomberg", "interia"],
        "polityka": ["kultura_liberalna", "klub_jagiellonski", "osw", "kanal_zero", "foreign_affairs", "politico_eu", "nowa_konfederacja"],
        "eseje": ["kultura_liberalna", "klub_jagiellonski", "kanal_zero", "foreign_affairs"]
    }
    allowed_ids = mapping.get(category, [])
    return [s for s in EDITORIAL_SOURCES if s["id"] in allowed_ids]

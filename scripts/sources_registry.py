# -*- coding: utf-8 -*-
"""
Rejestr Źródeł Redakcyjnych, Analitycznych i Inspiracji dla Bloga Laika.
Zawiera polskie i międzynarodowe media, eseje, think-tanki, serwisy finansowe oraz profile na X i LinkedIn,
z których pobierane są impulsy faktograficzne i metodologiczne do autorskiej Samokreacji.
"""
import os
import csv

EDITORIAL_SOURCES = [
    # =============================================================
    # 1. POLSKA — BEZPOŚREDNIA KONKURENCJA / INSPIRACJA ESEJOWA
    # =============================================================
    {
        "id": "kultura_liberalna",
        "name": "Kultura Liberalna",
        "category_group": "PL_ESEJ",
        "region": "Polska",
        "scope": "Polska / Europa",
        "lang": "PL",
        "flag": "🇵🇱",
        "type": "Tygodnik opinii / Think tank",
        "url": "https://kulturaliberalna.pl",
        "social": {
            "x": "https://x.com/KulturaLiberalna",
            "linkedin": "https://www.linkedin.com/company/kultura-liberalna/",
            "facebook": "https://www.facebook.com/KulturaLiberalna",
            "youtube": "https://www.youtube.com/@KulturaLiberalna"
        },
        "topics": ["Polityka", "Instytucje demokratyczne", "Kultura", "Filozofia społeczna", "Europa"],
        "desc": "Liberalny namysł nad państwem, prawem, kulturą i przemianami cywilizacyjnymi. Unika taniego populizmu.",
        "takeaway": "Nienachalny, elegancki ton namysłu nad instytucjami; eseje społeczne bez tabloidyzacji; newsletter ideowy wysokiej próby."
    },
    {
        "id": "klub_jagiellonski",
        "name": "Klub Jagielloński",
        "category_group": "PL_ESEJ",
        "region": "Polska",
        "scope": "Polska",
        "lang": "PL",
        "flag": "🇵🇱",
        "type": "Centrum analityczne / Pismo opinii",
        "url": "https://klubjagiellonski.pl",
        "social": {
            "x": "https://x.com/KlubJagiellonski",
            "linkedin": "https://www.linkedin.com/company/klub-jagielloński/",
            "facebook": "https://www.facebook.com/KlubJagiellonski/"
        },
        "topics": ["Wydolność państwa", "Demografia", "Deglomeracja", "Gospodarka", "Suwerenność"],
        "desc": "Republikańska i propaństwowa analiza instytucji, 'państwa z kartonu', polityki regionalnej i demografii.",
        "takeaway": "Twarda propaństwowość, diagnoza wad systemowych urzędów i prawa, regionalizm (Polska poza metropoliami) oraz demografia."
    },
    {
        "id": "nowa_konfederacja",
        "name": "Nowa Konfederacja",
        "category_group": "PL_ESEJ",
        "region": "Polska",
        "scope": "Polska / Geopolityka",
        "lang": "PL",
        "flag": "🇵🇱",
        "type": "Thinkzine / Ośrodek analityczny",
        "url": "https://nowakonfederacja.pl",
        "social": {
            "x": "https://x.com/NKonfederacja",
            "linkedin": "https://www.linkedin.com/company/nowa-konfederacja/",
            "youtube": "https://www.youtube.com/@NowaKonfederacja"
        },
        "topics": ["Bezpieczeństwo narodowe", "Konstytucjonalizm", "Dyplomacja", "Przemysł obronny"],
        "desc": "Eksperckie spojrzenie na strategiczne interesy Polski, relacje transatlantyckie i stan sił zbrojnych.",
        "takeaway": "Chłodny realizm geopolityczny, zbrojenia bez emocji propagandowych, bezlitosny bilans polskich interesów narodowych."
    },
    {
        "id": "krytyka_polityczna",
        "name": "Krytyka Polityczna",
        "category_group": "PL_ESEJ",
        "region": "Polska",
        "scope": "Polska / Społeczeństwo",
        "lang": "PL",
        "flag": "🇵🇱",
        "type": "Pismo społeczno-polityczne / Wydawnictwo",
        "url": "https://krytykapolityczna.pl",
        "social": {
            "x": "https://x.com/Krytyka",
            "linkedin": "https://www.linkedin.com/company/krytyka-polityczna/",
            "facebook": "https://www.facebook.com/KrytykaPolityczna/"
        },
        "topics": ["Rynek mieszkaniowy", "Prawa pracownicze", "Prekariat", "Ekologia", "Krytyka neoliberalizmu"],
        "desc": "Lewicowa perspektywa na koszty transformacji, nierówności majątkowe, wyzwania socjalne i rynek najmu.",
        "takeaway": "Wrażliwość na społeczne koszty rynkowych reform, problematyka rentierstwa i mieszkań, nośne i zaczepne tytuły esejowe."
    },
    {
        "id": "magazyn_kontakt_8000",
        "name": "Magazyn Kontakt / 8000 (Osiem tysięcy)",
        "category_group": "PL_ESEJ",
        "region": "Polska",
        "scope": "Polska / Gospodarka",
        "lang": "PL",
        "flag": "🇵🇱",
        "type": "Magazyn idei & Najlepszy newsletter gospodarczy LinkedIn",
        "url": "https://magazynkontakt.pl",
        "social": {
            "x": "https://x.com/MagazynKontakt",
            "linkedin": "https://www.linkedin.com/newsletters/osiem-tysi%C4%99cy-6962043685532585984/"
        },
        "topics": ["Dane makroekonomiczne", "Etyka społeczna", "Rynek pracy", "Płace", "Wykresy tygodnia"],
        "desc": "Dwa wzorce: Magazyn Kontakt (społeczno-etyczny) oraz '8000' – wybitny newsletter gospodarczy na LinkedIn.",
        "takeaway": "Format 'Osiem tysięcy' (8000): czyste wykresy, twarde dane makro podane bez hermetycznego żargonu ekonomicznego."
    },
    {
        "id": "kanal_zero",
        "name": "Kanał Zero (Publicystyka & Debaty)",
        "category_group": "PL_ESEJ",
        "region": "Polska",
        "scope": "Polska / Świat",
        "lang": "PL",
        "flag": "🇵🇱",
        "type": "Media internetowe / Format debat",
        "url": "https://www.youtube.com/@KanalZeroPL",
        "social": {
            "x": "https://x.com/OficjalneZero",
            "youtube": "https://www.youtube.com/@KanalZeroPL"
        },
        "topics": ["Debaty polityczne", "Gospodarka", "Geopolityka", "Spory społeczne", "Media"],
        "desc": "Szeroka dyskusja społeczna bez poprawności politycznej. Zderzenie różnych perspektyw w kluczowych sporach Polaków.",
        "takeaway": "Bezkompromisowe zadawanie prostych, laickich pytań ekspertom; dynamika starć argumentacyjnych na żywo."
    },
    {
        "id": "osw",
        "name": "Ośrodek Studiów Wschodnich (OSW)",
        "category_group": "PL_ESEJ",
        "region": "Polska",
        "scope": "Europa Środkowa / Wschód / Świat",
        "lang": "PL / EN",
        "flag": "🇵🇱",
        "type": "Rządowy instytut analityczny",
        "url": "https://www.osw.waw.pl",
        "social": {
            "x": "https://x.com/OSW_pl",
            "youtube": "https://www.youtube.com/@OSWOsrodekStudiowWschodnich"
        },
        "topics": ["Geopolityka", "Bezpieczeństwo", "Energetyka", "Niemcy", "Ukraina", "Rosja"],
        "desc": "Niezrównany, chłodny i precyzyjny aparat analityczny w sprawach bezpieczeństwa, surowców i równowagi sił.",
        "takeaway": "Rygor faktograficzny, oparcie na źródłach pierwotnych, myślenie procesami wieloletnimi a nie nagłówkami z wczoraj."
    },
    {
        "id": "interia",
        "name": "Interia (Wydarzenia & Biznes)",
        "category_group": "PL_ESEJ",
        "region": "Polska",
        "scope": "Polska",
        "lang": "PL",
        "flag": "🇵🇱",
        "type": "Portal ogólnoinformacyjny",
        "url": "https://wydarzenia.interia.pl",
        "social": {
            "x": "https://x.com/Int_Wydarzenia",
            "facebook": "https://www.facebook.com/interia"
        },
        "topics": ["Wiadomości krajowe", "Gospodarka codzienna", "Nastroje społeczne", "Prawo"],
        "desc": "Puls codziennego życia gospodarczego i politycznego w Polsce. Weryfikacja twardych decyzji rządu i nastrojów.",
        "takeaway": "Przekładanie skomplikowanych projektów ustaw na realny portfel i życie przeciętnego obywatela."
    },

    # =============================================================
    # 2. GOSPODARKA OGÓLNA, BIZNES I SUROWCE
    # =============================================================
    {
        "id": "business_insider",
        "name": "Business Insider (Polska & Global)",
        "category_group": "BIZNES_MAKRO",
        "region": "Polska / Globalny",
        "scope": "Gospodarka / Rynki / Biznes",
        "lang": "PL / EN",
        "flag": "🌍",
        "type": "Portal biznesowo-ekonomiczny",
        "url": "https://businessinsider.com.pl",
        "social": {
            "x": "https://x.com/BIPolska",
            "linkedin": "https://www.linkedin.com/company/business-insider-polska/"
        },
        "topics": ["Makroekonomia", "Trendy rynkowe", "Praca i wynagrodzenia", "Przedsiębiorczość", "Ceny surowców"],
        "desc": "Jeden z najpopularniejszych serwisów gospodarczych na świecie. Tłumaczy mechanizmy rynkowe i zmiany nawyków konsumentów.",
        "takeaway": "Dynamika narracji biznesowej, chwytliwe i merytoryczne ujęcia makro, zwięzłe infografiki trendów i psychologia pracy."
    },
    {
        "id": "financial_times",
        "name": "The Financial Times (FT)",
        "category_group": "BIZNES_MAKRO",
        "region": "Zagranica",
        "scope": "Globalny",
        "lang": "EN (do translacji)",
        "flag": "🇬🇧",
        "type": "Dziennik finansowy / Global benchmark",
        "url": "https://www.ft.com",
        "social": {
            "x": "https://x.com/FinancialTimes",
            "linkedin": "https://www.linkedin.com/company/financial-times/"
        },
        "topics": ["Makroekonomia", "Banki centralne (FED/EBC)", "Dług publiczny", "Handel globalny", "Geonomia"],
        "desc": "Światowy punkt odniesienia w analityce rynkowej. Wyjaśnia głębokie przepływy kapitałowe i politykę stóp procentowych.",
        "takeaway": "Globalny standard analizy długu suwerennego, polityki banków centralnych i długich cykli inwestycyjnych."
    },
    {
        "id": "investing",
        "name": "Investing.com",
        "category_group": "BIZNES_MAKRO",
        "region": "Zagranica",
        "scope": "Globalny / Rynki",
        "lang": "EN / PL",
        "flag": "🌍",
        "type": "Platforma rynkowa i surowcowa",
        "url": "https://pl.investing.com",
        "social": {
            "x": "https://x.com/Investingcom"
        },
        "topics": ["Ropa i gaz", "Obligacje skarbowe", "Waluty", "Kruszce", "Wskaźniki PMI/CPI"],
        "desc": "Dane rynkowe w czasie rzeczywistym, spready rentowności obligacji i twarde wskaźniki makro.",
        "takeaway": "Twarde dane liczbowe (rentowności 10-letnich obligacji, notowania ropy Brent i gazu TTF) jako tło dla polskich wpisów."
    },
    {
        "id": "bankier",
        "name": "Bankier.pl / Forsal",
        "category_group": "BIZNES_MAKRO",
        "region": "Polska",
        "scope": "Polska",
        "lang": "PL",
        "flag": "🇵🇱",
        "type": "Portal finansowo-ekonomiczny",
        "url": "https://www.bankier.pl",
        "social": {
            "x": "https://x.com/bankier_pl",
            "facebook": "https://www.facebook.com/bankierpl"
        },
        "topics": ["Stopy NBP", "Rynek nieruchomości", "Kredyty hipoteczne", "Podatki", "Budżet państwa"],
        "desc": "Kluczowe źródło danych o kondycji portfela polskiego obywatela, rynku mieszkań i polityce monetarnej RPP.",
        "takeaway": "Rozliczanie kolejnych programów dopłat mieszkaniowych i twarde dane o realnej sile nabywczej pensji."
    },
    {
        "id": "bloomberg",
        "name": "Bloomberg Markets",
        "category_group": "BIZNES_MAKRO",
        "region": "Zagranica",
        "scope": "Globalny",
        "lang": "EN (do translacji)",
        "flag": "🇺🇸",
        "type": "Agencja analityczno-finansowa",
        "url": "https://www.bloomberg.com",
        "social": {
            "x": "https://x.com/business",
            "linkedin": "https://www.linkedin.com/company/bloomberg-lp/"
        },
        "topics": ["Finanse korporacyjne", "Rynek surowców", "Łańcuchy dostaw", "Energetyka"],
        "desc": "Twarde dane z terminali rynkowych dotyczące fuzji, długu, sankcji oraz kondycji największych korporacji świata.",
        "takeaway": "Ekspresowa identyfikacja punktów zwrotnych w łańcuchach dostaw i decyzjach kapitałowych funduszy private equity."
    },

    # =============================================================
    # 3. ZAGRANICA — WZORCE ESEJOWE I METODOLOGICZNE DLA BLOGA LAIKA
    # =============================================================
    {
        "id": "works_in_progress",
        "name": "Works in Progress",
        "category_group": "ENG_ESEJ",
        "region": "Zagranica",
        "scope": "Świat / Cywilizacja",
        "lang": "EN (do translacji)",
        "flag": "🇬🇧",
        "type": "Magazyn esejów o postępie (Stripe Press)",
        "url": "https://worksinprogress.co",
        "social": {
            "x": "https://x.com/worksinprogress"
        },
        "topics": ["Postęp cywilizacyjny", "Infrastruktura", "Historia innowacji", "Materiały", "Miasta"],
        "desc": "Wybitny magazyn długich, dogłębnych esejów badających dlaczego rzeczy w świecie realnym działają tak, jak działają.",
        "takeaway": "Nacisk na fizyczny świat (budownictwo, energetyka, rolnictwo), drobiazgowość dowodowa i piękna, czysta typografia eseju."
    },
    {
        "id": "astral_codex_ten",
        "name": "Astral Codex Ten (Scott Alexander)",
        "category_group": "ENG_ESEJ",
        "region": "Zagranica",
        "scope": "Świat / Racjonalność",
        "lang": "EN (do translacji)",
        "flag": "🇺🇸",
        "type": "Substack / Eseje racjonalistyczne",
        "url": "https://www.astralcodexten.com",
        "social": {
            "x": "https://x.com/slatestarcodex",
            "substack": "https://www.astralcodexten.com"
        },
        "topics": ["Epistemologia", "Myślenie probabilistyczne", "Dekonstrukcja mitów", "Psychologia", "Przyszłość"],
        "desc": "Kultowy blog Scotta Alexandera (dawniej Slate Star Codex). Arcydzieło rygoru intelektualnego i uczciwości argumentacji.",
        "takeaway": "Dociekliwość laika weryfikującego twierdzenia ekspertów, myślenie Bayesowskie, badanie alternatywnych hipotez."
    },
    {
        "id": "slow_boring",
        "name": "Slow Boring (Matt Yglesias)",
        "category_group": "ENG_ESEJ",
        "region": "Zagranica",
        "scope": "USA / Polityka publiczna",
        "lang": "EN (do translacji)",
        "flag": "🇺🇸",
        "type": "Substack polityczno-gospodarczy",
        "url": "https://www.slowboring.com",
        "social": {
            "x": "https://x.com/mattyglesias",
            "substack": "https://www.slowboring.com"
        },
        "topics": ["Mieszkalnictwo (YIMBY)", "Polityka publiczna", "Instytucje", "Podatki", "Umiarkowanie"],
        "desc": "Trzeźwy, pragmatyczny i oparty na faktach namysł nad reformami państwa. Unika histerii i polaryzacyjnych wojen plemiennych.",
        "takeaway": "Model 'poważnego, umiarkowanego bloga politycznego', który szuka działających rozwiązań zamiast moralizowania."
    },
    {
        "id": "roots_of_progress",
        "name": "The Roots of Progress (Jason Crawford)",
        "category_group": "ENG_ESEJ",
        "region": "Zagranica",
        "scope": "Świat / Historia technologii",
        "lang": "EN (do translacji)",
        "flag": "🇺🇸",
        "type": "Substack & Instytut filozofii postępu",
        "url": "https://rootsofprogress.org",
        "social": {
            "x": "https://x.com/jasoncrawford",
            "substack": "https://rootsofprogress.org"
        },
        "topics": ["Filozofia postępu", "Historia inżynierii", "Czysta woda i higiena", "Energetyka jądrowa", "Przemysł"],
        "desc": "Analiza fundamentalnych przełomów w dziejach ludzkości podtrzymujących współczesny standard życia i zdrowia.",
        "takeaway": "Docenianie dorobku inżynierii i technologii z pozycji wdzięczności i głębokiego zrozumienia fundamentów materialnych."
    },
    {
        "id": "stratechery",
        "name": "Stratechery (Ben Thompson)",
        "category_group": "ENG_ESEJ",
        "region": "Zagranica",
        "scope": "Globalny / Big Tech",
        "lang": "EN (do translacji)",
        "flag": "🇺🇸",
        "type": "Monografia analityczna / Newsletter biznesowy",
        "url": "https://stratechery.com",
        "social": {
            "x": "https://x.com/benthompson",
            "linkedin": "https://www.linkedin.com/in/ben-thompson-stratechery/"
        },
        "topics": ["Teoria agregacji", "Monopole platformowe", "Strategia biznesowa", "Hardware vs Software"],
        "desc": "Najbardziej wpływowy jednoosobowy biuletyn analityczny o strategii technologicznej i ekonomii platform na świecie.",
        "takeaway": "Autorskie modele pojęciowe (Aggregation Theory) i chłodna analiza modeli biznesowych bez podniecania się PR-em."
    },
    {
        "id": "farnam_street",
        "name": "Farnam Street (Shane Parrish)",
        "category_group": "ENG_ESEJ",
        "region": "Zagranica",
        "scope": "Świat / Myślenie krytyczne",
        "lang": "EN (do translacji)",
        "flag": "🇨🇦",
        "type": "Katalog modeli mentalnych / Eseje",
        "url": "https://fs.blog",
        "social": {
            "x": "https://x.com/farnamstreet"
        },
        "topics": ["Modele mentalne", "Podejmowanie decyzji", "Brzytwa Ockhama", "Myślenie drugiego rzędu", "Mądrość"],
        "desc": "Słynny serwis poświęcony sztuce podejmowania trudnych decyzji i ponadczasowym modelom mentalnym (Charlie Munger).",
        "takeaway": "Wykorzystywanie pojęć 'myślenia drugiego rzędu' (second-order thinking) oraz inwersji problemu w polskich analizach."
    },
    {
        "id": "noahpinion",
        "name": "Noahpinion (Noah Smith)",
        "category_group": "ENG_ESEJ",
        "region": "Zagranica",
        "scope": "Świat / Makroekonomia",
        "lang": "EN (do translacji)",
        "flag": "🇺🇸",
        "type": "Substack ekonomiczny",
        "url": "https://www.noahpinion.blog",
        "social": {
            "x": "https://x.com/noahpinion",
            "substack": "https://www.noahpinion.blog"
        },
        "topics": ["Polityka przemysłowa", "Rywalizacja USA-Chiny", "Czipy i fabryki", "Płace", "Wykresy"],
        "desc": "Były felietonista Bloomberga obalający mity ekonomiczne za pomocą przejrzystych wykresów i surowych danych statystycznych.",
        "takeaway": "Wojna na twarde wykresy z danymi, re-industrializacja zachodu i powrót do budowy fabryk zamiast samej inżynierii finansowej."
    },
    {
        "id": "the_diff",
        "name": "The Diff (Byrne Hobart)",
        "category_group": "ENG_ESEJ",
        "region": "Zagranica",
        "scope": "Globalny / Rynki i Tech",
        "lang": "EN (do translacji)",
        "flag": "🇺🇸",
        "type": "Substack finansowo-analityczny",
        "url": "https://www.thediff.co",
        "social": {
            "x": "https://x.com/byrnehobart",
            "substack": "https://www.thediff.co"
        },
        "topics": ["Infleksje rynkowe", "Finanse korporacyjne", "Arbitraż regulacyjny", "Giełda"],
        "desc": "Dziennik śledzący głębokie przesunięcia kapitałowe, nieoczywiste zależności rynkowe i zmiany w modelach biznesowych.",
        "takeaway": "Zdolność do łączenia mikro-detali z wielkimi falami makroekonomicznymi i pokazywania, kto naprawdę zarabia."
    },

    # =============================================================
    # 4. POLITYKA MIĘDZYNARODOWA, GEOPOLITYKA I TECHNOLOGIA HARDWARE
    # =============================================================
    {
        "id": "foreign_affairs",
        "name": "Foreign Affairs",
        "category_group": "ENG_ESEJ",
        "region": "Zagranica",
        "scope": "Globalny",
        "lang": "EN (do translacji)",
        "flag": "🇺🇸",
        "type": "Kwartalnik stosunków międzynarodowych",
        "url": "https://www.foreignaffairs.com",
        "social": {
            "x": "https://x.com/ForeignAffairs"
        },
        "topics": ["Wielka strategia", "Rywalizacja mocarstw", "Przyszłość NATO", "Ład postliberalny"],
        "desc": "Najbardziej wpływowy magazyn politologiczny świata. Kształtuje debaty o równowadze sił i doktrynach obronnych.",
        "takeaway": "Makrostrukturalne spojrzenie na sojusze wojskowe i architekturę bezpieczeństwa w Europie Środkowej."
    },
    {
        "id": "politico_eu",
        "name": "Politico Europe",
        "category_group": "ENG_ESEJ",
        "region": "Europa",
        "scope": "Unia Europejska",
        "lang": "EN (do translacji)",
        "flag": "🇪🇺",
        "type": "Dziennikarstwo śledcze i unijne",
        "url": "https://www.politico.eu",
        "social": {
            "x": "https://x.com/PoliticoEurope"
        },
        "topics": ["Bruksela", "Komisja Europejska", "Regulacje handlowe", "Polityka klimatyczna", "Lobbying"],
        "desc": "Kulisy unijnych instytucji, targi między Berlinem, Paryżem i Warszawą oraz mechanizmy unijnego prawa.",
        "takeaway": "Kulisy gier gabinetowych w Brukseli i realny rozkład sił przy głosowaniach traktatowych."
    },
    {
        "id": "ars_technica",
        "name": "Ars Technica",
        "category_group": "TECH_PRZYSZLOSC",
        "region": "Zagranica",
        "scope": "Globalny",
        "lang": "EN (do translacji)",
        "flag": "🇺🇸",
        "type": "Publicystyka technologiczna",
        "url": "https://arstechnica.com",
        "social": {
            "x": "https://x.com/arstechnica"
        },
        "topics": ["Cyberbezpieczeństwo", "Hardware", "Polityka cyfrowa", "Kryptografia", "Prawa cyfrowe"],
        "desc": "Rzetelne dziennikarstwo technologiczne bez bezkrytycznego zachwytu nad nowościami. Twarda ocena kodu i sprzętu.",
        "takeaway": "Krytyczne spojrzenie na obietnice Doliny Krzemowej i ochrona praw użytkownika do własnego sprzętu."
    },
    {
        "id": "mit_tech_review",
        "name": "MIT Technology Review",
        "category_group": "TECH_PRZYSZLOSC",
        "region": "Zagranica",
        "scope": "Globalny",
        "lang": "EN (do translacji)",
        "flag": "🇺🇸",
        "type": "Magazyn naukowo-technologiczny",
        "url": "https://www.technologyreview.com",
        "social": {
            "x": "https://x.com/techreview"
        },
        "topics": ["Etyka technologii", "Przełomy laboratoryjne", "Klimatotech", "Biotechnologia"],
        "desc": "Krytyczny namysł nad wpływem inżynierii na społeczeństwo, rynek pracy i przyszłość człowieka.",
        "takeaway": "Oddzielanie realnych innowacji laboratoryjnych od giełdowego szumu i spekulacji."
    }
]

def get_source_by_id(source_id: str) -> dict:
    for src in EDITORIAL_SOURCES:
        if src["id"] == source_id:
            return src
    return None

def get_curated_social_bundles():
    """Zwraca gotowe zestawy do obserwowania na X i LinkedIn."""
    return {
        "x_lists": [
            {
                "name": "PL Esej & Debata",
                "desc": "Polskie środowisko eseju, myśli państwowej, liberalizmu, republikanizmu i debaty publicznej.",
                "handles": ["@KulturaLiberalna", "@KlubJagiellonski", "@NKonfederacja", "@Krytyka", "@MagazynKontakt", "@OficjalneZero", "@OSW_pl", "@BIPolska"],
                "url": "https://x.com/i/lists/create"
            },
            {
                "name": "ENG Esej & Progress",
                "desc": "Światowe wzorce głębokiego bloga, racjonalizmu, postępu cywilizacyjnego i analizy rynków.",
                "handles": ["@worksinprogress", "@slatestarcodex", "@mattyglesias", "@jasoncrawford", "@benthompson", "@farnamstreet", "@noahpinion", "@byrnehobart", "@FinancialTimes"],
                "url": "https://x.com/i/lists/create"
            }
        ],
        "linkedin_newsletters": [
            {
                "name": "Osiem tysięcy (8000)",
                "author": "Michał Gulczyński / Zespół 8000",
                "url": "https://www.linkedin.com/newsletters/osiem-tysi%C4%99cy-6962043685532585984/",
                "reason": "Najlepszy newsletter gospodarczy na polskim LinkedIn. Czyste dane, świetne wykresy, zero lania wody."
            },
            {
                "name": "Kultura Liberalna",
                "author": "Redakcja Kultury Liberalnej",
                "url": "https://www.linkedin.com/company/kultura-liberalna/",
                "reason": "Tygodniowy przegląd esejów o stanie demokracji, prawa i kultury europejskiej."
            },
            {
                "name": "Nowa Konfederacja",
                "author": "Bartłomiej Radziejewski i Zespół NK",
                "url": "https://www.linkedin.com/company/nowa-konfederacja/",
                "reason": "Realistyczna analiza polskiego bezpieczeństwa narodowego i przemysłu zbrojeniowego."
            },
            {
                "name": "Business Insider Polska",
                "author": "Redakcja BI",
                "url": "https://www.linkedin.com/company/business-insider-polska/",
                "reason": "Puls polskiego biznesu, kodeksu pracy i trendów konsumenckich."
            }
        ]
    }

def export_sources_to_csv(filepath: str):
    """Eksportuje pełną listę źródeł wraz z profilami X, LinkedIn, Substack i strategią 'co podkraść' do CSV."""
    fieldnames = [
        "Nazwa", "Region", "Kraj_Zasieg", "Typ_Medium", "X_Twitter", "LinkedIn", "Substack_WWW", "Tematyka", "Kluczowa_Wartosc_Dla_Laika", "Co_Zaadaptowac_Pod_Katem_Laika"
    ]
    with open(filepath, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for s in EDITORIAL_SOURCES:
            soc = s.get("social", {})
            writer.writerow({
                "Nazwa": f"{s['flag']} {s['name']}",
                "Region": s.get("region", "Polska"),
                "Kraj_Zasieg": s.get("scope", ""),
                "Typ_Medium": s.get("type", ""),
                "X_Twitter": soc.get("x", ""),
                "LinkedIn": soc.get("linkedin", ""),
                "Substack_WWW": soc.get("substack", s.get("url", "")),
                "Tematyka": " / ".join(s.get("topics", [])),
                "Kluczowa_Wartosc_Dla_Laika": s.get("desc", ""),
                "Co_Zaadaptowac_Pod_Katem_Laika": s.get("takeaway", "")
            })
    return filepath

if __name__ == "__main__":
    test_csv = os.path.join(os.path.dirname(__file__), "zrodla_inspiracji_laika.csv")
    export_sources_to_csv(test_csv)
    print(f"Wyeksportowano {len(EDITORIAL_SOURCES)} zródeł do: {test_csv}")

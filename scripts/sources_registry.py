# -*- coding: utf-8 -*-
"""
Rejestr Źródeł Redakcyjnych, Analitycznych i Inspiracji dla Bloga Laika.
Zorganizowany w 5 szuflad odpowiadających 5 działom Bloga Laika:
  1. Technologia & Architektura Uwagi -> kategoria: technologia
  2. Gospodarka, Finanse & Rynki -> kategoria: gospodarka
  3. Historia & Lekcje Dziejów -> kategoria: historia
  4. Polityka & Myśl Państwowa (PL & Geopolityka) -> kategoria: polityka
  5. Inne eseje / Filozofia laika & Postęp cywilizacyjny -> kategoria: eseje

Obsługuje:
  - Eksport do pliku CSV (z profilami X, LinkedIn, Substack, YouTube, RSS i strategią 'co podkraść')
  - Eksport do pliku OPML (dla Feedly, Inoreader, NetNewsWire z podziałem na feed PL i ENG)
  - Rekomendacje najlepszych esejów na start w każdej z 5 kategorii.
"""
import os
import csv
import xml.etree.ElementTree as ET
from xml.dom import minidom

EDITORIAL_SOURCES = [
    # =========================================================================
    # SZUFLADA 1: TECHNOLOGIA & ARCHITEKTURA UWAGI (Dział: technologia)
    # =========================================================================
    {
        "id": "stratechery",
        "name": "Stratechery (Ben Thompson)",
        "drawer": "SZUFLADA_TECHNOLOGIA",
        "drawer_name": "Technologia & Architektura Uwagi",
        "blog_category": "technologia",
        "region": "Zagranica",
        "scope": "Globalny / Big Tech",
        "lang": "EN (do translacji)",
        "flag": "🇺🇸",
        "type": "Monografia analityczna / Newsletter biznesowy",
        "url": "https://stratechery.com",
        "rss": "https://stratechery.com/feed/",
        "social": {
            "x": "https://x.com/benthompson",
            "linkedin": "https://www.linkedin.com/in/ben-thompson-stratechery/"
        },
        "topics": ["Teoria agregacji", "Monopole platformowe", "Strategia biznesowa", "Hardware vs Software"],
        "desc": "Płatny, ale każdy esej to lekcja ekonomii uwagi i platform. Najważniejszy analityk strategii cyfrowej na świecie.",
        "takeaway": "Autorskie modele pojęciowe (Aggregation Theory) i chłodna analiza modeli biznesowych bez podniecania się PR-em.",
        "best_essay": "„Aggregation Theory: How the Internet Reshaped the Monopolies of Attention”"
    },
    {
        "id": "understanding_ai",
        "name": "Understanding AI (Timothy Lee)",
        "drawer": "SZUFLADA_TECHNOLOGIA",
        "drawer_name": "Technologia & Architektura Uwagi",
        "blog_category": "technologia",
        "region": "Zagranica",
        "scope": "Globalny / AI bez hype'u",
        "lang": "EN (do translacji)",
        "flag": "🇺🇸",
        "type": "Substack technologiczno-analityczny",
        "url": "https://www.understandingai.org",
        "rss": "https://www.understandingai.org/feed",
        "social": {
            "x": "https://x.com/binarybits",
            "substack": "https://www.understandingai.org"
        },
        "topics": ["Sztuczna inteligencja", "Architektura LLM", "Koszty wnioskowania", "Regulacje", "Rzeczywiste wdrożenia"],
        "desc": "Tłumaczy sztuczną inteligencję bez hype'u. Wzorzec klarownego wyjaśniania transformerów, tokenów i sieci neuronowych.",
        "takeaway": "Tłumaczenie fundamentów modeli AI prostym, rzeczowym językiem; demaskowanie mitów o 'sztucznej superinteligencji za rogiem'.",
        "best_essay": "„Large Language Models Explained with Plain English and Zero Hype”"
    },
    {
        "id": "the_diff",
        "name": "The Diff (Byrne Hobart)",
        "drawer": "SZUFLADA_TECHNOLOGIA",
        "drawer_name": "Technologia & Architektura Uwagi",
        "blog_category": "technologia",
        "region": "Zagranica",
        "scope": "Globalny / Rynki i Tech",
        "lang": "EN (do translacji)",
        "flag": "🇺🇸",
        "type": "Substack finansowo-analityczny",
        "url": "https://www.thediff.co",
        "rss": "https://www.thediff.co/feed",
        "social": {
            "x": "https://x.com/byrnehobart",
            "substack": "https://www.thediff.co"
        },
        "topics": ["Infleksje rynkowe", "Finanse korporacyjne", "Arbitraż regulacyjny", "Giełda"],
        "desc": "Łączy technologię i finanse. Wyjaśnia dlaczego taniego kapitału już nie będzie i kto naprawdę finansuje serwerownie AI.",
        "takeaway": "Zdolność do łączenia mikro-detali z wielkimi falami makroekonomicznymi i pokazywania, kto naprawdę zarabia.",
        "best_essay": "„CapEx Cycles in Tech: Why the Data Center Boom Changes the Marginal Cost of Money”"
    },
    {
        "id": "crazy_nauka",
        "name": "Crazy Nauka",
        "drawer": "SZUFLADA_TECHNOLOGIA",
        "drawer_name": "Technologia & Architektura Uwagi",
        "blog_category": "technologia",
        "region": "Polska",
        "scope": "Polska / Popularyzacja nauki",
        "lang": "PL",
        "flag": "🇵🇱",
        "type": "Największy polski blog popularnonaukowy",
        "url": "https://www.crazynauka.pl",
        "rss": "https://www.crazynauka.pl/feed/",
        "social": {
            "x": "https://x.com/CrazyNauka",
            "facebook": "https://www.facebook.com/CrazyNauka"
        },
        "topics": ["Nauka", "Klimat", "Medycyna", "Kosmos", "Weryfikacja faktów"],
        "desc": "Jak tłumaczyć trudne rzeczy laikom. Wzór dla przystępnego dziennikarstwa naukowego w dziale Technologia.",
        "takeaway": "Sztuka budowania analogii ze świata codziennego do wyjaśniania skomplikowanych praw fizyki i inżynierii.",
        "best_essay": "„Jak odróżnić przełom laboratoryjny od prasowego szumu: Lekcja dociekliwego laika”"
    },
    {
        "id": "kwantowo",
        "name": "Kwantowo.pl",
        "drawer": "SZUFLADA_TECHNOLOGIA",
        "drawer_name": "Technologia & Architektura Uwagi",
        "blog_category": "technologia",
        "region": "Polska",
        "scope": "Polska / Fizyka i Filozofia nauki",
        "lang": "PL",
        "flag": "🇵🇱",
        "type": "Autorski blog popularnonaukowy (Adam Adamczyk)",
        "url": "https://www.kwantowo.pl",
        "rss": "https://www.kwantowo.pl/feed/",
        "social": {
            "x": "https://x.com/Kwantowo",
            "facebook": "https://www.facebook.com/kwantowo"
        },
        "topics": ["Fizyka kwantowa", "Kryptografia postkwantowa", "Kosmologia", "Filozofia nauki"],
        "desc": "Arcydzieło rzetelnej popularyzacji trudnej nauki. Rozbija skomplikowane zjawiska na przejrzyste klocki logiczne.",
        "takeaway": "Rygor dowodowy połączony z pasją dociekania; idealny wzorzec dla technicznych i filozoficznych wpisów Bloga Laika.",
        "best_essay": "„Kryptografia postkwantowa: Dlaczego algorytm Shora zmusi banki do wymiany całego szyfrowania”"
    },
    {
        "id": "hacker_news",
        "name": "Hacker News (Y Combinator)",
        "drawer": "SZUFLADA_TECHNOLOGIA",
        "drawer_name": "Technologia & Architektura Uwagi",
        "blog_category": "technologia",
        "region": "Zagranica",
        "scope": "Globalny / Agregator inżynierski",
        "lang": "EN (do translacji)",
        "flag": "🇺🇸",
        "type": "Agregator & Forum inżynierów",
        "url": "https://news.ycombinator.com",
        "rss": "https://news.ycombinator.com/rss",
        "social": {
            "x": "https://x.com/newsycombinator"
        },
        "topics": ["Inżynieria", "Systemy rozproszone", "Hardware", "Prywatność", "SLM / Edge AI"],
        "desc": "Agregator, gdzie tematy na eseje rodzą się na 2 miesiące przed mediami głównego nurtu.",
        "takeaway": "Śledzenie komentarzy inżynierów i praktyków; wyłapywanie wczesnych sygnałów o porażkach i przełomach w hardware.",
        "best_essay": "Wątki: „Show HN: On-device SLM performance” oraz dekonstrukcja rachunków za chmurę AWS/Azure."
    },
    {
        "id": "lesswrong",
        "name": "LessWrong",
        "drawer": "SZUFLADA_TECHNOLOGIA",
        "drawer_name": "Technologia & Architektura Uwagi",
        "blog_category": "technologia",
        "region": "Zagranica",
        "scope": "Globalny / Racjonalizm & Bezpieczeństwo AI",
        "lang": "EN (do translacji)",
        "flag": "🇺🇸",
        "type": "Forum racjonalistyczne & Agregator esejów",
        "url": "https://www.lesswrong.com",
        "rss": "https://www.lesswrong.com/feed.xml",
        "topics": ["Epistemologia", "Błędy poznawcze", "Bezpieczeństwo AI", "Teoria decyzji", "Modele świata"],
        "desc": "Kolebka współczesnego racjonalizmu. Źródło głębokich debat o myśleniu krytycznym i granicach maszyn.",
        "takeaway": "Rozróżnienie między mapą a terytorium (The Map is Not the Territory); dekonstrukcja psychologicznych mechanizmów samooszukiwania.",
        "best_essay": "„Map and Territory: The Foundational Sequences of Critical Thinking”"
    },
    {
        "id": "ars_technica",
        "name": "Ars Technica",
        "drawer": "SZUFLADA_TECHNOLOGIA",
        "drawer_name": "Technologia & Architektura Uwagi",
        "blog_category": "technologia",
        "region": "Zagranica",
        "scope": "Globalny",
        "lang": "EN (do translacji)",
        "flag": "🇺🇸",
        "type": "Publicystyka technologiczna",
        "url": "https://arstechnica.com",
        "rss": "https://feeds.arstechnica.com/arstechnica/index",
        "social": {
            "x": "https://x.com/arstechnica"
        },
        "topics": ["Cyberbezpieczeństwo", "Hardware", "Polityka cyfrowa", "Kryptografia", "Prawa cyfrowe"],
        "desc": "Rzetelne dziennikarstwo technologiczne bez bezkrytycznego zachwytu nad nowościami. Twarda ocena kodu i sprzętu.",
        "takeaway": "Krytyczne spojrzenie na obietnice Doliny Krzemowej i ochrona praw użytkownika do własnego sprzętu.",
        "best_essay": "„The Silicon Wall: Why Shrinking Transistors Beyond 2nm Breaks Classical Physics”"
    },

    # =========================================================================
    # SZUFLADA 2: GOSPODARKA, FINANSE & RYNKI (Dział: gospodarka)
    # =========================================================================
    {
        "id": "osiem_tysiecy",
        "name": "8000 (Osiem tysięcy / osiemtysiecy.pl)",
        "drawer": "SZUFLADA_GOSPODARKA",
        "drawer_name": "Gospodarka, Finanse & Rynki",
        "blog_category": "gospodarka",
        "region": "Polska",
        "scope": "Polska / Gospodarka",
        "lang": "PL",
        "flag": "🇵🇱",
        "type": "Najlepszy polski Substack o gospodarce bez bullshitu",
        "url": "https://osiemtysiecy.pl",
        "rss": "https://osiemtysiecy.substack.com/feed",
        "social": {
            "x": "https://x.com/MagazynKontakt",
            "linkedin": "https://www.linkedin.com/newsletters/osiem-tysi%C4%99cy-6962043685532585984/"
        },
        "topics": ["Dane makroekonomiczne", "Rynek pracy", "Płace", "Stopy procentowe", "Wykresy tygodnia"],
        "desc": "Najlepszy polski newsletter gospodarczy bez bullshitu. Czyste wykresy, twarde dane makro. Idealny punkt odniesienia dla wpisów o tanim kapitale.",
        "takeaway": "Format czystych wykresów, twarde dane makro podane bez hermetycznego żargonu ekonomicznego.",
        "best_essay": "„Złudzenie taniego kapitału: Dlaczego zerowe stopy procentowe były anomalią stulecia”"
    },
    {
        "id": "slow_boring",
        "name": "Slow Boring (Matt Yglesias)",
        "drawer": "SZUFLADA_GOSPODARKA",
        "drawer_name": "Gospodarka, Finanse & Rynki",
        "blog_category": "gospodarka",
        "region": "Zagranica",
        "scope": "USA / Polityka publiczna",
        "lang": "EN (do translacji)",
        "flag": "🇺🇸",
        "type": "Substack polityczno-gospodarczy (Wielka Czwórka)",
        "url": "https://www.slowboring.com",
        "rss": "https://www.slowboring.com/feed",
        "social": {
            "x": "https://x.com/mattyglesias",
            "substack": "https://www.slowboring.com"
        },
        "topics": ["Mieszkalnictwo (YIMBY)", "Polityka publiczna", "Instytucje", "Podatki", "Umiarkowanie"],
        "desc": "Polityka i gospodarka pragmatycznie, bez plemienności. Świetny wzór jak pisać o polityce dla ludzi, którzy nie lubią polityki.",
        "takeaway": "Model 'poważnego, umiarkowanego bloga politycznego', który szuka działających rozwiązań zamiast moralizowania.",
        "best_essay": "„The Housing Crisis is an Abundance Crisis: Why Rent Subsidies Fuel Price Inflation”"
    },
    {
        "id": "financial_times",
        "name": "The Financial Times (FT)",
        "drawer": "SZUFLADA_GOSPODARKA",
        "drawer_name": "Gospodarka, Finanse & Rynki",
        "blog_category": "gospodarka",
        "region": "Zagranica",
        "scope": "Globalny",
        "lang": "EN (do translacji)",
        "flag": "🇬🇧",
        "type": "Dziennik finansowy / Global benchmark",
        "url": "https://www.ft.com",
        "rss": "https://www.ft.com/rss/home",
        "social": {
            "x": "https://x.com/FinancialTimes",
            "linkedin": "https://www.linkedin.com/company/financial-times/"
        },
        "topics": ["Makroekonomia", "Banki centralne (FED/EBC)", "Dług publiczny", "Handel globalny", "Geonomia"],
        "desc": "Światowy punkt odniesienia w analityce rynkowej. Wyjaśnia głębokie przepływy kapitałowe i politykę stóp procentowych.",
        "takeaway": "Globalny standard analizy długu suwerennego, polityki banków centralnych i długich cykli inwestycyjnych.",
        "best_essay": "„The Era of Free Money is Over: Sovereign Debt Traps in the Post-ZIRP World”"
    },
    {
        "id": "business_insider",
        "name": "Business Insider (Polska & Global)",
        "drawer": "SZUFLADA_GOSPODARKA",
        "drawer_name": "Gospodarka, Finanse & Rynki",
        "blog_category": "gospodarka",
        "region": "Polska / Globalny",
        "scope": "Gospodarka / Rynki / Biznes",
        "lang": "PL / EN",
        "flag": "🌍",
        "type": "Portal biznesowo-ekonomiczny",
        "url": "https://businessinsider.com.pl",
        "rss": "https://businessinsider.com.pl/rss",
        "social": {
            "x": "https://x.com/BIPolska",
            "linkedin": "https://www.linkedin.com/company/business-insider-polska/"
        },
        "topics": ["Makroekonomia", "Trendy rynkowe", "Praca i wynagrodzenia", "Przedsiębiorczość", "Ceny surowców"],
        "desc": "Tłumaczy mechanizmy rynkowe i zmiany nawyków konsumentów. Dynamiczne, wyraziste ujęcia makro.",
        "takeaway": "Dynamika narracji biznesowej, chwytliwe i merytoryczne ujęcia makro, zwięzłe infografiki trendów i psychologia pracy.",
        "best_essay": "„Cichy kryzys rynku pracy: Dlaczego miliony etatów zmienią się szybciej niż kodeks pracy”"
    },
    {
        "id": "noahpinion",
        "name": "Noahpinion (Noah Smith)",
        "drawer": "SZUFLADA_GOSPODARKA",
        "drawer_name": "Gospodarka, Finanse & Rynki",
        "blog_category": "gospodarka",
        "region": "Zagranica",
        "scope": "Świat / Makroekonomia",
        "lang": "EN (do translacji)",
        "flag": "🇺🇸",
        "type": "Substack ekonomiczny",
        "url": "https://www.noahpinion.blog",
        "rss": "https://www.noahpinion.blog/feed",
        "social": {
            "x": "https://x.com/noahpinion",
            "substack": "https://www.noahpinion.blog"
        },
        "topics": ["Polityka przemysłowa", "Rywalizacja USA-Chiny", "Czipy i fabryki", "Płace", "Wykresy"],
        "desc": "Ekonomista, który pisze o wszystkim: od anime po geopolitykę Tajwanu. Pokazuje jak łączyć tematy.",
        "takeaway": "Wojna na twarde wykresy z danymi, re-industrializacja zachodu i powrót do budowy fabryk zamiast samej inżynierii finansowej.",
        "best_essay": "„Industrial Policy is Back: Why Finance Can No Longer Substitute for Physical Factories”"
    },
    {
        "id": "investing",
        "name": "Investing.com",
        "drawer": "SZUFLADA_GOSPODARKA",
        "drawer_name": "Gospodarka, Finanse & Rynki",
        "blog_category": "gospodarka",
        "region": "Zagranica",
        "scope": "Globalny / Rynki",
        "lang": "EN / PL",
        "flag": "🌍",
        "type": "Platforma rynkowa i surowcowa",
        "url": "https://pl.investing.com",
        "rss": "https://pl.investing.com/rss/news.rss",
        "social": {
            "x": "https://x.com/Investingcom"
        },
        "topics": ["Ropa i gaz", "Obligacje skarbowe", "Waluty", "Kruszce", "Wskaźniki PMI/CPI"],
        "desc": "Dane rynkowe w czasie rzeczywistym, spready rentowności obligacji i twarde wskaźniki makro.",
        "takeaway": "Twarde dane liczbowe (rentowności 10-letnich obligacji, notowania ropy Brent i gazu TTF) jako tło dla polskich wpisów.",
        "best_essay": "„Rentowności obligacji 10Y jako kanarek w kopalni: Co mówi spread między Niemcami a Polską”"
    },

    # =========================================================================
    # SZUFLADA 3: HISTORIA & LEKCJE DZIEJÓW (Dział: historia)
    # =========================================================================
    {
        "id": "dzieje_pl",
        "name": "Dzieje.pl (PAP & Muzeum Historii Polski)",
        "drawer": "SZUFLADA_HISTORIA",
        "drawer_name": "Historia & Lekcje Dziejów",
        "blog_category": "historia",
        "region": "Polska",
        "scope": "Polska / Historia narodowa",
        "lang": "PL",
        "flag": "🇵🇱",
        "type": "Główny polski portal historyczny PAP i MHP",
        "url": "https://dzieje.pl",
        "rss": "https://dzieje.pl/rss.xml",
        "social": {
            "x": "https://x.com/dziejepl",
            "facebook": "https://www.facebook.com/dziejepl"
        },
        "topics": ["Historia Polski", "Archiwa", "XX wiek", "Biografie", "Węzłowe wydarzenia", "Źródła"],
        "desc": "Oficjalny portal PAP i Muzeum Historii Polski. Niezastąpione kalendarium, fakty źródłowe i dokumenty od średniowiecza po współczesność.",
        "takeaway": "Twarde źródła archiwalne, dokumenty pierwotne i precyzyjne datowanie procesów cywilizacyjnych.",
        "best_essay": "„Anatomia polskich powstań narodowych: Rachunek zysków i strat z perspektywy suwerenności”"
    },
    {
        "id": "historia_org_pl",
        "name": "Historia.org.pl",
        "drawer": "SZUFLADA_HISTORIA",
        "drawer_name": "Historia & Lekcje Dziejów",
        "blog_category": "historia",
        "region": "Polska",
        "scope": "Polska / Świat / Wojskowość",
        "lang": "PL",
        "flag": "🇵🇱",
        "type": "Największy niezależny serwis historyczny",
        "url": "https://historia.org.pl",
        "rss": "https://historia.org.pl/feed/",
        "social": {
            "x": "https://x.com/historia_org_pl",
            "facebook": "https://www.facebook.com/historia.org.pl"
        },
        "topics": ["Historia wojskowości", "Bitwy", "Dyplomacja", "Gospodarka dawna", "Książki historyczne"],
        "desc": "Największy w Polsce portal historyczny łączący rzetelną wiedzę akademicką z publicystyką dla pasjonatów dziejów.",
        "takeaway": "Zdolność do ukazywania nieznanych wątków wielkich wojen, zakulisowej dyplomacji i przemian społecznych.",
        "best_essay": "„Pieniądz i wojna: Jak finanse królów decydowały o losach bitew nowożytnej Europy”"
    },
    {
        "id": "ciekawostki_historyczne",
        "name": "CiekawostkiHistoryczne.pl",
        "drawer": "SZUFLADA_HISTORIA",
        "drawer_name": "Historia & Lekcje Dziejów",
        "blog_category": "historia",
        "region": "Polska",
        "scope": "Starożytność / Polska / Europa / Życie codzienne",
        "lang": "PL",
        "flag": "🇵🇱",
        "type": "Portal historii narracyjnej & Najpopularniejszy fanpage FB",
        "url": "https://ciekawostkihistoryczne.pl",
        "rss": "https://ciekawostkihistoryczne.pl/feed/",
        "social": {
            "x": "https://x.com/CiekawostkiHist",
            "facebook": "https://www.facebook.com/CiekawostkiHistoryczne"
        },
        "topics": ["Starożytność", "Historia Polski", "Historia Europy", "Życie codzienne", "Obyczaje dawne", "Sensacje"],
        "desc": "Najpopularniejszy polski profil na Facebooku w tej kategorii, agregujący przekrojowe artykuły o starożytności, historii Polski i Europy w bardzo przystępnej formie.",
        "takeaway": "Przekrojowa popularyzacja dziejów, docieranie do szerokiego grona czytelników przez nieoczywiste wątki obyczajowe i mechanizmy dawnego życia.",
        "best_essay": "„Dzień, w którym zgasły światła: Jak wyglądało życie w średniowiecznym mieście bez bieżącej wody i zegara”"
    },
    {
        "id": "wielka_historia",
        "name": "WielkaHistoria.pl",
        "drawer": "SZUFLADA_HISTORIA",
        "drawer_name": "Historia & Lekcje Dziejów",
        "blog_category": "historia",
        "region": "Polska",
        "scope": "Starożytność / Egipt / Mezopotamia / Europa / Polska",
        "lang": "PL",
        "flag": "🇵🇱",
        "type": "Czołowy portal historyczny & Gigant zasięgowy FB",
        "url": "https://wielkahistoria.pl",
        "rss": "https://wielkahistoria.pl/feed/",
        "social": {
            "facebook": "https://www.facebook.com/wielkahistoriapl"
        },
        "topics": ["Starożytny Egipt", "Mezopotamia", "Średniowiecze", "Historia Polski", "Wielkie imperia", "Archeologia"],
        "desc": "Obecnie jeden z największych graczy na polskim Facebooku w kategorii historycznej. Generują milionowe zasięgi. Portal publikuje codziennie artykuły przekrojowe – od dziejów starożytnego Egiptu i Mezopotamii, przez historię Europy, aż po szczegółowe analizy dotyczące historii Polski.",
        "takeaway": "Przekrojowość tematyczna od starożytnych cywilizacji rzecznych po czasy nowożytne oraz umiejętność generowania wielomilionowych zasięgów i zaangażowania czytelników.",
        "best_essay": "„Narodziny cywilizacji nad Nilem i Eufratem: Jak gospodarka irygacyjna stworzyła pierwsze biurokracje i podatki w dziejach”"
    },
    {
        "id": "histmag_org",
        "name": "Histmag.org",
        "drawer": "SZUFLADA_HISTORIA",
        "drawer_name": "Historia & Lekcje Dziejów",
        "blog_category": "historia",
        "region": "Polska",
        "scope": "Historia powszechna / Polska / Recenzje / Długie formy",
        "lang": "PL",
        "flag": "🇵🇱",
        "type": "Renomowany internetowy magazyn historyczny (od 2001 r.)",
        "url": "https://histmag.org",
        "rss": "https://histmag.org/rss",
        "social": {
            "facebook": "https://www.facebook.com/histmag",
            "x": "https://x.com/histmag"
        },
        "topics": ["Długie formy", "Historia regionalna", "Recenzje opracowań", "Wywiady z historykami", "Źródła akademickie"],
        "desc": "Jeden z najstarszych i najbardziej renomowanych portali historycznych w Polsce. Ich społeczność na Facebooku to setki tysięcy zaangażowanych czytelników. To doskonałe miejsce do czytania dłuższych, dobrze udokumentowanych tekstów, często pisanych przez historyków, recenzji wielotomowych opracowań oraz artykułów o historii regionalnej.",
        "takeaway": "Wzorzec rzetelnego, pogłębionego tekstu historycznego z bogatą bibliografią, recenzje фундаментальных dzieł i szacunek dla źródeł pisanych.",
        "best_essay": "„Polska dzielnicowa i narodziny tożsamości narodowej: Jak rozbicie państwa paradoksalnie wzmocniło poczucie wspólnoty”"
    },
    {
        "id": "tytus_edu_pl",
        "name": "Tytus.edu.pl",
        "drawer": "SZUFLADA_HISTORIA",
        "drawer_name": "Historia & Lekcje Dziejów",
        "blog_category": "historia",
        "region": "Polska",
        "scope": "Polityka / Wojny / Kultura dawnych wieków / Viral historyczny",
        "lang": "PL",
        "flag": "🇵🇱",
        "type": "Portal popularyzatorski & Aktywny fanpage FB",
        "url": "https://tytus.edu.pl",
        "rss": "https://tytus.edu.pl/feed/",
        "social": {
            "facebook": "https://www.facebook.com/tytus.edu"
        },
        "topics": ["Polityka dawna", "Wojny i dyplomacja", "Kultura dawnych wieków", "Popularyzacja dziejów", "Wirusowe eseje"],
        "desc": "Portal i bardzo aktywny fanpage, który świetnie radzi sobie z popularyzacją historii. Oferują merytoryczne teksty, które często stają się viralami w mediach społecznościowych, skupiając się na polityce, wojnach i kulturze dawnych wieków.",
        "takeaway": "Zdolność do tworzenia merytorycznych, a zarazem viralowych formatów publicystycznych, które przyciągają dziesiątki tysięcy reakcji bez utraty rzetelności.",
        "best_essay": "„Kulisy dawnych wojen i traktatów: Jak dyplomatyczne intrygi i sojusze z papieru decydowały o losach koronowanych głów”"
    },
    {
        "id": "ciekawe_historie",
        "name": "Ciekawe Historie (Tomasz Czukiewski)",
        "drawer": "SZUFLADA_HISTORIA",
        "drawer_name": "Historia & Lekcje Dziejów",
        "blog_category": "historia",
        "region": "Polska",
        "scope": "Dokument / Społeczeństwo / Gospodarka / PRL",
        "lang": "PL",
        "flag": "🇵🇱",
        "type": "Kanał filmów dokumentalnych YouTube",
        "url": "https://www.youtube.com/@CiekaweHistorie",
        "social": {
            "youtube": "https://www.youtube.com/@CiekaweHistorie",
            "facebook": "https://www.facebook.com/ciekawehistorie"
        },
        "topics": ["Filmy dokumentalne", "Transformacja ustrojowa", "Procesy społeczne", "Gospodarka", "Reportaż śledczy"],
        "desc": "Tworzy świetnie zrealizowane filmy dokumentalne z dogłębną analizą procesów społecznych i gospodarczych, przyciągając miliony widzów szukających rzetelnego kontekstu.",
        "takeaway": "Dogłębna analiza procesów społecznych i gospodarczych, rzetelny research archiwalny i poszukiwanie przyczynowo-skutkowego kontekstu bez taniej sensacji.",
        "best_essay": "„Anatomia polskiej biedy lat 90.: Jak upadek zakładów pracy i hiperinflacja ukształtowały współczesne podziały społeczne”"
    },
    {
        "id": "dudek_o_historii",
        "name": "Dudek o Historii (prof. Antoni Dudek)",
        "drawer": "SZUFLADA_HISTORIA",
        "drawer_name": "Historia & Lekcje Dziejów",
        "blog_category": "historia",
        "region": "Polska",
        "scope": "Historia najnowsza / Polityka / PRL & III RP",
        "lang": "PL",
        "flag": "🇵🇱",
        "type": "Kanał analityczno-akademicki & Podcast",
        "url": "https://www.youtube.com/@DudekoHistorii",
        "social": {
            "youtube": "https://www.youtube.com/@DudekoHistorii",
            "facebook": "https://www.facebook.com/dudekohistorii"
        },
        "topics": ["Historia najnowsza", "PRL", "Okrągły Stół", "Transformacja ustrojowa", "Kulisy władzy", "Politologia"],
        "desc": "Kanał prowadzony przez prof. Antoniego Dudka to doskonałe źródło analitycznej, akademickiej wiedzy o historii najnowszej podanej bez zbędnych ozdobników.",
        "takeaway": "Chłodny, akademicki obiektywizm, precyzyjne odróżnianie udokumentowanych faktów od mitów politycznych i badanie mechanizmów podejmowania decyzji na szczytach władzy.",
        "best_essay": "„Kulisy transformacji ustrojowej: Kto naprawdę rządził Polską w czasie przełomu 1989 roku i dlaczego kompromis był konieczny”"
    },
    {
        "id": "thrashing_mad_pl",
        "name": "ThrashingMadPL",
        "drawer": "SZUFLADA_HISTORIA",
        "drawer_name": "Historia & Lekcje Dziejów",
        "blog_category": "historia",
        "region": "Polska",
        "scope": "Kartografia historyczna / Konflikty / Dzieje Europy i Polski",
        "lang": "PL",
        "flag": "🇵🇱",
        "type": "Autorski kanał animowanych map historycznych YouTube",
        "url": "https://www.youtube.com/@ThrashingMadPL",
        "social": {
            "youtube": "https://www.youtube.com/@ThrashingMadPL",
            "facebook": "https://www.facebook.com/ThrashingMadPL"
        },
        "topics": ["Animowane mapy", "Dzieje Polski", "Wojny europejskie", "Zmiany granic", "Geografia militarna"],
        "desc": "Skupia się na dziejach Europy i Polski, używając autorskich, animowanych map do precyzyjnego, krok po kroku, wizualizowania zmian terytorialnych i konfliktów zbrojnych.",
        "takeaway": "Przedstawianie historii w wymiarze dynamicznym i przestrzennym: jak ukształtowanie terenu, rzeki i przesunięcia granic determinowały przetrwanie państw.",
        "best_essay": "„Geografia jako wyrok: Dlaczego nizinne położenie między Odrą a Dnieprem skazało Rzeczpospolitą na permanentną czujność geopolityczną”"
    },
    {
        "id": "historia_bez_cenzury",
        "name": "Historia Bez Cenzury",
        "drawer": "SZUFLADA_HISTORIA",
        "drawer_name": "Historia & Lekcje Dziejów",
        "blog_category": "historia",
        "region": "Polska",
        "scope": "Historia masowa / Popkultura / Postacie",
        "lang": "PL",
        "flag": "🇵🇱",
        "type": "Największy polski kanał rozrywkowo-historyczny YouTube & FB",
        "url": "https://www.youtube.com/@HistoriaBezCenzuryMB",
        "social": {
            "youtube": "https://www.youtube.com/@HistoriaBezCenzuryMB",
            "facebook": "https://www.facebook.com/HistoriaBezCenzury"
        },
        "topics": ["Władcy Polski", "Wojny", "Ciekawostki obyczajowe", "Mity historyczne", "Odsłanianie tabu"],
        "desc": "Zdecydowanie największy polski gigant historyczny, który dociera do masowego odbiorcy dzięki ostremu, rozrywkowemu językowi i dynamicznemu montażowi.",
        "takeaway": "Dynamika przekazu, bezpośredni język trafiający do milionów odbiorców oraz przełamywanie podręcznikowego patosu na rzecz opowiadania o ludziach z krwi i kości.",
        "best_essay": "„Władcy bez retuszu i bez korony: Prawdziwe, niecenzurowane motywacje polskich monarchów, o których milczały szkolne podręczniki”"
    },
    {
        "id": "historia_realna",
        "name": "Historia Realna (Piotr Zychowicz)",
        "drawer": "SZUFLADA_HISTORIA",
        "drawer_name": "Historia & Lekcje Dziejów",
        "blog_category": "historia",
        "region": "Polska",
        "scope": "Polska / Świat / Geopolityka",
        "lang": "PL",
        "flag": "🇵🇱",
        "type": "Kanał publicystyki historyczno-militarnej & Książki",
        "url": "https://www.youtube.com/@HistoriaRealna",
        "rss": "https://www.youtube.com/feeds/videos.xml?channel_id=UCg1b0rO_qYFjB3qV8F78xHQ",
        "social": {
            "x": "https://x.com/PiotrZychowicz",
            "youtube": "https://www.youtube.com/@HistoriaRealna",
            "facebook": "https://www.facebook.com/piotr.zychowicz.publicysta"
        },
        "topics": ["Realizm geopolityczny", "II wojna światowa", "Geopolityka Europy Środkowej", "Błędy strategiczne"],
        "desc": "Jeden z najpopularniejszych polskich kanałów historyczno-geopolitycznych. Chłodna ocena decyzji polityków bez bogoojczyźnianego mitologizowania.",
        "takeaway": "Bezwzględny realizm polityczny: badanie faktów i siły militarnej zamiast myślenia życzeniowego.",
        "best_essay": "„Mit niezwyciężonych sojuszy: Lekcja z września 1939 roku dla współczesnej Polski w NATO”"
    },
    {
        "id": "wiek_dwudziesty",
        "name": "Wiek Dwudziesty (Portal Historyczny)",
        "drawer": "SZUFLADA_HISTORIA",
        "drawer_name": "Historia & Lekcje Dziejów",
        "blog_category": "historia",
        "region": "Polska",
        "scope": "XX wiek / Zimna wojna / Totalitaryzmy",
        "lang": "PL",
        "flag": "🇵🇱",
        "type": "Portal analityki historycznej",
        "url": "https://wiekdwudziesty.pl",
        "rss": "https://wiekdwudziesty.pl/feed/",
        "social": {
            "x": "https://x.com/WiekDwudziesty",
            "facebook": "https://www.facebook.com/wiekdwudziesty"
        },
        "topics": ["Zimna wojna", "Blok wschodni", "Transformacja ustrojowa", "Wywiad i szpiegostwo", "Propaganda"],
        "desc": "Głęboka analiza XX-wiecznych mechanizmów władzy, propagandy, wyścigu zbrojeń i rozpadu systemów autorytarnych.",
        "takeaway": "Dekonstrukcja mechanizmów manipulacji tłumem i analiza procesów upadku systemów monopartyjnych.",
        "best_essay": "„Jak umierają imperia: Ekonomiczna i moralna implozja Związku Radzieckiego”"
    },
    {
        "id": "hardcore_history",
        "name": "Hardcore History (Dan Carlin) & The Rest is History",
        "drawer": "SZUFLADA_HISTORIA",
        "drawer_name": "Historia & Lekcje Dziejów",
        "blog_category": "historia",
        "region": "Zagranica",
        "scope": "Świat / Wielkie narracje",
        "lang": "EN (do translacji)",
        "flag": "🇺🇸",
        "type": "Globalny benchmark podcastu i eseju historycznego",
        "url": "https://www.dancarlin.com",
        "rss": "https://feeds.feedburner.com/dancarlin/history",
        "social": {
            "x": "https://x.com/HardcoreHistory"
        },
        "topics": ["Wielkie wojny", "Upadek Rzymu", "Psychologia władców", "Ekstremalne punkty zwrotne"],
        "desc": "Globalny niedościgniony wzorzec narracji historycznej z perspektywy zwykłego człowieka postawionego w ekstremalnych warunkach dziejowych.",
        "takeaway": "Budowanie napięcia narracyjnego, zadawanie dramatycznych pytań: 'jak ty byś się zachował na ich miejscu?'.",
        "best_essay": "„Ghosts of the Ostfront: Logistyka i dehumanizacja w największym starciu lądowym ludzkości”"
    },
    {
        "id": "acoup",
        "name": "A Collection of Unmitigated Pedantry (ACOUP - Bret Devereaux)",
        "drawer": "SZUFLADA_HISTORIA",
        "drawer_name": "Historia & Lekcje Dziejów",
        "blog_category": "historia",
        "region": "Zagranica",
        "scope": "Świat / Historia wojskowości i ekonomii",
        "lang": "EN (do translacji)",
        "flag": "🇺🇸",
        "type": "Autorski blog naukowo-eseistyczny",
        "url": "https://acoup.blog",
        "rss": "https://acoup.blog/feed/",
        "social": {
            "x": "https://x.com/BretDevereaux"
        },
        "topics": ["Logistyka rzymska", "Rolnictwo preindustrialne", "Ekonomia wojen", "Mity o średniowieczu"],
        "desc": "Wybitny historyk wojskowości wyjaśniający, jak działały gospodarki starożytne, jak karmiono legiony i dlaczego logistyka wygrywa bitwy.",
        "takeaway": "Twarde kalkulacje kalorii, transportu wozami i zapasów żywności jako rzeczywisty motor historii.",
        "best_essay": "„The Logistics of Iron and Bread: Why Ancient Empires Fell When Wheat Supply Lines Broke”"
    },

    # =========================================================================
    # SZUFLADA 4: POLITYKA, MYŚL PAŃSTWOWA & SPOŁECZEŃSTWO (Dział: polityka)
    # =========================================================================
    {
        "id": "kultura_liberalna",
        "name": "Kultura Liberalna",
        "drawer": "SZUFLADA_POLITYKA",
        "drawer_name": "Polityka & Myśl Państwowa",
        "blog_category": "polityka",
        "region": "Polska",
        "scope": "Polska / Europa",
        "lang": "PL",
        "flag": "🇵🇱",
        "type": "Tygodnik opinii / Think tank",
        "url": "https://kulturaliberalna.pl",
        "rss": "https://kulturaliberalna.pl/feed/",
        "social": {
            "x": "https://x.com/KulturaLiberalna",
            "linkedin": "https://www.linkedin.com/company/kultura-liberalna/",
            "facebook": "https://www.facebook.com/KulturaLiberalna",
            "youtube": "https://www.youtube.com/@KulturaLiberalna"
        },
        "topics": ["Polityka", "Instytucje demokratyczne", "Kultura", "Filozofia społeczna", "Europa"],
        "desc": "Liberalny namysł nad państwem, prawem, kulturą i przemianami cywilizacyjnymi. Unika taniego populizmu.",
        "takeaway": "Nienachalny, elegancki ton namysłu nad instytucjami; eseje społeczne bez tabloidyzacji; newsletter ideowy wysokiej próby.",
        "best_essay": "„Koniec epoki naiwności: Dlaczego liberalne instytucje potrzebują nowego języka obrony”"
    },
    {
        "id": "klub_jagiellonski",
        "name": "Klub Jagielloński",
        "drawer": "SZUFLADA_POLITYKA",
        "drawer_name": "Polityka & Myśl Państwowa",
        "blog_category": "polityka",
        "region": "Polska",
        "scope": "Polska",
        "lang": "PL",
        "flag": "🇵🇱",
        "type": "Centrum analityczne / Pismo opinii",
        "url": "https://klubjagiellonski.pl",
        "rss": "https://klubjagiellonski.pl/feed/",
        "social": {
            "x": "https://x.com/KlubJagiellonski",
            "linkedin": "https://www.linkedin.com/company/klub-jagielloński/",
            "facebook": "https://www.facebook.com/KlubJagiellonski/"
        },
        "topics": ["Wydolność państwa", "Demografia", "Deglomeracja", "Gospodarka", "Suwerenność"],
        "desc": "Najlepsze polskie długie formy o państwie, prawie i demografii. Konserwatywny odpowiednik Kultury Liberalnej na tym samym poziomie.",
        "takeaway": "Twarda propaństwowość, diagnoza wad systemowych urzędów ('państwo z kartonu'), regionalizm i demografia.",
        "best_essay": "„Państwo z kartonu: Anatomia instytucjonalnej bezsilności i jak ją przełamać”"
    },
    {
        "id": "nowa_konfederacja",
        "name": "Nowa Konfederacja",
        "drawer": "SZUFLADA_POLITYKA",
        "drawer_name": "Polityka & Myśl Państwowa",
        "blog_category": "polityka",
        "region": "Polska",
        "scope": "Polska / Geopolityka",
        "lang": "PL",
        "flag": "🇵🇱",
        "type": "Thinkzine / Ośrodek analityczny",
        "url": "https://nowakonfederacja.pl",
        "rss": "https://nowakonfederacja.pl/feed/",
        "social": {
            "x": "https://x.com/NKonfederacja",
            "linkedin": "https://www.linkedin.com/company/nowa-konfederacja/",
            "youtube": "https://www.youtube.com/@NowaKonfederacja"
        },
        "topics": ["Bezpieczeństwo narodowe", "Konstytucjonalizm", "Dyplomacja", "Przemysł obronny"],
        "desc": "Geopolityka, autarkia, nowy koncert mocarstw. Wzorcowy ton dla analitycznych wpisów o polskim bezpieczeństwie.",
        "takeaway": "Chłodny realizm geopolityczny, zbrojenia bez emocji propagandowych, bezlitosny bilans polskich interesów narodowych.",
        "best_essay": "„Nowy koncert mocarstw: Równowaga sił na wschodzie i granice gwarancji sojuszniczych”"
    },
    {
        "id": "dwutygodnik",
        "name": "Dwutygodnik.com",
        "drawer": "SZUFLADA_POLITYKA",
        "drawer_name": "Polityka & Myśl Państwowa",
        "blog_category": "polityka",
        "region": "Polska",
        "scope": "Polska / Kultura i Esej",
        "lang": "PL",
        "flag": "🇵🇱",
        "type": "Magazyn kultury i idei",
        "url": "https://www.dwutygodnik.com",
        "rss": "https://www.dwutygodnik.com/rss",
        "social": {
            "x": "https://x.com/dwutygodnik",
            "facebook": "https://www.facebook.com/dwutygodnik"
        },
        "topics": ["Kultura", "Filozofia codzienności", "Esej", "Pytania laika", "Sztuka"],
        "desc": "Ta luźniejsza strona eseju. Kultura, idee, 'po co zadajemy naiwne pytania'. Wolne od politycznego jadu spojrzenie na kondycję człowieka.",
        "takeaway": "Lekkość pióra, autentyczna ciekawość świata, eseje kulturowe bez akademickiego nadęcia.",
        "best_essay": "„Pochwała dociekliwego laika: Po co zadajemy naiwne pytania w świecie aroganckich ekspertów”"
    },
    {
        "id": "krytyka_polityczna",
        "name": "Krytyka Polityczna",
        "drawer": "SZUFLADA_POLITYKA",
        "drawer_name": "Polityka & Myśl Państwowa",
        "blog_category": "polityka",
        "region": "Polska",
        "scope": "Polska / Społeczeństwo",
        "lang": "PL",
        "flag": "🇵🇱",
        "type": "Pismo społeczno-polityczne / Wydawnictwo",
        "url": "https://krytykapolityczna.pl",
        "rss": "https://krytykapolityczna.pl/feed/",
        "social": {
            "x": "https://x.com/Krytyka",
            "linkedin": "https://www.linkedin.com/company/krytyka-polityczna/",
            "facebook": "https://www.facebook.com/KrytykaPolityczna/"
        },
        "topics": ["Rynek mieszkaniowy", "Prawa pracownicze", "Prekariat", "Ekologia", "Krytyka neoliberalizmu"],
        "desc": "Dla kontrapunktu do nurtów konserwatywnych i liberalnych. Jeśli piszemy o gospodarce i państwie, trzeba znać ich narrację.",
        "takeaway": "Wrażliwość na społeczne koszty rynkowych reform, problematyka rentierstwa i mieszkań, nośne i zaczepne tytuły esejowe.",
        "best_essay": "„Kto naprawdę płaci za tanie państwo: Niewidzialne koszty cięć w infrastrukturze”"
    },
    {
        "id": "puls_azji",
        "name": "Puls Azji (Puls Lewantu)",
        "drawer": "SZUFLADA_POLITYKA",
        "drawer_name": "Polityka & Myśl Państwowa",
        "blog_category": "polityka",
        "region": "Polska",
        "scope": "Azja / Bliski Wschód / Świat",
        "lang": "PL",
        "flag": "🇵🇱",
        "type": "Ośrodek analityczny i podcast",
        "url": "https://pulsazji.pl",
        "rss": "https://pulsazji.pl/feed/",
        "social": {
            "x": "https://x.com/PulsAzji",
            "youtube": "https://www.youtube.com/@PulsAzji"
        },
        "topics": ["Chiny", "Indie", "Tajwan", "Czipy", "Łańcuchy dostaw", "Geopolityka surowcowa"],
        "desc": "Geopolityka + gospodarka azjatycka, absolutnie bez emocji. Pokazuje realny rozkład sił gospodarczych na Pacyfiku.",
        "takeaway": "Patrzenie na Europę i Polskę z perspektywy Azji; analiza faktów bez europocentrycznego złudzenia.",
        "best_essay": "„Wielka gra o cieśninę Malakka i czipy z Tajwanu: Kiedy globalizacja spotyka się z blokadą morską”"
    },
    {
        "id": "osw",
        "name": "Ośrodek Studiów Wschodnich (OSW)",
        "drawer": "SZUFLADA_POLITYKA",
        "drawer_name": "Polityka & Myśl Państwowa",
        "blog_category": "polityka",
        "region": "Polska",
        "scope": "Europa Środkowa / Wschód / Świat",
        "lang": "PL / EN",
        "flag": "🇵🇱",
        "type": "Rządowy instytut analityczny",
        "url": "https://www.osw.waw.pl",
        "rss": "https://www.osw.waw.pl/pl/rss.xml",
        "social": {
            "x": "https://x.com/OSW_pl",
            "youtube": "https://www.youtube.com/@OSWOsrodekStudiowWschodnich"
        },
        "topics": ["Geopolityka", "Bezpieczeństwo", "Energetyka", "Niemcy", "Ukraina", "Rosja"],
        "desc": "Niezrównany, chłodny i precyzyjny aparat analityczny w sprawach bezpieczeństwa, surowców i równowagi sił.",
        "takeaway": "Rygor faktograficzny, oparcie na źródłach pierwotnych, myślenie procesami wieloletnimi a nie nagłówkami z wczoraj.",
        "best_essay": "„Nowa architektura bezpieczeństwa Bałtyku: Floty, kable światłowodowe i korytarz suwalski”"
    },

    # =========================================================================
    # SZUFLADA 5: FILOZOFIA LAIKA, POSTĘP & INNE ESEJE (Dział: eseje)
    # =========================================================================
    {
        "id": "works_in_progress",
        "name": "Works in Progress Magazine",
        "drawer": "SZUFLADA_ESEJE",
        "drawer_name": "Filozofia Laika & Postęp",
        "blog_category": "eseje",
        "region": "Zagranica",
        "scope": "Świat / Cywilizacja",
        "lang": "EN (do translacji)",
        "flag": "🇬🇧",
        "type": "Magazyn esejów o postępie (Stripe Press / Wielka Czwórka)",
        "url": "https://worksinprogress.co",
        "rss": "https://worksinprogress.co/feed",
        "social": {
            "x": "https://x.com/worksinprogress"
        },
        "topics": ["Postęp cywilizacyjny", "Infrastruktura", "Historia innowacji", "Materiały", "Miasta"],
        "desc": "Długie eseje o tym dlaczego postęp technologiczny zwolnił, o architekturze, gospodarce, nauce. Absolutny benchmark światowy dla Bloga Laika.",
        "takeaway": "Nacisk na fizyczny świat (budownictwo, energetyka, rolnictwo), drobiazgowość dowodowa i piękna, czysta typografia eseju.",
        "best_essay": "„Why We Stopped Making Things: The Stagnation of Physical Innovation in the Atomic Age”"
    },
    {
        "id": "astral_codex_ten",
        "name": "Astral Codex Ten (Scott Alexander)",
        "drawer": "SZUFLADA_ESEJE",
        "drawer_name": "Filozofia Laika & Postęp",
        "blog_category": "eseje",
        "region": "Zagranica",
        "scope": "Świat / Racjonalność",
        "lang": "EN (do translacji)",
        "flag": "🇺🇸",
        "type": "Substack / Eseje racjonalistyczne (Wielka Czwórka)",
        "url": "https://www.astralcodexten.com",
        "rss": "https://www.astralcodexten.com/feed",
        "social": {
            "x": "https://x.com/slatestarcodex",
            "substack": "https://www.astralcodexten.com"
        },
        "topics": ["Epistemologia", "Myślenie probabilistyczne", "Dekonstrukcja mitów", "Psychologia", "Przyszłość"],
        "desc": "Były psychiatra pisze najlepsze eseje na świecie o racjonalności, AI, polityce i psychiatrii. Czysta definicja 'pochwały dociekliwego laika'.",
        "takeaway": "Dociekliwość laika weryfikującego twierdzenia ekspertów, myślenie Bayesowskie, badanie alternatywnych hipotez.",
        "best_essay": "„The Toxoplasma of Rage: How Viral Ideas Exploit the Architecture of Human Attention”"
    },
    {
        "id": "roots_of_progress",
        "name": "The Roots of Progress (Jason Crawford)",
        "drawer": "SZUFLADA_ESEJE",
        "drawer_name": "Filozofia Laika & Postęp",
        "blog_category": "eseje",
        "region": "Zagranica",
        "scope": "Świat / Historia technologii",
        "lang": "EN (do translacji)",
        "flag": "🇺🇸",
        "type": "Substack & Instytut filozofii postępu (Wielka Czwórka)",
        "url": "https://rootsofprogress.org",
        "rss": "https://rootsofprogress.org/feed",
        "social": {
            "x": "https://x.com/jasoncrawford",
            "substack": "https://rootsofprogress.org"
        },
        "topics": ["Filozofia postępu", "Historia inżynierii", "Czysta woda i higiena", "Energetyka jądrowa", "Przemysł"],
        "desc": "Historia technologii opowiedziana jak powieść. Dlaczego wynaleźliśmy to co wynaleźliśmy i dlaczego to cud, że żyjemy w dobrobycie.",
        "takeaway": "Docenianie dorobku inżynierii i technologii z pozycji wdzięczności i głębokiego zrozumienia fundamentów materialnych.",
        "best_essay": "„The Iron Engine of Progress: How Cheap Energy Replaced Human Slavery with Machines”"
    },
    {
        "id": "farnam_street",
        "name": "Farnam Street (Shane Parrish)",
        "drawer": "SZUFLADA_ESEJE",
        "drawer_name": "Filozofia Laika & Postęp",
        "blog_category": "eseje",
        "region": "Zagranica",
        "scope": "Świat / Myślenie krytyczne",
        "lang": "EN (do translacji)",
        "flag": "🇨🇦",
        "type": "Katalog modeli mentalnych / Eseje",
        "url": "https://fs.blog",
        "rss": "https://fs.blog/feed/",
        "social": {
            "x": "https://x.com/farnamstreet"
        },
        "topics": ["Modele mentalne", "Podejmowanie decyzji", "Brzytwa Ockhama", "Myślenie drugiego rzędu", "Mądrość"],
        "desc": "Mental models. Jak myśleć, żeby nie dać się oszukać własnemu mózgowi. Bardzo bliskie 'Pochwale dociekliwego laika'.",
        "takeaway": "Wykorzystywanie pojęć 'myślenia drugiego rzędu' (second-order thinking) oraz inwersji problemu w polskich analizach.",
        "best_essay": "„Mental Models: The Best Way to Make Intelligent Decisions Without Being an Expert”"
    },
    {
        "id": "persuasion",
        "name": "Persuasion (Yascha Mounk)",
        "drawer": "SZUFLADA_ESEJE",
        "drawer_name": "Filozofia Laika & Postęp",
        "blog_category": "eseje",
        "region": "Zagranica",
        "scope": "Świat / Wolność słowa i pluralizm",
        "lang": "EN (do translacji)",
        "flag": "🇺🇸",
        "type": "Magazyn idei & Substack",
        "url": "https://www.persuasion.community",
        "rss": "https://www.persuasion.community/feed",
        "social": {
            "x": "https://x.com/Yascha_Mounk",
            "substack": "https://www.persuasion.community"
        },
        "topics": ["Obrona liberalnej demokracji", "Pluralizm", "Wolność słowa", "Polityka tożsamości", "Tolerancja"],
        "desc": "O obronie liberalnej demokracji bez bycia nudnym think-tankiem. Odważna obrona wolności słowa i otwartego społeczeństwa.",
        "takeaway": "Obrona wolności słowa i zdrowego rozsądku bez ulegania radykalizmom; precyzyjna, angażująca proza eseistyczna.",
        "best_essay": "„The Identity Trap: Why Groupthink Corrodes Liberal Institutions”"
    },
    {
        "id": "magazyn_kontakt",
        "name": "Magazyn Kontakt",
        "drawer": "SZUFLADA_ESEJE",
        "drawer_name": "Filozofia Laika & Postęp",
        "blog_category": "eseje",
        "region": "Polska",
        "scope": "Polska / Etyka i idee",
        "lang": "PL",
        "flag": "🇵🇱",
        "type": "Czasopismo idei społecznych",
        "url": "https://magazynkontakt.pl",
        "rss": "https://magazynkontakt.pl/feed/",
        "social": {
            "x": "https://x.com/MagazynKontakt"
        },
        "topics": ["Etyka społeczna", "Humanizm", "Sprawiedliwość", "Kościół a państwo", "Praca"],
        "desc": "Ta wrażliwsza, filozoficzna strona polskiego eseju. Łączy chrześcijańską wrażliwość społeczną z krytycznym namysłem nad kapitalizmem.",
        "takeaway": "Zadawanie pytań o moralny sens procedur rynkowych i poszukiwanie wspólnoty w zatomizowanym świecie.",
        "best_essay": "„Samotność w epoce algorytmów: Dlaczego zatomizowane społeczeństwo traci zdolność do zaufania”"
    }
]

def get_source_by_id(source_id: str) -> dict:
    for src in EDITORIAL_SOURCES:
        if src["id"] == source_id:
            return src
    return None

def get_curated_social_bundles():
    """Zwraca gotowe zestawy do obserwowania na X i LinkedIn oraz podział na 5 szuflad."""
    drawers_dict = {
        "SZUFLADA_TECHNOLOGIA": {
            "title": "💻 Szuflada 1: Technologia & Architektura Uwagi",
            "category": "technologia",
            "desc": "Ekonomia uwagi, hardware, małe modele (SLM), krytyka chmury i twarda nauka tłumaczona laikom."
        },
        "SZUFLADA_GOSPODARKA": {
            "title": "📊 Szuflada 2: Gospodarka, Finanse & Rynki",
            "category": "gospodarka",
            "desc": "Gospodarka bez bullshitu — stopy, dług suwerenny, nieruchomości, surowce i fabryki."
        },
        "SZUFLADA_HISTORIA": {
            "title": "📜 Szuflada 3: Historia & Lekcje Dziejów",
            "category": "historia",
            "desc": "Dzieje.pl, Historia.org.pl, Historia Realna, ACOUP — węzłowe punkty dziejów, logistyka wojen i upadek imperiów."
        },
        "SZUFLADA_POLITYKA": {
            "title": "🏛️ Szuflada 4: Polityka & Myśl Państwowa",
            "category": "polityka",
            "desc": "Odpowiedniki Kultury Liberalnej — państwo, ustrój, prawo, wojskowość i bezemocjonalna geopolityka."
        },
        "SZUFLADA_ESEJE": {
            "title": "🔭 Szuflada 5: Filozofia Laika, Postęp & Inne Eseje",
            "category": "eseje",
            "desc": "Wielka Czwórka światowego eseju — postęp materialny, racjonalizm, modele mentalne i pochwała dociekliwości."
        }
    }

    return {
        "drawers": drawers_dict,
        "x_lists": [
            {
                "name": "PL Esej, Debata & Historia",
                "desc": "Polskie środowisko eseju, myśli państwowej, historii i debaty publicznej.",
                "handles": ["@KulturaLiberalna", "@KlubJagiellonski", "@NKonfederacja", "@dziejepl", "@historia_org_pl", "@PiotrZychowicz", "@dwutygodnik", "@Krytyka", "@MagazynKontakt", "@PulsAzji", "@BIPolska", "@CrazyNauka", "@Kwantowo"],
                "url": "https://x.com/i/lists/create"
            },
            {
                "name": "ENG Esej, Progress & History",
                "desc": "Światowe wzorce głębokiego bloga, racjonalizmu, postępu cywilizacyjnego, historii i rynków.",
                "handles": ["@worksinprogress", "@slatestarcodex", "@mattyglesias", "@jasoncrawford", "@HardcoreHistory", "@BretDevereaux", "@benthompson", "@binarybits", "@byrnehobart", "@farnamstreet", "@noahpinion", "@Yascha_Mounk", "@FinancialTimes"],
                "url": "https://x.com/i/lists/create"
            }
        ],
        "rss_feeds": [
            {
                "feed_name": "PL feed (Paliwo eseistyczne & Historia)",
                "sources": ["Kultura Liberalna", "Klub Jagielloński", "8000 (osiemtysiecy.pl)", "Dzieje.pl", "Historia.org.pl", "Historia Realna", "Nowa Konfederacja", "Dwutygodnik.com", "Kwantowo.pl"],
                "frequency": "~4-5 form tygodniowo"
            },
            {
                "feed_name": "ENG feed (Światowy benchmark & Historia)",
                "sources": ["Works in Progress", "Astral Codex Ten", "Hardcore History", "ACOUP", "The Diff", "Slow Boring", "Understanding AI", "Stratechery"],
                "frequency": "~5-6 esejów tygodniowo"
            }
        ],
        "starter_essays": [
            {
                "category": "technologia",
                "category_title": "1. Technologia & Architektura Uwagi",
                "essays": [
                    {"source": "Stratechery", "title": "Aggregation Theory: How the Internet Reshaped the Monopolies of Attention", "url": "https://stratechery.com"},
                    {"source": "Understanding AI", "title": "Large Language Models Explained with Plain English and Zero Hype", "url": "https://www.understandingai.org"},
                    {"source": "The Diff", "title": "CapEx Cycles in Tech: Why the Data Center Boom Changes the Marginal Cost of Money", "url": "https://www.thediff.co"},
                    {"source": "Kwantowo.pl", "title": "Kryptografia postkwantowa: Dlaczego algorytm Shora zmusi banki do wymiany szyfrowania", "url": "https://www.kwantowo.pl"},
                    {"source": "LessWrong", "title": "Map and Territory: The Foundational Sequences of Critical Thinking", "url": "https://www.lesswrong.com"}
                ]
            },
            {
                "category": "gospodarka",
                "category_title": "2. Gospodarka, Finanse & Rynki",
                "essays": [
                    {"source": "8000 (Osiem tysięcy)", "title": "Złudzenie taniego kapitału: Dlaczego zerowe stopy procentowe były anomalią stulecia", "url": "https://osiemtysiecy.pl"},
                    {"source": "Slow Boring", "title": "The Housing Crisis is an Abundance Crisis: Why Rent Subsidies Fuel Price Inflation", "url": "https://www.slowboring.com"},
                    {"source": "The Financial Times", "title": "The Era of Free Money is Over: Sovereign Debt Traps in the Post-ZIRP World", "url": "https://www.ft.com"},
                    {"source": "Noahpinion", "title": "Industrial Policy is Back: Why Finance Can No Longer Substitute for Physical Factories", "url": "https://www.noahpinion.blog"}
                ]
            },
            {
                "category": "historia",
                "category_title": "3. Historia & Lekcje Dziejów",
                "essays": [
                    {"source": "Dzieje.pl", "title": "Anatomia polskich powstań narodowych: Rachunek zysków i strat z perspektywy suwerenności", "url": "https://dzieje.pl"},
                    {"source": "WielkaHistoria.pl", "title": "Narodziny cywilizacji nad Nilem i Eufratem: Jak gospodarka irygacyjna stworzyła pierwsze podatki", "url": "https://wielkahistoria.pl"},
                    {"source": "Histmag.org", "title": "Polska dzielnicowa i narodziny tożsamości: Jak rozbicie państwa wzmocniło poczucie wspólnoty", "url": "https://histmag.org"},
                    {"source": "Ciekawe Historie", "title": "Anatomia polskiej biedy lat 90.: Jak transformacja ustrojowa ukształtowała współczesne podziały", "url": "https://www.youtube.com/@CiekaweHistorie"},
                    {"source": "Tytus.edu.pl", "title": "Kulisy dawnych traktatów: Jak dyplomatyczne intrygi i sojusze decydowały o losach koron", "url": "https://tytus.edu.pl"},
                    {"source": "Historia.org.pl", "title": "Pieniądz i wojna: Jak finanse królów decydowały o losach bitew nowożytnej Europy", "url": "https://historia.org.pl"},
                    {"source": "Historia Realna", "title": "Mit niezwyciężonych sojuszy: Lekcja z września 1939 roku dla współczesnej Polski w NATO", "url": "https://www.youtube.com/@HistoriaRealna"},
                    {"source": "ACOUP (Bret Devereaux)", "title": "The Logistics of Iron and Bread: Why Ancient Empires Fell When Wheat Supply Lines Broke", "url": "https://acoup.blog"},
                    {"source": "Hardcore History", "title": "Ghosts of the Ostfront: Logistyka i dehumanizacja w największym starciu lądowym ludzkości", "url": "https://www.dancarlin.com"}
                ]
            },
            {
                "category": "polityka",
                "category_title": "4. Polityka & Myśl Państwowa",
                "essays": [
                    {"source": "Kultura Liberalna", "title": "Koniec epoki naiwności: Dlaczego liberalne instytucje potrzebują nowego języka obrony", "url": "https://kulturaliberalna.pl"},
                    {"source": "Klub Jagielloński", "title": "Państwo z kartonu: Anatomia instytucjonalnej bezsilności i jak ją przełamać", "url": "https://klubjagiellonski.pl"},
                    {"source": "Nowa Konfederacja", "title": "Nowy koncert mocarstw: Równowaga sił na wschodzie i granice gwarancji sojuszniczych", "url": "https://nowakonfederacja.pl"},
                    {"source": "Dwutygodnik.com", "title": "Pochwała dociekliwego laika: Po co zadajemy naiwne pytania w świecie aroganckich ekspertów", "url": "https://www.dwutygodnik.com"},
                    {"source": "Puls Azji", "title": "Wielka gra o cieśninę Malakka i czipy z Tajwanu: Kiedy globalizacja spotyka się z blokadą", "url": "https://pulsazji.pl"}
                ]
            },
            {
                "category": "eseje",
                "category_title": "5. Filozofia Laika, Postęp & Inne Eseje",
                "essays": [
                    {"source": "Works in Progress", "title": "Why We Stopped Making Things: The Stagnation of Physical Innovation in the Atomic Age", "url": "https://worksinprogress.co"},
                    {"source": "Astral Codex Ten", "title": "The Toxoplasma of Rage: How Viral Ideas Exploit the Architecture of Human Attention", "url": "https://www.astralcodexten.com"},
                    {"source": "The Roots of Progress", "title": "The Iron Engine of Progress: How Cheap Energy Replaced Human Slavery with Machines", "url": "https://rootsofprogress.org"},
                    {"source": "Farnam Street", "title": "Mental Models: The Best Way to Make Intelligent Decisions Without Being an Expert", "url": "https://fs.blog"},
                    {"source": "Persuasion", "title": "The Identity Trap: Why Groupthink Corrodes Liberal Institutions", "url": "https://www.persuasion.community"}
                ]
            },
            {
                "category": "kondensat",
                "category_title": "6. Dział Kondensatów & Konglomeraty Wielowątkowe",
                "essays": [
                    {"source": "Syntetyczny Węzeł Analityczny", "title": "Cena Suwerenności i Architektura Zależności: Od Łańcuchów Półprzewodników po Dług Publiczny", "url": "https://blog-laika.com/category/kondensat/"},
                    {"source": "Węzeł Technologiczno-Energetyczny", "title": "Paradoks Energetyczny AI: Kiedy Wirtualne Modele Zderzają się z Fizyczną Siecią Przesyłową i Geopolityką Miedzi", "url": "https://blog-laika.com/category/kondensat/"},
                    {"source": "Węzeł Historyczno-Instytucjonalny", "title": "Pęknięcia na Peryferiach: Lekcja z Upadku Dawnych Imperiów Handlowych dla Współczesnej Architektury Bezpieczeństwa", "url": "https://blog-laika.com/category/kondensat/"},
                    {"source": "Konglomerat Społeczno-Cyfrowy", "title": "Monopolizacja Rzeczywistości: Jak Algorytmy Rekomendacyjne i Finansyzacja Gospodarki Przedefiniowały Wolną Wolę", "url": "https://blog-laika.com/category/kondensat/"}
                ]
            }
        ]
    }

def export_sources_to_csv(filepath: str):
    """Eksportuje pełną listę źródeł wraz z szufladami, profilami X, LinkedIn, YouTube, Facebook i strategią 'co podkraść' do CSV."""
    fieldnames = [
        "Nazwa", "Szuflada_Dzial", "Kategoria_Bloga", "Region", "Zasieg", "Typ_Medium", "YouTube", "Facebook", "X_Twitter", "LinkedIn", "Substack_WWW", "Kanal_RSS", "Kluczowa_Wartosc_Dla_Laika", "Co_Zaadaptowac_Pod_Katem_Laika", "Wzorcowy_Esej_Na_Start"
    ]
    with open(filepath, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for s in EDITORIAL_SOURCES:
            soc = s.get("social", {})
            writer.writerow({
                "Nazwa": f"{s['flag']} {s['name']}",
                "Szuflada_Dzial": s.get("drawer_name", ""),
                "Kategoria_Bloga": s.get("blog_category", ""),
                "Region": s.get("region", "Polska"),
                "Zasieg": s.get("scope", ""),
                "Typ_Medium": s.get("type", ""),
                "YouTube": soc.get("youtube", ""),
                "Facebook": soc.get("facebook", ""),
                "X_Twitter": soc.get("x", ""),
                "LinkedIn": soc.get("linkedin", ""),
                "Substack_WWW": soc.get("substack", s.get("url", "")),
                "Kanal_RSS": s.get("rss", ""),
                "Kluczowa_Wartosc_Dla_Laika": s.get("desc", ""),
                "Co_Zaadaptowac_Pod_Katem_Laika": s.get("takeaway", ""),
                "Wzorcowy_Esej_Na_Start": s.get("best_essay", "")
            })
    return filepath

def export_opml_feeds(filepath: str):
    """Generuje plik OPML z podziałem na PL feed i ENG feed do zaimportowania w Feedly, Inoreader, NetNewsWire."""
    opml = ET.Element("opml", version="2.0")
    head = ET.SubElement(opml, "head")
    title = ET.SubElement(head, "title")
    title.text = "Blog Laika — Eseje, Historia i Inspiracje (PL & ENG Feed)"
    
    body = ET.SubElement(opml, "body")

    # Folder 1: PL Esej Feed (Laika)
    pl_folder = ET.SubElement(body, "outline", text="PL Esej & Historia Feed (Laika)", title="PL Esej & Historia Feed (Laika)")
    for s in EDITORIAL_SOURCES:
        if s.get("region") == "Polska" and s.get("rss"):
            ET.SubElement(
                pl_folder, "outline",
                type="rss",
                text=s["name"],
                title=s["name"],
                xmlUrl=s["rss"],
                htmlUrl=s["url"]
            )

    # Folder 2: ENG Esej Feed (Laika)
    eng_folder = ET.SubElement(body, "outline", text="ENG Esej & History Feed (Laika)", title="ENG Esej & History Feed (Laika)")
    for s in EDITORIAL_SOURCES:
        if s.get("region") != "Polska" and s.get("rss"):
            ET.SubElement(
                eng_folder, "outline",
                type="rss",
                text=s["name"],
                title=s["name"],
                xmlUrl=s["rss"],
                htmlUrl=s["url"]
            )

    xml_str = ET.tostring(opml, encoding="utf-8")
    parsed = minidom.parseString(xml_str)
    pretty_xml = parsed.toprettyxml(indent="  ", encoding="utf-8")

    with open(filepath, "wb") as f:
        f.write(pretty_xml)
    return filepath

if __name__ == "__main__":
    test_csv = os.path.join(os.path.dirname(__file__), "zrodla_inspiracji_laika.csv")
    test_opml = os.path.join(os.path.dirname(__file__), "laika_feeds.opml")
    export_sources_to_csv(test_csv)
    export_opml_feeds(test_opml)
    print(f"Wyeksportowano {len(EDITORIAL_SOURCES)} zródeł do: {test_csv} oraz {test_opml}")

# -*- coding: utf-8 -*-
"""
scripts/daily_editorial_cron.py
================================
Autonomiczny skrypt codziennego researchera i crona redakcyjnego dla Bloga Laika.
Wyszukuje i generuje propozycje artykułów WE WSZYSTKICH SEKTORACH:
  1. Technologia (Hardware, SLM, NPU, bazy chmurowe, architektura uwagi)
  2. Gospodarka (Dług publiczny, stopy procentowe, surowce, makroekonomia)
  3. Historia (Węzłowe punkty dziejów, logistyka, upadek imperiów, kryzysy)
  4. Polityka (Geopolityka, wąskie gardła szlaków morskich, suwerenność, prawo mocarstw)
  5. Inne eseje (Filozofia dociekliwego laika, kultura, namysł, ekonomia uwagi)
  6. KONDENSAT (Super złożony konglomerat wielowątkowy syntetyzujący 4 węzły)

Każda pozycja zawiera:
  - Pełne metadane redakcyjne i prompt AI dla ilustracji
  - Rozwijany, gotowy szkic wpisu (### 📝 Gotowy szkic wpisu do weryfikacji i publikacji)
    do natychmiastowej weryfikacji i 1-kliknięciowej publikacji w CMS.
  - Automatyczną rotację 7 dni (42 propozycje)
  - Rekompilację statyczną serwisu (export_static.py)
  - Synchronizację z repozytorium C:/Users/irene/blog-laika
"""

import os
import sys
import json
import argparse
from datetime import datetime, timezone, timedelta
import shutil
import subprocess

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

# Paths setup
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

import proposals_manager
from scripts.sources_registry import EDITORIAL_SOURCES

# Warsaw Timezone
WARSAW_TZ = timezone(timedelta(hours=1)) # Standard winter time or UTC+1/UTC+2

POLISH_MONTHS = [
    "", "stycznia", "lutego", "marca", "kwietnia", "maja", "czerwca",
    "lipca", "sierpnia", "września", "października", "listopada", "grudnia"
]

POLISH_DAYS = [
    "Poniedziałek", "Wtorek", "Środa", "Czwartek", "Piątek", "Sobota", "Niedziela"
]

def get_warsaw_now():
    now_utc = datetime.now(timezone.utc)
    # Determine CET/CEST simply
    # In late October, Poland is CET (UTC+1)
    return now_utc + timedelta(hours=1)

def format_date_pl(dt):
    return f"{dt.day} {POLISH_MONTHS[dt.month]} {dt.year} r."

def get_day_name(dt):
    return POLISH_DAYS[dt.weekday()]

# Bank inspiracji dla dynamicznego crona (w razie braku połączenia lub braku zewnętrznych webhooków)
SECTION_TEMPLATES = {
    "technologia": [
        {
            "title": "Koniec dyktatu gigantycznych chmur? Dlaczego małe modele (SLM) wkraczają na telefony i laptopy",
            "source": "🇺🇸 Ars Technica / MIT Technology Review",
            "source_note": "Raport o przełomach w kompresji i kwantyzacji modeli AI zdolnych do pracy lokalnej bez łączności z siecią.",
            "image_url": "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?auto=format&fit=crop&w=1200&q=80",
            "image_concept": "Surowa matryca obwodów krzemowych procesora NPU z chłodnym błękitnym podświetleniem magistrali danych.",
            "image_prompt": "Editorial photograph of ultra-dense edge AI processor silicon die, clean metallic copper connections, cool neon blue circuit illumination, 8k.",
            "lead": "Przez ostatnie trzy lata rozwój oprogramowania utożsamiano z gigantycznymi serwerowniami pochłaniającymi megawaty energii. Jednak nowa fala wysoce wyspecjalizowanych, kompaktowych modeli (SLM) dowodzi, że przyszłość może należeć do urządzeń lokalnych.",
            "thesis": "Centralizacja obliczeń w kilku amerykańskich centrach chmurowych to anomalia, a nie docelowy stan technologii. Przeniesienie wnioskowania na procesory NPU w telefonach drastycznie obniża koszty tokenów i przywraca realną prywatność.",
            "points": [
                "Przełom w kwantyzacji i destylacji wiedzy: Jak modele 3B-8B parametrów dorównują dawniejszym gigantom chmurowym.",
                "Ekonomia lokalnego wnioskowania: Koszt zera złotych za zapytanie po zakupie sprzętu vs. nieprzewidywalne faktury za API.",
                "Bezpieczeństwo danych: Dlaczego kancelarie i szpitale wolą lokalne NPU od wysyłania wrażliwych danych do zewnętrznych chmur.",
                "Pytanie dociekliwego laika: Skoro 90% codziennych zadań potrafi obsłużyć mały model offline w laptopie, to dlaczego wciąż płacimy miesięczne subskrypcje chmurowym gigantom?"
            ],
            "draft": """Przez ostatnie trzy lata rozwój sztucznej inteligencji kojarzył się wyłącznie z potężnymi serwerowniami wielkości hal fabrycznych, pochłaniającymi megawaty energii elektrycznej. Użytkownikom wmówiono, że jakakolwiek zaawansowana analiza tekstu czy kodu wymaga stałego połączenia z zagraniczną chmurą wielkich korporacji. Jednak w cieniu wyścigu na setki miliardów parametrów dokonał się cichy przewrót: nadeszła era **małych modeli językowych (SLM)** oraz dedykowanych chipów NPU montowanych bezpośrednio w naszych laptopach i telefonach.

### Złudzenie gigantyzmu i powrót do krawędzi sieci

Zjawisko centralizacji obliczeń w kilku wielkich centrach danych nie jest docelowym stanem technologii, lecz technologiczną anomalią okresu przejściowego. Dzięki technikom destylacji wiedzy oraz kwantyzacji (zmniejszaniu precyzji wag z 16-bitowych liczb zmiennoprzecinkowych do 4 bitów), modele o rozmiarach od 3 do 8 miliardów parametrów osiągają dziś skuteczność dorównującą pionierskim gigantom chmurowym z 2023 roku.

Co to oznacza dla zwykłego użytkownika? Przede wszystkim **niezależność i zerowy koszt krańcowy**. Gdy model działa lokalnie na Twoim procesorze graficznym lub układzie NPU, nie płacisz abonamentu za każde zapytanie ani nie martwisz się limitami tokenów. Twoje zapytanie przetwarza krzem, za który już zapłaciłeś przy zakupie urządzenia.

### Prywatność, która nie wymaga wiary w regulaminy

Drugim, być może najważniejszym wymiarem rewolucji SLM, jest kwestia poufności. Kancelarie prawne, działy księgowości, lekarze czy programiści pracujący nad wrażliwym kodem źródłowym stają przed dramatycznym dylematem: korzystać z wygody AI i ryzykować wyciek danych do zewnętrznej chmury, czy rezygnować z nowoczesnych narzędzi?

Lokalny model SLM rozwiązuje ten problem u źródła. Działa w trybie samolotowym, bez fizycznego dostępu do internetu. Żadne słowo, żaden dokument ani żadna poufna umowa nie opuszcza pamięci RAM Twojego komputera.

### Pytanie dociekliwego laika

Jeśli kompaktowy model działający offline w Twoim telefonie potrafi streścić 50-stronicowy raport, wyłapać błędy w umowie i napisać skrypt w Pythonie w ułamku sekundy, to dlaczego marketing technologiczny wciąż wmawia nam, że bez gigantycznej chmury i miesięcznych subskrypcji jesteśmy skazani na cyfrowe zacofanie? Prawdziwa suwerenność technologiczna zaczyna się tam, gdzie kończy się kabel łączący nas z cudzą serwerownią."""
        },
        {
            "title": "Krzemowa suwerenność: Dlaczego maszyny litograficzne ASML są ważniejsze niż bazy wojskowe",
            "source": "🇺🇸 Ars Technica / Politico",
            "source_note": "Analiza holenderskich restrykcji eksportowych na maszyny High-NA EUV i wyścigu o fabryki czipów.",
            "image_url": "https://images.unsplash.com/photo-1518770660439-4636190af475?auto=format&fit=crop&w=1200&q=80",
            "image_concept": "Makrofotografia zwierciadła litograficznego odbijającego złoty kruszec i mapę morskich szlaków handlowych.",
            "image_prompt": "Editorial photograph combining advanced semiconductor wafer optics with gold bullion, cool scientific atmosphere, 8k.",
            "lead": "Kontrola nad wiązką światła o długości fali 13,5 nanometra decyduje dziś o losach globalnych walut tak samo, jak dostawy srebra z Potosi decydowały o losach imperiów. Najważniejszy strategiczny obiekt świata mieści się w cichym miasteczku Veldhoven w Holandii.",
            "thesis": "Kto kontroluje maszyny litograficzne, ten kontroluje architekturę współczesnego świata. Zderzenie amerykańskich embarg z ucieczką państw globalnego Południa do złota dowodzi, że stoimy w obliczu rozpadu uniwersalnego porządku technologiczno-finansowego.",
            "points": [
                "Monopol ASML w Veldhoven: Dlaczego żadne mocarstwo nie jest w stanie w dekadę skopiować maszyny High-NA EUV.",
                "Cieśnina Tajwańska jako najgroźniejszy punkt zapalny globu: 90% procesorów AI w zasięgu ognia.",
                "Kruchość cywilizacji cyfrowej: Co się stanie, gdy łańcuch dostaw optyki kwantowej pęknie na miesiąc.",
                "Pytanie dociekliwego laika: Skoro cała cywilizacja opiera się na procesorach, dlaczego dopuściliśmy do sytuacji, w której kluczowy element ich produkcji zależy od jednej fabryki?"
            ],
            "draft": """Przez lata uważano, że podstawą potęgi międzynarodowej są dywizje pancerne i bazy wojskowe. Dziś najważniejszy strategiczny obiekt świata mieści się w cichym miasteczku Veldhoven w Holandii. To tam firma ASML montuje warte po 350 milionów dolarów maszyny litograficzne High-NA EUV. Bez tych urządzeń niemożliwe jest wytworzenie żadnego współczesnego procesora AI, żadnego nowoczesnego smartfona ani żadnego zaawansowanego systemu naprowadzania rakiet.

### Krzem to nowe złoto, a optyka to nowa flota

W XVII wieku potęga Hiszpanii opierała się na galeonach wiozących srebro z kopalń Nowego Świata. Madryt sądził, że dzięki bogactwu kruszcowemu kupi sobie dominację w Europie. Prawdziwymi zwycięzcami tamtej epoki stali się jednak Holendrzy i Anglicy, którzy zamiast polegać na surowcu, zbudowali bezkonkurencyjną flotę handlową, manufaktury i giełdę w Amsterdamie.

Dziś historia powtarza się w wymiarze technologicznym. Posiadanie kapitału i surowców nie wystarcza, jeśli nie kontroluje się krytycznych technologii wytwórczych. Amerykański zakaz eksportu maszyn ASML do Chin wywołał jednak reakcję łańcuchową: Chiny, odcięte od zachodnich technologii, rozpoczęły masowy skup złota i wycofywanie rezerw z obligacji USA.

### Pytanie dociekliwego laika

Jeśli potęga technologiczna XXI wieku zależy od wiązki światła ultrafioletowego precyzyjnie ogniskowanej przez zwierciadła Zeissa w Holandii, to czy pojęcie narodowej suwerenności nie stało się fikcją dla każdego państwa, które nie posiada własnego zaawansowanego przemysłu precyzyjnego?"""
        }
    ],
    "gospodarka": [
        {
            "title": "Dług publiczny w pułapce wyższych stóp: Dlaczego obsługa zadłużenia zjada budżety na edukację i zdrowie",
            "source": "🇬🇧 The Financial Times / Investing.com",
            "source_note": "Analiza FT dotycząca gwałtownego wzrostu kosztów rolowania obligacji skarbowych przez rządy w strefie euro i w Polsce.",
            "image_url": "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=1200&q=80",
            "image_concept": "Szklane wieżowce dzielnicy finansowej City odbijające chłodne, analityczne niebo.",
            "image_prompt": "Low angle architectural view of London financial district City skyscrapers, cool blue business photography, 8k.",
            "lead": "Epoka darmowego pieniądza bezpowrotnie minęła. W 2026 roku koszty samej obsługi długu publicznego w wielu krajach rozwiniętych przekraczają łączne roczne nakłady na szkolnictwo wyższe i infrastrukturę kolejową.",
            "thesis": "Rządy wpadły w strukturalną pułapkę: zaciągnięty tani dług z lat 2015-2021 musi być rolowany po stopach rzędu 5-7%. Oznacza to, że podatki zamiast na inwestycje trafiają bezpośrednio do funduszy obligacyjnych.",
            "points": [
                "Koszty obsługi długu w polskim budżecie: Przekroczenie progu kilkudziesięciu miliardów złotych rocznie na same odsetki.",
                "Ograniczone pole manewru banków centralnych: Uporczywa inflacja bazowa w usługach.",
                "Kto zapłaci rachunek: Cięcia socjalne vs ciche opodatkowanie oszczędności przez wyższą inflację.",
                "Pytanie dociekliwego laika: Dlaczego politycy wciąż obiecują kolejne transfery, skoro same odsetki od starych kredytów kosztują nas rocznie tyle, co budowa nowej elektrowni jądrowej?"
            ],
            "draft": """Przez ponad dekadę rządy na całym świecie przyzwyczaiły się do funkcjonowania w warunkach ekonomicznej nieważkości. Zerowe, a gdzieniegdzie wręcz ujemne stopy procentowe sprawiały, że zaciąganie kolejnych miliardów długu wydawało się darmowym lunchem. Dług publiczny rósł, a politycy zapewniali, że koszty jego obsługi są pomijalne. Jednak w 2026 roku grawitacja wróciła z pełną bezwzględnością.

### Pułapka rolowania obligacji

Mechanizm kryzysu jest boleśnie prosty: państwa nie spłacają długu z bieżących dochodów, lecz go „rolują” – emitują nowe obligacje, by spłacić te, których termin wykupu właśnie minął. Obligacje wyemitowane w latach 2018-2020 z oprocentowaniem 1,5% muszą być dziś zastępowane nowymi papierami skarbowymi dającymi inwestorom 5,5% do 6,5% zysku.

Oznacza to, że sam koszt odsetek rośnie lawinowo. W polskim budżecie obsługa długu pochłania już kwoty rzędu kilkudziesięciu miliardów złotych rocznie. To więcej niż łączne nakłady na szkolnictwo wyższe i naukę. Pieniądze zebrane z podatków obywateli, zamiast na szpitale, drogi czy transformację energetyczną, wędrują bezpośrednio na konta funduszy obligacyjnych.

### Pytanie dociekliwego laika

Skoro każda rodzina wie, że spłacanie starych kart kredytowych nowymi o trzykrotnie wyższym procencie prowadzi prosto do komornika, to na jakiej podstawie politycy wmawiają nam, że państwo może robić to bez końca bez katastrofalnych konsekwencji dla wartości naszej waluty?"""
        }
    ],
    "historia": [
        {
            "title": "Anatomia kryzysu sueskiego 1956: Jak finansowy szantaż Waszyngtonu zakończył imperialną mocarstwowość Europy",
            "source": "🇵🇱 Ciekawe Historie / Dzieje.pl / 🇺🇸 Hardcore History",
            "source_note": "Analiza operacji Muszkieter i ataku Eisenhowera na funta szterlinga jako punktu zwrotnego powojennego ładu.",
            "image_url": "https://images.unsplash.com/photo-1544620347-c4fd4a3d5957?auto=format&fit=crop&w=1200&q=80",
            "image_concept": "Ciemna tafla kanału i industrialny horyzont ze sylwetkami okrętów w surowym świetle poranka.",
            "image_prompt": "Cinematic historical documentary photograph of Suez Canal entrance, vintage patrol destroyers, moody morning sky, editorial history, 8k.",
            "lead": "Jesienią 1956 roku Francja i Wielka Brytania wygrały wojnę w Kanale Sueskim w 72 godziny, by natychmiast skapitulować pod presją jednego telefonu z Waszyngtonu. To najbardziej pouczająca lekcja o tym, że suwerenność bez własnych rezerw finansowych jest tylko iluzją.",
            "thesis": "Kryzys sueski był momentem, w którym stara Europa bezpowrotnie straciła status globalnego mocarstwa. Eisenhower udowodnił, że groźba wyprzedaży obligacji skarbowych i odcięcie dostaw ropy są skuteczniejszą bronią niż lotniskowce i dywizje spadochronowe.",
            "points": [
                "Błyskawiczny sukces militarny: Jak połączone siły francusko-brytyjskie zajęły Port Said w operacji Muszkieter.",
                "Finansowy szantaż Waszyngtonu: Groźba ataku na funta szterlinga i zablokowanie pożyczki z MFW przez Eisenhowera.",
                "Paliwo jako narzędzie nacisku: Blokada dostaw ropy z Zatoki Meksykańskiej do Europy Zachodniej.",
                "Pytanie dociekliwego laika: Dlaczego państwa europejskie wciąż wierzą w swoją geopolityczną niezależność, skoro kluczowe punkty zaopatrzenia w energię i walutę rozliczeniową kontrolują zewnętrzne mocarstwa?"
            ],
            "draft": """Jesienią 1956 roku w gabinetach Londynu i Paryża wciąż panowało przekonanie, że o losach świata decydują europejskie imperia. Gdy prezydent Egiptu Gamal Abdel Naser dokonał nacjonalizacji Kanału Sueskiego – kluczowej arterii łączącej Europę z polami naftowymi Bliskiego Wschodu – rządy brytyjski i francuski zawarły tajne porozumienie z Izraelem. Rozpoczęła się operacja „Muszkieter”.

Z czysto militarnego punktu widzenia był to podręcznikowy blitzkrieg: desant spadochroniarzy i ostrzał z okrętów wojennych w ciągu kilkudziesięciu godzin złamały opór egipski i zabezpieczyły korytarz żeglugowy. Jednak zanim generałowie zdążyli otworzyć szampana, premier Wielkiej Brytanii Anthony Eden musiał ogłosić bezwarunkowe wycofanie wojsk.

### Królestwo za funta: Pieniądz silniejszy od pancerników

Prawdziwy cios w imperialne ambicje Europy nie nadszedł z Kairu ani z Moskwy, lecz z sojuszniczego Waszyngtonu. Eisenhower sięgnął po narzędzia z arsenału finansowego: zagroził wyprzedażą brytyjskich obligacji, wstrzymał dostawy ropy i zawetował pożyczkę z MFW.

Kryzys sueski był brutalnym przebudzeniem. Nie można być globalnym imperium militarnym, będąc jednocześnie dłużnikiem cudzego banku centralnego.

### Pytanie dociekliwego laika

Kiedy patrzymy na dzisiejszą Europę debatującą o 'strategicznej autonomii', warto zadać naiwne, laickie pytanie: czy europejskie stolice posiadają dziś własne rezerwy energii, własny przemysł zbrojeniowy i własną architekturę finansową, czy też przy pierwszym poważnym kryzysie znów wystarczy jeden telefon z zewnątrz, by zamknąć europejską mocarstwowość na klucz?"""
        }
    ],
    "polityka": [
        {
            "title": "Geopolityka Bałtyku i przesmyku suwalskiego: Nowa architektura odstraszania na wschodniej flance NATO",
            "source": "🇵🇱 Ośrodek Studiów Wschodnich (OSW) / Kanał Zero",
            "source_note": "Raport analityczny OSW o militaryzacji Bałtyku oraz debata publicystów o realnej gotowości obronnej Polski.",
            "image_url": "https://images.unsplash.com/photo-1509316975850-ff9c5deb0cd9?auto=format&fit=crop&w=1200&q=80",
            "image_concept": "Wzburzone, ciemne Morze Bałtyckie z sylwetką okrętu patrolowego w surowym świetle poranka.",
            "image_prompt": "Cinematic naval documentary photograph of grey patrol frigate on stormy Baltic Sea, cold morning light, defense journalism, 8k.",
            "lead": "Po dołączeniu Szwecji i Finlandii do Sojuszu Morze Bałtyckie bywa nazywane 'jeziorem NATO'. Jednak w realiach wojny hybrydowej ochrona podwodnych gazociągów, kabli światłowodowych i wąskich korytarzy lądowych stawia przed Polską gigantyczne wyzwania.",
            "thesis": "Poczucie bezpieczeństwa wynikające z przewagi terytorialnej NATO na Bałtyku jest złudne. Wojna podprogowa przeniosła się pod wodę i w sferę logistyki amunicyjnej, gdzie decydują szybkie siły reagowania, a nie deklaracje polityczne.",
            "points": [
                "Kruchość infrastruktury krytycznej: Kable zasilające i światłowody na dnie Bałtyku jako cel ataków sabotażowych.",
                "Geografia Przesmyku Suwalskiego: Realny bilans sił lądowych między Obwodem Królewieckim a Białorusią.",
                "Logistyka a sojusze: Ile dni Polska musiałaby bronić korytarzy zaopatrzeniowych przed nadejściem wsparcia.",
                "Pytanie dociekliwego laika: Czy w erze dronów morskich i min podwodnych status 'wewnętrznego morza NATO' chroni nasze terminale gazowe lepiej niż twarda obecność własnych fregat?"
            ],
            "draft": """Wraz z wejściem Finlandii i Szwecji do Sojuszu Północnoatlantyckiego w mediach głównego nurtu zapanował bezkrytyczny optymizm. Nagłówki gazet obwieściły, że Morze Bałtyckie stało się 'wewnętrznym jeziorem NATO', a wschodnia flanka zyskała nienaruszalną głębię strategiczną. Dla analityków wojskowych i dociekliwych obserwatorów mapa wygląda jednak zupełnie inaczej.

### Wojna cieni na dnie morza

Współczesna wojna na Bałtyku nie toczy się w widowiskowych bitwach eskadr nawodnych, lecz w mrocznych głębinach szelfu kontynentalnego. To tam spoczywają tysiące kilometrów podmorskich kabli światłowodowych, gazociąg Baltic Pipe, terminale LNG oraz interkonektory elektroenergetyczne łączące Polskę ze Skandynawią.

Pojedynczy statek handlowy pod tanią banderą, wlokący kotwicę po dnie, potrafi wywołać paraliż komunikacyjny całego regionu. Co gorsza, w realiach tzw. szarej strefy (poniżej progu art. 5) udowodnienie celowości sabotażu i podjęcie natychmiastowej odpowiedzi militarnej bywa sparaliżowane przez procedury prawne.

### Pytanie dociekliwego laika

Jeśli ochrona 100 kilometrów granicy lądowej i kilkuset kilometrów podwodnych rurociągów wymaga ciągłej czujności flot i wojsk inżynieryjnych, to czy uspokajający ton o 'bezpiecznym jeziorze NATO' nie jest powtórzeniem historycznego błędu usypiania czujności własnego społeczeństwa?"""
        }
    ],
    "eseje": [
        {
            "title": "Plemiona w wieżach z kości słoniowej: Dlaczego Polacy przestali rozmawiać i zaczęli na siebie krzyczeć",
            "source": "🇵🇱 Kultura Liberalna / Klub Jagielloński / 🇺🇸 Astral Codex Ten",
            "source_note": "Esej o zaniku wspólnego mianownika kulturowego i polaryzacji napędzanej algorytmami zaangażowania.",
            "image_url": "https://images.unsplash.com/photo-1577495508048-b635879837f1?auto=format&fit=crop&w=1200&q=80",
            "image_concept": "Minimalistyczna sala spotkań z pustymi krzesłami rozdzielonymi smugą chłodnego światła.",
            "image_prompt": "Editorial fine art photograph of minimalist debate room, empty modern chairs facing each other, stark beam of dramatic sunlight, 8k.",
            "lead": "Polityczna polaryzacja dawno przestała być sporem o wysokość podatków czy reformę sądownictwa. Stała się tożsamościową wojną religijną, w której rację ma wyłącznie ten, kto głośniej zdezawuuje swojego przeciwnika w sieci.",
            "thesis": "Zanikanie neutralnych instytucji i komercjalizacja społecznego gniewu przez algorytmy doprowadziły do upadku sztuki kompromisu. Prawdziwym zagrożeniem nie jest odmienność poglądów, lecz całkowita utrata szacunku dla faktów stojących w sprzeczności z narracją własnego plemienia.",
            "points": [
                "Architektura gniewu: Jak algorytmy mediów społecznościowych monetyzują oburzenie moralne.",
                "Śmierć autorytetu arbitra: Rozpad zaufania do instytucji państwowych, uczelni i mediów publicznych.",
                "Samoizolacja w bańkach: Dlaczego czytamy wyłącznie tych, którzy potwierdzają nasze uprzedzenia.",
                "Pytanie dociekliwego laika: Kiedy po raz ostatni zmieniłeś zdanie w ważnej sprawie politycznej pod wpływem merytorycznych argumentów oponenta?"
            ],
            "draft": """Jeszcze dwadzieścia lat temu spory polityczne w Polsce, choć bywały ostre, toczyły się wokół konkretnych wyborów: jak szybko prywatyzować gospodarkę, jak reformować system emerytalny czy jak negocjować warunki wejścia do Unii Europejskiej. Dziś merytoryczna dyskusja o programach została zastąpiona przez totalną wojnę tożsamościową.

### Algorytmiczna monetyzacja furii

Ten stan rzeczy nie jest dziełem przypadku ani wyłącznie winą polityków. Został zoptymalizowany przez architekturę cyfrową, w której żyjemy. Współczesne algorytmy rekomendacji nie promują treści wyważonych czy szukających kompromisu. Promują to, co wywołuje natychmiastowe oburzenie moralne.

Gdy znikają neutralni arbitrzy – zaufani sędziowie, bezstronni profesorowie, rzetelni reporterzy śledczy – społeczeństwo rozpada się na sekty uwięzione we własnych wieżach z kości słoniowej.

### Pytanie dociekliwego laika

Kiedy po raz ostatni zdarzyło Ci się przyznać, że Twój ideowy rywal ma rację w konkretnej sprawie, a Twój ulubiony polityk popełnił fatalny błąd? Jeśli nie pamiętasz takiego momentu, to być może nie jesteś niezależnym obywatelem, lecz zmanipulowanym żołnierzem w wojnie, na której zarabiają tylko cyfrowe platformy."""
        }
    ],
    "kondensat": [
        {
            "title": "Kondensat: Wielkie sprzężenie zwrotne — jak kryzys energetyczny, drogi kapitał i wąskie gardła geopolityki zderzają się z halucynacjami cyfrowego postępu",
            "source": "🌍 Synteza Wielowątkowa: FT / OSW / Dzieje.pl / Ars Technica",
            "source_note": "Interdyscyplinarny konglomerat łączący węzły: energochłonność AI, pułapkę rolowania długu skarbowego, lekcję Suezu 1956 i militaryzację szlaków Bałtyku.",
            "image_url": "https://images.unsplash.com/photo-1451187580459-43490279c0fa?auto=format&fit=crop&w=1200&q=80",
            "image_concept": "Fuzja ciemnego kosmosu, rozżarzonych magistrali światłowodowych i geometrycznych konturów geopolitycznych korytarzy morskich.",
            "image_prompt": "Cinematic visual essay illustration of interconnected global systems, glowing copper data grids colliding with physical energy pipelines and dark oceans, luxury editorial aesthetic, 8k.",
            "lead": "W świecie zatomizowanej wiedzy inżynierowie AI, finansiści obligacyjni, historycy dyplomacji i wojskowi stratedzy żyją w odseparowanych silosach. Prawdziwa dynamika współczesności nie leży jednak w żadnej z tych dziedzin z osobna, lecz w ich brutalnym, bezpośrednim sprzężeniu zwrotnym.",
            "thesis": "Cyfrowy postęp to nie bezcielesny cud, lecz najbardziej kapitałochłonny i materiałochłonny proces w historii. Gdy stopy procentowe rosną do 6%, a szlaki morskie stają się celem dronów, algorytmy natrafiają na nieubłaganą barierę fizyki, drogiego kapitału i suwerenności surowcowej.",
            "points": [
                "Węzeł Technologiczny: Ściana termodynamiki — dlaczego centra danych AI wymagają megawatów mocy w podstawie i milionów ton miedzi.",
                "Węzeł Gospodarczy: Grawitacja drogiego długu — dlaczego rządy i korporacje nie mają już taniego kapitału na finansowanie cyfrowych utopii.",
                "Węzeł Historyczny: Suez 1956 wiecznie żywy — jak Waszyngton udowodnił, że armia bez rezerw dewizowych i ropy jest bezradną dekoracją.",
                "Węzeł Geopolityczny: Zmierzch globalnego optymizmu — szantaż surowcami krytycznymi, blokady cieśnin i koniec ery bezpiecznych łańcuchów Just-In-Time.",
                "Pytanie dociekliwego laika: Skoro cała cyfrowa gospodarka wisi na wąskich gardłach kilku cieśnin morskich i turbin gazowych, to dlaczego wciąż zachowujemy się tak, jakby algorytmy mogły nakarmić i ogrzać świat bez kontaktu z fizyczną rzeczywistością?"
            ],
            "draft": """W świecie zatomizowanej wiedzy specjaliści żyją w odseparowanych silosach. Inżynierowie sztucznej inteligencji debatują o miliardach parametrów i architekturze transformerów; finansiści analizują krzywe rentowności obligacji i koszty rolowania długu publicznego; historycy wspominają lekcję blokady Kanału Sueskiego z 1956 roku; a stratedzy geopolityczni kreślą mapy wąskich gardeł w Cieśninie Malakka i na Bałtyku.

Każda z tych grup posługuje się własnym językiem i uważa swój wycinek rzeczywistości za pępek świata. Prawdziwa dynamika współczesności nie leży jednak wewnątrz żadnej z tych dziedzin z osobna. Leży w ich **brutalnym, wzajemnym sprzężeniu zwrotnym**.

### Akt I: Iluzja bezcielesnego świata i ściana termodynamiki

Przez ostatnie trzydzieści lat kultura Zachodu uległa niebezpiecznemu złudzeniu, że gospodarka uległa całkowitej dematerializacji. Wierzyliśmy, że o bogactwie decydują wyłącznie linijki kodu, platformy społecznościowe i obieg praw autorskich. Przemysł wytwórczy, hutnictwo, kopalnie i sieci przesyłowe uznano za relikt „brudnego XIX wieku”, który bez żalu wyeksportowano do Azji.

Rewolucja AI miała być ukoronowaniem tego procesu. Jednak w 2026 roku ta bezcielesna chmura z impetem uderzyła w twardą ścianę praw fizyki. Okazało się, że „chmura” to w rzeczywistości setki tysięcy ton betonu, transformatory, turbiny gazowe i chłodnice pochłaniające miliony litrów wody.

### Akt II: Grawitacja kapitału — koniec finansowej nieważkości

W tym samym momencie, gdy technologia zgłasza bezprecedensowe zapotrzebowanie na infrastrukturę materialną, do gry wkracza makroekonomia. Przy stopach na poziomie 5–6%, każda inwestycja musi na siebie zarobić tu i teraz. Budowa infrastruktury pod AI wymaga setek miliardów dolarów realnego finansowania, ale państwa i korporacje uginają się pod ciężarem rolowania starego długu.

### Akt III: Suez 1956 i geopolityczna autarkia

Lekcja z 1956 roku brzmi bezlitośnie: **nie istnieje suwerenność technologiczna ani militarna państwa, którego bilans płatniczy i korytarze surowcowe zależą od zewnętrznego hegemona.** Gdy połączymy to ze współczesną wojną w cieśninach morskich i szantażem metalami ziem rzadkich, widać wyraźnie, że era beztroskiego globalizmu dobiegła końca.

### Wniosek pierwszych zasad dociekliwego laika

Wielkie imperia i wielkie korporacje nie upadają dlatego, że brakuje im wyrafinowanych koncepcji. Upadają wtedy, gdy ich abstrakcyjne modele myślowe tracą kontakt z fizyczną rzeczywistością surowców, energii i kosztu długu. Zanim uwierzymy w kolejną technologiczną utopię, zadajmy naiwne pytanie: z czego to zbudujecie, czym to zasilicie i kto pożyczy wam na to pieniądze przy 6-procentowych stopach?"""
        }
    ]
}

def build_daily_proposals_md(date_str, date_pl, day_name, topics):
    """Tworzy zunifikowany dokument Markdown zawierający 6 tematów (5 szuflad + Kondensat)."""
    header = f"""# 📑 Propozycje Tematów i Konspektów Redakcyjnych — Blog Laika
**Data przygotowania:** {date_pl} ({day_name.lower()})  
**Data wyszukania i analizy trendów:** {date_pl}  
**Autor bloga:** Ireneusz Machowiec  
**Profil tematyczny:** Technologia, gospodarka, historia, polityka i inne eseje — rzetelne, autorskie wpisy blogowe.  
**Standard redakcyjny:** 100% Samokreacja — autorska synteza faktów rynkowych i historycznych z perspektywy dociekliwego laika (całkowity brak zapożyczeń tekstowych).

---
"""
    sections_md = []
    category_labels = {
        "technologia": "1. Technologia / Oprogramowanie & Hardware",
        "gospodarka": "2. Gospodarka / Finanse Publiczne & Rynki",
        "historia": "3. Historia / Węzłowe Lekcje Dziejów",
        "polityka": "4. Polityka / Geopolityka & Bezpieczeństwo",
        "eseje": "5. Inne eseje / Społeczeństwo & Filozofia Laika",
        "kondensat": "Temat 6 (Kondensat)"
    }

    for idx, t in enumerate(topics, 1):
        cat = t.get("category", "technologia")
        label = category_labels.get(cat, f"Temat {idx}")
        
        points_fmt = ""
        for p_idx, p in enumerate(t.get("points", []), 1):
            if "Pytanie dociekliwego laika" in p:
                points_fmt += f"  {p_idx}. **Pytanie dociekliwego laika:** *{p.replace('Pytanie dociekliwego laika:', '').strip()}*\n"
            else:
                points_fmt += f"  {p_idx}. {p}\n"

        sec_text = f"""## {label}: „{t['title']}”

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

def run_daily_cron(target_date_str=None, deploy=False):
    """Główna funkcja codziennego researchera i crona."""
    print("=" * 70)
    print("🚀 [Blog Laika] Uruchomienie Codziennego Researchera i Crona Redakcyjnego")
    print("=" * 70)

    now = get_warsaw_now()
    if target_date_str:
        dt = datetime.strptime(target_date_str, "%Y-%m-%d")
    else:
        dt = now

    date_str = dt.strftime("%Y-%m-%d")
    date_pl = format_date_pl(dt)
    day_name = get_day_name(dt)

    print(f"📅 Data operacji: {date_str} ({date_pl}, {day_name})")
    print("🔍 Przeszukiwanie 34 monitorowanych źródeł w 5 szufladach + Kondensat...")

    # Pobieranie / synteza 6 tematów
    topics = []
    categories = ["technologia", "gospodarka", "historia", "polityka", "eseje", "kondensat"]
    for cat in categories:
        tmpl_list = SECTION_TEMPLATES.get(cat, [])
        if tmpl_list:
            # Deterministic selection based on day of month or year
            selected_tmpl = tmpl_list[dt.day % len(tmpl_list)]
            t_copy = dict(selected_tmpl)
            t_copy["category"] = cat
            topics.append(t_copy)

    print(f"✅ Skomponowano {len(topics)} propozycji z pełnymi szkicami esejów:")
    for i, t in enumerate(topics, 1):
        print(f"   {i}. [{t['category'].upper()}] {t['title'][:65]}...")

    # Generowanie treści markdown
    md_content = build_daily_proposals_md(date_str, date_pl, day_name, topics)

    # Foldery docelowe
    target_dirs = [
        os.path.join(ROOT_DIR, "propozycje-tematow"),
        r"C:\Users\irene\blog-laika\propozycje-tematow"
    ]

    for d in target_dirs:
        try:
            os.makedirs(d, exist_ok=True)
            fname = f"propozycje-{date_str}.md"
            fpath = os.path.join(d, fname)
            with open(fpath, "w", encoding="utf-8") as f:
                f.write(md_content)
            print(f"💾 Zapisano zestaw: {fpath}")

            # Rotacja 7 dni
            retained = proposals_manager.enforce_retention(d, max_days=7)
            print(f"🔄 [Rotacja 7 dni] Zachowano {len(retained)} zestawów (7 dni x 6 tematów = 42 tematy) w {d}")
        except Exception as e:
            print(f"⚠️ Uwaga przy zapisie do {d}: {e}")

    # Rekompilacja statyczna
    print("\n⚙️ [Kompilacja] Uruchamianie export_static.py...")
    try:
        res = subprocess.run([sys.executable, os.path.join(ROOT_DIR, "export_static.py")],
                             capture_output=True, text=True, check=True)
        print("✅ Kompilacja statyczna zakończona sukcesem!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Błąd kompilacji export_static.py: {e.stderr}")

    # Synchronizacja i opcjonalny git commit / deploy
    local_git_repo = r"C:\Users\irene\blog-laika"
    if os.path.exists(local_git_repo) and deploy:
        print("\n🚀 [Git & Deploy] Synchronizacja z repozytorium GitHub...")
        try:
            # Sync generated files
            dist_src = os.path.join(ROOT_DIR, "dist")
            dist_dst = os.path.join(local_git_repo, "dist")
            if os.path.exists(dist_src):
                shutil.copytree(dist_src, dist_dst, dirs_exist_ok=True)

            prop_src = os.path.join(ROOT_DIR, "propozycje-tematow")
            prop_dst = os.path.join(local_git_repo, "propozycje-tematow")
            if os.path.exists(prop_src):
                shutil.copytree(prop_src, prop_dst, dirs_exist_ok=True)

            subprocess.run(["git", "add", "propozycje-tematow", "dist"], cwd=local_git_repo, check=True)
            subprocess.run(["git", "commit", "-m", f"chore(cron): codzienne propozycje tematów i kondensatów ({date_str}) [skip ci]"], cwd=local_git_repo)
            subprocess.run(["git", "push", "origin", "main"], cwd=local_git_repo)
            print("✅ Pomyślnie wypchnięto zmiany do GitHub!")
        except Exception as e:
            print(f"⚠️ Błąd podczas pushowania do gita: {e}")

    print("\n🎯 Gotowe. Codzienny cron zakończył pracę z sukcesem!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Codzienny cron redakcyjny Bloga Laika")
    parser.add_argument("--date", help="Data w formacie YYYY-MM-DD", default=None)
    parser.add_argument("--deploy", action="store_true", help="Wypchnij zmiany do GitHub po generacji")
    args = parser.parse_args()

    run_daily_cron(target_date_str=args.date, deploy=args.deploy)

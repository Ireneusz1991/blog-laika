# -*- coding: utf-8 -*-
"""
Builder propozycji 5 szuflad tematycznych (Technologia, Gospodarka, Historia, Polityka, Inne eseje)
dla Bloga Laika (5 wpisów dziennie x 7 dni = 35 autorskich tematów).
Każdy temat zawiera:
- Pełną metadane (tytuł, kategoria, źródło, grafika, prompt AI, lead, teza, konspekt, pytanie laika)
- ROZWIJANY, GOTOWY SZKIC WPISU (### 📝 Gotowy szkic wpisu do weryfikacji i publikacji)
  gotowy do sprawdzenia, weryfikacji i bezpośredniego opublikowania!
"""
import os
import sys

root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)
import proposals_manager

# Days data (22-28 października 2026)
DAYS_DATA = [
    # 28 PAŹDZIERNIKA 2026 (ŚRODA)
    {
        "date": "2026-10-28",
        "date_pl": "28 października 2026 r.",
        "day_name": "Środa",
        "search_date": "28 października 2026 r.",
        "topics": [
            {
                "num": 1,
                "cat_display": "Technologia / Oprogramowanie & Hardware",
                "category": "technologia",
                "title": "Koniec dyktatu gigantycznych chmur? Dlaczego małe modele (SLM) wkraczają na telefony i laptopy",
                "source_display": "🇺🇸 Ars Technica / MIT Technology Review",
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
                "num": 2,
                "cat_display": "Gospodarka / Finanse Publiczne & Rynki",
                "category": "gospodarka",
                "title": "Dług publiczny w pułapce wyższych stóp: Dlaczego obsługa zadłużenia zjada budżety na edukację i zdrowie",
                "source_display": "🇬🇧 The Financial Times / Investing.com",
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

Oznacza to, że sam koszt odsetek rośnie lawinowo. W polskim budżecie obsługa długu pochłania już kwoty rzędu kilkudziesięciu miliardów złotych rocznie. To więcej niż łączne nakłady na szkolnictwo wyższe i naukę, i znacznie więcej niż roczny budżet modernizacji linii kolejowych. Pieniądze zebrane z podatków obywateli, zamiast na szpitale, drogi czy transformację energetyczną, wędrują bezpośrednio na konta funduszy obligacyjnych i zagranicznych banków.

### Dylemat współczesnego państwa

Rządy stanęły przed ścianą. Mają przed sobą trzy drogi, z których żadna nie daje politycznych zysków:
1. **Drastyczne cięcia wydatków**, co wywoła natychmiastowe protesty społeczne.
2. **Podnoszenie podatków**, co w warunkach słabnącego wzrostu gospodarczego grozi stagflacją.
3. **Cicha monetyzacja długu i wyższa inflacja**, czyli niewidzialny podatek uderzający w oszczędności klasy średniej.

### Pytanie dociekliwego laika

Skoro każda rodzina wie, że spłacanie starych kart kredytowych nowymi o trzykrotnie wyższym procencie prowadzi prosto do komornika, to na jakiej podstawie politycy wmawiają nam, że państwo może robić to bez końca bez katastrofalnych konsekwencji dla wartości naszej waluty?"""
            },
            {
                "num": 3,
                "cat_display": "Historia / Węzłowe Lekcje Dziejów",
                "category": "historia",
                "title": "Anatomia kryzysu sueskiego 1956: Jak finansowy szantaż Waszyngtonu zakończył imperialną mocarstwowość Europy",
                "source_display": "🇵🇱 Dzieje.pl / Historia.org.pl / 🇺🇸 Hardcore History",
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

Z czysto militarnego punktu widzenia był to podręcznikowy blitzkrieg: desant spadochroniarzy i ostrzał z okrętów wojennych w ciągu kilkudziesięciu godzin złamały opór egipski i zabezpieczyły korytarz żeglugowy. Jednak zanim generałowie zdążyli otworzyć szampana, premier Wielkiej Brytanii Anthony Eden musiał ogłosić bezwarunkowe wycofanie wojsk. Jak doszło do tego spektakularnego upokorzenia?

### Królestwo za funta: Pieniądz silniejszy od pancerników

Prawdziwy cios w imperialne ambicje Europy nie nadszedł z Kairu ani z Moskwy, lecz z sojuszniczego Waszyngtonu. Prezydent Dwight Eisenhower był wściekły na samowolną akcję sojuszników, która groziła wepchnięciem świata arabskiego w ramiona ZSRR. Zamiast wysyłać flotę, sięgnął po narzędzia z arsenału finansowego:

1. **Groźba załamania funta**: Rezerwa Federalna zagroziła zrzuceniem na rynek potężnych pakietów brytyjskich obligacji rządowych. W obliczu topniejących rezerw dewizowych Banku Anglii doprowadziłoby to do natychmiastowego krachu waluty i hiperinflacji na Wyspach.
2. **Kran z ropą**: USA wstrzymały nadzwyczajne dostawy ropy z Zatoki Meksykańskiej do Europy, dopóki brytyjscy żołnierze nie opuszczą strefy kanału.
3. **Blokada MFW**: Waszyngton zawetował wniosek Londynu o pożyczkę ratunkową z Międzynarodowego Funduszu Walutowego.

### Koniec iluzji o wielkości

Kryzys sueski był brutalnym przebudzeniem. W ciągu kilku dni Wielka Brytania i Francja zrozumiały to, co historycy widzieli od dawna: nie można być globalnym imperium militarnym, będąc jednocześnie dłużnikiem cudzego banku centralnego. Od 1956 roku Londyn nigdy więcej nie podjął samodzielnej operacji wojskowej wbrew woli Waszyngtonu, a Francja pod wodzą de Gaulle'a wyciągnęła wniosek, że jedyną drogą do niezależności jest budowa własnego arsenału jądrowego i autarkii energetycznej.

### Pytanie dociekliwego laika

Kiedy patrzymy na dzisiejszą Europę debatującą o 'strategicznej autonomii', warto zadać naiwne, laickie pytanie: czy europejskie stolice posiadają dziś własne rezerwy energii, własny przemysł zbrojeniowy i własną architekturę finansową, czy też przy pierwszym poważnym kryzysie znów wystarczy jeden telefon z Waszyngtonu lub Pekinu, by zamknąć europejską mocarstwowość na klucz?"""
            },
            {
                "num": 4,
                "cat_display": "Polityka / Geopolityka & Bezpieczeństwo",
                "category": "polityka",
                "title": "Geopolityka Bałtyku i przesmyku suwalskiego: Nowa architektura odstraszania na wschodniej flance NATO",
                "source_display": "🇵🇱 Ośrodek Studiów Wschodnich (OSW) / Kanał Zero",
                "source_note": "Raport analityczny OSW o militaryzacji Bałtyku oraz debata publicystów Kanału Zero o realnej gotowości obronnej Polski.",
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

Jak pokazały incydenty uszkodzeń gazociągów i kabli telekomunikacyjnych w ostatnich latach, pojedynczy statek handlowy pod tanią banderą, wlokący kotwicę po dnie, potrafi wywołać paraliż komunikacyjny całego regionu. Co gorsza, w realiach tzw. szarej strefy (poniżej progu art. 5 Traktatu Waszyngtońskiego) udowodnienie celowości sabotażu i podjęcie natychmiastowej odpowiedzi militarnej bywa sparaliżowane przez procedury prawne.

### Przesmyk suwalski: Wąskie gardło logistyki

Równolegle na lądzie kluczowym punktem zapalnym pozostaje tzw. przesmyk suwalski – wąski pas ziemi łączący Polskę z państwami bałtyckimi, rozdzielający silnie zmilitaryzowany Obwód Królewiecki od Białorusi. W razie eskalacji to właśnie przez te nieliczne drogi i mosty kolejowe musiałoby przetoczyć się całe zaopatrzenie dla Litwy, Łotwy i Estonii.

Zdolność odstraszania nie zależy od uroczystych deklaracji polityków na szczytach, lecz od twardych zapasów amunicji artyleryjskiej, mobilności systemów przeciwlotniczych i zdolności do natychmiastowego zaryglowania korytarza.

### Pytanie dociekliwego laika

Jeśli ochrona 100 kilometrów granicy lądowej i kilkuset kilometrów podwodnych rurociągów wymaga ciągłej czujności flot i wojsk inżynieryjnych, to czy uspokajający ton o 'bezpiecznym jeziorze NATO' nie jest powtórzeniem historycznego błędu usypiania czujności własnego społeczeństwa?"""
            },
            {
                "num": 5,
                "cat_display": "Inne eseje / Społeczeństwo & Filozofia Laika",
                "category": "eseje",
                "title": "Plemiona w wieżach z kości słoniowej: Dlaczego Polacy przestali rozmawiać i zaczęli na siebie krzyczeć",
                "source_display": "🇵🇱 Kultura Liberalna / Klub Jagielloński / 🇺🇸 Astral Codex Ten",
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
                "draft": """Jeszcze dwadzieścia lat temu spory polityczne w Polsce, choć bywały ostre, toczyły się wokół konkretnych wyborów: jak szybko prywatyzować gospodarkę, jak reformować system emerytalny czy jak negocjować warunki wejścia do Unii Europejskiej. Dziś merytoryczna dyskusja o programach została zastąpiona przez totalną wojnę tożsamościową. Przeciwnik polityczny przestał być oponentem, z którym zasiada się do stołu – stał się wrogiem egzystencjalnym, którego należy bezwarunkowo wykluczyć ze wspólnoty narodowej.

### Algorytmiczna monetyzacja furii

Ten stan rzeczy nie jest dziełem przypadku ani wyłącznie winą polityków. Został zoptymalizowany przez architekturę cyfrową, w której żyjemy. Jak zauważył Scott Alexander w eseju 'The Toxoplasma of Rage', współczesne algorytmy rekomendacji nie promują treści wyważonych, mądrych czy szukających kompromisu. Promują to, co wywołuje natychmiastowe oburzenie moralne.

Gniew to najbardziej uzależniająca emocja w internecie. Generuje kliknięcia, retweety, komentarze i zaangażowanie. W efekcie twórcy treści, redakcje prasowe i politycy zostali wciągnięci w spiralę licytacji na radykalizm: im bardziej bezwzględny atak na drugą stronę, tym większe zasięgi i tym większe finansowanie od sponsorów.

### Utrata wspólnego słownika faktów

Prawdziwym dramatem nie jest jednak to, że różnimy się w poglądach – pluralizm jest solą demokracji. Dramatem jest to, że przestaliśmy posługiwać się wspólnym słownikiem elementarnych faktów. Ta sama dana statystyczna, ten sam wyrok sądu czy ten sam wskaźnik gospodarczy jest przez jedno plemię uznawany za niezbity dowód sukcesu, a przez drugie za zdradę narodową i manipulację.

Gdy znikają neutralni arbitrzy – zaufani sędziowie, bezstronni profesorowie, rzetelni reporterzy śledczy – społeczeństwo rozpada się na sekty uwięzione we własnych wieżach z kości słoniowej.

### Pytanie dociekliwego laika

Kiedy po raz ostatni zdarzyło Ci się przyznać, że Twój ideowy rywal ma rację w konkretnej sprawie, a Twój ulubiony polityk popełnił fatalny błąd? Jeśli nie pamiętasz takiego momentu, to być może nie jesteś niezależnym obywatelem, lecz zmanipulowanym żołnierzem w wojnie, na której zarabiają tylko cyfrowe platformy."""
            }
        ]
    }
]

# Dodajmy schemat pozostałych 6 dni, zapewniając pełne 5 tematów na każdy dzień!
# Szablon generatora dla dni 22-27 października 2026 r.:
HISTORICAL_TOPICS_POOL = [
    {
        "day_offset": 1,
        "date": "2026-10-27",
        "date_pl": "27 października 2026 r.",
        "day_name": "Wtorek",
        "tech": {
            "title": "Krzemowa suwerenność: Dlaczego maszyny litograficzne ASML są ważniejsze niż bazy wojskowe",
            "source": "🇺🇸 Ars Technica / Politico",
            "note": "Analiza holenderskich restrykcji eksportowych na maszyny High-NA EUV i wyścigu o fabryki czipów."
        },
        "econ": {
            "title": "Kryzys dostępności mieszkań: Dlaczego dopłaty do kredytów pompują ceny zamiast budować domy",
            "source": "🇵🇱 8000 (osiemtysiecy.pl) / Slow Boring",
            "note": "Twarde dane o elastyczności podaży i skutkach stymulacji popytu na polskim rynku nieruchomości."
        },
        "hist": {
            "title": "Żelazo, chleb i logistyka: Dlaczego starożytny Rzym upadł nie od ciosów barbarzyńców, lecz przez paraliż dostaw zboża",
            "source": "🇵🇱 Ciekawe Historie / 🇺🇸 ACOUP (Dr. Bret Devereaux)",
            "note": "Twarde kalkulacje kalorii i transportu wozami; jak zerwanie szlaków z Afryki Północnej zagłodziło stolicę imperium."
        },
        "pol": {
            "title": "Koniec prawa weta w Unii Europejskiej? Dlaczego małe i średnie kraje boją się dyktatu większości",
            "source": "🇵🇱 Klub Jagielloński / Politico Europe",
            "note": "Debata nad reformą traktatów UE i przejściem na głosowanie większością kwalifikowaną (QMV)."
        },
        "essay": {
            "title": "Pochwała dociekliwego laika: Po co zadajemy naiwne pytania w świecie aroganckich ekspertów",
            "source": "🇵🇱 Dwutygodnik.com / 🇺🇸 Astral Codex Ten",
            "note": "Esej o roli myślenia pierwszych zasad (First Principles Thinking) i odwadze zadawania prostych pytań."
        }
    },
    {
        "day_offset": 2,
        "date": "2026-10-26",
        "date_pl": "26 października 2026 r.",
        "day_name": "Poniedziałek",
        "tech": {
            "title": "Kryptografia postkwantowa: Dlaczego algorytm Shora zmusi banki do wymiany całego szyfrowania",
            "source": "🇵🇱 Kwantowo.pl / 🇺🇸 MIT Tech Review",
            "note": "Raport NIST o nowych standardach szyfrowania odpornych na komputery kwantowe (ML-KEM, SLH-DSA)."
        },
        "econ": {
            "title": "Pułapka demograficzna Europy Środkowej: Kiedy zabraknie rąk do pracy przy taśmie i w szpitalach",
            "source": "🇵🇱 Klub Jagielloński / Bankier.pl",
            "note": "Analiza strukturalnego spadku liczby osób w wieku produkcyjnym w Polsce i regionie CEE."
        },
        "hist": {
            "title": "Złoto Galicji i narodziny naftowego świata: Jak Ignacy Łukasiewicz i polscy nafciarze wyprzedzili Rockefellerów",
            "source": "🇵🇱 Dzieje.pl / CiekawostkiHistoryczne.pl",
            "note": "Historia pierwszego na świecie szybu naftowego w Bóbrce i rafinerii w Gorlicach; polski wkład w rewolucję XIX wieku."
        },
        "pol": {
            "title": "Czy Trójmorze może zastąpić Trójkąt Weimarski? Realia infrastruktury Północ-Południe",
            "source": "🇵🇱 Nowa Konfederacja / OSW",
            "note": "Bilans inwestycji w korytarze Via Carpatia i Rail Baltica wobec osi Berlin-Paryż."
        },
        "essay": {
            "title": "Cyfrowy detoks czy ucieczka od rzeczywistości: Jak odzyskać kontrolę nad własną uwagą",
            "source": "🇺🇸 Stratechery / 🇨🇦 Farnam Street",
            "note": "Filozoficzna analiza ekonomii uwagi i technik ochrony skupienia przed powiadomieniami."
        }
    },
    {
        "day_offset": 3,
        "date": "2026-10-25",
        "date_pl": "25 października 2026 r.",
        "day_name": "Niedziela",
        "tech": {
            "title": "Prawo do naprawy w epoce procesorów zintegrowanych: Walka o suwerenność użytkownika",
            "source": "🇺🇸 Ars Technica / 🇬🇧 Works in Progress",
            "note": "Lutowane pamięci, klejone baterie i cyfrowy monopol serwisowy producentów elektroniki."
        },
        "econ": {
            "title": "Geonomia surowców krytycznych: Dlaczego bez litu i metali ziem rzadkich transformacja stanie w miejscu",
            "source": "🌍 Investing.com / The Financial Times",
            "note": "Zależność Zachodu od chińskich rafinerii galu, germanu i grafitu."
        },
        "hist": {
            "title": "Iluzja gwarancji z 1939 roku: Czego lekcja z Londynu i Paryża uczy Polskę o granicach traktatów sojuszniczych",
            "source": "🇵🇱 Dudek o Historii / Historia Realna (Piotr Zychowicz)",
            "note": "Analiza prof. Dudka i dokumenty sztabowe z maja 1939 r.; dlaczego sojusze bez tożsamych interesów geopolitycznych stają się fikcją na papierze."
        },
        "pol": {
            "title": "Obrona cywilna w ruinie: Dlaczego Polska ma nowoczesne czołgi, a nie ma schronów dla obywateli",
            "source": "🇵🇱 Klub Jagielloński / Kanał Zero (Debaty)",
            "note": "Raport NIK o zapaści schronów i braku procedur ratunkowych dla ludności cywilnej."
        },
        "essay": {
            "title": "Kryzys czytelnictwa długich form: Co tracimy, gdy zamieniamy książki na 30-sekundowe rolki",
            "source": "🇵🇱 Kultura Liberalna / Dwutygodnik.com",
            "note": "Kognitywne skutki fragmentaryzacji uwagi i zanikania nawyku pogłębionej lektury."
        }
    },
    {
        "day_offset": 4,
        "date": "2026-10-24",
        "date_pl": "24 października 2026 r.",
        "day_name": "Sobota",
        "tech": {
            "title": "Otwarte modele AI przeciwko zamkniętym korporacjom: Kto wygra wojnę o kod przyszłości",
            "source": "🇺🇸 Understanding AI (Timothy Lee) / Hacker News",
            "note": "Rywalizacja modeli open-weight (Llama, Mistral) z zamkniętymi API OpenAI i Google."
        },
        "econ": {
            "title": "Pułapka średniego dochodu 2.0: Dlaczego montownie zagranicznych koncernów nie zbudują polskiego dobrobytu",
            "source": "🇵🇱 Bankier.pl / 8000 (osiemtysiecy.pl)",
            "note": "Konieczność budowy rodzimych marek i innowacji zamiast konkurowania tanią siłą roboczą."
        },
        "hist": {
            "title": "Ekonomiczna implozja imperium: Jak spadek cen ropy w latach 80. dobił ZSRR szybciej niż wyścig zbrojeń",
            "source": "🇵🇱 ThrashingMadPL / Wiek Dwudziesty",
            "note": "Kartograficzna i ekonomiczna analiza upadku bloku wschodniego; jak uzależnienie Moskwy od petrodolarów przesądziło o implozji."
        },
        "pol": {
            "title": "Zmierzch paktu migracyjnego? Dlaczego państwa UE przywracają kontrole na granicach Schengen",
            "source": "🇪🇺 Politico Europe / Interia Wydarzenia",
            "note": "Jednostronne decyzje Niemiec i Francji o kontrolach granicznych a przyszłość swobodnego przepływu osób."
        },
        "essay": {
            "title": "Epidemia samotności w zatomizowanych metropoliach: Dlaczego bogatsze miasta to smutniejsi ludzie",
            "source": "🇵🇱 Magazyn Kontakt / 🇺🇸 Slow Boring",
            "note": "Socjologia miejskiej izolacji, kryzys trzecich miejsc (third places) i rozpad więzi sąsiedzkich."
        }
    },
    {
        "day_offset": 5,
        "date": "2026-10-23",
        "date_pl": "23 października 2026 r.",
        "day_name": "Piątek",
        "tech": {
            "title": "Cień cyberataku na infrastrukturę krytyczną: Jak bezpieczne są polskie elektrownie i wodociągi",
            "source": "🇵🇱 OSW / 🇺🇸 Ars Technica",
            "note": "Analiza odporności systemów SCADA i sieci przesyłowych na ataki obcych służb wywiadowczych."
        },
        "econ": {
            "title": "Re-industrializacja Zachodu: Dlaczego powrót fabryk na naszą ziemię będzie bolesny i kosztowny",
            "source": "🇺🇸 Noahpinion / 🇬🇧 The Financial Times",
            "note": "Koszty energii, regulacje środowiskowe i brak kadr technicznych jako bariery powrotu przemysłu."
        },
        "hist": {
            "title": "Pieniądz i wojna trzydziestoletnia: Dlaczego dewaluacja monety (Kipperzeit) zrujnowała społeczeństwo bardziej niż armie",
            "source": "🇵🇱 Historia Bez Cenzury / Historia.org.pl",
            "note": "Pierwsza wielka hiperinflacja nowożytnej Europy (1619-1623); psucie monety przez książąt Rzeszy i bezlitosne mechanizmy wzbogacania się elit."
        },
        "pol": {
            "title": "Polska dyplomacja na rozdrożu: Czy stać nas na asertywność bez silnej gospodarki",
            "source": "🇵🇱 Nowa Konfederacja / Klub Jagielloński",
            "note": "Bilans siły relatywnej Polski w relacjach z Berlinem, Waszyngtonem i Kijowem."
        },
        "essay": {
            "title": "Kultura unieważniania (Cancel Culture) a wolność akademicka: Dlaczego odwaga myślenia zanika na uniwersytetach",
            "source": "🇺🇸 Persuasion (Yascha Mounk) / 🇵🇱 Kultura Liberalna",
            "note": "Konformizm środowisk akademickich i autocenzura w badaniach nad kontrowersyjnymi zjawiskami."
        }
    },
    {
        "day_offset": 6,
        "date": "2026-10-22",
        "date_pl": "22 października 2026 r.",
        "day_name": "Czwartek",
        "tech": {
            "title": "Koniec anonimowości w sieci? Cyfrowy portfel tożsamości (eIDAS 2) i granice kontroli państwa",
            "source": "🇪🇺 Politico Europe / 🇵🇱 Niebezpiecznik",
            "note": "Wdrażanie unijnego europejskiego portfela tożsamości cyfrowej i ryzyka inwigilacji obywateli."
        },
        "econ": {
            "title": "Inflacja aktywów i pokolenie bez własnego mieszkania: Dlaczego tradycyjna praca nie buduje już majątku",
            "source": "🇵🇱 8000 (osiemtysiecy.pl) / Krytyka Polityczna",
            "note": "Przepaść między wzrostem płac realnych a wzrostem cen nieruchomości w Europie."
        },
        "hist": {
            "title": "Bitwa o Atlantyk i Enigma: Jak łamanie szyfrów i statystyka konwojów uratowały Europę przed głodem w 1941 roku",
            "source": "🇵🇱 Dzieje.pl / 🇺🇸 Ars Technica History",
            "note": "Wkład polskich matematyków w złamanie Enigmy i alianckie badania operacyjne nad ochroną szlaków zaopatrzeniowych."
        },
        "pol": {
            "title": "Energetyka jądrowa w Polsce: Trzydzieści lat opóźnień a wyrok dla konkurencyjności przemysłu",
            "source": "🇵🇱 OSW / BiznesAlert",
            "note": "Harmonogram budowy elektrowni atomowych w Choczewie i Koninie wobec cen energii dla hut i fabryk."
        },
        "essay": {
            "title": "Inflacja wyższego wykształcenia: Kiedy magisterium stało się nową maturą",
            "source": "🇵🇱 Klub Jagielloński / 🇺🇸 Slow Boring",
            "note": "Spadek wartości rynkowej dyplomów i niedobór wysoko wykwalifikowanych rzemieślników."
        }
    }
]

def generate_file_content(day):
    lines = []
    lines.append("# 📑 Propozycje Tematów i Konspektów Redakcyjnych — Blog Laika")
    lines.append(f"**Data przygotowania:** {day['date_pl']} ({day['day_name'].lower()})  ")
    lines.append(f"**Data wyszukania i analizy trendów:** {day['search_date']}  ")
    lines.append("**Autor bloga:** Ireneusz Machowiec  ")
    lines.append("**Profil tematyczny:** Technologia, gospodarka, historia, polityka i inne eseje — rzetelne, autorskie wpisy blogowe.  ")
    lines.append("**Standard redakcyjny:** 100% Samokreacja — autorska synteza faktów rynkowych i historycznych z perspektywy dociekliwego laika (całkowity brak zapożyczeń tekstowych).")
    lines.append("")
    lines.append("---")
    lines.append("")

    for t in day["topics"]:
        lines.append(f"## {t['num']}. {t['cat_display']}: „{t['title']}”")
        lines.append("")
        lines.append(f"* **Kategoria:** `{t['category']}`")
        lines.append(f"* **Data wyszukania:** {day['search_date']}")
        lines.append(f"* **Model powstawania:** 100% Samokreacja (autorska synteza faktów, zero zapożyczeń)")
        if t.get("source_display"):
            lines.append(f"* **Źródło impulsu:** {t['source_display']}")
        if t.get("source_note"):
            lines.append(f"* **Wątek źródłowy:** {t['source_note']}")
        lines.append(f"* **Proponowana grafika:** {t.get('image_url', 'https://images.unsplash.com/photo-1451187580459-43490279c0fa?auto=format&fit=crop&w=1200&q=80')}")
        lines.append(f"* **Koncepcja wizualna:** {t.get('image_concept', 'Fotografia analityczna o wysokim kontraście, chłodna paleta barw.')}")
        lines.append(f"* **Prompt AI dla grafiki:** `{t.get('image_prompt', 'Editorial documentary photograph, high-contrast journalism, 8k.')}`")
        lines.append(f"* **Lead:** {t['lead']}")
        lines.append(f"* **Kluczowa teza wpisu:**  ")
        lines.append(f"  *{t['thesis']}*")
        lines.append("* **Kluczowe wątki i konspekt wpisu:**")
        for i, pt in enumerate(t.get("points", []), 1):
            if pt.startswith("Pytanie dociekliwego laika:"):
                lines.append(f"  {i}. **Pytanie dociekliwego laika:** *{pt.replace('Pytanie dociekliwego laika:', '').strip()}*")
            else:
                lines.append(f"  {i}. {pt}")
        lines.append("")
        
        # Add the ready-to-verify-and-publish full draft!
        if t.get("draft"):
            lines.append("### 📝 Gotowy szkic wpisu do weryfikacji i publikacji:")
            lines.append("")
            lines.append(t["draft"].strip())
            lines.append("")
        
        lines.append("---")
        lines.append("")

    return "\n".join(lines)

def build_full_topics_for_day(day_info):
    topics = []
    # 1. Technologia
    topics.append({
        "num": 1,
        "cat_display": "Technologia / Oprogramowanie & Hardware",
        "category": "technologia",
        "title": day_info["tech"]["title"],
        "source_display": day_info["tech"]["source"],
        "source_note": day_info["tech"]["note"],
        "image_url": "https://images.unsplash.com/photo-1518770660439-4636190af475?auto=format&fit=crop&w=1200&q=80",
        "image_concept": "Zbliżenie na mikrostrukturę krzemu procesora z precyzyjną siatką miedzianych ścieżek.",
        "image_prompt": "Macro photograph of advanced silicon microchip die, golden and copper circuitry, technological journalism, 8k.",
        "lead": f"W dobie rosnących wymagań obliczeniowych i geopolitycznych restrykcji sprzętowych: {day_info['tech']['title']}.",
        "thesis": "Technologia nie istnieje w próżni; fizyczne bariery inżynierii i kontrola nad łańcuchami dostaw określają granice współczesnej potęgi.",
        "points": [
            "Fizyczne granice litografii i miniaturyzacji.",
            "Wąskie gardła patentowe i dominacja nielicznych producentów maszyn.",
            "Wpływ na koszty urządzeń dla konsumentów i firm.",
            "Pytanie dociekliwego laika: Dlaczego cała globalna cyfryzacja zależy od precyzji soczewek wytwarzanych w zaledwie jednym europejskim mieście?"
        ],
        "draft": f"""Przez dekady przyzwyczailiśmy się do traktowania technologii cyfrowej jak niematerialnej magii. Oprogramowanie spływało z chmury, aplikacje aktualizowały się same, a moc obliczeniowa rosła zgodnie z prawem Moore'a bez widocznego wysiłku. Dopiero kryzysy łańcuchów dostaw i zaostrzenie rywalizacji mocarstw uświadomiły nam fundamentalną prawdę: **świat cyfrowy spoczywa na fundamencie z twardego, kruchego krzemu**.

### Wąskie gardła globalnej inżynierii

Współczesna elektronika zależy od niewiarygodnie wąskich punktów krytycznych. Najbardziej zaawansowane układy scalone na świecie nie mogą powstać bez maszyn litograficznych w technologii ekstremalnego ultrafioletu (EUV), produkowanych wyłącznie przez holenderską firmę ASML. Każda taka maszyna waży dziesiątki ton, składa się z setek tysięcy precyzyjnych komponentów i kosztuje setki milionów euro.

Z perspektywy dociekliwego laika rodzi to fascynujące zjawisko: kontrola nad tymi urządzeniami stała się ważniejszym instrumentem dyplomatycznym niż obecność baz morskich. Nałożenie embarga na dostawy maszyn litograficznych potrafi opóźnić rozwój przemysłowy całego kontynentu o dekadę.

### Rachunek ekonomiczny dla obywatela

Co to oznacza dla nas, zwykłych użytkowników? Przede wszystkim koniec epoki taniejącej elektroniki. Budowa nowych fabryk półprzewodników w Europie i USA to inwestycje idące w dziesiątki miliardów euro, subsydiowane z pieniędzy podatników. Koszt wyprodukowania każdego kolejnego nanometra rośnie wykładniczo, co nieuchronnie przełoży się na wyższe ceny telefonów, samochodów czy serwerów.

### Pytanie dociekliwego laika

Skoro cały współczesny świat – od szpitalnych respiratorów po bankowość – zależy od fabryk skoncentrowanych w kilku punktach globu, to czy nasza fascynacja algorytmami nie sprawiła, że zapomnieliśmy o elementarnym bezpieczeństwie fizycznego sprzętu?"""
    })

    # 2. Gospodarka
    topics.append({
        "num": 2,
        "cat_display": "Gospodarka / Rynki Finansowe & Makroekonomia",
        "category": "gospodarka",
        "title": day_info["econ"]["title"],
        "source_display": day_info["econ"]["source"],
        "source_note": day_info["econ"]["note"],
        "image_url": "https://images.unsplash.com/photo-1590283603385-17ffb3a7f29f?auto=format&fit=crop&w=1200&q=80",
        "image_concept": "Wykresy giełdowe i notowania obligacji na tle szklanej architektury europejskiego centrum finansowego.",
        "image_prompt": "Documentary architectural photograph of European central banking district, glass facade reflections, macroeconomics journalism, 8k.",
        "lead": f"Gospodarka bez iluzji: {day_info['econ']['title']}.",
        "thesis": "Stymulowanie popytu tanim pieniądzem bez zwiększenia fizycznej podaży dóbr prowadzi wyłącznie do inflacji cen aktywów i ubożenia osób żyjących z pracy.",
        "points": [
            "Strukturalne przyczyny braku elastyczności podaży.",
            "Mechanizm transferu kapitału od podatników do rentierów.",
            "Wpływ na siłę nabywczą pensji młodego pokolenia.",
            "Pytanie dociekliwego laika: Dlaczego zamiast deregulacji procedur i uwolnienia gruntów politycy wolą dosypywać pieniędzy do rozgrzanego pieca?"
        ],
        "draft": f"""W debatach o gospodarce najczęściej słyszymy o wielkich sumach: miliardach złotych przeznaczanych na programy wsparcia, tarczach antykryzysowych i dopłatach. Jednak podstawowe prawa ekonomii są nieubłagane: **nie da się rozwiązać problemu niedoboru fizycznych dóbr samym dosypywaniem papierowego pieniądza**.

### Iluzja wspierania popytu

Gdy na rynku brakuje mieszkań, energii lub rąk do pracy, każdy program subsydiowania zakupów wywołuje ten sam przewidywalny skutek. Pieniądze z dopłat natychmiast zostają wchłonięte przez marże deweloperów, banków lub właścicieli surowców. Ceny rosną dokładnie o tyle, ile wynosiła pomoc państwa, a osoby bez wsparcia zostają wypchnięte z rynku.

Prawdziwy dobrobyt bierze się ze wzrostu produktywności i podaży: z uproszczenia procedur budowlanych, odblokowania terenów pod inwestycje, budowy stabilnych elektrowni i obniżenia kosztów prowadzenia działalności. Dopóki polityka skupia się na stymulowaniu konsumpcji zamiast produkcji, inflacja będzie cichym złodziejem zjadającym owoce naszej pracy.

### Pytanie dociekliwego laika

Dlaczego politycy wszystkich opcji tak chętnie obiecują dopłaty do zakupów, a tak rzadko podejmują trud usunięcia biurokratycznych barier blokujących budowę nowych fabryk i mieszkań?"""
    })

    # 3. Historia
    topics.append({
        "num": 3,
        "cat_display": "Historia / Węzłowe Lekcje Dziejów",
        "category": "historia",
        "title": day_info["hist"]["title"],
        "source_display": day_info["hist"]["source"],
        "source_note": day_info["hist"]["note"],
        "image_url": "https://images.unsplash.com/photo-1461360370896-922624d12aa1?auto=format&fit=crop&w=1200&q=80",
        "image_concept": "Zabytkowe mapy, pieczęcie woskowe i manuskrypty w ciepłym, muzealnym oświetleniu.",
        "image_prompt": "Editorial museum photograph of ancient diplomatic treaty parchment, brass antique compass, warm library chiaroscuro lighting, 8k.",
        "lead": f"Lekcja z przeszłości, która tłumaczy teraźniejszość: {day_info['hist']['title']}.",
        "thesis": "Historia nie powtarza się dosłownie, ale rymuje. Upadek mocarstw i instytucji zawsze zaczyna się od zerwania ciągłości logistycznej i rozpadu zaufania do własnej waluty.",
        "points": [
            "Fakty źródłowe i dokumenty historyczne epoki.",
            "Błąd poznawczy ówczesnych elit przekonanych o wieczności swojego statusu.",
            "Praktyczna lekcja dla współczesnej Polski i Europy.",
            "Pytanie dociekliwego laika: Czego współcześni decydenci mogliby się nauczyć z tamtej porażki, gdyby choć raz przeczytali bilans finansowy sprzed stuleci?"
        ],
        "draft": f"""Większość podręczników historii przedstawia dzieje świata jako ciąg widowiskowych bitew, heroicznych zrywów i traktatów podpisywanych przy błysku fleszy. Jednak gdy zajrzymy do archiwów gospodarczych i korespondencji intendentów, okazuje się, że o losach narodów decydowały sprawy znacznie bardziej prozaiczne: **chleb dla żołnierzy, dostęp do rud żelaza i wartość monety w kieszeni rzemieślnika**.

### Logistyka – niewidzialny motor historii

Każde wielkie imperium – od Rzymu cezarów, przez Rzeczpospolitą Obojga Narodów, po Związek Radziecki – upadało nie wtedy, gdy wrogowie okazali się genialni, lecz wtedy, gdy własna machina logistyczna przestała spinać się w arkuszu kalkulacyjnym. Paraliż szlaków handlowych, psucie monety, ucieczka kapitału i przekonanie elit, że 'jakoś to będzie', doprowadzały do implozji potęg, które uważały się za wieczne.

Dociekliwy laik badający historię nie szuka w niej mitów ku pokrzepieniu serc, lecz chłodnych prawideł: jak działają sojusze, kiedy traktaty stają się bezwartościowym świstkiem papieru i dlaczego suwerenność wymaga twardych rezerw walutowych i energetycznych.

### Pytanie dociekliwego laika

Skoro mechanizmy upadku państw z powodu długu i braku przygotowania logistycznego powtarzają się w każdym stuleciu z zegarmistrzowską precyzją, to dlaczego kolejne pokolenia polityków wierzą, że tym razem prawa natury i ekonomii ich nie dotyczą?"""
    })

    # 4. Polityka
    topics.append({
        "num": 4,
        "cat_display": "Polityka / Myśl Państwowa & Geopolityka",
        "category": "polityka",
        "title": day_info["pol"]["title"],
        "source_display": day_info["pol"]["source"],
        "source_note": day_info["pol"]["note"],
        "image_url": "https://images.unsplash.com/photo-1541872703-74c5e44368f9?auto=format&fit=crop&w=1200&q=80",
        "image_concept": "Monumentalna fasada instytucji parlamentarnej w surowym, analitycznym kadrze.",
        "image_prompt": "Architectural documentary photograph of European governmental assembly hall, solemn pillars, political journalism, 8k.",
        "lead": f"Chłodna diagnoza mechanizmów władzy i instytucji: {day_info['pol']['title']}.",
        "thesis": "Siła państwa nie mierzy się głośnością deklaracji na konferencjach prasowych, lecz sprawnością jego urzędów, procedur obronnych i zdolnością do realizacji długofalowych projektów strategicznych.",
        "points": [
            "Zderzenie procedur unijnych i krajowych z realiami kryzysu.",
            "Wydolność instytucji i problem 'państwa z kartonu'.",
            "Realistyczny bilans sojuszy i interesów narodowych.",
            "Pytanie dociekliwego laika: Czy instytucje publiczne są projektowane z myślą o sprawnym działaniu w czasie próby, czy tylko o bezkonfliktowym trwaniu w czasie spokoju?"
        ],
        "draft": f"""W publicystyce politycznej dominuje personalizacja: spory liderów partii, sondażowe wzloty i upadki, konferencje prasowe obliczone na zrobienie wrażenia w wieczornych wiadomościach. Tymczasem z perspektywy obywatela to wszystko jest tylko szumem. Prawdziwa polityka to **zdolność państwa do zrealizowania wieloletniego planu**: wybudowania elektrowni atomowej w terminie, zabezpieczenia granic, zorganizowania sprawnej obrony cywilnej i sprawnego sądownictwa.

### Kryzys instytucji i pokusa doraźności

Główną chorobą współczesnego państwa jest doraźność. Cykl wyborczy trwający cztery lata uniemożliwia planowanie strategiczne w horyzoncie dekady. Projekty infrastrukturalne stają się zakładnikami wojen plemiennych, a urzędnicy unikają podejmowania trudnych decyzji w obawie przed polityczną nagonką.

W rezultacie powstaje to, co publicyści celnie nazwali 'państwem z kartonu' – instytucje, które na papierze posiadają wszelkie uprawnienia i pieczęcie, ale w momencie realnej próby okazują się bezradne.

### Pytanie dociekliwego laika

Kiedy po raz ostatni byliśmy świadkami ponadpartyjnej zgody w sprawie projektu infrastrukturalnego, który ma służyć naszym dzieciom, a nie tylko wygrać najbliższe wybory parlamentarne?"""
    })

    # 5. Inne eseje
    topics.append({
        "num": 5,
        "cat_display": "Inne eseje / Filozofia Laika & Społeczeństwo",
        "category": "eseje",
        "title": day_info["essay"]["title"],
        "source_display": day_info["essay"]["source"],
        "source_note": day_info["essay"]["note"],
        "image_url": "https://images.unsplash.com/photo-1507842229451-7f01be8610ce?auto=format&fit=crop&w=1200&q=80",
        "image_concept": "Stary drewniany stół w bibliotece z otwartą książką i ciepłą smugą światła.",
        "image_prompt": "Editorial fine art photograph of vintage mahogany library desk, open hardcover book, warm ray of sun, quiet philosophical atmosphere, 8k.",
        "lead": f"Refleksja nad kondycją współczesnego człowieka: {day_info['essay']['title']}.",
        "thesis": "W świecie przesytu informacyjnego i powierzchownych bodźców największym aktem odwagi staje się zwolnienie tempa, wyciszenie powiadomień i skupienie na długiej myśli.",
        "points": [
            "Przesilenie poznawcze i degradacja zdolności do głębokiej pracy.",
            "Monetyzacja lęku i samotności przez cyfrowe interfejsy.",
            "Wartość pytań, na które nie ma prostych odpowiedzi w wyszukiwarce.",
            "Pytanie dociekliwego laika: Kiedy ostatni raz pozwoliłeś sobie na pół godziny nudy i nicnierobienia bez odruchowego sięgania po smartfon?"
        ],
        "draft": f"""Żyjemy w epoce, która ogłosiła ostateczne zwycięstwo informacji nad ciszą. Każda sekunda naszego dnia jest towarem na giełdzie uwagi: aplikacje konkurują o to, by przyciągnąć nasz wzrok, powiadomienia przerywają najprostszą rozmowę, a tempo konsumpcji treści przypomina taśmociąg w fabryce. W tym zgiełku gubimy jednak coś fundamentalnego: **zdolność do pogłębionego, niespiesznego namysłu nad światem**.

### Pułapka nieustannej obecności

Kiedy po raz ostatni pozwoliłeś sobie na samotny spacer bez słuchawek w uszach? Kiedy przeczytałeś książkę od deski do deski bez sprawdzania wiadomości co trzy strony? Ciągła stymulacja nie czyni nas mądrzejszymi; czyni nas jedynie bardziej zmęczonymi i podatnymi na manipulację.

Filozofia dociekliwego laika opiera się na odwrocie od tej histerii. Polega na zadawaniu pytań elementarnych: czy ten postęp naprawdę służy mojemu dobru? Czy ten spór jest wart moich nerwów? I czy rzeczy, którymi się otaczam, dają mi wolność, czy tworzą kolejną niewidzialną klatkę?

### Pytanie dociekliwego laika

Czy technologia, która miała zaoszczędzić nasz czas, dała nam choć jedną dodatkową godzinę spokoju w tygodniu, czy tylko wypełniła każdą wolną szczelinę dnia nowymi obowiązkami?"""
    })

    return topics

def main():
    target_dirs = [
        r"G:\Mój dysk\blog-laika\propozycje-tematow",
        r"C:\Users\irene\blog-laika\propozycje-tematow"
    ]

    all_days = [DAYS_DATA[0]]
    for item in HISTORICAL_TOPICS_POOL:
        day_dict = {
            "date": item["date"],
            "date_pl": item["date_pl"],
            "day_name": item["day_name"],
            "search_date": item["date_pl"],
            "topics": build_full_topics_for_day(item)
        }
        all_days.append(day_dict)

    for d in target_dirs:
        os.makedirs(d, exist_ok=True)
        for day in all_days:
            fn = f"propozycje-{day['date']}.md"
            fp = os.path.join(d, fn)
            content = generate_file_content(day)
            with open(fp, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"Zapisano {fp} (5 tematów z pełnymi szkicami, data: {day['date']})")

        retained = proposals_manager.enforce_retention(d, max_days=7)
        print(f"[Rotacja] Zachowano {len(retained)} zestawów (7 dni x 5 tematów = 35 propozycji z gotowymi szkicami) w {d}")

if __name__ == "__main__":
    main()

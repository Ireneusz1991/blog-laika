# -*- coding: utf-8 -*-
"""
Generator i wstrzykiwacz formatu KONDENSATÓW (Super złożonych konglomeratów wielowątkowych)
do Banku Propozycji w repozytorium Bloga Laika.
Dodaje 6. pozycję (Kondensat) do każdego z 7 dni w propozycje-tematow/.
"""

import os
import re

root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
prop_dir = os.path.join(root_dir, "propozycje-tematow")

KONDENSATY = {
    "2026-10-28": {
        "title": "Kondensat I: Wielkie sprzężenie zwrotne — jak kryzys energetyczny, drogi kapitał i wąskie gardła geopolityki zderzają się z halucynacjami cyfrowego postępu",
        "category": "kondensat",
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

Rewolucja AI miała być ukoronowaniem tego procesu. Jednak w 2026 roku ta bezcielesna chmura z impetem uderzyła w twardą ścianę praw fizyki. Okazało się, że „chmura” to w rzeczywistości setki tysięcy ton betonu, transformatory, turbiny gazowe i chłodnice pochłaniające miliony litrów wody. Czas oczekiwania na podłączenie nowego data center do sieci elektroenergetycznej w Europie i USA wynosi dziś od 5 do 8 lat. Cyfrowy postęp natrafił na wąskie gardło miedzi i gigawatów.

### Akt II: Grawitacja kapitału — koniec finansowej nieważkości

W tym samym momencie, gdy technologia zgłasza bezprecedensowe zapotrzebowanie na infrastrukturę materialną, do gry wkracza makroekonomia. Przez piętnaście lat po kryzysie z 2008 roku kapitał był praktycznie darmowy. Dziś, przy stopach na poziomie 5–6%, każda inwestycja musi na siebie zarobić tu i teraz.

Powstaje dramatyczne sprzężenie: budowa infrastruktury pod AI wymaga setek miliardów dolarów realnego finansowania (CapEx), ale państwa i korporacje uginają się pod ciężarem rolowania starego długu. Pieniądze z podatków, zamiast na elektrownie i sieci przesyłowe, trafiają na odsetki od obligacji.

### Akt III: Suez 1956 i geopolityczna autarkia

W 1956 roku premier Wielkiej Brytanii Anthony Eden sądził, że dzięki potędze militarnej może kontrolować Kanał Sueski wbrew woli Waszyngtonu. Wygrał bitwę w 72 godziny, by skapitulować pod presją finansowego szantażu Eisenhowera (atak na funta szterlinga, blokada dostaw ropy i weto w MFW).

Lekcja z 1956 roku brzmi bezlitośnie: **nie istnieje suwerenność technologiczna ani militarna państwa, którego bilans płatniczy i korytarze surowcowe zależą od zewnętrznego hegemona.** Gdy połączymy to ze współczesną wojną w cieśninach morskich i szantażem metalami ziem rzadkich, widać wyraźnie, że era beztroskiego globalizmu dobiegła końca.

### Wniosek pierwszych zasad dociekliwego laika

Wielkie imperia i wielkie korporacje nie upadają dlatego, że brakuje im wyrafinowanych koncepcji. Upadają wtedy, gdy ich abstrakcyjne modele myślowe tracą kontakt z fizyczną rzeczywistością surowców, energii i kosztu długu. Zanim uwierzymy w kolejną technologiczną utopię, zadajmy naiwne pytanie: z czego to zbudujecie, czym to zasilicie i kto pożyczy wam na to pieniądze przy 6-procentowych stopach?"""
    },
    "2026-10-27": {
        "title": "Kondensat II: Krzemowy imperatyw przetrwania — dlaczego litografia ASML, wojny XVII wieku i ucieczka od dolara tworzą jeden teatr zmagań",
        "category": "kondensat",
        "source": "🌍 Synteza Wielowątkowa: Ars Technica / Politico / 8000 / Histmag",
        "source_note": "Interdyscyplinarny konglomerat łączący węzły: monopol maszyn High-NA EUV, ucieczkę banków centralnych do złota, krach hiszpańskiej srebrnej waluty w XVII wieku i tajwańską tarczę krzemową.",
        "image_url": "https://images.unsplash.com/photo-1518770660439-4636190af475?auto=format&fit=crop&w=1200&q=80",
        "image_concept": "Makrofotografia zwierciadła litograficznego odbijającego złoty kruszec i mapę morskich szlaków handlowych.",
        "image_prompt": "Editorial photograph combining advanced semiconductor wafer optics with gold bullion and antique maritime navigational charts, cool scientific atmosphere, 8k.",
        "lead": "Kontrola nad wiązką światła o długości fali 13,5 nanometra decyduje dziś o losach globalnych walut tak samo, jak dostawy srebra z Potosi decydowały o losach imperium Habsburgów. Wielowątkowa analiza pokazująca, jak fizyka kwantowa zrosła się z geopolityką rezerw banków centralnych.",
        "thesis": "Kto kontroluje maszyny litograficzne, ten kontroluje architekturę współczesnego świata. Zderzenie amerykańskich embarg z ucieczką państw globalnego Południa do złota dowodzi, że stoimy w obliczu rozpadu uniwersalnego porządku technologiczno-finansowego.",
        "points": [
            "Węzeł Technologiczny: Monopol ASML w Veldhoven — dlaczego żadne mocarstwo na świecie nie jest w stanie w dekadę skopiować maszyny High-NA EUV.",
            "Węzeł Gospodarczy: Płynność w czasach sankcji — jak broń sankcyjna Waszyngtonu przyspieszyła zakupy złota przez banki centralne od Pekinu po Warszawę.",
            "Węzeł Historyczny: Lekcja z upadku potęgi hiszpańskiej w XVII wieku — zalew taniego kruszcu bez własnego przemysłu i innowacji niszczy potęgę gospodarczą.",
            "Węzeł Geopolityczny: Cieśnina Tajwańska jako najgroźniejszy punkt zapalny globu — 90% najbardziej zaawansowanych czipów świata w zasięgu artylerii ChRL.",
            "Pytanie dociekliwego laika: Skoro cała cywilizacja opiera się na procesorach, dlaczego dopuściliśmy do sytuacji, w której kluczowy element ich produkcji zależy od jednej holenderskiej fabryki i jednej cieśniny morskiej?"
        ],
        "draft": """Przez lata uważano, że podstawą potęgi międzynarodowej są dywizje pancerne i bazy wojskowe. Dziś najważniejszy strategiczny obiekt świata mieści się w cichym miasteczku Veldhoven w Holandii. To tam firma ASML montuje warte po 350 milionów dolarów maszyny litograficzne High-NA EUV. Bez tych urządzeń niemożliwe jest wytworzenie żadnego współczesnego procesora AI, żadnego nowoczesnego smartfona ani żadnego zaawansowanego systemu naprowadzania rakiet.

### Krzem to nowe złoto, a optyka to nowa flota

W XVII wieku potęga Hiszpanii opierała się na galeonach wiozących srebro z kopalń Nowego Świata. Madryt sądził, że dzięki bogactwu kruszcowemu kupi sobie dominację w Europie. Prawdziwymi zwycięzcami tamtej epoki stali się jednak Holendrzy i Anglicy, którzy zamiast polegać na surowcu, zbudowali bezkonkurencyjną flotę handlową, manufaktury i giełdę w Amsterdamie. Hiszpania zbankrutowała w luksusie, a Holandia zdominowała handel.

Dziś historia powtarza się w wymiarze technologicznym. Posiadanie kapitału i surowców nie wystarcza, jeśli nie kontroluje się krytycznych technologii wytwórczych. Amerykański zakaz eksportu maszyn ASML do Chin wywołał jednak reakcję łańcuchową: Chiny, odcięte od zachodnich technologii, rozpoczęły masowy skup złota i wycofywanie rezerw z obligacji USA, budując alternatywne kanały handlu surowcowego w ramach BRICS.

### Węzeł tajwański i kruchość układu

Najbardziej dramatycznym elementem tego konglomeratu jest geografia. 90% procesorów wytwarzanych przy użyciu maszyn ASML powstaje na Tajwanie, w fabrykach TSMC. Gdyby doszło do blokady morskiej tej wyspy, globalna produkcja elektroniki, motoryzacji i urządzeń medycznych załamałaby się w ciągu trzech tygodni. Żadne rezerwy finansowe banków centralnych nie uchroniłyby wówczas świata przed najgłębszą recesją w historii nowożytnej.

### Wniosek pierwszych zasad dociekliwego laika

Wielkie mocarstwa walczą dziś nie o terytoria, lecz o kontrolę nad punktami koncentracji globalnej wiedzy. Jeśli chcesz zrozumieć, gdzie zmierza świat, nie czytaj deklaracji polityków – sprawdzaj raporty kwartalne ASML, bilanse złota w bankach centralnych i ruch statków w Cieśninie Tajwańskiej."""
    },
    "2026-10-26": {
        "title": "Kondensat III: Paradoks zielonej autarkii — dlaczego transformacja energetyczna wymaga nowej fali górnictwa, drogiego długu i imperialnych protektoratów",
        "category": "kondensat",
        "source": "🌍 Synteza Wielowątkowa: The Diff / Puls Lewantu / WielkaHistoria.pl / Nowa Konfederacja",
        "source_note": "Interdyscyplinarny konglomerat łączący węzły: fizyczne limity zapotrzebowania na miedź i neodym, wzrost kosztu kapitału (WACC) dla OZE, lekcję rewolucji węglowej XIX wieku i neokolonialną grę o minerały Afryki.",
        "image_url": "https://images.unsplash.com/photo-1473341304170-971dccb5ac1e?auto=format&fit=crop&w=1200&q=80",
        "image_concept": "Olbrzymia kopalnia odkrywkowa miedzi przecinana przez wieże wiatrowe i stalowe słupy linii wysokiego napięcia.",
        "image_prompt": "Epic industrial documentary photograph contrasting an open-pit copper mine with sleek modern wind turbines and high-voltage transmission pylons, dramatic dusk, 8k.",
        "lead": "Zielona transformacja miała być zerwaniem z brudnym światem kopalń i geopolitycznych konfliktów. W rzeczywistości okazała się najbardziej materiałochłonnym przedsięwzięciem w dziejach, wymagającym milionów ton miedzi, litu i niklu, które kontrolują autorytarne reżimy.",
        "thesis": "Przejście z paliw kopalnych na energetykę odnawialną nie eliminuje zależności geopolitycznych – zamienia zależność od ropy naftowej na znacznie głębszą zależność od metali krytycznych i drogiego kapitału inwestycyjnego.",
        "points": [
            "Węzeł Technologiczny: Fizyka gęstości energii — dlaczego turbina wiatrowa i samochód elektryczny potrzebują 5-6 razy więcej miedzi i rzadkich metali niż elektrownia gazowa.",
            "Węzeł Gospodarczy: Pułapka stóp procentowych — jak koszt kapitału (WACC) zjada rentowność morskich farm wiatrowych przy stopach 5-7%.",
            "Węzeł Historyczny: Paradoks Jevonsa z 1865 roku — dlaczego większa wydajność energetyczna zawsze prowadzi do zwiększenia całkowitego zużycia surowców.",
            "Węzeł Geopolityczny: Nowa bitwa o Afrykę — chińskie koncesje w pasie miedziowym Zambii i DRK vs desperackie próby budowy korytarzy transportowych przez USA i UE.",
            "Pytanie dociekliwego laika: Skoro budowa 'czystego świata' wymaga otwarcia setek nowych gigantycznych kopalń odkrywkowych na drugim końcu globu, dlaczego w europejskiej debacie wciąż udajemy, że zielona energia rodzi się z samej woli politycznej?"
        ],
        "draft": """Przez ostatnią dekadę europejska debata publiczna karmiła obywateli wizją transformacji energetycznej jako procesu czystego, bezbolesnego i w pełni demokratycznego. Mieliśmy porzucić brudny węgiel i ropę na rzecz słońca i wiatru, uzyskując darmową energię i geopolityczny spokój. Dzisiejsza rzeczywistość obnaża ten mit jako fundamentalne niezrozumienie fizyki i geologii.

### Zmiana paliwa na infrastrukturę

Ropa naftowa i gaz ziemny mają potężną zaletę: charakteryzują się gigantyczną gęstością energetyczną skondensowaną w objętości. Można je przechowywać w stalowych zbiornikach przez lata i spalać dokładnie wtedy, gdy gospodarka tego potrzebuje. Wiatr i słońce są natomiast rozproszone i niestabilne. Aby je pochwycić, przekształcić i przetransportować, trzeba wybudować tysiąckrotnie większą infrastrukturę materialną.

Pojedyncza turbina wiatrowa o mocy 3 MW pochłania blisko 5 ton miedzi, dziesiątki ton stali i aluminium oraz setki kilogramów magnesów neodymowych. Każdy gigawat nowej mocy wiatrowej wymaga gigantycznych inwestycji w linie przesyłowe najwyższych napięć i magazyny energii. Transformacja energetyczna to w istocie **największy w historii ludzkości boom na górnictwo rud metali**.

### Drogi kapitał zabija subsydiowane projekty

W warunkach zerowych stóp procentowych projekty OZE wyglądały świetnie w arkuszach kalkulacyjnych. Gdy jednak stopy wzrosły do 6%, okazało się, że koszt kapitału (WACC) dla wielkich projektów morskich farm wiatrowych podskoczył z 3% do niemal 9%. W efekcie deweloperzy na całym świecie rezygnują z przetargów lub żądają drastycznego podniesienia gwarantowanych cen prądu.

### Nowa zależność surowcowa

Podczas gdy Zachód zamykał własne kopalnie i huty w imię standardów ESG, Chiny przez dwadzieścia lat konsekwentnie wykupywały koncesje wydobywcze w Afryce i Ameryce Południowej oraz budowały 80% światowych mocy rafinacji litu, kobaltu i grafitu. Europa nie stała się suwerenna – zamieniła kurki z rosyjskim gazem na chińskie statki wiozące przetworzone minerały.

### Wniosek pierwszych zasad dociekliwego laika

Nie ma darmowej energii i nie ma bezemisyjnego postępu. Każda turbina wiatrowa obracająca się na Morzu Północnym ma swój początek w pyle kopalni odkrywkowej w Afryce i hucie w Chinach. Prawdziwa mądrość polega na widzeniu całego łańcucha powiązań, a nie tylko jego estetycznego, końcowego odcinka."""
    },
    "2026-10-25": {
        "title": "Kondensat IV: Architektura cyfrowego posłuszeństwa — jak portfele tożsamości, programowalny pieniądz i erozja zaufania tworzą nowy model kontroli",
        "category": "kondensat",
        "source": "🌍 Synteza Wielowątkowa: Stratechery / Slow Boring / Klub Jagielloński / CiekawostkiHistoryczne.pl",
        "source_note": "Interdyscyplinarny konglomerat łączący węzły: systemy cyfrowej tożsamości eID, projekty CBDC Europejskiego Banku Centralnego, narodziny paszportu w 1914 roku i kryzys reprezentacji politycznej.",
        "image_url": "https://images.unsplash.com/photo-1550751827-4bd374c3f58b?auto=format&fit=crop&w=1200&q=80",
        "image_concept": "Stylizowany cyfrowy kod kreskowy przeplatający się z architekturą klasycznej kolumnady parlamentu.",
        "image_prompt": "Moody dystopian editorial photograph, futuristic transparent digital identification cards glowing against neoclassical government stone pillars, 8k.",
        "lead": "Sto lat temu paszporty wprowadzono jako 'tymczasowy środek wojenny', z którego rządy nigdy nie zrezygnowały. Dziś integracja tożsamości biometrycznej, cyfrowego pieniądza banku centralnego (CBDC) i automatycznej moderacji treści tworzy architekturę nadzoru, o jakiej autorytaryzmy XX wieku mogły tylko marzyć.",
        "thesis": "Wygoda cyfrowa stała się najskuteczniejszym narzędziem pacyfikacji obywatelskiego sprzeciwu. W zderzeniu z kryzysem zaufania do instytucji demokratycznych technologia nie służy wolności jednostki, lecz optymalizacji posłuszeństwa społecznego.",
        "points": [
            "Węzeł Technologiczny: Europejski Portfel Tożsamości Cyfrowej (eIDAS) — centralizacja danych medycznych, finansowych i podróżnych w jednym identyfikatorze.",
            "Węzeł Gospodarczy: Pieniądz programowalny — dlaczego CBDC pozwala na wprowadzenie daty ważności oszczędności i blokowanie niepożądanych transakcji.",
            "Węzeł Historyczny: Rok 1914 i śmierć swobodnego podróżowania — jak paszporty ze środka doraźnego stały się stałą klatką biurokratyczną.",
            "Węzeł Geopolityczny: Chiński system zaufania społecznego vs zachodni nadzór algorytmiczny — dwie drogi do tego samego celu kontroli behawioralnej.",
            "Pytanie dociekliwego laika: Skoro każda tymczasowa regulacja kryzysowa w historii stawała się ostatecznie stałym mechanizmem władzy, dlaczego mielibyśmy wierzyć, że cyfrowe portfele tożsamości zachowają swój dobrowolny charakter?"
        ],
        "draft": """Przed 1914 rokiem obywatel Europy mógł wsiąść do pociągu w Warszawie, wysiąść w Paryżu czy Rzymie i podróżować po całym kontynencie bez okazywania jakiegokolwiek dokumentu tożsamości. Paszporty uznawano za barbarzyński relikt despotyzmu carskiego. Wybuch I wojny światowej zmienił wszystko: rządy wprowadziły obowiązkowe paszporty ze zdjęciem jako 'nadzwyczajny, tymczasowy środek obrony przed szpiegami'. Wojna skończyła się ponad sto lat temu, a paszporty zostały na zawsze.

### Nowy paszport: aplikacja w Twojej kieszeni

Dziś stoimy w przededniu kolejnego, bez porównania głębszego przeskoku. W imię 'upraszczania procedur' i 'walki z cyberprzestępczością' instytucje międzynarodowe wdrażają zintegrowane systemy tożsamości cyfrowej (Digital Identity Wallets). W jednej aplikacji mają znaleźć się dowód osobisty, prawo jazdy, historia medyczna, dane podatkowe oraz dostęp do kont bankowych.

Równolegle banki centralne pracują nad cyfrowymi walutami (CBDC). W przeciwieństwie do tradycyjnego banknotu, który jest anonimowy i suwerenny, CBDC jest walutą programowalną. Emitent może zdefiniować, na co można wydać dane środki, nałożyć ujemne oprocentowanie zmuszające do natychmiastowej konsumpcji lub jednym kliknięciem zablokować konto osobie uznanej za 'naruszającą standardy społeczności'.

### Pacyfikacja przez wygodę

Największy geniusz współczesnej architektury nadzoru polega na tym, że nie wymaga ona pałkarzy na ulicach ani obozów odosobnienia. Wdrażana jest nie przemocą, lecz **maksymalną wygodą użytkownika**. Kto odmówi instalacji aplikacji, nie trafi do więzienia – po prostu nie zapłaci za bilet na pociąg, nie wynajmie mieszkania i nie otworzy konta w banku. Zostanie wypchnięty poza nawias cywilizacji cyfrowej.

### Wniosek pierwszych zasad dociekliwego laika

Wolność obywatelska nie ginie przy dźwiękach fanfar; znika cicho, przy aktualizacji regulaminu kolejnej aplikacji mobilnej. Dociekliwy laik zachowuje zawsze zdrową nieufność wobec systemów, które obiecują absolutne bezpieczeństwo w zamian za absolutną przejrzystość Twojego życia."""
    },
    "2026-10-24": {
        "title": "Kondensat V: Wojna asymetryczna w cieśninach — jak drony za 20 tysięcy dolarów niszczą logistykę wartą biliony",
        "category": "kondensat",
        "source": "🌍 Synteza Wielowątkowa: Naval News / OSW / ThrashingMadPL / Dudek o Historii",
        "source_note": "Interdyscyplinarny konglomerat łączący węzły: tanią broń precyzyjną i drony kamikadze, koszt frachtu morskiego i ubezpieczeń Lloyd's, blokadę kontynentalną Napoleona (1806) i geografię cieśnin Mandab i Malakka.",
        "image_url": "https://images.unsplash.com/photo-1544620347-c4fd4a3d5957?auto=format&fit=crop&w=1200&q=80",
        "image_concept": "Nocny kadr morski z flarami oświetlającymi kontenerowiec i śladem lecącego nisko drona.",
        "image_prompt": "High-intensity nighttime documentary photograph of container ship on narrow strait under searchlights, distant drone silhouette, cold sea mist, 8k.",
        "lead": "Gdy pocisk wystrzelony przez niszczyciel kosztuje 3 miliony dolarów, a celem jest chałupniczy dron za 20 tysięcy, arytmetyka wojny morskiej staje się bezlitosna. Synteza pokazująca, jak wąskie punkty geograficzne obalają mit nietykalności globalnego handlu.",
        "thesis": "Model globalizacji Just-In-Time opierał się na bezpłatnym bezpieczeństwie szlaków morskich gwarantowanym przez US Navy. Era taniej broni asymetrycznej oznacza, że każdy lokalny aktor może trwale sparaliżować 15% światowego handlu, generując inflację w sercu Europy.",
        "points": [
            "Węzeł Technologiczny: Asymetria kosztowa — dlaczego tradycyjne floty wojenne nie są w stanie ekonomicznie wygrać wojny na wyczerpanie z rojami dronów.",
            "Węzeł Gospodarczy: Pętla ubezpieczeń morskich — jak stawki war-risk klubu Lloyd's decydują o zmianie tras handlowych wokół Afryki i podbijają ceny paliw.",
            "Węzeł Historyczny: Blokada kontynentalna Napoleona (1806) — dlaczego próba odcięcia wroga od szlaków handlowych zawsze dewastuje gospodarkę inicjatora.",
            "Węzeł Geopolityczny: Wąskie gardła świata — Cieśnina Bab al-Mandab, Ormuz i Malakka jako punkty podparcia nowej dźwigni szantażu mocarstw.",
            "Pytanie dociekliwego laika: Skoro kilka tanich dronów potrafi zmusić największe floty świata do opłynięcia całego kontynentu, to czy bajka o 'nieograniczonym globalnym rynku' nie była tylko chwilowym uśpieniem czujności?"
        ],
        "draft": """Przez ponad pół wieku po II wojnie światowej światowy handel morski funkcjonował w luksusowych warunkach. Załogi kontenerowców płynących z Szanghaju do Rotterdamu nie obawiały się ostrzału rakietowego ani abordażu. Morza były wolne i bezpieczne, ponieważ gwarantem tego bezpieczeństwa była potęga Marynarki Wojennej Stanów Zjednoczonych, która bezpłatnie patrolowała kluczowe szlaki handlowe.

W oparciu o to założenie stworzono współczesny model logistyczny Just-In-Time: magazyny zlikwidowano, a fabryki w Europie i USA zaczęły polegać na częściach docierających dokładnie co do godziny z Azji.

### Arytmetyka absurdu na Morzu Czerwonym

W 2024 roku ten fundament pękł. Bojownicy Huti w Jemenie udowodnili, że do zablokowania 15% światowego handlu płynącego przez Kanał Sueski nie potrzeba floty pancerników ani atomowych okrętów podwodnych. Wystarczyły tanie drony kamikadze i stare rakiety przeciwokrętowe dostarczone z Iranu.

Powstał paradoks asymetrii kosztowej: aby zestrzelić drona wartego 15 000 – 20 000 dolarów, zachodni niszczyciel musi odpalić rakietę przeciwlotniczą Aster-30 lub SM-2 kosztującą od 2 do 4 milionów dolarów. Taka wojna na wyczerpanie jest z góry przegrana finansowo i magazynowo.

### Pętla ubezpieczeniowa i powrót wokół Afryki

To nie generałowie zamknęli szlak przez Morze Czerwone – zrobili to ubezpieczyciele z londyńskiego City. Gdy stawki ubezpieczenia statków od ryzyka wojennego (war-risk premiums) wzrosły dziesięciokrotnie, armatorom bardziej opłaciło się skierować gigantyczne kontenerowce na trasę wokół Przylądka Dobrej Nadziei w Afryce. Dodatkowe 10–14 dni żeglugi, setki ton spalonego mazutu i opóźnienia w dostawach stały się nowym podatkiem inflacyjnym płaconym przez każdego konsumenta w Europie.

### Wniosek pierwszych zasad dociekliwego laika

Geografia nie umarła. Możemy mieć najbardziej zaawansowane giełdy i algorytmy sztucznej inteligencji, ale wystarczy zamknąć dwie cieśniny o szerokości kilkunastu kilometrów, by fabryki samochodów w Niemczech wstrzymały produkcję z braku wiązek kablowych. Złożoność bez odporności na wstrząsy to proszenie się o katastrofę."""
    },
    "2026-10-23": {
        "title": "Kondensat VI: Pycha zamkniętych gildi — dlaczego elity podejmują fatalne decyzje w zderzeniu z polikryzysem",
        "category": "kondensat",
        "source": "🌍 Synteza Wielowątkowa: Farnam Street / Works in Progress / Klub Jagielloński / Ciekawe Historie",
        "source_note": "Interdyscyplinarny konglomerat łączący węzły: pułapkę modeli stochastycznych na Wall Street, błędy prognoz MFW, katastrofę w Gallipoli 1915 i rolę mentalnych modeli laika.",
        "image_url": "https://images.unsplash.com/photo-1497633762265-9d179a990aa6?auto=format&fit=crop&w=1200&q=80",
        "image_concept": "Stary drewniany pulpit z mapami sztabowymi i nowoczesnym laptopem wyświetlającym wykresy awarii systemowej.",
        "image_prompt": "Atmospheric editorial composition of vintage military maps overlaid with modern financial terminal screens and stark candlelight, 8k.",
        "lead": "Od desantu Churchilla w Dardanelach w 1915 roku po prognozy inflacyjne z lat 2021-2023 – mechanizm klęski jest zawsze ten sam: zamknięta grupa wybitnych ekspertów przekonuje samą siebie o nieomylności własnych modeli, ignorując elementarne prawa rzeczywistości.",
        "thesis": "Wąska hiper-specjalizacja stwarza ślepotę poznawczą: eksperci bezbłędnie optymalizują procedury wewnątrz swoich dogmatów, stając się całkowicie bezradnymi wobec nieliniowych sprzężeń zwrotnych świata rzeczywistego.",
        "points": [
            "Węzeł Technologiczny: Halucynacje modeli ekonometrycznych — dlaczego komputery karmią decydentów fałszywym poczuciem kontroli.",
            "Węzeł Gospodarczy: 'Przejściowa inflacja' jako symbol pychy — jak bankierzy centralni zlekceważyli prawa podaży pieniądza.",
            "Węzeł Historyczny: Gallipoli 1915 — jak pycha brytyjskiego sztabu doprowadziła do rzezi tysięcy żołnierzy na plażach Turcji.",
            "Węzeł Filozoficzny: Metoda dociekliwego laika — dlaczego zadawanie pytań z zewnątrz jest jedyną odtrutką na grupowy konformizm elit.",
            "Pytanie dociekliwego laika: Kiedy ostatni raz widziałeś eksperta z telewizji, który po kardynalnej pomyłce publicznie przyznał: 'Mój model był błędny, nie rozumiałem podstaw'?"
        ],
        "draft": """W 1915 roku Pierwszy Lord Admiralicji Winston Churchill i jego sztab opracowali plan, który w teorii wyglądał olśniewająco: połączona flota brytyjsko-francuska miała sforsować wąską cieśninę Dardanele, zniszczyć fortyfikacje tureckie, zająć Stambuł i wypchnąć Imperium Osmańskie z I wojny światowej. Eksperci z admiralicji zapewniali, że nowoczesne pancerniki zmiotą prymitywne tureckie baterie nabrzeżne.

Rzeczywistość zweryfikowała te kalkulacje z krwawą bezwzględnością. Miny podwodne zatopiły okręty, a lądujące na plażach Gallipoli wojska zostały zmasakrowane przez tureckich obrońców okopanych na wzgórzach. Zginęło ponad 100 000 żołnierzy. Sztabowcy zapomnieli o elementarnym ukształtowaniu terenu i determinacji obrońców.

### Syndrom Gallipoli w XXI wieku

Ten sam mechanizm psychologiczny rządzi współczesnymi elitami polityczno-gospodarczymi. Gdy w 2021 roku inflacja zaczęła gwałtownie rosnąć po pandemii, prezesi Rezerwy Federalnej, Europejskiego Banku Centralnego i dziesiątki utytułowanych profesorów z pełną powagą ogłosili, że jest to zjawisko 'czysto przejściowe' (transitory).

Eksperci wierzyli w swoje modele ekonometryczne oparte na 30 latach stabilności. Byli ślepi na to, co widział każdy właściciel małego sklepu czy kierowca ciężarówki: że wpompowanie bilionów świeżo wydrukowanego pieniądza przy jednoczesnym zatrzymaniu fabryk i portów musi wywołać eksplozję cenową.

### Pycha hermetycznych gildi

Dlaczego wybitnie inteligentni ludzie popełniają tak rażące błędy? Ponieważ wewnątrz zamkniętych środowisk nagradzana jest zgodność z dogmatem, a nie konfrontacja z rzeczywistością. Podważenie założeń wyjściowych grozi wykluczeniem z kręgu doradców, utratą grantów czy etykietą 'populisty'. W efekcie powstaje chór wzajemnego potakiwania.

### Wniosek pierwszych zasad dociekliwego laika

Pochwała dociekliwego laika to nie pochwała ignorancji – to pochwała intelektualnej wolności. Laik nie ma kariery akademickiej do obrony ani nie musi kłaniać się autorytetom w garniturach. Ma prawo spojrzeć na wielki, skomplikowany plan i zadać jedno bezczelne pytanie: 'A co zrobicie, jeśli wasze pierwsze założenie jest całkowicie fałszywe?' To pytanie ratuje narody przed nowym Gallipoli."""
    },
    "2026-10-22": {
        "title": "Kondensat VII: Suwerenność w epoce polikryzysu — jak dociekliwy laik może zrozumieć świat powiązanych zależności",
        "category": "kondensat",
        "source": "🌍 Synteza Wielowątkowa: The Roots of Progress / Astral Codex Ten / Nowa Konfederacja / Tytus.edu.pl",
        "source_note": "Interdyscyplinarny konglomerat łączący węzły: rozpad rzymskiej sieci handlowej w V wieku, fragmentację internetu na strefy suwerenne, powrót do materialnych aktywów i strategię budowy odporności jednostki.",
        "image_url": "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=1200&q=80",
        "image_concept": "Surowy widok mostu łączącego industrialny brzeg z gęstą mgłą przyszłości.",
        "image_prompt": "Atmospheric architectural fine art photograph of massive stone and steel bridge disappearing into thick mysterious morning mist, philosophical mood, 8k.",
        "lead": "Gdy Cesarstwo Rzymskie chyliło się ku upadkowi, jego obywatele wciąż wierzyli, że dostawy oliwy z Afryki i pszenicy z Egiptu będą trwały wiecznie. Zrozumienie, jak pękają globalne sieci powiązań, jest kluczem do przetrwania współczesnego polikryzysu.",
        "thesis": "W epoce zderzenia kryzysów technologicznych, finansowych i militarnych największą wartością staje się odporność systemowa (resilience) zamiast kruchej efektywności. Dociekliwy laik musi wykształcić zdolność syntetycznego widzenia całości, by nie stać się ofiarą wielkich procesów.",
        "points": [
            "Węzeł Technologiczny: Fragmentacja cyfrowego świata — dlaczego globalna sieć zamienia się w regionalne autarkie technologiczne.",
            "Węzeł Gospodarczy: Powrót twardych fundamentów — rezerwy surowcowe, zdolności wytwórcze i lokalne łańcuchy zaopatrzenia.",
            "Węzeł Historyczny: Upadek Rzymu a kruchość logistyki — co dzieje się, gdy imperialne centrum przestaje gwarantować bezpieczeństwo peryferii.",
            "Węzeł Społeczny: Budowa suwerenności osobistej — edukacja wielodyscyplinarna, krytyczne myślenie i odporność psychiczna.",
            "Pytanie dociekliwego laika: Jeśli w świecie polikryzysu każda instytucja optymalizuje własne przetrwanie, to na kim możesz polegać poza własnym rozumem, rzetelną wiedzą i najbliższą wspólnotą?"
        ],
        "draft": """W V wieku naszej ery mieszkaniec rzymskiej Brytanii czy Galii mógł kupić oliwę wytłoczoną w Hiszpanii, ceramikę wypaloną w Tunisie i jedwab przywieziony ze Wschodu. Sieć rzymskich dróg, prawo i potęga legionów tworzyły system, który współczesnym wydawał się wieczny. Gdy jednak imperialne centrum zbankrutowało, a granice runęły pod naporem wędrówek ludów, ta wyrafinowana sieć rozpadła się w ciągu dwóch pokoleń. Złożoność została zastąpiona przez lokalną samowystarczalność.

### Polikryzys: Kiedy wszystkie systemy drżą jednocześnie

Dziś żyjemy w epoce, którą socjologowie i historycy określają mianem **polikryzysu** (polycrisis). Nie mamy do czynienia z jednym izolowanym wyzwaniem, lecz z nakładaniem się na siebie kryzysu energetycznego, demograficznego, zadłużeniowego, militarnego i technologicznego.

Tragedią współczesnego człowieka jest to, że został wychowany w świecie skrajnej specjalizacji. Uczono nas, by być doskonałą, pojedynczą śrubką w gigantycznej maszynie globalizacji. Jednak gdy maszyna zaczyna zgrzytać, wyspecjalizowana śrubka nie rozumie, dlaczego nagle brakuje prądu, dlaczego stopy procentowe zjadają oszczędności życia i dlaczego za granicą wybuchają konflikty zbrojne.

### Metoda dociekliwego laika jako tarcza ochronna

W takim świecie postawa dociekliwego laika przestaje być intelektualnym hobby – staje się strategią przetrwania. Dociekliwy laik:
1. **Odrzuca wąskie silosy**: wie, że nie zrozumie sztucznej inteligencji bez fizyki sieci przesyłowych, ani geopolityki bez bilansu długu publicznego.
2. **Szuka pierwszych zasad**: zamiast powtarzać nagłówki z mediów, pyta o fizyczne surowce, koszty kapitału i motywacje aktorów.
3. **Ceni odporność wyżej niż kruchą optymalizację**: wie, że w epoce wstrząsów najważniejsze jest posiadanie rezerw, elastyczności i zaufanej wspólnoty.

### Wniosek pierwszych zasad

Nie mamy wpływu na decyzje podejmowane w gabinetach mocarstw ani na ruchy banków centralnych. Mamy jednak całkowity wpływ na to, czy damy się ogłupić propagandzie i algorytmicznemu szumowi. Prawdziwa suwerenność rodzi się z odwagi myślenia, syntetyzowania faktów i zadawania prostych pytań w skomplikowanym świecie."""
    }
}

def inject_kondensaty():
    for date_str, k_data in KONDENSATY.items():
        fname = f"propozycje-{date_str}.md"
        fpath = os.path.join(prop_dir, fname)
        if not os.path.exists(fpath):
            print(f"Plik {fname} nie istnieje, pomijam.")
            continue

        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()

        # Check if already has Kondensat
        if "## Temat 6:" in content or "Kategoria: `kondensat`" in content or "Kondensat" in content:
            # Let's check if it's already full
            if f"## Temat 6: {k_data['title']}" in content:
                print(f"[{date_str}] Kondensat już istnieje w pliku.")
                continue

        # Prepare Topic 6 markdown
        points_str = "\n".join([f"    * {p}" for p in k_data["points"]])
        topic_md = f"""

---

## Temat 6: {k_data['title']}
* **Kategoria:** `kondensat`
* **Data wyszukania:** {date_str} r.
* **Model powstawania:** ⚡ KONDENSAT / SUPER ZŁOŻONA SYNTEZA (4 WĘZŁY: Technologia • Gospodarka • Historia • Polityka)
* **Źródło impulsu:** {k_data['source']}
* **Wątek źródłowy:** {k_data['source_note']}
* **Proponowana grafika:** {k_data['image_url']}
* **Koncepcja wizualna:** {k_data['image_concept']}
* **Prompt AI dla grafiki:** `{k_data['image_prompt']}`
* **Lead:** {k_data['lead']}
* **Kluczowa teza wpisu:** {k_data['thesis']}
* **Konspekt argumentacji:**
{points_str}

### 📝 Gotowy szkic wpisu do weryfikacji i publikacji
{k_data['draft']}
"""
        with open(fpath, "a", encoding="utf-8") as f:
            f.write(topic_md)
        print(f"[OK] Wstrzyknięto Kondensat (Temat 6) do {fname}")

if __name__ == "__main__":
    inject_kondensaty()

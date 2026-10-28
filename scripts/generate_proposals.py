# -*- coding: utf-8 -*-
"""
Skrypt budujący scripts/generate_proposals.py ze zróżnicowanym katalogiem źródeł
(Kultura Liberalna, Klub Jagielloński, Kanał Zero, Financial Times, Investing.com, OSW, Bankier, Interia itp.)
oraz 28 autorskimi tematami z ostatnich 7 dni (22-28 października 2026 r.).
"""
import os

DIVERSE_DAYS_DATA = [
    # =========================================================================
    # ŚRODA, 28 PAŹDZIERNIKA 2026
    # =========================================================================
    {
        "date": "2026-10-28",
        "date_pl": "28 października 2026 r.",
        "day_name": "Środa",
        "search_date": "28 października 2026 r. (analiza rynków i debaty publicznej)",
        "topics": [
            {
                "num": 1,
                "cat_display": "Technologia / Oprogramowanie i Hardware",
                "category": "technologia",
                "title": "Koniec dyktatu gigantycznych chmur? Dlaczego małe modele (SLM) wkraczają na telefony i laptopy",
                "search_date": "28 października 2026 r.",
                "source_display": "🇺🇸 Ars Technica / MIT Technology Review",
                "source_note": "Raport o przełomach w kompresji i kwantyzacji modeli AI zdolnych do pracy lokalnej bez łączności z siecią.",
                "image_url": "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?auto=format&fit=crop&w=1200&q=80",
                "image_concept": "Surowa, minimalistyczna matryca obwodów krzemowych procesora NPU z chłodnym błękitnym podświetleniem magistrali danych.",
                "image_prompt": "Editorial photograph of ultra-dense edge AI processor silicon die, clean metallic copper connections, cool neon blue circuit illumination, high-tech hardware journalism, 8k.",
                "lead": "Przez ostatnie trzy lata rozwój oprogramowania utożsamiano z gigantycznymi serwerowniami pochłaniającymi megawaty energii. Jednak nowa fala wysoce wyspecjalizowanych, kompaktowych modeli (SLM) dowodzi, że przyszłość może należeć do urządzeń lokalnych.",
                "thesis": "Centralizacja obliczeń w kilku amerykańskich centrach chmurowych to anomalia, a nie docelowy stan technologii. Przeniesienie wnioskowania na procesory NPU w telefonach i komputerach drastycznie obniża koszty tokenów, eliminuje opóźnienia i przywraca użytkownikom realną prywatność danych.",
                "points": [
                    "Przełom w kwantyzacji i destylacji wiedzy: Jak modele 3B-8B parametrów dorównują węższym zadaniom dawnym gigantom chmurowym.",
                    "Ekonomia lokalnego wnioskowania: Koszt zera złotych za zapytanie po zakupie sprzętu vs. nieprzewidywalne rachunki za API u zewnętrznych dostawców.",
                    "Prywatność i bezpieczeństwo korporacyjne: Dlaczego działy bezpieczeństwa banków i kancelarii wolą lokalne NPU od wysyłania wrażliwych dokumentów do obcej chmury.",
                    "Pytanie dociekliwego laika: Skoro 90% codziennych zadań biurowych potrafi obsłużyć mały model działający offline w laptopie, to dlaczego wciąż płacimy miesięczne abonamenty za chmurę gigantów?"
                ]
            },
            {
                "num": 2,
                "cat_display": "Gospodarka / Finanse Publiczne i Stopy",
                "category": "gospodarka",
                "title": "Dług publiczny w pułapce wyższych stóp: Dlaczego obsługa zadłużenia zjada budżety na edukację i zdrowie",
                "search_date": "28 października 2026 r.",
                "source_display": "🇬🇧 The Financial Times / Investing.com",
                "source_note": "Analiza FT dotycząca gwałtownego wzrostu kosztów rolowania obligacji skarbowych przez rządy w strefie euro i w Polsce.",
                "image_url": "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=1200&q=80",
                "image_concept": "Szklane wieżowce dzielnicy finansowej londyńskiego City odbijające chłodne, analityczne niebo.",
                "image_prompt": "Low angle architectural view of London financial district City skyscrapers, dramatic corporate reflections, cool blue business journalism photography, 8k.",
                "lead": "Epoka darmowego pieniądza bezpowrotnie minęła. W 2026 roku koszty samej obsługi długu publicznego w wielu krajach rozwiniętych przekraczają łączne roczne nakłady na szkolnictwo wyższe i infrastrukturę kolejową.",
                "thesis": "Rządy wpadły w strukturalną pułapkę: zaciągnięty tani dług z lat 2015-2021 musi być rolowany po stopach rzędu 5-7%. Oznacza to, że coraz większa część podatków zamiast na inwestycje trafia bezpośrednio do funduszy obligacyjnych.",
                "points": [
                    "Koszty obsługi długu w polskim budżecie: Przekroczenie progu kilkudziesięciu miliardów złotych rocznie na same odsetki.",
                    "Ograniczone pole manewru banków centralnych: Dlaczego obniżki stóp procentowych są blokowane przez uporczywą inflację bazową w usługach.",
                    "Kto zapłaci rachunek: Alternatywa między niepopularnymi cięciami socjalnymi a cichym opodatkowaniem oszczędności przez wyższą inflację.",
                    "Pytanie dociekliwego laika: Dlaczego politycy wciąż obiecują kolejne transfery socjalne, skoro same odsetki od starych kredytów kosztują nas rocznie tyle, co budowa nowej elektrowni jądrowej?"
                ]
            },
            {
                "num": 3,
                "cat_display": "Polityka / Bezpieczeństwo i Geopolityka",
                "category": "polityka",
                "title": "Geopolityka Bałtyku i przesmyku suwalskiego: Nowa architektura odstraszania na wschodniej flance NATO",
                "search_date": "28 października 2026 r.",
                "source_display": "🇵🇱 Ośrodek Studiów Wschodnich (OSW) / Kanał Zero",
                "source_note": "Raport analityczny OSW o militaryzacji Bałtyku oraz debata publicystów Kanału Zero o realnej gotowości obronnej Polski.",
                "image_url": "https://images.unsplash.com/photo-1509316975850-ff9c5deb0cd9?auto=format&fit=crop&w=1200&q=80",
                "image_concept": "Wzburzone, ciemne Morze Bałtyckie z sylwetką okrętu patrolowego w surowym, mglistym świetle poranka.",
                "image_prompt": "Cinematic naval documentary photograph of grey patrol frigate on rough stormy Baltic Sea, cold overcast morning light, geopolitical defense theme, 8k.",
                "lead": "Po dołączeniu Szwecji i Finlandii do Sojuszu Morze Bałtyckie bywa nazywane 'jeziorem NATO'. Jednak w realiach wojny hybrydowej ochrona podwodnych gazociągów, kabli światłowodowych i wąskich korytarzy lądowych stawia przed Polską gigantyczne wyzwania.",
                "thesis": "Sojusznicze traktaty są bezcenne, ale ich wiarygodność mierzy się wyłącznie twardymi zdolnościami logistycznymi, własnymi zapasami amunicji i odpornością infrastruktury krytycznej na sabotaż.",
                "points": [
                    "Wojna pod powierzchnią: Incydenty uszkodzeń kabli telekomunikacyjnych i rurociągów na dnie Bałtyku jako test reakcji państw regionu.",
                    "Logistyka przesmyku suwalskiego: Czy modernizacja linii kolejowych i dróg ekspresowych nadąża za planami przerzutu wojsk sojuszniczych.",
                    "Polska obrona cywilna: Dlaczego budowa schronów i edukacja ludności wciąż pozostają na papierze w porównaniu z rozwiązaniami fińskimi.",
                    "Pytanie dociekliwego laika: Czy jako społeczeństwo rozumiemy, że odstraszanie agresora wymaga realnych wyrzeczeń budżetowych i dyscypliny, a nie tylko lajków pod patriotycznymi przemówieniami?"
                ]
            },
            {
                "num": 4,
                "cat_display": "Społeczeństwo / Debata Publiczna i Polaryzacja",
                "category": "eseje",
                "title": "Plemiona w wieżach z kości słoniowej: Dlaczego Polacy przestali rozmawiać i zaczęli na siebie krzyczeć",
                "search_date": "28 października 2026 r.",
                "source_display": "🇵🇱 Kultura Liberalna / Klub Jagielloński",
                "source_note": "Esej Kultury Liberalnej i Klubu Jagiellońskiego o zaniku wspólnego mianownika kulturowego i polaryzacji algorytmicznej.",
                "image_url": "https://images.unsplash.com/photo-1517048676732-d65bc937f952?auto=format&fit=crop&w=1200&q=80",
                "image_concept": "Minimalistyczna sala spotkań z dwoma pustymi krzesłami rozdzielonymi smugą chłodnego światła symbolizującą brak dialogu.",
                "image_prompt": "Atmospheric editorial photo of modern minimalist meeting room, single ray of morning light dividing two empty chairs, themes of political polarization and civic silence, 8k.",
                "lead": "Polityczna polaryzacja dawno przestała być sporem o wysokość podatków czy reformę sądownictwa. Stała się tożsamościową wojną religijną, w której rację ma wyłącznie ten, kto głośniej zdezawuuje swojego przeciwnika w sieci.",
                "thesis": "Zanikanie neutralnych instytucji i monetyzacja społecznego gniewu przez media doprowadziły do upadku sztuki kompromisu. Prawdziwym zagrożeniem dla wspólnoty nie jest odmienność poglądów, lecz całkowita utrata szacunku dla faktów stojących w sprzeczności z własnym plemieniem.",
                "points": [
                    "Biznesplan na nienawiść: Dlaczego algorytmy platform społecznościowych premiują emocjonalny hejt zamiast wyważonej argumentacji.",
                    "Erozja autorytetów: Jak zniszczyliśmy zaufanie do naukowców, lekarzy i sędziów, zastępując ich partyjnymi komentatorami.",
                    "Praktyka ponownego łączenia: Czy w spolaryzowanym społeczeństwie istnieje jeszcze przestrzeń na debatę o sprawach fundamentalnych (CPK, atom, edukacja).",
                    "Pytanie dociekliwego laika: Kiedy ostatnio zmieniłeś zdanie w ważnej sprawie publicznej pod wpływem merytorycznych argumentów osoby z drugiego obozu politycznego?"
                ]
            }
        ]
    },

    # =========================================================================
    # WTOREK, 27 PAŹDZIERNIKA 2026
    # =========================================================================
    {
        "date": "2026-10-27",
        "date_pl": "27 października 2026 r.",
        "day_name": "Wtorek",
        "search_date": "27 października 2026 r. (analiza rynków i debaty publicznej)",
        "topics": [
            {
                "num": 1,
                "cat_display": "Technologia / Oprogramowanie i Bezpieczeństwo",
                "category": "technologia",
                "title": "Autonomiczni agenci oprogramowania a monopol wielkich platform cyfrowych",
                "search_date": "27 października 2026 r.",
                "source_display": "🇺🇸 Ars Technica / Bloomberg Tech",
                "source_note": "Analiza procesów antymonopolowych w USA i UE wobec platform kontrolujących dostęp do cyfrowych API.",
                "image_url": "https://images.unsplash.com/photo-1551288049-bebda4e38f71?auto=format&fit=crop&w=1200&q=80",
                "image_concept": "Pulpit analityczny z przepływem danych i schematem blokowym architektury systemowej.",
                "image_prompt": "Editorial photo of high-tech digital workflow dashboard, abstract glowing API data streams connecting corporate systems, dark blue corporate minimalist aesthetics, 8k.",
                "lead": "Przez dekady oprogramowanie oznaczało klikanie w formularze, menu i tabele. Wdrożenie agentów potrafiących komunikować się bezpośrednio z bazami danych zmienia relację między użytkownikiem a dostawcą oprogramowania.",
                "thesis": "Model aplikacji z interfejsem graficznym (GUI) przestaje być jedynym sposobem pracy z danymi. Przyszłość firmowych systemów to agenci realizujący cele biznesowe w tle, co uderza w dotychczasowe przychody z drogich licencji 'per user'.",
                "points": [
                    "Koniec monopolu interfejsów klikanych: Przejście z ręcznego wprowadzania danych na instrukcje zadaniowe.",
                    "Kwestia kontroli i audytowalności: Jak firmy weryfikują decyzje podejmowane autonomicznie przez agentów w logistyce i obsłudze klienta.",
                    "Ryzyko uzależnienia od zamkniętych ekosystemów API kilku globalnych korporacji.",
                    "Pytanie dociekliwego laika: Czy firmy są gotowe powierzyć realne budżety i operacje algorytmom, nad którymi nikt nie czuwa przy każdym kliknięciu?"
                ]
            },
            {
                "num": 2,
                "cat_display": "Gospodarka / Nieruchomości i Rynek Kredytów",
                "category": "gospodarka",
                "title": "Ceny mieszkań a dopłaty państwa: Dlaczego programy tanich kredytów napędzają marże deweloperów",
                "search_date": "27 października 2026 r.",
                "source_display": "🇵🇱 Bankier.pl / Interia Biznes",
                "source_note": "Raport Bankier.pl o wpływie rządowych programów wsparcia popytu na średnie ceny transakcyjne za metr kwadratowy w największych miastach.",
                "image_url": "https://images.unsplash.com/photo-1560518883-ce09059eeffa?auto=format&fit=crop&w=1200&q=80",
                "image_concept": "Nowoczesne osiedle mieszkaniowe z betonu i szkła z żurawiami budowlanymi w tle w perspektywie rynku nieruchomości.",
                "image_prompt": "Contemporary residential apartment blocks in metropolitan city, architectural photography, concrete and glass balconies, construction cranes, economics editorial, 8k.",
                "lead": "Kupno własnego mieszkania przez młodych ludzi w polskich metropoliach stało się barierą nie do przebycia. Zamiast zwiększać podaż gruntów i budować mieszkania komunalne, rządy od lat pompują w rynek kolejne dopłaty do kredytów.",
                "thesis": "Dotowanie popytu przy sztywnej podaży gruntów prowadzi wyłącznie do jednego rezultatu: natychmiastowego wzrostu cen mieszkań i rekordowych zysków banków oraz deweloperów. To polityka, która zamyka drogę do samodzielności całemu pokoleniu.",
                "points": [
                    "Mechanizm inflacji mieszkaniowej: Jak zapowiedź każdego kolejnego programu dopłat podnosiła ceny ofertowe w ciągu 48 godzin.",
                    "Model wiedeński vs. model polski: Dlaczego w Europie Zachodniej państwo stawia na tani najem instytucjonalny, a w Polsce wyłącznie na zadłużanie obywateli na 30 lat.",
                    "Wpływ drożyzny mieszkaniowej na zapaść demograficzną: Brak stabilnego dachu nad głową jako kluczowy powód odkładania decyzji o dzieciach.",
                    "Pytanie dociekliwego laika: Dlaczego miliardy złotych z podatków wszystkich Polaków mają iść na subsydiowanie odsetek bankowych, zamiast na budowę dostępnych mieszkań miejskich?"
                ]
            },
            {
                "num": 3,
                "cat_display": "Polityka / Unia Europejska i Suwerenność",
                "category": "polityka",
                "title": "Spór o zniesienie weta w UE: Czy federalizacja Brukseli leży w polskim interesie narodowym?",
                "search_date": "27 października 2026 r.",
                "source_display": "🇵🇱 Klub Jagielloński / Politico Europe",
                "source_note": "Dyskusja Klubu Jagiellońskiego i doniesienia Politico o pracach nad reformą traktatów unijnych i głosowaniem większościowym (QMV).",
                "image_url": "https://images.unsplash.com/photo-1451187580459-43490279c0fa?auto=format&fit=crop&w=1200&q=80",
                "image_concept": "Podświetlona mapa kontynentu europejskiego z siecią powiązań instytucjonalnych i granic państwowych.",
                "image_prompt": "Cinematic visual of European continent at night with glowing network lines representing institutional ties, dark geopolitical photography, 8k.",
                "lead": "W stolicach Europy Zachodniej narasta presja na odejście od zasady jednomyślności w polityce zagranicznej i obronnej Unii Europejskiej. Zwolennicy reformy mówią o decyzyjnej sprawności wspólnoty, przeciwnicy – o dominacji największych graczy.",
                "thesis": "Prawo weta to dla państw średnich, takich jak Polska, jedyny twardy bezpiecznik chroniący przed decyzjami sprzecznymi z ich żywotnym bezpieczeństwem. Zgoda na jego likwidację bez żelaznych gwarancji strategicznych osłabi pozycję Warszawy w Europie.",
                "points": [
                    "Lekcja z przeszłości: Jak Niemcy i Francja przez lata forsowały współpracę energetyczną z Rosją wbrew ostrzeżeniom Europy Środkowej.",
                    "Mechanizm większości kwalifikowanej (QMV): Czy koalicja państw wschodniej flanki ma wystarczającą siłę blokującą w 27-osobowej unii.",
                    "Jak zreformować UE, by nie wpaść w paraliż, a jednocześnie nie zredukować roli państw narodowych do wykonawców brukselskich dyrektyw.",
                    "Pytanie dociekliwego laika: Czy w sprawach kluczowych dla obrony granic Polski chcemy, aby o naszych działaniach decydowało głosowanie większościowe w Brukseli?"
                ]
            },
            {
                "num": 4,
                "cat_display": "Społeczeństwo / Styl Życia i Zdrowie Psychiczne",
                "category": "eseje",
                "title": "Kult nieustannej produktywności: Dlaczego w pogoni za sukcesem staliśmy się chronicznie zmęczeni",
                "search_date": "27 października 2026 r.",
                "source_display": "🇵🇱 Kultura Liberalna / Interia Opinie",
                "source_note": "Esej Kultury Liberalnej o syndromie 'hustle culture', wypaleniu zawodowym młodych specjalistów i ucieczce od odpoczynku.",
                "image_url": "https://images.unsplash.com/photo-1498050108023-c5249f4df085?auto=format&fit=crop&w=1200&q=80",
                "image_concept": "Nowoczesne biurko z laptopem i notatkami w surowym, profesjonalnym minimalistycznym stylu.",
                "image_prompt": "Overhead shot of sleek modern workspace desk with open laptop showing analytical charts, coffee cup and notebook, calm minimalist Scandinavian office aesthetic, 8k.",
                "lead": "Aplikacje do optymalizacji czasu, podcasty słuchane w przyspieszeniu 1.5x i wieczne poczucie winy, gdy nie robimy nic pożytecznego. Współczesny człowiek zamienił własne życie w arkusz kalkulacyjny nakierowany na optymalizację wyników.",
                "thesis": "Utożsamienie wartości człowieka z jego efektywnością rynkową to prosta droga do epidemii depresji i poczucia pustki. Zdolność do niespiesznego myślenia, nudy i bezinteresownej rozmowy to warunek konieczny zachowania zdrowia psychicznego.",
                "points": [
                    "Tyrania samodyscypliny: Przejście od zewnętrznego przymusu pracy w fabryce do wewnętrznego terroru bycia 'najlepszą wersją siebie'.",
                    "Dlaczego odpoczynek traktujemy jako nagrodę za wyczerpanie, zamiast jako naturalny stan regeneracji organizmu.",
                    "Jak odzyskać kontrolę nad własnym czasem w świecie powiadomień korporacyjnych komunikatorów.",
                    "Pytanie dociekliwego laika: Kiedy po raz ostatni spędziłeś całe popołudnie na robieniu czegoś, co nie miało żadnego celu zarobkowego ani nie przyniosło żadnej wymiernej korzyści?"
                ]
            }
        ]
    },

    # =========================================================================
    # PONIEDZIAŁEK, 26 PAŹDZIERNIKA 2026
    # =========================================================================
    {
        "date": "2026-10-26",
        "date_pl": "26 października 2026 r.",
        "day_name": "Poniedziałek",
        "search_date": "26 października 2026 r. (analiza rynków i debaty publicznej)",
        "topics": [
            {
                "num": 1,
                "cat_display": "Technologia / Cyberbezpieczeństwo i Infrastruktura",
                "category": "technologia",
                "title": "Cyberwojna poniżej progu wojny: Jak paraliż szpitali i wodociągów stał się nową normą",
                "search_date": "26 października 2026 r.",
                "source_display": "🇬🇧 The Financial Times / Ars Technica",
                "source_note": "Raport FT i agencji wywiadowczych o zmasowanych atakach ransomware na zachodnią infrastrukturę komunalną i energetyczną.",
                "image_url": "https://images.unsplash.com/photo-1550751827-4bd374c3f58b?auto=format&fit=crop&w=1200&q=80",
                "image_concept": "Ciemna serwerownia z migającymi diodami światłowodów i chłodnym oświetleniem w klimacie cyberbezpieczeństwa.",
                "image_prompt": "High-tech server room with glowing fiber optic cables and cybersecurity alert status lights, dramatic corporate technology journalism photo, 8k.",
                "lead": "Nowoczesne państwo można sparaliżować bez wystrzelenia ani jednego pocisku. Ataki hakerskie na bazy danych szpitali, stacje uzdatniania wody czy systemy sterowania ruchem pociągów przestały być domeną filmów science-fiction.",
                "thesis": "Cyfryzacja bez analogowych bezpieczników i rygorystycznej ochrony kryptograficznej to zaproszenie do katastrofy. Skupiając się na wygodzie aplikacji online, zapomnieliśmy o fizycznej odporności państwa na sabotaż.",
                "points": [
                    "Wojna hybrydowa w szarej strefie: Dlaczego rządom trudno oficjalnie odpowiedzieć na ataki grup hakerskich działających na zlecenie obcych wywiadów.",
                    "Dług technologiczny polskiego sektora publicznego: Przetargi 'najniższa cena' a przestarzałe oprogramowanie w urzędach i szpitalach.",
                    "Koncepcja odporności analogowej: Dlaczego kluczowe zawory, zwrotnice i generatory muszą posiadać ręczne sterowanie na wypadek odcięcia sieci.",
                    "Pytanie dociekliwego laika: Co zrobi Twoje miasto, gdy w wyniku cyberataku na 72 godziny zniknie woda w kranach i prąd w lodówkach?"
                ]
            },
            {
                "num": 2,
                "cat_display": "Gospodarka / Handel Międzynarodowy i Cła",
                "category": "gospodarka",
                "title": "Wojna celna USA–Chiny: Koniec epoki tanich towarów i powrót twardego protekcjonizmu",
                "search_date": "26 października 2026 r.",
                "source_display": "🌍 Investing.com / Bloomberg",
                "source_note": "Analiza rynkowa Investing.com dotycząca nowych taryf celnych na samochody elektryczne, panele fotowoltaiczne i metale ziem rzadkich.",
                "image_url": "https://images.unsplash.com/photo-1578575437130-527eed3abbec?auto=format&fit=crop&w=1200&q=80",
                "image_concept": "Kontenery towarowe w wielkim terminalu przeładunkowym portu morskiego o wschodzie słońca.",
                "image_prompt": "Shipping containers stacked in international cargo seaport terminal at sunrise, industrial cargo crane, global trade economics photography, 8k.",
                "lead": "Trzydzieści lat globalizacji opartej na zasadzie 'produkujmy tam, gdzie najtaniej' właśnie dobiega końca. Zarówno Waszyngton, jak i Bruksela wznoszą mury celne, aby chronić rodzime miejsca pracy przed zalewem dotowanych produktów z Azji.",
                "thesis": "Bezpieczeństwo dostaw i suwerenność przemysłowa kosztują. Powrót produkcji do krajów zachodnich oznacza trwale wyższą inflację i konieczność zaakceptowania wyższych cen codziennych produktów konsumpcyjnych.",
                "points": [
                    "Efekt skali i chiński dumping: Dlaczego żaden zachodni producent nie jest w stanie konkurować cenowo z państwowymi subsydiami w Pekinie.",
                    "Koszty 'friend-shoringu': Przenoszenie fabryk do Meksyku, Indii czy Polski a rosnące wydatki inwestycyjne korporacji.",
                    "Dylemat europejskiego konsumenta: Chcemy zielonej transformacji, ale nie chcemy płacić dwukrotnie więcej za auta i baterie wyprodukowane w Europie.",
                    "Pytanie dociekliwego laika: Czy jako konsumenci jesteśmy gotowi płacić 30% więcej za elektronikę i ubrania, aby fabryki i miejsca pracy wróciły do Europy?"
                ]
            },
            {
                "num": 3,
                "cat_display": "Polityka / Demografia i Społeczeństwo",
                "category": "polityka",
                "title": "Kryzys demograficzny Polski: Dlaczego transfery finansowe nie skłoniły Polaków do rodzenia dzieci?",
                "search_date": "26 października 2026 r.",
                "source_display": "🇵🇱 Klub Jagielloński / Kanał Zero (Debaty)",
                "source_note": "Analiza Klubu Jagiellońskiego dotycząca danych GUS o rekordowo niskiej liczbie urodzeń w Polsce i dyskusja na Kanale Zero.",
                "image_url": "https://images.unsplash.com/photo-1502086223501-7ea6ecd79368?auto=format&fit=crop&w=1200&q=80",
                "image_concept": "Pusta ulica z zabawkami dziecięcymi i cichym podwórkiem miejskim w ciepłym świetle popołudnia.",
                "image_prompt": "Atmospheric documentary photo of quiet residential park bench with single forgotten child toy, soft afternoon sunlight, demographic transition theme, 8k.",
                "lead": "Kolejne programy wsparcia finansowego rodzin miały odwrócić negatywne trendy ludnościowe. Tymczasem wskaźniki dzietności w Polsce spadły do najniższych poziomów w powojennej historii kraju.",
                "thesis": "Pieniądze do ręki nie zastąpią dostępnych żłobków, stabilnej pracy, nowoczesnej opieki okołoporodowej i przystępnych cenowo mieszkań. Zapaść demograficzna to wotum nieufności obywateli wobec jakości usług publicznych świadczonych przez państwo.",
                "points": [
                    "Diagnoza przyczyn: Poczucie braku stabilności u młodych kobiet jako główny czynnik odraczania macierzyństwa.",
                    "Przyszłość systemu emerytalnego ZUS: Kto sfinansuje emerytury obecnych 30- i 40-latków, gdy na jednego emeryta przypadać będzie jeden pracownik.",
                    "Konieczność mądrej i kontrolowanej polityki imigracyjnej zamiast zamiatania tematu pod dywan.",
                    "Pytanie dociekliwego laika: Skoro kolejne setki miliardów złotych wydane na programy socjalne nie przyniosły ani jednego dodatkowego dziecka, dlaczego nikt nie weryfikuje sensu tej polityki?"
                ]
            },
            {
                "num": 4,
                "cat_display": "Społeczeństwo / Kultura i Edukacja",
                "category": "eseje",
                "title": "Atrofia czytelnictwa: Jak konsumpcja 15-sekundowych rolek niszczy zdolność rozumienia złożonego świata",
                "search_date": "26 października 2026 r.",
                "source_display": "🇵🇱 Kultura Liberalna / Klub Jagielloński",
                "source_note": "Esej Kultury Liberalnej i Klubu Jagiellońskiego o degradacji uwagi, spadku sprzedaży książek i kryzysie humanistycznym.",
                "image_url": "https://images.unsplash.com/photo-1457369804613-52c61a468e7d?auto=format&fit=crop&w=1200&q=80",
                "image_concept": "Stare i nowe książki na drewnianym regale w ciepłym świetle domowej biblioteki.",
                "image_prompt": "Artistic close-up of classical hardcover books stacked on wooden shelf, soft glowing dust particles in library sunlight, quiet intellectual focus, 8k.",
                "lead": "Przeczytanie kilkustronicowego artykułu lub powieści staje się dla wielu osób wysiłkiem ponad siły. Mózgi wytresowane przez algorytmy TikToka i Instagrama domagają się natychmiastowego strzału dopaminy co kilkanaście sekund.",
                "thesis": "Spadek czytelnictwa to nie tylko problem księgarzy, lecz fundamentalne zagrożenie dla demokracji. Człowiek niezdolny do skupienia uwagi na długim tekście staje się bezbronny wobec prymitywnej propagandy i emocjonalnych manipulacji.",
                "points": [
                    "Mechanizm 'rozproszonej uwagi': Dlaczego przerywanie lektury sprawdzaniem telefonu oducza mózg myślenia przyczynowo-skutkowego.",
                    "Szkoła w kryzysie: Tradycyjny kanon lektur w zderzeniu z pokoleniem, które przyswaja rzeczywistość wyłącznie w formie wizualnych skrótów.",
                    "Czytanie książek jako akt politycznego oporu przeciwko rynkowi algorytmicznego uzależnienia.",
                    "Pytanie dociekliwego laika: Kiedy ostatnio przeczytałeś książkę od deski do deski bez sięgania po smartfon co piętnaście minut?"
                ]
            }
        ]
    },

    # =========================================================================
    # NIEDZIELA, 25 PAŹDZIERNIKA 2026
    # =========================================================================
    {
        "date": "2026-10-25",
        "date_pl": "25 października 2026 r.",
        "day_name": "Niedziela",
        "search_date": "25 października 2026 r. (analiza rynków i debaty publicznej)",
        "topics": [
            {
                "num": 1,
                "cat_display": "Technologia / Prawa Autorskie i Media",
                "category": "technologia",
                "title": "Kradzież czy postęp? Kto ma prawo do zysków, gdy algorytmy szkolą się na dorobku ludzkości",
                "search_date": "25 października 2026 r.",
                "source_display": "🇺🇸 Ars Technica / Politico",
                "source_note": "Spory sądowe wydawców prasowych i autorów z korporacjami technologicznymi w Nowym Jorku i Brukseli.",
                "image_url": "https://images.unsplash.com/photo-1589829545856-d10d557cf95f?auto=format&fit=crop&w=1200&q=80",
                "image_concept": "Sędziowski młotek na tle regałów z księgami prawniczymi w klimacie prawa autorskiego.",
                "image_prompt": "Judicial wooden gavel resting on leather bound law books, dramatic courtroom library lighting, copyright and intellectual property editorial photo, 8k.",
                "lead": "Wszystkie wiodące korporacje cyfrowe zbudowały swoje modele w oparciu o teksty, obrazy i kod stworzone przez miliony pisarzy, dziennikarzy i programistów. Gdy przyszło do podziału zysków, autorzy zostali z niczym.",
                "thesis": "Koncepcja 'dozwolonego użytku' nie może służyć jako parawan dla bezpłatnej eksploatacji własności intelektualnej na skalę przemysłową. Jeśli zniszczymy model biznesowy niezależnego dziennikarstwa i twórczości, wkrótce algorytmy będą karmić się wyłącznie syntetycznym bełkotem.",
                "points": [
                    "Pozwy zbiorowe mediów przeciwko Big Tech: Bitwa o licencjonowanie treści i definicję cytatu.",
                    "Problem 'zanieczyszczenia danych': Co się stanie z modelami, gdy w sieci zabraknie nowych tekstów napisanych przez żywych ludzi.",
                    "Jak wycenić wkład pojedynczego autora w model zasilany bilionami tokenów.",
                    "Pytanie dociekliwego laika: Czy gdybyś skopiował treść całej encyklopedii i sprzedawał ją pod własnym nazwiskiem, sąd nazwałby to innowacją czy zwykłym piractwem?"
                ]
            },
            {
                "num": 2,
                "cat_display": "Gospodarka / Energetyka i Przemysł",
                "category": "gospodarka",
                "title": "Reindustrializacja Europy czy ucieczka kapitału? Dlaczego fabryki przenoszą się do USA i Azji",
                "search_date": "25 października 2026 r.",
                "source_display": "🇬🇧 The Financial Times / OSW",
                "source_note": "Raport Mario Draghiego i analizy FT o drastycznym spadku konkurencyjności europejskiego przemysłu chemicznego i maszynowego.",
                "image_url": "https://images.unsplash.com/photo-1581091226825-a6a2a5aee158?auto=format&fit=crop&w=1200&q=80",
                "image_concept": "Zautomatyzowana linia produkcyjna w fabryce przemysłowej z precyzyjnymi ramionami robotycznymi.",
                "image_prompt": "Automated modern automotive manufacturing plant with robotic assembly arms and precision laser welding, cool blue industrial photography, 8k.",
                "lead": "Wysokie koszty energii elektrycznej, restrykcyjna polityka klimatyczna ETS i biurokracja sprawiają, że europejskie koncerny masowo ogłaszają inwestycje poza kontynentem. Europa staje w obliczu realnego ryzyka dezindustrializacji.",
                "thesis": "Nie da się utrzymać dobrobytu i wysokich standardów socjalnych wyłącznie w oparciu o turystykę i usługi finansowe. Jeśli Europa straci bazę przemysłową, stanie się bezsilnym skansenem uzależnionym od dostaw z zewnątrz.",
                "points": [
                    "Różnica w kosztach energii: Dlaczego gaz i prąd dla przemysłu w USA są trzykrotnie tańsze niż w Niemczech i Polsce.",
                    "Amerykańska ustawa IRA i subsydia: Jak Waszyngton przyciąga europejski kapitał podatkowymi ulgami.",
                    "Co oznacza utrata przemysłu dla polskiego eksportu: Jesteśmy poddostawcą niemieckich fabryk, więc ich kryzys uderzy w polskie pensje.",
                    "Pytanie dociekliwego laika: Skąd weźmiemy pieniądze na obronność i szpitale, jeśli największe zakłady produkcyjne zamkną się i przeniosą do Teksasu lub Chin?"
                ]
            },
            {
                "num": 3,
                "cat_display": "Polityka / Bezpieczeństwo i Obrona Cywilna",
                "category": "polityka",
                "title": "Obrona cywilna w Polsce: Pomiędzy papierowymi procedurami a twardą rzeczywistością schronów",
                "search_date": "25 października 2026 r.",
                "source_display": "🇵🇱 Kanał Zero / Nowa Konfederacja",
                "source_note": "Debata Kanału Zero z udziałem ekspertów wojskowych i samorządowców o braku ustawy o obronie cywilnej i stanie schronów.",
                "image_url": "https://images.unsplash.com/photo-1541888946425-d0fbb186c5f7?auto=format&fit=crop&w=1200&q=80",
                "image_concept": "Podziemny surowy żelbetowy korytarz schronu ochronnego z hermetycznymi drzwiami stalowymi.",
                "image_prompt": "Underground heavy reinforced concrete protective shelter corridor with heavy steel blast doors, stark emergency lighting, civil defense documentary photo, 8k.",
                "lead": "Wydajemy setki miliardów złotych na czołgi, myśliwce i wyrzutnie rakiet. Jednocześnie miliony obywateli w polskich miastach w razie nalotu nie mają pojęcia, gdzie szukać bezpiecznego schronienia.",
                "thesis": "Prawdziwa siła obronna państwa leży w ochronie ludności cywilnej. Zaniedbania w obszarze schronów, magazynów wody pitnej i procedur ewakuacyjnych to najsłabsze ogniwo polskiego systemu bezpieczeństwa.",
                "points": [
                    "Luka prawna po likwidacji Obrony Cywilnej Kraju: Samorządy bez budżetów i bez jasnych wytycznych technicznych.",
                    "Stan techniczny piwnic i parkingów podziemnych: Dlaczego 95% z nich nie spełnia norm ochrony przed falami uderzeniowymi i gazami bojowymi.",
                    "Wzór szwajcarski i izraelski: Jak małe państwa potrafiły zbudować system, w którym miejsce w schronie ma zapewniony każdy obywatel.",
                    "Pytanie dociekliwego laika: Na co komu najnowocześniejsze myśliwce na niebie, jeśli na dole nikt nie potrafi zabezpieczyć ujęć wody i szpitali przed pierwszym atakiem?"
                ]
            },
            {
                "num": 4,
                "cat_display": "Społeczeństwo / Media i Autorytety",
                "category": "eseje",
                "title": "Kryzys autorytetów: Dlaczego w epoce niepewności zaufaliśmy influencerom bardziej niż naukowcom?",
                "search_date": "25 października 2026 r.",
                "source_display": "🇵🇱 Kultura Liberalna / Interia Opinie",
                "source_note": "Analiza socjologiczna w Kulturze Liberalnej o upadku zaufania do tradycyjnych ekspertów i triumfie charyzmatycznych twórców internetowych.",
                "image_url": "https://images.unsplash.com/photo-1516321318423-f06f85e504b3?auto=format&fit=crop&w=1200&q=80",
                "image_concept": "Samotna postać w półmroku przed świecącym ekranem smartfona w wielkim mieście nocą.",
                "image_prompt": "Solitary person looking at glowing smartphone screen at night by apartment window overlooking metropolitan skyline, intimate emotional technology theme, 8k.",
                "lead": "Naukowcy mówią językiem pełnym zastrzeżeń, prawdopodobieństw i skomplikowanych danych. Twórca internetowy oferuje proste odpowiedzi, emocjonalną autentyczność i poczucie bliskości. W efekcie to on kształtuje opinie milionów.",
                "thesis": "Kryzys tradycyjnych autorytetów nie wynika z ignorancji ludzi, lecz z hermetyczności i arogancji instytucji akademickich. Gdy eksperci zamknęli się w wieżach z kości słoniowej, próżnię natychmiast wypełnili sprawni handlarze emocji i teorii spiskowych.",
                "points": [
                    "Paradoks dostępności wiedzy: Mamy pod ręką całą wiedzę ludzkości, a wierzymy w najprostsze szarlataństwa medyczne i finansowe.",
                    "Dlaczego 'charyzma z TikToka' wygrywa z rzetelnym dorobkiem profesorskim.",
                    "Jak przywrócić szacunek dla twardej nauki w świecie, w którym każdy ma prawo do własnej prawdy.",
                    "Pytanie dociekliwego laika: Dlaczego w sprawach zdrowia czy finansów jesteśmy skłonni zaufać osobie znanej z internetu, której jedyną kwalifikacją jest wysoka liczba obserwujących?"
                ]
            }
        ]
    },

    # =========================================================================
    # SOBOTA, 24 PAŹDZIERNIKA 2026
    # =========================================================================
    {
        "date": "2026-10-24",
        "date_pl": "24 października 2026 r.",
        "day_name": "Sobota",
        "search_date": "24 października 2026 r. (analiza rynków i debaty publicznej)",
        "topics": [
            {
                "num": 1,
                "cat_display": "Technologia / Bezpieczeństwo i Komputery Kwantowe",
                "category": "technologia",
                "title": "Kwantowe odliczanie do zera: Dlaczego banki i armie już dziś wymieniają kryptografię",
                "search_date": "24 października 2026 r.",
                "source_display": "🇺🇸 MIT Technology Review / Ars Technica",
                "source_note": "Publikacja MIT Tech Review o wdrożeniach algorytmów Post-Quantum Cryptography (PQC) certyfikowanych przez NIST.",
                "image_url": "https://images.unsplash.com/photo-1635070041078-e363dbe005cb?auto=format&fit=crop&w=1200&q=80",
                "image_concept": "Abstrakcyjna geometria kwantowa ze złotymi cylindrami chłodzenia kriogenicznego procesora.",
                "image_prompt": "Golden quantum computing cryostat chandelier in dark research laboratory, futuristic quantum physics technology photo, 8k.",
                "lead": "Choć komercyjne komputery kwantowe zdolne złamać klucze RSA jeszcze nie powstały, wrogie wywiady już teraz przechwytują i magazynują szyfrowany ruch w sieci. Zasada brzmi: przechwyć dziś, odszyfruj za 5 lat.",
                "thesis": "Zagrożenie kwantowe nie jest kwestią odległej przyszłości, lecz dzisiejszej logistyki IT. Instytucje finansowe i wojskowe, które spóźnią się z migracją na kryptografię postkwantową, staną się bezbronnym celem szantażu.",
                "points": [
                    "Strategia 'Store Now, Decrypt Later': Dlaczego poufne dane dyplomatyczne i patenty medyczne są kopiowane przez obce państwa już dziś.",
                    "Wyzwania wdrożeniowe: Dlaczego wymiana algorytmów w tysiącach bankomatów i kart płatniczych zajmie dekadę.",
                    "Kto przewodzi w wyścigu: Amerykańscy giganci technologiczni vs. państwowe laboratoria w Szanghaju.",
                    "Pytanie dociekliwego laika: Czy Twoje hasła bankowe i prywatne wiadomości z dzisiaj będą cokolwiek warte, gdy ktoś odszyfruje je jednym kliknięciem za kilka lat?"
                ]
            },
            {
                "num": 2,
                "cat_display": "Gospodarka / Surowce i Rynki Energetyczne",
                "category": "gospodarka",
                "title": "Baryłka ropy a globalna inflacja: Dlaczego surowce wciąż dyktują koszty życia w Europie",
                "search_date": "24 października 2026 r.",
                "source_display": "🌍 Investing.com / The Financial Times",
                "source_note": "Dane rynkowe Investing.com dotyczące polityki wydobywczej OPEC+, transportu przez cieśninę Ormuz i cen paliw w detalu.",
                "image_url": "https://images.unsplash.com/photo-1518709268805-4e9042af9f23?auto=format&fit=crop&w=1200&q=80",
                "image_concept": "Platforma wiertnicza na otwartym oceanie o zachodzie słońca z płonącym pochodnią gazową.",
                "image_prompt": "Offshore deepwater oil drilling platform on vast dark ocean waves at sunset, glowing industrial flare, energy commodities economics photography, 8k.",
                "lead": "Mimo haseł o odchodzeniu od paliw kopalnych ropa naftowa i gaz ziemny pozostają krwioobiegiem globalnego transportu i przemysłu chemicznego. Każdy skok cen baryłki na giełdzie w Nowym Jorku przekłada się na ceny żywności w polskim dyskoncie.",
                "thesis": "Zielona transformacja prowadzona bez zabezpieczenia stabilnych źródeł konwencjonalnych na okres przejściowy naraża gospodarki na potężne szoki podażowe. Zamiast uniezależnienia od dyktatu karteli surowcowych, wpadamy w kolejne uzależnienia.",
                "points": [
                    "Koszt transportu morskiego i ubezpieczeń tankowców w rejonach zapalnych (Morze Czerwone, Cieśnina Malakka).",
                    "Ropa jako fundament nawozów sztucznych i tworzyw: Dlaczego droga ropa to automatycznie droższy chleb i warzywa.",
                    "Strategiczne rezerwy surowcowe państwa: Czy Polska jest odporna na nagłe wstrzymanie dostaw morskich.",
                    "Pytanie dociekliwego laika: Skoro od lat słyszymy o nieuchronnym końcu ery ropy, dlaczego decyzje kilku szejków wciąż decydują o tym, ile płacimy przy dystrybutorze?"
                ]
            },
            {
                "num": 3,
                "cat_display": "Polityka / Infrastruktura i Korytarze Strategiczne",
                "category": "polityka",
                "title": "Trójmorze, CPK i Via Carpatia: Czy Polska potrafi przekształcić swoje położenie w twardą siłę?",
                "search_date": "24 października 2026 r.",
                "source_display": "🇵🇱 Nowa Konfederacja / Klub Jagielloński",
                "source_note": "Analiza Nowej Konfederacji i Klubu Jagiellońskiego na temat rentowności wielkich projektów infrastrukturalnych na osi Północ-Południe.",
                "image_url": "https://images.unsplash.com/photo-1544620347-c4fd4a3d5957?auto=format&fit=crop&w=1200&q=80",
                "image_concept": "Nowoczesny pociąg ekspresowy na estakadzie kolejowej przecinającej równiny o świcie.",
                "image_prompt": "High-speed modern aerodynamic passenger train speeding on concrete viaduct at dawn, cinematic transportation infrastructure photography, 8k.",
                "lead": "Przez stulecia położenie geograficzne między Niemcami a Rosją było dla Polski geopolitycznym przekleństwem. Budowa lotniczych hubów przeładunkowych, sieci Kolei Dużych Prędkości i szlaków z Bałtyku nad Morze Czarne może zamienić je w źródło potężnych przychodów.",
                "thesis": "Wielka infrastruktura logistyczna to nie kwestia narodowej megalomanii, lecz warunek przeskoczenia z pozycji gospodarki peryferyjnej do roli węzła tranzytowego całej Europy Środkowej. Rezygnacja z takich projektów to dobrowolne oddanie marży logistycznej sąsiadom.",
                "points": [
                    "Wąskie gardła transportu wojskowego (Military Mobility): Dlaczego armie sojusznicze potrzebują hubu cargo i mostów o wysokiej nośności.",
                    "Oś Północ-Południe w kontrze do osi Wschód-Zachód: Jak powiązanie państw Trójmorza uniezależnia region od dominacji szlaków przez Niemcy.",
                    "Spór polityczny w Warszawie: Dlaczego w Polsce wielkie inwestycje padają ofiarą plemiennej walki kolejnych ekip rządowych.",
                    "Pytanie dociekliwego laika: Dlaczego Niemcy, Francuzi i Holendrzy rozbudowują swoje wielkie lotniska i porty, a w Polsce każda strategiczna budowa jest przedstawiana jako niepotrzebny luksus?"
                ]
            },
            {
                "num": 4,
                "cat_display": "Społeczeństwo / Urbanistyka i Samotność",
                "category": "eseje",
                "title": "Samotność w betonowych sypialniach: Dlaczego w tłumie milionów ludzi czujemy się najbardziej wyobcowani",
                "search_date": "24 października 2026 r.",
                "source_display": "🇵🇱 Kultura Liberalna / Klub Jagielloński",
                "source_note": "Badania socjologiczne publikowane w Kulturze Liberalnej o zaniku więzi sąsiedzkich i atomizacji mieszkańców grodzonych osiedli.",
                "image_url": "https://images.unsplash.com/photo-1509198397868-475647b2a1e5?auto=format&fit=crop&w=1200&q=80",
                "image_concept": "Nocne okna wielkiego wieżowca z pojedynczymi ciepłymi punktami światła w wielomilionowym mieście.",
                "image_prompt": "Night urban shot of sprawling high-rise residential building with scattered warm illuminated windows, themes of loneliness in modern city life, cinematic, 8k.",
                "lead": "Mieszkamy ściana w ścianę z setkami obcych ludzi, mijamy ich w windach bez słowa powitania, a zakupy zamawiamy do paczkomatu, byle uniknąć kontaktu ze sprzedawcą. Miasta stały się maszynami do anonimowego funkcjonowania.",
                "thesis": "Architektura zorientowana na maksymalizację zysku z metra kwadratowego wyeliminowała wspólne przestrzenie: place zabaw, ławki, domy kultury. Przestrzeń miejska, która nie sprzyja przypadkowym spotkaniom, skazuje ludzi na izolację i depresję.",
                "points": [
                    "Grodzone osiedla jako symbol strachu przed współobywatelem i utraty zaufania społecznego.",
                    "Zjawisko 'trzecich miejsc': Gdzie podziały się kawiarnie, biblioteki i parki, w których można przebywać bez konieczności płacenia za konsumpcję.",
                    "Epidemia samotności wśród osób starszych i młodych singli: Koszty zdrowotne i społeczne rozpadu tradycyjnych wspólnot.",
                    "Pytanie dociekliwego laika: Kiedy ostatnio pożyczyłeś od sąsiada cukier lub zapytałeś go, jak się czuje, zamiast patrzeć w podłogę podczas jazdy windą?"
                ]
            }
        ]
    },

    # =========================================================================
    # PIĄTEK, 23 PAŹDZIERNIKA 2026
    # =========================================================================
    {
        "date": "2026-10-23",
        "date_pl": "23 października 2026 r.",
        "day_name": "Piątek",
        "search_date": "23 października 2026 r. (analiza rynków i debaty publicznej)",
        "topics": [
            {
                "num": 1,
                "cat_display": "Technologia / Regulacje i Wolność Słowa",
                "category": "technologia",
                "title": "Cenzura wbudowana w kod: Kto decyduje o poglądach i ograniczeniach cyfrowych asystentów",
                "search_date": "23 października 2026 r.",
                "source_display": "🇬🇧 The Financial Times / Ars Technica",
                "source_note": "Spór o regulacje moderacji treści i wytyczne etyczne nakładane na wyszukiwarki i boty konwersacyjne w USA i UE.",
                "image_url": "https://images.unsplash.com/photo-1510511459019-5dda7724fd87?auto=format&fit=crop&w=1200&q=80",
                "image_concept": "Zamknięta cyfrowa kłódka nałożona na zielony kod programu symbolizująca cenzurę i blokady systemowe.",
                "image_prompt": "Digital padlock locking glowing source code lines, digital censorship and corporate speech control theme, stark dark cyber aesthetic, 8k.",
                "lead": "Gdy setki milionów ludzi używają asystentów do pisania e-maili, szukania informacji medycznych czy odrabiania lekcji, to, co dany system uzna za 'niedozwolone' lub 'niewłaściwe', staje się nowym wyznacznikiem prawdy.",
                "thesis": "Zarządy kilku spółek technologicznych w Dolinie Krzemowej arbitralnie ustalają granice dozwolonej dyskusji o historii, polityce i obyczajowości. To bezprecedensowa koncentracja władzy nad słowem, wymykająca się jakiejkolwiek demokratycznej kontroli.",
                "points": [
                    "Jak wytyczne systemowe (system prompts) kształtują polityczny światopogląd odpowiedzi algorytmów.",
                    "Różnice między modelami amerykańskimi, chińskimi a europejskimi projektami otwartoźródłowymi.",
                    "Zjawisko 'halucynacji politycznej': Unikanie faktów w imię korporacyjnej poprawności i unikania sporów sądowych.",
                    "Pytanie dociekliwego laika: Czy chcemy, aby o tym, co jest właściwym poglądem historycznym lub dopuszczalną opinią, decydował regulamin jednej korporacji z Kalifornii?"
                ]
            },
            {
                "num": 2,
                "cat_display": "Gospodarka / Nieruchomości Komercyjne i Praca",
                "category": "gospodarka",
                "title": "Puste biurowce i zamrożony kapitał: Jak praca zdalna uderza w fundamenty funduszy nieruchomości",
                "search_date": "23 października 2026 r.",
                "source_display": "🌍 Investing.com / Bloomberg",
                "source_note": "Raport rynkowy Bloomberg o wskaźnikach pustostanów w centrach finansowych i problemach z refinansowaniem obligacji biurowych.",
                "image_url": "https://images.unsplash.com/photo-1497366216548-37526070297c?auto=format&fit=crop&w=1200&q=80",
                "image_concept": "Puste, przeszklone piętro nowoczesnego biurowca z fotelami i gasnącym światłem wielkiego miasta.",
                "image_prompt": "Empty corporate office floor with minimalist desks and floor to ceiling glass windows overlooking evening city, quiet economic transition theme, 8k.",
                "lead": "Korporacje na całym świecie próbują zmusić pracowników do powrotu za biurka. Jednak model pracy hybrydowej okazał się zbyt wygodny, by z niego zrezygnować. W efekcie tysiące szklanych wieżowców w stolicach świeci pustkami.",
                "thesis": "Rynek biurowy stoi przed strukturalnym załamaniem wycen. Fundusze emerytalne, które ulokowały miliardy w obligacjach zabezpieczonych nieruchomościami komercyjnymi, stoją w obliczu bolesnych odpisów aktualizujących.",
                "points": [
                    "Wskaźniki pustostanów w Warszawie, Londynie i Nowym Jorku: Dlaczego renegocjacja umów najmu oznacza spadki przychodów o 30-40%.",
                    "Kryzys otoczenia biznesowego: Jak brak pracowników w biurowcach niszczy małą gastronomię, piekarnie i pralnie w centrach miast.",
                    "Czy możliwa jest konwersja biurowców na mieszkania: Ogromne bariery architektoniczne, sanitarne i prawne.",
                    "Pytanie dociekliwego laika: Skoro praca z domu okazała się w wielu branżach równie efektywna, dlaczego korporacje wydają miliony na zmuszanie ludzi do stania w korkach?"
                ]
            },
            {
                "num": 3,
                "cat_display": "Polityka / Wojna Informacyjna i Dezinformacja",
                "category": "polityka",
                "title": "Fabryki kłamstwa w Twoim telefonie: Jak wrogie narracje rozbijają polskie zaufanie do państwa",
                "search_date": "23 października 2026 r.",
                "source_display": "🇵🇱 Ośrodek Studiów Wschodnich (OSW) / Kanał Zero",
                "source_note": "Opracowanie OSW na temat rosyjskich i białoruskich operacji psychologicznych skierowanych na polską infosferę i debatę publiczną.",
                "image_url": "https://images.unsplash.com/photo-1504711434969-e33886168f5c?auto=format&fit=crop&w=1200&q=80",
                "image_concept": "Stos starych gazet z nagłówkami mieszający się z cyfrowym ekranem smartfona w świetle studia informacyjnego.",
                "image_prompt": "Newspapers and digital media screens collision, dramatic journalism aesthetic, disinformation and media integrity theme, 8k.",
                "lead": "Wojna informacyjna XXI wieku nie polega na przekonywaniu ludzi do pokochania agresora. Polega na przekonaniu ich, że ich własne państwo jest bezradne, armia nie istnieje, a sąsiadowi nie można ufać.",
                "thesis": "Najgroźniejszą bronią w operacjach hybrydowych jest podsycenie istniejących już podziałów społecznych. Podatność polskiej debaty publicznej na wrogie wrzutki wynika z chronicznego braku zaufania obywateli do instytucji publicznych.",
                "points": [
                    "Taktyka 'zalewania szumem': Publikowanie sprzecznych wersji tego samego wydarzenia, aby wywołać apatię i poczucie, że prawda nie istnieje.",
                    "Wykorzystywanie lokalnych tematów zapalnych: Spory wokół uchodźców, rolnictwa i cen energii jako paliwo dla botów.",
                    "Jak odróżnić uzasadnioną krytykę rządu od zorganizowanej akcji dywersyjnej w mediach społecznościowych.",
                    "Pytanie dociekliwego laika: Kiedy ostatnio sprawdziłeś źródło sensacyjnej informacji z internetu, zanim z oburzeniem przesłałeś ją znajomym?"
                ]
            },
            {
                "num": 4,
                "cat_display": "Społeczeństwo / Rynek Pracy i Edukacja",
                "category": "eseje",
                "title": "Inflacja dyplomów: Dlaczego wyższe wykształcenie przestało gwarantować bezpieczną przyszłość",
                "search_date": "23 października 2026 r.",
                "source_display": "🇵🇱 Klub Jagielloński / Interia",
                "source_note": "Raport Klubu Jagiellońskiego o degradacji poziomu szkolnictwa wyższego w Polsce i zjawisku prekaryzacji absolwentów.",
                "image_url": "https://images.unsplash.com/photo-1523050854058-8df90110c9f1?auto=format&fit=crop&w=1200&q=80",
                "image_concept": "Pusta aula uniwersytecka z drewnianymi ławami i rozproszonym światłem poranka w neogotyckim gmachu.",
                "image_prompt": "Historic wooden university lecture hall interior with sunbeams piercing through tall windows, academic tradition and future of education theme, 8k.",
                "lead": "Przez dekady rodzice powtarzali dzieciom: 'idź na studia, to będziesz miał dobre życie'. Dziś Polska ma jeden z najwyższych odsetków magistrów w Europie, a jednocześnie tysiące absolwentów pracuje poniżej kwalifikacji.",
                "thesis": "Masowa produkcja dyplomów przez setki prywatnych i państwowych uczelni zdewaluowała wartość akademickiego wykształcenia. Rynek pracy pilnie potrzebuje techników, rzemieślników i inżynierów, a system edukacji wciąż produkuje teoretyków.",
                "points": [
                    "Erozja prestiżu uniwersytetu: Gdy zdanie egzaminu sprowadza się do klikania w testy jednokrotnego wyboru.",
                    "Renesans zawodów technicznych i rzemiosła: Dlaczego wykwalifikowany elektryk, hydraulik czy mechanik zarabia dziś więcej niż pracownik biurowy z tytułem magistra.",
                    "Jak zreformować polskie uczelnie, by uczyły odwagi myślenia i rzetelnych umiejętności, a nie tylko formalnej obecności.",
                    "Pytanie dociekliwego laika: Czy pięć lat spędzone na studiach dało Ci narzędzia do zrozumienia świata, czy tylko papier, o który nikt w pracy Cię nie zapytał?"
                ]
            }
        ]
    },

    # =========================================================================
    # CZWARTEK, 22 PAŹDZIERNIKA 2026
    # =========================================================================
    {
        "date": "2026-10-22",
        "date_pl": "22 października 2026 r.",
        "day_name": "Czwartek",
        "search_date": "22 października 2026 r. (analiza rynków i debaty publicznej)",
        "topics": [
            {
                "num": 1,
                "cat_display": "Technologia / Open Source i Społeczność",
                "category": "technologia",
                "title": "Niewidzialny kręgosłup sieci: Kto utrzyma darmowe oprogramowanie, na którym stoi świat",
                "search_date": "22 października 2026 r.",
                "source_display": "🇺🇸 Ars Technica / MIT Tech Review",
                "source_note": "Wykrycie podatności XZ Utils i debata w Ars Technica o wypaleniu wolontariuszy utrzymujących biblioteki open-source.",
                "image_url": "https://images.unsplash.com/photo-1555066931-4365d14bab8c?auto=format&fit=crop&w=1200&q=80",
                "image_concept": "Zbliżenie na ekran programisty z czystym, wielokolorowym kodem źródłowym w ciemnym motywie.",
                "image_prompt": "Close-up macro of clean programming source code lines on dark glowing developer monitor, software craftsmanship editorial photo, 8k.",
                "lead": "Banki, linie lotnicze, szpitale i smartfony działają w oparciu o tysiące darmowych bibliotek tworzonych przez pasjonatów w ich wolnym czasie. Niewielu zdaje sobie sprawę, jak kruchy jest ten fundament.",
                "thesis": "Globalny biznes zarabia biliony dolarów na darmowym kodzie open-source, nie przeznaczając niemal nic na wynagrodzenia dla jego twórców. To pasożytniczy model, który otwiera wrota dla agentów obcych wywiadów przejmujących kontrolę nad porzuconymi projektami.",
                "points": [
                    "Przypadek ataku na XZ Utils: Jak cierpliwa infiltracja jednego wolontariusza o krok nie doprowadziła do globalnego paraliżu serwerów Linux.",
                    "Wypalenie twórców: Dlaczego programiści porzucają kluczowe projekty używane przez miliony firm.",
                    "Konieczność państwowego i korporacyjnego finansowania krytycznej infrastruktury otwartego oprogramowania.",
                    "Pytanie dociekliwego laika: Dlaczego największe korporacje świata płacą miliardy za prawników i marketing, a żałują kilku tysięcy dolarów człowiekowi, na którego darmowym kodzie stoi cała ich firma?"
                ]
            },
            {
                "num": 2,
                "cat_display": "Gospodarka / Przemysł Europejski i Niemcy",
                "category": "gospodarka",
                "title": "Koniec niemieckiego cudu gospodarczego: Jak kryzys w Berlinie uderzy w polskie portfele",
                "search_date": "22 października 2026 r.",
                "source_display": "🇬🇧 The Financial Times / OSW",
                "source_note": "Analiza Financial Times i OSW o stagnacji niemieckiego sektora motoryzacyjnego, drogiej energii i problemach Volkswagena.",
                "image_url": "https://images.unsplash.com/photo-1503376780353-7e6692767b70?auto=format&fit=crop&w=1200&q=80",
                "image_concept": "Nowoczesny samochód w hali fabrycznej w chłodnym, surowym oświetleniu przemysłowym.",
                "image_prompt": "Automotive assembly line in Germany with luxury car silhouette under cold factory lights, European industrial stagnation theme, 8k.",
                "lead": "Przez dekady gospodarka Niemiec opierała się na trzech filarach: taniej energii z Rosji, chłonnym rynku zbytu w Chinach i gwarancjach bezpieczeństwa z USA. W 2026 roku żaden z tych filarów już nie istnieje.",
                "thesis": "Niemcy to największy partner handlowy Polski. Każda redukcja etatów w fabrykach w Stuttgarcie i Wolfsburgu oznacza wstrzymanie zamówień u setek polskich kooperantów na Śląsku i w Wielkopolsce.",
                "points": [
                    "Spóźniona rewolucja elektromobilności: Jak niemieckie koncerny przespały rozwój chińskich aut elektrycznych i oprogramowania.",
                    "Brak inwestycji w infrastrukturę: Pękające mosty, opóźnienia pociągów Deutsche Bahn i biurokracja za Odrą.",
                    "Szansa na emancypację polskiego biznesu: Czy polskie firmy potrafią znaleźć rynki zbytu poza niemieckim łańcuchem dostaw.",
                    "Pytanie dociekliwego laika: Skoro ponad jedna czwarta polskiego eksportu trafia do Niemiec, dlaczego wciąż udajemy, że kłopoty naszego sąsiada nas nie dotyczą?"
                ]
            },
            {
                "num": 3,
                "cat_display": "Polityka / Dyplomacja i Europa Środkowa",
                "category": "polityka",
                "title": "Trójkąt Weimarski a wschodnia flanka: Czy Paryż i Berlin są gotowe na polskie przywództwo w regionie?",
                "search_date": "22 października 2026 r.",
                "source_display": "🇵🇱 Kultura Liberalna / Nowa Konfederacja",
                "source_note": "Esej w Kulturze Liberalnej i komentarz Nowej Konfederacji na temat relacji Warszawa-Berlin-Paryż w dobie wojny w Europie.",
                "image_url": "https://images.unsplash.com/photo-1529107386315-e1a2ed48a620?auto=format&fit=crop&w=1200&q=80",
                "image_concept": "Flagi państw europejskich powiewające przed gmachem instytucji dyplomatycznej w chłodnym świetle.",
                "image_prompt": "European national flags waving outside modern diplomatic institution building, solemn cloudy sky, European geopolitics and leadership theme, 8k.",
                "lead": "Wojna w Ukrainie bezpowrotnie przesunęła środek ciężkości europejskiej geopolityki na wschód. Polska, wydająca blisko 5% PKB na obronność, stała się kluczowym filarem bezpieczeństwa całego kontynentu.",
                "thesis": "Sama potęga militarna nie wystarczy do realnego przywództwa. Bez zdolności budowania sojuszy w regionie i mądrego współdziałania z Francją i Niemcami Polska nie zdoła przekuć swoich wydatków na trwałe wpływy polityczne.",
                "points": [
                    "Renesans Trójkąta Weimarskiego: Czy Warszawa potrafi być partnerem, a nie tylko petentem Berlina i Paryża.",
                    "Różnice percepcji zagrożenia: Dlaczego dla Francji priorytetem pozostaje Morze Śródziemne i Afryka, a dla Polski granica wschodnia.",
                    "Budowa pozycji lidera Europy Środkowej: Relacje z państwami bałtyckimi, Rumunią i Skandynawią.",
                    "Pytanie dociekliwego laika: Czy chcemy być wyłącznie 'państwem frontowym' kupującym najwięcej czołgów, czy krajem potrafiącym współtworzyć strategiczne decyzje całej Europy?"
                ]
            },
            {
                "num": 4,
                "cat_display": "Społeczeństwo / Wolność Słowa i Kultura",
                "category": "eseje",
                "title": "Kultura unieważniania (cancel culture) a wolność dyskusji: Gdzie leży granica między odpowiedzialnością a linczem?",
                "search_date": "22 października 2026 r.",
                "source_display": "🇵🇱 Kultura Liberalna / Klub Jagielloński / Kanał Zero",
                "source_note": "Debata w Kulturze Liberalnej i dyskusja na Kanale Zero o granicach swobody wypowiedzi na uniwersytetach i w korporacjach.",
                "image_url": "https://images.unsplash.com/photo-1455390582262-044cdead277a?auto=format&fit=crop&w=1200&q=80",
                "image_concept": "Otwarte stare pióro na pożółkłym papierze rękopisu w ciepłym świetle zabytkowego biurka.",
                "image_prompt": "Close-up of vintage fountain pen on handwritten manuscript paper, quiet atmospheric study lighting, free speech and intellectual freedom theme, 8k.",
                "lead": "Jeden niefortunny wpis w mediach społecznościowych sprzed dziesięciu lat potrafi dziś zniszczyć karierę naukowca, artysty czy przedsiębiorcy. Społeczny lincz zastąpił salę sądową i spokojną polemikę.",
                "thesis": "Kultura unieważniania tworzy atmosferę paraliżującego strachu, w której nikt nie odważy się postawić trudnego pytania ani zakwestionować obowiązującej ortodoksji. Bez prawa do błędu i dyskusji nie ma mowy o rozwoju naukowym i intelektualnym.",
                "points": [
                    "Różnica między pociągnięciem kogoś do odpowiedzialności za kłamstwo a internetowym polowaniem na czarownice.",
                    "Autocenzura na uniwersytetach: Dlaczego profesorowie unikają trudnych tematów w obawie przed skargami aktywistów.",
                    "Jak odzyskać kulturę publicznej polemiki, w której krytykuje się argumenty, a nie niszczy człowieka.",
                    "Pytanie dociekliwego laika: Czy świat, w którym wszyscy boją się powiedzieć to, co myślą, z obawy przed utratą pracy, jest jeszcze wolnym społeczeństwem?"
                ]
            }
        ]
    }
]

def generate_file_content(day):
    lines = []
    lines.append("# 📑 Propozycje Tematów i Konspektów Redakcyjnych — Blog Laika")
    lines.append(f"**Data przygotowania:** {day['date_pl']} ({day['day_name'].lower()})  ")
    lines.append(f"**Data wyszukania i analizy trendów:** {day['search_date']}  ")
    lines.append("**Autor bloga:** Ireneusz Machowiec  ")
    lines.append("**Profil tematyczny:** Technologia, gospodarka, geopolityka i społeczeństwo — rzetelne, autorskie wpisy blogowe.  ")
    lines.append("**Standard redakcyjny:** 100% Samokreacja — autorska synteza faktów rynkowych z perspektywy dociekliwego laika (całkowity brak zapożyczeń tekstowych).")
    lines.append("")
    lines.append("---")
    lines.append("")

    for t in day["topics"]:
        lines.append(f"## {t['num']}. {t['cat_display']}: „{t['title']}”")
        lines.append("")
        lines.append(f"* **Kategoria:** `{t['category']}`")
        lines.append(f"* **Data wyszukania:** {t['search_date']}")
        lines.append(f"* **Model powstawania:** 100% Samokreacja (autorska synteza faktów, zero zapożyczeń)")
        if t.get("source_display"):
            lines.append(f"* **Źródło impulsu:** {t['source_display']}")
        if t.get("source_note"):
            lines.append(f"* **Wątek źródłowy:** {t['source_note']}")
        lines.append(f"* **Proponowana grafika:** {t['image_url']}")
        lines.append(f"* **Koncepcja wizualna:** {t['image_concept']}")
        lines.append(f"* **Prompt AI dla grafiki:** `{t['image_prompt']}`")
        lines.append(f"* **Lead:** {t['lead']}")
        lines.append(f"* **Kluczowa teza wpisu:**  ")
        lines.append(f"  *{t['thesis']}*")
        lines.append("* **Kluczowe wątki i konspekt wpisu:**")
        for i, pt in enumerate(t["points"], 1):
            if pt.startswith("Pytanie dociekliwego laika:"):
                lines.append(f"  {i}. **Pytanie dociekliwego laika:** *{pt.replace('Pytanie dociekliwego laika:', '').strip()}*")
            else:
                lines.append(f"  {i}. {pt}")
        lines.append("")
        lines.append("---")
        lines.append("")

    return "\n".join(lines)

def main():
    target_dirs = [
        r"G:\Mój dysk\blog-laika\propozycje-tematow",
        r"C:\Users\irene\blog-laika\propozycje-tematow"
    ]

    import sys
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if root_dir not in sys.path:
        sys.path.insert(0, root_dir)
    import proposals_manager

    for d in target_dirs:
        os.makedirs(d, exist_ok=True)
        for day in DIVERSE_DAYS_DATA:
            fn = f"propozycje-{day['date']}.md"
            fp = os.path.join(d, fn)
            content = generate_file_content(day)
            with open(fp, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"Zapisano {fp} (4 tematy z grafikami i źródłami, data: {day['date']})")
        
        # Enforce 7-day retention
        retained = proposals_manager.enforce_retention(d, max_days=7)
        print(f"[Rotacja] Zachowano {len(retained)} zestawów (7 dni x 4 = 28 tematów) w {d}")

if __name__ == "__main__":
    main()

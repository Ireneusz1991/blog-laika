from database import create_post, get_posts, init_db

SAMPLE_POSTS = [
    {
        "title": "Architektura uwagi: Czy modele AI naprawdę myślą, czy tylko bezbłędnie zgadują?",
        "slug": "architektura-uwagi-czy-ai-mysli",
        "category": "technologia",
        "tags": "sztuczna inteligencja, technologia, transformery, filozofia umyslu",
        "cover_image": "https://images.unsplash.com/photo-1620712943543-bcc4688e7485?auto=format&fit=crop&w=1200&q=80",
        "featured": 0,
        "content_markdown": """# Architektura uwagi: Czy modele AI naprawdę myślą?

Kiedy po raz pierwszy prowadzimy dłuższą rozmowę z zaawansowanym modelem sztucznej inteligencji, trudno oprzeć się złudzeniu, że po drugiej stronie ekranu ktoś siedzi. Odpowiedzi są dowcipne, strukturyzowane, nasycone erudycją. Jednak gdy zajrzymy pod maskę, napotykamy fundamentalne pytanie: **gdzie kończy się zaawansowana statystyka, a zaczyna rozumienie?**

## Mechanizm Attention – rewolucja roku 2017

Kluczowy przełom nastąpił w 2017 roku wraz z publikacją słynnej pracy badaczy Google pt. *„Attention Is All You Need”*. Zamiast sekwencyjnie przetwarzać słowo po słowie, modele typu Transformer nauczyły się analizować relacje między wszystkimi wyrazami w całym dokumencie jednocześnie.

- **Kontekst dynamiczny**: Słowo *„zamek”* w zdaniu o średniowieczu zyskuje zupełnie inne powiązania niż to samo słowo w tekście o kurtkach zimowych czy zamkach do drzwi.
- **Skalowanie obliczeniowe**: Zwiększenie liczby parametrów i danych treningowych ujawniło tzw. *zdolności emergentne* (właściwości wyłaniające się nagle przy odpowiedniej skali).

```python
# Uproszczona idea mechanizmu uwagi:
# Attention(Q, K, V) = softmax(Q * K^T / sqrt(d_k)) * V
```

## Papuga stochastyczna czy nowy rodzaj umysłu?

Krytycy, tacy jak Emily Bender czy Timnit Gebru, ukuły termin **„stochastyczna papuga”** (*stochastic parrot*). Według tej tezy model nie ma pojęcia o świecie fizycznym ani o prawdzie; jest jedynie genialnym symulatorem prawdopodobieństwa wystąpienia kolejnego tokena.

Z drugiej strony zwolennicy koncepcji *world models* (modeli świata) argumentują, że aby wiarygodnie przewidzieć kolejne słowo w złożonych tekstach opisujących fizykę, szachy czy emocje, sieć **musi wewnętrznie zbudować uproszczoną reprezentację rzeczywistości**.

Niezależnie od definicji świadomości, jedno jest pewne: granica między „mechanicznym powtarzaniem” a „twórczym syntetyzowaniem” została bezpowrotnie zatarta.
"""
    },
    {
        "title": "Złudzenie taniego kapitału: Dlaczego dekada zerowych stóp procentowych zmieniła wszystko",
        "slug": "zludzenie-taniego-kapitalu-zerowe-stopy",
        "category": "gospodarka",
        "tags": "gospodarka, makroekonomia, finanse, inflacja, banki centralne",
        "cover_image": "https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?auto=format&fit=crop&w=1200&q=80",
        "featured": 0,
        "content_markdown": """# Złudzenie taniego kapitału: Lekcja z dekady zerowych stóp

Przez ponad dziesięć lat po kryzysie finansowym z 2008 roku świat zachodni funkcjonował w warunkach bezprecedensowego eksperymentu monetarnego. Pieniądz był praktycznie darmowy, a stopy procentowe banków centralnych w strefie euro czy Japonii spadały poniżej zera.

Dla przeciętnego obserwatora brzmiało to jak złoty wiek: tanie kredyty hipoteczne, dynamiczny wzrost wycen startupów technologicznych, eksplozja platform cyfrowych. Jednak ekonomia rzadko oferuje darmowe obiady.

---

## Skutki uboczne sztucznie zaniżonego kosztu ryzyka

Gdy cena pieniądza (czyli stopa procentowa) wynosi zero, tradycyjna selekcja rynkowa przestaje działać sprawnie:

1. **Firmy zombie**: Podmioty, które w normalnych warunkach zbankrutowałyby ze względu na brak rentowności, mogły latami rolować dług po mikroskopijnych kosztach.
2. **Inflacja aktywów**: Tani kapitał nie trafiał do realnych fabryk czy infrastruktury w takim stopniu, jak do rynków nieruchomości, akcji technologicznych czy kryptowalut.
3. **Rozwarstwienie majątkowe**: Posiadacze kapitału i nieruchomości gwałtownie się bogacili, podczas gdy osoby żyjące wyłącznie z pracy etatowej traciły zdolność nabywczą mieszkania.

## Powrót grawitacji

Kiedy w latach 2021-2023 powróciła wysoka inflacja wymuszająca gwałtowne podwyżki stóp, wielu uczestników rynku przeżyło szok poznawczy. Okazało się, że projekty rentowne tylko przy stopie 0% przestają mieć sens przy stopie 5%.

Prawdziwym wyzwaniem kolejnej dekady nie będzie wyłącznie walka ze wskaźnikiem CPI, lecz odnalezienie równowagi w świecie, w którym kapitał znów ma swoją cenę.
"""
    },
    {
        "title": "Nowy koncert mocarstw: Od wolnego handlu do geopolitycznej autarkii",
        "slug": "nowy-koncert-mocarstw-geopolityka",
        "category": "polityka",
        "tags": "polityka, geopolityka, globalizacja, bezpieczenstwo",
        "cover_image": "https://images.unsplash.com/photo-1541872703-74c5e44368f9?auto=format&fit=crop&w=1200&q=80",
        "featured": 0,
        "content_markdown": """# Nowy koncert mocarstw: Od wolnego handlu do geopolitycznej autarkii

Początek lat 90. przyniósł słynną tezę Francisa Fukuyamy o „końcu historii”. Powszechnie wierzono, że wolny handel, wzajemne powiązania gospodarcze i globalne łańcuchy dostaw uczynią wojny między mocarstwami czystym ekonomicznym absurdem. Niemiecka koncepcja *Wandel durch Handel* (zmiana poprzez handel) była sztandarową doktryną tego okresu.

Dziś, z perspektywy połowy lat 20., widzimy, jak bardzo te nadzieje były naiwne.

---

## Broń ukryta w łańcuchach dostaw (*Weaponized Interdependence*)

Globalizacja nie zlikwidowała rywalizacji mocarstw – przekształciła jedynie jej oręż. Okazało się, że w świecie ciasnych powiązań kluczowa staje się kontrola nad tzw. **wąskimi gardłami** (*chokepoints*):

- **Półprzewodniki**: Maszyny litograficzne EUV (holenderskie ASML) i zaawansowane fabryki na Tajwanie (TSMC) stały się ważniejszym obiektem strategicznym niż bazy wojskowe.
- **Surowce krytyczne**: Pierwiastki ziem rzadkich, lit, kobalt i grafit – bez nich transformacja energetyczna i elektromobilność pozostają mrzonką.
- **Infrastruktura danych**: Kable podmorskie, chmury obliczeniowe i systemy satelitarne.

## Czy to koniec globalizacji?

Nie mamy do czynienia z prostym cofnięciem się do XIX wieku, lecz z procesem określanym jako **de-risking** i **friendshoring**. Państwa nie rezygnują z handlu międzynarodowego, lecz przenoszą kluczowe węzły produkcyjne do sojuszników politycznych.

Świat staje się bardziej podzielony, droższy i bardziej nieprzewidywalny. Dla laika obserwującego te procesy płynie z tego jedna kluczowa lekcja: **nigdy nie bierz stabilności za pewnik**.
"""
    },
    {
        "title": "Anatomia kryzysu sueskiego 1956: Dzień, w którym Europa zrozumiała, że nie jest już centrum świata",
        "slug": "kryzys-sueski-1956-lekcja-historii",
        "category": "historia",
        "tags": "historia, geopolityka, suez, ropa, wielka brytania, suwerennosc, imperia",
        "cover_image": "https://images.unsplash.com/photo-1544620347-c4fd4a3d5957?auto=format&fit=crop&w=1200&q=80",
        "featured": 0,
        "content_markdown": """# Anatomia kryzysu sueskiego 1956: Lekcja utraconej suwerenności

Jesienią 1956 roku rządy Wielkiej Brytanii i Francji, w porozumieniu z Izraelem, rozpoczęły tajną operację militarną mającą na celu odzyskanie kontroli nad znacjonalizowanym przez Gamala Abdela Nasera Kanałem Sueskim. Z wojskowego punktu widzenia operacja „Muszkieter” była niemal natychmiastowym sukcesem – desant spadochroniarzy błyskawicznie zabezpieczył newralgiczne punkty korytarza morskiego.

Mimo to w ciągu zaledwie kilkudziesięciu godzin dumne europejskie mocarstwa zostały zmuszone do bezwarunkowej i upokarzającej kapitulacji. Jak do tego doszło?

---

## Broń finansowa silniejsza od pancerników

Kluczowy cios nie padł na piaskach Synaju ani w wodach Port Saidu. Zadał go prezydent USA Dwight Eisenhower, sięgając po narzędzie, które do dziś decyduje o losach globalnej geopolityki: **panikę na rynku walutowym i szantaż rezerwami kapitałowymi**.

1. **Atak na funta szterlinga**: Waszyngton zagroził wyprzedażą brytyjskich obligacji rządowych, co doprowadziłoby do natychmiastowego załamania kursu funta i bankructwa Banku Anglii.
2. **Kran z ropą naftową**: Stany Zjednoczone zablokowały dostawy ropy z Zatoki Meksykańskiej do Europy, dopóki wojska koalicji nie wycofają się z Egiptu.
3. **Weto w MFW**: Administracja USA zablokowała brytyjski wniosek o pożyczkę ratunkową z Międzynarodowego Funduszu Walutowego.

## Czego uczy nas Suez w XXI wieku?

Dla dociekliwego obserwatora historii kryzys sueski to nie zakurzony podręcznikowy epizod, lecz fundamentalne studium mechanizmów władzy:

- **Złudzenie dawnej potęgi**: Państwa często podejmują decyzje strategiczne w oparciu o pamięć o swojej dawnej sile, ignorując zmianę globalnego układu bilansu kapitałowego.
- **Suwerenność ma cenę w rezerwach**: Nie można prowadzić niezależnej polityki zagranicznej, będąc zadłużonym u podmiotu, którego interesy w danym regionie są odmienne od naszych.
- **Wąskie gardła geograficzne**: Cieśniny, kanały żeglugowe i rurociągi są od wieków tym samym – punktami nacisku, w których lokalny konflikt może sparaliżować gospodarki oddalone o tysiące kilometrów.

Lekcja z 1956 roku brzmi chłodno: armia bez suwerenności finansowej i energetycznej jest tylko kosztowną dekoracją.
"""
    },
    {
        "title": "Pochwała dociekliwego laika: Dlaczego w epoce wąskich specjalizacji najbardziej potrzebujemy spojrzenia z zewnątrz",
        "slug": "pochwala-dociekliwego-laika",
        "category": "eseje",
        "tags": "eseje, filozofia laika, edukacja, spoleczenstwo, krytyczne myslenie",
        "cover_image": "https://images.unsplash.com/photo-1497633762265-9d179a990aa6?auto=format&fit=crop&w=1200&q=80",
        "featured": 0,
        "content_markdown": """# Pochwała dociekliwego laika: Spojrzenie z zewnątrz

Współczesny świat nagradza hiper-specjalizację. Od inżynierów oprogramowania, przez analityków finansowych, po lekarzy i politologów – każdy zamyka się we własnym hermetycznym żargonie, własnych konferencjach i wąskich modelach myślowych. Zjawisko to przyniosło olbrzymi postęp techniczny, lecz stworzyło zarazem groźną lukę: **niemal nikt nie łączy kropek między poszczególnymi dziedzinami**.

Właśnie w tym miejscu pojawia się postać dociekliwego laika.

---

## Naiwne pytania jako najpotężniejsze narzędzie poznania

Ekspert często cierpi na tzw. klątwę wiedzy (*curse of knowledge*). Gdy spędziłeś dekadę na optymalizacji jednego algorytmu lub jednej procedury podatkowej, pewne założenia stają się dla Ciebie przezroczyste jak powietrze. Nie podważasz ich, bo stanowią fundament Twojej dyscypliny.

Dociekliwy laik ma przywilej zadawania pytań z pozoru dziecinnych, które burzą skostniałe dogmaty:
- *„Dlaczego właściwie ten system musi tak działać?”*
- *„Jaki jest rzeczywisty cel tej procedury, poza tym, że robimy to od dwudziestu lat?”*
- *„Co się stanie, gdy jedno założenie wyjściowe okaże się błędne?”*

Największe innowacje rzadko powstają w samym centrum ugruntowanej branży; najczęściej rodzą się na jej peryferiach, gdy ktoś przynosi mentalne modele z zupełnie innej dyscypliny.

## Odwaga myślenia wbrew szumowi informacyjnemu

Być dociekliwym laikiem nie oznacza ignorancji. Wręcz przeciwnie – oznacza to pokorę wobec złożoności świata połączoną z odmową biernej konsumpcji gotowych haseł. Oznacza gotowość do czytania pierwotnych raportów zamiast nagłówków w mediach społecznościowych, do sprawdzania liczb w oficjalnych statystykach i do konfrontowania sprzecznych punktów widzenia.

W świecie zalanym płytką sensacją, umiejętność zatrzymania się i zadania jednego rzetelnego pytania: *„Zaraz, jak to naprawdę działa?”* – staje się najcenniejszą formą intelektualnej suwerenności.
"""
    }
]

def seed_database():
    init_db()
    existing = get_posts(status="all", limit=1)
    if not existing:
        for p in SAMPLE_POSTS:
            create_post(
                title=p["title"],
                content_markdown=p["content_markdown"],
                category=p["category"],
                slug=p["slug"],
                tags=p["tags"],
                cover_image=p["cover_image"],
                featured=p["featured"]
            )
        print("Sample posts seeded successfully.")
    else:
        print("Database already contains posts.")

if __name__ == "__main__":
    seed_database()

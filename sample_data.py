from database import create_post, get_posts, init_db

SAMPLE_POSTS = [
    {
        "title": "Pochwała dociekliwego laika: Dlaczego warto zadawać naiwne pytania w skomplikowanym świecie",
        "slug": "pochwala-dociekliwego-laika",
        "category": "eseje",
        "tags": "filozofia, eseje, myslenie, ciekawosc",
        "cover_image": "https://images.unsplash.com/photo-1457369804613-52c61a468e7d?auto=format&fit=crop&w=1200&q=80",
        "featured": 1,
        "content_markdown": """# Pochwała dociekliwego laika

Żyjemy w epoce wąskiej hiper-specjalizacji. Aby czuć się uprawnionym do zabrania głosu w jakiejkolwiek dyskusji, współczesna kultura zdaje się wymagać certyfikatu, doktoratu lub przynajmniej dziesięciu lat pracy w danej niszy. Jeśli wypowiadasz się o sztucznej inteligencji, powinieneś pisać o architekturze transformera. Jeśli o inflacji – o krzywej Phillipsa. Jeśli o polityce zagranicznej – znać na wyrywki historię traktatów granicznych.

Ale czy na pewno?

Często to właśnie **laik** – osoba patrząca z zewnątrz, nieobarczona branżowym żargonem ani lojalnością wobec akademickich dogmatów – potrafi zadać najbardziej niewygodne i odkrywcze pytanie: *„Zaraz, ale dlaczego właściwie to tak działa?”*.

---

## Wolność od klątwy wiedzy

Psychologia poznawcza od dawna zna zjawisko zwane **klątwą wiedzy** (*curse of knowledge*). Kiedy ekspert przez dekady bada jeden problem, struktura jego myślenia staje się tak zoptymalizowana pod istniejące reguły, że przestaje widzieć fundamenty, na których te reguły stoją.

> „Ekspert to człowiek, który popełnił wszystkie możliwe błędy w bardzo wąskiej dziedzinie.”  
> — Niels Bohr

Laik ma ten przywilej, że może łączyć kropki ponad silosami. Gdy patrzy na rozwój modeli LLM, widzi nie tylko wagi wag sieci neuronowych, lecz dynamikę społeczną przypominającą rewolucję druku Gutenberga. Kiedy analizuje politykę energetyczną, nie gubi się w tabelach bilansowych, lecz dostrzega odwieczną walkę o hegemonię surowcową.

## Dlaczego powstał Blog Laika?

Ten blog nie ma aspiracji akademickiego podręcznika ani wyroczni. To dziennik intelektualnych poszukiwań. Zasada, którą się tu kierujemy, jest prosta:

1. **Szacunek dla faktów** – logika i rzetelność są nienegocjowalne.
2. **Odrzucenie żargonu** – jeśli jakiejś koncepcji nie da się wytłumaczyć prostymi słowami, prawdopodobnie sami jej jeszcze dostatecznie nie rozumiemy.
3. **Wielodyscyplinarność** – technologia wpływa na gospodarkę, gospodarka dyktuje politykę, a polityka kształtuje ramy naszego życia.

Zapraszam do wspólnej lektury, polemiki i zadawania kolejnych prostych, lecz niełatwych pytań.
"""
    },
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

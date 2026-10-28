# Python Knowledge Base — globalna powtórka

Przekrojowe notatki po polsku: od podstaw języka po testowanie, API, współbieżność i praktyki przydatne w DevOps oraz AI Engineering.

**Jak korzystać:** przeczytaj definicję, przewidź wynik przykładu, uruchom go, a następnie odpowiedz własnymi słowami na pytanie. Przykłady dotyczą Python 3.11+; cechy zależne od implementacji są opisane osobno.

## Mapa powtórki

| Etap | Tematy | Cel |
| --- | --- | --- |
| Podstawy | Typy, kolekcje, operatory, sterowanie | Rozumieć działanie prostego programu |
| Funkcje i obiekty | Argumenty, zakresy, OOP, dataclasses | Pisać czytelny, podzielony kod |
| Mechanizmy języka | Iteratory, generatory, dekoratory, kontekst | Rozumieć typowe idiomy |
| Praca z danymi | Pliki, JSON, CSV, SQL, daty | Bezpiecznie przetwarzać dane |
| Aplikacje | HTTP, API, async, konfiguracja | Budować integracje i usługi |
| Jakość | Testy, typing, logi, bezpieczeństwo | Utrzymywać i diagnozować kod |
| Rekrutacja | Pułapki, złożoność, ćwiczenia | Wyjaśniać wybory i rozwiązywać zadania |

## Spis treści

1. [Jak działa Python](#1-jak-działa-python)
2. [Typy, referencje i mutowalność](#2-typy-referencje-i-mutowalność)
3. [Kolekcje i złożoność](#3-kolekcje-i-złożoność)
4. [Operatory i sterowanie](#4-operatory-i-sterowanie)
5. [Napisy i kodowanie](#5-napisy-i-kodowanie)
6. [Funkcje i argumenty](#6-funkcje-i-argumenty)
7. [Zakresy, closures i lambda](#7-zakresy-closures-i-lambda)
8. [Comprehensions i narzędzia wbudowane](#8-comprehensions-i-narzędzia-wbudowane)
9. [Iteratory i generatory](#9-iteratory-i-generatory)
10. [Dekoratory i context managers](#10-dekoratory-i-context-managers)
11. [OOP i dataclasses](#11-oop-i-dataclasses)
12. [Typowanie i walidacja](#12-typowanie-i-walidacja)
13. [Wyjątki](#13-wyjątki)
14. [Moduły, pakiety i środowisko](#14-moduły-pakiety-i-środowisko)
15. [Pliki, JSON, CSV i daty](#15-pliki-json-csv-i-daty)
16. [SQL i transakcje](#16-sql-i-transakcje)
17. [HTTP i API](#17-http-i-api)
18. [Async, wątki, procesy i GIL](#18-async-wątki-procesy-i-gil)
19. [Testowanie](#19-testowanie)
20. [Logowanie i diagnostyka](#20-logowanie-i-diagnostyka)
21. [Bezpieczeństwo i jakość](#21-bezpieczeństwo-i-jakość)
22. [Python w DevOps i AI](#22-python-w-devops-i-ai)
23. [Pułapki i pytania rekrutacyjne](#23-pułapki-i-pytania-rekrutacyjne)
24. [Ćwiczenia i plan powtórki](#24-ćwiczenia-i-plan-powtórki)
25. [Materiały w repozytorium i źródła](#25-materiały-w-repozytorium-i-źródła)

## 1. Jak działa Python

Python to język wysokiego poziomu z dynamicznym typowaniem. Obiekty mają typ, a nazwy odnoszą się do obiektów.

W **CPythonie** kod jest kompilowany do bytecode, który wykonuje interpreter. Pliki `.pyc` mogą przechowywać cache bytecode. Określenie „interpretowany” nie oznacza, że kompilacji nie ma.

- **Dynamiczne typowanie:** nazwa może zostać powiązana z obiektami różnych typów.
- **Silne typowanie:** Python zwykle nie wykonuje dowolnych niejawnych konwersji między niezgodnymi typami, np. `"3" + 2` zgłasza błąd.
- **Duck typing:** liczy się obsługiwane zachowanie obiektu, nie tylko jego konkretna klasa.
- Wcięcia wyznaczają bloki; konwencja to 4 spacje.
- PEP 8 opisuje konwencje stylu; czytelność ma znaczenie.

**Pytanie:** dlaczego „Python jest interpretowany” to uproszczenie?

## 2. Typy, referencje i mutowalność

| Typ | Przykład | Mutowalny? | Typowe zastosowanie |
| --- | --- | --- | --- |
| int | 42 | Nie | Liczniki, indeksy |
| float | 3.14 | Nie | Obliczenia przybliżone |
| bool | True | Nie | Warunki |
| str | "agent" | Nie | Tekst Unicode |
| list | [1, 2] | Tak | Sekwencja zmiennych danych |
| tuple | (1, 2) | Nie, ale element może być mutowalny | Stała struktura wartości |
| dict | {"status": "ok"} | Tak | Mapowanie klucz → wartość |
| set | {1, 2} | Tak | Unikalność i operacje zbiorowe |
| frozenset | frozenset({1, 2}) | Nie | Niezmienny zbiór |
| bytes | b"abc" | Nie | Dane binarne |
| NoneType | None | Nie | Brak wartości |

Przypisanie nie kopiuje obiektu:

```python
a = [1, 2]
b = a
b.append(3)
assert a == [1, 2, 3]
assert a is b
```

**Mutacja** zmienia obiekt. **Ponowne przypisanie** wiąże nazwę z innym obiektem.

```python
a = [1]
b = a
a = [2]
assert b == [1]
```

- `==` porównuje wartości według definicji typu.
- `is` sprawdza tożsamość obiektu. Do sprawdzania braku wartości używaj `x is None`.
- `copy.copy()` i `list.copy()` robią kopię płytką; obiekty zagnieżdżone pozostają współdzielone.
- `copy.deepcopy()` kopiuje rekurencyjnie z uwzględnieniem mechanizmu kopiowania danego typu.

```python
from copy import deepcopy

original = [[1], [2]]
shallow = original.copy()
deep = deepcopy(original)
shallow[0].append(9)

assert original == [[1, 9], [2]]
assert deep == [[1], [2]]
```

Liczby float reprezentują wiele ułamków tylko przybliżenie. Do porównań numerycznych używaj np. `math.isclose()`, a do dokładnej arytmetyki dziesiętnej rozważ `Decimal` tworzony z napisu.

## 3. Kolekcje i złożoność

| Struktura / operacja | Typowa złożoność | Uwaga |
| --- | --- | --- |
| list: dostęp po indeksie | O(1) | Przechowuje uporządkowaną sekwencję |
| list: wyszukiwanie wartości | O(n) | Sprawdza kolejne elementy |
| list: append | Zamortyzowane O(1) | Pojedyncza realokacja może kosztować więcej |
| list: wstawienie/usunięcie na początku | O(n) | Przesunięcie elementów |
| dict: odczyt po kluczu | Średnio O(1) | Najgorszy przypadek może być O(n) |
| set: sprawdzanie przynależności | Średnio O(1) | Wymaga hashowalnych elementów |
| sorted | O(n log n) w najgorszym przypadku | Tworzy nową listę |
| deque: append/popleft | O(1) | Dobry wybór dla kolejki |

To typowe charakterystyki implementacji, a nie gwarancja stałego czasu każdej operacji.

Klucze słownika i elementy zbioru muszą być **hashowalne**: hash musi być stabilny przez czas życia obiektu, a równe obiekty muszą mieć ten sam hash. Lista nie jest hashowalna. Krotka jest hashowalna, jeśli wszystkie jej elementy są hashowalne.

- `dict` zachowuje kolejność wstawiania; nie sortuje kluczy automatycznie.
- `set` nie gwarantuje kolejności do wykorzystania w logice programu.
- `list.sort()` zmienia listę i zwraca `None`.
- `sorted(iterable)` zwraca nową listę.
- `append(x)` dodaje jeden element, a `extend(iterable)` dodaje elementy z iterable.

Przydatne: `collections.Counter`, `defaultdict`, `deque`.

## 4. Operatory i sterowanie

| Zapis | Znaczenie |
| --- | --- |
| / | Dzielenie, zwykle wynik float dla int |
| // | Dzielenie z zaokrągleniem w dół, także dla liczb ujemnych |
| % | Reszta zgodna z regułą dzielenia Pythona |
| ** | Potęgowanie |
| in | Przynależność |
| and / or | Zwracają jeden z operandów, niekoniecznie bool |
| not | Negacja logiczna, zwraca bool |

Fałszywe są m.in. `None`, `False`, zero i puste kolekcje. **Nie myl zera z brakiem danych.**

```python
value = 0
result = value if value is not None else 10
assert result == 0
assert (value or 10) == 10
assert -3 // 2 == -2
```

- `break` kończy pętlę, `continue` przechodzi do następnej iteracji.
- `else` przy pętli wykonuje się, gdy pętla skończyła się bez `break`.
- `range(3)` daje 0, 1, 2; granica końcowa jest wyłączna.
- `match/case` służy do dopasowania wzorców, nie tylko porównania wartości.
- Nie modyfikuj rozmiaru iterowanej kolekcji bez świadomego planu; często lepiej zbudować nową.

## 5. Napisy i kodowanie

`str` to tekst Unicode, `bytes` to bajty. `encode()` zamienia tekst na bajty, `decode()` wykonuje operację odwrotną.

```python
text = "Zażółć"
raw = text.encode("utf-8")
assert raw.decode("utf-8") == text

names = ["Ada", "Joanna"]
assert ", ".join(names) == "Ada, Joanna"
assert "  ok\n".strip() == "ok"
assert "a,b,c".split(",") == ["a", "b", "c"]
assert "python"[1:4] == "yth"
```

- Slicing ma postać `start:stop:step`; stop jest wyłączny.
- `strip("ab")` usuwa wskazane znaki z obu końców, a nie dokładny prefiks „ab”.
- Do dokładnego prefiksu/sufiksu używaj `removeprefix()` / `removesuffix()`.
- `f"{name}"` ułatwia formatowanie; nie zapewnia ochrony przed SQL injection.
- Przy regexach przydaje się raw string, np. `r"\d+"`.
- Przy niezaufanych regexach lub danych uwzględnij koszt obliczeniowy i długość wejścia.

## 6. Funkcje i argumenty

```python
def describe(name: str, /, *, active: bool = True) -> str:
    return f"{name}: {active}"

assert describe("agent", active=False) == "agent: False"
```

- Parametry przed `/` są positional-only.
- Parametry po `*` są keyword-only.
- `*args` zbiera argumenty pozycyjne do krotki.
- `**kwargs` zbiera argumenty nazwane do słownika.
- `return` kończy funkcję; brak jawnego `return` oznacza zwrot `None`.
- Funkcja może zwrócić wiele wartości przez jedną krotkę, np. `return status, message`.

### Pułapka: mutowalny argument domyślny

Wartości domyślne obliczane są przy definiowaniu funkcji. `items=[]` może współdzielić listę między wywołaniami.

```python
def add_item(value: int, items: list[int] | None = None) -> list[int]:
    if items is None:
        items = []
    items.append(value)
    return items

assert add_item(1) == [1]
assert add_item(2) == [2]
```

Argumenty przekazywane są przez współdzielenie referencji do obiektów. Mutacja przekazanej listy może być widoczna u wywołującego; ponowne przypisanie lokalnego parametru nie zmienia jego nazwy u wywołującego.

## 7. Zakresy, closures i lambda

**LEGB:** Local → Enclosing → Global → Builtins.

- `global` pozwala przypisać nazwę z zakresu modułu.
- `nonlocal` pozwala przypisać istniejącą nazwę w otaczającym zakresie funkcji.
- Closure to funkcja korzystająca ze zmiennych otaczającego zakresu.
- `lambda` jest krótką funkcją z jednym wyrażeniem; nie zastępuje czytelnej funkcji dla złożonej logiki.

### Late binding

Funkcje w closure zwykle odczytują zmienną w czasie wywołania, a nie tworzenia:

```python
functions = [lambda: i for i in range(3)]
assert [f() for f in functions] == [2, 2, 2]

captured = [lambda i=i: i for i in range(3)]
assert [f() for f in captured] == [0, 1, 2]
```

Domyślny parametr w drugim przykładzie zapisuje aktualną wartość przy tworzeniu funkcji.

## 8. Comprehensions i narzędzia wbudowane

```python
values = [1, 2, 3, 4]
squares = [x * x for x in values if x % 2 == 0]
assert squares == [4, 16]

positions = {name: index for index, name in enumerate(["a", "b"])}
assert positions == {"a": 0, "b": 1}

pairs = list(zip(["a", "b"], [1, 2], strict=True))
assert pairs == [("a", 1), ("b", 2)]
```

| Narzędzie | Zastosowanie |
| --- | --- |
| enumerate | Indeks i element |
| zip | Łączenie odpowiadających sobie elementów |
| any / all | Czy dowolny / każdy warunek jest prawdziwy |
| sum / min / max | Agregacje |
| sorted(..., key=...) | Sortowanie według klucza |
| isinstance | Sprawdzenie typu z uwzględnieniem dziedziczenia |
| map / filter | Leniwe przekształcanie / filtrowanie |

Domyślny `zip` kończy się na najkrótszym wejściu; `strict=True` wykrywa różne długości podczas iteracji. `all([])` to `True`, a `any([])` to `False`.

Comprehension powinna pozostać czytelna. Złożona logika zasługuje na zwykłą pętlę lub funkcję.

## 9. Iteratory i generatory

- **Iterable:** obiekt, z którego można uzyskać iterator przez `iter()`.
- **Iterator:** przechowuje stan i zwraca kolejne elementy przez `next()`; koniec sygnalizuje `StopIteration`.
- **Generator:** szczególny iterator tworzony przez funkcję z `yield` albo generator expression.

```python
def even_numbers(limit: int):
    for number in range(limit):
        if number % 2 == 0:
            yield number

stream = even_numbers(6)
assert next(stream) == 0
assert list(stream) == [2, 4]
assert list(stream) == []  # iterator jest już wyczerpany
```

`[f(x) for x in data]` tworzy listę wyników od razu. `(f(x) for x in data)` oblicza wyniki przy pobieraniu. Generator może ograniczyć zużycie pamięci, ale nie gwarantuje, że samo źródło danych nie jest już w pamięci.

Zastosowania: duże pliki, strumienie zdarzeń, porcjowanie danych.

## 10. Dekoratory i context managers

**Dekorator** przyjmuje funkcję lub klasę i zwraca obiekt, który zastępuje dekorowany obiekt. Przy funkcjach często dodaje logowanie, pomiar czasu albo kontrolę dostępu.

```python
from functools import wraps

def announce(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        return result
    return wrapper

@announce
def square(number: int) -> int:
    return number * number

assert square(3) == 9
assert square.__name__ == "square"
```

`@announce` odpowiada przypisaniu `square = announce(square)`. `wraps` zachowuje istotne metadane. Wrapper dla funkcji async powinien prawidłowo obsługiwać `await`.

**Context manager** zarządza wejściem i wyjściem z kontekstu przez `with`, np. zamyka plik także przy wyjątku. Może implementować `__enter__` / `__exit__` albo korzystać z `contextlib.contextmanager`.

```python
from contextlib import contextmanager

@contextmanager
def tracked_resource():
    resource = {"open": True}
    try:
        yield resource
    finally:
        resource["open"] = False

with tracked_resource() as resource:
    assert resource["open"]
assert not resource["open"]
```

## 11. OOP i dataclasses

| Pojęcie | Znaczenie |
| --- | --- |
| Klasa | Definicja zachowania i struktury instancji |
| Instancja | Konkretny obiekt danej klasy |
| self | Umowna nazwa referencji do instancji |
| __init__ | Inicjalizacja utworzonej instancji; samo tworzenie wiąże się z __new__ |
| Dziedziczenie | Rozszerzanie / specjalizacja klasy |
| Kompozycja | Budowanie obiektu z innych obiektów |
| Polimorfizm | Wspólny interfejs dla różnych implementacji |

- Metoda instancji otrzymuje `self`.
- `@classmethod` otrzymuje `cls`, np. dla alternatywnego konstruktora.
- `@staticmethod` nie otrzymuje automatycznie instancji ani klasy.
- `@property` pozwala udostępnić obliczaną lub kontrolowaną właściwość.
- `_name` oznacza konwencję wewnętrznego użycia; nie jest kontrolą dostępu.
- `__name` uruchamia name mangling, nie gwarantuje prywatności.

### Dataclass i pola mutowalne

```python
from dataclasses import dataclass, field

@dataclass
class Incident:
    identifier: str
    tags: list[str] = field(default_factory=list)

first = Incident("INC-1")
second = Incident("INC-2")
first.tags.append("aks")
assert second.tags == []
```

`dataclass` może wygenerować m.in. `__init__`, `__repr__` i `__eq__`. `frozen=True` blokuje zwykłe przypisywanie pól, ale nie czyni zagnieżdżonych list głęboko niemutowalnymi.

**Pułapka:** mutowalny atrybut klasy jest wspólny dla instancji. Dane pojedynczej instancji zwykle inicjalizuj w `__init__` albo przez `default_factory`.

Wzorce do rozumienia: Strategy (wymienne zachowanie), Adapter (dopasowanie interfejsu), Factory (tworzenie obiektów), Observer (powiadomienia). Nie dodawaj wzorca, jeśli zwykła funkcja rozwiązuje problem.

## 12. Typowanie i walidacja

Adnotacje typów pomagają narzędziom, IDE i czytelnikowi. **Interpreter zwykle nie egzekwuje ich automatycznie.**

```python
from typing import Protocol

class DiagnosticProvider(Protocol):
    def collect(self, namespace: str) -> list[str]: ...

def summarize(provider: DiagnosticProvider, namespace: str) -> int:
    return len(provider.collect(namespace))
```

| Mechanizm | Rola |
| --- | --- |
| list[str], dict[str, int] | Typy zawartości kolekcji |
| str \| None | Wartość może być napisem albo None |
| Any | Wyłącza część kontroli statycznej; używać świadomie |
| TypedDict | Statyczny opis kluczy i wartości słownika |
| Protocol | Strukturalny opis wymaganego zachowania |
| dataclass | Wygodne modele danych, bez pełnej walidacji runtime |
| Pydantic | Walidacja i parsowanie danych podczas działania |
| mypy / Pyright | Analiza statyczna typów |

Waliduj dane na granicach systemu: HTTP, pliki konfiguracyjne, baza, odpowiedź LLM. Poprawna struktura nie oznacza jeszcze poprawnych uprawnień ani prawdziwości danych. Przy walidatorach uwzględnij reguły konwersji typów i tryb strict.

## 13. Wyjątki

```python
def parse_count(raw: str) -> int:
    try:
        value = int(raw)
    except ValueError as error:
        raise ValueError("Licznik musi być liczbą całkowitą") from error
    if value < 0:
        raise ValueError("Licznik nie może być ujemny")
    return value

assert parse_count("3") == 3
```

- `try`: kod, który może zgłosić wyjątek.
- `except`: obsługa wskazanego typu wyjątku.
- `else`: wykonuje się, jeśli blok try nie zgłosił wyjątku.
- `finally`: sprzątanie przy zwykłym opuszczaniu bloku, również przez wyjątek.
- `raise`: zgłoszenie wyjątku; samo `raise` w handlerze ponawia bieżący.
- `raise ... from error`: jawny łańcuch przyczyn.

Łap konkretne wyjątki. Nie ukrywaj błędów przez `except Exception: pass`. `KeyboardInterrupt` i `SystemExit` nie są zwykłymi podklasami `Exception`.

Nie używaj `assert` jako walidacji bezpieczeństwa wejścia — instrukcje assert mogą być wyłączone opcją optymalizacji.

## 14. Moduły, pakiety i środowisko

- Moduł to jednostka importu, często plik `.py`.
- Pakiet organizuje moduły; zwykłe pakiety zawierają `__init__.py`, istnieją też namespace packages.
- Import może wykonać kod na poziomie modułu. Unikaj inicjalizowania połączeń chmurowych jako efektu importu.
- Nie nazywaj pliku `json.py` lub `logging.py`, jeśli przesłoniłby potrzebny moduł.
- `if __name__ == "__main__":` oddziela uruchomienie skryptu od importowania.
- Importy cykliczne często wskazują na problem z podziałem odpowiedzialności.

### Środowisko wirtualne

```bash
python -m venv .venv
# Linux / macOS
source .venv/bin/activate
# Windows PowerShell
# .\.venv\Scripts\Activate.ps1

python -m pip install -e ".[dev]"
python -m pytest
```

Instalacja `.[dev]` zakłada projekt z odpowiednim extra w `pyproject.toml`. To schemat dla aplikacji, nie deklaracja, że to repo jest instalowalnym pakietem.

`venv` izoluje zależności projektu, ale nie jest sandboxem bezpieczeństwa. `python -m pip` pomaga instalować pakiety do właściwego interpretera. `pyproject.toml` opisuje m.in. metadane i konfigurację narzędzi. Lockfile ustala rozwiązane wersje; sama lista szerokich zakresów nie zapewnia powtarzalnego środowiska.

## 15. Pliki, JSON, CSV i daty

```python
import json
from pathlib import Path
from tempfile import TemporaryDirectory

with TemporaryDirectory() as directory:
    path = Path(directory) / "config.json"
    path.write_text(
        json.dumps({"name": "agent", "enabled": True}, ensure_ascii=False),
        encoding="utf-8",
    )
    data = json.loads(path.read_text(encoding="utf-8"))
    assert data["enabled"] is True
```

- `json.loads()` / `dumps()`: napis ↔ obiekt.
- `json.load()` / `dump()`: odczyt/zapis przez obiekt plikowy.
- JSON nie przechowuje dowolnych obiektów Pythona, np. dataclass bez konwersji.
- Do CSV używaj modułu `csv`, a nie prostego `split(",")`; pola mogą zawierać przecinki i cudzysłowy.
- Przy plikach CSV otwieranych w trybie tekstowym zwykle używaj `newline=""`.
- Duże pliki przetwarzaj strumieniowo, zamiast bezwarunkowo wczytywać całość.
- Dla danych finansowych rozważ `Decimal`.
- Daty zapisuj ze świadomym wyborem strefy czasowej.

```python
from datetime import datetime, timezone

now = datetime.now(timezone.utc)
serialized = now.isoformat()
assert datetime.fromisoformat(serialized).tzinfo is not None
```

Nie mieszaj nieświadomie dat naive i aware. Do mierzenia czasu trwania używaj `time.perf_counter()` lub `time.monotonic()`, zamiast zegara kalendarzowego.

## 16. SQL i transakcje

**Parametryzuj wartości zamiast doklejać dane do SQL.** Składnia placeholderów zależy od sterownika.

```python
import sqlite3

connection = sqlite3.connect(":memory:")
try:
    with connection:
        connection.execute("CREATE TABLE incidents (id TEXT PRIMARY KEY)")
        connection.execute("INSERT INTO incidents (id) VALUES (?)", ("INC-1",))
    row = connection.execute(
        "SELECT id FROM incidents WHERE id = ?", ("INC-1",)
    ).fetchone()
    assert row == ("INC-1",)
finally:
    connection.close()
```

- Transakcja grupuje zmiany; commit zatwierdza, rollback wycofuje.
- Context manager połączenia SQLite obsługuje transakcję, ale nie zamyka automatycznie połączenia.
- Parametry zwykle dotyczą wartości, nie nazw tabel czy kolumn. Dynamiczne identyfikatory wymagają kontrolowanego wyboru lub właściwych narzędzi sterownika.
- ORM nie zwalnia z rozumienia zapytań, indeksów i problemu N+1.
- Nie trzymaj transakcji otwartej podczas długiego oczekiwania na LLM lub zewnętrzny HTTP.

## 17. HTTP i API

| Pojęcie | Do zapamiętania |
| --- | --- |
| GET | Pobranie reprezentacji |
| POST | Wykonanie operacji / często utworzenie zasobu |
| PUT | Zastąpienie reprezentacji zasobu; semantycznie idempotentne |
| PATCH | Częściowa zmiana; idempotencja zależy od operacji |
| DELETE | Usunięcie; idempotencja dotyczy efektu, nie identycznego kodu odpowiedzi |
| 2xx / 4xx / 5xx | Sukces / problem żądania / problem serwera |

Przykład funkcji z biblioteką HTTPX — wymaga jej instalacji; samo zdefiniowanie funkcji nie wysyła żądania:

```python
import httpx

def get_json(url: str) -> dict:
    with httpx.Client(timeout=10.0) as client:
        response = client.get(url)
        response.raise_for_status()
        data = response.json()
        if not isinstance(data, dict):
            raise ValueError("Oczekiwano obiektu JSON")
        return data
```

W aplikacji obsługującej wiele żądań współdziel klienta w kontrolowanym cyklu życia, aby korzystać z puli połączeń.

- Ustawiaj timeouty i limity; wartość timeout w kliencie nie zawsze jest jednym limitem całkowitego czasu operacji.
- Rozróżniaj błąd transportu, kod HTTP i błąd danych odpowiedzi.
- Retry stosuj do wybranych błędów przejściowych, z limitem, backoff i jitter.
- Ponowienie POST może powielić operację. Rozważ idempotency key.
- Przy 429 uwzględnij `Retry-After`, jeśli jest dostępny.
- Waliduj odpowiedź API przed użyciem.
- Nie pobieraj dowolnego URL podanego przez użytkownika bez kontroli SSRF.
- FastAPI korzysta m.in. ze Starlette i Pydantic. Walidacja requestu nie zastępuje uwierzytelnienia ani autoryzacji.
- ASGI obsługuje m.in. aplikacje async; WSGI to synchroniczny interfejs aplikacji webowych.

## 18. Async, wątki, procesy i GIL

**Współbieżność** oznacza postęp wielu zadań w nakładającym się czasie. **Równoległość** oznacza ich jednoczesne wykonywanie.

| Mechanizm | Typowy wybór |
| --- | --- |
| asyncio | Dużo operacji I/O z asynchronicznymi bibliotekami |
| Wątki | Blokujące operacje I/O i biblioteki synchroniczne |
| Procesy | Ciężkie obliczenia Python CPU-bound, izolacja |
| Biblioteki natywne | Obliczenia wektorowe; ich model wątków/GIL trzeba sprawdzić |

```python
import asyncio

async def work(number: int) -> int:
    await asyncio.sleep(0)
    return number * 2

async def main() -> list[int]:
    async with asyncio.TaskGroup() as group:
        tasks = [group.create_task(work(i)) for i in range(3)]
    return [task.result() for task in tasks]

assert asyncio.run(main()) == [0, 2, 4]
```

- Wywołanie `async def` tworzy coroutine; samo nie wykonuje całej funkcji.
- `await` oczekuje na awaitable; gdy operacja się zawiesza, inne zadania mogą dostać czas.
- `time.sleep()` blokuje wątek; w coroutine zwykle używamy `await asyncio.sleep()`.
- Synchroniczny klient HTTP w `async def` może blokować event loop.
- `asyncio.to_thread()` może przenieść blokujące I/O do wątku.
- Ograniczaj współbieżność, np. semaforem. Tysiące jednoczesnych requestów mogą przeciążyć usługę.
- Obsługuj anulowanie i sprzątaj zasoby; zwykle nie należy połykać `CancelledError`.
- W działającym event loop, np. notebooku, zwykle używamy `await main()`, zamiast zagnieżdżać `asyncio.run()`.

**GIL:** w standardowym buildzie CPythona z włączonym GIL jeden wątek naraz wykonuje bytecode Pythona. Nie oznacza to, że wątki nie pomagają w I/O. Część bibliotek natywnych zwalnia GIL. Istnieją też buildy free-threaded, więc zdanie „Python nigdy nie wykonuje wątków równolegle” jest nieprawdziwe.

GIL nie zapewnia poprawności złożonych współdzielonych operacji. Dla wspólnego stanu potrzebujesz odpowiedniej synchronizacji. Osobne procesy zwykle oznaczają koszt komunikacji i serializacji.

## 19. Testowanie

| Rodzaj testu | Zakres |
| --- | --- |
| Unit | Mała jednostka logiki z kontrolowanymi zależnościami |
| Integration | Współpraca z rzeczywistą bazą, adapterem lub usługą |
| End-to-end | Cały przepływ z perspektywy użytkownika/systemu |
| Smoke | Podstawowe sprawdzenie, czy system działa |

Przykład pytest — wymaga instalacji pytest:

```python
import pytest

def divide(a: float, b: float) -> float:
    if b == 0:
        raise ValueError("Dzielenie przez zero")
    return a / b

@pytest.mark.parametrize("a,b,expected", [(6, 2, 3), (0, 2, 0)])
def test_divide(a, b, expected):
    assert divide(a, b) == expected

def test_divide_by_zero():
    with pytest.raises(ValueError, match="zero"):
        divide(1, 0)
```

- Fixture przygotowuje zależności/dane; fixture z `yield` może też sprzątać.
- `tmp_path` daje katalog tymczasowy.
- `monkeypatch` pomaga kontrolować środowisko i zależności.
- Mockuj w miejscu, gdzie obiekt jest odczytywany przez testowany kod, a nie zawsze w miejscu jego pierwotnej definicji.
- `AsyncMock` służy do mockowania funkcji asynchronicznych.
- Coverage pokazuje wykonany kod, nie jakość asercji.
- Mockowane API nie dowodzi zgodności z prawdziwą usługą.
- Testy jednostkowe nie powinny wymagać przypadkowo aktywnej sesji Azure ani prawdziwych sekretów.
- Testuj granice, puste dane, błędne odpowiedzi, timeouty i odmowę wykonania operacji.

## 20. Logowanie i diagnostyka

```python
import logging

logger = logging.getLogger(__name__)

def record_completion(correlation_id: str, count: int) -> None:
    logger.info("Completed request=%s count=%s", correlation_id, count)
```

- Konfiguruj handlery i format na poziomie aplikacji.
- Używaj poziomów DEBUG, INFO, WARNING, ERROR.
- `logger.exception()` w bloku except dołącza traceback.
- Zapisuj identyfikatory korelacji, czas, status i istotne metadane.
- Nie loguj tokenów, haseł, pełnych danych osobowych ani bezrefleksyjnie całych promptów.
- Debugger i traceback pomagają zlokalizować błąd; profiler pomaga znaleźć koszt wykonania.
- `timeit` służy do małych pomiarów, `cProfile` do profilowania, `tracemalloc` do analizy alokacji.
- Najpierw mierz, potem optymalizuj. Lepszy algorytm często daje więcej niż drobna zmiana składni.

CPython wykorzystuje m.in. zliczanie referencji i mechanizmy wykrywania cykli. `del name` usuwa powiązanie nazwy; nie gwarantuje natychmiastowego zwolnienia całej pamięci do systemu. Zasoby zewnętrzne zamykaj jawnie przez `with` lub `try/finally`.

## 21. Bezpieczeństwo i jakość

| Ryzyko | Praktyka |
| --- | --- |
| SQL injection | Parametry zapytań |
| Command injection | Lista argumentów subprocess, kontrola wartości, zwykle shell=False |
| Niebezpieczna deserializacja | Nie używać pickle dla niezaufanych danych |
| Wykonanie wejścia jako kodu | Unikać eval/exec na niezaufanym wejściu |
| Sekrety w repo/logach | Kontrolowane dostarczanie sekretów i skanowanie |
| Path traversal | Kontrolowany katalog bazowy i walidacja ścieżek |
| Zbyt duże dane | Limity wielkości, czasu i zasobów |
| Podatne zależności | SCA, aktualizacje i przegląd zmian |

`shell=False` ogranicza interpretację przez powłokę, ale nie zapobiega każdemu argument injection. Także argumenty programu muszą być kontrolowane.

Dla YAML używaj bezpiecznego loadera dla niezaufanych danych i waliduj wynik. JSON nie wykonuje kodu tak jak pickle, ale nadal może wymagać ograniczeń zasobów i walidacji.

| Narzędzie | Rola |
| --- | --- |
| Ruff | Lint i formatowanie |
| mypy / Pyright | Statyczna kontrola typów |
| pytest | Testy |
| Bandit | SAST dla Pythona |
| pip-audit | Znane podatności zależności |
| Trivy | M.in. skany kontenerów, sekretów i konfiguracji |

Rozsądna kolejność w CI: lint → typing → testy → skany → raporty → wymagany gate. Część zadań można uruchamiać równolegle. Blokada merge wymaga reguł repozytorium, nie tylko czerwonego workflowu.

Więcej: [Security Knowledge Base](https://github.com/JeanneBM/security-knowledge-base).

## 22. Python w DevOps i AI

### DevOps

- CLI: argparse, poprawne kody wyjścia i pomoc.
- Konfiguracja: zmienne środowiskowe, pliki i walidacja.
- API chmurowe: timeouty, retry, minimalne uprawnienia.
- Automatyzacja: idempotencja, dry-run, kontrola zakresu zmian.
- Kubernetes: oddzielenie diagnostyki od wykonania operacji.
- Logi: struktura, korelacja i brak sekretów.
- Biblioteki projektuj tak, aby samo importowanie nie wykonywało deploymentu.

### AI Engineering i agenci

| Element | Co trzeba umieć w Pythonie |
| --- | --- |
| Wywołanie modelu | Klient HTTP/SDK, timeout, obsługa błędu, limity |
| Structured output | Walidacja modelu danych i reguł biznesowych |
| Narzędzia agenta | Wąskie interfejsy, allowlist, kontrola argumentów |
| Stan | Jawny model, SQLite/inna baza, transakcje |
| RAG | Przetwarzanie tekstu, metadane, retrieval, cytowania |
| Streaming | Iteratory/asynchroniczne iteratory i obsługa przerwania |
| Ewaluacja | Scenariusze, metryki, asercje, zapis dowodów |
| Testy | Oddzielenie testów offline od rzeczywistych wywołań modelu |

Odpowiedź LLM to niezaufane dane wejściowe. Poprawny JSON nie oznacza prawdziwej diagnozy ani zgody na operację. Autoryzację egzekwuje kod i polityka poza modelem.

Dla powtarzanych wywołań uwzględnij koszty, limit prób, duplikację skutków, rate limiting i korelację zdarzeń. Cache powinien mieć świadomie określone klucze, czas życia i zasady ochrony danych.

## 23. Pułapki i pytania rekrutacyjne

| Pytanie | Krótka odpowiedź |
| --- | --- |
| list vs tuple? | Lista jest mutowalna, krotka nie zmienia swoich referencji do elementów |
| is vs ==? | Tożsamość vs porównanie wartości |
| shallow vs deep copy? | Nowy obiekt z tymi samymi zagnieżdżonymi referencjami vs rekurencyjne kopiowanie |
| Czemu nie items=[] w definicji? | Wartość domyślna jest tworzona przy definiowaniu funkcji i może być współdzielona |
| Czy funkcja może zmienić argument? | Może mutować przekazany obiekt; lokalne przypisanie nie zmienia nazwy u wywołującego |
| Co to generator? | Leniwy iterator, często tworzony funkcją z yield |
| Czy iterator można przejść ponownie? | Zwykle nie po wyczerpaniu; potrzebny jest nowy iterator/źródło |
| Co daje dekorator? | Zastępuje obiekt wynikiem innego wywołania, często opakowując zachowanie |
| Co robi with? | Zapewnia protokół zarządzania zasobem przy wejściu i wyjściu |
| Czy type hints walidują request? | Same adnotacje zwykle nie; potrzebna walidacja runtime |
| Czy async oznacza równoległość CPU? | Nie; pomaga organizować współbieżne operacje, głównie I/O |
| Czy GIL eliminuje race conditions? | Nie |
| append vs extend? | Jeden element vs elementy z iterable |
| sort vs sorted? | Mutacja listy i None vs nowa posortowana lista |
| Dlaczego set do wyszukiwania? | Średnio O(1), gdy elementy są hashowalne |
| Co to idempotencja? | Powtórzenie operacji daje ten sam zamierzony efekt stanu |
| Czy retry jest zawsze bezpieczne? | Nie, może powielić skutki operacji |
| Czy 100% coverage dowodzi jakości? | Nie, ważne są scenariusze i asercje |
| unittest vs pytest? | unittest jest w bibliotece standardowej; pytest oferuje m.in. fixture i wygodną parametryzację |
| Dlaczego logger zamiast print? | Poziomy, konfiguracja, handlery, kontekst i integracje |

### Cztery wyniki, które warto przewidzieć

```python
matrix = [[0] * 2] * 2
matrix[0][0] = 1
assert matrix == [[1, 0], [1, 0]]  # współdzielony wewnętrzny obiekt

independent = [[0] * 2 for _ in range(2)]
independent[0][0] = 1
assert independent == [[1, 0], [0, 0]]

values = [3, 1, 2]
result = values.sort()
assert result is None
assert values == [1, 2, 3]

assert all([]) is True
assert any([]) is False
```

## 24. Ćwiczenia i plan powtórki

### Zadania

| Zadanie | Co sprawdza | Przypadki brzegowe |
| --- | --- | --- |
| Usuń duplikaty, zachowując kolejność | dict/set, złożoność | Puste wejście, powtórzenia; określ wymóg hashowalności |
| Policz słowa w tekście | Napisy, Counter | Interpunkcja, wielkość liter, Unicode |
| Wczytaj JSON i sprawdź konfigurację | Pliki, walidacja, wyjątki | Brak pliku, błędny JSON, brak klucza, niewłaściwy typ |
| Przetwórz logi strumieniowo | Generatory | Duży plik, uszkodzony rekord, puste linie |
| Dodaj klienta API z timeoutem | HTTP, testy | 429, 500, błędny JSON, timeout |
| Ogranicz liczbę równoległych requestów | asyncio, semafor | Anulowanie, błąd jednego zadania, limit czasu |
| Zapisz incydenty w SQLite | SQL i transakcje | Duplikat ID, rollback, parametryzacja |
| Oddziel politykę od wykonawcy agenta | Protocol, dependency injection | Odmowa, błędne argumenty, test braku skutków ubocznych |

### Przykładowe rozwiązanie: unikalne elementy

Dla hashowalnych wartości i zachowania kolejności:

```python
def unique_in_order(values: list[str]) -> list[str]:
    return list(dict.fromkeys(values))

assert unique_in_order(["a", "b", "a"]) == ["a", "b"]
assert unique_in_order([]) == []
```

### Plan 7 sesji

| Sesja | Zakres | Sprawdzenie |
| --- | --- | --- |
| 1 | Typy, referencje, kolekcje | Wyjaśnij kopię płytką i dobierz list/set/dict |
| 2 | Funkcje, zakresy, pułapki | Napraw mutable default i late binding |
| 3 | Iteratory, generatory, dekoratory, with | Zbuduj strumieniowe przetwarzanie pliku |
| 4 | OOP, dataclasses, typing, wyjątki | Oddziel interfejs od implementacji |
| 5 | Pliki, JSON, SQL, HTTP | Przetestuj błędne dane i parametry SQL |
| 6 | Async, testy i logi | Ogranicz współbieżność i zamockuj klienta API |
| 7 | DevOps/AI, bezpieczeństwo, pytania | Wyjaśnij projekt i rozwiąż 3 zadania bez podglądania |

To plan do samodzielnej powtórki, nie automatyczny harmonogram.

## 25. Materiały w repozytorium i źródła

### Istniejące materiały

Starsze pliki są materiałami do ćwiczeń i porównania podejść; nie należy traktować każdego historycznego przykładu jako aktualnego wzorca produkcyjnego.

- [Owoce Programowania](Owoce%20Programowania/) — ćwiczenia od podstaw po OOP i rekurencję.
- [Automate the Boring Stuff with Python](Automate%20the%20Boring%20Stuff%20with%20Python/) — automatyzacja, pliki i dane.
- [Python for DevOps](Python%20for%20DevOps/) — materiały DevOps.
- [Tests](Tests/) — materiały pytest, unittest i inne.
- [Decorators](Decorators/) — dekoratory.
- [Data](Data/) — materiały o danych.
- [Scripts](Scripts/) — skrypty do analizy i ćwiczeń; przed uruchomieniem sprawdź zależności i skutki.
- [Mine](Mine/) — wcześniejsze eksperymenty i przykłady.

### Oficjalne źródła

- [Python Tutorial](https://docs.python.org/3/tutorial/)
- [Typy wbudowane](https://docs.python.org/3/library/stdtypes.html)
- [Model danych](https://docs.python.org/3/reference/datamodel.html)
- [Funkcje i argumenty](https://docs.python.org/3/tutorial/controlflow.html)
- [typing](https://docs.python.org/3/library/typing.html) i [dataclasses](https://docs.python.org/3/library/dataclasses.html)
- [asyncio](https://docs.python.org/3/library/asyncio.html) i [free-threading](https://docs.python.org/3/howto/free-threading-python.html)
- [unittest.mock](https://docs.python.org/3/library/unittest.mock.html)
- [sqlite3](https://docs.python.org/3/library/sqlite3.html)
- [Python Packaging User Guide](https://packaging.python.org/)
- [pytest](https://docs.pytest.org/)
- [HTTPX](https://www.python-httpx.org/)
- [FastAPI](https://fastapi.tiangolo.com/) i [Pydantic](https://docs.pydantic.dev/)
- [PEP 8](https://peps.python.org/pep-0008/)

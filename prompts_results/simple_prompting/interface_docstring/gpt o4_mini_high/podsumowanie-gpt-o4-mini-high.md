# Podsumowanie analizy pokrycia testów jednostkowych (Model: gpt o4-mini-high)
# Kontekst: interfejs + docstring
# Strategia promptowania: simple prompting

## coverage.py
- missing: 1
- partial: 1
- coverage: 99%

## Ogólne informacje

Liczba wszystkich własnych scenariuszy: 54

- Testy wygenerowane przez LLM: 30
<br/> <strong>NOTKA: pojawiają się testy z kilkoma asercjami</strong>
- Testy zakończone powodzeniem: 29
- Testy zakończone niepowodzeniem: 1


- Liczba pokrytych scenariuszy testowych: 46
- Liczba niepotrzebnych testów: 0
- Liczba scenariuszy niepokrytych: 8
- Szybkość: wysoka

## Plusy

- 29/30 testów przechodzi. Jeden test zawiera błąd logiczny.
- Testy są dobrze zorganizowane i podzielone na różne klasy.
- Testy mają przejrzyste i czytelne nazwy metod.
- Testy dobrze odzwierciedlają spodziewane wyjątki, np. `ValueError` i `TypeError`.
- Pokrywa znaczną większość typowych funkcjonalności
- Model wykazuje potencjał do generowania różnorodnych testów i uwzględniania nietypowych przypadków testowych - takich jak sprawdzanie różnych inputów dla metod, sprawdzanie częściowo precyzji obliczeń przez weryfikacje wyników dla większych wartości czy też sprawdzenie dokładnie edge case'ów przy ograniczeniach wartości.
- Inteligentnie łączy wiele asercji testujących podobne zachowanie w jednym teście, dzięki czemu testów jest mniej, a ich jakość i pokrycie nie spada

## Minusy

- Brakuje testów związanych z wydajnością, np. dodanie lub usunięcie tysięcy produktów.
- Brakuje testów odpornościowych, np. bardzo duże liczby, wartości typu `None`, `inf`, `NaN`.
- Brakuje pojedyńczych corner case'ów, niektóre zostały pominięte.

## Pomijane scenariusze

- testy precyzji obliczeń
- test wydajnościowe / odpornościowe
- corner case'y rzucający wyjątek ValueError przy za długiej nazwie name
- scenariusz testowy: obliczanie totalu z założeniem że jest zniżka i doliczmay shipping


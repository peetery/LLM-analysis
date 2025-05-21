# Podsumowanie analizy pokrycia testów jednostkowych (Model: gpt o4-mini-high)
# Kontekst: interfejs + docstring
# Strategia promptowania: chain-of-thought

## coverage.py
- missing: 1
- partial: 1
- coverage: 99%

## Ogólne informacje

Liczba wszystkich własnych scenariuszy: 54

- Testy wygenerowane przez LLM: 65
<br/> <strong>NOTKA: pojawiają się testy z kilkoma asercjami</strong>
- Testy zakończone powodzeniem: 65
- Testy zakończone niepowodzeniem: 0


- Liczba pokrytych scenariuszy testowych: 47
- Liczba niepotrzebnych testów: 18
- <br/> <strong>NOTKA: ciężko stwierdzić czy wszystkie te testy są niepotrzebne, ponieważ testują one na bardzo wiele sposobów metody, co można uznać za plus, a nie za minus.</strong>
- Liczba scenariuszy niepokrytych: 7
- Szybkość: bardzo niska (ponad 4 minuty na 3 prompty)

## Plusy

- 65/65 testów przechodzi.
- Testy są dobrze zorganizowane i podzielone na różne klasy, dobre nazewnictwo.
- Testy mają przejrzyste i czytelne nazwy metod.
- Testy dobrze odzwierciedlają spodziewane wyjątki, np. `ValueError` i `TypeError`.
- Pokrywa wszystkie typowe funkcjonalności i typowe corner case.
- Model wykazuje potencjał do generowania różnorodnych testów i uwzględniania nietypowych przypadków testowych - takich jak sprawdzanie różnych inputów dla metod (chociaż różnorodność moglaby być lepsza), sprawdza równiez edge case'y i zachowania metod w nietypowych sytuacjach.

## Minusy

- Brakuje testów związanych z precyzją obliczeń, model testuje dla troche nietypowych wartościach, ale dalej są one dosyć proste. Mogłoby być lepiej.
- Brakuje testów związanych z wydajnością, np. dodanie lub usunięcie tysięcy produktów.
- Brakuje testów odpornościowych, np. bardzo duże liczby, wartości typu `None`, `inf`, `NaN`.

## Pomijane scenariusze

- testy precyzji obliczeń
- test wydajnościowe / odpornościowe
- corner case'y rzucający wyjątek ValueError przy za długiej nazwie name


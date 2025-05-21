# Podsumowanie analizy pokrycia testów jednostkowych (Model: DeepSeek)
# Kontekst: interfejs + docstring
# Strategia promptowania: chain-of-thought

## coverage.py
- missing: 2
- partial: 2
- coverage: 97%

## Ogólne informacje

Liczba wszystkich własnych scenariuszy: 54

- Testy wygenerowane przez LLM: 53
- Testy zakończone powodzeniem: 51
- Testy zakończone niepowodzeniem: 2


- Liczba pokrytych scenariuszy testowych: 45
- Liczba niepotrzebnych testów: 6
- Liczba scenariuszy niepokrytych: 9
- Szybkość: wysoka (3 minuty na 3 prompty)

## Plusy

- Model pokrył prawie wszystkie typowe scenariusze testowe (z wyjątkiem 2).
- Model pokrył prawie wszystkie typowe corner case'y (z wyjątkiem 1).
- Testy są dobrze zorganizowane i świetnie podzielone na pojedyncze asercje.
- Testy mają przejrzyste i czytelne nazwy metod.
- Model wykazuje potencjał do wykrywania edge case'ów. W kilku przypadkach sprawdzał skrajne wartości.
- (!) Dla metody get_subtotal stworzył test sprawdzający precyzje obliczeń, jednak był on dość nieprecyzyjny z racji że sprawdzał tylko dokładność float do 1 liczby po przecinku.

## Minusy

- Brakuje testów związanych z wydajnością, np. dodanie lub usunięcie tysięcy produktów.
- Brakuje testów odpornościowych, np. bardzo duże liczby, wartości typu `None`, `inf`, `NaN`.
- Brakuje większej różnorodności inputów.

## Pomijane scenariusze

- brakuje 2 typowych scenariuszy testowych
- brakuje 1 typowego corner case
- testy precyzji obliczeń
- test wydajnościowe / odpornościowe


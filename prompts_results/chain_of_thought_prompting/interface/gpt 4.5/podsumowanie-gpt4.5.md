# Podsumowanie analizy pokrycia testów jednostkowych (Model: gpt 4.5)
# Kontekst: interfejs
# Strategia promptowania: chain-of-thought

## coverage.py
- missing: 16
- partial: 16
- coverage: 79%

## mutmut.py
⠇ 217/217  🎉 108 🫥 0  ⏰ 0  🤔 0  🙁 109  🔇 0

## Rezultaty
- Compilation success rate: 88%
- Statement coverage: 79%
- Branch coverage: 71%
- Mutation score: 50%

## Ogólne informacje

Liczba wszystkich własnych scenariuszy: 54

- Testy wygenerowane przez LLM: 40
- Testy zakończone powodzeniem: 35
- Testy zakończone niepowodzeniem: 5


- Liczba wykrytych corner case'ów: 9 (3 niepoprawny)


- Liczba pokrytych scenariuszy testowych: 30
- Liczba niepotrzebnych testów: 10
- Liczba scenariuszy niepokrytych: 24
- Szybkość: bardzo niska (+2 minuty na 3 prompty)

## Plusy

- 35/40 testów przechodzi.
- Testy są dobrze zorganizowane i podzielone na różne klasy.
- Testy mają przejrzyste i czytelne nazwy metod.
- Bazując tylko na interfejsach wykrywa 9 corner case'ów, które są związane z niepoprawnym inputem

## Minusy

- Brakuje testów związanych z wydajnością, np. dodanie lub usunięcie tysięcy produktów.
- Brakuje testów odpornościowych, np. bardzo duże liczby, wartości typu `None`, `inf`, `NaN`.
- Brakuje większej różnorodności inputów
- Brakuje mnóstwo corner case'ów związanych z niepoprawnym użyciem metod. Wykryte jest tylko kilka i sprawia wrażenie, że zostały one wybrane losowo - reszta metod nie zawiera sprawdzania niepoprawnych wartości.
- Nie sprawdza w ogóle niepoprawnego typu inputów.
- Brakuje dużo typowych scenariuszy testowych.

## Pomijane scenariusze

- testy precyzji obliczeń
- test wydajnościowe / odpornościowe
- corner case'y rzucające wyjątki TypeError czy też ValueError
- dużo typowych scenariuszy testowych

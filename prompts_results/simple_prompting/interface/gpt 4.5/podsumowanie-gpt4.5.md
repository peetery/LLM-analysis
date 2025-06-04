# Podsumowanie analizy pokrycia testów jednostkowych (Model: gpt 4.5)
# Kontekst: interfejs
# Strategia promptowania: simple prompting

## coverage.py
- missing: 24
- partial: 21
- coverage: 68%

## mutmut.py
⠹ 217/217  🎉 93 🫥 0  ⏰ 0  🤔 0  🙁 124  🔇 0

## Rezultaty
- Compilation success rate: 88%
- Statement coverage: 68%
- Branch coverage: 63%
- Mutation score: 43%

## Ogólne informacje

Liczba wszystkich własnych scenariuszy: 54

- Testy wygenerowane przez LLM: 17
- Testy zakończone powodzeniem: 15
- Testy zakończone niepowodzeniem: 2


- Liczba pokrytych scenariuszy testowych: 20
- Liczba niepotrzebnych testów: 0
- Liczba scenariuszy niepokrytych: 34
- Liczba wykrytych corner case'ów: 5 (1 niepoprawny)
- Szybkość: bardzo niska

## Plusy

- 15/17 testów przechodzi. Jeden test zawiera błąd logiczny, natomiast drugi (corner case) zakłada rzucenie innego wyjątku niż jest rzucany w rzeczywistości.
- Testy są dobrze zorganizowane i podzielone na różne klasy.
- Testy mają przejrzyste i czytelne nazwy metod.
- Bazując tylko na interfejsach wykrywa 5 corner case'ów, które są związane z niepoprawnym użyciem metod.

## Minusy

- Brakuje testów związanych z wydajnością, np. dodanie lub usunięcie tysięcy produktów.
- Brakuje testów odpornościowych, np. bardzo duże liczby, wartości typu `None`, `inf`, `NaN`.
- Brakuje większej różnorodności inputów
- Brakuje mnóstwo corner case'ów związanych z niepoprawnym użyciem metod. Wykryte jest tylko kilka i sprawia wrażenie, że zostały one wybrane losowo - reszta metod nie zawiera sprawdzania niepoprawnych wartości.
- Brakuje dużo typowych scenariuszy testowych. Bazując na samym interfejsie model jest w stanie dobrze przetestować tylko na prawdę bardzo proste metody - gdy już jakaś metoda jest trochę bardziej skomplikowana to po samej nazwie metody nie jest w stanie przewidzieć jej funkcjonowania.

## Pomijane scenariusze

- testy precyzji obliczeń
- test wydajnościowe / odpornościowe
- corner case'y rzucające wyjątki TypeError czy też ValueError
- dużo typowych scenariuszy testowych

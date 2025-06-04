# Podsumowanie analizy pokrycia testów jednostkowych (Model: gpt 4.5)
# Kontekst: full context
# Strategia promptowania: chain-of-thought

## coverage.py
- missing: 9
- partial: 7
- coverage: 89%

## mutmut.py
⠦ 217/217  🎉 102 🫥 6  ⏰ 0  🤔 0  🙁 109  🔇 0

## Rezultaty
- Compilation success rate: 98%
- Statement coverage: 89%
- Branch coverage: 88%
- Mutation score: 47%

## Ogólne informacje

Liczba wszystkich własnych scenariuszy: 54

- Testy wygenerowane przez LLM: 40
- Testy zakończone powodzeniem: 39
- Testy zakończone niepowodzeniem: 1


- Liczba pokrytych scenariuszy testowych: 32
- Liczba niepotrzebnych testów: 8
- Liczba scenariuszy niepokrytych: 22
- Szybkość: bardzo niska (4.5 minuty na 3 prompty)

## Plusy

- 39/40 testów przechodzi
- Testy są dobrze zorganizowane i podzielone na różne klasy, są zwięzłe.
- Testy mają przejrzyste i czytelne nazwy metod.
- Raz udaje mu się sprawdzić precyzje obliczeń - warto odnotować.

## Minusy

- Brakuje testów związanych z wydajnością, np. dodanie lub usunięcie tysięcy produktów.
- Brakuje testów odpornościowych, np. bardzo duże liczby, wartości typu `None`, `inf`, `NaN`.
- Brakuje większej różnorodności inputów
- Brakuje mnóstwo corner case'ów związanych z niepoprawnym użyciem metod. Nie sprawdza obu wartości poza zakresem, nie sprawdza czy wszystkie parametry są poprawnego typu.
- Brakuje dużo typowych scenariuszy testowych.
- Wydaje się, że model przy większym kontekście zaczyna się gubić. Rozpisał znacznie więcej scenariuszy niż napisał rzeczywistych testów.

## Pomijane scenariusze

- testy precyzji obliczeń
- test wydajnościowe / odpornościowe
- corner case'y rzucające wyjątki TypeError czy też ValueError
- dużo typowych scenariuszy testowych

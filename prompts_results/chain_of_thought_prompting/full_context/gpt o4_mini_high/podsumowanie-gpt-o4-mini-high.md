# Podsumowanie analizy pokrycia testów jednostkowych (Model: gpt o4-mini-high)
# Kontekst: full context
# Strategia promptowania: chain-of-thought

## coverage.py
- missing: 1
- partial: 1
- coverage: 99%

## mutmut.py
⠹ 217/217  🎉 118 🫥 0  ⏰ 0  🤔 0  🙁 99  🔇 0

## Rezultaty
- Compilation success rate: 100%
- Statement coverage: 99%
- Branch coverage: 98%
- Mutation score: 54%

## Ogólne informacje

Liczba wszystkich własnych scenariuszy: 54

- Testy wygenerowane przez LLM: 67
<br/> <strong>NOTKA: pojawiają się testy z kilkoma asercjami</strong>
- Testy zakończone powodzeniem: 67
- Testy zakończone niepowodzeniem: 0

- Liczba pokrytych scenariuszy testowych: 48
- Liczba niepotrzebnych testów: 19
- <br/> <strong>NOTKA: nie można jednoznacznie ocenić że wszystkie testy są niepotrzebne, testują testy na wiele różnych sposobów, co można uznać też za atut w pewnym sensie.</strong>
- Liczba scenariuszy niepokrytych: 6
- Szybkość: niska (3 minuty na 3 prompty)

## Plusy

- 67/67 testów przechodzi.
- Testy są dobrze zorganizowane i podzielone na różne klasy.
- Testy mają przejrzyste i czytelne nazwy metod.
- Świetnie wykrywa corner case'y - pokrył wszystkie typowe corner-case'y.
- Pokrywa wszystkie typowe funkcjonalności.
- Model wykazuje potencjał do wykrywania edge case'ów - sprawdzania skrajnych wartości przy ifach etc.
- Model wykazuje potencjał do sprawdzania różnych inputów i weryfikowania działania metod na bardziej nietypowych liczbach.
- ! Model jako jedyny sprawdził przy calculate_tax obliczenia dla ogromnej liczby! (1e6) 

## Minusy

- Brakuje testów związanych z wydajnością, np. dodanie lub usunięcie tysięcy produktów.
- Brakuje testów odpornościowych, np. bardzo duże liczby, wartości typu `None`, `inf`, `NaN`.

## Pomijane scenariusze

- testy precyzji obliczeń
- test wydajnościowe / odpornościowe

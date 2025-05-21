# Podsumowanie analizy pokrycia testów jednostkowych (Model: claude 3.7 sonet)
# Kontekst: interfejs + docstring
# Strategia promptowania: chain-of-thought

## coverage.py
- missing: 1
- partial: 1
- coverage: 99%

## Ogólne informacje

Liczba wszystkich własnych scenariuszy: 54

- Testy wygenerowane przez LLM: 75
<br/> <strong>NOTKA: pojawiają się testy z kilkoma asercjami</strong>
- Testy zakończone powodzeniem: 74
- Testy zakończone niepowodzeniem: 1


- Liczba pokrytych scenariuszy testowych: 47
- Liczba niepotrzebnych testów: 21
- <br/> <strong>NOTKA: ciężko ocenić czy wszystkie testy są niepotrzebne, ponieważ testują one metody w bardzo nietypowych warunkach. Dodatkowo warto zwrócić uwagę że pojawiąsię kilka testów integracyjnych testujących pełny workflow działania klasy OrderCalculator.</strong>
- Liczba scenariuszy niepokrytych: 6
- Szybkość: bardzo niska (5 minut na 3 prompty, claude bardzo długo pisze sam kod do testów)

## Plusy

- 74/75 testów przechodzi.
- Pokrywa wszystkie typowe scenariusze testowe.
- Pokrywa wszystkie typowe corner case'y.
- Model wykazuje potencjał do uwzględniania sprawdzania wartości tzw edge case'ów w przypadku ograniczeń dla parametrów sprawdza wartości skrajne czy przechodzą czy nie.
- Model wykazuje również dobrą kreatywność w sprawdzaniu różnego podejścia do weryfikacji testów - sprawdza nietypowe okolizności.
- Model wykazuje niewielki potencjał do sprawdzania różnych inputów i weryfikowania trudniejszych obliczeń - jednak tutaj mogłoby być znacznie lepiej, bo liczby nie są takie banalne, ale dalej dość proste.

## Minusy

- Brakuje testów związanych z wydajnością, np. dodanie lub usunięcie tysięcy produktów.
- Brakuje testów odpornościowych, np. bardzo duże liczby, wartości typu `None`, `inf`, `NaN`.

## Pomijane scenariusze

- testy precyzji obliczeń
- test wydajnościowe / odpornościowe


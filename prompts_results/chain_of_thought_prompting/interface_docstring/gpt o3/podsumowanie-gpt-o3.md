# Podsumowanie analizy pokrycia testów jednostkowych (Model: gpt o3)
# Kontekst: interfejs + docstring
# Strategia promptowania: chain-of-thought

## coverage.py
- missing: 1
- partial: 1
- coverage: 99%

## Ogólne informacje

Liczba wszystkich własnych scenariuszy: 54

- Testy wygenerowane przez LLM: 58
<br/> <strong>NOTKA: pojawiają się testy z kilkoma asercjami</strong>
- Testy zakończone powodzeniem: 57
- Testy zakończone niepowodzeniem: 1


- Liczba pokrytych scenariuszy testowych: 47
- Liczba niepotrzebnych testów: 11
- Liczba scenariuszy niepokrytych: 7
- <br/><strong>NOTKA: niektóre testy są niepotrzebne, ponieważ pokrywają się z innymi testami, chociaż niektóre z nich można ocenić za dalej wartościowe z powodu testowania metody na inny sposób.</strong>
- Szybkość: niska (3.5 minuty na 3 prompty)

## Plusy

- 57/58 testów przechodzi.
- Pokrywa wszystkie typowe scenariusze testowe.
- Pokrya wszystkie typowe corner case'y
- Model wykazuje potencjał do uwzględniania sprawdzania wartości tzw edge case'ów w przypadku ograniczeń dla parametrów sprawdza wartości skrajne czy przechodzą czy nie.
- Model wykazuje potencjał do sprawdzania różnorodnych inputó, przy calculate_total przyjmował ciekawe wartości, jednak tylko tutaj można to wyróznić. Mogło być znacznie lepiej, ale jest potencjał.

## Minusy

- Brakuje większości testów precyzji obliczeń.
- Brakuje testów związanych z wydajnością, np. dodanie lub usunięcie tysięcy produktów.
- Brakuje testów odpornościowych, np. bardzo duże liczby, wartości typu `None`, `inf`, `NaN`.

## Pomijane scenariusze

- testy precyzji obliczeń
- test wydajnościowe / odpornościowe


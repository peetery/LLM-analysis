# Podsumowanie analizy pokrycia testów jednostkowych (Model: gpt o3)
# Kontekst: interfejs
# Strategia promptowania: simple prompting

## coverage.py
- missing: 18
- partial: 18
- coverage: 76%

## Ogólne informacje

Liczba wszystkich własnych scenariuszy: 54

- Testy wygenerowane przez LLM: 22
<br/> <strong>NOTKA: pojawiają się testy z kilkoma asercjami</strong>
- Testy zakończone powodzeniem: 19
- Testy zakończone niepowodzeniem: 3


- Liczba wykrytych corner case'ów: 7 (niepoprawnie 1)


- Liczba pokrytych scenariuszy testowych: 25
- Liczba niepotrzebnych testów: 0
- Liczba scenariuszy niepokrytych: 19
- Szybkość: umiarkowana

## Plusy

- 19/22 testów przechodzi.
- Model wykazuje potencjał do uwzględniania sprawdzania wartości tzw edge case'ów w przypadku ograniczeń dla parametrów sprawdza wartości skrajne czy przechodzą czy nie.
- Model wykazuje potencjał do przewidywania corner case'ów, jednak sprawdza ich niewiele - a wybór wydaje się być przypadkowy.
- Testy są dobrze zorganizowane i podzielone, mają przejrzyste nazwy metod.

## Minusy

- Brakuje testów związanych z wydajnością, np. dodanie lub usunięcie tysięcy produktów.
- Brakuje testów odpornościowych, np. bardzo duże liczby, wartości typu `None`, `inf`, `NaN`.
- Brakuje wiele typowych scenariuszy testowych.
- Brakuje wiele corner case'ów

## Pomijane scenariusze

- testy precyzji obliczeń
- test wydajnościowe / odpornościowe
- corner case'y
- typowe scenariusze testowe


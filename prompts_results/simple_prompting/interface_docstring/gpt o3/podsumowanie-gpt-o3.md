# Podsumowanie analizy pokrycia testów jednostkowych (Model: gpt o3)
# Kontekst: interfejs + docstring
# Strategia promptowania: simple prompting

## coverage.py
- missing: 6
- partial: 6
- coverage: 92%

## mutmut.py
⠇ 217/217  🎉 109 🫥 0  ⏰ 0  🤔 0  🙁 108  🔇 0

## Ogólne informacje

Liczba wszystkich własnych scenariuszy: 54

- Testy wygenerowane przez LLM: 45
<br/> <strong>NOTKA: pojawiają się testy z kilkoma asercjami</strong>
- Testy zakończone powodzeniem: 45
- Testy zakończone niepowodzeniem: 0


- Liczba pokrytych scenariuszy testowych: 44
- Liczba niepotrzebnych testów: 1
- Liczba scenariuszy niepokrytych: 10
- Szybkość: umiarkowana

## Plusy

- 45/45 testów przechodzi. 100% skuteczność testów jest bardzo zadowalająca i zasługuje na wyróżnienie.
- Pokrywa wszystkie typowe scenariusze testowe.
- Model wykazuje potencjał do uwzględniania sprawdzania wartości tzw edge case'ów w przypadku ograniczeń dla parametrów sprawdza wartości skrajne czy przechodzą czy nie.

## Minusy

- Brakuje testów związanych z wydajnością, np. dodanie lub usunięcie tysięcy produktów.
- Brakuje testów odpornościowych, np. bardzo duże liczby, wartości typu `None`, `inf`, `NaN`.
- Brakuje pojedyńczych corner case'ów, niektóre zostały pominięte - dla init nie sprawdza dla 2 parametrów wyjątku TypeError.

## Pomijane scenariusze

- testy precyzji obliczeń
- test wydajnościowe / odpornościowe
- corner case'y rzucające wyjątki TypeError dla init


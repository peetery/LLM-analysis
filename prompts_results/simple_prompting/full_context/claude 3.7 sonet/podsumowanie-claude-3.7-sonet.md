# Podsumowanie analizy pokrycia testów jednostkowych (Model: claude 3.7 sonet)
# Kontekst: full context
# Strategia promptowania: simple prompting

## coverage.py
- missing: 1
- partial: 1
- coverage: 99%

## mutmut.py
⠋ 217/217  🎉 108 🫥 0  ⏰ 0  🤔 0  🙁 109  🔇 0

## Ogólne informacje

Liczba wszystkich własnych scenariuszy: 54

- Testy wygenerowane przez LLM: 46
- Testy zakończone powodzeniem: 46
- Testy zakończone niepowodzeniem: 0


- Liczba pokrytych scenariuszy testowych: 46
- Liczba niepotrzebnych testów: 0
- Liczba scenariuszy niepokrytych: 8
- Szybkość: umiarkowana

## Plusy

- Przechodzi 46/46 testów.
- Brak niepotrzebnych testów. Pokrywa wszystkie najważniejsze scenariusze, w tym podstawowe corner case'y. Jest to imponującę, że mamy zachowaną idealną proporcję testów do scenariuszy.
- Model wykazuje potencjał do uwzględniania sprawdzania wartości tzw edge case'ów w przypadku ograniczeń dla parametrów sprawdza wartości skrajne czy przechodzą czy nie.
- Model wykazuje również przyzwoitą kreatywność w sprawdzaniu różnego podejścia do weryfikacji testów i sprawdzania różnych inputów - daje nieoczywiste wartości i sprawdza trudniejsze obliczenia.
- Świetna organizacja testów i nazewnictwo, pojedyńcze asercje.

## Minusy

- Brakuje testów związanych z wydajnością, np. dodanie lub usunięcie tysięcy produktów.
- Brakuje testów odpornościowych, np. bardzo duże liczby, wartości typu `None`, `inf`, `NaN`.

## Pomijane scenariusze

- testy precyzji obliczeń
- test wydajnościowe / odpornościowe


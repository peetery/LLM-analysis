# Podsumowanie analizy pokrycia testów jednostkowych (Model: claude 3.7 sonet)
# Kontekst: full context
# Strategia promptowania: chain-of-thought

## coverage.py
- missing: 1
- partial: 1
- coverage: 99%

## mutmut.py
⠧ 217/217  🎉 109 🫥 0  ⏰ 0  🤔 0  🙁 108  🔇 0

## Rezultaty
- Statement coverage: 99%
- Branch coverage: 98%
- Mutation score: 50%

## Ogólne informacje

Liczba wszystkich własnych scenariuszy: 54

- Testy wygenerowane przez LLM: 56
- Testy zakończone powodzeniem: 46
- Testy zakończone niepowodzeniem: 0


- Liczba pokrytych scenariuszy testowych: 48
- Liczba niepotrzebnych testów: 8
<br/> <strong>NOTKA: nie można tak jednoznacznie uznać wszystkiych testów za niepotrzebne, ponieważ sprawdzają często np różne edge case'y </strong>
- Liczba scenariuszy niepokrytych: 6
- Szybkość: umiarkowana (3 minuty)

## Plusy

- Przechodzi 48/48 testów.
- Pokrywa wszystkie najważniejsze funkcjonalności.
- Pokrywa wszystkie typowe corner case'y.
- Model wykazuje potencjał do uwzględniania sprawdzania wartości tzw edge case'ów w przypadku ograniczeń dla parametrów sprawdza wartości skrajne czy przechodzą czy nie.
- Model wykazuje również przyzwoitą kreatywność w sprawdzaniu różnego podejścia do weryfikacji testów i sprawdzania różnych inputów - daje nieoczywiste wartości i sprawdza trudniejsze obliczenia.

## Minusy

- (!) Nie słucha się poleceń. Po 1 prompcie zaczął generować kod, mimo prośby niepisania kodu. Dodatkowo napisał sam całą implementację klasy wraz z docstringami mimo że dostał w prompcie cały kontekst. Przez to chain-of-thought stracił sens, testy były po 1 prompcie.
- Pisze komentarze w kodzie.
- Brakuje testów związanych z wydajnością, np. dodanie lub usunięcie tysięcy produktów.
- Brakuje testów odpornościowych, np. bardzo duże liczby, wartości typu `None`, `inf`, `NaN`.

## Pomijane scenariusze

- testy precyzji obliczeń (z wyjątkiem calculate_total)
- test wydajnościowe / odpornościowe


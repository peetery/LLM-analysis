# Podsumowanie analizy pokrycia testów jednostkowych (Model: claude 3.7 sonet)
# Kontekst: interfejs
# Strategia promptowania: simple prompting

## coverage.py
- missing: 18
- partial: 18
- coverage: 76%

## mutmut.py
⠼ 217/217  🎉 79 🫥 18  ⏰ 0  🤔 0  🙁 120  🔇 0

## Ogólne informacje

Liczba wszystkich własnych scenariuszy: 54

- Testy wygenerowane przez LLM: 40
<br/> <strong>NOTKA: pojawiają się testy z kilkoma asercjami</strong>
- Testy zakończone powodzeniem: 23
- Testy zakończone niepowodzeniem: 17


- Liczba pokrytych scenariuszy testowych: 31
- Liczba niepotrzebnych testów: 9
- Liczba scenariuszy niepokrytych: 23
- Szybkość: umiarkowana

## Plusy

- Dobre nazewnictwo testów, są uporządkowane
- Model wykazuje potencjał do uwzględniania sprawdzania wartości tzw edge case'ów w przypadku ograniczeń dla parametrów sprawdza wartości skrajne czy przechodzą czy nie.
- Model wykazuje również przyzwoitą kreatywność w sprawdzaniu różnego podejścia do weryfikacji testów i sprawdzania różnych inputów - daje nieoczywiste wartości i sprawdza trudniejsze obliczenia.
- ! Przewidział poprawne zachowanie przy dodaniu dwa razy przedmiotu o tej samej nazwie i cenie - domyślił się że quantity będzie sumowane i przetestował to.

## Minusy

- Wygenerowane testy pokrywają tylko 31/54 scenariuszy testowych
- Niektóre testy są niepotrzebne, ponieważ pewne rzeczy są sprawdzane wielokrotnie w różnych testach na podobne sposoby. Można by było części testów się pozbyć.
- Brakuje sprawdzania przekazywania niepoprawnych typów w testach - nie ma pokrycia żadnego z takich przypadków.
- Brakuje testów związanych z wydajnością, np. dodanie lub usunięcie tysięcy produktów.
- Brakuje testów odpornościowych, np. bardzo duże liczby, wartości typu `None`, `inf`, `NaN`.

## Pomijane scenariusze

- niektóre testy z niepoprawnymi wartościami argumentów
- testy z niepoprawnymi typami
- testy precyzji obliczeń
- test wydajnościowe / odpornościowe


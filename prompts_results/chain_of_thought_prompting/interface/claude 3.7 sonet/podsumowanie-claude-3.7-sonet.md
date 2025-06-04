# Podsumowanie analizy pokrycia testów jednostkowych (Model: claude 3.7 sonet)
# Kontekst: interfejs
# Strategia promptowania: chain-of-thought

## coverage.py
- missing: 10
- partial: 10
- coverage: 87%

## mutmut.py
⠋ 217/217  🎉 94 🫥 0  ⏰ 0  🤔 0  🙁 123  🔇 0

## Rezultaty
- Compilation success rate: 68%
- Statement coverage: 87%
- Branch coverage: 82%
- Mutation score: 43%

## Ogólne informacje

Liczba wszystkich własnych scenariuszy: 54

- Testy wygenerowane przez LLM: 60
<br/> <strong>NOTKA: pojawiają się testy z kilkoma asercjami</strong>
- Testy zakończone powodzeniem: 41
- Testy zakończone niepowodzeniem: 19


- Liczba pokrytych scenariuszy testowych: 38
- Liczba niepotrzebnych testów: 22
- <br/> <strong>NOTKA: ciężko ocenić czy wszystkie te testy można uznać za niepotrzebne, ponieważ testuje on metody na wiele sposobów i robi to bardzo dokładnie, ma to swoje plusy i może zostać uznane też za korzyść</strong>
- Liczba scenariuszy niepokrytych: 16
- Szybkość: niska (wszystkie 3 prompty to ponad 2-3 minuty)

## Plusy

- Model bardzo dokładnie sprawdza poprawność metod i ich zachowań, weryfikując działanie różnego rodzaju asercjami
- ! Jako jedyny do tej pory sprawdził działanie z przekazaniem np None
- Dobre nazewnictwo testów, są uporządkowane
- Model wykazuje potencjał do uwzględniania sprawdzania wartości tzw edge case'ów w przypadku ograniczeń dla parametrów sprawdza wartości skrajne czy przechodzą czy nie.
- Model wykazuje również przyzwoitą kreatywność w sprawdzaniu różnego podejścia do weryfikacji testów.
- ! Przewidział poprawne zachowanie przy dodaniu dwa razy przedmiotu o tej samej nazwie i cenie - domyślił się że quantity będzie sumowane i przetestował to.

## Minusy

- Ignoruje prośbę, że ma wygenerować tylko testy jednostkowe i bez komentarzy. Implementuję swój własny OrderCalculator
- Wygenerowane testy pokrywają tylko 38/54 scenariuszy testowych
- Niektóre testy są niepotrzebne, ponieważ pewne rzeczy są sprawdzane wielokrotnie w różnych testach na podobne sposoby. Można by było części testów się pozbyć.
- Brakuje sprawdzania przekazywania niepoprawnych typów w testach - pokrycie jest tylko kilku takich przypadków
- Brakuje testów związanych z wydajnością, np. dodanie lub usunięcie tysięcy produktów.
- Brakuje testów odpornościowych, np. bardzo duże liczby, wartości typu `inf`, `NaN`.

## Pomijane scenariusze

- niektóre testy z niepoprawnymi wartościami argumentów
- niektóre testy z niepoprawnymi typami
- testy precyzji obliczeń
- test wydajnościowe / odpornościowe


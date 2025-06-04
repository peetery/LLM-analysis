# Podsumowanie analizy pokrycia testów jednostkowych (Model: DeepSeek)
# Kontekst: full context
# Strategia promptowania: chain-of-thought

## coverage.py
- missing: 1
- partial: 1
- coverage: 99%

## mutmut.py
⠋ 217/217  🎉 108 🫥 0  ⏰ 0  🤔 0  🙁 109  🔇 0

## Rezultaty
- Statement coverage: 99%
- Branch coverage: 98%
- Mutation score: 50%

## Ogólne informacje

Liczba wszystkich własnych scenariuszy: 54

- Testy wygenerowane przez LLM: 61
- Testy zakończone powodzeniem: 61
- Testy zakończone niepowodzeniem: 0


- Liczba pokrytych scenariuszy testowych: 46
- Liczba niepotrzebnych testów: 15
<br/>NOTKA: Niektóre z tych testów można uznać za ciekawe przypadki, ale jednak większość rzeczywiście jest niepotrzebna.
- Liczba scenariuszy niepokrytych: 8
- Szybkość: wysoka (2 minuty 50 sekund na 3 prompty)

## Plusy

- 61/61 testów przechodzi.
- Model pokrył prawie wszystkie typowe scenariusze testowe (z wyjątkiem 1).
- Model pokrył prawie wszystkie typowe corner case'y.
- Testy są dobrze zorganizowane i świetnie podzielone na pojedyncze asercje.
- Testy mają przejrzyste i czytelne nazwy metod.
- Model wykazuje potencjał do wykrywania edge case'ów. W kilku przypadkach sprawdzał skrajne wartości.

## Minusy

- Brakuje testów związanych z wydajnością, np. dodanie lub usunięcie tysięcy produktów.
- Brakuje testów odpornościowych, np. bardzo duże liczby, wartości typu `None`, `inf`, `NaN`.
- Brakuje większej różnorodności inputów.

## Pomijane scenariusze

- brakuje 1 typowego scenariusza testowego
- testy precyzji obliczeń
- test wydajnościowe / odpornościowe


# Podsumowanie analizy pokrycia testów jednostkowych (Model: DeepSeek)
# Kontekst: full context
# Strategia promptowania: simple prompting

## coverage.py
- missing: 1
- partial: 1
- coverage: 99%

## mutmut.py
⠇ 217/217  🎉 90 🫥 0  ⏰ 0  🤔 0  🙁 127  🔇 0

## Rezultaty
- Compilation success rate: 95%
- Statement coverage: 99%
- Branch coverage: 98%
- Mutation score: 41%

## Ogólne informacje

Liczba wszystkich własnych scenariuszy: 54

- Testy wygenerowane przez LLM: 42
<br/> <strong>NOTKA: pojawiają się testy z kilkoma asercjami</strong>
- Testy zakończone powodzeniem: 40
- Testy zakończone niepowodzeniem: 2


- Liczba pokrytych scenariuszy testowych: 45
- Liczba niepotrzebnych testów: 0
- Liczba scenariuszy niepokrytych: 10
- Szybkość: średnia (1 minuta 10 sekund)

## Plusy

- Testy są dobrze zorganizowane i podzielone na różne klasy.
- Testy mają przejrzyste i czytelne nazwy metod.
- (!) Testy pokrywają bardzo dużo scenariuszy testowych względem liczby testów. Genialna proporcja. Brak testów niepotrzebnych.
- Nieduża ilość kodu, niewielka ilość testów, a pokrycie scenariuszy wysokie.
- Pokrywa prawie wszystkie typowe scenariusze (pomija 2).
- Pokrywa wszystkie typowe corner case'y.

## Minusy

- Model nie sprawdza kompletnie edge case'ów.
- Brakuje testów związanych z wydajnością, np. dodanie lub usunięcie tysięcy produktów.
- Brakuje testów odpornościowych, np. bardzo duże liczby, wartości typu `None`, `inf`, `NaN`.
- Brakuje większej różnorodności inputów.

## Pomijane scenariusze

- 2 typowe scenariusze testowe
- testy precyzji obliczeń
- test wydajnościowe / odpornościowe


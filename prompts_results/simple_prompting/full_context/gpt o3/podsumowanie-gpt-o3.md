# Podsumowanie analizy pokrycia testów jednostkowych (Model: gpt o3)
# Kontekst: full context
# Strategia promptowania: simple prompting

## coverage.py
- missing: 6
- partial: 6
- coverage: 92%

## mutmut.py
⠋ 217/217  🎉 106 🫥 0  ⏰ 0  🤔 0  🙁 111  🔇 0

## Rezultaty
- Statement coverage: 92%
- Branch coverage: 89%
- Mutation score: 49%

## Ogólne informacje

Liczba wszystkich własnych scenariuszy: 54

- Testy wygenerowane przez LLM: 36
<br/> <strong>NOTKA: pojawiają się testy z kilkoma asercjami</strong>
- Testy zakończone powodzeniem: 36
- Testy zakończone niepowodzeniem: 0


- Liczba pokrytych scenariuszy testowych: 38
- Liczba niepotrzebnych testów: 0
- Liczba scenariuszy niepokrytych: 17
- Szybkość: umiarkowana

## Plusy

- Wszystkie testy przechodzą
- Testy są dobrze zorganizowane i podzielone, mają przejrzyste nazwy metod.

## Minusy

- Brakuje testów związanych z wydajnością, np. dodanie lub usunięcie tysięcy produktów.
- Brakuje testów odpornościowych, np. bardzo duże liczby, wartości typu `None`, `inf`, `NaN`.
- Brakuje pojedynczych typowych scenariuszy testowych.
- Brakuje wiele corner case'ów, sprawdza często niepoprawne wartości ale robi to tylko dla 'jednej strony'. Niedokładnie sprawdza corner case'y przez co nie pokrywa wszystkich przypadków.
- Patrząc na ilość dostarczonego kontekstu, testy wypadają bardzo słabo.

## Pomijane scenariusze

- testy precyzji obliczeń
- test wydajnościowe / odpornościowe
- niektóre corner case'y
- pojedyncze scenariusze testowe


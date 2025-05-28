# Podsumowanie analizy pokrycia testów jednostkowych (Model: gpt o3)
# Kontekst: full context
# Strategia promptowania: chain-of-thought

## coverage.py
- missing: 1
- partial: 1
- coverage: 99%

## mutmut.py
⠦ 217/217  🎉 114 🫥 0  ⏰ 0  🤔 0  🙁 103  🔇 0

## Ogólne informacje

Liczba wszystkich własnych scenariuszy: 54

- Testy wygenerowane przez LLM: 49
<br/> <strong>NOTKA: pojawiają się testy z kilkoma asercjami</strong>
- Testy zakończone powodzeniem: 49
- Testy zakończone niepowodzeniem: 0


- Liczba pokrytych scenariuszy testowych: 48
- Liczba niepotrzebnych testów: 1
- Liczba scenariuszy niepokrytych: 6
- Szybkość: umiarkowana (2 minuty na 3 prompty)

## Plusy

- Wszystkie testy przechodzą
- Testy są dobrze zorganizowane i podzielone, mają przejrzyste nazwy metod. Wręcz wzorowy układ testów.
- Model wykazuje potencjał do sprawdzania edge case'ów
- Model wykazuje potencjał do sprawdzania różnorodnych inputów, a co za tym idzie sprawdzania precyzji obliczeń (dla calculate_total sprawdzał trudniejsze obliczenia)
- Pokrywa wszystkie typowe scenariusze testowe
- Pokrywa wszystkie typowe corner case'y
- Testy są zwięzłe, na 49 testów jest pokrycie 48 scenariuszy.

## Minusy

- Brakuje testów związanych z wydajnością, np. dodanie lub usunięcie tysięcy produktów.
- Brakuje testów odpornościowych, np. bardzo duże liczby, wartości typu `None`, `inf`, `NaN`.

## Pomijane scenariusze

- testy precyzji obliczeń
- test wydajnościowe / odpornościowe


# Podsumowanie analizy pokrycia testów jednostkowych (Model: DeepSeek)
# Kontekst: interface
# Strategia promptowania: simple prompting

## Ogólne informacje

Liczba wszystkich własnych scenariuszy: 54

- Testy wygenerowane przez LLM: 23
<br/> <strong>NOTKA: pojawiają się testy z kilkoma asercjami</strong>
- Testy zakończone powodzeniem: 18
- Testy zakończone niepowodzeniem: 5


- Liczba wykrytych corner case (poprawnie): 5
- Liczba wykrytych corner case (niepoprawnie): 0


- Liczba pokrytych scenariuszy testowych: 22
- Liczba niepotrzebnych testów: 1
- Liczba scenariuszy niepokrytych: 32
- Szybkość: wysoka (40 sekund)

## Plusy

- Wykrył 5 coner case'ów na bazie samego interfejsu i przewidział jeszcze je poprawnie.
- Testy są dobrze zorganizowane i podzielone na różne klasy.
- Testy mają przejrzyste i czytelne nazwy metod.
- Prawie tyle samo testów co pokrytych scenariuszy testowych. Tylko jeden test niepotrzebny.

## Minusy

- Brakuje wielu typowych scenariuszy testowych.
- Brakuje wielu corner case.
- Model wykazuje mały potencjał na sprawdzanie edge casów, zrobił to tylko w 2 przypadkach, robi to losowo.
- Brakuje testów związanych z wydajnością, np. dodanie lub usunięcie tysięcy produktów.
- Brakuje testów odpornościowych, np. bardzo duże liczby, wartości typu `None`, `inf`, `NaN`.
- Brakuje większej różnorodności inputów.

## Pomijane scenariusze

- typowe scenariusze testowe
- corner case'y
- testy precyzji obliczeń
- test wydajnościowe / odpornościowe


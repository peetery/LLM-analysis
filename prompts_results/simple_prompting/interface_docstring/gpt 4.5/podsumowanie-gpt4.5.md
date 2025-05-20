# Podsumowanie analizy pokrycia testów jednostkowych (Model: gpt 4.5)

## Ogólne informacje

Liczba wszystkich własnych scenariuszy: 54

- Testy wygenerowane przez LLM: 26
<br/> <strong>NOTKA: pojawiają się testy z kilkoma asercjami</strong>
- Testy zakończone powodzeniem: 25
- Testy zakończone niepowodzeniem: 1


- Liczba pokrytych scenariuszy testowych: 30
- Liczba niepotrzebnych testów: 0
- Liczba scenariuszy niepokrytych: 24
- Szybkość: bardzo niska

## Plusy

- 25/26 testów przechodzi. Jeden test zawiera błąd logiczny.
- Testy są dobrze zorganizowane i podzielone na różne klasy.
- Testy mają przejrzyste i czytelne nazwy metod.

## Minusy

- Brakuje testów związanych z wydajnością, np. dodanie lub usunięcie tysięcy produktów.
- Brakuje testów odpornościowych, np. bardzo duże liczby, wartości typu `None`, `inf`, `NaN`.
- Brakuje większej różnorodności inputów
- Brakuje dużo corner case'ów - często były sprawdzane tylko pojedyncze argumenty z danych metod i czy są rzucane wtedy wyjątki, model zapominał sprawdzić wszystkie parametry
- Brakuje corner case'a sprawdzenia czy poprawnie zachowuje sie add_item gdy dodajemy 2 produkty o tych samych nazwach, ale innych cenach

## Pomijane scenariusze

- testy precyzji obliczeń
- test wydajnościowe / odpornościowe
- corner case'y rzucające wyjątki TypeError czy też ValueError
- niektóre scenariusze testowe typu obliczanie totalu z różnymi założeniami w kwestii zniżek czy shippingu


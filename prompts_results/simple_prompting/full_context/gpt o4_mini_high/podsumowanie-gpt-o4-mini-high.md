# Podsumowanie analizy pokrycia testów jednostkowych (Model: gpt o4-mini-high)
# Kontekst: full context
# Strategia promptowania: simple prompting

## coverage.py
- missing: 1
- partial: 1
- coverage: 99%

## mutmut.py
⠋ 217/217  🎉 109 🫥 0  ⏰ 0  🤔 0  🙁 108  🔇 0

## Ogólne informacje

Liczba wszystkich własnych scenariuszy: 54

- Testy wygenerowane przez LLM: 51
<br/> <strong>NOTKA: pojawiają się testy z kilkoma asercjami</strong>
- Testy zakończone powodzeniem: 51
- Testy zakończone niepowodzeniem: 0

- Liczba pokrytych scenariuszy testowych: 48
- Liczba niepotrzebnych testów: 3 (pod znakiem zapytania, ponieważ te testy mają swoją wartość dodatnią, że sprawdzają precyzyjnie dane zachowanie lub robią to na wiele różnych sposobów. Nie do końca można je uznać za całkowicie bezużyteczne)
- Liczba scenariuszy niepokrytych: 6
- Szybkość: wysoka

## Plusy

- 51/51 testów przechodzi.
- Testy są dobrze zorganizowane i podzielone na różne klasy.
- Testy mają przejrzyste i czytelne nazwy metod.
- Świetnie wykrywa corner case'y - pokrył wszystkie typowe corner-case'y.
- Pokrywa wszystkie typowe funkcjonalności.
- Model wykazuje potencjał do wykrywania edge case'ów - sprawdzania skrajnych wartości przy ifach etc.
- Model wykazuje potencjał do sprawdzania różnych inputów i weryfikowania działania metod na bardziej nietypowych liczbach.

## Minusy

- Brakuje testów związanych z wydajnością, np. dodanie lub usunięcie tysięcy produktów.
- Brakuje testów odpornościowych, np. bardzo duże liczby, wartości typu `None`, `inf`, `NaN`.

## Pomijane scenariusze

- testy precyzji obliczeń
- test wydajnościowe / odpornościowe

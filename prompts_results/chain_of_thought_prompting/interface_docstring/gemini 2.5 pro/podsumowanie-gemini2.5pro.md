# Podsumowanie analizy pokrycia testów jednostkowych (Model: gemini 2.5 pro)
# Strategia promptowania: chain-of-thought

## Ogólne informacje

Liczba wszystkich własnych scenariuszy: 54

- Testy wygenerowane przez LLM: 88
<br/> <strong>NOTKA: pojawiają się testy z kilkoma asercjami</strong>
- Testy zakończone powodzeniem: 61
- Testy zakończone niepowodzeniem: 17
- <br/> <strong>NOTKA: tyle niepowodzeń wynika z tego że model ma duże halucynacje i się nie słucha. Tworzy wlasna implementacje OrderCalculator i jak sprawdza np wyjatki to weryfikuje czy komunikat jest identyczny... przez co porównanie do realnej klasy powoduje sporo blędów</strong>


- Liczba pokrytych scenariuszy testowych: 48
- Liczba niepotrzebnych testów: 40
- <br/> <strong>NOTKA: nie wszystkie testy można jednoznacznie uznać za niepotrzebnie, ponieważ wiele testów sprawdza metody na niepospolite sposoby, co daje pewną wartość dodatnią</strong>
- Liczba scenariuszy niepokrytych: 7 
- Szybkość: niska

## Plusy

- Model wykazuje dużą kreatywność w generowaniu testów, co prowadzi do dużej liczby testów i sprawdzania różnych inputów, co wyróżnia go na tle pozostałych pod tym względem. Sprawdza też edge case'y.
- Pokrywa wszystkie typowe funkcjonalności, z tym że popełnia mnóstwo błędów, przez co sporo testów kończy się niepowodzeniem
- Pokrywa wszystkie typowe corner case'y.
- Dobre nazewnictwo testów i organizacja.

## Minusy

- Tylko 61/88 testów przechodzi.
- Bardzo duże halucynacje, dziwne zachowanie. Przy sprawdzaniu wyjątków chce sprawdzać również czy został rzucony poprawny komunikat, a o strukturze komunikatu nie ma pojęcia z docstringów. Z tego wynika mnóstwo błędów.
- Błędy wynikają głównie z tego że model stwierdził, że napisze na podstawie docstringów swoją klasę OrderCalculator, którą nastepnie będzie testował. Przez co tworzy potem różniące od rzeczywistości działanie niektórych metod.
- Zignorował instrukcję, aby nie pisać komentarzy.
- Niektóre testy są bardzo podobne do siebie i mogłyby zostać uproszczone lub połączone.
- Brakuje testów związanych z wydajnością, np. dodanie lub usunięcie tysięcy produktów.
- Brakuje testów odpornościowych, np. bardzo duże liczby, wartości typu `None`, `inf`, `NaN`.

## Pomijane scenariusze

- testy precyzji obliczeń
- test wydajnościowe / odpornościowe


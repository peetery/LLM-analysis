# Podsumowanie analizy pokrycia testów jednostkowych (Model: gemini 2.5 pro)
# Kontekst: interfejs + docstring
# Strategia promptowania: simple prompting

## coverage.py
- missing: 1
- partial: 1
- coverage: 99%

## mutmut.py
⠇ 217/217  🎉 128 🫥 0  ⏰ 0  🤔 0  🙁 89  🔇 0

## Rezultaty
- Compilation success rate: 64%
- Statement coverage: 99%
- Branch coverage: 98%
- Mutation score: 59%

## Ogólne informacje

Liczba wszystkich własnych scenariuszy: 54

- Testy wygenerowane przez LLM: 73
<br/> <strong>NOTKA: pojawiają się testy z kilkoma asercjami</strong>
- Testy zakończone powodzeniem: 47
- Testy zakończone niepowodzeniem: 26


- Liczba pokrytych scenariuszy testowych (poprawnie): 16
- Liczba pokrytych scenariuszy testowych (niepoprawnie): 31 
- Liczba niepotrzebnych testów: 26
- Liczba scenariuszy niepokrytych: 7 
- Szybkość: niska

## Plusy

- Model wykazuje dużą kreatywność w generowaniu testów, co prowadzi do dużej liczby testów i sprawdzania różnych inputów, co wyróżnia go na tle pozostałych pod tym względem. Sprawdza też edge case'y.
- Pokrywa wszystkie typowe funkcjonalności, z tym że popełnia mnóstwo błędów, przez co większość testów kończy się niepowodzeniem.

## Minusy

- Tylko 47/73 testów przechodzi, z czego pokrywają one raptem 16 scenariuszy testowych. Jednak te 16 scenariuszy testowych jest sprawdzonych na wiele różnych sposobów.
- Bardzo duże halucynacje, dziwne zachowanie. Przy sprawdzaniu wyjątków chce sprawdzać również czy został rzucony poprawny komunikat, a o strukturze komunikatu nie ma pojęcia z docstringów. Oprócz tego pomylił nazwę items, którą nazywał _items. Z tych dwóch błędów wynikła masa nieskutecznych testów.
- Błędy wynikają głównie z tego że model stwierdził, że napisze na podstawie docstringów swoją klasę OrderCalculator, którą nastepnie będzie testował. Przez co tworzy potem różniące od rzeczywistości działanie niektórych metod.
- Zignorował instrukcję, aby nie pisać komentarzy.
- Niektóre testy są bardzo podobne do siebie i mogłyby zostać uproszczone lub połączone.
- Brakuje testów związanych z wydajnością, np. dodanie lub usunięcie tysięcy produktów.
- Brakuje testów odpornościowych, np. bardzo duże liczby, wartości typu `None`, `inf`, `NaN`.

## Pomijane scenariusze

- testy precyzji obliczeń
- test wydajnościowe / odpornościowe


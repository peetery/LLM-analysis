# Podsumowanie analizy pokrycia testów jednostkowych (Model: gpt 4.5)
# Kontekst: interfejs + docstring
# Strategia promptowania: chain-of-thought

## coverage.py
- missing: 7
- partial: 8
- coverage: 91%

## mutmut.py
⠹ 217/217  🎉 101 🫥 5  ⏰ 0  🤔 0  🙁 111  🔇 0

## Rezultaty
- Statement coverage: 91%
- Branch coverage: 86%
- Mutation score: 47%

## Ogólne informacje

Liczba wszystkich własnych scenariuszy: 54

- Testy wygenerowane przez LLM: 43
- Testy zakończone powodzeniem: 42
- Testy zakończone niepowodzeniem: 1


- Liczba pokrytych scenariuszy testowych: 37
- Liczba niepotrzebnych testów: 6
- Liczba scenariuszy niepokrytych: 17
- Szybkość: bardzo niska (ponad 4 minuty na 3 prompty)

## Plusy

- 42/43 testów przechodzi. Jeden test zawiera błąd logiczny.
- Testy są dobrze zorganizowane i podzielone na różne klasy. Są atomiczne (mają po jednej asercji).
- Testy mają przejrzyste i czytelne nazwy metod.
- Model wykazuje potencjał do sprawdzania edge case'ów, ale przypadki sprawdzane są wybierane losowo i nie sprawdza wszystkich.

## Minusy

- Brakuje testów związanych z wydajnością, np. dodanie lub usunięcie tysięcy produktów.
- Brakuje testów odpornościowych, np. bardzo duże liczby, wartości typu `None`, `inf`, `NaN`.
- Brakuje większej różnorodności inputów
- Brakuje niektórych corner case'ów dla niepoprawnych typow.
- Zgubił kontekst z czatu, rozpisał znacznie wiecej scenariuszy niż napisał testów.

## Pomijane scenariusze

- testy precyzji obliczeń
- test wydajnościowe / odpornościowe
- corner case'y rzucające wyjątki TypeError czy też ValueError
- niektóre scenariusze testowe typu obliczanie totalu z różnymi założeniami w kwestii zniżek czy shippingu
- pojedyncze typowe scenariusze


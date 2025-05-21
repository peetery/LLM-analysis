# Podsumowanie analizy pokrycia testów jednostkowych (Model: gemini 2.5 pro)
# Kontekst: interfejs
# Strategia promptowania: chain-of-thought

## coverage.py
- missing: 1
- partial: 1
- coverage: 99%

## Ogólne informacje

Liczba wszystkich własnych scenariuszy: 54

- Testy wygenerowane przez LLM: 95 (!!!)
- Testy zakończone powodzeniem: 79
- Testy zakończone niepowodzeniem: 16


- Liczba pokrytych scenariuszy testowych: 47
- Liczba niepotrzebnych testów: 48
<br/> <strong>NOTKA: nie można jednoznacznie stwierdzić że wszystkie testy są niepotrzebne. Wiele z nich bardzo precyzyjnie i w sposób niespotykany dotąd testuje metody na wiele różnych sposobów, sprawdzając na prawdę dużą różnorodność przypadków i inputów - to zasługuje na pochwałę i mimo że te testy pokrywają czasem te same przypadki to część z nich można dalej uznać za wartościowe.</strong>
- Liczba scenariuszy niepokrytych: 7
- Szybkość: niska (3 prompty to czas koło 2 minut)

## Plusy

- Wybitne pokrycie scenariuszy testowych przy jedynie interfejsie jako kontekście klasy. Dodatkowo 16 niepowodzeń przy 95 testach jest dalej świetnym wynikiem.
- BARDZO Dobre nazewnictwo metod, schematycznie poukładane testy, które są łatwe do zrozumienia.
- Bardzo dokładnie, na mnóstwo sposobów sprawdza metody, jest bardzo kreatywny przy tworzeniu scenariuszy testowych.
- Sprawdza niepoprawny typ dla None!
- Model wykazuje potencjał do sprawdzania dużej ilości edge case'ów, co może być przydatne w testowaniu.
- Model wykazuje dużą kreatywność w generowaniu testów, co prowadzi do dużej liczby testów i sprawdzania różnych inputów, co wyróżnia go na tle pozostałych pod tym względem. Sprawdza też edge case'y.
- Jako jeden z niewielu model wykazuje ogromny potencjał w testowaniu precyzji obliczeń, a nawet weryfikowania działania metod w mnóstwie różnych przypadków - pozwala wykryć nawet przypadki, które nie były do tej pory przewidziane i nad którymi może warto byłoby się zastanowić. Jest to bardzo imponujące.
- Pokrywa wszystkie typowe funkcjonalności oraz corner case'y.

## Minusy

- Model pisze sam implementację klasy, mimo braku takiej prośby w prompcie. To może być przyczyną dużych halucynacji w odpowiedziach, bo zależy jak wygeneruje tą klasę - było widać to na przykładzie interface+docstirng dla gemini 2.5 pro.
- Niektóre testy są bardzo podobne do siebie i mogłyby zostać uproszczone lub połączone.
- Brakuje testów związanych z wydajnością, np. dodanie lub usunięcie tysięcy produktów.
- Brakuje testów odpornościowych, np. bardzo duże liczby, wartości typu `None`, `inf`, `NaN`.

## Pomijane scenariusze

- niektóre testy precyzji, sprawdza to tylko dla niektórych metod, brakuje tutaj bycia bardziej systematycznym
- test wydajnościowe / odpornościowe
- brakuje jednego typowego corner case (init z tax_rate > 1.0) oraz jednego typowego scenariusza testowego (calculate_total na pustym order)


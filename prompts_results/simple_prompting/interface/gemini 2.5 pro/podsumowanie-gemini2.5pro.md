# Podsumowanie analizy pokrycia testów jednostkowych (Model: gemini 2.5 pro)
# Kontekst: interfejs
# Strategia promptowania: simple prompting

## coverage.py
- missing: 2
- partial: 2
- coverage: 97%

## mutmut.py
⠦ 217/217  🎉 111 🫥 0  ⏰ 0  🤔 0  🙁 106  🔇 0

## Ogólne informacje

Liczba wszystkich własnych scenariuszy: 54

- Testy wygenerowane przez LLM: 80
<br/> <strong>NOTKA: pojawiają się testy z kilkoma asercjami</strong>
- Testy zakończone powodzeniem: 68
- Testy zakończone niepowodzeniem: 12


- Liczba pokrytych scenariuszy testowych: 46
- Liczba niepotrzebnych testów: 34
<br/> <strong>NOTKA: nie można jednoznacznie stwierdzić że wszystkie 34 testy są niepotrzebne. Wiele z nich bardzo precyzyjnie i w sposób niespotykany dotąd testuje metody na wiele różnych sposobów, sprawdzając na prawdę dużą różnorodność przypadków i inputów - to zasługuje na pochwałę i mimo że te testy pokrywają czasem te same przypadki to część z nich można dalej uznać za wartościowe.</strong>
- Liczba scenariuszy niepokrytych: 8
- Szybkość: niska

## Plusy

- Dobre nazewnictwo metod, schematycznie poukładane testy, które są łatwe do zrozumienia.
- Model wykazuje dużą kreatywność w generowaniu testów, co prowadzi do dużej liczby testów i sprawdzania różnych inputów, co wyróżnia go na tle pozostałych pod tym względem. Sprawdza też edge case'y.
- Jako jeden z niewielu model wykazuje ogromny potencjał w testowaniu precyzji obliczeń, a nawet weryfikowania działania metod w mnóstwie różnych przypadków - pozwala wykryć nawet przypadki, które nie były do tej pory przewidziane i nad którymi może warto byłoby się zastanowić. Jest to bardzo imponujące.
- Pokrywa wszystkie typowe funkcjonalności oraz corner case'y.

## Minusy

- Tylko 68/80 testów przechodzi, z czego pokrywają one 46 scenariuszy.
- Model pisze sam implementację klasy, mimo braku takiej prośby w prompcie. To może być przyczyną dużych halucynacji w odpowiedziach, bo zależy jak wygeneruje tą klasę - było widać to na przykładzie interface+docstirng dla gemini 2.5 pro.
- Niektóre testy są bardzo podobne do siebie i mogłyby zostać uproszczone lub połączone.
- Brakuje testów związanych z wydajnością, np. dodanie lub usunięcie tysięcy produktów.
- Brakuje testów odpornościowych, np. bardzo duże liczby, wartości typu `None`, `inf`, `NaN`.

## Pomijane scenariusze

- test wydajnościowe / odpornościowe
- brakuje jednego typowego corner case (init z tax_rate > 1.0) oraz jednego typowego scenariusza testowego (calculate_total na pustym order)


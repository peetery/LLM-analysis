# Podsumowanie analizy pokrycia testów jednostkowych (Model: gemini 2.5 pro)

## Ogólne informacje

Liczba wszystkich własnych scenariuszy: 54

- Testy wygenerowane przez LLM: 72
- Testy zakończone powodzeniem: 72
- Testy zakończone niepowodzeniem: 0


- Liczba pokrytych scenariuszy testowych: 48
- Liczba niepotrzebnych testów: 24
<br/> <strong>NOTKA: nie można jednoznacznie stwierdzić że wszystkie 24 testy są niepotrzebne. Wiele z nich bardzo precyzyjnie i w sposób niespotykany dotąd testuje metody na wiele różnych sposobów, sprawdzając na prawdę dużą różnorodność przypadków i inputów - to zasługuje na pochwałę i mimo że te testy pokrywają czasem te same przypadki to część z nich można dalej uznać za wartościowe. Metody są sprawdzane bardzo dokładnie, testowane są wszystkie edge case'y. Ciężko mieć jakieś zarzuty wobec tych testów. Są świetne.</strong>
- Liczba scenariuszy niepokrytych: 6
- Szybkość: niska

## Plusy

- 72/72 testów przechodzi.
- Dobre nazewnictwo metod, schematycznie poukładane testy, które są łatwe do zrozumienia.
- Świetna organizacja testów, podzielenie że każdy test sprawdza jednną metodę i jej konkretne jedno działanie. Są dzięki temu bardzo przejrzyste.
- Model wykazuje dużą kreatywność w generowaniu testów, co prowadzi do dużej liczby testów i sprawdzania różnych inputów, co wyróżnia go na tle pozostałych pod tym względem. Sprawdza też edge case'y, swoją analizę wykonuje na prawdę bardzo dokładnie.
- Jako jeden z niewielu model wykazuje ogromny potencjał w testowaniu precyzji obliczeń, a nawet weryfikowania działania metod w mnóstwie różnych przypadków - pozwala wykryć nawet przypadki, które nie były do tej pory przewidziane i nad którymi może warto byłoby się zastanowić. Jest to bardzo imponujące.
- Pokrywa wszystkie typowe funkcjonalności oraz corner case'y.

## Minusy

- Model pisze sam implementację klasy, mimo braku takiej prośby w prompcie.
- Niektóre testy są bardzo podobne do siebie i mogłyby zostać uproszczone lub połączone.
- Brakuje testów związanych z wydajnością, np. dodanie lub usunięcie tysięcy produktów.
- Brakuje testów odpornościowych, np. bardzo duże liczby, wartości typu `None`, `inf`, `NaN`.

## Pomijane scenariusze

- test wydajnościowe / odpornościowe

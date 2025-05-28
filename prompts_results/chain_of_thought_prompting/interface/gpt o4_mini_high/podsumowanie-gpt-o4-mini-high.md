# Podsumowanie analizy pokrycia testów jednostkowych (Model: gpt o4-mini-high)
# Kontekst: interfejs
# Strategia promptowania: chain-of-thought

## coverage.py
- missing: 9
- partial: 9
- coverage: 88%

## mutmut.py
⠦ 217/217  🎉 104 🫥 0  ⏰ 0  🤔 0  🙁 113  🔇 0

## Ogólne informacje

Liczba wszystkich własnych scenariuszy: 54

- Testy wygenerowane przez LLM: 65
<br/> <strong>NOTKA: pojawiają się testy z kilkoma asercjami</strong>
- Testy zakończone powodzeniem: 45
- Testy zakończone niepowodzeniem: 19

- Wykryte corner case: 14 (niepoprawnie: 4)

- Liczba pokrytych scenariuszy testowych: 35
- Liczba niepotrzebnych testów: 30
<br/> <strong>NOTKA: nie można wszystkich uznać za niepotrzebne, choć faktycznie część z nich jest niepotrzebna. Natomiast jest sporo testów, które prezentują ciekawe podejście do problemu i testują funkcje w nietypowy sposób w specyifcznych warunkach, które ciężko by było przewidzieć.</strong>
- Liczba scenariuszy niepokrytych: 19
- Szybkość: umiarkowana (60sekund na 3 prompty, samo generowanie testów to 50s)

## Plusy

- 45/65 testów przechodzi.
- Testy są dobrze zorganizowane i podzielone na różne klasy.
- Testy mają przejrzyste i czytelne nazwy metod.
- Przyzwoicie wykrywa corner case'y na bazie samych interfejsów - przewidział aż 16 corner case'ów z czego jeden błędnie.
- Pokrywa znaczną większość typowych funkcjonalności
- Model wykazuje potencjał do wykrywania edge case'ów i dobrej umiejętności przewidywania zawartości klasy na podstawie samego interfejsu.
- Model testuje funkcje na różnorodnych inputach.
- ! Przewidział poprawne zachowanie przy dodaniu dwa razy przedmiotu o tej samej nazwie i cenie - domyślił się że quantity będzie sumowane i przetestował to.

## Minusy

- Brakuje testów związanych z wydajnością, np. dodanie lub usunięcie tysięcy produktów.
- Brakuje testów odpornościowych, np. bardzo duże liczby, wartości typu `None`, `inf`, `NaN`.
- Brakuje pojedyńczych corner case'ów, niektóre zostały pominięte. Sprawdzanie rzucania wyjątków jest trochę losowe, model w dobry sposób myśli, ale nie przewiduje wszystkich możliwych scenariuszy.
- popełnił pare błędów logicznych, jednak jest to zrozumiałe przy samym interfejsie.

## Pomijane scenariusze

- testy precyzji obliczeń
- test wydajnościowe / odpornościowe
- corner case'y dla niektórych metod - wykrywanie TypeError czy ValueError
- pomija pojedyncze scenariusze testowe

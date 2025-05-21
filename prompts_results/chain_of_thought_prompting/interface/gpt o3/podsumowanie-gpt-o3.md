# Podsumowanie analizy pokrycia testów jednostkowych (Model: gpt o3)
# Kontekst: interfejs
# Strategia promptowania: chain-of-thought

## coverage.py
- missing: 13
- partial: 13
- coverage: 83%

## Ogólne informacje

Liczba wszystkich własnych scenariuszy: 54

- Testy wygenerowane przez LLM: 56
<br/> <strong>NOTKA: pojawiają się testy z kilkoma asercjami</strong>
- Testy zakończone powodzeniem: 43
- Testy zakończone niepowodzeniem: 13


- Liczba wykrytych corner case'ów: 12 (niepoprawnie 5)


- Liczba pokrytych scenariuszy testowych: 37
- Liczba niepotrzebnych testów: 17
<br/> <strong>NOTKA: ciężko to ocenić tak jednoznacznie, ponieważ generuje bardzo ciekawe testy, weryfikuje bardzo nietypowe scenariusze testowe, ktore nie zostały uwzględnione w autorksich testach, ponieważ ciężko rozpisać je jako scenariusze ale weryfikują działanie klasy w specyficznych warunkach. Jest to na pewno duży plus.</strong>
- Liczba scenariuszy niepokrytych: 19
- Szybkość: umiarkowana (50-60s na 3 prompty)

## Plusy

- Model wykazuje potencjał do generowania testów wydajnościowych i testów odpornościowych - sprawdza dla pojedynczych przypadków wydajność czy precyzyjność testowanych metod poprzez ogromne liczby bądź długie liczby zmiennoprzecinkowe.
- Model wykazuje bardzo dużą kreatywność i ciekawe podejście w generowaniu testów jednostkowych - sprawdza bardzo nietypowe scenariusze, które weryfikują działąnie klasy w nietypowych warunkach. Pozwala to poszerzyć horyzonty i spojrzeć na problem z innej perspektywy.
- Model wykazuje potencjał do uwzględniania sprawdzania wartości tzw edge case'ów w przypadku ograniczeń dla parametrów sprawdza wartości skrajne czy przechodzą czy nie.
- Model wykazuje potencjał do przewidywania corner case'ów, jednak sprawdza ich niewiele - a wybór wydaje się być przypadkowy.
- Testy są dobrze zorganizowane i podzielone, mają przejrzyste nazwy metod.

## Minusy

- Brakuje kilku testów związanych z wydajnością, np. dodanie lub usunięcie tysięcy produktów.
- Brakuje testów odpornościowych z wartościami typu `None`, `inf`, `NaN`.
- Brakuje trochę typowych scenariuszy testowych, lecz wynik i tak jest przyzwoity.
- Brakuje corner case'ów sprawdzających niepoprawne typy danych
- Popełnia dużo błędów w założeniach logiki, lecz jest to zrozumiałe. Bazował tylko na interfejsie klasy.

## Pomijane scenariusze

- niektóre test wydajnościowe / odpornościowe
- corner case'y związane z niepoprawnymi typami danych


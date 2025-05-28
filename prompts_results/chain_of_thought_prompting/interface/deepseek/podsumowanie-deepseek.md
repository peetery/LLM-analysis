# Podsumowanie analizy pokrycia testów jednostkowych (Model: DeepSeek)
# Kontekst: interfejs
# Strategia promptowania: chain-of-thought

## coverage.py
- missing: 17
- partial: 17
- coverage: 77%

## mutmut.py
⠹ 217/217  🎉 96 🫥 0  ⏰ 0  🤔 0  🙁 121  🔇 0

## Ogólne informacje

Liczba wszystkich własnych scenariuszy: 54

- Testy wygenerowane przez LLM: 37
<br/> <strong>NOTKA: pojawiają się testy z kilkoma asercjami</strong>
- Testy zakończone powodzeniem: 28
- Testy zakończone niepowodzeniem: 9


- Liczba wykrytych corner case (poprawnie): 6
- Liczba wykrytych corner case (niepoprawnie): 2


- Liczba pokrytych scenariuszy testowych: 29
- Liczba niepotrzebnych testów: 9
<br/> <strong>NOTKA: nie można jednoznacznie stwierdzić czy wszystkie są niepotrzebnie, niektóre z testów sprawdzają specyficzne zachowanie metod, są to nawet do tory niespotykane scenariusze, więc można to też potraktować jako pewien plus. Ciekawe przypadki. </strong>
- Liczba scenariuszy niepokrytych: 15
- Szybkość: wysoka (2 minuty 40 sekund na 3 prompty)

## Plusy

- Wykrył 8 coner case'ów na bazie samego interfejsu i przewidział 6/8 poprawnie.
- Model wykazuje potencjał do wykrywania corner case'ów, lecz jest w tym co robi niekonsekwetny. Sprawdzał poprawność typów, ale tylko dla losowo wybranych przykładów. Gdyby sprawdził wszędzie, wykryłby znacznie więcej corner case'ów.
- Testy są dobrze zorganizowane i podzielone na różne klasy.
- Testy mają przejrzyste i czytelne nazwy metod.
- Model wykazuje potencjał (choć nie jest bardzo dobrze) do wykrywania edge case'ów. W kilku przypadkach sprawdzał skrajne wartości.
- Model wykazuje duży potencjał do sprawdzania różnorodności inputów i sprawdzania nie takich prostych obliczeń
- (!) Jako jedyny do tej pory jako ceny produktów zawsze przyjmował wartości x.49, x.99 etc. co dobrze odzwierciedla rzeczywiste ceny produktów w sklepach.

## Minusy

- Brakuje wielu typowych scenariuszy testowych.
- Brakuje wielu corner case.
- Brakuje testów związanych z wydajnością, np. dodanie lub usunięcie tysięcy produktów.
- Brakuje testów odpornościowych, np. bardzo duże liczby, wartości typu `None`, `inf`, `NaN`.
- Brakuje większej różnorodności inputów.

## Pomijane scenariusze

- typowe scenariusze testowe
- corner case'y
- testy precyzji obliczeń
- test wydajnościowe / odpornościowe


# Podsumowanie analizy pokrycia testów jednostkowych (Model: gpt o4-mini-high)
# Kontekst: interfejs
# Strategia promptowania: simple prompting

## coverage.py
- missing: 9
- partial: 9
- coverage: 88%

## mutmut.py
⠇ 217/217  🎉 104 🫥 1  ⏰ 0  🤔 0  🙁 112  🔇 0

## Rezultaty
- Compilation success rate: 88%
- Statement coverage: 88%
- Branch coverage: 84%
- Mutation score: 48%

## Ogólne informacje

Liczba wszystkich własnych scenariuszy: 54

- Testy wygenerowane przez LLM: 33
<br/> <strong>NOTKA: pojawiają się testy z kilkoma asercjami</strong>
- Testy zakończone powodzeniem: 29
- Testy zakończone niepowodzeniem: 4

- Wykryte corner case: 16 (niepoprawnie 1)

- Liczba pokrytych scenariuszy testowych: 35
- Liczba niepotrzebnych testów: 0
- Liczba scenariuszy niepokrytych: 19
- Szybkość: wysoka

## Plusy

- 29/33 testów przechodzi. Jeden test zawiera błąd logiczny.
- Testy są dobrze zorganizowane i podzielone na różne klasy.
- Testy mają przejrzyste i czytelne nazwy metod.
- Świetnie wykrywa corner case'y na bazie samych interfejsów - przewidział aż 16 corner case'ów z czego jeden błędnie.
- Pokrywa znaczną większość typowych funkcjonalności
- Model wykazuje potencjał do wykrywania edge case'ów i dobrej umiejętności przewidywania zawartości klasy na podstawie samego interfejsu.
- Inteligentnie łączy wiele asercji testujących podobne zachowanie w jednym teście, dzięki czemu testów jest mniej, a ich jakość i pokrycie nie spada
- ! Przewidział poprawne zachowanie przy dodaniu dwa razy przedmiotu o tej samej nazwie i cenie - domyślił się że quantity będzie sumowane i przetestował to.

## Minusy

- Brakuje testów związanych z wydajnością, np. dodanie lub usunięcie tysięcy produktów.
- Brakuje testów odpornościowych, np. bardzo duże liczby, wartości typu `None`, `inf`, `NaN`.
- Brakuje pojedyńczych corner case'ów, niektóre zostały pominięte. Sprawdzanie rzucania wyjątków jest trochę losowe, model w dobry sposób myśli, ale nie przewiduje wszystkich możliwych scenariuszy.
- popełnił pare błędów logicznych przez błedne założenia przy chociażby calculate total, nie przewidział braku możliwości get_subtotal gdy items jest puste.

## Pomijane scenariusze

- testy precyzji obliczeń
- test wydajnościowe / odpornościowe
- corner case'y dla niektórych metod - wykrywanie TypeError czy ValueError
- pomija pojedyncze scenariusze testowe

# Scenariusze testowe do klasy `OrderCalculator`

**Łączna liczba scenariuszy: 54**

---

## 0. Inicjalizacja klasy (10 scenariuszy)

### Scenariusz: Domyślna inicjalizacja
- **Wejście:** `OrderCalculator()` bez argumentów
- **Oczekiwany rezultat:** `tax_rate=0.23`, `free_shipping_threshold=100.0`, `shipping_cost=10.0`

### Scenariusz: Poprawna inicjalizacja z własnymi wartościami
- **Wejście:** `tax_rate=0.08`, `free_shipping_threshold=50.0`, `shipping_cost=5.0`
- **Oczekiwany rezultat:** Obiekt utworzony z podanymi wartościami

### Corner case: tax_rate > 1.0
- **Wejście:** `tax_rate=1.01`
- **Oczekiwany rezultat:** `ValueError: "Tax rate must be between 0.0 and 1.0."`

### Corner case: tax_rate < 0.0
- **Wejście:** `tax_rate=-0.01`
- **Oczekiwany rezultat:** `ValueError: "Tax rate must be between 0.0 and 1.0."`

### Corner case: free_shipping_threshold < 0.0
- **Wejście:** `free_shipping_threshold=-0.01`
- **Oczekiwany rezultat:** `ValueError: "Free shipping threshold cannot be negative."`

### Corner case: shipping_cost < 0.0
- **Wejście:** `shipping_cost=-0.01`
- **Oczekiwany rezultat:** `ValueError: "Shipping cost cannot be negative."`

### Corner case: nieoczekiwany typ tax_rate
- **Wejście:** `tax_rate="abc"` lub `tax_rate=None`
- **Oczekiwany rezultat:** `TypeError: "Tax rate must be a float or int."`

### Corner case: nieoczekiwany typ free_shipping_threshold
- **Wejście:** `free_shipping_threshold="abc"` lub `free_shipping_threshold=None`
- **Oczekiwany rezultat:** `TypeError: "Free shipping threshold must be a float or int."`

### Corner case: nieoczekiwany typ shipping_cost
- **Wejście:** `shipping_cost="abc"` lub `shipping_cost=None`
- **Oczekiwany rezultat:** `TypeError: "Shipping cost must be a float or int."`

### Scenariusz: Test wydajności (ekstremalna liczba items)
- **Wejście:** Dodanie 12 789 produktów
- **Oczekiwany rezultat:** `items` zawiera 12 789 elementów, system działa stabilnie

---

## 1. add_item() (10 scenariuszy)

### Scenariusz: Dodanie poprawnego produktu
- **Wejście:** `name="Laptop"`, `price=2999.99`, `quantity=1`
- **Oczekiwany rezultat:** `items` zawiera jeden element, `subtotal` = 2999.99

### Scenariusz: Dodanie tego samego produktu 2 razy (identyczna cena)
- **Wejście 1:** `name="Book"`, `price=50.0`, `quantity=2`
- **Wejście 2:** `name="Book"`, `price=50.0`, `quantity=3`
- **Oczekiwany rezultat:** `items` zawiera jeden element "Book" z ilością 5, `subtotal` = 250.0

### Scenariusz: Bardzo długa nazwa produktu
- **Wejście:** `name="A" * 1000`, `price=50.0`, `quantity=2`
- **Oczekiwany rezultat:** `items` zawiera jeden element z długą nazwą, `subtotal` = 100.0

### Scenariusz: Test wydajności (wielokrotne dodawanie produktów)
- **Wejście:** 1000 razy dodaj produkt "item_x"
- **Oczekiwany rezultat:** Ilość produktu zsumowana do 1000, system działa stabilnie

### Corner case: quantity <= 0
- **Wejście:** `quantity=0` lub `quantity=-1`
- **Oczekiwany rezultat:** `ValueError: "Quantity must be at least 1."`

### Corner case: price <= 0
- **Wejście:** `price=0.0` lub `price=-10.0`
- **Oczekiwany rezultat:** `ValueError: "Price must be greater than 0."`

### Corner case: name = "" (pusty)
- **Wejście:** `name=""`
- **Oczekiwany rezultat:** `ValueError: "Item name cannot be empty."`

### Corner case: Dodanie tego samego produktu 2 razy z różnymi cenami
- **Wejście 1:** `name="Book"`, `price=50.0`, `quantity=2`
- **Wejście 2:** `name="Book"`, `price=60.0`, `quantity=3`
- **Oczekiwany rezultat:** `ValueError: "Item with the same name but different price already exists."`

### Corner case: nieoczekiwany typ name
- **Wejście:** `name=123` lub `name=None`
- **Oczekiwany rezultat:** `TypeError: "Item name must be a string."`

### Corner case: nieoczekiwany typ price
- **Wejście:** `price="abc"` lub `price=None`
- **Oczekiwany rezultat:** `TypeError: "Price must be a number."`

### Corner case: nieoczekiwany typ quantity
- **Wejście:** `quantity="abc"` lub `quantity=1.5`
- **Oczekiwany rezultat:** `TypeError: "Quantity must be an integer."`

---

## 2. remove_item() (4 scenariusze)

### Scenariusz: Usunięcie istniejącego produktu
- **Wejście:** `name="Laptop"` (produkt istnieje w koszyku)
- **Oczekiwany rezultat:** `items` nie zawiera tego produktu

### Scenariusz: Test wydajności (wielokrotne usuwanie produktów)
- **Wejście:** Usunięcie 1000 różnych produktów
- **Oczekiwany rezultat:** Wszystkie produkty usunięte, system działa stabilnie

### Corner case: Usunięcie nieistniejącego produktu
- **Wejście:** `name="NonExistent"`
- **Oczekiwany rezultat:** `ValueError: "Item with name 'NonExistent' does not exist in the order."`

### Corner case: nieoczekiwany typ name
- **Wejście:** `name=123` lub `name=None`
- **Oczekiwany rezultat:** `TypeError: "Item name must be a string."`

---

## 3. get_subtotal() (3 scenariusze)

### Scenariusz: Poprawne obliczanie subtotal
- **Wejście:** 2x "Mouse" po 50.0, 1x "Keyboard" za 200.0
- **Oczekiwany rezultat:** `subtotal` = 300.0

### Scenariusz: Test precyzji obliczeń
- **Wejście:** `price=0.000000001`, `quantity=1_000_000_000`
- **Oczekiwany rezultat:** `subtotal` = 1.0

### Corner case: Subtotal na pustym zamówieniu
- **Wejście:** Puste `items`
- **Oczekiwany rezultat:** `ValueError: "Cannot calculate subtotal on empty order."`

---

## 4. apply_discount() (7 scenariuszy)

### Scenariusz: Poprawna zniżka 20%
- **Wejście:** `subtotal=100.0`, `discount=0.2`
- **Oczekiwany rezultat:** 80.0

### Scenariusz: Test precyzji obliczeń
- **Wejście:** `subtotal=1_234_567_890.1234`, `discount=0.6543`
- **Oczekiwany rezultat:** Wynik obliczony poprawnie z zachowaniem precyzji

### Corner case: discount < 0
- **Wejście:** `discount=-0.1`
- **Oczekiwany rezultat:** `ValueError: "Discount must be between 0.0 and 1.0."`

### Corner case: discount > 1
- **Wejście:** `discount=1.1`
- **Oczekiwany rezultat:** `ValueError: "Discount must be between 0.0 and 1.0."`

### Corner case: subtotal < 0.0
- **Wejście:** `subtotal=-0.1`
- **Oczekiwany rezultat:** `ValueError: "Cannot apply discount on negative subtotal."`

### Corner case: nieoczekiwany typ subtotal
- **Wejście:** `subtotal="abc"` lub `subtotal=None`
- **Oczekiwany rezultat:** `TypeError: "Subtotal must be a number."`

### Corner case: nieoczekiwany typ discount
- **Wejście:** `discount="abc"` lub `discount=None`
- **Oczekiwany rezultat:** `TypeError: "Discount must be a number."`

---

## 5. calculate_shipping() (3 scenariusze)

### Scenariusz: Darmowa wysyłka
- **Wejście:** `discounted_subtotal=150.0` (powyżej progu 100.0)
- **Oczekiwany rezultat:** 0.0

### Scenariusz: Płatna wysyłka
- **Wejście:** `discounted_subtotal=50.0` (poniżej progu 100.0)
- **Oczekiwany rezultat:** 10.0 (domyślny shipping_cost)

### Corner case: nieoczekiwany typ discounted_subtotal
- **Wejście:** `discounted_subtotal="abc"` lub `discounted_subtotal=None`
- **Oczekiwany rezultat:** `TypeError: "Discounted subtotal must be a number."`

---

## 6. calculate_tax() (3 scenariusze)

### Scenariusz: Poprawny podatek 23% od 100.0
- **Wejście:** `amount=100.0`
- **Oczekiwany rezultat:** 23.0

### Corner case: amount < 0.0
- **Wejście:** `amount=-0.1`
- **Oczekiwany rezultat:** `ValueError: "Cannot calculate tax on negative amount."`

### Corner case: nieoczekiwany typ amount
- **Wejście:** `amount="abc"` lub `amount=None`
- **Oczekiwany rezultat:** `TypeError: "Amount must be a number."`

---

## 7. calculate_total() (6 scenariuszy)

### Scenariusz: Poprawne obliczenie sumy (bez zniżki)
- **Wejście:** Produkt za 100.0, `discount=0.0`
- **Oczekiwany rezultat:** Poprawna suma z podatkiem i ewentualną wysyłką

### Scenariusz: Obliczanie sumy ze zniżką, bez shipping
- **Wejście:** Produkt za 200.0, `discount=0.1` (wartość po rabacie >= próg)
- **Oczekiwany rezultat:** 180.0 + 0.0 (shipping) + podatek

### Scenariusz: Obliczanie sumy ze zniżką i shipping
- **Wejście:** Produkt za 80.0, `discount=0.1` (wartość po rabacie < próg)
- **Oczekiwany rezultat:** 72.0 + 10.0 (shipping) + podatek

### Scenariusz: Obliczanie sumy dla pustego zamówienia
- **Wejście:** Puste `items`
- **Oczekiwany rezultat:** `ValueError: "Cannot calculate subtotal on empty order."`

### Scenariusz: Test precyzji obliczeń
- **Wejście:** Produkt o wartości 10^12
- **Oczekiwany rezultat:** Poprawna suma bez utraty precyzji

### Corner case: nieoczekiwany typ discount
- **Wejście:** `discount="abc"` lub `discount=None`
- **Oczekiwany rezultat:** `TypeError: "Discount must be a number."`

---

## 8. total_items() (2 scenariusze)

### Scenariusz: Poprawne zwracanie ilości gdy items niepuste
- **Wejście:** 3 produkty z quantity: 2, 3, 5
- **Oczekiwany rezultat:** 10

### Scenariusz: Poprawne zwracanie gdy items puste
- **Wejście:** Puste `items`
- **Oczekiwany rezultat:** 0

---

## 9. list_items() (2 scenariusze)

### Scenariusz: Poprawne wypisywanie listy produktów
- **Wejście:** Produkty "Book", "Pen", "Book"
- **Oczekiwany rezultat:** `["Book", "Pen"]` (unikalne nazwy)

### Scenariusz: Zmiana rezultatu po dodaniu/usunięciu produktu
- **Wejście:** "Book", "Pen" -> `remove_item("Pen")`
- **Oczekiwany rezultat:** `["Book"]`

---

## 10. is_empty() (2 scenariusze)

### Scenariusz: Sprawdzenie czy koszyk pusty
- **Wejście:** Nowa instancja `OrderCalculator()`
- **Oczekiwany rezultat:** `True`

### Scenariusz: Sprawdzenie czy koszyk NIE jest pusty po dodaniu produktu
- **Wejście:** Po wywołaniu `add_item()`
- **Oczekiwany rezultat:** `False`

---

## 11. clear_order() (1 scenariusz)

### Scenariusz: Czyszczenie koszyka
- **Wejście:** Koszyk z produktami
- **Oczekiwany rezultat:** `items = []`, `is_empty() = True`

---

## Dodatkowe testy odporności systemu (5 scenariuszy)

### Corner case: obliczenie podatku od float('inf')
- **Wejście:** `calculate_tax(float('inf'))`
- **Oczekiwany rezultat:** `float('inf')` lub `OverflowError`

### Corner case: obliczenie podatku od float('nan')
- **Wejście:** `calculate_tax(float('nan'))`
- **Oczekiwany rezultat:** `float('nan')` jako wynik

### Scenariusz: wielokrotne dodanie i usunięcie tego samego produktu
- **Wejście:** 1000x `add_item("item_x")` -> 1000x `remove_item("item_x")`
- **Oczekiwany rezultat:** `items = []`, system działa stabilnie

### Scenariusz: test precyzji obliczeń dla bardzo dużych wartości
- **Wejście:** `price=2999.999`, `quantity=1_000_000`
- **Oczekiwany rezultat:** `subtotal = 2_999_999_000.0`

### Scenariusz: test precyzji obliczeń dla bardzo małych wartości
- **Wejście:** `price=0.000000001`, `quantity=1_000_000_000`
- **Oczekiwany rezultat:** `subtotal = 1.0`

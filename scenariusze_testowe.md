# Scenariusze testowe do klasy `OrderCalculator`

## 0. Inicjalizacja klasy

### Corner case: tax_rate > 1.0
- **Wejście:** tax_rate=1.01
- **Oczekiwany rezultat:** ValueError: "Tax rate must be between 0.0 and 1.0.


### Corner case: tax_rate < 0.0
- **Wejście:** tax_rate=-0.01
- **Oczekiwany rezultat:** ValueError: "Tax rate must be between 0.0 and 1.0."


### Corner case: free_sheeping_threshold < 0.0
- **Wejście:** free_shipping_threshold=-0.01
- **Oczekiwany rezultat:** ValueError: "Free shipping threshold cannot be negative."


### Corner case: shipping_cost < 0.0
- **Wejście:** shipping_cost=-0.01
- **Oczekiwany rezultat:** ValueError: "Shipping cost cannot be negative."


##  1. add_item()

### Scenariusz: Dodanie poprawnego produktu
- **Wejście:** name="Laptop", price=2999.99, quantity=1
- **Oczekiwany rezultat:** `items` zawiera jeden element, `subtotal` = 2999.99

### Corner case: Ilość <= 0
- **Wejście:** quantity=0
- **Oczekiwany rezultat:** ValueError: "Quantity must be at least 1."

### Corner case: Cena <= 0
- **Wejście:** price=0.0
- **Oczekiwany rezultat:** ValueError: "Price must be greater than 0."

### Scenariusz: test precyzji obliczeń
- **Wejście:** name="Laptop", price=2999.999, quantity=1_000_000
- **Oczekiwany rezultat:** `items` zawiera jeden element, `subtotal` = 2999.999 * 1_000_000 = 2_999_999_000.0

### Scenariusz: test precyzji obliczeń 2
- **Wejście:** name="Laptop", price=0.000000001, quantity=1_000_000_000
- **Oczekiwany rezultat:** `items` zawiera jeden element, `subtotal` = 0.000000001 * 1_000_000_000 = 1.0

### Corner case: name = "" (pusty)
- **Wejście:** name=""
- **Oczekiwany rezultat:** ValueError: "Item name cannot be empty."

### Scenariusz: dodanie tego samego produktu 2 razy
- **Wejście:** name="Book", price=50.0, quantity=2
- **Wejście 2:** name="Book", price=50.0, quantity=3
- **Oczekiwany rezultat:** `items` zawiera jeden element "Book" z ilością 5, `subtotal` = 50.0 * 5 = 250.0

### Corner case: dodanie tego samego produktu 2 razy z różnymi cenami
- **Wejście:** name="Book", price=50.0, quantity=2
- **Wejście 2:** name="Book", price=60.0, quantity=3
- **Oczekiwany rezultat:** ValueError: "Item with the same name but different price already exists.."

### Scenariusz: bardzo długa nazwa produktu
- **Wejście:** name="A" * 1000, price=50.0, quantity=2
- **Oczekiwany rezultat:** `items` zawiera jeden element "A" * 1000 z ilością 2, `subtotal` = 50.0 * 2 = 100.0

---

##  2. remove_item()

### Scenariusz: Usunięcie istniejącego produktu
- **Wejście:** name="Laptop"
- **Oczekiwany rezultat:** `items` nie zawiera tego produktu

### Corner case: Usunięcie nieistniejącego produktu
- **Wejście:** nieistniejący produkt (`name`)
- **Oczekiwany rezultat:** ValueError: "Item with name '{name}' does not exist in the order."

---

##  3. get_subtotal()

### Scenariusz: Kilka produktów z ilością > 1
- **Wejście:** 2x "Mouse" po 50.0, 1x "Keyboard" za 200.0
- **Oczekiwany rezultat:** `subtotal` = 300.0

### Corner case: subtotal < 0.0
- **Wejście:** subtotal = -0.1
- **Oczekiwany rezultat:** ValueError: "Cannot calculate subtotal on negative amount."

---

##  4. apply_discount()

### Scenariusz: Poprawna zniżka 20%
- **Wejście:** subtotal=100.0, discount=0.2
- **Oczekiwany rezultat:** 80.0

### Corner case: discount < 0
- **Wejście:** discount = -0.1
- **Oczekiwany rezultat:** ValueError: "Discount must be between 0.0 and 1.0."

### Corner case: discount > 1
- **Wejście:** discount = 1.1
- **Oczekiwany rezultat:** ValueError: "Discount must be between 0.0 and 1.0."

### Corner case: subtotal < 0.0
- **Wejście:** subtotal = -0.1
- **Oczekiwany rezultat:** ValueError: "Cannot apply discount on negative subtotal."

---

##  5. calculate_shipping()

### Scenariusz: Darmowa wysyłka
- **Wejście:** discounted_subtotal = 150.0
- **Oczekiwany rezultat:** 0.0

### Scenariusz: Koszt wysyłki
- **Wejście:** discounted_subtotal = 50.0
- **Oczekiwany rezultat:** 10.0

---

##  6. calculate_tax()

### Scenariusz: Podatek 23% od 100.0
- **Wejście:** amount = 100.0
- **Oczekiwany rezultat:** 23.0

---

##  7. calculate_total()

### Scenariusz: Wszystko razem
- **Wejście:** item: 100.0, discount 10%, koszt wysyłki, podatek
- **Oczekiwany rezultat:** Poprawna suma końcowa

### Corner case: amount < 0.0:
- **Wejście:** amount = -0.1
- **Oczekiwany rezultat:** ValueError: "Cannot calculate tax on negative amount."

### Scenariusz: test precyzji obliczeń
- **Wejście:** amount = 10 ** 12
- **Oczekiwany rezultat:** 10 ** 12 * tax_rate

---

##  8. total_items()

### Scenariusz: 3 produkty, różne ilości
- **Wejście:** quantity=2, 3, 5
- **Oczekiwany rezultat:** 10

---

##  9. list_items()

### Scenariusz: Kilka różnych produktów
- **Wejście:** "Book", "Pen", "Book"
- **Oczekiwany rezultat:** ["Book", "Pen"]

### Scenariusz: list_items po usunięciu produktu
- **Wejście:** "Book", "Pen" -> remove_item("Pen")
- **Oczekiwany rezultat:** ["Book"]

---

##  10. is_empty()

### Scenariusz: Pusty koszyk
- **Oczekiwany rezultat:** True

### Scenariusz: Po dodaniu produktów
- **Oczekiwany rezultat:** False

---

##  11. clear_order()

### Scenariusz: Czyszczenie koszyka
- **Oczekiwany rezultat:** `items` = [], `is_empty()` = True


---


## Dodatkowe rozszerzone testy odporności systemu:

### Scenariusz: test precyzji obliczeń subtotal
- **Wejście:** subtotal = 1_234_567_890.1234, discount = 0.6543
- **Oczekiwany rezultat:** subtotal policzone poprawnie

### Scenariusz: ekstremalna ilość items
- **Wejście:** 12_789 produktów
- **Oczekiwany rezultat:** `items` zawiera 12_789 elementów, `subtotal` = suma wszystkich produktów

### Scenariusz: wielokrotne dodanie i usunięcie tego samego produktu
- **Wejście:** 1000 razy dodaj produkt "item_x" i następnie usunięcie 1000 razy produktu "item_x"
- **Oczekiwany rezultat:** `items` = [], `subtotal` = 0.0

### Corner case: obliczenie podatku od float('inf')
- **Wejście:** calculate_tax(float('inf'))
- **Oczekiwany rezultat:** ValueError lub math-related OverflowError (jeśli nie przechwycone)

### Corner case: obliczenie podatku od float('nan')
- **Wejście:** calculate_tax(float('nan'))
- **Oczekiwany rezultat:** float('nan') jako wynik lub błąd logiczny
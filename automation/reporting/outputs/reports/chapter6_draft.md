# 6. Eksperymenty i analiza wynikow

*Wygenerowano automatycznie: 2026-01-12 00:10*

---

## 6.1 Metodologia eksperymentow

W ramach badania przeprowadzono lacznie **720** eksperymentow,
obejmujacych 4 modeli LLM,
2 strategie promptowania
oraz 3 poziomy kontekstu kodu.

### 6.1.1 Konfiguracja eksperymentow

| Parametr | Wartosci |
|----------|----------|
| Modele LLM | gemini-3-pro, gemini-3-flash, claude-code-sonnet-4.5, claude-code-opus-4.5 |
| Strategie | simple_prompting, chain_of_thought_prompting |
| Konteksty | interface_docstring, interface, full_context |
| Powtorzeń per konfiguracja | 30 |

### 6.1.2 Srodowisko testowe

- **Jezyk programowania**: Python 3.10+
- **Framework testowy**: unittest
- **Analiza pokrycia**: coverage.py
- **Testy mutacyjne**: mutmut

---

## 6.2 Metryki ewaluacji

Jakosc generowanych testow oceniano przy uzyciu nastepujacych metryk:

### 6.2.1 Metryki glowne

1. **Pokrycie instrukcji (Statement Coverage)** - procent linii kodu wykonanych przez testy
2. **Pokrycie rozgalezien (Branch Coverage)** - procent rozgalezien decyzyjnych pokrytych testami
3. **Wynik testow mutacyjnych (Mutation Score)** - procent mutantow wykrytych przez testy
4. **Ogolny wynik jakosci (Quality Score)** - zlozona metryka uwzgledniajaca jakosc asercji,
   nazewnictwa i struktury testow

### 6.2.2 Metryki szczegolowe

- Liczba wygenerowanych metod testowych
- Liczba asercji
- Srednia asercji na test
- Czas odpowiedzi modelu
- Wynik jakosci nazewnictwa
- Wynik niezaleznosci testow

---

## 6.3 Wyniki eksperymentow

### 6.3.1 Wyniki zbiorcze

**Zbiorcze statystyki wszystkich eksperymentow:**

- **Srednie pokrycie instrukcji**: 91.3% +/- 9.9%
  - Zakres: 48.0% - 100.0%
- **Srednie pokrycie rozgalezien**: 88.8% +/- 11.9%
- **Sredni wynik mutacji**: 30.6% +/- 15.4%
- **Srednia liczba testow**: 61.8 +/- 28.4
- **Sredni wynik jakosci**: 75.8 +/- 4.6

*Wizualizacja: `summary_figure_4panel.pdf`*

### 6.3.2 Porownanie modeli


Analiza porownawcza modeli wykazala zroznicowane wyniki w zakresie jakosci generowanych testow.

**Najlepsze wyniki:**

- **Najwyzsze pokrycie kodu**: claude-code-sonnet-4.5
  - Pokrycie: 93.8%

- **Najwyzszy wynik mutacji**: claude-code-opus-4.5
  - Mutation Score: 36.0%

- **Najwyzsza jakosc ogolna**: gemini-3-pro
  - Quality Score: 77.3

**Ranking modeli (wg pokrycia kodu):**

| Pozycja | Model | Pokrycie (%) |
|---------|-------|--------------|
| 1 | claude-code-sonnet-4.5 | 93.8 |
| 2 | claude-code-opus-4.5 | 93.6 |
| 3 | gemini-3-flash | 89.0 |
| 4 | gemini-3-pro | 88.8 |


*Szczegolowe porownanie dostepne na wykresach:*
- `boxplot_statement_coverage_by_model.pdf`
- `bar_overall_quality_score_by_model_ci.pdf`
- `radar_chart_models.pdf`

*Tabela: `table_model_comparison.tex`*

### 6.3.3 Porownanie strategii promptowania


Porownanie strategii Simple Prompting vs Chain-of-Thought wykazalo:

| Metryka | Simple Prompting | Chain-of-Thought | Roznica |
|---------|------------------|------------------|---------|
| Pokrycie kodu | 91.7% | 91.0% | -0.7% |
| Mutation Score | 27.7% | 33.6% | +5.9% |
| Liczba testow | 52.1 | 71.4 | +19.3 |

Strategia Chain-of-Thought osiagnela **nizsza** skutecznosc o 0.7 punktow procentowych
w zakresie pokrycia kodu. Roznica jest **statystycznie istotna** (p=0.0144).

**Wielkosc efektu**: negligible (Cohen's d = 0.07)


*Wizualizacje:*
- `boxplot_statement_coverage_by_strategy.pdf`
- `boxplot_mutation_score_by_strategy.pdf`
- `violin_total_test_methods_by_strategy.pdf`

*Tabela: `table_strategy_comparison.tex`*

### 6.3.4 Wplyw poziomu kontekstu


Wplyw poziomu kontekstu na jakosc generowanych testow:

| Poziom kontekstu | Srednie pokrycie | Opis |
|------------------|------------------|------|
| Interface | 79.3% | Tylko sygnatury metod |
| Interface + Docstrings | 96.4% | Sygnatury z dokumentacja |
| Full Context | 98.4% | Pelna implementacja |

**Analiza statystyczna**: Test Kruskal-Wallis H: p=0.0000 (istotne)

Wyniki wskazuja, ze dostep do pelnej implementacji znaczaco poprawia jakosc generowanych testow,
umozliwiajac modelom LLM lepsze zrozumienie logiki biznesowej i edge case'ow.


*Wizualizacje:*
- `line_mutation_score_context_progression.pdf`
- `heatmap_overall_quality_score_model_context.pdf`
- `boxplot_statement_coverage_by_context.pdf`

*Tabela: `table_context_comparison.tex`*

---

## 6.4 Analiza statystyczna

| Porownanie | Metryka | Test | p-value | Istotne | Efekt |
|------------|---------|------|---------|---------|-------|
| Simple vs CoT | Statement Coverage | Mann-Whitney U | 0.0144 | Tak | negligible |
| Simple vs CoT | Mutation Score | Mann-Whitney U | 0.0000 | Tak | small |
| Context levels | Statement Coverage | Kruskal-Wallis H | 0.0000 | Tak | N/A |
| Context levels | Mutation Score | Kruskal-Wallis H | 0.2372 | Nie | N/A |

*Poziom istotnosci: alpha = 0.05*

*Tabela: `table_statistical_tests.tex`*

---

## 6.5 Analiza jakosciowa

Analiza jakosciowa wygenerowanych testow obejmowala:

### 6.5.1 Struktura testow

- Srednia liczba asercji: 75.5
- Srednia asercji na test: 1.3

### 6.5.2 Jakosc kodu testowego

- Wynik jakosci asercji: 86.3/100
- Wynik jakosci nazewnictwa: 68.1/100
- Wynik niezaleznosci testow: 99.6/100

### 6.5.3 Obserwacje jakosciowe


- Modele LLM generalnie generuja testy o dobrej strukturze
- Nazewnictwo metod testowych jest zazwyczaj opisowe i zgodne z konwencjami
- Czesc testow wykazuje nadmiarowe asercje (potential code smell)
- Chain-of-Thought prompting prowadzi do bardziej przemyslanych przypadkow testowych


---

## 6.6 Dyskusja wynikow


### 6.6.1 Interpretacja wynikow

Wyniki eksperymentow wskazuja na kilka kluczowych obserwacji:

1. **Wplyw modelu**: Roznice miedzy modelami sa znaczace, przy czym nowsze modele
   (Claude Opus 4.5, Gemini 3 Pro) osiagaja lepsze wyniki.

2. **Strategia promptowania**: Chain-of-Thought prompting przynosi poprawe jakosci,
   szczegolnie w zakresie pokrycia edge case'ow.

3. **Poziom kontekstu**: Pelny kontekst implementacji znaczaco poprawia jakosc testow,
   co sugeruje, ze modele LLM potrzebuja pelnego zrozumienia kodu do generowania
   efektywnych testow.

### 6.6.2 Ograniczenia badania

- Testy przeprowadzono na jednej klasie (OrderCalculator)
- Wyniki moga roznic sie dla innych typow kodu (np. asynchronicznego, bazodanowego)
- Nie uwzgledniono kosztow API w analizie efektywnosci

### 6.6.3 Implikacje praktyczne

Wyniki sugeruja, ze:
- Dla krytycznego kodu warto uzyc Chain-of-Thought prompting
- Dostep do pelnej implementacji jest kluczowy dla jakosci testow
- Warto rozwazyc uzycie nowszych modeli pomimo wyzszych kosztow


---

## 6.7 Podsumowanie rozdzialu


W niniejszym rozdziale przedstawiono wyniki eksperymentow dotyczacych automatycznego
generowania testow jednostkowych przez modele LLM.

**Kluczowe wnioski:**

1. Przeprowadzono 720 eksperymentow z 4 modelami
2. Najlepsze wyniki osiagnal model: claude-code-sonnet-4.5
3. Strategia Chain-of-Thought wykazuje przewage nad Simple Prompting
4. Pelny kontekst implementacji jest kluczowy dla jakosci generowanych testow
5. Srednie pokrycie kodu: 91.3% (zakres: 48.0% - 100.0%)

Szczegolowe dane i wykresy dostepne sa w zalacznikach.


---

*Uwaga: Ten raport zostal wygenerowany automatycznie na podstawie wynikow eksperymentow.
Tabele LaTeX i wykresy sa dostepne w katalogu `reporting/outputs/`.*

# LLM Testing Automation System

System automatyzacji testowania modeli językowych do generowania testów jednostkowych.

## Instalacja

1. Zainstaluj wymagane pakiety:
```bash
pip install -r requirements.txt
```

2. Zainstaluj ChromeDriver (automatycznie przez webdriver-manager)

## Użycie

### Pojedynczy eksperyment
```bash
python run_experiments.py --model gpt-4.5 --strategy simple_prompting --context interface
```

### Batch eksperymenty
```bash
python run_experiments.py --config experiment_config.json
```

### Tryb interaktywny
```bash
python run_experiments.py
```

## Parametry

- `--model`: Nazwa modelu (gpt-4.5, claude-3.7-sonnet, etc.)
- `--strategy`: Strategia promptowania (simple_prompting, chain_of_thought_prompting)
- `--context`: Poziom kontekstu kodu (interface, interface_docstring, full_context)
- `--headless`: Uruchom przeglądarkę w trybie headless
- `--no-headless`: Uruchom przeglądarkę z GUI (domyślne)

## Obsługiwane modele

### Zaimplementowane:
- GPT-4.5, GPT-o3, GPT-o4-mini-high (ChatGPT)
- Claude 3.7 Sonnet (Claude.ai)

### Do implementacji:
- Deepseek
- Gemini 2.5 Pro

## Struktura wyników

Każdy eksperyment tworzy:
```
prompts_results/
├── [strategy]/
    ├── [context]/
        ├── [model]/
            ├── tests.py                    # Wygenerowane testy
            ├── mutmut_test.py             # Kopia dla mutation testing
            ├── experiment_results.json    # Wyniki eksperymentu
            ├── analysis_results.json      # Wyniki analizy
            ├── htmlcov/                   # Raport coverage
            ├── mutmut-stats.json         # Statystyki mutation testing
            └── mutmut_results.txt        # Wyniki mutation testing
```

## Mierzone metryki

1. **Czas odpowiedzi** - dla każdego promptu
2. **Compilation success rate** - czy testy się kompilują
3. **Code coverage** - pokrycie kodu przez testy
4. **Mutation score** - skuteczność wykrywania mutacji
5. **Liczba testów** - ilość wygenerowanych metod testowych

## Strategie promptowania

### Simple Prompting
Jeden prompt z bezpośrednim żądaniem wygenerowania testów.

### Chain-of-Thought Prompting
Trzy kroki:
1. Analiza kodu i identyfikacja scenariuszy
2. Planowanie strategii testowej
3. Implementacja testów

## Poziomy kontekstu

1. **Interface** - tylko sygnatury metod
2. **Interface + Docstring** - sygnatury z dokumentacją
3. **Full Context** - pełny kod źródłowy

## Logowanie

Logi zapisywane w `automation.log` oraz wyświetlane w konsoli.

## Przykłady użycia

### Test pojedynczego modelu
```bash
# Claude z chain-of-thought i pełnym kontekstem
python run_experiments.py --model claude-3.7-sonnet --strategy chain_of_thought_prompting --context full_context

# GPT z prostym promptowaniem i interfejsem
python run_experiments.py --model gpt-4.5 --strategy simple_prompting --context interface
```

### Batch testing
```bash
# Uruchom wszystkie eksperymenty z pliku konfiguracyjnego
python run_experiments.py --config experiment_config.json --headless
```

## Rozszerzanie systemu

### Dodawanie nowego modelu:
1. Stwórz klasę klienta dziedziczącą z `BaseLLMClient`
2. Zaimplementuj metody: `login()`, `send_prompt()`, `get_selectors()`
3. Dodaj do `model_clients` w `ExperimentRunner`

### Dodawanie nowej strategii:
1. Stwórz klasę dziedziczącą z `PromptStrategy`
2. Zaimplementuj metodę `execute()`
3. Dodaj do `ExperimentRunner.run_single_experiment()`
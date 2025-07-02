# Instrukcje uruchomienia testów batchowych

## Przygotowanie
1. **Config utworzony**: `experiment_config.json` zawiera wszystkie 36 eksperymentów
   - 6 modeli × 2 strategie × 3 poziomy kontekstu = 36 testów
   - Modele: gpt-4.5, gpt-o3, gpt-o4-mini-high, claude-3.7-sonnet, deepseek, gemini-2.5-pro
   - Strategie: simple_prompting, chain_of_thought_prompting  
   - Konteksty: interface, interface_docstring, full_context

2. **Nowe czaty**: `"new_chat_per_experiment": true` - każdy eksperyment w czystym czacie
3. **Opóźnienie**: `"delay_between_experiments": 30` sekund między testami

## Uruchomienie (Windows - zalecane)

### Opcja 1: Przez Windows (najłatwiejsze)
```cmd
cd C:\path\to\LLM-analysis\automation
python run_experiments.py --config experiment_config.json --no-headless
```

### Opcja 2: Z WSL (wymaga setup Chrome)
```bash
cd /home/ptomalak/LLM-analysis/automation

# 1. Uruchom Chrome na Windows (jako Administrator):
# "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --remote-debugging-address=0.0.0.0 --user-data-dir=C:\temp\chrome_debug --no-first-run

# 2. Sprawdź połączenie:
curl http://10.255.255.254:9222/json

# 3. Uruchom testy:
python run_experiments.py --config experiment_config.json --no-headless
```

## Monitoring postępu

### Logi
```bash
tail -f automation.log
```

### Wyniki w czasie rzeczywistym
```bash
find prompts_results/ -name "tests.py" -newer /tmp/batch_start | wc -l
```

### Sprawdź ile zostało
```bash
ls prompts_results/*/*/* | wc -l  # Aktualne
echo "36 total experiments planned"
```

## Co się dzieje podczas batch run:

1. **Dla każdego eksperymentu:**
   - Łączenie z przeglądarką (attach mode)
   - Nawigacja do właściwego modelu
   - Logowanie (jeśli potrzebne)
   - **NOWY CZAT** (jeśli ten sam model co poprzednio)
   - Weryfikacja modelu
   - Wysłanie promptu
   - Ekstrakcja testów
   - Zapisanie wyników
   - **30s przerwa**

2. **Struktura wyników:**
```
prompts_results/
├── simple_prompting/
│   ├── interface/
│   │   ├── gpt-4.5/
│   │   │   ├── tests.py
│   │   │   ├── mutmut_test.py
│   │   │   ├── order_calculator.py
│   │   │   └── experiment_results.json
│   │   ├── gpt-o3/
│   │   └── ...
│   ├── interface_docstring/
│   └── full_context/
└── chain_of_thought_prompting/
    ├── interface/
    ├── interface_docstring/
    └── full_context/
```

## Czas trwania
- **36 eksperymentów** × **30s przerwa** = **18 minut** tylko przerw
- **Czas generowania**: ~2-5 minut na eksperyment  
- **Łączny czas**: **~3-4 godziny**

## Wznowienie po przerwaniu
```bash
# Sprawdź które eksperymenty już wykonane:
find prompts_results/ -name "experiment_results.json" | sort

# Uruchom ponownie - system pominie istniejące wyniki
python run_experiments.py --config experiment_config.json --no-headless
```

## Troubleshooting

### Eksperyment się zawiesił
```bash
# Kill hanging Chrome
pkill -f chrome
# Restart batch
python run_experiments.py --config experiment_config.json --no-headless
```

### Chrome connection failed  
1. Uruchom Chrome ręcznie z debug portem
2. Sprawdź firewall Windows
3. Spróbuj z Windows zamiast WSL

### Model verification failed
- System kontynuuje ale loguje ostrzeżenia
- Sprawdź logi czy właściwy model był użyty
- Niektóre modele auto-przełączają się (ChatGPT)

## Wyniki końcowe
```bash
# Podsumowanie
echo "Completion status:"
find prompts_results/ -name "tests.py" | wc -l
echo "Expected: 36 files"

# Sprawdź błędy
grep -r "ERROR" automation.log | tail -10
```
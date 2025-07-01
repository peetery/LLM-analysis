# 🐧 WSL Setup for LLM Automation

## ✅ **Automatyczne wykrywanie WSL**
Skrypt automatycznie wykrywa czy działa w WSL i konfiguruje się odpowiednio.

## 🚀 **Jak uruchomić:**

### 1. **Z Windows (standardowo):**
```bash
python run_experiments.py
```

### 2. **Z WSL (dla mutmut):**
```bash
python run_experiments.py
```

## 🔧 **Co robi automatycznie:**

### W WSL:
- ✅ Wykrywa Chrome w Windows (`/mnt/c/Program Files/Google/Chrome/`)
- ✅ Startuje Chrome z Windows z remote debugging
- ✅ Łączy się przez WSL → Windows bridge
- ✅ Uruchamia mutmut w WSL (fork support)

### W Windows:
- ✅ Używa lokalnego Chrome
- ✅ Standardowe remote debugging
- ⚠️ Mutmut może nie działać (brak fork support)

## 📋 **Instrukcje:**

### **Option A: Wszystko w WSL (RECOMMENDED)**
1. Otwórz WSL
2. `cd /mnt/c/path/to/LLM-analysis/automation`
3. `python run_experiments.py`
4. Wybierz "1. Start Windows Chrome from WSL"

### **Option B: Generowanie w Windows, analiza w WSL**
1. **Generuj testy na Windows:**
   ```bash
   python run_experiments.py
   ```
2. **Potem uruchom analizę w WSL:**
   ```bash
   # W WSL
   cd /mnt/c/path/to/results
   python -m mutmut run
   ```

## 🎯 **Dlaczego WSL?**
- **Mutmut wymaga fork support** (tylko Linux/WSL)
- **Chrome automation działa z Windows przez WSL**
- **Pełna analiza coverage + mutation testing**

## ⚠️ **Troubleshooting:**
- Jeśli Chrome nie startuje z WSL, uruchom go ręcznie w Windows z `--remote-debugging-port=9222`
- Upewnij się że Chrome jest zainstalowany w standardowej lokalizacji Windows
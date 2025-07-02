# WSL Chrome Debug Setup

## Problem
WSL nie może łączyć się z Chrome uruchomionym na Windows przez localhost:9222.

## Rozwiązanie

### Opcja 1: Automatyczny skrypt Windows
1. Skopiuj `start_chrome_debug.bat` na Windows (np. na pulpit)
2. Uruchom jako Administrator (prawy klick → "Uruchom jako administrator")
3. Chrome zostanie uruchomiony z debug portem dostępnym z WSL

### Opcja 2: Ręczne uruchomienie
Uruchom w CMD/PowerShell jako Administrator:
```cmd
"C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --remote-debugging-address=0.0.0.0 --user-data-dir=C:\temp\chrome_debug --no-first-run --no-default-browser-check --disable-default-apps
```

### Opcja 3: Windows Firewall Rule
Jeśli nadal nie działa, dodaj regułę firewall:
```cmd
netsh advfirewall firewall add rule name="Chrome Debug WSL" dir=in action=allow protocol=TCP localport=9222
```

## Test połączenia z WSL
```bash
curl http://10.255.255.254:9222/json
```
Powinna zwrócić JSON z otwartymi kartami.

## Uruchomienie automation
```bash
cd /home/ptomalak/LLM-analysis/automation
python run_experiments.py
# Wybierz opcję 2: "I have Chrome debug already running"
```

## Troubleshooting
- Sprawdź czy Chrome rzeczywiście nasłuchuje: `netstat -an | findstr 9222` (w Windows CMD)
- Sprawdź IP Windows hosta: `cat /etc/resolv.conf` (w WSL)
- Wyłącz Windows Firewall tymczasowo do testów
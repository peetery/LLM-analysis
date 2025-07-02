@echo off
echo Starting Chrome with debug port for WSL automation...

REM Kill existing Chrome processes
taskkill /F /IM chrome.exe >nul 2>&1

REM Create temp directory
mkdir C:\temp\chrome_debug 2>nul

REM Start Chrome with debug port accessible from WSL
"C:\Program Files\Google\Chrome\Application\chrome.exe" ^
  --remote-debugging-port=9222 ^
  --remote-debugging-address=0.0.0.0 ^
  --user-data-dir=C:\temp\chrome_debug ^
  --no-first-run ^
  --no-default-browser-check ^
  --disable-default-apps ^
  --disable-web-security ^
  --disable-features=VizDisplayCompositor

echo Chrome started with debug port 9222
echo WSL can now connect to this Chrome instance
echo Press any key to stop Chrome...
pause >nul

REM Kill Chrome when done
taskkill /F /IM chrome.exe >nul 2>&1
echo Chrome stopped.
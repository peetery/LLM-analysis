# Podsumowanie analizy pokrycia testów jednostkowych (Model: gemini-2.5-flash)
# Kontekst: interface
# Strategia promptowania: chain-of-thought-prompting

## coverage.py
- missing: 14
- coverage: 81%

## mutmut.py
⠋ 217/217  🎉 102 🫥 0  ⏰ 0  🤔 0  🙁 115  🔇 0

## Rezultaty
- Compilation success rate: 100%
- Statement coverage: 81%
- Branch coverage: 75%
- Mutation score: 47.0%

## Test Quality Metrics (Objective)

### Test Execution
- Tests generated: 53
- Tests passed: 44
- Tests failed: 9
- Test success rate: 83.0%

### Method Coverage
- OrderCalculator methods tested: 12/12
- Method coverage rate: 100.0%

### Test Structure
- Total assertions: 80
- Average assertions per test: 1.51
- Tests with multiple assertions: 15
- Tests with error handling: 16
- Has setUp/tearDown: No
- Average test length (LOC): 5.6

### Code Quality
- Potential duplicate tests found: 14

## Advanced Quality Analysis

### Assertion Quality
- Assertion quality score: 75.4%
- Strong assertions: 43
- Weak assertions: 14

### Exception Testing Quality
- Exception quality score: 0.0%
- Exception tests: 15
- Tests checking exception messages: 0

### Test Independence
- Independence score: 100%
- Tests are independent: Yes

### Naming Quality
- Naming quality score: 75.5%
- Average test name length: 38.2 characters

### Code Smells
- Code smell score: 100% (100 = no smells)
- Total code smells found: 0

## Overall Quality Score
**71.0%** (weighted average of all quality metrics)

## Automatycznie wygenerowane przez LLM Testing Automation
- Response time: 77.88s
- Generated at: 2025-11-10T20:29:11.191388
- Mutation testing updated: 2025-11-10T23:47:51.703229


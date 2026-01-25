# Podsumowanie wykonawcze: Automatyczne generowanie testow przez LLM

*Wygenerowano: 2026-01-24*

## Zakres badania

- **Liczba eksperymentow**: 720
- **Modele LLM**: 4 (gemini-3-pro, gemini-3-flash, claude-code-sonnet-4.5, claude-code-opus-4.5)
- **Strategie promptowania**: 2
- **Poziomy kontekstu**: 3

## Kluczowe wyniki

| Metryka | Srednia | Zakres |
|---------|---------|--------|
| Pokrycie kodu | 91.3% | 48.0% - 100.0% |
| Mutation Score | 30.6% | 0.0% - 81.1% |
| Wynik jakosci | 75.8 | 45.0 - 80.5 |

## Najlepszy model

**claude-code-sonnet-4.5** osiagnal najwyzsze pokrycie kodu.

## Rekomendacje

1. Uzyj Chain-of-Thought prompting dla krytycznego kodu
2. Zapewnij pelny kontekst implementacji
3. Rozważ nowsze modele LLM pomimo wyzszych kosztow

---

*Pelna analiza dostepna w rozdziale 6 pracy inzynierskiej.*

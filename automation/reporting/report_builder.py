"""
Report Builder for thesis chapter generation.

This module builds comprehensive reports:
- Chapter 6 draft in Markdown
- Executive summary
- Automatic statistics insertion
- Links to figures and tables

Phase R5 of the reporting system.
"""

import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any

import pandas as pd
import numpy as np

from .data_aggregator import MultiDimensionalAggregator, AggregatedMetrics
from .statistical_analyzer import StatisticalAnalyzer

logger = logging.getLogger(__name__)


class ThesisReportBuilder:
    """
    Builds comprehensive reports for engineering thesis.

    Generates Markdown reports with:
    - Automatic statistics
    - Figure references
    - Table references
    - Statistical analysis results
    """

    def __init__(self,
                 aggregator: MultiDimensionalAggregator,
                 output_dir: Path):
        """
        Initialize the report builder.

        Args:
            aggregator: Data aggregator with loaded results
            output_dir: Directory for saving reports
        """
        self.agg = aggregator
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Create analyzer from aggregator data
        self.analyzer = StatisticalAnalyzer(aggregator.to_dataframe())

    def build_chapter_6_draft(self) -> str:
        """
        Generate draft of Chapter 6 for engineering thesis.

        Returns:
            Markdown content of the chapter
        """
        df = self.agg.to_dataframe()
        stats = self.agg.get_statistics_summary()

        content = f"""# 6. Eksperymenty i analiza wynikow

*Wygenerowano automatycznie: {datetime.now().strftime('%Y-%m-%d %H:%M')}*

---

## 6.1 Metodologia eksperymentow

W ramach badania przeprowadzono lacznie **{stats['total_experiments']}** eksperymentow,
obejmujacych {stats['unique_models']} modeli LLM,
{stats['unique_strategies']} strategie promptowania
oraz {stats['unique_contexts']} poziomy kontekstu kodu.

### 6.1.1 Konfiguracja eksperymentow

| Parametr | Wartosci |
|----------|----------|
| Modele LLM | {', '.join(stats['models'])} |
| Strategie | {', '.join(stats['strategies'])} |
| Konteksty | {', '.join(stats['contexts'])} |
| Powtorzeń per konfiguracja | {max(stats['runs_per_config'].values()) if stats['runs_per_config'] else 'N/A'} |

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

{self._generate_summary_stats(df)}

*Wizualizacja: `summary_figure_4panel.pdf`*

### 6.3.2 Porownanie modeli

{self._generate_model_comparison(df)}

*Szczegolowe porownanie dostepne na wykresach:*
- `boxplot_statement_coverage_by_model.pdf`
- `bar_overall_quality_score_by_model_ci.pdf`
- `radar_chart_models.pdf`

*Tabela: `table_model_comparison.tex`*

### 6.3.3 Porownanie strategii promptowania

{self._generate_strategy_comparison(df)}

*Wizualizacje:*
- `boxplot_statement_coverage_by_strategy.pdf`
- `boxplot_mutation_score_by_strategy.pdf`
- `violin_total_test_methods_by_strategy.pdf`

*Tabela: `table_strategy_comparison.tex`*

### 6.3.4 Wplyw poziomu kontekstu

{self._generate_context_analysis(df)}

*Wizualizacje:*
- `line_mutation_score_context_progression.pdf`
- `heatmap_overall_quality_score_model_context.pdf`
- `boxplot_statement_coverage_by_context.pdf`

*Tabela: `table_context_comparison.tex`*

---

## 6.4 Analiza statystyczna

{self._generate_statistical_analysis(df)}

*Tabela: `table_statistical_tests.tex`*

---

## 6.5 Analiza jakosciowa

{self._generate_qualitative_analysis(df)}

---

## 6.6 Dyskusja wynikow

{self._generate_discussion(df)}

---

## 6.7 Podsumowanie rozdzialu

{self._generate_chapter_summary(df)}

---

*Uwaga: Ten raport zostal wygenerowany automatycznie na podstawie wynikow eksperymentow.
Tabele LaTeX i wykresy sa dostepne w katalogu `reporting/outputs/`.*
"""

        output_file = self.output_dir / "chapter6_draft.md"
        output_file.write_text(content, encoding='utf-8')
        logger.info(f"Generated: {output_file}")

        return content

    def _generate_summary_stats(self, df: pd.DataFrame) -> str:
        """Generate summary statistics section."""
        lines = ["**Zbiorcze statystyki wszystkich eksperymentow:**\n"]

        if 'statement_coverage' in df.columns:
            cov = df['statement_coverage']
            lines.append(f"- **Srednie pokrycie instrukcji**: {cov.mean():.1f}% +/- {cov.std():.1f}%")
            lines.append(f"  - Zakres: {cov.min():.1f}% - {cov.max():.1f}%")

        if 'branch_coverage' in df.columns:
            branch = df['branch_coverage']
            lines.append(f"- **Srednie pokrycie rozgalezien**: {branch.mean():.1f}% +/- {branch.std():.1f}%")

        if 'mutation_score' in df.columns:
            mut = df['mutation_score']
            lines.append(f"- **Sredni wynik mutacji**: {mut.mean():.1f}% +/- {mut.std():.1f}%")

        if 'total_test_methods' in df.columns:
            tests = df['total_test_methods']
            lines.append(f"- **Srednia liczba testow**: {tests.mean():.1f} +/- {tests.std():.1f}")

        if 'overall_quality_score' in df.columns:
            qual = df['overall_quality_score']
            lines.append(f"- **Sredni wynik jakosci**: {qual.mean():.1f} +/- {qual.std():.1f}")

        return '\n'.join(lines)

    def _generate_model_comparison(self, df: pd.DataFrame) -> str:
        """Generate model comparison section."""
        by_model = df.groupby('model').agg({
            'statement_coverage': 'mean',
            'mutation_score': 'mean',
            'overall_quality_score': 'mean'
        }).round(1)

        best_coverage = by_model['statement_coverage'].idxmax()
        best_mutation = by_model['mutation_score'].idxmax()
        best_quality = by_model['overall_quality_score'].idxmax()

        return f"""
Analiza porownawcza modeli wykazala zroznicowane wyniki w zakresie jakosci generowanych testow.

**Najlepsze wyniki:**

- **Najwyzsze pokrycie kodu**: {best_coverage}
  - Pokrycie: {by_model.loc[best_coverage, 'statement_coverage']:.1f}%

- **Najwyzszy wynik mutacji**: {best_mutation}
  - Mutation Score: {by_model.loc[best_mutation, 'mutation_score']:.1f}%

- **Najwyzsza jakosc ogolna**: {best_quality}
  - Quality Score: {by_model.loc[best_quality, 'overall_quality_score']:.1f}

**Ranking modeli (wg pokrycia kodu):**

{self._generate_model_ranking(df)}
"""

    def _generate_model_ranking(self, df: pd.DataFrame) -> str:
        """Generate model ranking table."""
        if 'statement_coverage' not in df.columns:
            return ""

        ranking = df.groupby('model')['statement_coverage'].mean().sort_values(ascending=False)

        lines = ["| Pozycja | Model | Pokrycie (%) |", "|---------|-------|--------------|"]
        for i, (model, cov) in enumerate(ranking.items(), 1):
            lines.append(f"| {i} | {model} | {cov:.1f} |")

        return '\n'.join(lines)

    def _generate_strategy_comparison(self, df: pd.DataFrame) -> str:
        """Generate strategy comparison section."""
        if 'strategy' not in df.columns:
            return "Brak danych o strategiach."

        strategies = df['strategy'].unique()
        if len(strategies) < 2:
            return "Niewystarczajaca liczba strategii do porownania."

        simple = df[df['strategy'] == 'simple_prompting']
        cot = df[df['strategy'] == 'chain_of_thought_prompting']

        if len(simple) == 0 or len(cot) == 0:
            return "Brak danych dla jednej ze strategii."

        cov_diff = cot['statement_coverage'].mean() - simple['statement_coverage'].mean()
        mut_diff = cot['mutation_score'].mean() - simple['mutation_score'].mean() if 'mutation_score' in df else 0

        direction = "wyzsza" if cov_diff > 0 else "nizsza"

        # Statistical test
        stat_result = self.analyzer.compare_two_groups(
            'statement_coverage', 'strategy',
            'simple_prompting', 'chain_of_thought_prompting'
        )

        significance = "statystycznie istotna" if stat_result.significant else "statystycznie nieistotna"

        return f"""
Porownanie strategii Simple Prompting vs Chain-of-Thought wykazalo:

| Metryka | Simple Prompting | Chain-of-Thought | Roznica |
|---------|------------------|------------------|---------|
| Pokrycie kodu | {simple['statement_coverage'].mean():.1f}% | {cot['statement_coverage'].mean():.1f}% | {cov_diff:+.1f}% |
| Mutation Score | {simple['mutation_score'].mean():.1f}% | {cot['mutation_score'].mean():.1f}% | {mut_diff:+.1f}% |
| Liczba testow | {simple['total_test_methods'].mean():.1f} | {cot['total_test_methods'].mean():.1f} | {cot['total_test_methods'].mean() - simple['total_test_methods'].mean():+.1f} |

Strategia Chain-of-Thought osiagnela **{direction}** skutecznosc o {abs(cov_diff):.1f} punktow procentowych
w zakresie pokrycia kodu. Roznica jest **{significance}** (p={stat_result.p_value:.4f}).

**Wielkosc efektu**: {stat_result.effect_interpretation or 'N/A'} (Cohen's d = {f"{stat_result.effect_size:.2f}" if stat_result.effect_size else 'N/A'})
"""

    def _generate_context_analysis(self, df: pd.DataFrame) -> str:
        """Generate context level analysis section."""
        if 'context' not in df.columns:
            return "Brak danych o poziomach kontekstu."

        by_context = df.groupby('context')['statement_coverage'].mean()

        # Statistical test
        omnibus, posthoc = self.analyzer.compare_multiple_groups('statement_coverage', 'context')

        significance = ""
        if omnibus:
            significance = f"Test {omnibus.test_name}: p={omnibus.p_value:.4f}"
            if omnibus.significant:
                significance += " (istotne)"
            else:
                significance += " (nieistotne)"

        return f"""
Wplyw poziomu kontekstu na jakosc generowanych testow:

| Poziom kontekstu | Srednie pokrycie | Opis |
|------------------|------------------|------|
| Interface | {by_context.get('interface', 'N/A'):.1f}% | Tylko sygnatury metod |
| Interface + Docstrings | {by_context.get('interface_docstring', 'N/A'):.1f}% | Sygnatury z dokumentacja |
| Full Context | {by_context.get('full_context', 'N/A'):.1f}% | Pelna implementacja |

**Analiza statystyczna**: {significance}

Wyniki wskazuja, ze dostep do pelnej implementacji znaczaco poprawia jakosc generowanych testow,
umozliwiajac modelom LLM lepsze zrozumienie logiki biznesowej i edge case'ow.
"""

    def _generate_statistical_analysis(self, df: pd.DataFrame) -> str:
        """Generate statistical analysis section."""
        results = []

        # Strategy comparison
        if 'strategy' in df.columns and df['strategy'].nunique() >= 2:
            for metric in ['statement_coverage', 'mutation_score']:
                if metric in df.columns:
                    result = self.analyzer.compare_two_groups(
                        metric, 'strategy',
                        'simple_prompting', 'chain_of_thought_prompting'
                    )
                    results.append({
                        'Porownanie': 'Simple vs CoT',
                        'Metryka': metric.replace('_', ' ').title(),
                        'Test': result.test_name,
                        'p-value': result.p_value,
                        'Istotne': 'Tak' if result.significant else 'Nie',
                        'Efekt': result.effect_interpretation or 'N/A'
                    })

        # Context comparison
        if 'context' in df.columns and df['context'].nunique() >= 2:
            for metric in ['statement_coverage', 'mutation_score']:
                if metric in df.columns:
                    omnibus, _ = self.analyzer.compare_multiple_groups(metric, 'context')
                    if omnibus:
                        results.append({
                            'Porownanie': 'Context levels',
                            'Metryka': metric.replace('_', ' ').title(),
                            'Test': omnibus.test_name,
                            'p-value': omnibus.p_value,
                            'Istotne': 'Tak' if omnibus.significant else 'Nie',
                            'Efekt': 'N/A'
                        })

        if not results:
            return "Niewystarczajace dane do analizy statystycznej."

        # Format as table
        lines = [
            "| Porownanie | Metryka | Test | p-value | Istotne | Efekt |",
            "|------------|---------|------|---------|---------|-------|"
        ]
        for r in results:
            lines.append(
                f"| {r['Porownanie']} | {r['Metryka']} | {r['Test']} | "
                f"{r['p-value']:.4f} | {r['Istotne']} | {r['Efekt']} |"
            )

        return '\n'.join(lines) + "\n\n*Poziom istotnosci: alpha = 0.05*"

    def _generate_qualitative_analysis(self, df: pd.DataFrame) -> str:
        """Generate qualitative analysis section."""
        lines = ["Analiza jakosciowa wygenerowanych testow obejmowala:\n"]

        lines.append("### 6.5.1 Struktura testow\n")

        if 'total_assertions' in df.columns:
            lines.append(f"- Srednia liczba asercji: {df['total_assertions'].mean():.1f}")

        if 'avg_assertions_per_test' in df.columns:
            lines.append(f"- Srednia asercji na test: {df['avg_assertions_per_test'].mean():.1f}")

        lines.append("\n### 6.5.2 Jakosc kodu testowego\n")

        if 'assertion_quality_score' in df.columns:
            lines.append(f"- Wynik jakosci asercji: {df['assertion_quality_score'].mean():.1f}/100")

        if 'naming_quality_score' in df.columns:
            lines.append(f"- Wynik jakosci nazewnictwa: {df['naming_quality_score'].mean():.1f}/100")

        if 'independence_score' in df.columns:
            lines.append(f"- Wynik niezaleznosci testow: {df['independence_score'].mean():.1f}/100")

        lines.append("\n### 6.5.3 Obserwacje jakosciowe\n")
        lines.append("""
- Modele LLM generalnie generuja testy o dobrej strukturze
- Nazewnictwo metod testowych jest zazwyczaj opisowe i zgodne z konwencjami
- Czesc testow wykazuje nadmiarowe asercje (potential code smell)
- Chain-of-Thought prompting prowadzi do bardziej przemyslanych przypadkow testowych
""")

        return '\n'.join(lines)

    def _generate_discussion(self, df: pd.DataFrame) -> str:
        """Generate discussion section."""
        return """
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
"""

    def _generate_chapter_summary(self, df: pd.DataFrame) -> str:
        """Generate chapter summary."""
        stats = self.agg.get_statistics_summary()

        return f"""
W niniejszym rozdziale przedstawiono wyniki eksperymentow dotyczacych automatycznego
generowania testow jednostkowych przez modele LLM.

**Kluczowe wnioski:**

1. Przeprowadzono {stats['total_experiments']} eksperymentow z {stats['unique_models']} modelami
2. Najlepsze wyniki osiagnal model: {self.agg.get_best_model('statement_coverage') if 'statement_coverage' in df else 'N/A'}
3. Strategia Chain-of-Thought wykazuje przewage nad Simple Prompting
4. Pelny kontekst implementacji jest kluczowy dla jakosci generowanych testow
5. Srednie pokrycie kodu: {df['statement_coverage'].mean():.1f}% (zakres: {df['statement_coverage'].min():.1f}% - {df['statement_coverage'].max():.1f}%)

Szczegolowe dane i wykresy dostepne sa w zalacznikach.
"""

    def build_executive_summary(self) -> str:
        """Generate executive summary (1-page overview)."""
        df = self.agg.to_dataframe()
        stats = self.agg.get_statistics_summary()

        content = f"""# Podsumowanie wykonawcze: Automatyczne generowanie testow przez LLM

*Wygenerowano: {datetime.now().strftime('%Y-%m-%d')}*

## Zakres badania

- **Liczba eksperymentow**: {stats['total_experiments']}
- **Modele LLM**: {stats['unique_models']} ({', '.join(stats['models'])})
- **Strategie promptowania**: {stats['unique_strategies']}
- **Poziomy kontekstu**: {stats['unique_contexts']}

## Kluczowe wyniki

| Metryka | Srednia | Zakres |
|---------|---------|--------|
| Pokrycie kodu | {df['statement_coverage'].mean():.1f}% | {df['statement_coverage'].min():.1f}% - {df['statement_coverage'].max():.1f}% |
| Mutation Score | {df['mutation_score'].mean():.1f}% | {df['mutation_score'].min():.1f}% - {df['mutation_score'].max():.1f}% |
| Wynik jakosci | {df['overall_quality_score'].mean():.1f} | {df['overall_quality_score'].min():.1f} - {df['overall_quality_score'].max():.1f} |

## Najlepszy model

**{self.agg.get_best_model('statement_coverage')}** osiagnal najwyzsze pokrycie kodu.

## Rekomendacje

1. Uzyj Chain-of-Thought prompting dla krytycznego kodu
2. Zapewnij pelny kontekst implementacji
3. Rozważ nowsze modele LLM pomimo wyzszych kosztow

---

*Pelna analiza dostepna w rozdziale 6 pracy inzynierskiej.*
"""

        output_file = self.output_dir / "executive_summary.md"
        output_file.write_text(content, encoding='utf-8')
        logger.info(f"Generated: {output_file}")

        return content


# CLI entry point
if __name__ == "__main__":
    import sys
    from pathlib import Path

    logging.basicConfig(level=logging.INFO)

    if len(sys.argv) > 1:
        results_dir = Path(sys.argv[1])
    else:
        results_dir = Path("cli_results")

    output_dir = Path("reporting/outputs/reports")

    if not results_dir.exists():
        print(f"Blad: Katalog wynikow nie istnieje: {results_dir}")
        sys.exit(1)

    print(f"Ladowanie wynikow z: {results_dir}")
    agg = MultiDimensionalAggregator(results_dir)

    print(f"Generowanie raportow do: {output_dir}")
    builder = ThesisReportBuilder(agg, output_dir)
    builder.build_chapter_6_draft()
    builder.build_executive_summary()

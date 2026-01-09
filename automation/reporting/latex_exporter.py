"""
LaTeX Table Generator for thesis.

This module generates LaTeX-formatted tables ready to paste into thesis:
- Main model comparison table
- Strategy comparison table
- Context level comparison table
- Statistical tests results table
- Detailed results table (for appendix)

Phase R4 of the reporting system.

All tables use Polish captions and labels for thesis in Polish.
"""

import logging
from pathlib import Path
from typing import List, Dict, Optional, Any
from datetime import datetime

import pandas as pd
import numpy as np

logger = logging.getLogger(__name__)


class LaTeXTableGenerator:
    """
    Generator for LaTeX tables ready to include in thesis.

    All tables use booktabs style for professional appearance.
    """

    def __init__(self, output_dir: Path):
        """
        Initialize the LaTeX exporter.

        Args:
            output_dir: Directory for saving .tex files
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def _save_table(self, content: str, name: str) -> Path:
        """Save table content to .tex file."""
        path = self.output_dir / f"{name}.tex"
        path.write_text(content, encoding='utf-8')
        logger.info(f"Saved: {path}")
        return path

    def _escape_latex(self, text: str) -> str:
        """Escape special LaTeX characters."""
        replacements = {
            '_': r'\_',
            '%': r'\%',
            '&': r'\&',
            '#': r'\#',
            '$': r'\$',
        }
        for old, new in replacements.items():
            text = text.replace(old, new)
        return text

    def _shorten_model_name(self, model: str) -> str:
        """Shorten model name for table display."""
        return (model
                .replace('claude-code-', 'Claude ')
                .replace('gemini-', 'Gemini ')
                .replace('-', ' ')
                .title())

    def _format_mean_std(self, mean: float, std: float) -> str:
        """Format as mean +/- std."""
        return f"{mean:.1f} $\\pm$ {std:.1f}"

    # ========================================
    # MAIN MODEL COMPARISON TABLE
    # ========================================

    def table_main_comparison(self, df: pd.DataFrame) -> str:
        """
        Generate main model comparison table.

        Format:
        | Model | Coverage (%) | Branch (%) | Mutation (%) | Quality | N |
        """
        # Aggregate per model
        agg = df.groupby('model').agg({
            'statement_coverage': ['mean', 'std'],
            'branch_coverage': ['mean', 'std'],
            'mutation_score': ['mean', 'std'],
            'overall_quality_score': ['mean', 'std'],
            'model': 'count'
        }).round(1)

        agg.columns = ['Cov_mean', 'Cov_std', 'Branch_mean', 'Branch_std',
                      'Mut_mean', 'Mut_std', 'Quality_mean', 'Quality_std', 'N']

        # Sort by coverage descending
        agg = agg.sort_values('Cov_mean', ascending=False)

        # Find best values for highlighting
        best_cov = agg['Cov_mean'].max()
        best_branch = agg['Branch_mean'].max()
        best_mut = agg['Mut_mean'].max()
        best_qual = agg['Quality_mean'].max()

        lines = [
            r"% Wygenerowano automatycznie: " + datetime.now().strftime('%Y-%m-%d %H:%M'),
            r"\begin{table}[htbp]",
            r"\centering",
            r"\caption{Porownanie modeli LLM do automatycznego generowania testow jednostkowych}",
            r"\label{tab:model-comparison}",
            r"\begin{tabular}{lccccr}",
            r"\toprule",
            r"Model & Pokrycie (\%) & Rozgal. (\%) & Mutacje (\%) & Jakosc & N \\",
            r"\midrule"
        ]

        for model, row in agg.iterrows():
            short_name = self._shorten_model_name(model)

            # Highlight best values with bold
            cov = self._format_mean_std(row['Cov_mean'], row['Cov_std'])
            if row['Cov_mean'] == best_cov:
                cov = r"\textbf{" + cov + "}"

            branch = self._format_mean_std(row['Branch_mean'], row['Branch_std'])
            if row['Branch_mean'] == best_branch:
                branch = r"\textbf{" + branch + "}"

            mut = self._format_mean_std(row['Mut_mean'], row['Mut_std'])
            if row['Mut_mean'] == best_mut:
                mut = r"\textbf{" + mut + "}"

            qual = self._format_mean_std(row['Quality_mean'], row['Quality_std'])
            if row['Quality_mean'] == best_qual:
                qual = r"\textbf{" + qual + "}"

            n = int(row['N'])

            lines.append(f"{short_name} & {cov} & {branch} & {mut} & {qual} & {n} \\\\")

        lines.extend([
            r"\bottomrule",
            r"\end{tabular}",
            r"\begin{tablenotes}",
            r"\small",
            r"\item Wartosci podano jako srednia $\pm$ odchylenie standardowe. Najlepsze wyniki pogrubiono.",
            r"\end{tablenotes}",
            r"\end{table}"
        ])

        content = '\n'.join(lines)
        self._save_table(content, 'table_model_comparison')
        return content

    # ========================================
    # STRATEGY COMPARISON TABLE
    # ========================================

    def table_strategy_comparison(self, df: pd.DataFrame) -> str:
        """
        Generate table comparing Simple vs Chain-of-Thought prompting.
        """
        metrics = ['statement_coverage', 'branch_coverage', 'mutation_score',
                  'total_test_methods', 'response_time']
        metrics = [m for m in metrics if m in df.columns]

        metric_labels = {
            'statement_coverage': 'Pokrycie instrukcji (\\%)',
            'branch_coverage': 'Pokrycie rozgalezien (\\%)',
            'mutation_score': 'Wynik mutacji (\\%)',
            'total_test_methods': 'Liczba testow',
            'response_time': 'Czas odpowiedzi (s)'
        }

        lines = [
            r"% Wygenerowano automatycznie: " + datetime.now().strftime('%Y-%m-%d %H:%M'),
            r"\begin{table}[htbp]",
            r"\centering",
            r"\caption{Porownanie strategii promptowania}",
            r"\label{tab:strategy-comparison}",
            r"\begin{tabular}{lccc}",
            r"\toprule",
            r"Metryka & Simple Prompting & Chain-of-Thought & $\Delta$ \\",
            r"\midrule"
        ]

        for metric in metrics:
            simple = df[df['strategy'] == 'simple_prompting'][metric]
            cot = df[df['strategy'] == 'chain_of_thought_prompting'][metric]

            if len(simple) == 0 or len(cot) == 0:
                continue

            simple_str = self._format_mean_std(simple.mean(), simple.std())
            cot_str = self._format_mean_std(cot.mean(), cot.std())
            delta = cot.mean() - simple.mean()
            delta_str = f"+{delta:.1f}" if delta > 0 else f"{delta:.1f}"

            # Highlight positive delta
            if delta > 0:
                delta_str = r"\textcolor{green!70!black}{" + delta_str + "}"
            elif delta < 0:
                delta_str = r"\textcolor{red!70!black}{" + delta_str + "}"

            metric_name = metric_labels.get(metric, metric.replace('_', ' ').title())
            lines.append(f"{metric_name} & {simple_str} & {cot_str} & {delta_str} \\\\")

        lines.extend([
            r"\bottomrule",
            r"\end{tabular}",
            r"\begin{tablenotes}",
            r"\small",
            r"\item $\Delta$ oznacza roznice (CoT - Simple). Wartosci dodatnie na korzysc CoT.",
            r"\end{tablenotes}",
            r"\end{table}"
        ])

        content = '\n'.join(lines)
        self._save_table(content, 'table_strategy_comparison')
        return content

    # ========================================
    # CONTEXT COMPARISON TABLE
    # ========================================

    def table_context_comparison(self, df: pd.DataFrame) -> str:
        """
        Generate table comparing context levels.
        """
        context_order = ['interface', 'interface_docstring', 'full_context']
        context_labels = ['Interfejs', 'Interfejs + Docstring', 'Pelny kontekst']

        metrics = ['statement_coverage', 'mutation_score', 'overall_quality_score']
        metrics = [m for m in metrics if m in df.columns]

        metric_labels = {
            'statement_coverage': 'Pokrycie instrukcji (\\%)',
            'mutation_score': 'Wynik mutacji (\\%)',
            'overall_quality_score': 'Jakosc ogolna'
        }

        lines = [
            r"% Wygenerowano automatycznie: " + datetime.now().strftime('%Y-%m-%d %H:%M'),
            r"\begin{table}[htbp]",
            r"\centering",
            r"\caption{Wplyw poziomu kontekstu na jakosc generowanych testow}",
            r"\label{tab:context-comparison}",
            r"\begin{tabular}{l" + "c" * len(context_labels) + "}",
            r"\toprule",
            r"Metryka & " + " & ".join(context_labels) + r" \\",
            r"\midrule"
        ]

        for metric in metrics:
            row_values = []
            best_val = -float('inf')
            best_idx = -1

            for i, ctx in enumerate(context_order):
                ctx_data = df[df['context'] == ctx][metric]
                if len(ctx_data) > 0:
                    val = self._format_mean_std(ctx_data.mean(), ctx_data.std())
                    row_values.append((val, ctx_data.mean()))
                    if ctx_data.mean() > best_val:
                        best_val = ctx_data.mean()
                        best_idx = i
                else:
                    row_values.append(("N/A", 0))

            # Bold best value
            formatted = []
            for i, (val, _) in enumerate(row_values):
                if i == best_idx and val != "N/A":
                    formatted.append(r"\textbf{" + val + "}")
                else:
                    formatted.append(val)

            metric_name = metric_labels.get(metric, metric.replace('_', ' ').title())
            lines.append(f"{metric_name} & " + " & ".join(formatted) + r" \\")

        lines.extend([
            r"\bottomrule",
            r"\end{tabular}",
            r"\begin{tablenotes}",
            r"\small",
            r"\item Najlepsze wyniki dla kazdej metryki pogrubiono.",
            r"\end{tablenotes}",
            r"\end{table}"
        ])

        content = '\n'.join(lines)
        self._save_table(content, 'table_context_comparison')
        return content

    # ========================================
    # STATISTICAL TESTS TABLE
    # ========================================

    def table_statistical_tests(self, test_results: pd.DataFrame) -> str:
        """
        Generate table with statistical test results.

        Args:
            test_results: DataFrame with columns:
                - Comparison, Test, Statistic, p-value, Significant, Effect
        """
        lines = [
            r"% Wygenerowano automatycznie: " + datetime.now().strftime('%Y-%m-%d %H:%M'),
            r"\begin{table}[htbp]",
            r"\centering",
            r"\caption{Istotnosc statystyczna zaobserwowanych roznic}",
            r"\label{tab:statistical-tests}",
            r"\begin{tabular}{llcccl}",
            r"\toprule",
            r"Porownanie & Test & Statystyka & p-value & Ist. & Efekt \\",
            r"\midrule"
        ]

        for _, row in test_results.iterrows():
            comparison = self._escape_latex(str(row.get('Comparison', '')))
            test = str(row.get('Test', ''))
            stat = row.get('Statistic', 0)
            p_val = row.get('p-value', 1)
            sig = row.get('Significant', False)
            effect = str(row.get('Effect', 'N/A'))

            sig_mark = r"\checkmark" if sig else ""

            # Format p-value with significance stars
            if p_val < 0.001:
                p_str = "< 0.001***"
            elif p_val < 0.01:
                p_str = f"{p_val:.3f}**"
            elif p_val < 0.05:
                p_str = f"{p_val:.3f}*"
            else:
                p_str = f"{p_val:.3f}"

            lines.append(
                f"{comparison} & {test} & {stat:.3f} & {p_str} & {sig_mark} & {effect} \\\\"
            )

        lines.extend([
            r"\bottomrule",
            r"\end{tabular}",
            r"\begin{tablenotes}",
            r"\small",
            r"\item Istotnosc: * p < 0.05, ** p < 0.01, *** p < 0.001",
            r"\item Interpretacja wielkosci efektu: maly (d < 0.5), sredni (0.5 $\leq$ d < 0.8), duzy (d $\geq$ 0.8)",
            r"\end{tablenotes}",
            r"\end{table}"
        ])

        content = '\n'.join(lines)
        self._save_table(content, 'table_statistical_tests')
        return content

    # ========================================
    # DETAILED RESULTS TABLE (APPENDIX)
    # ========================================

    def table_detailed_results(self,
                              df: pd.DataFrame,
                              metrics: Optional[List[str]] = None) -> str:
        """
        Generate detailed results table for appendix.
        Uses longtable for multi-page support.
        """
        if metrics is None:
            metrics = ['statement_coverage', 'branch_coverage', 'mutation_score',
                      'total_test_methods', 'overall_quality_score']
            metrics = [m for m in metrics if m in df.columns]

        lines = [
            r"% Wygenerowano automatycznie: " + datetime.now().strftime('%Y-%m-%d %H:%M'),
            r"\begin{longtable}{llllrrrrr}",
            r"\caption{Szczegolowe wyniki eksperymentow} \\",
            r"\label{tab:detailed-results}",
            r"\toprule",
            r"Model & Strategia & Kontekst & N & Pokr. & Rozg. & Mut. & Testy & Jakosc \\",
            r"\midrule",
            r"\endfirsthead",
            r"\multicolumn{9}{c}{{\tablename\ \thetable{} -- kontynuacja z poprzedniej strony}} \\",
            r"\toprule",
            r"Model & Strategia & Kontekst & N & Pokr. & Rozg. & Mut. & Testy & Jakosc \\",
            r"\midrule",
            r"\endhead",
            r"\midrule",
            r"\multicolumn{9}{r}{{Kontynuacja na nastepnej stronie}} \\",
            r"\endfoot",
            r"\bottomrule",
            r"\endlastfoot"
        ]

        # Group and aggregate
        grouped = df.groupby(['model', 'strategy', 'context']).agg({
            'statement_coverage': 'mean',
            'branch_coverage': 'mean',
            'mutation_score': 'mean',
            'total_test_methods': 'mean',
            'overall_quality_score': 'mean',
            'model': 'count'
        }).round(1)

        grouped.columns = ['Cov', 'Branch', 'Mut', 'Tests', 'Quality', 'N']
        grouped = grouped.reset_index()

        for _, row in grouped.iterrows():
            model_short = (row['model']
                          .replace('claude-code-', 'C-')
                          .replace('gemini-', 'G-'))
            strategy_short = 'Simple' if 'simple' in row['strategy'] else 'CoT'
            context_short = {'interface': 'INT',
                           'interface_docstring': 'DOC',
                           'full_context': 'FULL'}.get(row['context'], row['context'][:3].upper())

            lines.append(
                f"{model_short} & {strategy_short} & {context_short} & "
                f"{int(row['N'])} & {row['Cov']:.1f} & {row['Branch']:.1f} & "
                f"{row['Mut']:.1f} & {row['Tests']:.0f} & {row['Quality']:.1f} \\\\"
            )

        lines.append(r"\end{longtable}")

        content = '\n'.join(lines)
        self._save_table(content, 'table_detailed_results')
        return content

    # ========================================
    # GENERATE ALL TABLES
    # ========================================

    def generate_all_tables(self,
                           df: pd.DataFrame,
                           stat_results: Optional[pd.DataFrame] = None) -> Dict[str, str]:
        """
        Generate all thesis tables.

        Returns dictionary mapping table name to content.
        """
        tables = {}

        logger.info("Generowanie tabel LaTeX...")

        # Main comparison table
        tables['model_comparison'] = self.table_main_comparison(df)

        # Strategy comparison
        if 'strategy' in df.columns:
            tables['strategy_comparison'] = self.table_strategy_comparison(df)

        # Context comparison
        if 'context' in df.columns:
            tables['context_comparison'] = self.table_context_comparison(df)

        # Statistical tests (if provided)
        if stat_results is not None and len(stat_results) > 0:
            tables['statistical_tests'] = self.table_statistical_tests(stat_results)

        # Detailed results
        tables['detailed_results'] = self.table_detailed_results(df)

        logger.info(f"Wygenerowano {len(tables)} tabel LaTeX do: {self.output_dir}")
        return tables


# CLI entry point
if __name__ == "__main__":
    import sys
    from pathlib import Path
    from data_aggregator import MultiDimensionalAggregator

    logging.basicConfig(level=logging.INFO)

    if len(sys.argv) > 1:
        results_dir = Path(sys.argv[1])
    else:
        results_dir = Path("cli_results")

    output_dir = Path("reporting/outputs/tables/latex")

    if not results_dir.exists():
        print(f"Blad: Katalog wynikow nie istnieje: {results_dir}")
        sys.exit(1)

    print(f"Ladowanie wynikow z: {results_dir}")
    agg = MultiDimensionalAggregator(results_dir)
    df = agg.to_dataframe()

    print(f"Generowanie tabel LaTeX do: {output_dir}")
    latex = LaTeXTableGenerator(output_dir)
    latex.generate_all_tables(df)

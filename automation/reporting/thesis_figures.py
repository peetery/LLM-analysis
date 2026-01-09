"""
Thesis Figures Generator.

Main entry point for generating all figures, tables, and reports
for the engineering thesis.

Usage:
    python -m reporting.thesis_figures [results_dir] [output_dir]
    python -m reporting.thesis_figures --help

Examples:
    python -m reporting.thesis_figures cli_results reporting/outputs
    python -m reporting.thesis_figures  # Uses defaults
"""

import argparse
import logging
import sys
from pathlib import Path
from datetime import datetime

from .data_aggregator import MultiDimensionalAggregator
from .statistical_analyzer import StatisticalAnalyzer
from .chart_generator import ThesisChartGenerator
from .latex_exporter import LaTeXTableGenerator
from .report_builder import ThesisReportBuilder

logger = logging.getLogger(__name__)


def generate_all_thesis_artifacts(results_dir: Path, output_dir: Path) -> dict:
    """
    Generate all thesis artifacts: figures, tables, and reports.

    Args:
        results_dir: Path to cli_results directory
        output_dir: Base output directory for all artifacts

    Returns:
        Dictionary with generation summary
    """
    summary = {
        'start_time': datetime.now().isoformat(),
        'results_dir': str(results_dir),
        'output_dir': str(output_dir),
        'figures': [],
        'tables': [],
        'reports': [],
        'errors': []
    }

    print("=" * 60)
    print("GENERATOR WYKRESOW I RAPORTOW DO PRACY INZYNIERSKIEJ")
    print("=" * 60)
    print(f"\nKatalog wynikow: {results_dir}")
    print(f"Katalog wyjsciowy: {output_dir}\n")

    # Create output directories
    figures_dir = output_dir / "figures"
    tables_dir = output_dir / "tables" / "latex"
    reports_dir = output_dir / "reports"

    for d in [figures_dir, tables_dir, reports_dir]:
        d.mkdir(parents=True, exist_ok=True)

    # Step 1: Load and aggregate data
    print("[1/5] Ladowanie wynikow eksperymentow...")
    try:
        agg = MultiDimensionalAggregator(results_dir)
        df = agg.to_dataframe()

        if len(df) == 0:
            print("BLAD: Nie znaleziono wynikow eksperymentow!")
            summary['errors'].append("Nie znaleziono wynikow eksperymentow")
            return summary

        stats = agg.get_statistics_summary()
        print(f"      Zaladowano {stats['total_experiments']} eksperymentow")
        print(f"      Modele: {stats['unique_models']}")
        print(f"      Strategie: {stats['unique_strategies']}")
        print(f"      Konteksty: {stats['unique_contexts']}")

    except Exception as e:
        print(f"BLAD ladowania wynikow: {e}")
        summary['errors'].append(f"Blad ladowania: {e}")
        return summary

    # Step 2: Generate figures
    print("\n[2/5] Generowanie wykresow...")
    try:
        chart_gen = ThesisChartGenerator(figures_dir)
        chart_gen.generate_all_figures(df)
        summary['figures'].append(str(figures_dir))
        print(f"      Zapisano do: {figures_dir}")
    except Exception as e:
        print(f"BLAD generowania wykresow: {e}")
        summary['errors'].append(f"Blad wykresow: {e}")
        logger.exception("Figure generation failed")

    # Step 3: Run statistical analysis
    print("\n[3/5] Analiza statystyczna...")
    try:
        analyzer = StatisticalAnalyzer(df)

        # Generate comparison report
        comparisons = []
        if 'strategy' in df.columns and df['strategy'].nunique() >= 2:
            strategies = df['strategy'].unique()
            comparisons.append(('strategy', strategies[0], strategies[1]))

        if comparisons:
            stat_report = analyzer.generate_comparison_report('statement_coverage', comparisons)
            print(f"      Wykonano {len(stat_report)} porownan statystycznych")
        else:
            stat_report = None
            print("      Brak porownan (niewystarczajaca liczba grup)")

    except Exception as e:
        print(f"BLAD analizy statystycznej: {e}")
        summary['errors'].append(f"Blad statystyk: {e}")
        stat_report = None

    # Step 4: Generate LaTeX tables
    print("\n[4/5] Generowanie tabel LaTeX...")
    try:
        latex_gen = LaTeXTableGenerator(tables_dir)
        latex_gen.generate_all_tables(df, stat_report)
        summary['tables'].append(str(tables_dir))
        print(f"      Zapisano do: {tables_dir}")
    except Exception as e:
        print(f"BLAD generowania tabel: {e}")
        summary['errors'].append(f"Blad tabel: {e}")
        logger.exception("Table generation failed")

    # Step 5: Generate reports
    print("\n[5/5] Generowanie raportow...")
    try:
        report_builder = ThesisReportBuilder(agg, reports_dir)
        report_builder.build_chapter_6_draft()
        report_builder.build_executive_summary()
        summary['reports'].append(str(reports_dir))
        print(f"      Zapisano do: {reports_dir}")
    except Exception as e:
        print(f"BLAD generowania raportow: {e}")
        summary['errors'].append(f"Blad raportow: {e}")
        logger.exception("Report generation failed")

    # Export raw data
    print("\n[Bonus] Eksport surowych danych...")
    try:
        csv_path = output_dir / "raw_data.csv"
        df.to_csv(csv_path, index=False, encoding='utf-8')
        print(f"      Zapisano do: {csv_path}")

        summary_csv = output_dir / "summary_by_config.csv"
        agg.to_summary_dataframe().to_csv(summary_csv, index=False, encoding='utf-8')
        print(f"      Zapisano do: {summary_csv}")

    except Exception as e:
        print(f"BLAD eksportu danych: {e}")
        summary['errors'].append(f"Blad eksportu: {e}")

    # Summary
    print("\n" + "=" * 60)
    print("GENEROWANIE ZAKONCZONE")
    print("=" * 60)

    if summary['errors']:
        print(f"\nUWAGA: Wystapilo {len(summary['errors'])} bledow:")
        for err in summary['errors']:
            print(f"  - {err}")
    else:
        print("\nWszystkie artefakty wygenerowane pomyslnie!")

    print(f"\nLokalizacje plikow wyjsciowych:")
    print(f"  Wykresy: {figures_dir}")
    print(f"  Tabele:  {tables_dir}")
    print(f"  Raporty: {reports_dir}")
    print(f"  Dane:    {output_dir}")

    summary['end_time'] = datetime.now().isoformat()
    return summary


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description='Generuje wszystkie wykresy, tabele i raporty do pracy inzynierskiej',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Przyklady uzycia:
  python -m reporting.thesis_figures
  python -m reporting.thesis_figures cli_results
  python -m reporting.thesis_figures cli_results reporting/outputs

Generator tworzy:
  - figures/pdf/  - wykresy PDF do LaTeX
  - figures/png/  - wykresy PNG do podgladu
  - tables/latex/ - tabele LaTeX (pliki .tex)
  - reports/      - raporty Markdown
  - raw_data.csv  - eksport danych eksperymentalnych
"""
    )

    parser.add_argument(
        'results_dir',
        nargs='?',
        default='cli_results',
        help='Katalog z wynikami eksperymentow (domyslnie: cli_results)'
    )

    parser.add_argument(
        'output_dir',
        nargs='?',
        default='reporting/outputs',
        help='Katalog wyjsciowy dla artefaktow (domyslnie: reporting/outputs)'
    )

    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Wlacz szczegolowe logowanie'
    )

    args = parser.parse_args()

    # Setup logging
    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('thesis_figures.log'),
            logging.StreamHandler()
        ]
    )

    # Resolve paths
    results_dir = Path(args.results_dir)
    output_dir = Path(args.output_dir)

    if not results_dir.exists():
        print(f"BLAD: Katalog wynikow nie istnieje: {results_dir}")
        print("\nUpewnij sie, ze masz wyniki eksperymentow w katalogu cli_results.")
        sys.exit(1)

    # Generate artifacts
    summary = generate_all_thesis_artifacts(results_dir, output_dir)

    # Exit with error code if there were errors
    if summary['errors']:
        sys.exit(1)


if __name__ == "__main__":
    main()

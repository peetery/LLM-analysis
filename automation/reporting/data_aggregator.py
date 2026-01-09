"""
Data Aggregator for multi-dimensional experiment analysis.

This module provides tools for loading and aggregating experiment results
across multiple dimensions: models, strategies, and context levels.

Phase R1 of the reporting system.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
from pathlib import Path
import json
import logging

import pandas as pd
import numpy as np

logger = logging.getLogger(__name__)


@dataclass
class ExperimentConfig:
    """Configuration for a single experiment."""
    model: str
    strategy: str
    context: str
    run_id: int

    @property
    def config_key(self) -> str:
        """Unique configuration key (without run_id)."""
        return f"{self.model}_{self.strategy}_{self.context}"

    def __str__(self) -> str:
        return f"{self.model}/{self.strategy}/{self.context}/run_{self.run_id:03d}"


@dataclass
class AggregatedMetrics:
    """Aggregated metrics for a group of experiments."""
    n: int                    # Number of observations
    mean: float
    std: float
    median: float
    min: float
    max: float
    ci_95_lower: float        # 95% confidence interval lower bound
    ci_95_upper: float        # 95% confidence interval upper bound
    cv: float                 # Coefficient of variation (%)
    iqr: float                # Interquartile range
    raw_values: List[float] = field(default_factory=list, repr=False)

    @classmethod
    def from_values(cls, values: List[float]) -> 'AggregatedMetrics':
        """Calculate all metrics from a list of values."""
        if not values or len(values) == 0:
            return cls(
                n=0, mean=0.0, std=0.0, median=0.0,
                min=0.0, max=0.0, ci_95_lower=0.0, ci_95_upper=0.0,
                cv=0.0, iqr=0.0, raw_values=[]
            )

        arr = np.array(values, dtype=float)
        n = len(arr)
        mean_val = float(np.mean(arr))
        std_val = float(np.std(arr, ddof=1)) if n > 1 else 0.0

        # 95% CI using t-distribution for small samples
        if n > 1:
            from scipy import stats as scipy_stats
            se = std_val / np.sqrt(n)
            # Use t-distribution for small samples
            if n < 30:
                t_val = scipy_stats.t.ppf(0.975, n - 1)
                ci_margin = t_val * se
            else:
                ci_margin = 1.96 * se  # z-value for 95% CI
            ci_lower = mean_val - ci_margin
            ci_upper = mean_val + ci_margin
        else:
            ci_lower = ci_upper = mean_val

        # CV (coefficient of variation)
        cv = (std_val / mean_val * 100) if mean_val != 0 else 0.0

        return cls(
            n=n,
            mean=round(mean_val, 2),
            std=round(std_val, 2),
            median=round(float(np.median(arr)), 2),
            min=round(float(np.min(arr)), 2),
            max=round(float(np.max(arr)), 2),
            ci_95_lower=round(ci_lower, 2),
            ci_95_upper=round(ci_upper, 2),
            cv=round(cv, 2),
            iqr=round(float(np.percentile(arr, 75) - np.percentile(arr, 25)), 2),
            raw_values=values
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary (without raw values)."""
        return {
            'n': self.n,
            'mean': self.mean,
            'std': self.std,
            'median': self.median,
            'min': self.min,
            'max': self.max,
            'ci_95_lower': self.ci_95_lower,
            'ci_95_upper': self.ci_95_upper,
            'cv': self.cv,
            'iqr': self.iqr
        }

    def format_mean_std(self) -> str:
        """Format as 'mean +/- std'."""
        return f"{self.mean:.1f} +/- {self.std:.1f}"

    def format_mean_ci(self) -> str:
        """Format as 'mean [CI_lower, CI_upper]'."""
        return f"{self.mean:.1f} [{self.ci_95_lower:.1f}, {self.ci_95_upper:.1f}]"


class MultiDimensionalAggregator:
    """
    Multi-dimensional aggregator for experiment results.

    Supports aggregation by:
    - model
    - strategy
    - context level
    - any combination of the above
    """

    # Main metrics to track
    METRICS = [
        'statement_coverage',
        'branch_coverage',
        'mutation_score',
        'test_success_rate',
        'total_test_methods',
        'total_assertions',
        'overall_quality_score',
        'response_time',
        'assertion_quality_score',
        'naming_quality_score',
        'independence_score',
        'avg_assertions_per_test',
        'average_test_length'
    ]

    # Primary metrics for main comparisons
    PRIMARY_METRICS = [
        'statement_coverage',
        'branch_coverage',
        'mutation_score',
        'overall_quality_score'
    ]

    def __init__(self, results_dir: Path):
        """
        Initialize the aggregator.

        Args:
            results_dir: Path to cli_results directory
        """
        self.results_dir = Path(results_dir)
        self.raw_data: Optional[pd.DataFrame] = None
        self._load_all_results()

    def _load_all_results(self) -> None:
        """Load all experiment results into a DataFrame."""
        records = []
        errors = []

        for analysis_file in self.results_dir.rglob("analysis_results.json"):
            run_dir = analysis_file.parent
            config = self._parse_path(run_dir)

            if config:
                metrics = self._load_metrics(analysis_file)
                if metrics:
                    record = {
                        'model': config.model,
                        'strategy': config.strategy,
                        'context': config.context,
                        'run_id': config.run_id,
                        'config_key': config.config_key,
                        'result_dir': str(run_dir),
                        **metrics
                    }
                    records.append(record)
                else:
                    errors.append(f"Failed to load metrics from: {analysis_file}")
            else:
                errors.append(f"Failed to parse path: {run_dir}")

        self.raw_data = pd.DataFrame(records)

        if errors:
            logger.warning(f"Encountered {len(errors)} errors while loading results")
            for err in errors[:5]:
                logger.debug(err)

        logger.info(f"Loaded {len(self.raw_data)} experiment results")

    def _parse_path(self, run_dir: Path) -> Optional[ExperimentConfig]:
        """Parse directory path to experiment configuration."""
        # Expected: cli_results/strategy/context/model/run_XXX
        parts = run_dir.parts
        try:
            # Find 'cli_results' in path
            idx = None
            for i, part in enumerate(parts):
                if 'cli_results' in part:
                    idx = i
                    break

            if idx is None:
                return None

            return ExperimentConfig(
                strategy=parts[idx + 1],
                context=parts[idx + 2],
                model=parts[idx + 3],
                run_id=int(parts[idx + 4].replace('run_', ''))
            )
        except (ValueError, IndexError) as e:
            logger.debug(f"Failed to parse path {run_dir}: {e}")
            return None

    def _load_metrics(self, analysis_file: Path) -> Optional[Dict[str, Any]]:
        """Load metrics from analysis_results.json file."""
        try:
            with open(analysis_file, encoding='utf-8') as f:
                data = json.load(f)

            # Try different possible structures
            metrics = {}

            # Check for 'summary' key
            if 'summary' in data:
                metrics.update(data['summary'])

            # Check for direct metrics
            for key in self.METRICS:
                if key in data:
                    metrics[key] = data[key]

            # Check for coverage_analysis
            if 'coverage_analysis' in data:
                cov = data['coverage_analysis']
                if 'statement_coverage' in cov:
                    metrics['statement_coverage'] = cov['statement_coverage']
                if 'branch_coverage' in cov:
                    metrics['branch_coverage'] = cov['branch_coverage']

            # Check for mutation_analysis
            if 'mutation_analysis' in data:
                mut = data['mutation_analysis']
                if 'mutation_score' in mut:
                    metrics['mutation_score'] = mut['mutation_score']

            # Check for test_analysis
            if 'test_analysis' in data:
                test = data['test_analysis']
                if 'test_success_rate' in test:
                    metrics['test_success_rate'] = test['test_success_rate']
                if 'total_test_methods' in test:
                    metrics['total_test_methods'] = test['total_test_methods']

            # Check for quality_analysis
            if 'quality_analysis' in data:
                qual = data['quality_analysis']
                if 'overall_quality_score' in qual:
                    metrics['overall_quality_score'] = qual['overall_quality_score']

            return metrics if metrics else None

        except (json.JSONDecodeError, IOError) as e:
            logger.error(f"Failed to load {analysis_file}: {e}")
            return None

    # --- Aggregation Methods ---

    def aggregate_by_model(self) -> Dict[str, Dict[str, AggregatedMetrics]]:
        """Aggregate results per model (across all strategies and contexts)."""
        return self._aggregate_by_column('model')

    def aggregate_by_strategy(self) -> Dict[str, Dict[str, AggregatedMetrics]]:
        """Aggregate results per strategy."""
        return self._aggregate_by_column('strategy')

    def aggregate_by_context(self) -> Dict[str, Dict[str, AggregatedMetrics]]:
        """Aggregate results per context level."""
        return self._aggregate_by_column('context')

    def aggregate_by_config(self) -> Dict[str, Dict[str, AggregatedMetrics]]:
        """Aggregate results per configuration (model+strategy+context)."""
        return self._aggregate_by_column('config_key')

    def aggregate_model_by_strategy(self) -> pd.DataFrame:
        """
        Create pivot table: models x strategies.
        Useful for main comparison tables.
        """
        pivot = self.raw_data.pivot_table(
            values=self.PRIMARY_METRICS,
            index='model',
            columns='strategy',
            aggfunc=['mean', 'std']
        )
        return pivot

    def aggregate_model_by_context(self) -> pd.DataFrame:
        """Create pivot table: models x contexts."""
        pivot = self.raw_data.pivot_table(
            values=self.PRIMARY_METRICS,
            index='model',
            columns='context',
            aggfunc=['mean', 'std']
        )
        return pivot

    def aggregate_strategy_by_context(self) -> pd.DataFrame:
        """Create pivot table: strategies x contexts."""
        pivot = self.raw_data.pivot_table(
            values=self.PRIMARY_METRICS,
            index='strategy',
            columns='context',
            aggfunc=['mean', 'std']
        )
        return pivot

    def _aggregate_by_column(self, column: str) -> Dict[str, Dict[str, AggregatedMetrics]]:
        """Generic aggregation by selected column."""
        result = {}

        for group_name, group_df in self.raw_data.groupby(column):
            result[group_name] = {}
            for metric in self.METRICS:
                if metric in group_df.columns:
                    values = group_df[metric].dropna().tolist()
                    if values:
                        result[group_name][metric] = AggregatedMetrics.from_values(values)

        return result

    def get_best_model(self, metric: str = 'statement_coverage') -> str:
        """Get the model with highest mean for given metric."""
        by_model = self.raw_data.groupby('model')[metric].mean()
        return by_model.idxmax()

    def get_best_strategy(self, metric: str = 'statement_coverage') -> str:
        """Get the strategy with highest mean for given metric."""
        by_strategy = self.raw_data.groupby('strategy')[metric].mean()
        return by_strategy.idxmax()

    def get_best_context(self, metric: str = 'statement_coverage') -> str:
        """Get the context level with highest mean for given metric."""
        by_context = self.raw_data.groupby('context')[metric].mean()
        return by_context.idxmax()

    # --- Export Methods ---

    def to_dataframe(self) -> pd.DataFrame:
        """Return raw data as DataFrame."""
        return self.raw_data.copy()

    def to_summary_dataframe(self) -> pd.DataFrame:
        """
        Create summary DataFrame with mean+/-std for each configuration.
        Ideal for LaTeX export.
        """
        summary_records = []

        for config_key, group_df in self.raw_data.groupby('config_key'):
            first_row = group_df.iloc[0]

            record = {
                'Model': first_row['model'],
                'Strategy': first_row['strategy'],
                'Context': first_row['context'],
                'N': len(group_df)
            }

            for metric in self.PRIMARY_METRICS:
                if metric in group_df.columns:
                    agg = AggregatedMetrics.from_values(
                        group_df[metric].dropna().tolist()
                    )
                    record[f'{metric}_mean'] = agg.mean
                    record[f'{metric}_std'] = agg.std
                    record[f'{metric}_ci'] = f"[{agg.ci_95_lower}, {agg.ci_95_upper}]"

            summary_records.append(record)

        return pd.DataFrame(summary_records)

    def to_model_summary(self) -> pd.DataFrame:
        """Create per-model summary DataFrame."""
        records = []

        for model, metrics in self.aggregate_by_model().items():
            record = {'Model': model}
            for metric_name, agg in metrics.items():
                if metric_name in self.PRIMARY_METRICS:
                    record[f'{metric_name}_mean'] = agg.mean
                    record[f'{metric_name}_std'] = agg.std
                    record['N'] = agg.n
            records.append(record)

        df = pd.DataFrame(records)
        if 'statement_coverage_mean' in df.columns:
            df = df.sort_values('statement_coverage_mean', ascending=False)
        return df

    def to_strategy_summary(self) -> pd.DataFrame:
        """Create per-strategy summary DataFrame."""
        records = []

        for strategy, metrics in self.aggregate_by_strategy().items():
            record = {'Strategy': strategy}
            for metric_name, agg in metrics.items():
                if metric_name in self.PRIMARY_METRICS:
                    record[f'{metric_name}_mean'] = agg.mean
                    record[f'{metric_name}_std'] = agg.std
                    record['N'] = agg.n
            records.append(record)

        return pd.DataFrame(records)

    def to_context_summary(self) -> pd.DataFrame:
        """Create per-context summary DataFrame."""
        records = []

        for context, metrics in self.aggregate_by_context().items():
            record = {'Context': context}
            for metric_name, agg in metrics.items():
                if metric_name in self.PRIMARY_METRICS:
                    record[f'{metric_name}_mean'] = agg.mean
                    record[f'{metric_name}_std'] = agg.std
                    record['N'] = agg.n
            records.append(record)

        return pd.DataFrame(records)

    def get_statistics_summary(self) -> Dict[str, Any]:
        """Get overall statistics summary."""
        df = self.raw_data

        return {
            'total_experiments': len(df),
            'unique_models': df['model'].nunique(),
            'unique_strategies': df['strategy'].nunique(),
            'unique_contexts': df['context'].nunique(),
            'unique_configs': df['config_key'].nunique(),
            'models': df['model'].unique().tolist(),
            'strategies': df['strategy'].unique().tolist(),
            'contexts': df['context'].unique().tolist(),
            'runs_per_config': df.groupby('config_key').size().to_dict(),
            'overall_coverage_mean': df['statement_coverage'].mean() if 'statement_coverage' in df else None,
            'overall_mutation_mean': df['mutation_score'].mean() if 'mutation_score' in df else None,
        }

    def export_to_csv(self, output_path: Path) -> None:
        """Export summary to CSV file."""
        summary_df = self.to_summary_dataframe()
        summary_df.to_csv(output_path, index=False, encoding='utf-8')
        logger.info(f"Exported summary to: {output_path}")


# Example usage and CLI
if __name__ == "__main__":
    import sys

    logging.basicConfig(level=logging.INFO)

    if len(sys.argv) > 1:
        results_dir = Path(sys.argv[1])
    else:
        results_dir = Path("cli_results")

    if not results_dir.exists():
        print(f"Blad: Katalog wynikow nie istnieje: {results_dir}")
        sys.exit(1)

    print(f"Ladowanie wynikow z: {results_dir}")
    agg = MultiDimensionalAggregator(results_dir)

    stats = agg.get_statistics_summary()
    print(f"\n{'='*60}")
    print(f"Zaladowano {stats['total_experiments']} eksperymentow")
    print(f"Modele: {stats['unique_models']}")
    print(f"Strategie: {stats['unique_strategies']}")
    print(f"Konteksty: {stats['unique_contexts']}")
    print(f"{'='*60}\n")

    # Show model summary
    print("Podsumowanie modeli:")
    print(agg.to_model_summary().to_string())

    # Export to CSV
    output_csv = results_dir / "aggregated_summary.csv"
    agg.export_to_csv(output_csv)

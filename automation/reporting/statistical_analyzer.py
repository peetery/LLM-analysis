"""
Statistical Analyzer for experiment comparisons.

This module provides statistical tests for comparing groups:
- Normality tests (Shapiro-Wilk)
- Two-group comparisons (t-test, Mann-Whitney U)
- Multiple group comparisons (ANOVA, Kruskal-Wallis)
- Effect size calculations (Cohen's d)
- Post-hoc tests with Bonferroni correction

Phase R2 of the reporting system.
"""

from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional, Any
import logging

import numpy as np
import pandas as pd
from scipy import stats

logger = logging.getLogger(__name__)


@dataclass
class StatisticalTestResult:
    """Result of a statistical test."""
    test_name: str
    statistic: float
    p_value: float
    significant: bool           # p < alpha
    effect_size: Optional[float] = None
    effect_interpretation: Optional[str] = None  # negligible/small/medium/large
    group1_name: Optional[str] = None
    group2_name: Optional[str] = None
    n1: Optional[int] = None
    n2: Optional[int] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'test_name': self.test_name,
            'statistic': round(self.statistic, 4),
            'p_value': round(self.p_value, 6),
            'significant': self.significant,
            'effect_size': round(self.effect_size, 3) if self.effect_size else None,
            'effect_interpretation': self.effect_interpretation,
            'group1': self.group1_name,
            'group2': self.group2_name,
            'n1': self.n1,
            'n2': self.n2
        }

    def to_latex(self) -> str:
        """Format result for LaTeX."""
        sig_marker = "*" if self.significant else ""
        return f"{self.statistic:.3f}{sig_marker} (p={self.p_value:.4f})"

    def __str__(self) -> str:
        sig = "significant" if self.significant else "not significant"
        effect = f", effect={self.effect_interpretation}" if self.effect_interpretation else ""
        return f"{self.test_name}: stat={self.statistic:.4f}, p={self.p_value:.4f} ({sig}{effect})"


@dataclass
class NormalityTestResult:
    """Result of normality test for a group."""
    group_name: str
    statistic: float
    p_value: float
    is_normal: bool  # p > alpha means normal distribution
    n: int

    def __str__(self) -> str:
        normal = "normal" if self.is_normal else "non-normal"
        return f"{self.group_name}: W={self.statistic:.4f}, p={self.p_value:.4f} ({normal}, n={self.n})"


class StatisticalAnalyzer:
    """
    Performs statistical tests for group comparisons.

    Automatically selects appropriate tests based on:
    - Sample size
    - Normality of distributions
    - Number of groups
    """

    ALPHA = 0.05  # Significance level

    def __init__(self, data: pd.DataFrame, alpha: float = 0.05):
        """
        Initialize the analyzer.

        Args:
            data: DataFrame with experiment results
            alpha: Significance level (default 0.05)
        """
        self.data = data
        self.ALPHA = alpha

    # --- Normality Tests ---

    def test_normality(self,
                      column: str,
                      group_by: Optional[str] = None) -> Dict[str, NormalityTestResult]:
        """
        Perform Shapiro-Wilk normality test.

        Args:
            column: Column to test
            group_by: Optional grouping column

        Returns:
            Dictionary of normality test results per group
        """
        results = {}

        if group_by:
            for group_name, group_df in self.data.groupby(group_by):
                values = group_df[column].dropna().values
                if len(values) >= 3:
                    stat, p = stats.shapiro(values)
                    results[group_name] = NormalityTestResult(
                        group_name=str(group_name),
                        statistic=float(stat),
                        p_value=float(p),
                        is_normal=p > self.ALPHA,
                        n=len(values)
                    )
                else:
                    logger.warning(f"Group {group_name} has < 3 observations, skipping normality test")
        else:
            values = self.data[column].dropna().values
            if len(values) >= 3:
                stat, p = stats.shapiro(values)
                results['all'] = NormalityTestResult(
                    group_name='all',
                    statistic=float(stat),
                    p_value=float(p),
                    is_normal=p > self.ALPHA,
                    n=len(values)
                )

        return results

    def check_all_normal(self,
                        column: str,
                        group_by: str) -> Tuple[bool, Dict[str, NormalityTestResult]]:
        """
        Check if all groups have normal distribution.

        Returns:
            (all_normal, normality_results)
        """
        results = self.test_normality(column, group_by)
        all_normal = all(r.is_normal for r in results.values())
        return all_normal, results

    # --- Two-Group Comparisons ---

    def compare_two_groups(self,
                          column: str,
                          group_by: str,
                          group1: str,
                          group2: str) -> StatisticalTestResult:
        """
        Compare two groups using appropriate test.

        Automatically selects:
        - Independent t-test if both groups are normal
        - Mann-Whitney U test otherwise

        Args:
            column: Metric to compare
            group_by: Grouping column
            group1: Name of first group
            group2: Name of second group

        Returns:
            StatisticalTestResult
        """
        g1_data = self.data[self.data[group_by] == group1][column].dropna().values
        g2_data = self.data[self.data[group_by] == group2][column].dropna().values

        if len(g1_data) < 3 or len(g2_data) < 3:
            logger.warning(f"Insufficient data for comparison: {group1}={len(g1_data)}, {group2}={len(g2_data)}")
            return StatisticalTestResult(
                test_name="Insufficient data",
                statistic=0.0,
                p_value=1.0,
                significant=False,
                group1_name=group1,
                group2_name=group2,
                n1=len(g1_data),
                n2=len(g2_data)
            )

        # Test normality
        _, p1 = stats.shapiro(g1_data)
        _, p2 = stats.shapiro(g2_data)
        both_normal = p1 > self.ALPHA and p2 > self.ALPHA

        if both_normal:
            # Check variance equality (Levene's test)
            _, levene_p = stats.levene(g1_data, g2_data)
            equal_var = levene_p > self.ALPHA

            # Independent samples t-test
            stat, p = stats.ttest_ind(g1_data, g2_data, equal_var=equal_var)
            test_name = "Independent t-test" + (" (Welch's)" if not equal_var else "")
        else:
            # Mann-Whitney U test (non-parametric)
            stat, p = stats.mannwhitneyu(g1_data, g2_data, alternative='two-sided')
            test_name = "Mann-Whitney U"

        # Calculate effect size (Cohen's d)
        cohens_d = self._cohens_d(g1_data, g2_data)
        effect_interp = self._interpret_cohens_d(cohens_d)

        return StatisticalTestResult(
            test_name=test_name,
            statistic=float(stat),
            p_value=float(p),
            significant=p < self.ALPHA,
            effect_size=cohens_d,
            effect_interpretation=effect_interp,
            group1_name=group1,
            group2_name=group2,
            n1=len(g1_data),
            n2=len(g2_data)
        )

    # --- Multiple Group Comparisons ---

    def compare_multiple_groups(self,
                               column: str,
                               group_by: str) -> Tuple[StatisticalTestResult, Optional[pd.DataFrame]]:
        """
        Compare multiple groups using ANOVA or Kruskal-Wallis.

        Args:
            column: Metric to compare
            group_by: Grouping column

        Returns:
            (omnibus_result, post_hoc_dataframe if significant)
        """
        groups = []
        group_names = []

        for name, group_df in self.data.groupby(group_by):
            values = group_df[column].dropna().values
            if len(values) >= 3:
                groups.append(values)
                group_names.append(str(name))

        if len(groups) < 2:
            logger.warning("Less than 2 groups with sufficient data")
            return None, None

        # Check normality for all groups
        all_normal = all(
            stats.shapiro(g)[1] > self.ALPHA for g in groups if len(g) >= 3
        )

        # Check variance homogeneity
        if all_normal:
            _, levene_p = stats.levene(*groups)
            equal_var = levene_p > self.ALPHA
        else:
            equal_var = False

        if all_normal and equal_var:
            # One-way ANOVA
            stat, p = stats.f_oneway(*groups)
            test_name = "One-way ANOVA"
        else:
            # Kruskal-Wallis H test (non-parametric)
            stat, p = stats.kruskal(*groups)
            test_name = "Kruskal-Wallis H"

        omnibus_result = StatisticalTestResult(
            test_name=test_name,
            statistic=float(stat),
            p_value=float(p),
            significant=p < self.ALPHA
        )

        # Post-hoc tests if omnibus is significant
        post_hoc = None
        if p < self.ALPHA:
            post_hoc = self._post_hoc_tests(groups, group_names, all_normal)

        return omnibus_result, post_hoc

    def _post_hoc_tests(self,
                       groups: List[np.ndarray],
                       names: List[str],
                       parametric: bool) -> pd.DataFrame:
        """Perform pairwise post-hoc tests with Bonferroni correction."""
        results = []
        n_comparisons = len(groups) * (len(groups) - 1) // 2
        adjusted_alpha = self.ALPHA / n_comparisons  # Bonferroni correction

        for i in range(len(groups)):
            for j in range(i + 1, len(groups)):
                if parametric:
                    stat, p = stats.ttest_ind(groups[i], groups[j])
                    test = "t-test"
                else:
                    stat, p = stats.mannwhitneyu(groups[i], groups[j], alternative='two-sided')
                    test = "Mann-Whitney U"

                # Effect size
                cohens_d = self._cohens_d(groups[i], groups[j])

                results.append({
                    'Group 1': names[i],
                    'Group 2': names[j],
                    'Test': test,
                    'Statistic': round(stat, 4),
                    'p-value': round(p, 6),
                    'p-adjusted': round(min(p * n_comparisons, 1.0), 6),
                    'Significant': p < adjusted_alpha,
                    'Cohen_d': round(cohens_d, 3),
                    'Effect': self._interpret_cohens_d(cohens_d)
                })

        return pd.DataFrame(results)

    # --- Effect Size Calculations ---

    def _cohens_d(self, group1: np.ndarray, group2: np.ndarray) -> float:
        """Calculate Cohen's d effect size."""
        n1, n2 = len(group1), len(group2)

        if n1 < 2 or n2 < 2:
            return 0.0

        var1 = np.var(group1, ddof=1)
        var2 = np.var(group2, ddof=1)

        # Pooled standard deviation
        pooled_std = np.sqrt(((n1 - 1) * var1 + (n2 - 1) * var2) / (n1 + n2 - 2))

        if pooled_std == 0:
            return 0.0

        return float((np.mean(group1) - np.mean(group2)) / pooled_std)

    def _interpret_cohens_d(self, d: float) -> str:
        """Interpret Cohen's d effect size magnitude."""
        d = abs(d)
        if d < 0.2:
            return "negligible"
        elif d < 0.5:
            return "small"
        elif d < 0.8:
            return "medium"
        else:
            return "large"

    # --- Correlation Analysis ---

    def correlation_matrix(self,
                          columns: Optional[List[str]] = None) -> pd.DataFrame:
        """Calculate correlation matrix for metrics."""
        if columns is None:
            columns = [c for c in self.data.columns
                      if self.data[c].dtype in ['float64', 'int64']
                      and c not in ['run_id']]

        return self.data[columns].corr()

    def correlation_with_significance(self,
                                     col1: str,
                                     col2: str) -> Tuple[float, float]:
        """Calculate Pearson correlation with p-value."""
        valid = self.data[[col1, col2]].dropna()
        if len(valid) < 3:
            return 0.0, 1.0

        r, p = stats.pearsonr(valid[col1], valid[col2])
        return float(r), float(p)

    # --- Report Generation ---

    def generate_comparison_report(self,
                                  metric: str,
                                  comparisons: List[Tuple[str, str, str]]) -> pd.DataFrame:
        """
        Generate comparison report for multiple pairs.

        Args:
            metric: Metric to compare
            comparisons: List of (group_by, group1, group2) tuples

        Returns:
            DataFrame with comparison results
        """
        results = []

        for group_by, g1, g2 in comparisons:
            result = self.compare_two_groups(metric, group_by, g1, g2)
            results.append({
                'Comparison': f"{g1} vs {g2}",
                'Metric': metric,
                'Test': result.test_name,
                'Statistic': round(result.statistic, 4),
                'p-value': round(result.p_value, 6),
                'Significant': "Yes" if result.significant else "No",
                'Effect Size': result.effect_size,
                'Effect': result.effect_interpretation,
                'n1': result.n1,
                'n2': result.n2
            })

        return pd.DataFrame(results)

    def generate_full_analysis(self,
                              metrics: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Generate comprehensive statistical analysis.

        Returns dictionary with:
        - strategy_comparison: Simple vs CoT comparison
        - context_comparison: Interface vs Interface+Doc vs Full comparison
        - model_comparison: All models comparison
        - correlation_matrix: Metric correlations
        """
        if metrics is None:
            metrics = ['statement_coverage', 'branch_coverage',
                      'mutation_score', 'overall_quality_score']

        results = {
            'metrics_analyzed': metrics,
            'alpha': self.ALPHA,
            'strategy_comparisons': {},
            'context_comparisons': {},
            'model_comparisons': {}
        }

        # Strategy comparisons
        strategies = self.data['strategy'].unique()
        if len(strategies) >= 2:
            for metric in metrics:
                if metric in self.data.columns:
                    result = self.compare_two_groups(
                        metric, 'strategy',
                        strategies[0], strategies[1]
                    )
                    results['strategy_comparisons'][metric] = result.to_dict()

        # Context comparisons (multiple groups)
        for metric in metrics:
            if metric in self.data.columns:
                omnibus, posthoc = self.compare_multiple_groups(metric, 'context')
                if omnibus:
                    results['context_comparisons'][metric] = {
                        'omnibus': omnibus.to_dict(),
                        'post_hoc': posthoc.to_dict('records') if posthoc is not None else None
                    }

        # Model comparisons (multiple groups)
        for metric in metrics:
            if metric in self.data.columns:
                omnibus, posthoc = self.compare_multiple_groups(metric, 'model')
                if omnibus:
                    results['model_comparisons'][metric] = {
                        'omnibus': omnibus.to_dict(),
                        'post_hoc': posthoc.to_dict('records') if posthoc is not None else None
                    }

        return results


# Example usage
if __name__ == "__main__":
    import sys
    from pathlib import Path

    logging.basicConfig(level=logging.INFO)

    # Example with mock data
    np.random.seed(42)
    n = 30

    mock_data = pd.DataFrame({
        'model': ['model_a'] * n + ['model_b'] * n,
        'strategy': (['simple'] * 15 + ['cot'] * 15) * 2,
        'context': (['interface'] * 10 + ['docstring'] * 10 + ['full'] * 10) * 2,
        'statement_coverage': np.random.normal(85, 10, n * 2),
        'mutation_score': np.random.normal(70, 15, n * 2),
    })

    analyzer = StatisticalAnalyzer(mock_data)

    print("Porownanie strategii (Pokrycie instrukcji):")
    result = analyzer.compare_two_groups('statement_coverage', 'strategy', 'simple', 'cot')
    print(result)

    print("\nPorownanie kontekstow (Wiele grup):")
    omnibus, posthoc = analyzer.compare_multiple_groups('statement_coverage', 'context')
    print(f"Test omnibus: {omnibus}")
    if posthoc is not None:
        print(f"Testy post-hoc:\n{posthoc}")

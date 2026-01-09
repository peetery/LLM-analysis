"""
Reporting module for LLM test generation analysis.

This module provides comprehensive tools for:
- Multi-dimensional data aggregation (R1)
- Statistical analysis with significance tests (R2)
- Publication-quality chart generation (R3)
- LaTeX table export (R4)
- Automatic report building (R5)

Usage:
    from reporting import (
        MultiDimensionalAggregator,
        StatisticalAnalyzer,
        ThesisChartGenerator,
        LaTeXTableGenerator,
        ThesisReportBuilder
    )
"""

from .data_aggregator import (
    MultiDimensionalAggregator,
    AggregatedMetrics,
    ExperimentConfig
)
from .statistical_analyzer import (
    StatisticalAnalyzer,
    StatisticalTestResult
)
from .chart_generator import ThesisChartGenerator
from .latex_exporter import LaTeXTableGenerator
from .report_builder import ThesisReportBuilder

__all__ = [
    'MultiDimensionalAggregator',
    'AggregatedMetrics',
    'ExperimentConfig',
    'StatisticalAnalyzer',
    'StatisticalTestResult',
    'ThesisChartGenerator',
    'LaTeXTableGenerator',
    'ThesisReportBuilder',
]

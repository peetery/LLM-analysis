"""
Generator wykresow do pracy inzynierskiej.

Modul tworzy rozne typy wykresow:
- Boxploty (wizualizacja rozkladu)
- Heatmapy (porownania 2D)
- Wykresy radarowe (porownanie wielowymiarowe)
- Wykresy slupkowe z przedzialami ufnosci
- Wykresy liniowe (trendy)
- Wykresy skrzypcowe (szczegoly rozkladu)
- Zbiorcze wykresy wielopanelowe

Faza R3 systemu raportowania.
"""

import logging
from pathlib import Path
from typing import List, Dict, Optional, Tuple, Union

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import pandas as pd

try:
    import seaborn as sns
    HAS_SEABORN = True
except ImportError:
    HAS_SEABORN = False
    logging.warning("Seaborn niedostepny, niektore wykresy moga byc ograniczone")

logger = logging.getLogger(__name__)


class ThesisChartGenerator:
    """
    Generator wykresow publikacyjnych do pracy inzynierskiej.

    Funkcjonalnosci:
    - Spojny styl wszystkich wykresow
    - Palety przyjazne dla daltonistow
    - Eksport w wielu formatach (PDF, PNG, SVG)
    - Wymiary odpowiednie do pracy dyplomowej
    """

    # Kolor domyslny dla wykresow gdzie rozroznienie kolorami nie ma znaczenia
    DEFAULT_COLOR = '#2E86AB'

    COLORS = {
        'claude-code-opus-4.5': '#2E86AB',
        'claude-code-sonnet-4.5': '#A23B72',
        'claude-code-opus-4.1': '#F18F01',
        'gemini-3-pro': '#C73E1D',
        'gemini-3-flash': '#3B1F2B',
        'gemini-2.5-pro': '#95C623',
        'gemini-2.5-flash': '#7B2D26',
    }

    STRATEGY_COLORS = {
        'simple_prompting': '#2E86AB',
        'chain_of_thought_prompting': '#C73E1D'
    }

    CONTEXT_COLORS = {
        'interface': '#2E86AB',
        'interface_docstring': '#F18F01',
        'full_context': '#95C623'
    }

    CONTEXT_ORDER = ['interface', 'interface_docstring', 'full_context']

    METRIC_NAMES_PL = {
        'statement_coverage': 'Pokrycie instrukcji',
        'branch_coverage': 'Pokrycie rozgałęzień',
        'mutation_score': 'Wynik mutacyjny',
        'test_success_rate': 'Wskaźnik sukcesu testów',
        'total_test_methods': 'Liczba metod testowych',
        'total_assertions': 'Liczba asercji',
        'overall_quality_score': 'Ogólny wynik jakości',
        'response_time': 'Czas odpowiedzi',
        'assertion_quality_score': 'Jakość asercji',
        'naming_quality_score': 'Jakość nazewnictwa',
        'independence_score': 'Niezależność testów',
        'avg_assertions_per_test': 'Średnia asercji na test',
        'average_test_length': 'Średnia długość testu'
    }

    STRATEGY_NAMES_PL = {
        'simple_prompting': 'Strategia jednokrokowa',
        'chain_of_thought_prompting': 'Strategia wielokrokowa'
    }

    CONTEXT_NAMES_PL = {
        'interface': 'Interfejs',
        'interface_docstring': 'Interfejs + Docstring',
        'full_context': 'Pełny kontekst'
    }

    def __init__(self,
                 output_dir: Path,
                 style_file: Optional[Path] = None,
                 figsize: Tuple[float, float] = (6.5, 4.0)):
        """
        Inicjalizacja generatora wykresow.

        Args:
            output_dir: Katalog do zapisu wykresow
            style_file: Opcjonalny plik stylu matplotlib
            figsize: Domyslny rozmiar figury (szerokosc, wysokosc) w calach
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.figsize = figsize

        # Utworz podkatalogi dla formatow
        for fmt in ['png', 'pdf', 'svg']:
            (self.output_dir / fmt).mkdir(exist_ok=True)

        # Zaladuj styl
        if style_file and style_file.exists():
            plt.style.use(str(style_file))
        else:
            self._set_default_style()

        if HAS_SEABORN:
            sns.set_palette("colorblind")

    def _set_default_style(self) -> None:
        """Ustawia domyslny styl matplotlib dla wykresow."""
        plt.rcParams.update({
            'font.size': 10,
            'font.family': 'serif',
            'axes.labelsize': 10,
            'axes.titlesize': 11,
            'axes.titleweight': 'bold',
            'legend.fontsize': 9,
            'xtick.labelsize': 9,
            'ytick.labelsize': 9,
            'figure.figsize': self.figsize,
            'figure.dpi': 150,
            'figure.facecolor': 'white',
            'axes.facecolor': 'white',
            'axes.spines.top': False,
            'axes.spines.right': False,
            'axes.grid': True,
            'grid.alpha': 0.3,
            'grid.linestyle': '--',
            'savefig.dpi': 300,
            'savefig.bbox': 'tight',
            'savefig.pad_inches': 0.1,
        })

    def _save_figure(self,
                    fig: plt.Figure,
                    name: str,
                    formats: List[str] = None) -> List[Path]:
        """Zapisuje figure w wielu formatach."""
        if formats is None:
            formats = ['pdf', 'png']

        saved_paths = []
        for fmt in formats:
            path = self.output_dir / fmt / f"{name}.{fmt}"
            # PNG z przezroczystym tlem, PDF z bialym
            if fmt == 'png':
                fig.savefig(path, format=fmt, dpi=300, bbox_inches='tight',
                           facecolor='none', edgecolor='none', transparent=True)
            else:
                fig.savefig(path, format=fmt, dpi=300, bbox_inches='tight',
                           facecolor='white', edgecolor='none')
            saved_paths.append(path)
            logger.info(f"Zapisano: {path}")

        plt.close(fig)
        return saved_paths

    def _get_model_color(self, model: str) -> str:
        """Pobiera kolor dla modelu."""
        return self.COLORS.get(model, '#888888')

    def _format_metric_name(self, metric: str) -> str:
        """Formatuje nazwe metryki po polsku."""
        return self.METRIC_NAMES_PL.get(metric, metric.replace('_', ' ').title())

    def _format_strategy_name(self, strategy: str) -> str:
        """Formatuje nazwe strategii po polsku."""
        return self.STRATEGY_NAMES_PL.get(strategy, strategy)

    def _format_context_name(self, context: str) -> str:
        """Formatuje nazwe kontekstu po polsku."""
        return self.CONTEXT_NAMES_PL.get(context, context)

    # ========================================
    # BOXPLOTY
    # ========================================

    def boxplot_by_model(self,
                        df: pd.DataFrame,
                        metric: str,
                        title: Optional[str] = None,
                        ylabel: Optional[str] = None,
                        show_points: bool = True) -> plt.Figure:
        """
        Tworzy boxplot rozkladu metryki dla kazdego modelu.
        Uzywa jednego koloru dla wszystkich modeli (nazwy sa na osi X).
        """
        fig, ax = plt.subplots(figsize=(8, 5))

        # Kolejnosc modeli wg sredniej (malejaco)
        order = df.groupby('model')[metric].mean().sort_values(ascending=False).index.tolist()

        if HAS_SEABORN:
            sns.boxplot(
                data=df,
                x='model',
                y=metric,
                order=order,
                color=self.DEFAULT_COLOR,
                ax=ax,
                width=0.6,
                linewidth=1
            )

            if show_points:
                sns.stripplot(
                    data=df,
                    x='model',
                    y=metric,
                    order=order,
                    color='black',
                    alpha=0.3,
                    size=3,
                    ax=ax
                )
        else:
            data_by_model = [df[df['model'] == m][metric].dropna().values for m in order]
            bp = ax.boxplot(data_by_model, patch_artist=True)
            for patch in bp['boxes']:
                patch.set_facecolor(self.DEFAULT_COLOR)
            ax.set_xticklabels(order)

        ax.set_xlabel('')
        ax.set_ylabel(ylabel or self._format_metric_name(metric))
        ax.set_title(title or f'Rozkład {self._format_metric_name(metric)} wg modelu')

        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()

        self._save_figure(fig, f'boxplot_{metric}_by_model')
        return fig

    def boxplot_by_strategy(self,
                           df: pd.DataFrame,
                           metric: str,
                           split_by_model: bool = True,
                           title: Optional[str] = None) -> plt.Figure:
        """
        Tworzy boxplot porownujacy strategie promptowania.
        """
        if split_by_model:
            fig, ax = plt.subplots(figsize=(10, 5))

            if HAS_SEABORN:
                sns.boxplot(
                    data=df,
                    x='model',
                    y=metric,
                    hue='strategy',
                    palette=self.STRATEGY_COLORS,
                    ax=ax
                )
            plt.xticks(rotation=45, ha='right')
            ax.legend(title='Strategia', loc='upper right',
                     labels=[self._format_strategy_name(s) for s in df['strategy'].unique()])
        else:
            fig, ax = plt.subplots(figsize=(6, 5))

            if HAS_SEABORN:
                sns.boxplot(
                    data=df,
                    x='strategy',
                    y=metric,
                    palette=self.STRATEGY_COLORS,
                    ax=ax
                )
            ax.set_xticklabels([self._format_strategy_name(s) for s in df['strategy'].unique()])

        ax.set_ylabel(self._format_metric_name(metric))
        ax.set_xlabel('')
        ax.set_title(title or f'{self._format_metric_name(metric)}: porównanie strategii')

        plt.tight_layout()
        self._save_figure(fig, f'boxplot_{metric}_by_strategy')
        return fig

    def boxplot_by_context(self,
                          df: pd.DataFrame,
                          metric: str,
                          split_by_model: bool = True,
                          title: Optional[str] = None) -> plt.Figure:
        """
        Tworzy boxplot porownujacy poziomy kontekstu.
        """
        if split_by_model:
            fig, ax = plt.subplots(figsize=(10, 5))

            if HAS_SEABORN:
                sns.boxplot(
                    data=df,
                    x='model',
                    y=metric,
                    hue='context',
                    hue_order=self.CONTEXT_ORDER,
                    palette=self.CONTEXT_COLORS,
                    ax=ax
                )
            plt.xticks(rotation=45, ha='right')
            # Pobierz handles i ustaw polskie etykiety zachowujac kolory
            handles, _ = ax.get_legend_handles_labels()
            ax.legend(handles, [self._format_context_name(c) for c in self.CONTEXT_ORDER],
                     title='Poziom kontekstu', loc='upper center',
                     bbox_to_anchor=(0.5, -0.40), ncol=3)
            plt.subplots_adjust(bottom=0.35)
        else:
            fig, ax = plt.subplots(figsize=(6, 5))

            if HAS_SEABORN:
                sns.boxplot(
                    data=df,
                    x='context',
                    y=metric,
                    order=self.CONTEXT_ORDER,
                    palette=self.CONTEXT_COLORS,
                    ax=ax
                )
            ax.set_xticklabels([self._format_context_name(c) for c in self.CONTEXT_ORDER])

        ax.set_ylabel(self._format_metric_name(metric))
        ax.set_xlabel('')
        ax.set_title(title or f'{self._format_metric_name(metric)} wg poziomu kontekstu')

        plt.tight_layout()
        self._save_figure(fig, f'boxplot_{metric}_by_context')
        return fig

    # ========================================
    # HEATMAPY
    # ========================================

    def heatmap_model_vs_strategy(self,
                                  df: pd.DataFrame,
                                  metric: str,
                                  show_values: bool = True,
                                  title: Optional[str] = None) -> plt.Figure:
        """
        Tworzy heatmape: modele vs strategie.
        """
        pivot = df.pivot_table(
            values=metric,
            index='model',
            columns='strategy',
            aggfunc='mean'
        )

        # Zmien nazwy kolumn na polskie
        pivot.columns = [self._format_strategy_name(c) for c in pivot.columns]

        fig, ax = plt.subplots(figsize=(6, 5))

        if HAS_SEABORN:
            sns.heatmap(
                pivot,
                annot=show_values,
                fmt='.1f',
                cmap='RdYlGn',
                center=pivot.values.mean(),
                ax=ax,
                cbar_kws={'label': self._format_metric_name(metric)},
                linewidths=0.5
            )
        else:
            im = ax.imshow(pivot.values, cmap='RdYlGn', aspect='auto')
            plt.colorbar(im, ax=ax, label=self._format_metric_name(metric))
            ax.set_xticks(range(len(pivot.columns)))
            ax.set_yticks(range(len(pivot.index)))
            ax.set_xticklabels(pivot.columns)
            ax.set_yticklabels(pivot.index)

        ax.set_title(title or f'{self._format_metric_name(metric)}: Model x Strategia')
        ax.set_xlabel('Strategia')
        ax.set_ylabel('Model')

        plt.tight_layout()
        self._save_figure(fig, f'heatmap_{metric}_model_strategy')
        return fig

    def heatmap_model_vs_context(self,
                                 df: pd.DataFrame,
                                 metric: str,
                                 title: Optional[str] = None) -> plt.Figure:
        """
        Tworzy heatmape: modele vs poziomy kontekstu.
        """
        pivot = df.pivot_table(
            values=metric,
            index='model',
            columns='context',
            aggfunc='mean'
        )

        # Zmien kolejnosc i nazwy kolumn
        pivot = pivot.reindex(columns=[c for c in self.CONTEXT_ORDER if c in pivot.columns])
        pivot.columns = [self._format_context_name(c) for c in pivot.columns]

        fig, ax = plt.subplots(figsize=(7, 5))

        if HAS_SEABORN:
            sns.heatmap(
                pivot,
                annot=True,
                fmt='.1f',
                cmap='RdYlGn',
                ax=ax,
                cbar_kws={'label': self._format_metric_name(metric)},
                linewidths=0.5
            )

        ax.set_title(title or f'{self._format_metric_name(metric)}: Model x Kontekst')

        plt.tight_layout()
        self._save_figure(fig, f'heatmap_{metric}_model_context')
        return fig

    def heatmap_all_metrics(self,
                           df: pd.DataFrame,
                           group_by: str = 'model',
                           title: Optional[str] = None) -> plt.Figure:
        """
        Tworzy heatmape wszystkich glownych metryk.
        """
        metrics = ['statement_coverage', 'branch_coverage', 'mutation_score',
                  'test_success_rate', 'overall_quality_score']
        metrics = [m for m in metrics if m in df.columns]

        # Agregacja
        agg_df = df.groupby(group_by)[metrics].mean()

        # Normalizacja do 0-100
        normalized = (agg_df - agg_df.min()) / (agg_df.max() - agg_df.min()) * 100

        fig, ax = plt.subplots(figsize=(8, 6))

        if HAS_SEABORN:
            annot_values = agg_df.round(1).values
            annot_str = [[f'{v:.1f}' for v in row] for row in annot_values]

            sns.heatmap(
                normalized,
                annot=annot_str,
                fmt='',
                cmap='RdYlGn',
                ax=ax,
                cbar_kws={'label': 'Wynik znormalizowany'},
                linewidths=0.5
            )

        # Polskie etykiety metryk
        ax.set_xticklabels([self._format_metric_name(m) for m in metrics], rotation=45, ha='right')
        group_name_pl = {'model': 'modelu', 'strategy': 'strategii', 'context': 'kontekstu'}
        ax.set_title(title or f'Wszystkie metryki wg {group_name_pl.get(group_by, group_by)}')

        plt.tight_layout()
        self._save_figure(fig, f'heatmap_all_metrics_by_{group_by}')
        return fig

    # ========================================
    # WYKRESY RADAROWE
    # ========================================

    def radar_chart_models(self,
                          df: pd.DataFrame,
                          models: Optional[List[str]] = None,
                          title: Optional[str] = None) -> plt.Figure:
        """
        Tworzy wykres radarowy porownujacy modele.
        """
        metrics = ['statement_coverage', 'branch_coverage', 'mutation_score',
                  'test_success_rate', 'overall_quality_score']
        metrics = [m for m in metrics if m in df.columns]

        if models is None:
            models = df['model'].unique().tolist()[:5]

        # Agregacja wartosci
        values_dict = {}
        for model in models:
            model_df = df[df['model'] == model]
            values_dict[model] = [model_df[m].mean() for m in metrics]

        # Normalizacja do 0-100
        max_vals = [df[m].max() for m in metrics]
        for model in values_dict:
            values_dict[model] = [v / max_vals[i] * 100 if max_vals[i] > 0 else 0
                                  for i, v in enumerate(values_dict[model])]

        # Wykres radarowy
        angles = np.linspace(0, 2 * np.pi, len(metrics), endpoint=False).tolist()
        angles += angles[:1]

        fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))

        for model in models:
            values = values_dict[model] + values_dict[model][:1]
            color = self._get_model_color(model)
            ax.plot(angles, values, 'o-', linewidth=2, label=model, color=color)
            ax.fill(angles, values, alpha=0.1, color=color)

        # Etykiety po polsku
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels([self._format_metric_name(m) for m in metrics])
        ax.set_ylim(0, 100)

        ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.0), title='Model')
        ax.set_title(title or 'Porównanie modeli wg metryk', y=1.08)

        plt.tight_layout()
        self._save_figure(fig, 'radar_chart_models')
        return fig

    # ========================================
    # WYKRESY SLUPKOWE Z PRZEDZIALAMI UFNOSCI
    # ========================================

    def bar_chart_with_ci(self,
                         df: pd.DataFrame,
                         metric: str,
                         group_by: str,
                         title: Optional[str] = None) -> plt.Figure:
        """
        Tworzy wykres slupkowy z 95% przedzialem ufnosci.
        """
        # Oblicz średnia i CI
        agg = df.groupby(group_by)[metric].agg(['mean', 'std', 'count'])
        agg['ci'] = 1.96 * agg['std'] / np.sqrt(agg['count'])
        agg = agg.sort_values('mean', ascending=False)

        fig, ax = plt.subplots(figsize=(8, 5))

        # Jeden kolor dla wszystkich slupkow - nazwy kategorii sa na osi X,
        # wiec rozroznienie kolorami nie ma znaczenia i moze wprowadzac w blad
        colors = self.DEFAULT_COLOR

        bars = ax.bar(
            range(len(agg)),
            agg['mean'],
            yerr=agg['ci'],
            capsize=5,
            color=colors,
            edgecolor='black',
            linewidth=0.5,
            error_kw={'linewidth': 1}
        )

        ax.set_xticks(range(len(agg)))

        # Formatuj etykiety wg typu grupowania
        if group_by == 'strategy':
            labels = [self._format_strategy_name(x) for x in agg.index]
        elif group_by == 'context':
            labels = [self._format_context_name(x) for x in agg.index]
        else:
            labels = agg.index

        ax.set_xticklabels(labels, rotation=45, ha='right')
        ax.set_ylabel(self._format_metric_name(metric))

        group_name_pl = {'model': 'modelu', 'strategy': 'strategii', 'context': 'kontekstu'}
        ax.set_title(title or f'{self._format_metric_name(metric)} wg {group_name_pl.get(group_by, group_by)} (95% CI)')

        # Dodaj wartosci nad slupkami
        for i, (idx, row) in enumerate(agg.iterrows()):
            ax.text(i, row['mean'] + row['ci'] + 1,
                   f"{row['mean']:.1f}", ha='center', va='bottom', fontsize=8)

        plt.tight_layout()
        self._save_figure(fig, f'bar_{metric}_by_{group_by}_ci')
        return fig

    # ========================================
    # WYKRESY LINIOWE (TRENDY)
    # ========================================

    def line_plot_context_progression(self,
                                     df: pd.DataFrame,
                                     metric: str,
                                     models: Optional[List[str]] = None,
                                     title: Optional[str] = None) -> plt.Figure:
        """
        Tworzy wykres liniowy pokazujacy zmiane metryki wg poziomu kontekstu.
        """
        if models is None:
            models = df['model'].unique().tolist()

        fig, ax = plt.subplots(figsize=(8, 5))

        for model in models:
            model_df = df[df['model'] == model]
            means = []
            stds = []

            for ctx in self.CONTEXT_ORDER:
                ctx_df = model_df[model_df['context'] == ctx]
                if len(ctx_df) > 0:
                    means.append(ctx_df[metric].mean())
                    stds.append(ctx_df[metric].std())
                else:
                    means.append(np.nan)
                    stds.append(0)

            color = self._get_model_color(model)
            ax.errorbar(
                range(len(self.CONTEXT_ORDER)),
                means,
                yerr=stds,
                marker='o',
                label=model,
                capsize=4,
                color=color,
                linewidth=1.5
            )

        ax.set_xticks(range(len(self.CONTEXT_ORDER)))
        ax.set_xticklabels([self._format_context_name(c) for c in self.CONTEXT_ORDER])
        ax.set_ylabel(self._format_metric_name(metric))
        ax.set_xlabel('Poziom kontekstu')
        ax.set_title(title or f'{self._format_metric_name(metric)} vs poziom kontekstu')
        ax.legend(bbox_to_anchor=(1.02, 1), loc='upper left', title='Model')

        plt.tight_layout()
        self._save_figure(fig, f'line_{metric}_context_progression')
        return fig

    # ========================================
    # WYKRESY SKRZYPCOWE
    # ========================================

    def violin_plot_comparison(self,
                              df: pd.DataFrame,
                              metric: str,
                              compare_by: str,
                              title: Optional[str] = None) -> plt.Figure:
        """
        Tworzy wykres skrzypcowy pokazujacy pelny rozklad.
        """
        fig, ax = plt.subplots(figsize=(8, 5))

        if compare_by == 'strategy':
            palette = self.STRATEGY_COLORS
            order = None
            use_single_color = False
        elif compare_by == 'context':
            palette = self.CONTEXT_COLORS
            order = self.CONTEXT_ORDER
            use_single_color = False
        else:
            # Dla modeli uzywamy jednego koloru - nazwy sa na osi X
            palette = None
            order = None
            use_single_color = True

        if HAS_SEABORN:
            if use_single_color:
                sns.violinplot(
                    data=df,
                    x=compare_by,
                    y=metric,
                    color=self.DEFAULT_COLOR,
                    order=order,
                    ax=ax,
                    inner='box'
                )
            else:
                sns.violinplot(
                    data=df,
                    x=compare_by,
                    y=metric,
                    palette=palette,
                    order=order,
                    ax=ax,
                    inner='box'
                )

        ax.set_xlabel('')
        ax.set_ylabel(self._format_metric_name(metric))

        # Formatuj etykiety
        if compare_by == 'strategy':
            ax.set_xticklabels([self._format_strategy_name(s) for s in df['strategy'].unique()])
            compare_name_pl = 'strategii'
        elif compare_by == 'context':
            ax.set_xticklabels([self._format_context_name(c) for c in self.CONTEXT_ORDER])
            compare_name_pl = 'kontekstu'
        else:
            compare_name_pl = 'modelu'
            plt.xticks(rotation=45, ha='right')

        ax.set_title(title or f'Rozkład {self._format_metric_name(metric)} wg {compare_name_pl}')

        plt.tight_layout()
        self._save_figure(fig, f'violin_{metric}_by_{compare_by}')
        return fig

    # ========================================
    # ZBIORCZA FIGURA WIELOPANELOWA
    # ========================================

    def create_summary_figure(self,
                             df: pd.DataFrame,
                             title: Optional[str] = None) -> plt.Figure:
        """
        Tworzy zbiorcza figure 4-panelowa - idealna na pelna strone pracy.
        """
        fig = plt.figure(figsize=(12, 10))
        gs = fig.add_gridspec(2, 2, hspace=0.3, wspace=0.3)

        # 1. Pokrycie wg modelu (slupki + CI)
        ax1 = fig.add_subplot(gs[0, 0])
        if 'statement_coverage' in df.columns:
            agg = df.groupby('model')['statement_coverage'].agg(['mean', 'std', 'count'])
            agg['ci'] = 1.96 * agg['std'] / np.sqrt(agg['count'])
            agg = agg.sort_values('mean', ascending=False)

            ax1.bar(range(len(agg)), agg['mean'], yerr=agg['ci'], capsize=3,
                   color=self.DEFAULT_COLOR, edgecolor='black', linewidth=0.5)
            ax1.set_xticks(range(len(agg)))
            short_names = [m.split('-')[-1] if '-' in m else m for m in agg.index]
            ax1.set_xticklabels(short_names, rotation=45, ha='right')
            ax1.set_ylabel('Pokrycie instrukcji (%)')
            ax1.set_title('A) Pokrycie wg modelu')

        # 2. Wynik mutacji wg strategii (boxplot)
        ax2 = fig.add_subplot(gs[0, 1])
        if 'mutation_score' in df.columns and HAS_SEABORN:
            sns.boxplot(data=df, x='strategy', y='mutation_score',
                       palette=self.STRATEGY_COLORS, ax=ax2)
            ax2.set_xticklabels(['Jednokrokowa', 'Wielokrokowa'])
            ax2.set_ylabel('Wynik mutacyjny (%)')
            ax2.set_xlabel('')
            ax2.set_title('B) Wynik mutacyjny wg strategii')

        # 3. Heatmapa model vs kontekst
        ax3 = fig.add_subplot(gs[1, 0])
        if 'overall_quality_score' in df.columns and HAS_SEABORN:
            pivot = df.pivot_table(values='overall_quality_score',
                                  index='model', columns='context', aggfunc='mean')
            pivot = pivot.reindex(columns=[c for c in self.CONTEXT_ORDER if c in pivot.columns])
            pivot.columns = [self._format_context_name(c) for c in pivot.columns]
            sns.heatmap(pivot, annot=True, fmt='.1f', cmap='RdYlGn',
                       ax=ax3, cbar=False, linewidths=0.5)
            ax3.set_title('C) Wynik jakości: Model x Kontekst')

        # 4. Skrzypce - rozklad liczby testow
        ax4 = fig.add_subplot(gs[1, 1])
        if 'total_test_methods' in df.columns and HAS_SEABORN:
            available_contexts = [c for c in self.CONTEXT_ORDER if c in df['context'].values]
            sns.violinplot(data=df, x='context', y='total_test_methods',
                          palette=self.CONTEXT_COLORS, ax=ax4, inner='box',
                          order=available_contexts)
            ax4.set_xticklabels([self._format_context_name(c) for c in available_contexts])
            ax4.set_ylabel('Liczba wygenerowanych testów')
            ax4.set_xlabel('')
            ax4.set_title('D) Liczba testów wg kontekstu')

        if title:
            fig.suptitle(title, fontsize=14, fontweight='bold', y=1.02)

        plt.tight_layout()
        self._save_figure(fig, 'summary_figure_4panel')
        return fig

    # ========================================
    # GENEROWANIE WSZYSTKICH WYKRESOW
    # ========================================

    def generate_all_figures(self, df: pd.DataFrame) -> Dict[str, List[Path]]:
        """
        Generuje wszystkie wykresy do pracy.
        """
        saved_figures = {}

        logger.info("Generowanie wykresow do pracy...")

        # Wykresy porownania modeli
        logger.info("[6.3.2] Wykresy porownania modeli...")
        if 'statement_coverage' in df.columns:
            self.boxplot_by_model(df, 'statement_coverage',
                                 title='Rozkład pokrycia instrukcji wg modelu',
                                 ylabel='Pokrycie (%)')

        if 'mutation_score' in df.columns:
            self.boxplot_by_model(df, 'mutation_score',
                                 title='Rozkład wyniku mutacji wg modelu')

        if 'overall_quality_score' in df.columns:
            self.bar_chart_with_ci(df, 'overall_quality_score', 'model',
                                  title='Ogólny wynik jakości wg modelu (95% CI)')

        self.radar_chart_models(df)

        # Wykresy porownania strategii
        logger.info("[6.3.3] Wykresy porownania strategii...")
        if 'statement_coverage' in df.columns:
            self.boxplot_by_strategy(df, 'statement_coverage', split_by_model=True)

        if 'mutation_score' in df.columns:
            self.boxplot_by_strategy(df, 'mutation_score', split_by_model=False)

        if 'total_test_methods' in df.columns:
            self.violin_plot_comparison(df, 'total_test_methods', 'strategy')

        # Wykresy poziomu kontekstu
        logger.info("[6.3.4] Wykresy poziomu kontekstu...")
        if 'statement_coverage' in df.columns:
            self.boxplot_by_context(df, 'statement_coverage', split_by_model=True)

        if 'mutation_score' in df.columns:
            self.line_plot_context_progression(df, 'mutation_score')

        if 'overall_quality_score' in df.columns:
            self.heatmap_model_vs_context(df, 'overall_quality_score')

        # Wykresy zbiorcze
        logger.info("[6.3.1] Wykresy zbiorcze...")
        self.heatmap_all_metrics(df, 'model')
        self.create_summary_figure(df)

        # Dodatkowe wykresy
        logger.info("[Dodatkowe] Wykresy dodatkowe...")
        if 'mutation_score' in df.columns:
            self.heatmap_model_vs_strategy(df, 'mutation_score')

        if 'response_time' in df.columns:
            self.violin_plot_comparison(df, 'response_time', 'model')

        logger.info(f"Wszystkie wykresy zapisane do: {self.output_dir}")
        return saved_figures


# CLI
if __name__ == "__main__":
    import sys
    from pathlib import Path
    from data_aggregator import MultiDimensionalAggregator

    logging.basicConfig(level=logging.INFO)

    if len(sys.argv) > 1:
        results_dir = Path(sys.argv[1])
    else:
        results_dir = Path("cli_results")

    output_dir = Path("reporting/outputs/figures")

    if not results_dir.exists():
        print(f"Blad: Katalog wynikow nie istnieje: {results_dir}")
        sys.exit(1)

    print(f"Ladowanie wynikow z: {results_dir}")
    agg = MultiDimensionalAggregator(results_dir)
    df = agg.to_dataframe()

    print(f"Generowanie wykresow do: {output_dir}")
    charts = ThesisChartGenerator(output_dir)
    charts.generate_all_figures(df)

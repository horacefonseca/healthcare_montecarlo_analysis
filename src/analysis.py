"""
Statistical Analysis Module for Monte Carlo Healthcare Simulations
Provides comprehensive analysis and visualization functions
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, List, Tuple, Optional
from scipy import stats


class HealthcareAnalyzer:
    """Comprehensive analysis tools for healthcare simulation results"""

    def __init__(self):
        """Initialize the analyzer with plotting defaults"""
        sns.set_style("whitegrid")
        plt.rcParams['figure.figsize'] = (12, 8)
        plt.rcParams['font.size'] = 10

    def generate_summary_statistics(self, results_df: pd.DataFrame) -> Dict:
        """
        Generate comprehensive summary statistics from simulation results

        Args:
            results_df: DataFrame with simulation results

        Returns:
            Dictionary with summary statistics
        """
        summary = {
            'total_patients': len(results_df),
            'treatments': {
                'distribution': results_df['treatment'].value_counts().to_dict(),
                'success_rates': {}
            },
            'overall_metrics': {
                'mean_success_rate': results_df['probability_of_success'].mean(),
                'mean_complication_rate': results_df['probability_of_complications'].mean(),
                'high_risk_patients': (results_df['baseline_severity'] > 70).sum(),
                'low_risk_patients': (results_df['baseline_severity'] < 30).sum()
            }
        }

        # Calculate success rates by treatment
        for treatment in results_df['treatment'].unique():
            treatment_data = results_df[results_df['treatment'] == treatment]
            summary['treatments']['success_rates'][treatment] = {
                'mean': treatment_data['probability_of_success'].mean(),
                'std': treatment_data['probability_of_success'].std(),
                'median': treatment_data['probability_of_success'].median()
            }

        return summary

    def compare_treatments_analysis(self, results_df: pd.DataFrame) -> pd.DataFrame:
        """
        Compare treatment effectiveness across different metrics

        Args:
            results_df: DataFrame with simulation results

        Returns:
            DataFrame with comparative analysis
        """
        comparison = []

        for treatment in results_df['treatment'].unique():
            treatment_data = results_df[results_df['treatment'] == treatment]

            comparison.append({
                'Treatment': treatment,
                'N_Patients': len(treatment_data),
                'Mean_Success_Rate': treatment_data['probability_of_success'].mean(),
                'Mean_Complication_Rate': treatment_data['probability_of_complications'].mean(),
                'Mean_Recovery_Days': treatment_data['recovery_time'].apply(lambda x: x['mean']).mean(),
                'Mean_Severity_Reduction': treatment_data['severity_reduction'].apply(lambda x: x['mean']).mean(),
                'Success_Rate_Std': treatment_data['probability_of_success'].std()
            })

        comparison_df = pd.DataFrame(comparison)
        comparison_df = comparison_df.sort_values('Mean_Success_Rate', ascending=False)

        return comparison_df

    def risk_stratification_analysis(self, results_df: pd.DataFrame) -> Dict:
        """
        Analyze outcomes by risk stratification

        Args:
            results_df: DataFrame with simulation results

        Returns:
            Dictionary with risk-stratified analysis
        """
        # Define risk categories
        results_df['risk_category'] = pd.cut(
            results_df['baseline_severity'],
            bins=[0, 30, 50, 70, 100],
            labels=['Low', 'Moderate', 'High', 'Very High']
        )

        risk_analysis = {}

        for category in ['Low', 'Moderate', 'High', 'Very High']:
            category_data = results_df[results_df['risk_category'] == category]

            if len(category_data) > 0:
                risk_analysis[category] = {
                    'n_patients': len(category_data),
                    'mean_success_rate': category_data['probability_of_success'].mean(),
                    'mean_complication_rate': category_data['probability_of_complications'].mean(),
                    'mean_recovery_time': category_data['recovery_time'].apply(lambda x: x['mean']).mean(),
                    'mean_baseline_severity': category_data['baseline_severity'].mean()
                }

        return risk_analysis

    def confidence_interval_analysis(
        self,
        results_df: pd.DataFrame,
        metric: str = 'probability_of_success',
        confidence_level: float = 0.95
    ) -> pd.DataFrame:
        """
        Calculate confidence intervals for success rates by treatment

        Args:
            results_df: DataFrame with simulation results
            metric: Metric to analyze
            confidence_level: Confidence level for intervals

        Returns:
            DataFrame with confidence intervals
        """
        ci_results = []

        for treatment in results_df['treatment'].unique():
            treatment_data = results_df[results_df['treatment'] == treatment][metric]

            mean = treatment_data.mean()
            std_err = treatment_data.sem()
            ci = stats.t.interval(confidence_level, len(treatment_data) - 1, mean, std_err)

            ci_results.append({
                'Treatment': treatment,
                'Mean': mean,
                'Lower_CI': ci[0],
                'Upper_CI': ci[1],
                'Margin_of_Error': (ci[1] - ci[0]) / 2
            })

        return pd.DataFrame(ci_results)

    def generate_visualization_report(
        self,
        results_df: pd.DataFrame,
        output_path: Optional[str] = None
    ) -> plt.Figure:
        """
        Generate comprehensive visualization report

        Args:
            results_df: DataFrame with simulation results
            output_path: Optional path to save the figure

        Returns:
            Matplotlib figure object
        """
        fig = plt.figure(figsize=(16, 12))
        gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)

        # 1. Treatment Success Rates
        ax1 = fig.add_subplot(gs[0, 0])
        treatment_success = results_df.groupby('treatment')['probability_of_success'].mean().sort_values()
        treatment_success.plot(kind='barh', ax=ax1, color='steelblue')
        ax1.set_xlabel('Mean Success Rate')
        ax1.set_title('Success Rate by Treatment')
        ax1.set_xlim(0, 1)

        # 2. Complication Rates
        ax2 = fig.add_subplot(gs[0, 1])
        complication_rates = results_df.groupby('treatment')['probability_of_complications'].mean().sort_values()
        complication_rates.plot(kind='barh', ax=ax2, color='coral')
        ax2.set_xlabel('Mean Complication Rate')
        ax2.set_title('Complication Rate by Treatment')
        ax2.set_xlim(0, 0.5)

        # 3. Recovery Time Distribution
        ax3 = fig.add_subplot(gs[0, 2])
        recovery_times = results_df['recovery_time'].apply(lambda x: x['mean'])
        for treatment in results_df['treatment'].unique():
            treatment_data = results_df[results_df['treatment'] == treatment]
            recovery = treatment_data['recovery_time'].apply(lambda x: x['mean'])
            ax3.hist(recovery, alpha=0.5, label=treatment, bins=20)
        ax3.set_xlabel('Recovery Time (days)')
        ax3.set_ylabel('Frequency')
        ax3.set_title('Recovery Time Distribution')
        ax3.legend()

        # 4. Severity Reduction by Treatment
        ax4 = fig.add_subplot(gs[1, 0])
        severity_data = []
        treatments = []
        for treatment in results_df['treatment'].unique():
            treatment_data = results_df[results_df['treatment'] == treatment]
            severity_reductions = treatment_data['severity_reduction'].apply(lambda x: x['mean'])
            severity_data.append(severity_reductions)
            treatments.append(treatment)
        ax4.boxplot(severity_data, labels=treatments)
        ax4.set_ylabel('Severity Reduction')
        ax4.set_title('Severity Reduction by Treatment')
        ax4.tick_params(axis='x', rotation=45)

        # 5. Success Rate vs Baseline Severity
        ax5 = fig.add_subplot(gs[1, 1])
        scatter_colors = {'Standard Care': 'blue', 'Intensive Therapy': 'green', 'Experimental Treatment': 'red'}
        for treatment in results_df['treatment'].unique():
            treatment_data = results_df[results_df['treatment'] == treatment]
            ax5.scatter(
                treatment_data['baseline_severity'],
                treatment_data['probability_of_success'],
                alpha=0.5,
                label=treatment,
                color=scatter_colors.get(treatment, 'gray')
            )
        ax5.set_xlabel('Baseline Severity')
        ax5.set_ylabel('Probability of Success')
        ax5.set_title('Success Rate vs Initial Severity')
        ax5.legend()

        # 6. Risk Stratification
        ax6 = fig.add_subplot(gs[1, 2])
        results_df['risk_category'] = pd.cut(
            results_df['baseline_severity'],
            bins=[0, 30, 50, 70, 100],
            labels=['Low', 'Moderate', 'High', 'Very High']
        )
        risk_success = results_df.groupby('risk_category')['probability_of_success'].mean()
        risk_success.plot(kind='bar', ax=ax6, color='teal')
        ax6.set_xlabel('Risk Category')
        ax6.set_ylabel('Mean Success Rate')
        ax6.set_title('Success Rate by Risk Category')
        ax6.tick_params(axis='x', rotation=45)

        # 7. Treatment Comparison Heatmap
        ax7 = fig.add_subplot(gs[2, :2])
        comparison_metrics = []
        for treatment in results_df['treatment'].unique():
            treatment_data = results_df[results_df['treatment'] == treatment]
            comparison_metrics.append({
                'Success Rate': treatment_data['probability_of_success'].mean(),
                'Complication Rate': treatment_data['probability_of_complications'].mean(),
                'Recovery Time': treatment_data['recovery_time'].apply(lambda x: x['mean']).mean() / 100,
                'Severity Reduction': treatment_data['severity_reduction'].apply(lambda x: x['mean']).mean() / 100
            })
        heatmap_df = pd.DataFrame(comparison_metrics, index=results_df['treatment'].unique())
        sns.heatmap(heatmap_df.T, annot=True, fmt='.3f', cmap='RdYlGn', ax=ax7, cbar_kws={'label': 'Score'})
        ax7.set_title('Treatment Comparison Heatmap (Normalized Metrics)')

        # 8. Success Rate Distribution
        ax8 = fig.add_subplot(gs[2, 2])
        ax8.hist(results_df['probability_of_success'], bins=30, color='skyblue', edgecolor='black')
        ax8.axvline(results_df['probability_of_success'].mean(), color='red', linestyle='--', label='Mean')
        ax8.axvline(results_df['probability_of_success'].median(), color='green', linestyle='--', label='Median')
        ax8.set_xlabel('Probability of Success')
        ax8.set_ylabel('Number of Patients')
        ax8.set_title('Overall Success Rate Distribution')
        ax8.legend()

        plt.suptitle('Healthcare Monte Carlo Simulation - Comprehensive Analysis Report', fontsize=16, y=0.995)

        if output_path:
            plt.savefig(output_path, dpi=300, bbox_inches='tight')

        return fig

    def export_detailed_report(
        self,
        results_df: pd.DataFrame,
        output_path: str
    ) -> None:
        """
        Export detailed analysis report to CSV

        Args:
            results_df: DataFrame with simulation results
            output_path: Path to save the CSV report
        """
        # Create detailed report
        report_data = []

        for idx, row in results_df.iterrows():
            report_data.append({
                'Patient_ID': row['patient_id'],
                'Treatment': row['treatment'],
                'Baseline_Severity': row['baseline_severity'],
                'Mean_Final_Severity': row['final_severity']['mean'],
                'Median_Final_Severity': row['final_severity']['median'],
                'Mean_Severity_Reduction': row['severity_reduction']['mean'],
                'P5_Severity_Reduction': row['severity_reduction']['percentile_5'],
                'P95_Severity_Reduction': row['severity_reduction']['percentile_95'],
                'Mean_Recovery_Days': row['recovery_time']['mean'],
                'Median_Recovery_Days': row['recovery_time']['median'],
                'P90_Recovery_Days': row['recovery_time']['percentile_90'],
                'Success_Probability': row['probability_of_success'],
                'Complication_Probability': row['probability_of_complications'],
                'Expected_Efficacy': row['expected_efficacy']
            })

        report_df = pd.DataFrame(report_data)
        report_df.to_csv(output_path, index=False)
        print(f"Detailed report exported to: {output_path}")


if __name__ == "__main__":
    print("=" * 80)
    print("Healthcare Analysis Module - Test Run")
    print("=" * 80)
    print("\nThis module provides comprehensive analysis tools for Monte Carlo simulations.")
    print("Import this module in your main application to access analysis functions.")

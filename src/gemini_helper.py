"""
Helper functions for Gemini AI integration and report generation
"""

import streamlit as st
import pandas as pd


def create_gemini_button_with_report(report_text: str, stage_name: str):
    """
    Creates a Gemini button with copy-to-clipboard functionality

    Args:
        report_text: Structured report text (max 500 chars)
        stage_name: Name of the analysis stage
    """
    # Ensure report is max 500 characters
    if len(report_text) > 500:
        report_text = report_text[:497] + "..."

    col1, col2 = st.columns([3, 1])

    with col1:
        # Copy button with report text (built-in copy button for mobile)
        st.markdown("📋 **Copy this summary to ask Gemini:**")
        st.code(report_text, language=None)

    with col2:
        st.markdown("### Ask Gemini")
        st.markdown(
            """
            <a href="https://gemini.google.com/app" target="_blank">
                <img src="https://www.gstatic.com/lamda/images/gemini_sparkle_v002_d4735304ff6292a690345.svg"
                     width="40" height="40" style="vertical-align: middle;">
                <br>
                <button style="
                    background-color: #4285f4;
                    color: white;
                    padding: 10px 20px;
                    border: none;
                    border-radius: 5px;
                    cursor: pointer;
                    font-size: 14px;
                    margin-top: 10px;
                ">Ask Gemini</button>
            </a>
            """,
            unsafe_allow_html=True
        )
        st.caption("Copy text above, then click to open Gemini")


def generate_patient_report(df: pd.DataFrame) -> str:
    """Generate structured report for patient generation stage"""
    report = f"""HEALTHCARE PATIENT DATA SUMMARY
Total: {len(df)} patients
Age: Mean {df['age'].mean():.0f}, Range {df['age'].min():.0f}-{df['age'].max():.0f}
Severity: Mean {df['severity_score'].mean():.1f}/10
Comorbidities: Mean {df['num_comorbidities'].mean():.1f}
Top Conditions: {', '.join(df['condition'].value_counts().head(3).index.tolist())}

Question: What insights can you provide about this patient dataset?"""

    return report[:500]


def generate_simulation_report(results_df: pd.DataFrame, params: dict) -> str:
    """Generate structured report for simulation results"""
    overall_success = results_df['success_rate'].mean() * 100
    overall_improvement = results_df['quality_improvement'].mean()

    # Handle cost structure
    if 'total_cost' in results_df.columns:
        cost_values = results_df['total_cost'].apply(lambda x: x['mean'] if isinstance(x, dict) else x)
        mean_cost = cost_values.mean()
    else:
        mean_cost = 0

    report = f"""MONTE CARLO SIMULATION RESULTS
Simulations: {params.get('num_simulations', 10000):,} per patient
Time Horizon: {params.get('time_horizon', 365)} days
Sample Size: {params.get('sample_size', 100)} patients

OVERALL METRICS:
Success Rate: {overall_success:.1f}%
Quality Improvement: {overall_improvement:.1f} points
Mean Total Cost: ${mean_cost:,.0f}

Question: What do these results tell about treatment effectiveness?"""

    return report[:500]


def generate_analysis_report(stats: dict) -> str:
    """Generate structured report for comprehensive analysis"""
    report = f"""HEALTHCARE TREATMENT ANALYSIS
Total Treatments: {stats.get('total_treatments', 0)}
Overall Success Rate: {stats.get('overall_success', 0):.1f}%
Mean Quality Improvement: {stats.get('mean_improvement', 0):.1f} points

TREATMENT COMPARISON:
"""

    if 'treatment_comparison' in stats:
        for treatment, metrics in list(stats['treatment_comparison'].items())[:3]:
            report += f"{treatment}: {metrics.get('success', 0):.0f}% success, ${metrics.get('cost', 0):,.0f} cost\n"

    report += "\nQuestion: Which treatment option is most effective?"

    return report[:500]


def generate_single_patient_report(patient: dict, results: dict) -> str:
    """Generate structured report for single patient analysis"""
    report = f"""PATIENT PROFILE & RESULTS
Age: {patient.get('age', 0):.0f} years
Severity: {patient.get('severity_score', 0):.1f}/10
Comorbidities: {patient.get('num_comorbidities', 0)}
Condition: {patient.get('condition', 'N/A')}

TREATMENT RESULTS:
"""

    for treatment, metrics in list(results.items())[:3]:
        success = metrics.get('success_rate', 0) * 100
        improvement = metrics.get('mean_improvement', 0)
        report += f"{treatment}: {success:.0f}% success, {improvement:.1f} improvement\n"

    report += f"\nRecommended: {results.get('recommended_treatment', 'N/A')}\n"
    report += "Question: What should this patient do and why?"

    return report[:500]


def add_sensitivity_sliders():
    """Add parameter sensitivity adjustment sliders to sidebar"""
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🔧 Adjust Assumptions")

    treatment_efficacy = st.sidebar.slider(
        "Treatment Efficacy Baseline",
        min_value=50.0,
        max_value=95.0,
        value=75.0,
        step=2.5,
        format="%.1f%%",
        help="Baseline treatment success rate assumption"
    )

    treatment_cost_factor = st.sidebar.slider(
        "Treatment Cost Factor",
        min_value=0.5,
        max_value=2.0,
        value=1.0,
        step=0.1,
        format="%.1fx",
        help="Multiplier for treatment costs (1.0 = baseline)"
    )

    complication_rate = st.sidebar.slider(
        "Complication Rate",
        min_value=1.0,
        max_value=20.0,
        value=5.0,
        step=1.0,
        format="%.0f%%",
        help="Expected rate of treatment complications"
    )

    recovery_time_factor = st.sidebar.slider(
        "Recovery Time Factor",
        min_value=0.5,
        max_value=2.0,
        value=1.0,
        step=0.1,
        format="%.1fx",
        help="Multiplier for expected recovery times"
    )

    return {
        'treatment_efficacy': treatment_efficacy / 100,
        'treatment_cost_factor': treatment_cost_factor,
        'complication_rate': complication_rate / 100,
        'recovery_time_factor': recovery_time_factor
    }


def interpret_results_locally(success_rate: float, improvement: float, treatment: str, severity: float) -> str:
    """
    Local rule-based interpretation when AI is not available
    """
    if success_rate > 80:
        risk_level = "✅ HIGH SUCCESS"
        interpretation = f"{success_rate:.0f}% success rate indicates excellent outcomes. "
        interpretation += f"Quality improvement of {improvement:.1f} points is substantial. "
        interpretation += "This treatment is highly recommended for this patient profile."

    elif success_rate > 60:
        risk_level = "✅ MODERATE SUCCESS"
        interpretation = f"{success_rate:.0f}% success rate shows positive outcomes. "
        interpretation += f"Expected improvement: {improvement:.1f} points. "
        interpretation += "Benefits likely outweigh risks for most patients."

    elif success_rate > 40:
        risk_level = "⚠️ UNCERTAIN"
        interpretation = f"{success_rate:.0f}% success rate indicates mixed outcomes. "
        interpretation += "Consider alternative treatments or additional risk mitigation. "
        if severity > 7:
            interpretation += "High severity may require more aggressive intervention."

    else:
        risk_level = "⚠️ LOW SUCCESS"
        interpretation = f"{success_rate:.0f}% success rate is concerning. "
        interpretation += "Recommend exploring alternative treatments or second opinions. "
        interpretation += "Benefits may not outweigh risks for this patient."

    return f"**{risk_level}**: {interpretation}"

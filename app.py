"""
Healthcare Treatment Outcome Analyzer
Monte Carlo Simulation Web Application

A comprehensive Streamlit application for simulating and analyzing
healthcare treatment outcomes using Monte Carlo methods.
"""

import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sys
from pathlib import Path

# Add src directory to path
sys.path.append(str(Path(__file__).parent / 'src'))

from data_generator import HealthcareDataGenerator
from monte_carlo_simulator import MonteCarloHealthcareSimulator
from analysis import HealthcareAnalyzer


# Page configuration
st.set_page_config(
    page_title="Healthcare Monte Carlo Analyzer",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    .stAlert {
        padding: 1rem;
        margin: 1rem 0;
    }
    h1 {
        color: #1f77b4;
    }
    h2 {
        color: #2ca02c;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    </style>
""", unsafe_allow_html=True)


# Initialize session state
if 'patients_df' not in st.session_state:
    st.session_state.patients_df = None
if 'simulation_results' not in st.session_state:
    st.session_state.simulation_results = None
if 'selected_patient' not in st.session_state:
    st.session_state.selected_patient = None


def main():
    """Main application function"""

    # Header
    st.title("🏥 Healthcare Treatment Outcome Analyzer")
    st.markdown("""
    ### Monte Carlo Simulation for Evidence-Based Treatment Planning

    This application uses Monte Carlo simulation to quantify uncertainty in treatment outcomes,
    helping healthcare professionals make data-driven decisions with confidence intervals and risk assessments.
    """)

    # Sidebar
    with st.sidebar:
        st.header("⚙️ Configuration")

        app_mode = st.radio(
            "Select Mode",
            ["📊 Generate Patient Data", "🎲 Run Simulations", "📈 Analyze Results", "🔬 Single Patient Analysis"],
            index=0
        )

        st.divider()

        st.markdown("""
        ### About
        This tool implements:
        - Synthetic patient data generation
        - Monte Carlo treatment simulation
        - Statistical risk assessment
        - Comparative treatment analysis

        **Developed for academic research and clinical decision support.**
        """)

    # Main content based on selected mode
    if app_mode == "📊 Generate Patient Data":
        generate_patient_data_page()

    elif app_mode == "🎲 Run Simulations":
        run_simulations_page()

    elif app_mode == "📈 Analyze Results":
        analyze_results_page()

    elif app_mode == "🔬 Single Patient Analysis":
        single_patient_analysis_page()


def generate_patient_data_page():
    """Page for generating patient cohort data"""

    st.header("📊 Generate Patient Cohort")

    col1, col2 = st.columns(2)

    with col1:
        n_patients = st.slider(
            "Number of Base Patients",
            min_value=50,
            max_value=5000,
            value=1000,
            step=50,
            help="Number of patients to generate in the base population"
        )

        amplify = st.checkbox(
            "Enable Synthetic Data Amplification",
            value=True,
            help="Add synthetic edge cases to improve model robustness"
        )

    with col2:
        if amplify:
            amplification_factor = st.slider(
                "Amplification Factor",
                min_value=0.1,
                max_value=0.5,
                value=0.3,
                step=0.05,
                help="Proportion of synthetic patients to add (focuses on edge cases)"
            )
        else:
            amplification_factor = 0.0

        random_seed = st.number_input(
            "Random Seed",
            min_value=0,
            max_value=9999,
            value=42,
            help="Set seed for reproducible results"
        )

    if st.button("🔄 Generate Patient Data", type="primary"):
        with st.spinner("Generating patient cohort..."):
            generator = HealthcareDataGenerator(random_seed=random_seed)
            patients_df = generator.generate_patient_cohort(
                n_patients=n_patients,
                amplify=amplify,
                amplification_factor=amplification_factor
            )

            st.session_state.patients_df = patients_df
            st.success(f"✅ Successfully generated {len(patients_df)} patients!")

    # Display patient data if available
    if st.session_state.patients_df is not None:
        df = st.session_state.patients_df

        st.subheader("Patient Cohort Summary")

        # Summary metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Patients", len(df))
        with col2:
            st.metric("Mean Age", f"{df['age'].mean():.1f}")
        with col3:
            st.metric("Mean BMI", f"{df['bmi'].mean():.1f}")
        with col4:
            st.metric("Mean Severity", f"{df['baseline_severity'].mean():.1f}")

        # Distribution charts
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Disease Distribution")
            disease_counts = df['disease'].value_counts()
            fig1, ax1 = plt.subplots(figsize=(8, 6))
            disease_counts.plot(kind='bar', ax=ax1, color='steelblue')
            ax1.set_xlabel('Disease Type')
            ax1.set_ylabel('Number of Patients')
            ax1.set_title('Patient Distribution by Disease')
            plt.xticks(rotation=45, ha='right')
            st.pyplot(fig1)

        with col2:
            st.subheader("Treatment Distribution")
            treatment_counts = df['treatment'].value_counts()
            fig2, ax2 = plt.subplots(figsize=(8, 6))
            treatment_counts.plot(kind='bar', ax=ax2, color='coral')
            ax2.set_xlabel('Treatment Type')
            ax2.set_ylabel('Number of Patients')
            ax2.set_title('Patient Distribution by Treatment')
            plt.xticks(rotation=45, ha='right')
            st.pyplot(fig2)

        # Data table
        st.subheader("Patient Data Preview")
        st.dataframe(
            df.head(20),
            use_container_width=True,
            height=400
        )

        # Download option
        csv = df.to_csv(index=False)
        st.download_button(
            label="📥 Download Patient Data (CSV)",
            data=csv,
            file_name="patient_cohort.csv",
            mime="text/csv"
        )


def run_simulations_page():
    """Page for running Monte Carlo simulations"""

    st.header("🎲 Run Monte Carlo Simulations")

    if st.session_state.patients_df is None:
        st.warning("⚠️ Please generate patient data first!")
        return

    df = st.session_state.patients_df

    col1, col2 = st.columns(2)

    with col1:
        num_simulations = st.select_slider(
            "Number of Simulations per Patient",
            options=[1000, 5000, 10000, 20000, 50000],
            value=10000,
            help="More simulations = more accurate results but slower"
        )

        sample_size = st.slider(
            "Sample Size (for faster testing)",
            min_value=10,
            max_value=min(500, len(df)),
            value=min(100, len(df)),
            help="Simulate a subset of patients for faster results"
        )

    with col2:
        st.info(f"""
        **Simulation Parameters:**
        - Total patients: {len(df)}
        - Patients to simulate: {sample_size}
        - Simulations per patient: {num_simulations:,}
        - Total simulations: {sample_size * num_simulations:,}

        Estimated time: ~{sample_size * num_simulations / 50000:.1f} minutes
        """)

    if st.button("▶️ Run Simulations", type="primary"):
        with st.spinner("Running Monte Carlo simulations... This may take a few minutes."):
            simulator = MonteCarloHealthcareSimulator(random_seed=42)

            # Progress bar
            progress_bar = st.progress(0)
            status_text = st.empty()

            # Run simulations
            results_df = simulator.simulate_cohort(
                df,
                num_simulations=num_simulations,
                sample_size=sample_size
            )

            progress_bar.progress(100)
            status_text.text("Simulations complete!")

            st.session_state.simulation_results = results_df
            st.success(f"✅ Successfully simulated {len(results_df)} patients!")

    # Display simulation results if available
    if st.session_state.simulation_results is not None:
        results = st.session_state.simulation_results

        st.subheader("Simulation Results Summary")

        # Summary metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric(
                "Mean Success Rate",
                f"{results['probability_of_success'].mean()*100:.1f}%"
            )
        with col2:
            st.metric(
                "Mean Complication Rate",
                f"{results['probability_of_complications'].mean()*100:.1f}%"
            )
        with col3:
            mean_recovery = results['recovery_time'].apply(lambda x: x['mean']).mean()
            st.metric(
                "Mean Recovery Time",
                f"{mean_recovery:.0f} days"
            )
        with col4:
            mean_reduction = results['severity_reduction'].apply(lambda x: x['mean']).mean()
            st.metric(
                "Mean Severity Reduction",
                f"{mean_reduction:.1f} points"
            )

        st.subheader("Results Preview")
        st.dataframe(
            results[['patient_id', 'treatment', 'baseline_severity',
                    'probability_of_success', 'probability_of_complications']].head(20),
            use_container_width=True
        )


def analyze_results_page():
    """Page for analyzing simulation results"""

    st.header("📈 Comprehensive Results Analysis")

    if st.session_state.simulation_results is None:
        st.warning("⚠️ Please run simulations first!")
        return

    results = st.session_state.simulation_results
    analyzer = HealthcareAnalyzer()

    # Generate summary statistics
    summary = analyzer.generate_summary_statistics(results)

    st.subheader("📊 Overall Statistics")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Patients Analyzed", summary['total_patients'])
        st.metric("High-Risk Patients", summary['overall_metrics']['high_risk_patients'])
    with col2:
        st.metric("Overall Success Rate", f"{summary['overall_metrics']['mean_success_rate']*100:.1f}%")
        st.metric("Low-Risk Patients", summary['overall_metrics']['low_risk_patients'])
    with col3:
        st.metric("Overall Complication Rate", f"{summary['overall_metrics']['mean_complication_rate']*100:.1f}%")

    # Treatment comparison
    st.subheader("🏆 Treatment Comparison")
    comparison_df = analyzer.compare_treatments_analysis(results)
    st.dataframe(comparison_df.style.format({
        'Mean_Success_Rate': '{:.2%}',
        'Mean_Complication_Rate': '{:.2%}',
        'Mean_Recovery_Days': '{:.1f}',
        'Mean_Severity_Reduction': '{:.1f}',
        'Success_Rate_Std': '{:.3f}'
    }), use_container_width=True)

    # Risk stratification
    st.subheader("🎯 Risk Stratification Analysis")
    risk_analysis = analyzer.risk_stratification_analysis(results)

    risk_df = pd.DataFrame(risk_analysis).T
    st.dataframe(risk_df.style.format({
        'n_patients': '{:.0f}',
        'mean_success_rate': '{:.2%}',
        'mean_complication_rate': '{:.2%}',
        'mean_recovery_time': '{:.1f}',
        'mean_baseline_severity': '{:.1f}'
    }), use_container_width=True)

    # Visualizations
    st.subheader("📊 Comprehensive Visualization Report")
    with st.spinner("Generating visualizations..."):
        fig = analyzer.generate_visualization_report(results)
        st.pyplot(fig)

    # Export options
    st.subheader("💾 Export Results")
    col1, col2 = st.columns(2)

    with col1:
        if st.button("📥 Download Detailed Report (CSV)"):
            import io
            buffer = io.StringIO()

            report_data = []
            for idx, row in results.iterrows():
                report_data.append({
                    'Patient_ID': row['patient_id'],
                    'Treatment': row['treatment'],
                    'Baseline_Severity': row['baseline_severity'],
                    'Success_Probability': row['probability_of_success'],
                    'Complication_Probability': row['probability_of_complications'],
                })

            report_df = pd.DataFrame(report_data)
            csv = report_df.to_csv(index=False)

            st.download_button(
                label="Download CSV",
                data=csv,
                file_name="simulation_results.csv",
                mime="text/csv"
            )


def single_patient_analysis_page():
    """Page for analyzing a single patient with treatment comparison"""

    st.header("🔬 Single Patient Treatment Analysis")

    if st.session_state.patients_df is None:
        st.warning("⚠️ Please generate patient data first!")
        return

    df = st.session_state.patients_df

    st.markdown("""
    Analyze a specific patient and compare all treatment options using Monte Carlo simulation.
    This provides personalized treatment recommendations based on patient characteristics.
    """)

    # Patient selection
    patient_id = st.selectbox(
        "Select Patient ID",
        options=df['patient_id'].tolist(),
        index=0
    )

    patient = df[df['patient_id'] == patient_id].iloc[0]

    # Display patient information
    st.subheader("👤 Patient Information")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Age", f"{patient['age']} years")
        st.metric("Gender", patient['gender'])
    with col2:
        st.metric("BMI", f"{patient['bmi']:.1f}")
        st.metric("Disease", patient['disease'])
    with col3:
        st.metric("Systolic BP", f"{patient['baseline_systolic']:.0f}")
        st.metric("Diastolic BP", f"{patient['baseline_diastolic']:.0f}")
    with col4:
        st.metric("Glucose", f"{patient['baseline_glucose']:.0f}")
        st.metric("HbA1c", f"{patient['baseline_hba1c']:.2f}")

    st.metric("Baseline Severity Score", f"{patient['baseline_severity']:.1f}/100")

    # Simulation parameters
    num_simulations = st.select_slider(
        "Number of Simulations",
        options=[1000, 5000, 10000, 20000],
        value=10000
    )

    if st.button("🎲 Compare All Treatments", type="primary"):
        with st.spinner("Running comparative simulations..."):
            simulator = MonteCarloHealthcareSimulator(random_seed=42)
            comparison = simulator.compare_treatments(patient, num_simulations)

            # Display comparison results
            st.subheader("📊 Treatment Comparison Results")

            # Create comparison table
            comparison_data = []
            for treatment, result in comparison.items():
                comparison_data.append({
                    'Treatment': treatment,
                    'Success Rate': f"{result['probability_of_success']*100:.1f}%",
                    'Complication Rate': f"{result['probability_of_complications']*100:.1f}%",
                    'Mean Recovery (days)': f"{result['recovery_time']['mean']:.0f}",
                    'Median Recovery (days)': f"{result['recovery_time']['median']:.0f}",
                    '90% Confidence Recovery': f"{result['recovery_time']['percentile_90']:.0f}",
                    'Mean Severity Reduction': f"{result['severity_reduction']['mean']:.1f}"
                })

            comparison_df = pd.DataFrame(comparison_data)
            st.dataframe(comparison_df, use_container_width=True)

            # Visualizations
            col1, col2 = st.columns(2)

            with col1:
                st.subheader("Success Rates")
                success_rates = {k: v['probability_of_success'] for k, v in comparison.items()}
                fig1, ax1 = plt.subplots(figsize=(8, 6))
                plt.bar(success_rates.keys(), [v*100 for v in success_rates.values()], color='steelblue')
                plt.ylabel('Success Rate (%)')
                plt.title('Treatment Success Rates')
                plt.xticks(rotation=45, ha='right')
                plt.ylim(0, 100)
                st.pyplot(fig1)

            with col2:
                st.subheader("Recovery Time Distribution")
                fig2, ax2 = plt.subplots(figsize=(8, 6))
                recovery_data = []
                labels = []
                for treatment, result in comparison.items():
                    recovery_data.append([
                        result['recovery_time']['percentile_25'],
                        result['recovery_time']['percentile_50'],
                        result['recovery_time']['percentile_75']
                    ])
                    labels.append(treatment)

                x = np.arange(len(labels))
                width = 0.25

                for i, percentile in enumerate(['25th', '50th', '75th']):
                    values = [data[i] for data in recovery_data]
                    plt.bar(x + i*width, values, width, label=f'{percentile} Percentile')

                plt.xlabel('Treatment')
                plt.ylabel('Days')
                plt.title('Recovery Time by Percentile')
                plt.xticks(x + width, labels, rotation=45, ha='right')
                plt.legend()
                st.pyplot(fig2)

            # Recommendation
            st.subheader("🎯 Treatment Recommendation")

            best_treatment = max(comparison.items(), key=lambda x: x[1]['probability_of_success'])
            safest_treatment = min(comparison.items(), key=lambda x: x[1]['probability_of_complications'])
            fastest_treatment = min(comparison.items(), key=lambda x: x[1]['recovery_time']['median'])

            col1, col2, col3 = st.columns(3)

            with col1:
                st.success(f"""
                **Highest Success Rate**

                {best_treatment[0]}

                Success: {best_treatment[1]['probability_of_success']*100:.1f}%
                """)

            with col2:
                st.info(f"""
                **Lowest Complication Rate**

                {safest_treatment[0]}

                Complications: {safest_treatment[1]['probability_of_complications']*100:.1f}%
                """)

            with col3:
                st.warning(f"""
                **Fastest Recovery**

                {fastest_treatment[0]}

                Median: {fastest_treatment[1]['recovery_time']['median']:.0f} days
                """)


if __name__ == "__main__":
    main()

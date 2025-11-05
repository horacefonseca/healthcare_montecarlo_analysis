"""
Monte Carlo Simulator for Healthcare Treatment Outcomes
Simulates patient treatment responses using probabilistic models
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass


@dataclass
class TreatmentParameters:
    """Parameters for treatment simulation"""
    efficacy_mean: float  # Average treatment effectiveness (0-1)
    efficacy_std: float  # Standard deviation of effectiveness
    recovery_days_optimistic: int  # Best case recovery time
    recovery_days_likely: int  # Most likely recovery time
    recovery_days_pessimistic: int  # Worst case recovery time
    complication_rate: float  # Probability of complications (0-1)
    side_effect_severity: float  # Severity of side effects (0-10)


class MonteCarloHealthcareSimulator:
    """Monte Carlo simulation engine for healthcare treatment outcomes"""

    def __init__(self, random_seed: int = 42):
        """
        Initialize the simulator

        Args:
            random_seed: Random seed for reproducibility
        """
        np.random.seed(random_seed)

        # Define treatment parameters based on realistic medical scenarios
        self.treatment_params = {
            'Standard Care': TreatmentParameters(
                efficacy_mean=0.65,
                efficacy_std=0.15,
                recovery_days_optimistic=30,
                recovery_days_likely=60,
                recovery_days_pessimistic=120,
                complication_rate=0.10,
                side_effect_severity=2.5
            ),
            'Intensive Therapy': TreatmentParameters(
                efficacy_mean=0.78,
                efficacy_std=0.18,
                recovery_days_optimistic=20,
                recovery_days_likely=45,
                recovery_days_pessimistic=90,
                complication_rate=0.18,
                side_effect_severity=4.5
            ),
            'Experimental Treatment': TreatmentParameters(
                efficacy_mean=0.72,
                efficacy_std=0.22,
                recovery_days_optimistic=15,
                recovery_days_likely=40,
                recovery_days_pessimistic=100,
                complication_rate=0.25,
                side_effect_severity=5.5
            )
        }

    def simulate_treatment_outcome(
        self,
        patient: pd.Series,
        num_simulations: int = 10000
    ) -> Dict:
        """
        Run Monte Carlo simulation for a single patient's treatment outcome

        Args:
            patient: Patient data as pandas Series
            num_simulations: Number of Monte Carlo simulations to run

        Returns:
            Dictionary with simulation results
        """
        treatment = patient['treatment']
        baseline_severity = patient['baseline_severity']
        age = patient['age']
        bmi = patient['bmi']

        params = self.treatment_params[treatment]

        # Adjust efficacy based on patient characteristics
        age_penalty = (age - 50) * 0.002  # Slight decrease with age
        bmi_penalty = max(0, (bmi - 30) * 0.005)  # Penalty for obesity
        severity_penalty = (baseline_severity / 100) * 0.1  # Worse outcomes for severe cases

        adjusted_efficacy_mean = params.efficacy_mean - age_penalty - bmi_penalty - severity_penalty
        adjusted_efficacy_mean = np.clip(adjusted_efficacy_mean, 0.2, 0.95)

        # Arrays to store simulation results
        final_severity_reduction = np.zeros(num_simulations)
        recovery_times = np.zeros(num_simulations)
        complications = np.zeros(num_simulations, dtype=bool)
        success = np.zeros(num_simulations, dtype=bool)

        for sim in range(num_simulations):
            # Simulate treatment efficacy (beta distribution for bounded 0-1)
            alpha = adjusted_efficacy_mean * 10
            beta = (1 - adjusted_efficacy_mean) * 10
            efficacy = np.random.beta(alpha, beta)

            # Calculate severity reduction
            severity_reduction = baseline_severity * efficacy
            final_severity_reduction[sim] = severity_reduction

            # Simulate recovery time (triangular distribution)
            recovery_time = np.random.triangular(
                params.recovery_days_optimistic,
                params.recovery_days_likely,
                params.recovery_days_pessimistic
            )
            recovery_times[sim] = recovery_time

            # Simulate complications
            complication_prob = params.complication_rate * (1 + severity_penalty)
            complications[sim] = np.random.random() < complication_prob

            # Define success: severity reduced by at least 40% without complications
            success[sim] = (severity_reduction >= baseline_severity * 0.4) and not complications[sim]

        # Calculate final severity scores
        final_severity_scores = baseline_severity - final_severity_reduction

        # Compile results
        results = {
            'patient_id': patient['patient_id'],
            'treatment': treatment,
            'baseline_severity': baseline_severity,
            'simulations': num_simulations,
            'final_severity': {
                'mean': final_severity_scores.mean(),
                'median': np.median(final_severity_scores),
                'std': final_severity_scores.std(),
                'percentile_5': np.percentile(final_severity_scores, 5),
                'percentile_25': np.percentile(final_severity_scores, 25),
                'percentile_75': np.percentile(final_severity_scores, 75),
                'percentile_95': np.percentile(final_severity_scores, 95)
            },
            'severity_reduction': {
                'mean': final_severity_reduction.mean(),
                'median': np.median(final_severity_reduction),
                'std': final_severity_reduction.std(),
                'percentile_5': np.percentile(final_severity_reduction, 5),
                'percentile_25': np.percentile(final_severity_reduction, 25),
                'percentile_75': np.percentile(final_severity_reduction, 75),
                'percentile_95': np.percentile(final_severity_reduction, 95)
            },
            'recovery_time': {
                'mean': recovery_times.mean(),
                'median': np.median(recovery_times),
                'std': recovery_times.std(),
                'percentile_5': np.percentile(recovery_times, 5),
                'percentile_25': np.percentile(recovery_times, 25),
                'percentile_50': np.percentile(recovery_times, 50),
                'percentile_75': np.percentile(recovery_times, 75),
                'percentile_90': np.percentile(recovery_times, 90),
                'percentile_95': np.percentile(recovery_times, 95)
            },
            'probability_of_success': success.sum() / num_simulations,
            'probability_of_complications': complications.sum() / num_simulations,
            'expected_efficacy': adjusted_efficacy_mean,
            'side_effect_severity': params.side_effect_severity
        }

        return results

    def simulate_cohort(
        self,
        patients_df: pd.DataFrame,
        num_simulations: int = 10000,
        sample_size: Optional[int] = None
    ) -> pd.DataFrame:
        """
        Run Monte Carlo simulations for an entire patient cohort

        Args:
            patients_df: DataFrame with patient data
            num_simulations: Number of simulations per patient
            sample_size: If specified, randomly sample this many patients

        Returns:
            DataFrame with simulation results for all patients
        """
        if sample_size:
            patients_df = patients_df.sample(n=min(sample_size, len(patients_df)))

        results_list = []

        for idx, patient in patients_df.iterrows():
            result = self.simulate_treatment_outcome(patient, num_simulations)
            results_list.append(result)

        return pd.DataFrame(results_list)

    def compare_treatments(
        self,
        patient: pd.Series,
        num_simulations: int = 10000
    ) -> Dict:
        """
        Compare all treatment options for a single patient

        Args:
            patient: Patient data as pandas Series
            num_simulations: Number of simulations per treatment

        Returns:
            Dictionary with comparative results
        """
        comparison = {}

        for treatment in self.treatment_params.keys():
            # Create a modified patient with this treatment
            test_patient = patient.copy()
            test_patient['treatment'] = treatment

            # Run simulation
            result = self.simulate_treatment_outcome(test_patient, num_simulations)
            comparison[treatment] = result

        return comparison

    def calculate_var(
        self,
        baseline_severity: float,
        final_severity_array: np.ndarray,
        confidence_level: float = 0.95
    ) -> Dict:
        """
        Calculate Value at Risk (VaR) for treatment outcomes

        Args:
            baseline_severity: Initial severity score
            final_severity_array: Array of simulated final severity scores
            confidence_level: Confidence level for VaR calculation

        Returns:
            Dictionary with VaR metrics
        """
        percentile = (1 - confidence_level) * 100
        var_value = np.percentile(final_severity_array, 100 - percentile)
        improvement = baseline_severity - var_value

        return {
            'var_score': var_value,
            'confidence_level': confidence_level,
            'expected_improvement': improvement,
            'interpretation': f"With {confidence_level*100}% confidence, severity will decrease to at most {var_value:.1f}"
        }


if __name__ == "__main__":
    # Test the simulator
    from data_generator import HealthcareDataGenerator

    print("=" * 80)
    print("Monte Carlo Healthcare Simulator - Test Run")
    print("=" * 80)

    # Generate test patient
    generator = HealthcareDataGenerator(random_seed=42)
    patients = generator.generate_patient_cohort(n_patients=10, amplify=False)

    # Initialize simulator
    simulator = MonteCarloHealthcareSimulator(random_seed=42)

    # Test single patient simulation
    test_patient = patients.iloc[0]
    print(f"\nTesting single patient simulation:")
    print(f"Patient ID: {test_patient['patient_id']}")
    print(f"Age: {test_patient['age']}, BMI: {test_patient['bmi']}")
    print(f"Disease: {test_patient['disease']}")
    print(f"Treatment: {test_patient['treatment']}")
    print(f"Baseline Severity: {test_patient['baseline_severity']:.1f}")

    result = simulator.simulate_treatment_outcome(test_patient, num_simulations=10000)

    print(f"\nSimulation Results ({result['simulations']:,} simulations):")
    print(f"\nSeverity Reduction:")
    print(f"  Mean: {result['severity_reduction']['mean']:.1f}")
    print(f"  Median: {result['severity_reduction']['median']:.1f}")
    print(f"  5th-95th percentile: {result['severity_reduction']['percentile_5']:.1f} - {result['severity_reduction']['percentile_95']:.1f}")

    print(f"\nRecovery Time (days):")
    print(f"  Mean: {result['recovery_time']['mean']:.1f}")
    print(f"  Median: {result['recovery_time']['median']:.1f}")
    print(f"  50% confidence: {result['recovery_time']['percentile_50']:.1f} days")
    print(f"  90% confidence: {result['recovery_time']['percentile_90']:.1f} days")

    print(f"\nOutcome Probabilities:")
    print(f"  Success Rate: {result['probability_of_success']*100:.1f}%")
    print(f"  Complication Rate: {result['probability_of_complications']*100:.1f}%")

    print("\n" + "=" * 80)
    print("Test completed successfully!")

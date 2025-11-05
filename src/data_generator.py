"""
Healthcare Patient Data Generator with Synthetic Data Amplification
Generates realistic patient profiles for chronic disease treatment simulations
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple
from datetime import datetime, timedelta


class HealthcareDataGenerator:
    """Generate synthetic patient data with realistic correlations"""

    def __init__(self, random_seed: int = 42):
        """
        Initialize the data generator

        Args:
            random_seed: Random seed for reproducibility
        """
        np.random.seed(random_seed)
        self.diseases = ['Type 2 Diabetes', 'Hypertension', 'Both']
        self.treatments = ['Standard Care', 'Intensive Therapy', 'Experimental Treatment']

    def generate_base_population(self, n_patients: int = 1000) -> pd.DataFrame:
        """
        Generate base patient population with realistic characteristics

        Args:
            n_patients: Number of patients to generate

        Returns:
            DataFrame with patient characteristics
        """
        # Generate age with realistic distribution (skewed toward older adults)
        ages = np.random.gamma(shape=8, scale=7, size=n_patients) + 30
        ages = np.clip(ages, 30, 85).astype(int)

        # Generate gender
        genders = np.random.choice(['Male', 'Female'], size=n_patients, p=[0.48, 0.52])

        # Generate BMI with realistic correlation to age
        base_bmi = np.random.normal(28, 5, size=n_patients)
        age_factor = (ages - 50) * 0.05  # Slight increase with age
        bmi = base_bmi + age_factor
        bmi = np.clip(bmi, 18, 50)

        # Generate baseline blood pressure (correlated with BMI and age)
        systolic = 110 + (bmi - 25) * 1.2 + (ages - 50) * 0.3 + np.random.normal(0, 8, size=n_patients)
        systolic = np.clip(systolic, 90, 180)

        diastolic = 70 + (bmi - 25) * 0.6 + (ages - 50) * 0.15 + np.random.normal(0, 5, size=n_patients)
        diastolic = np.clip(diastolic, 60, 120)

        # Generate baseline glucose levels (correlated with BMI)
        glucose = 95 + (bmi - 25) * 1.5 + np.random.normal(0, 12, size=n_patients)
        glucose = np.clip(glucose, 70, 180)

        # Generate HbA1c (correlated with glucose)
        hba1c = 5.5 + (glucose - 100) * 0.015 + np.random.normal(0, 0.3, size=n_patients)
        hba1c = np.clip(hba1c, 4.5, 10)

        # Assign disease based on risk factors
        disease_risk = (bmi > 30).astype(int) + (systolic > 140).astype(int) + (glucose > 126).astype(int)
        disease_probs = np.clip(disease_risk / 6, 0.1, 0.8)
        diseases = []
        for prob in disease_probs:
            if prob > 0.6:
                diseases.append(np.random.choice(self.diseases, p=[0.3, 0.3, 0.4]))
            elif prob > 0.3:
                diseases.append(np.random.choice(self.diseases, p=[0.4, 0.4, 0.2]))
            else:
                diseases.append(np.random.choice(self.diseases, p=[0.5, 0.45, 0.05]))

        # Randomly assign treatments
        treatments = np.random.choice(self.treatments, size=n_patients)

        # Calculate baseline severity score (0-100)
        severity = (
            (bmi - 18) / 32 * 25 +  # BMI contribution
            (systolic - 90) / 90 * 25 +  # BP contribution
            (glucose - 70) / 110 * 25 +  # Glucose contribution
            (hba1c - 4.5) / 5.5 * 25  # HbA1c contribution
        )
        severity = np.clip(severity, 0, 100)

        # Create DataFrame
        df = pd.DataFrame({
            'patient_id': [f'PT{str(i).zfill(6)}' for i in range(1, n_patients + 1)],
            'age': ages,
            'gender': genders,
            'bmi': np.round(bmi, 1),
            'baseline_systolic': np.round(systolic, 0),
            'baseline_diastolic': np.round(diastolic, 0),
            'baseline_glucose': np.round(glucose, 0),
            'baseline_hba1c': np.round(hba1c, 2),
            'disease': diseases,
            'treatment': treatments,
            'baseline_severity': np.round(severity, 1)
        })

        return df

    def amplify_edge_cases(self, df: pd.DataFrame, amplification_factor: float = 0.3) -> pd.DataFrame:
        """
        Amplify edge cases (high-risk and low-risk patients) using synthetic data

        Args:
            df: Original patient dataframe
            amplification_factor: Proportion of additional synthetic patients to generate

        Returns:
            Amplified dataframe with additional edge case patients
        """
        n_synthetic = int(len(df) * amplification_factor)

        # Generate high-risk patients (top 10% severity)
        high_risk_samples = df[df['baseline_severity'] > df['baseline_severity'].quantile(0.9)]
        n_high_risk = n_synthetic // 2

        synthetic_high_risk = []
        for _ in range(n_high_risk):
            base_patient = high_risk_samples.sample(1).iloc[0].copy()
            # Add noise while maintaining high risk
            synthetic_patient = base_patient.copy()
            synthetic_patient['patient_id'] = f'SYN{np.random.randint(100000, 999999)}'
            synthetic_patient['age'] += np.random.randint(-5, 5)
            synthetic_patient['bmi'] += np.random.normal(0, 2)
            synthetic_patient['baseline_systolic'] += np.random.normal(0, 5)
            synthetic_patient['baseline_diastolic'] += np.random.normal(0, 3)
            synthetic_patient['baseline_glucose'] += np.random.normal(0, 8)
            synthetic_patient['baseline_hba1c'] += np.random.normal(0, 0.2)
            synthetic_high_risk.append(synthetic_patient)

        # Generate low-risk patients (bottom 10% severity)
        low_risk_samples = df[df['baseline_severity'] < df['baseline_severity'].quantile(0.1)]
        n_low_risk = n_synthetic - n_high_risk

        synthetic_low_risk = []
        for _ in range(n_low_risk):
            base_patient = low_risk_samples.sample(1).iloc[0].copy()
            synthetic_patient = base_patient.copy()
            synthetic_patient['patient_id'] = f'SYN{np.random.randint(100000, 999999)}'
            synthetic_patient['age'] += np.random.randint(-5, 5)
            synthetic_patient['bmi'] += np.random.normal(0, 1.5)
            synthetic_patient['baseline_systolic'] += np.random.normal(0, 4)
            synthetic_patient['baseline_diastolic'] += np.random.normal(0, 2)
            synthetic_patient['baseline_glucose'] += np.random.normal(0, 5)
            synthetic_patient['baseline_hba1c'] += np.random.normal(0, 0.15)
            synthetic_low_risk.append(synthetic_patient)

        # Combine all data
        synthetic_df = pd.DataFrame(synthetic_high_risk + synthetic_low_risk)
        amplified_df = pd.concat([df, synthetic_df], ignore_index=True)

        return amplified_df

    def generate_patient_cohort(
        self,
        n_patients: int = 1000,
        amplify: bool = True,
        amplification_factor: float = 0.3
    ) -> pd.DataFrame:
        """
        Generate complete patient cohort with optional amplification

        Args:
            n_patients: Number of base patients
            amplify: Whether to amplify edge cases
            amplification_factor: Proportion of synthetic patients to add

        Returns:
            Complete patient cohort dataframe
        """
        base_df = self.generate_base_population(n_patients)

        if amplify:
            cohort_df = self.amplify_edge_cases(base_df, amplification_factor)
        else:
            cohort_df = base_df

        return cohort_df


if __name__ == "__main__":
    # Test the data generator
    generator = HealthcareDataGenerator(random_seed=42)
    patients = generator.generate_patient_cohort(n_patients=1000, amplify=True)

    print("=" * 80)
    print("Healthcare Patient Data Generator - Test Run")
    print("=" * 80)
    print(f"\nGenerated {len(patients)} patients")
    print(f"\nDataset shape: {patients.shape}")
    print(f"\nFirst 5 patients:")
    print(patients.head())
    print(f"\nDataset summary:")
    print(patients.describe())
    print(f"\nDisease distribution:")
    print(patients['disease'].value_counts())
    print(f"\nTreatment distribution:")
    print(patients['treatment'].value_counts())

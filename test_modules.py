"""
Test script to verify all modules work correctly
Run this before deploying the application
"""

import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent / 'src'))

from data_generator import HealthcareDataGenerator
from monte_carlo_simulator import MonteCarloHealthcareSimulator
from analysis import HealthcareAnalyzer

def test_data_generator():
    """Test patient data generation"""
    print("\n" + "="*80)
    print("TEST 1: Data Generator")
    print("="*80)

    try:
        generator = HealthcareDataGenerator(random_seed=42)
        patients = generator.generate_patient_cohort(n_patients=100, amplify=True)

        assert len(patients) > 100, "Amplification should increase patient count"
        assert 'patient_id' in patients.columns, "Missing patient_id column"
        assert 'baseline_severity' in patients.columns, "Missing baseline_severity column"

        print(f"[OK] Generated {len(patients)} patients successfully")
        print(f"[OK] Columns: {list(patients.columns)}")
        print(f"[OK] Age range: {patients['age'].min()} - {patients['age'].max()}")
        print(f"[OK] Severity range: {patients['baseline_severity'].min():.1f} - {patients['baseline_severity'].max():.1f}")

        return patients

    except Exception as e:
        print(f"[FAIL] Data generator test failed: {str(e)}")
        return None


def test_monte_carlo_simulator(patients):
    """Test Monte Carlo simulation"""
    print("\n" + "="*80)
    print("TEST 2: Monte Carlo Simulator")
    print("="*80)

    if patients is None:
        print("[FAIL] Skipping simulator test (no patient data)")
        return None

    try:
        simulator = MonteCarloHealthcareSimulator(random_seed=42)

        # Test single patient simulation
        test_patient = patients.iloc[0]
        print(f"\nTesting single patient: {test_patient['patient_id']}")
        result = simulator.simulate_treatment_outcome(test_patient, num_simulations=1000)

        assert 'probability_of_success' in result, "Missing success probability"
        assert 'recovery_time' in result, "Missing recovery time"
        assert 0 <= result['probability_of_success'] <= 1, "Invalid success probability"

        print(f"[OK] Single patient simulation successful")
        print(f"  - Success probability: {result['probability_of_success']*100:.1f}%")
        print(f"  - Mean recovery: {result['recovery_time']['mean']:.1f} days")

        # Test cohort simulation
        print(f"\nTesting cohort simulation (10 patients)...")
        results_df = simulator.simulate_cohort(patients, num_simulations=1000, sample_size=10)

        assert len(results_df) == 10, "Incorrect number of simulation results"
        print(f"[OK] Cohort simulation successful")
        print(f"  - Simulated {len(results_df)} patients")
        print(f"  - Mean success rate: {results_df['probability_of_success'].mean()*100:.1f}%")

        return results_df

    except Exception as e:
        print(f"[FAIL] Simulator test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return None


def test_analyzer(results_df):
    """Test analysis module"""
    print("\n" + "="*80)
    print("TEST 3: Analyzer")
    print("="*80)

    if results_df is None:
        print("[FAIL] Skipping analyzer test (no simulation results)")
        return False

    try:
        analyzer = HealthcareAnalyzer()

        # Test summary statistics
        summary = analyzer.generate_summary_statistics(results_df)
        assert 'total_patients' in summary, "Missing total_patients in summary"
        print(f"[OK] Summary statistics generated")
        print(f"  - Total patients: {summary['total_patients']}")

        # Test treatment comparison
        comparison = analyzer.compare_treatments_analysis(results_df)
        assert len(comparison) > 0, "No treatment comparison results"
        print(f"[OK] Treatment comparison successful")
        print(f"  - Compared {len(comparison)} treatments")

        # Test risk stratification
        risk_analysis = analyzer.risk_stratification_analysis(results_df)
        print(f"[OK] Risk stratification successful")
        print(f"  - Risk categories: {len(risk_analysis)}")

        return True

    except Exception as e:
        print(f"[FAIL] Analyzer test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests"""
    print("\n" + "="*80)
    print("HEALTHCARE MONTE CARLO ANALYZER - MODULE TESTS")
    print("="*80)

    # Test 1: Data Generation
    patients = test_data_generator()

    # Test 2: Monte Carlo Simulation
    results_df = test_monte_carlo_simulator(patients)

    # Test 3: Analysis
    analyzer_ok = test_analyzer(results_df)

    # Summary
    print("\n" + "="*80)
    print("TEST SUMMARY")
    print("="*80)

    all_passed = (patients is not None) and (results_df is not None) and analyzer_ok

    if all_passed:
        print("[SUCCESS] ALL TESTS PASSED")
        print("\nThe application is ready to deploy!")
        print("\nNext steps:")
        print("1. Run the app locally: streamlit run app.py")
        print("2. Push to GitHub")
        print("3. Deploy on Streamlit Cloud")
    else:
        print("[FAIL] SOME TESTS FAILED")
        print("\nPlease fix the errors before deploying.")

    print("="*80 + "\n")

    return all_passed


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

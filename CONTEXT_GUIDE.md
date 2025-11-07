# Quick Context Guide - Healthcare Treatment Outcome Analyzer

**Purpose:** Navigate to the right documentation to understand this app quickly.

---

## 🎯 To Understand This App (Start Here)

**1. High-Level Overview (5 min read):**
- → `EXECUTIVE_SUMMARY.md` - Problem, solution, findings, business value

**2. Full Documentation (15 min read):**
- → `README.md` - Features, methodology, deployment, usage

**3. Original Research (Optional):**
- → `healthcare_treatment_monte_carlo.ipynb` - Jupyter notebook with detailed analysis

---

## 📝 Recent Changes & Why

**Gemini Integration (Commit 1afc87a):**
- Added `src/gemini_helper.py` - Mobile-friendly copy buttons for AI interpretation
- Integrated Gemini buttons in all 4 app pages
- Uses `st.code()` for one-tap copy (mobile + desktop)

**Sidebar Reorganization:**
- Moved sensitivity sliders UP (right after mode selection)
- Moved About section DOWN to bottom
- Better UX hierarchy

**Sensitivity Sliders Added:**
- Treatment Efficacy Baseline (50-95%)
- Treatment Cost Factor (0.5-2.0x)
- Complication Rate (1-20%)
- Recovery Time Factor (0.5-2.0x)

**Methodology Documentation:**
- Added Synthetic Data Generation section to README and Executive Summary
- Explains why synthetic > real datasets (privacy, reproducibility)

---

## 🔧 Model Parameters Reference

**Key Distributions:**

File: `src/monte_carlo_simulator.py`

| Distribution | Use Case | Parameters | Location |
|--------------|----------|------------|----------|
| Beta | Treatment efficacy (bounded 0-1) | alpha, beta vary by treatment | Function `_simulate_treatment_outcome()` |
| Triangular | Recovery time (PERT) | min, mode, max (optimistic/likely/pessimistic) | Function `_simulate_recovery_time()` |
| Bernoulli | Complications (yes/no) | probability varies by age/severity | Function `_simulate_complications()` |
| Normal | Cost variation | mean ± std based on complications | Function `_calculate_treatment_cost()` |

**Treatment Protocols:**
- Standard Care: 70% efficacy baseline
- Intensive Therapy: 75% efficacy, higher cost
- Experimental Treatment: 80% efficacy, uncertain outcomes

---

## 🧪 How to Resume Work / Test

**1. Verify Setup:**
```bash
cd montecarlo_analysis_app
python test_modules.py              # Validates all imports
python -m py_compile app.py src/*.py  # Check syntax
```

**2. Run App Locally:**
```bash
streamlit run app.py
```

**3. Check Recent Commits:**
```bash
git log --oneline -10
```

**4. Review Notebook Analysis:**
```bash
jupyter notebook healthcare_treatment_monte_carlo.ipynb
```

---

## 📂 File Structure Guide

**Core Modules:**
- `src/data_generator.py` - Synthetic patient cohort creation
- `src/monte_carlo_simulator.py` - **Main simulation engine** (10,000+ scenarios)
- `src/analysis.py` - Statistical analysis and visualization
- `src/gemini_helper.py` - AI integration + sensitivity sliders (NEW)

**Key Functions to Understand:**
- `MonteCarloHealthcareSimulator.simulate_treatment()` - Single patient simulation
- `MonteCarloHealthcareSimulator.simulate_cohort()` - Batch processing
- `MonteCarloHealthcareSimulator.compare_treatments()` - Multi-treatment comparison
- `HealthcareAnalyzer.generate_visualization_report()` - Creates 6-panel plot

**Test Files:**
- `test_modules.py` - Validates all module imports

**Documentation Files:**
- `EXECUTIVE_SUMMARY.md` - 1-page overview
- `README.md` - Full documentation
- `QUICKSTART.md` - Quick setup guide
- `DEPLOYMENT_GUIDE.md` - Streamlit Cloud setup
- `PROJECT_SUMMARY.md` - Technical deep dive
- `COMPLETION_REPORT.md` - Delivery summary
- `PROCESS_FLOW.md` - Visual workflow

---

## 🏗️ Architecture Overview

```
User Input (app.py)
    ↓
Sidebar Sliders (gemini_helper.py)
    ↓
Stored in st.session_state
    ↓
MonteCarloHealthcareSimulator()
    ↓
Generate Synthetic Patients (Beta, Normal distributions)
    ↓
10,000 simulations per patient × 3 treatments
    ↓
Results: success %, complications %, recovery time, severity reduction
    ↓
HealthcareAnalyzer (statistical analysis)
    ↓
6-panel visualization + risk stratification
    ↓
Gemini reports (structured summaries for AI interpretation)
```

---

## 🚨 Known Issues / Limitations

**Documented in:** `COMPLETION_REPORT.md` and `PROJECT_SUMMARY.md`

1. **Synthetic data only** - No real patient data (intentional for privacy)
2. **Limited to 2 diseases** - Type 2 Diabetes, Hypertension (can be expanded)
3. **3 treatment protocols** - Standard, Intensive, Experimental
4. **Recovery time varies widely** - 90% CI spans 20-30 days (realistic uncertainty)

---

## 🔄 Common Tasks

**Add a new treatment protocol:**
1. Edit `src/monte_carlo_simulator.py`
2. Add to `TREATMENT_PARAMS` dict (defines efficacy, cost, recovery)
3. Update `compare_treatments()` method

**Add a new disease type:**
1. Edit `src/data_generator.py`
2. Add to `DISEASE_TYPES` list
3. Define baseline severity ranges

**Adjust treatment efficacy:**
1. Edit `src/monte_carlo_simulator.py`
2. Modify Beta distribution parameters (alpha, beta) in `_simulate_treatment_outcome()`

**Change visualization style:**
1. Edit `src/analysis.py`
2. Modify `generate_visualization_report()` function (matplotlib/seaborn)

---

## 🎓 Academic Context

**Synthetic Data Justification:**
- → `EXECUTIVE_SUMMARY.md` lines 17-29
- → `README.md` lines 38-57
- → `app.py` lines 107-141 (About section)

**Why it's valid:** Standard practice in healthcare Monte Carlo research; eliminates HIPAA concerns; enables controlled experimentation with population parameters.

**Based on Article:**
- "Stop Guessing About Risk: Use Monte Carlo Simulation in Python to Make Data-Driven Decisions Under Uncertainty"

---

## 📊 Dataset Info

**Generated Data:**
- `data/` - Patient cohorts (if generated, not tracked in Git)
- `outputs/` - Simulation results (if generated, not tracked in Git)

**Regenerate using app:**
1. Mode 1: Generate Patient Data
2. Mode 2: Run Simulations
3. Mode 3: Analyze Results

---

## 🔗 Deployment

**Live App:** Streamlit Cloud (auto-deploys from GitHub main branch)
**Repository:** https://github.com/horacefonseca/healthcare_montecarlo_analysis

**Deployment docs:**
- → `DEPLOYMENT_GUIDE.md` - Full Streamlit Cloud setup
- → `STREAMLIT_CLOUD_SETUP.md` - Step-by-step instructions
- → `.python-version` specifies Python 3.10
- → `requirements.txt` has all dependencies

---

## 📈 Key Metrics to Understand

**From Simulations:**
- **Probability of Success** - % of simulations where treatment succeeded
- **Probability of Complications** - % of simulations with adverse events
- **Recovery Time** - Days until patient returns to baseline (percentiles: 5th, 25th, 50th, 75th, 95th)
- **Severity Reduction** - Decrease in disease severity score (0-100 scale)
- **Total Cost** - Treatment cost + complication costs

**Risk Stratification:**
- Low Risk: Severity < 40
- Moderate Risk: Severity 40-60
- High Risk: Severity 60-80
- Very High Risk: Severity > 80

---

## 🎨 Visualization Components

**6-Panel Report (generated by `HealthcareAnalyzer`):**
1. Success Rate by Treatment (bar chart)
2. Complication Rate by Treatment (bar chart)
3. Recovery Time Distribution (box plot)
4. Severity Reduction (violin plot)
5. Cost Distribution (histogram)
6. Risk-Stratified Outcomes (heatmap)

**Single Patient Graphs:**
- Success rate comparison (bar)
- Recovery time by percentile (grouped bar)

---

## 🔍 Debugging Tips

**App won't run:**
- Check: `python test_modules.py` (verifies all imports)
- Check: `.python-version` matches your Python (3.10)
- Check: `pip install -r requirements.txt`

**Simulation too slow:**
- Reduce `num_simulations` (try 1000 instead of 10000)
- Reduce `sample_size` (try 50 instead of 100)

**Results look wrong:**
- Check patient characteristics (age, BMI, severity)
- Verify treatment parameters in `monte_carlo_simulator.py`
- Review distributions (Beta for efficacy, Triangular for recovery)

---

**Last Updated:** January 2025
**For Questions:** Check GitHub issues or re-read documentation files listed above

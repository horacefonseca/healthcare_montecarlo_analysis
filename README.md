# Healthcare Treatment Outcome Analyzer

## Monte Carlo Simulation for Evidence-Based Treatment Planning

A comprehensive web application that uses Monte Carlo simulation to quantify uncertainty in healthcare treatment outcomes, enabling data-driven clinical decision-making with confidence intervals and risk assessments.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28%2B-red)
![License](https://img.shields.io/badge/License-MIT-green)

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Deployment](#deployment)
- [Academic Context](#academic-context)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

This application applies Monte Carlo simulation techniques to healthcare treatment planning, specifically focusing on chronic disease management (Type 2 Diabetes, Hypertension). It demonstrates:

- **Synthetic Data Amplification**: Generating realistic patient profiles with edge case amplification
- **Probabilistic Modeling**: Using Monte Carlo methods to simulate treatment outcomes
- **Risk Quantification**: Calculating confidence intervals, Value at Risk, and probability distributions
- **Comparative Analysis**: Evaluating multiple treatment options for individual patients

**Based on the methodology described in:** "Stop Guessing About Risk: Use Monte Carlo Simulation in Python to Make Data-Driven Decisions Under Uncertainty"

### Synthetic Data Generation Approach

**Why Synthetic Data Instead of Real Patient Datasets?**

This project employs **synthetic patient generation** rather than searching for static healthcare datasets. This is **standard practice in Monte Carlo simulation research** because it:

1. **Enables controlled experimentation** - Define and test specific population parameters
2. **Eliminates data privacy issues** - No HIPAA violations or patient information exposure
3. **Provides unlimited samples** - Generate 100 to 100,000+ patients on demand
4. **Maintains statistical validity** - Uses real medical distributions from clinical trials and population health data
5. **Supports reproducibility** - Identical synthetic cohorts for academic validation
6. **Avoids data quality concerns** - No missing values, inconsistencies, or outdated snapshots

**Data Sources for Calibration:**
- Clinical trial efficacy rates (medical literature)
- Population health statistics (CDC, medical databases)
- Treatment cost data (healthcare economics research)
- Recovery time distributions (published medical studies)

**Academic Justification:** Published Monte Carlo studies in healthcare, clinical trials, and medical decision analysis routinely use synthetic data to control confounding variables and test sensitivity to distributional assumptions. This methodology is academically rigorous and aligns with simulation best practices.

---

## Features

### 1. Patient Data Generation
- Generate synthetic patient cohorts with realistic correlations between:
  - Age, BMI, blood pressure, glucose levels, HbA1c
  - Disease types and severity scores
- **Synthetic Data Amplification**: Automatically create edge cases (high-risk and low-risk patients)
- Customizable population size and amplification factors

### 2. Monte Carlo Simulation
- Simulate treatment outcomes using probabilistic models:
  - **Beta distribution** for treatment efficacy (bounded 0-1)
  - **Triangular distribution** for recovery time (PERT-based)
  - **Bernoulli trials** for complications
- Adjusts predictions based on patient characteristics (age, BMI, baseline severity)
- Supports three treatment protocols:
  - Standard Care
  - Intensive Therapy
  - Experimental Treatment

### 3. Comprehensive Analysis
- **Treatment Comparison**: Success rates, complication rates, recovery times
- **Risk Stratification**: Analysis by severity categories (Low, Moderate, High, Very High)
- **Statistical Metrics**:
  - Percentiles (5th, 25th, 50th, 75th, 95th)
  - Confidence intervals
  - Probability of success/complications
  - Expected recovery times with confidence levels

### 4. Interactive Visualizations
- Success rate comparisons
- Recovery time distributions
- Risk-stratified outcomes
- Treatment comparison heatmaps
- Individual patient analysis

### 5. Single Patient Analysis
- Compare all treatment options for a specific patient
- Personalized recommendations based on:
  - Highest success rate
  - Lowest complication rate
  - Fastest recovery time
- Visual comparison of outcomes across treatments

---

## Project Structure

```
montecarlo_analysis_app/
│
├── app.py                          # Main Streamlit application
├── requirements.txt                # Python dependencies
├── README.md                       # This file
├── .gitignore                      # Git ignore file
│
├── src/                            # Source code modules
│   ├── data_generator.py           # Synthetic patient data generator
│   ├── monte_carlo_simulator.py    # Monte Carlo simulation engine
│   └── analysis.py                 # Statistical analysis and visualization
│
├── config/                         # Configuration files
│   └── simulation_config.json      # Simulation parameters
│
├── data/                           # Generated data storage (gitignored)
│
└── outputs/                        # Analysis outputs (gitignored)
```

---

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager
- Git (for cloning repository)

### Local Installation

1. **Clone the repository:**
```bash
git clone <your-repository-url>
cd montecarlo_analysis_app
```

2. **Create a virtual environment (recommended):**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Run the application:**
```bash
streamlit run app.py
```

The application will open in your default web browser at `http://localhost:8501`

---

## Usage

### 1. Generate Patient Data

1. Select **"Generate Patient Data"** mode from the sidebar
2. Configure parameters:
   - Number of patients (50-5000)
   - Enable synthetic data amplification
   - Set amplification factor (0.1-0.5)
   - Choose random seed for reproducibility
3. Click **"Generate Patient Data"**
4. Review the generated cohort statistics and distributions
5. Download patient data if needed

### 2. Run Monte Carlo Simulations

1. Switch to **"Run Simulations"** mode
2. Configure simulation parameters:
   - Number of simulations per patient (1,000-50,000)
   - Sample size (for faster testing)
3. Click **"Run Simulations"**
4. Wait for simulations to complete (progress bar shown)
5. Review summary statistics

### 3. Analyze Results

1. Switch to **"Analyze Results"** mode
2. Review comprehensive analysis:
   - Overall statistics
   - Treatment comparison table
   - Risk stratification analysis
   - Comprehensive visualization report
3. Export results:
   - Download detailed CSV reports
   - Save visualization figures

### 4. Single Patient Analysis

1. Switch to **"Single Patient Analysis"** mode
2. Select a patient from the dropdown
3. Review patient information and baseline metrics
4. Click **"Compare All Treatments"**
5. Review:
   - Comparative success rates
   - Recovery time distributions
   - Personalized treatment recommendations

---

## Deployment

### Deploy to Streamlit Cloud

1. **Push your code to GitHub:**
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin <your-github-repo-url>
git push -u origin main
```

2. **Deploy on Streamlit Cloud:**
   - Go to [streamlit.io/cloud](https://streamlit.io/cloud)
   - Click "New app"
   - Select your GitHub repository
   - Set main file path: `app.py`
   - Click "Deploy"

3. **Configuration:**
   - Streamlit Cloud will automatically install dependencies from `requirements.txt`
   - No additional configuration needed

### Deploy to Other Platforms

#### Heroku
1. Create a `Procfile`:
```
web: sh setup.sh && streamlit run app.py
```

2. Create `setup.sh`:
```bash
mkdir -p ~/.streamlit/
echo "[server]
headless = true
port = $PORT
enableCORS = false
" > ~/.streamlit/config.toml
```

#### Docker
1. Create `Dockerfile`:
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "app.py"]
```

2. Build and run:
```bash
docker build -t healthcare-mc-app .
docker run -p 8501:8501 healthcare-mc-app
```

---

## Academic Context

### Research Application

This project demonstrates a complete Monte Carlo analysis pipeline suitable for:

- **Academic Research**: Quantifying uncertainty in clinical trials
- **Healthcare Analytics**: Treatment outcome prediction
- **Risk Assessment**: Patient-specific risk stratification
- **Decision Support**: Evidence-based treatment selection

### Key Methodologies

1. **Synthetic Data Amplification**
   - Addresses limited real-world data availability
   - Preserves statistical properties while adding edge cases
   - Enables robust model testing

2. **Monte Carlo Simulation**
   - Models uncertainty through probabilistic distributions
   - Generates confidence intervals for all predictions
   - Quantifies risk through multiple scenarios

3. **Statistical Analysis**
   - Percentile-based reporting (not just means)
   - Confidence interval calculation
   - Risk stratification
   - Comparative effectiveness research

### Citation

If you use this tool in academic research, please cite:

```
Healthcare Treatment Outcome Analyzer: A Monte Carlo Simulation Approach
[Your Name], 2024
GitHub: [Repository URL]
Based on Monte Carlo methodology from Dr. Ernesto Lee
```

---

## Technical Details

### Data Generation Algorithm

The synthetic patient generator creates realistic correlations:
- Age follows gamma distribution (realistic age distribution)
- BMI correlates with age
- Blood pressure correlates with BMI and age
- Glucose levels correlate with BMI
- HbA1c correlates with glucose levels
- Disease assignment based on risk factors

### Simulation Models

**Treatment Efficacy**: Beta distribution
```python
efficacy ~ Beta(α, β)
where α and β are derived from mean efficacy and adjusted for patient characteristics
```

**Recovery Time**: Triangular distribution
```python
recovery ~ Triangular(optimistic, likely, pessimistic)
```

**Complications**: Bernoulli trial
```python
complication ~ Bernoulli(p)
where p = base_rate * (1 + severity_penalty)
```

### Performance Considerations

- **10,000 simulations** per patient: ~0.5 seconds
- **100 patients**: ~50 seconds for complete analysis
- Memory usage: ~500MB for 1000 patients with 10,000 simulations each

---

## Troubleshooting

### Common Issues

1. **Import errors:**
   - Ensure all dependencies are installed: `pip install -r requirements.txt`
   - Check Python version: `python --version` (should be 3.8+)

2. **Slow performance:**
   - Reduce number of simulations
   - Use smaller sample sizes during testing
   - Ensure sufficient RAM available

3. **Visualization errors:**
   - Update matplotlib: `pip install --upgrade matplotlib`
   - Clear Streamlit cache: Click "Clear cache" in menu

---

## Future Enhancements

- [ ] Add real patient data import functionality
- [ ] Implement additional disease types
- [ ] Add cost-effectiveness analysis
- [ ] Include longitudinal outcome tracking
- [ ] Add machine learning models for efficacy prediction
- [ ] Implement multi-criteria decision analysis
- [ ] Add export to medical report format

---

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/YourFeature`)
3. Commit your changes (`git commit -m 'Add YourFeature'`)
4. Push to the branch (`git push origin feature/YourFeature`)
5. Open a Pull Request

---

## License

This project is licensed under the MIT License. See LICENSE file for details.

---

## Acknowledgments

- Methodology inspired by "Stop Guessing About Risk: Use Monte Carlo Simulation in Python" by Dr. Ernesto Lee
- Built with [Streamlit](https://streamlit.io/)
- Visualization powered by [Matplotlib](https://matplotlib.org/) and [Seaborn](https://seaborn.pydata.org/)

---

## Contact

For questions, issues, or collaboration opportunities, please open an issue on GitHub.

**Project Link:** [GitHub Repository URL]

---

**Disclaimer:** This tool is for educational and research purposes only. It should not be used as the sole basis for clinical decision-making. Always consult qualified healthcare professionals for medical decisions.

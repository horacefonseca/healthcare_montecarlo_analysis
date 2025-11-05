# Quick Start Guide

Get the Healthcare Monte Carlo Analyzer running in 5 minutes!

## 🚀 Option 1: Run Locally (Fastest)

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Test Installation
```bash
python test_modules.py
```

Expected output: `[SUCCESS] ALL TESTS PASSED`

### Step 3: Launch Application
```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

**That's it! You're ready to go!**

---

## 🌐 Option 2: Deploy to Streamlit Cloud (Free)

### Step 1: Push to GitHub
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main
```

### Step 2: Deploy
1. Go to https://share.streamlit.io/
2. Sign in with GitHub
3. Click "New app"
4. Select your repository
5. Set main file: `app.py`
6. Click "Deploy"

**Your app will be live in 2-5 minutes!**

---

## 📖 First-Time User Tutorial

### 1. Generate Patient Data
- Click "Generate Patient Data" in sidebar
- Set number of patients (start with 100)
- Enable "Synthetic Data Amplification"
- Click "Generate Patient Data"
- Review the cohort statistics and distributions

### 2. Run Simulations
- Switch to "Run Simulations" mode
- Set simulations per patient (start with 1,000)
- Set sample size (start with 10 for testing)
- Click "Run Simulations"
- Wait for completion (progress bar shown)

### 3. Analyze Results
- Switch to "Analyze Results" mode
- Review overall statistics
- Explore treatment comparisons
- Check risk stratification
- View comprehensive visualizations
- Download results if needed

### 4. Single Patient Analysis
- Switch to "Single Patient Analysis"
- Select a patient from dropdown
- Click "Compare All Treatments"
- Review personalized recommendations

---

## 🎯 Quick Tips

### For Best Performance
- Start with 1,000 simulations during testing
- Use sample sizes of 10-50 for quick experiments
- Increase to 10,000+ simulations for final analysis

### Understanding Results
- **Success Rate**: Probability of achieving ≥40% severity reduction without complications
- **Recovery Time**: Days until treatment completion
- **Percentiles**: Risk assessment at different confidence levels
- **VaR**: Maximum expected loss at given confidence level

### Common Use Cases

**1. Compare Treatment Effectiveness**
- Generate cohort → Run simulations → View treatment comparison table

**2. Risk Assessment**
- Generate cohort → Run simulations → Check risk stratification analysis

**3. Individual Patient Decision**
- Generate cohort → Switch to single patient mode → Compare treatments

---

## 📊 Example Workflow

```
1. Generate 500 patients with amplification
   ↓
2. Run 10,000 simulations per patient (sample 100)
   ↓
3. Analyze results:
   - Overall success rate
   - Treatment rankings
   - Risk-stratified outcomes
   ↓
4. Single patient analysis for high-risk cases
   ↓
5. Download detailed CSV report
```

---

## ⚡ Keyboard Shortcuts

- `Ctrl + R` - Rerun Streamlit app
- `Ctrl + Shift + R` - Clear cache and rerun
- `?` - View keyboard shortcuts (in app)

---

## 🔧 Troubleshooting

### "Module not found" error
```bash
pip install -r requirements.txt
```

### Visualizations not showing
```bash
pip install --upgrade matplotlib seaborn
```

### App won't start
```bash
# Check Streamlit installation
streamlit --version

# Reinstall if needed
pip install --upgrade streamlit
```

### Slow performance
- Reduce number of simulations (try 1,000)
- Use smaller sample sizes
- Close other applications

---

## 📚 Learn More

- **Full Documentation**: See README.md
- **Deployment Guide**: See DEPLOYMENT_GUIDE.md
- **Project Overview**: See PROJECT_SUMMARY.md
- **Test Modules**: Run `python test_modules.py`

---

## 🎓 For Academics

### Running Experiments

**Small-scale test:**
```python
# In Python console
from src.data_generator import HealthcareDataGenerator
from src.monte_carlo_simulator import MonteCarloHealthcareSimulator

generator = HealthcareDataGenerator(random_seed=42)
patients = generator.generate_patient_cohort(n_patients=100)

simulator = MonteCarloHealthcareSimulator(random_seed=42)
results = simulator.simulate_cohort(patients, num_simulations=10000, sample_size=10)

print(results['probability_of_success'].describe())
```

**Batch processing:**
```bash
# Use the web interface for interactive analysis
streamlit run app.py
```

---

## 💻 Development Setup

### For Contributors

```bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git
cd montecarlo_analysis_app

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run tests
python test_modules.py

# Start development server
streamlit run app.py
```

---

## 📞 Need Help?

1. **Check documentation**: README.md has extensive troubleshooting
2. **Run tests**: `python test_modules.py` to diagnose issues
3. **GitHub Issues**: Report bugs or request features
4. **Streamlit Community**: https://discuss.streamlit.io/

---

## 🎉 You're Ready!

Start exploring healthcare treatment outcomes with Monte Carlo simulation!

**Remember:** This is for educational and research purposes only. Always consult healthcare professionals for medical decisions.

---

**Quick Reference Commands:**

```bash
# Test everything
python test_modules.py

# Run locally
streamlit run app.py

# Deploy
git push origin main
# Then use Streamlit Cloud dashboard
```

Happy analyzing! 📊🏥

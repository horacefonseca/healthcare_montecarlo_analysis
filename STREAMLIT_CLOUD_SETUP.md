# Streamlit Cloud Setup Guide

## ✅ Compatibility Verified

This application is specifically configured for **Streamlit Cloud** deployment with the following compatibility settings:

### Python Version
- **Specified:** Python 3.10 (via `.python-version` file)
- **Compatible:** Python 3.9, 3.10, 3.11
- **Streamlit Cloud Default:** Python 3.10 (our configuration)

### Package Versions (Verified Compatible)

All packages are pinned to versions that work reliably with Streamlit Cloud:

```
numpy>=1.21.0,<2.0.0        # Compatible with Python 3.9+
pandas>=1.3.0,<3.0.0        # Stable version for Streamlit
scipy>=1.7.0,<2.0.0         # Compatible with Python 3.9+
matplotlib>=3.5.0,<4.0.0    # Tested with Streamlit
seaborn>=0.11.0,<1.0.0      # Stable visualization
streamlit>=1.20.0,<2.0.0    # Stable Streamlit version
openpyxl>=3.0.0             # Data handling
plotly>=5.0.0               # Interactive plots
```

### Why These Versions?

1. **numpy 1.21.0**: First version with full Python 3.9 support
2. **pandas 1.3.0**: Stable, widely tested with Streamlit apps
3. **scipy 1.7.0**: Compatible with numpy 1.21+
4. **matplotlib 3.5.0**: Works reliably in Streamlit's rendering
5. **streamlit 1.20.0**: Stable version with all features we use

### Configuration Files

#### `.python-version`
```
3.10
```
Tells Streamlit Cloud to use Python 3.10 specifically.

#### `requirements.txt`
Contains all Python package dependencies with version constraints.

#### `app.py`
Main application entry point (Streamlit Cloud looks for this).

---

## 🚀 Deployment Steps for Streamlit Cloud

### Method 1: Using Streamlit Cloud Dashboard (Recommended)

1. **Push to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Healthcare Monte Carlo Analyzer - Streamlit Cloud Ready"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
   git push -u origin main
   ```

2. **Deploy on Streamlit Cloud**
   - Go to: https://share.streamlit.io/
   - Sign in with GitHub
   - Click "New app"
   - Repository: Select your repo
   - Branch: `main`
   - Main file path: `app.py`
   - Click "Deploy"

3. **Monitor Deployment**
   - Watch the deployment logs
   - Should complete in 2-5 minutes
   - Application will be available at: `https://YOUR-APP-NAME.streamlit.app`

### Method 2: Using Streamlit CLI

If you have Streamlit CLI installed:

```bash
streamlit cloud deploy app.py
```

---

## 🔧 Streamlit Cloud Configuration

### Automatic Configuration

Streamlit Cloud automatically reads:
- `.python-version` → Python version
- `requirements.txt` → Python packages
- `app.py` → Application entry point

### Optional: Advanced Configuration

Create `.streamlit/config.toml` (if needed):

```toml
[theme]
primaryColor = "#1f77b4"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
font = "sans serif"

[server]
maxUploadSize = 200
enableCORS = false
enableXsrfProtection = true
```

---

## ✅ Pre-Deployment Checklist

Before deploying to Streamlit Cloud:

- [x] `.python-version` file exists (Python 3.10)
- [x] `requirements.txt` uses compatible versions
- [x] `app.py` is in root directory
- [x] All imports use relative paths
- [x] No hardcoded file paths (only relative)
- [x] .gitignore excludes `__pycache__` and data files
- [x] All tests passing (`python test_modules.py`)

---

## 🐛 Troubleshooting Streamlit Cloud Deployment

### Issue: "Module not found" error

**Solution 1:** Check requirements.txt
```bash
# Verify all imports are listed
grep -r "import" app.py src/*.py | grep -v "#"
```

**Solution 2:** Add missing package
```bash
# If you see "ModuleNotFoundError: No module named 'xyz'"
# Add to requirements.txt:
echo "xyz>=1.0.0" >> requirements.txt
git add requirements.txt
git commit -m "Add missing dependency"
git push
```

### Issue: "Python version mismatch"

**Solution:** Verify `.python-version` file
```bash
cat .python-version
# Should show: 3.10
```

If missing:
```bash
echo "3.10" > .python-version
git add .python-version
git commit -m "Add Python version specification"
git push
```

### Issue: Package version conflicts

**Solution:** Use the exact versions we specified
```bash
# Copy our tested requirements.txt
# It has version constraints that work together
```

### Issue: App crashes on startup

**Solution 1:** Check logs in Streamlit Cloud dashboard
- Look for specific error messages
- Check for missing files or incorrect paths

**Solution 2:** Test locally first
```bash
# Install exact same versions
pip install -r requirements.txt

# Run locally
streamlit run app.py
```

### Issue: Slow loading or timeout

**Solution:** Reduce default simulation sizes
- In `app.py`, find initial values
- Reduce default `num_simulations` to 1000
- Reduce default `sample_size` to 50

---

## 🎯 Streamlit Cloud Limits (Free Tier)

Be aware of these limits:

| Resource | Free Tier Limit |
|----------|----------------|
| RAM | 1 GB |
| CPU | 1 core |
| Storage | Temporary only |
| Apps | Unlimited public apps |
| Bandwidth | Generous but not unlimited |

### Optimization Tips:

1. **Memory Management**
   - Don't load all data at once
   - Use `@st.cache_data` for expensive computations
   - Clear unnecessary variables

2. **CPU Efficiency**
   - Start with smaller simulation counts
   - Let users increase for detailed analysis
   - Use sampling for large datasets

3. **Storage**
   - Don't store large files in repo
   - Generate data on-the-fly
   - Use downloads instead of saving locally

---

## 📊 Performance Expectations

On Streamlit Cloud (free tier):

| Task | Expected Time |
|------|--------------|
| App startup | 10-20 seconds |
| Generate 100 patients | 1-2 seconds |
| 1,000 simulations | 5-10 seconds |
| 10,000 simulations (10 patients) | 15-30 seconds |
| Generate visualizations | 3-5 seconds |

---

## 🔒 Security Considerations

### Public App (Free Tier)

Your app will be **publicly accessible**. This is fine because:
- ✅ Uses only synthetic data
- ✅ No real patient information
- ✅ No authentication required
- ✅ Educational/research purpose

### Private App (Paid Tier)

If you need private access:
- Upgrade to Streamlit Cloud Team ($250/month)
- Add authentication
- Control access with invitations

---

## 📈 Monitoring Your App

### Streamlit Cloud Dashboard

Monitor:
- **Active users** - How many people are using your app
- **Resource usage** - RAM and CPU consumption
- **Logs** - Real-time application logs
- **Errors** - Any crashes or exceptions

### Usage Analytics

Track:
- Page views
- Feature usage
- Average session duration
- Error rates

---

## 🔄 Updating Your Deployed App

### Automatic Deployment

Any push to your `main` branch triggers automatic redeployment:

```bash
# Make changes
git add .
git commit -m "Update: describe your changes"
git push origin main

# Streamlit Cloud automatically redeploys (2-3 minutes)
```

### Manual Reboot

In Streamlit Cloud dashboard:
1. Go to your app
2. Click "⋮" menu
3. Select "Reboot app"

### Clear Cache

If you need to clear cached data:
1. In app, click "≡" menu (top right)
2. Select "Clear cache"
3. Or add in code: `st.cache_data.clear()`

---

## 🎓 Best Practices for Streamlit Cloud

### 1. Code Organization
```python
# Good: Modular structure
from src.data_generator import HealthcareDataGenerator
from src.monte_carlo_simulator import MonteCarloHealthcareSimulator
from src.analysis import HealthcareAnalyzer

# Bad: Everything in one file
```

### 2. Caching
```python
# Cache expensive operations
@st.cache_data
def load_data():
    # This only runs once
    return expensive_operation()
```

### 3. Error Handling
```python
# Always use try-except for user operations
try:
    result = run_simulation()
except Exception as e:
    st.error(f"Error: {str(e)}")
    st.stop()
```

### 4. User Feedback
```python
# Show progress for long operations
with st.spinner("Running simulations..."):
    results = simulator.run()
st.success("Complete!")
```

---

## 🆘 Getting Help

### Official Resources
- Streamlit Documentation: https://docs.streamlit.io/
- Streamlit Community Forum: https://discuss.streamlit.io/
- Streamlit Cloud Docs: https://docs.streamlit.io/streamlit-community-cloud

### For This App
- Check README.md for usage help
- Check QUICKSTART.md for setup issues
- Run `python test_modules.py` to verify installation

---

## ✅ Final Verification

Before going live, verify:

1. **Local Test**
   ```bash
   python test_modules.py
   # Should show: [SUCCESS] ALL TESTS PASSED
   ```

2. **Local Streamlit Test**
   ```bash
   streamlit run app.py
   # Should open in browser without errors
   ```

3. **Git Status**
   ```bash
   git status
   # All files should be committed
   ```

4. **Requirements Check**
   ```bash
   pip install -r requirements.txt
   # Should install without errors
   ```

---

## 🎉 You're Ready for Streamlit Cloud!

Your application is now:
- ✅ Using compatible Python version (3.10)
- ✅ Using compatible package versions
- ✅ Properly configured for Streamlit Cloud
- ✅ Tested and verified
- ✅ Ready to deploy!

**Next Step:** Follow the deployment steps above and go live! 🚀

---

## 📞 Support

If you encounter issues during deployment:
1. Check the troubleshooting section above
2. Review Streamlit Cloud logs
3. Post on Streamlit Community Forum
4. Check GitHub Issues for this project

---

**Configuration Last Updated:** 2024
**Verified Compatible with:** Streamlit Cloud (as of 2024)
**Python Version:** 3.10
**Streamlit Version:** 1.20.0+

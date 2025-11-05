# Deployment Guide

## Quick Start Deployment to Streamlit Cloud

### Prerequisites
- GitHub account
- Git installed locally
- Code pushed to a GitHub repository

### Step-by-Step Deployment

#### 1. Prepare Your Repository

Make sure your repository has this structure:
```
montecarlo_analysis_app/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── src/
│   ├── __init__.py
│   ├── data_generator.py
│   ├── monte_carlo_simulator.py
│   └── analysis.py
└── config/
    └── simulation_config.json
```

#### 2. Push to GitHub

```bash
# Initialize git repository (if not already done)
cd montecarlo_analysis_app
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit: Healthcare Monte Carlo Analyzer"

# Add remote repository
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git

# Push to GitHub
git push -u origin main
```

If you get an error about the default branch, try:
```bash
git branch -M main
git push -u origin main
```

#### 3. Deploy on Streamlit Cloud

1. **Go to Streamlit Cloud**
   - Visit: https://share.streamlit.io/
   - Sign in with your GitHub account

2. **Create New App**
   - Click "New app" button
   - Select your repository
   - Set branch: `main`
   - Set main file path: `app.py`
   - Click "Deploy!"

3. **Wait for Deployment**
   - Streamlit will automatically install dependencies from `requirements.txt`
   - This usually takes 2-5 minutes
   - You'll see a live deployment log

4. **Access Your App**
   - Once deployed, you'll get a URL like: `https://your-app-name.streamlit.app`
   - Share this URL with others!

### Troubleshooting Deployment

#### Issue: Module Not Found Error
**Solution:** Make sure `requirements.txt` includes all dependencies:
```
numpy>=1.24.0
pandas>=2.0.0
scipy>=1.10.0
matplotlib>=3.7.0
seaborn>=0.12.0
streamlit>=1.28.0
```

#### Issue: Import Errors
**Solution:** Verify the `src` directory structure and `__init__.py` file exists

#### Issue: App Crashes on Start
**Solution:** Check the logs in Streamlit Cloud dashboard for specific errors

### Advanced Configuration

#### Custom Domain
1. Go to App Settings in Streamlit Cloud
2. Navigate to "General" tab
3. Add your custom domain

#### Secrets Management
For sensitive data (if needed in future):
1. Go to App Settings
2. Click "Secrets"
3. Add secrets in TOML format:
```toml
[api_keys]
key = "value"
```

#### Resource Limits
Free tier limits:
- 1 GB RAM
- 1 CPU core
- Public apps only

For more resources, upgrade to Streamlit Cloud Team/Enterprise.

### Testing Before Deployment

Always test locally first:
```bash
# Install dependencies
pip install -r requirements.txt

# Test modules
python test_modules.py

# Run app locally
streamlit run app.py
```

### Updating Your Deployed App

Any push to the `main` branch will automatically trigger a redeployment:

```bash
# Make changes to your code
git add .
git commit -m "Update: description of changes"
git push origin main
```

Streamlit Cloud will automatically detect changes and redeploy.

### Monitoring and Logs

1. Go to Streamlit Cloud dashboard
2. Click on your app
3. View logs in real-time
4. Monitor usage statistics

### Alternative Deployment Options

#### Heroku

1. Install Heroku CLI
2. Create `Procfile`:
```
web: sh setup.sh && streamlit run app.py
```

3. Create `setup.sh`:
```bash
mkdir -p ~/.streamlit/
echo "[server]
headless = true
port = $PORT
enableCORS = false
" > ~/.streamlit/config.toml
```

4. Deploy:
```bash
heroku login
heroku create your-app-name
git push heroku main
```

#### Docker

1. Build image:
```bash
docker build -t healthcare-mc-app .
```

2. Run container:
```bash
docker run -p 8501:8501 healthcare-mc-app
```

3. Deploy to cloud (AWS, GCP, Azure)

### Best Practices

1. **Version Control**
   - Always commit working code
   - Use meaningful commit messages
   - Tag releases: `git tag v1.0.0`

2. **Testing**
   - Run `test_modules.py` before deploying
   - Test locally with `streamlit run app.py`
   - Verify all features work

3. **Documentation**
   - Keep README.md updated
   - Document any configuration changes
   - Add comments to complex code

4. **Performance**
   - Use caching in Streamlit (`@st.cache_data`)
   - Limit default simulation sizes
   - Optimize data processing

### Security Considerations

1. **Data Privacy**
   - This app uses synthetic data only
   - Never commit real patient data
   - Use `.gitignore` for sensitive files

2. **API Keys**
   - Use Streamlit Secrets for any API keys
   - Never hardcode credentials

3. **Access Control**
   - Free Streamlit apps are public
   - For private apps, upgrade to paid tier

### Support and Resources

- Streamlit Documentation: https://docs.streamlit.io/
- Streamlit Community: https://discuss.streamlit.io/
- GitHub Issues: [Your repository]/issues

### Deployment Checklist

Before deploying, verify:
- [ ] All files are committed to GitHub
- [ ] `requirements.txt` is complete and up-to-date
- [ ] `test_modules.py` passes all tests
- [ ] App runs locally without errors
- [ ] README.md is complete
- [ ] .gitignore excludes unnecessary files
- [ ] No sensitive data in repository

After deploying:
- [ ] App loads without errors
- [ ] All features work as expected
- [ ] UI is responsive
- [ ] Visualizations render correctly
- [ ] Downloads work properly

### Need Help?

If you encounter issues:
1. Check Streamlit Cloud logs
2. Review error messages
3. Test locally to isolate the problem
4. Check GitHub Issues for similar problems
5. Ask on Streamlit Community forum

---

**Congratulations!** Your Healthcare Monte Carlo Analyzer is now deployed and accessible worldwide! 🎉

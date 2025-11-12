# Quick Start Guide

Get up and running with the Marketing A/B Test Evaluation Platform in 5 minutes!

## Prerequisites Check

- [ ] Node.js 16+ installed (`node --version`)
- [ ] npm installed (`npm --version`)
- [ ] Python 3.8+ installed (`python --version`)
- [ ] Git installed (`git --version`)

## Installation (3 steps)

### Step 1: Install Node.js Dependencies
```bash
npm install
```

### Step 2: Install Python Dependencies
```bash
pip install pandas numpy scipy matplotlib seaborn statsmodels jupyter
```

### Step 3: Start Development Server
```bash
npm run dev
```

**That's it!** Open http://localhost:3000 in your browser.

## Optional: Generate Analysis Data

If you have `marketing_AB.csv`:

```bash
python ab_test_eda.py
python ab_test_frequentist.py
python ab_test_bayesian.py
python ab_test_business_impact.py
```

This generates JSON files that the dashboard will automatically load.

## Troubleshooting

### Port Already in Use
```bash
# Kill process on port 3000 (Windows)
netstat -ano | findstr :3000
taskkill /PID <PID> /F

# Or use a different port
npm run dev -- --port 3001
```

### Python Not Found
- Windows: Use `py` instead of `python`
- Mac/Linux: Check PATH or use `python3`

### Module Not Found
```bash
pip install --upgrade pandas numpy scipy matplotlib seaborn statsmodels
```

## Next Steps

1. Explore the dashboard tabs
2. Adjust confidence levels
3. Check out the Jupyter notebooks
4. Read the full [README.md](README.md)

## Need Help?

- Check [README.md](README.md) for detailed documentation
- Review [DEPLOYMENT.md](docs/DEPLOYMENT.md) for deployment
- Open an issue on GitHub

---

**Happy Testing!** 🚀


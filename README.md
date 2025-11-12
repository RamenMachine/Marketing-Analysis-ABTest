# 📊 Marketing A/B Test Evaluation Platform

[![React](https://img.shields.io/badge/React-18.2.0-61DAFB?logo=react)](https://reactjs.org/)
[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?logo=python)](https://www.python.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.0+-3178C6?logo=typescript)](https://www.typescriptlang.org/)
[![Vite](https://img.shields.io/badge/Vite-5.0-646CFF?logo=vite)](https://vitejs.dev/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

A comprehensive, production-ready platform for analyzing marketing campaign effectiveness through rigorous A/B testing methodology. This project combines advanced statistical analysis, interactive data visualization, and business intelligence to provide actionable insights for marketing decision-making.

![Dashboard Preview](https://via.placeholder.com/800x400/1a1a1a/ffffff?text=A%2FB+Test+Dashboard)

---

## 📋 Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Analysis Methodology](#analysis-methodology)
- [Technologies Used](#technologies-used)
- [Project Structure](#project-structure)
- [Installation & Setup](#installation--setup)
- [Usage Guide](#usage-guide)
- [Statistical Methods Explained](#statistical-methods-explained)
- [Business Metrics](#business-metrics)
- [Dashboard Features](#dashboard-features)
- [Jupyter Notebooks](#jupyter-notebooks)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [License](#license)

---

## 🎯 Overview

This platform provides a complete solution for evaluating marketing A/B tests, featuring:

- **Dual Statistical Approaches**: Both Frequentist and Bayesian methodologies for robust analysis
- **Interactive Dashboard**: Real-time visualizations with adjustable confidence levels
- **Business Intelligence**: ROAS, ROI, CPA, and scaling projections
- **Professional Documentation**: Comprehensive Jupyter notebooks with mathematical formulas
- **Production-Ready Code**: TypeScript, error handling, and deployment configurations

### Problem Statement

Marketing teams need reliable, statistically rigorous methods to evaluate campaign effectiveness. Traditional approaches often lack:
- Multiple statistical perspectives for robust conclusions
- Business impact translation from statistical results
- Interactive visualization for stakeholder communication
- Real-time confidence level adjustment

### Solution

A full-stack platform that bridges statistical rigor with business insights, featuring:
- Multiple testing approaches (Frequentist + Bayesian)
- Real-time dashboard with adjustable parameters
- Direct translation to revenue metrics
- Professional presentation for stakeholders

---

## ✨ Key Features

### 📊 Statistical Analysis

#### Frequentist Methods
- **Two-Sample T-Test (Welch's)**: Tests for difference in means with unequal variances
- **Chi-Square Test for Independence**: Tests whether group assignment and conversion are independent
- **Bootstrap Confidence Intervals**: Non-parametric confidence interval estimation using 10,000 resamples
- **Effect Size Calculation**: Cohen's h (for proportions) and Cohen's d (for continuous variables)
- **Statistical Power Analysis**: Assesses the probability of detecting a true effect

#### Bayesian Methods
- **Beta-Binomial Model**: Conjugate prior for binary outcomes with uniform Beta(1,1) prior
- **Posterior Distributions**: Full uncertainty quantification through 100,000 Monte Carlo samples
- **Credible Intervals**: Intuitive probability interpretation (95% credible intervals)
- **Probability of Superiority**: Direct probability statements (P(Ad > PSA | data))
- **Expected Value Calculations**: Business impact estimation from posterior distributions

#### Dynamic Features
- **Adjustable Confidence Levels**: Real-time switching between 90%, 95%, and 99% confidence intervals
- **Interactive Visualizations**: Hover tooltips, zoom, and filter capabilities
- **Export Functionality**: JSON export for further analysis

### 💼 Business Intelligence

- **Incremental Conversions**: Additional conversions directly attributed to the advertising campaign
- **ROAS (Return on Ad Spend)**: Revenue generated per dollar spent on advertising
- **ROI (Return on Investment)**: Net profit relative to investment
- **CPA (Cost per Incremental Acquisition)**: Cost to acquire one incremental conversion
- **Break-Even Analysis**: Minimum performance threshold needed to justify campaign costs
- **Scaling Projections**: Expected impact at different user volumes (10K, 50K, 100K, 500K, 1M users)

### 🎨 Interactive Dashboard

- **Glassmorphism UI Design**: Modern, professional aesthetic with backdrop blur effects
- **Responsive Layout**: Works seamlessly on desktop and tablet devices
- **Real-time Updates**: Dynamic recalculation of confidence intervals and metrics
- **Multiple Tabs**: Overview, Statistics, Visualizations, and Insights
- **Heat Map Visualization**: Optimal ad timing analysis by day and hour

### 📈 Advanced Analytics

- **Temporal Pattern Analysis**: Conversion rates by day of week and hour of day
- **Dose-Response Analysis**: Relationship between ad exposure frequency and conversion rates
- **Exploratory Data Analysis**: Comprehensive data quality checks, missing value detection, duplicate identification
- **Correlation Analysis**: Pearson and Spearman correlation tests

---

## 🔬 Analysis Methodology

### Data Processing Pipeline

1. **Data Loading & Quality Assessment**
   - Load CSV data with Pandas
   - Check for missing values, duplicates, and data consistency
   - Verify unique user identification
   - Validate group randomization

2. **Exploratory Data Analysis (EDA)**
   - Overall conversion rate calculation
   - Group-wise conversion rate comparison
   - Temporal pattern identification (day/hour effects)
   - Dose-response relationship investigation
   - Correlation analysis between ad exposure and conversion

3. **Statistical Testing**
   - **Frequentist**: T-test, Chi-square, Bootstrap, Effect size, Power analysis
   - **Bayesian**: Beta-Binomial model, Posterior sampling, Credible intervals
   - Results exported to JSON for dashboard consumption

4. **Business Impact Calculation**
   - Incremental conversions and revenue
   - Cost analysis (CPA, total campaign cost)
   - ROI and ROAS calculation
   - Break-even analysis
   - Scaling projections

5. **Visualization & Reporting**
   - Interactive dashboard with real-time updates
   - Jupyter notebooks with mathematical explanations
   - Exportable results for stakeholder presentations

### Analysis Workflow

```
Raw Data (CSV)
    ↓
Data Quality Checks
    ↓
Exploratory Analysis
    ↓
Statistical Testing (Frequentist + Bayesian)
    ↓
Business Metrics Calculation
    ↓
JSON Results Generation
    ↓
Interactive Dashboard Visualization
    ↓
Jupyter Notebook Documentation
```

---

## 🛠️ Technologies Used

### Frontend Stack

| Technology | Version | Purpose |
|------------|---------|---------|
| **React** | 18.2.0 | UI framework for building interactive components |
| **TypeScript** | 5.0+ | Type safety and enhanced developer experience |
| **Vite** | 5.0.8 | Fast build tool and development server |
| **Recharts** | 2.10.3 | Data visualization library for React |
| **Tailwind CSS** | Latest | Utility-first CSS framework for styling |
| **Lucide React** | 0.294.0 | Modern icon library |

### Backend/Analysis Stack

| Technology | Version | Purpose |
|------------|---------|---------|
| **Python** | 3.8+ | Data analysis and statistical computing |
| **Pandas** | Latest | Data manipulation and analysis |
| **NumPy** | Latest | Numerical computing and array operations |
| **SciPy** | Latest | Statistical functions and hypothesis testing |
| **Matplotlib** | Latest | Static data visualization |
| **Seaborn** | Latest | Statistical data visualization |
| **Statsmodels** | Latest | Statistical modeling and power analysis |
| **Jupyter** | Latest | Interactive notebooks for documentation |

### Development Tools

- **Git**: Version control
- **npm**: Package management for Node.js
- **pip**: Package management for Python
- **ESLint/TypeScript**: Code quality and type checking

### Statistical Libraries

- **scipy.stats**: T-tests, chi-square tests, correlation tests
- **statsmodels.stats.power**: Statistical power analysis
- **scipy.stats.beta**: Beta distribution for Bayesian analysis
- **numpy.random**: Monte Carlo sampling for Bayesian inference

---

## 📁 Project Structure

```
ABMarketing/
├── src/                              # Frontend source code
│   ├── ab_test_dashboard.tsx       # Main React dashboard component
│   ├── main.jsx                      # React application entry point
│   └── index.css                     # Global styles with glassmorphism
│
├── public/                            # Static assets
│   ├── frequentist_results.json      # Frequentist statistical test results
│   ├── bayesian_results.json         # Bayesian analysis results
│   ├── business_impact_results.json  # Business metrics results
│   └── marketing_AB.csv              # Sample data (if included)
│
├── docs/                              # Documentation
│   ├── STATISTICAL_METHODS.md        # Detailed statistical methods guide
│   └── DEPLOYMENT.md                  # Deployment instructions
│
├── ab_test_eda.ipynb                 # Exploratory Data Analysis notebook
├── ab_test_frequentist.ipynb         # Frequentist statistical tests notebook
├── ab_test_bayesian.ipynb             # Bayesian analysis notebook
├── ab_test_business_impact.ipynb     # Business impact analysis notebook
│
├── ab_test_eda.py                    # EDA Python script
├── ab_test_frequentist.py            # Frequentist analysis script
├── ab_test_bayesian.py               # Bayesian analysis script
├── ab_test_business_impact.py        # Business metrics script
│
├── ab_test_prd.md                    # Product Requirements Document
├── PROJECT_SUMMARY.md                 # Executive project summary
├── QUICK_START.md                    # Quick setup guide
│
├── package.json                       # Node.js dependencies and scripts
├── vite.config.js                    # Vite build configuration
├── index.html                        # HTML entry point
├── .gitignore                        # Git ignore rules
├── LICENSE                           # MIT License
└── README.md                          # This file
```

---

## 🚀 Installation & Setup

### Prerequisites

- **Node.js**: 16.0.0 or higher
- **npm**: 7.0.0 or higher (comes with Node.js)
- **Python**: 3.8 or higher
- **pip**: Python package installer
- **Git**: For version control (optional)

### Step-by-Step Installation

#### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/ABMarketing.git
cd ABMarketing
```

#### 2. Install Node.js Dependencies

```bash
npm install
```

This installs:
- React and React DOM
- TypeScript types
- Recharts for visualization
- Vite for building
- Tailwind CSS and other dev dependencies

#### 3. Install Python Dependencies

```bash
pip install pandas numpy scipy matplotlib seaborn statsmodels jupyter
```

Or use a requirements file (create `requirements.txt`):
```txt
pandas>=1.5.0
numpy>=1.23.0
scipy>=1.9.0
matplotlib>=3.6.0
seaborn>=0.12.0
statsmodels>=0.13.0
jupyter>=1.0.0
```

Then install:
```bash
pip install -r requirements.txt
```

#### 4. (Optional) Generate Analysis Data

If you have `marketing_AB.csv` data file:

```bash
# Run Python scripts to generate JSON results
python ab_test_eda.py
python ab_test_frequentist.py
python ab_test_bayesian.py
python ab_test_business_impact.py
```

This generates JSON files in the `public/` directory that the dashboard will automatically load.

#### 5. Start Development Server

```bash
npm run dev
```

The dashboard will be available at **http://localhost:3000**

### Verification

1. Open http://localhost:3000 in your browser
2. You should see the dashboard with mock data (if JSON files aren't available)
3. Try adjusting the confidence level dropdown
4. Navigate through different tabs

---

## 📖 Usage Guide

### Running Statistical Analysis

#### Using Python Scripts

```bash
# 1. Exploratory Data Analysis
python ab_test_eda.py
# Output: Data quality report, conversion rates, temporal patterns

# 2. Frequentist Statistical Tests
python ab_test_frequentist.py
# Output: frequentist_results.json with t-test, chi-square, bootstrap results

# 3. Bayesian Analysis
python ab_test_bayesian.py
# Output: bayesian_results.json with posterior distributions and probabilities

# 4. Business Impact Calculation
python ab_test_business_impact.py
# Output: business_impact_results.json with ROAS, ROI, CPA metrics
```

#### Using Jupyter Notebooks

```bash
# Start Jupyter
jupyter notebook

# Open and run:
# - ab_test_eda.ipynb
# - ab_test_frequentist.ipynb
# - ab_test_bayesian.ipynb
# - ab_test_business_impact.ipynb
```

### Using the Dashboard

1. **Overview Tab**: View key metrics, conversion rates, and lift
2. **Statistics Tab**: 
   - Toggle between Frequentist and Bayesian methods
   - Adjust confidence level (90%, 95%, 99%)
   - View p-values, confidence intervals, effect sizes
3. **Visualizations Tab**: 
   - Time series charts
   - Distribution comparisons
   - Heat maps for optimal ad timing
4. **Insights Tab**: 
   - Test conclusions
   - Business recommendations
   - Risk assessment

### Exporting Results

Click the "Export JSON" button in the dashboard header to download all analysis results for:
- Further analysis in other tools
- Reporting to stakeholders
- Archiving test results

---

## 📐 Statistical Methods Explained

### Frequentist Approach

#### 1. Two-Sample T-Test (Welch's)

**Purpose**: Tests whether there is a statistically significant difference between two groups.

**Null Hypothesis (H₀)**: μ_ad = μ_psa  
**Alternative Hypothesis (H₁)**: μ_ad ≠ μ_psa

**Formula**:
$$t = \frac{\bar{x}_1 - \bar{x}_2}{\sqrt{\frac{s_1^2}{n_1} + \frac{s_2^2}{n_2}}}$$

**Degrees of Freedom (Welch's Approximation)**:
$$df = \frac{\left(\frac{s_1^2}{n_1} + \frac{s_2^2}{n_2}\right)^2}{\frac{(s_1^2/n_1)^2}{n_1-1} + \frac{(s_2^2/n_2)^2}{n_2-1}}$$

**Confidence Interval**:
$$CI = (\bar{x}_1 - \bar{x}_2) \pm t_{\alpha/2, df} \times SE$$

**Interpretation**:
- p < 0.05: Statistically significant difference
- p ≥ 0.05: No significant difference detected

#### 2. Chi-Square Test for Independence

**Purpose**: Tests whether group assignment and conversion are independent.

**Formula**:
$$\chi^2 = \sum \frac{(O_{ij} - E_{ij})^2}{E_{ij}}$$

**Expected Frequencies**:
$$E_{ij} = \frac{(\text{Row Total}_i) \times (\text{Column Total}_j)}{\text{Grand Total}}$$

**Degrees of Freedom**:
$$df = (r-1) \times (c-1)$$

#### 3. Bootstrap Confidence Intervals

**Purpose**: Non-parametric method for confidence interval estimation.

**Procedure**:
1. Resample n₁ observations from group 1 with replacement
2. Resample n₂ observations from group 2 with replacement
3. Calculate difference in means
4. Repeat B times (typically 10,000)
5. Use percentiles for confidence intervals

**Formula**:
$$CI = [Q_{\alpha/2}, Q_{1-\alpha/2}]$$

where Q_p is the p-th percentile of the bootstrap distribution.

#### 4. Effect Size (Cohen's h and d)

**Cohen's h (for Proportions)**:
$$h = 2 \times (\arcsin(\sqrt{p_1}) - \arcsin(\sqrt{p_2}))$$

**Cohen's d (for Continuous)**:
$$d = \frac{\mu_1 - \mu_2}{\sigma_{\text{pooled}}}$$

**Interpretation**:
- |h| < 0.2: Negligible effect
- 0.2 ≤ |h| < 0.5: Small effect
- 0.5 ≤ |h| < 0.8: Medium effect
- |h| ≥ 0.8: Large effect

#### 5. Statistical Power Analysis

**Purpose**: Assesses the probability of detecting a true effect.

**Power Formula**:
$$\text{Power} = 1 - \beta = P(\text{reject } H_0 | H_1 \text{ is true})$$

**Required Sample Size**:
$$n = \frac{2(z_{\alpha/2} + z_{\beta})^2 \sigma^2}{(\mu_1 - \mu_2)^2}$$

### Bayesian Approach

#### 1. Beta-Binomial Model

**Purpose**: Models conversion rates using conjugate prior for binary outcomes.

**Prior Distribution**: Beta(α, β) - We use uniform Beta(1, 1)

**Posterior Distribution**:
$$\text{Posterior} = \text{Beta}(\alpha + \text{successes}, \beta + \text{failures})$$

**Posterior Mean**:
$$E[p | \text{data}] = \frac{\alpha + \text{successes}}{\alpha + \beta + \text{total trials}}$$

**Probability Density Function**:
$$f(p | \alpha, \beta) = \frac{p^{\alpha-1}(1-p)^{\beta-1}}{B(\alpha, \beta)}$$

#### 2. Credible Intervals

**Purpose**: Bayesian equivalent of confidence intervals with intuitive interpretation.

**Interpretation**: "There is a 95% probability that the true value lies in this interval"

**Calculation**: Use inverse CDF (percentile function) of Beta distribution

#### 3. Probability of Superiority

**Purpose**: Direct probability statement about which group is better.

**Formula**: P(p_ad > p_psa | data)

**Estimation**: Sample from posterior distributions and calculate proportion where p_ad > p_psa

**Advantage**: More intuitive than p-values for business stakeholders

---

## 💼 Business Metrics

### Incremental Conversions

**Formula**:
$$\text{Incremental Conversions} = n_{\text{ad}} \times (CR_{\text{ad}} - CR_{\text{control}})$$

Represents conversions directly attributed to the advertising campaign.

### Return on Ad Spend (ROAS)

**Formula**:
$$\text{ROAS} = \frac{\text{Revenue}}{\text{Ad Spend}}$$

**Interpretation**:
- ROAS > 1.0: Campaign is profitable
- ROAS = 1.0: Break-even
- ROAS < 1.0: Campaign is losing money

### Return on Investment (ROI)

**Formula**:
$$\text{ROI} = \frac{\text{Revenue} - \text{Cost}}{\text{Cost}} = \text{ROAS} - 1$$

### Cost per Incremental Acquisition (CPA)

**Formula**:
$$\text{CPA} = \frac{\text{Total Campaign Cost}}{\text{Incremental Conversions}}$$

### Break-Even Analysis

**Break-Even Conversions**:
$$\text{Break-Even Conversions} = \frac{\text{Total Campaign Cost}}{\text{Value per Conversion}}$$

**Break-Even Conversion Rate**:
$$\text{Break-Even CR Lift} = \frac{\text{Break-Even Conversions}}{n_{\text{ad}}}$$

### Scaling Projections

For n users:
- **Projected Incremental Conversions**: n × (CR_ad - CR_psa)
- **Projected Revenue**: Projected Incremental Conversions × Value per Conversion
- **Projected Cost**: n × (Total Impressions / n_ad) × Cost per Impression

---

## 🎨 Dashboard Features

### Overview Tab

- **Key Metrics Summary**: Overall conversion rates, lift, sample sizes
- **Conversion Rate Comparison**: Side-by-side bar chart
- **Lift Visualization**: Horizontal bar showing relative lift
- **Group Details**: User counts, conversion counts, conversion rates

### Statistics Tab

- **Method Toggle**: Switch between Frequentist and Bayesian views
- **Confidence Level Adjuster**: Dropdown for 90%, 95%, 99%
- **Test Results Display**:
  - Frequentist: T-statistic, p-value, chi-square, effect sizes, power
  - Bayesian: Posterior means, credible intervals, probability of superiority
- **Dynamic Updates**: Confidence intervals recalculate in real-time

### Visualizations Tab

- **Time Series Charts**: Conversion patterns over time
- **Distribution Comparisons**: Histograms and density plots
- **Heat Maps**: Optimal ad timing by day and hour
- **Interactive Tooltips**: Hover for detailed information

### Insights Tab

- **Test Conclusions**: Summary of statistical significance
- **Business Recommendations**: Actionable insights based on results
- **Risk Assessment**: Potential risks and mitigations
- **Next Steps**: Recommended follow-up actions

---

## 📓 Jupyter Notebooks

The project includes four comprehensive Jupyter notebooks with detailed analysis:

### 1. `ab_test_eda.ipynb` - Exploratory Data Analysis

**Contents**:
- Data loading and initial inspection
- Data quality assessment (missing values, duplicates)
- Conversion rate analysis by group
- Dose-response analysis (ad exposure impact)
- Temporal pattern analysis (day/hour effects)
- Visualizations: Conversion rate comparisons, temporal patterns

**Key Sections**:
- Data Quality Assessment
- Conversion Rate Analysis with formulas
- Dose-Response Analysis with correlation tests
- Temporal Patterns Analysis

### 2. `ab_test_frequentist.ipynb` - Frequentist Statistical Analysis

**Contents**:
- Two-sample t-test (Welch's) with formulas
- Chi-square test for independence
- Effect size calculation (Cohen's h and d)
- Bootstrap confidence intervals
- Statistical power analysis
- Visualizations: Distribution comparisons, confidence intervals

**Key Sections**:
- Hypothesis testing with mathematical formulas
- Effect size interpretation
- Bootstrap methodology
- Power analysis and sample size requirements

### 3. `ab_test_bayesian.ipynb` - Bayesian Statistical Analysis

**Contents**:
- Beta-Binomial model setup
- Prior and posterior distributions
- Credible intervals calculation
- Probability of superiority
- Expected value calculations
- Visualizations: Posterior distributions, difference distributions

**Key Sections**:
- Beta-Binomial conjugate prior explanation
- Posterior distribution sampling (100,000 samples)
- Credible interval interpretation
- Business impact from posterior distributions

### 4. `ab_test_business_impact.ipynb` - Business Impact Analysis

**Contents**:
- Incremental conversions calculation
- Cost per incremental acquisition (CPA)
- Return on ad spend (ROAS)
- Return on investment (ROI)
- Break-even analysis
- Scaling projections
- Visualizations: ROAS comparison, revenue vs cost, scaling charts

**Key Sections**:
- Financial metrics with formulas
- Break-even point calculation
- Scaling projections for different user volumes
- Business recommendations based on metrics

**All Notebooks Include**:
- Executive summaries
- Mathematical formulas in LaTeX
- Step-by-step explanations
- Professional visualizations
- Summary sections with key findings

---

## 🚀 Deployment

### Build for Production

```bash
npm run build
```

This creates an optimized production build in the `dist/` directory.

### Deployment Options

#### Vercel (Recommended)

1. Push code to GitHub
2. Go to [vercel.com](https://vercel.com)
3. Click "New Project" and import repository
4. Configure:
   - Framework Preset: Vite
   - Build Command: `npm run build`
   - Output Directory: `dist`
5. Deploy!

**Advantages**: Automatic deployments, free tier, fast CDN

#### Netlify

1. Push code to GitHub
2. Go to [netlify.com](https://netlify.com)
3. Click "New site from Git"
4. Configure:
   - Build command: `npm run build`
   - Publish directory: `dist`
5. Deploy!

#### GitHub Pages

```bash
npm install -g gh-pages
npm run build
gh-pages -d dist
```

Then enable GitHub Pages in repository settings.

For detailed deployment instructions, see [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md).

---

## 🤝 Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Development Workflow

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Test thoroughly
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👤 Author

**Your Name**
- LinkedIn: [Your LinkedIn Profile](https://linkedin.com/in/yourprofile)
- GitHub: [@yourusername](https://github.com/yourusername)
- Portfolio: [Your Portfolio](https://yourportfolio.com)

---

## 🙏 Acknowledgments

- Statistical methods based on industry-standard A/B testing practices
- UI design inspired by modern glassmorphism trends
- Data visualization best practices from Recharts documentation
- Jupyter notebook structure inspired by data science best practices

---

## 📚 Additional Resources

- [Product Requirements Document](ab_test_prd.md) - Complete PRD
- [Project Summary](PROJECT_SUMMARY.md) - Executive summary
- [Statistical Methods Guide](docs/STATISTICAL_METHODS.md) - Detailed statistical explanations
- [Quick Start Guide](QUICK_START.md) - 5-minute setup
- [Deployment Guide](docs/DEPLOYMENT.md) - Deployment instructions

---

## 🎓 Key Learnings & Skills Demonstrated

This project demonstrates expertise in:

### Data Science & Statistics
- Hypothesis testing (t-test, chi-square)
- Bayesian inference (Beta-Binomial model)
- Bootstrap methods
- Effect size calculation
- Power analysis
- Confidence/Credible intervals

### Software Development
- React.js and TypeScript
- Python data analysis
- RESTful data handling
- Responsive design
- Code organization and documentation

### Business Intelligence
- Financial metrics (ROAS, ROI, CPA)
- Break-even analysis
- Scaling projections
- Data-driven decision making

### Professional Practices
- Comprehensive documentation
- Mathematical rigor
- Code quality and organization
- Deployment readiness

---

⭐ **If you found this project helpful, please consider giving it a star!**

---

## 📞 Support

For questions or issues:
- Open an issue on GitHub
- Check the [documentation](docs/)
- Review the [Jupyter notebooks](ab_test_eda.ipynb) for detailed analysis

---

**Last Updated**: November 2025  
**Version**: 1.0.0  
**Status**: ✅ Production Ready

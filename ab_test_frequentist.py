"""
Marketing A/B Test - Frequentist Statistical Analysis
======================================================
This notebook performs comprehensive frequentist statistical testing including:
- Two-sample t-test
- Chi-square test
- Bootstrap confidence intervals
- Effect size (Cohen's d/h)
- Power analysis
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from scipy.stats import chi2_contingency
from statsmodels.stats.power import TTestIndPower
import warnings
warnings.filterwarnings('ignore')

# Set style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

# ============================================================================
# 1. DATA LOADING
# ============================================================================

print("="*80)
print("MARKETING A/B TEST - FREQUENTIST STATISTICAL ANALYSIS")
print("="*80)

# Load data
df = pd.read_csv('marketing_AB.csv')

# Separate groups
ad_group = df[df['test group'] == 'ad']
psa_group = df[df['test group'] == 'psa']

# Extract conversion data
ad_conversions = ad_group['converted'].values
psa_conversions = psa_group['converted'].values

# Calculate conversion rates
cr_ad = ad_conversions.mean()
cr_psa = psa_conversions.mean()
n_ad = len(ad_conversions)
n_psa = len(psa_conversions)

print(f"\n📊 Sample Sizes:")
print(f"   Ad Group:  {n_ad:,}")
print(f"   PSA Group: {n_psa:,}")

print(f"\n📈 Conversion Rates:")
print(f"   Ad Group:  {cr_ad:.6f} ({cr_ad*100:.4f}%)")
print(f"   PSA Group: {cr_psa:.6f} ({cr_psa*100:.4f}%)")
print(f"   Difference: {cr_ad - cr_psa:.6f} ({(cr_ad - cr_psa)*100:.4f}%)")
print(f"   Relative Lift: {((cr_ad - cr_psa) / cr_psa * 100):.4f}%")

# ============================================================================
# 2. TWO-SAMPLE T-TEST
# ============================================================================

print("\n" + "="*80)
print("TWO-SAMPLE T-TEST")
print("="*80)

# Perform t-test (unequal variances)
t_stat, p_value = stats.ttest_ind(ad_conversions, psa_conversions, equal_var=False)

# Calculate standard errors
se_ad = np.std(ad_conversions, ddof=1) / np.sqrt(n_ad)
se_psa = np.std(psa_conversions, ddof=1) / np.sqrt(n_psa)
se_diff = np.sqrt(se_ad**2 + se_psa**2)

# Degrees of freedom (Welch's approximation)
var_ad = np.var(ad_conversions, ddof=1)
var_psa = np.var(psa_conversions, ddof=1)
df_welch = (se_ad**2 + se_psa**2)**2 / (se_ad**4/(n_ad-1) + se_psa**4/(n_psa-1))

# 95% Confidence interval
ci_95_lower = (cr_ad - cr_psa) - stats.t.ppf(0.975, df_welch) * se_diff
ci_95_upper = (cr_ad - cr_psa) + stats.t.ppf(0.975, df_welch) * se_diff

print(f"\n📊 Test Results:")
print(f"   T-statistic: {t_stat:.6f}")
print(f"   P-value: {p_value:.6f}")
print(f"   Degrees of Freedom (Welch): {df_welch:.2f}")
print(f"   95% CI for difference: [{ci_95_lower:.6f}, {ci_95_upper:.6f}]")
print(f"   95% CI for difference (%): [{(ci_95_lower*100):.4f}%, {(ci_95_upper*100):.4f}%]")

# Interpretation
alpha = 0.05
if p_value < alpha:
    significance = "Statistically Significant"
    symbol = "✅"
else:
    significance = "Not Statistically Significant"
    symbol = "⚠️"

print(f"\n{symbol} Interpretation:")
print(f"   {significance} (p < {alpha})")
if p_value < 0.001:
    print(f"   Highly significant (p < 0.001)")
elif p_value < 0.01:
    print(f"   Very significant (p < 0.01)")
elif p_value < 0.05:
    print(f"   Significant (p < 0.05)")
elif p_value < 0.10:
    print(f"   Marginally significant (p < 0.10)")

# ============================================================================
# 3. CHI-SQUARE TEST
# ============================================================================

print("\n" + "="*80)
print("CHI-SQUARE TEST FOR INDEPENDENCE")
print("="*80)

# Create contingency table
contingency_table = pd.crosstab(df['test group'], df['converted'])
print("\n📊 Contingency Table:")
print(contingency_table)

# Perform chi-square test
chi2, p_chi2, dof, expected = chi2_contingency(contingency_table)

print(f"\n📊 Chi-Square Test Results:")
print(f"   Chi-square statistic: {chi2:.6f}")
print(f"   P-value: {p_chi2:.6f}")
print(f"   Degrees of Freedom: {dof}")
print(f"\n   Expected Frequencies:")
print(pd.DataFrame(expected, index=contingency_table.index, columns=contingency_table.columns))

# Interpretation
if p_chi2 < alpha:
    print(f"\n✅ Groups are NOT independent (significant association)")
else:
    print(f"\n⚠️  Groups appear independent (no significant association)")

# ============================================================================
# 4. EFFECT SIZE (COHEN'S H)
# ============================================================================

print("\n" + "="*80)
print("EFFECT SIZE CALCULATION")
print("="*80)

# Cohen's h for proportions (arcsine transformation)
def cohens_h(p1, p2):
    """Calculate Cohen's h for two proportions"""
    h = 2 * (np.arcsin(np.sqrt(p1)) - np.arcsin(np.sqrt(p2)))
    return h

# Cohen's d (for continuous, using conversion rates as means)
pooled_std = np.sqrt(((n_ad - 1) * var_ad + (n_psa - 1) * var_psa) / (n_ad + n_psa - 2))
cohens_d = (cr_ad - cr_psa) / pooled_std if pooled_std > 0 else 0

# Cohen's h
cohens_h_value = cohens_h(cr_ad, cr_psa)

print(f"\n📊 Effect Size Metrics:")
print(f"   Cohen's h: {cohens_h_value:.6f}")
print(f"   Cohen's d: {cohens_d:.6f}")

# Interpretation
def interpret_effect_size_h(h):
    """Interpret Cohen's h"""
    abs_h = abs(h)
    if abs_h < 0.2:
        return "Negligible"
    elif abs_h < 0.5:
        return "Small"
    elif abs_h < 0.8:
        return "Medium"
    else:
        return "Large"

effect_interpretation = interpret_effect_size_h(cohens_h_value)
print(f"\n📈 Effect Size Interpretation:")
print(f"   {effect_interpretation} effect (|h| = {abs(cohens_h_value):.4f})")

# ============================================================================
# 5. BOOTSTRAP CONFIDENCE INTERVALS
# ============================================================================

print("\n" + "="*80)
print("BOOTSTRAP CONFIDENCE INTERVALS")
print("="*80)

def bootstrap_ci(data1, data2, n_bootstrap=10000, ci_level=0.95):
    """Calculate bootstrap confidence interval for difference in means"""
    n1, n2 = len(data1), len(data2)
    differences = []
    
    for _ in range(n_bootstrap):
        # Resample with replacement
        sample1 = np.random.choice(data1, size=n1, replace=True)
        sample2 = np.random.choice(data2, size=n2, replace=True)
        # Calculate difference
        diff = sample1.mean() - sample2.mean()
        differences.append(diff)
    
    differences = np.array(differences)
    alpha = 1 - ci_level
    lower = np.percentile(differences, 100 * alpha/2)
    upper = np.percentile(differences, 100 * (1 - alpha/2))
    
    return lower, upper, differences

print(f"\n🔄 Running Bootstrap (10,000 iterations)...")
bootstrap_lower, bootstrap_upper, bootstrap_diffs = bootstrap_ci(
    ad_conversions, psa_conversions, n_bootstrap=10000, ci_level=0.95
)

print(f"\n📊 Bootstrap Results:")
print(f"   95% CI for difference: [{bootstrap_lower:.6f}, {bootstrap_upper:.6f}]")
print(f"   95% CI for difference (%): [{(bootstrap_lower*100):.4f}%, {(bootstrap_upper*100):.4f}%]")
print(f"   Bootstrap mean difference: {bootstrap_diffs.mean():.6f}")
print(f"   Bootstrap std error: {bootstrap_diffs.std():.6f}")

# ============================================================================
# 6. POWER ANALYSIS
# ============================================================================

print("\n" + "="*80)
print("STATISTICAL POWER ANALYSIS")
print("="*80)

# Observed effect size
observed_effect = cr_ad - cr_psa

# Calculate achieved power
power_analysis = TTestIndPower()
achieved_power = power_analysis.power(
    effect_size=cohens_d,
    nobs1=n_ad,
    ratio=n_psa/n_ad,
    alpha=0.05,
    alternative='two-sided'
)

print(f"\n📊 Power Analysis Results:")
print(f"   Observed effect size (Cohen's d): {cohens_d:.6f}")
print(f"   Sample size (Ad): {n_ad:,}")
print(f"   Sample size (PSA): {n_psa:,}")
print(f"   Achieved power: {achieved_power:.4f} ({achieved_power*100:.2f}%)")

# Calculate required sample size for 80% power
required_n = power_analysis.solve_power(
    effect_size=cohens_d,
    power=0.80,
    ratio=1.0,
    alpha=0.05,
    alternative='two-sided'
)

print(f"\n📈 Sample Size Requirements:")
print(f"   Required sample size per group (80% power): {int(np.ceil(required_n)):,}")
print(f"   Current sample size (Ad): {n_ad:,}")
if n_ad >= required_n:
    print(f"   ✅ Sample size is adequate")
else:
    print(f"   ⚠️  Sample size may be insufficient")

# ============================================================================
# 7. SUMMARY STATISTICS
# ============================================================================

print("\n" + "="*80)
print("SUMMARY STATISTICS")
print("="*80)

summary = {
    'ad_group_size': n_ad,
    'psa_group_size': n_psa,
    'ad_conversion_rate': cr_ad,
    'psa_conversion_rate': cr_psa,
    'absolute_lift': cr_ad - cr_psa,
    'relative_lift': (cr_ad - cr_psa) / cr_psa,
    't_statistic': t_stat,
    'p_value': p_value,
    'chi2_statistic': chi2,
    'chi2_p_value': p_chi2,
    'cohens_h': cohens_h_value,
    'cohens_d': cohens_d,
    'ci_95_lower': ci_95_lower,
    'ci_95_upper': ci_95_upper,
    'bootstrap_ci_lower': bootstrap_lower,
    'bootstrap_ci_upper': bootstrap_upper,
    'statistical_power': achieved_power,
    'required_sample_size': int(np.ceil(required_n)),
    'is_significant': p_value < 0.05
}

print("\n📋 Key Metrics:")
for key, value in summary.items():
    if isinstance(value, float):
        print(f"   {key}: {value:.6f}")
    else:
        print(f"   {key}: {value}")

# Save summary
import json
with open('frequentist_results.json', 'w') as f:
    json.dump({k: float(v) if isinstance(v, (np.integer, np.floating)) else v 
              for k, v in summary.items()}, f, indent=2)

print("\n💾 Results saved to 'frequentist_results.json'")

print("\n" + "="*80)
print("FREQUENTIST ANALYSIS COMPLETE ✓")
print("="*80)


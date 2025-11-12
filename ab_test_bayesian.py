"""
Marketing A/B Test - Bayesian Statistical Analysis
====================================================
This notebook performs comprehensive Bayesian analysis including:
- Beta-binomial model for conversion rates
- Posterior distributions
- Credible intervals
- Probability of superiority
- Expected value calculations
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from scipy.stats import beta
import warnings
warnings.filterwarnings('ignore')

# Set style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

# ============================================================================
# 1. DATA LOADING
# ============================================================================

print("="*80)
print("MARKETING A/B TEST - BAYESIAN STATISTICAL ANALYSIS")
print("="*80)

# Load data
df = pd.read_csv('marketing_AB.csv')

# Separate groups
ad_group = df[df['test group'] == 'ad']
psa_group = df[df['test group'] == 'psa']

# Extract conversion data
ad_conversions = ad_group['converted'].sum()
ad_non_conversions = len(ad_group) - ad_conversions
n_ad = len(ad_group)

psa_conversions = psa_group['converted'].sum()
psa_non_conversions = len(psa_group) - psa_conversions
n_psa = len(psa_group)

print(f"\n📊 Sample Sizes:")
print(f"   Ad Group:  {n_ad:,} (Conversions: {ad_conversions:,}, Non-conversions: {ad_non_conversions:,})")
print(f"   PSA Group: {n_psa:,} (Conversions: {psa_conversions:,}, Non-conversions: {psa_non_conversions:,})")

# Observed conversion rates
cr_ad = ad_conversions / n_ad
cr_psa = psa_conversions / n_psa

print(f"\n📈 Observed Conversion Rates:")
print(f"   Ad Group:  {cr_ad:.6f} ({cr_ad*100:.4f}%)")
print(f"   PSA Group: {cr_psa:.6f} ({cr_psa*100:.4f}%)")
print(f"   Difference: {cr_ad - cr_psa:.6f} ({(cr_ad - cr_psa)*100:.4f}%)")

# ============================================================================
# 2. BETA-BINOMIAL MODEL
# ============================================================================

print("\n" + "="*80)
print("BETA-BINOMIAL MODEL")
print("="*80)

# Prior parameters (non-informative uniform prior: Beta(1, 1))
alpha_prior_ad = 1
beta_prior_ad = 1
alpha_prior_psa = 1
beta_prior_psa = 1

# Posterior parameters (Beta(alpha + successes, beta + failures))
alpha_post_ad = alpha_prior_ad + ad_conversions
beta_post_ad = beta_prior_ad + ad_non_conversions

alpha_post_psa = alpha_prior_psa + psa_conversions
beta_post_psa = beta_prior_psa + psa_non_conversions

print(f"\n📊 Prior Distribution (Non-informative):")
print(f"   Ad Group:  Beta({alpha_prior_ad}, {beta_prior_ad})")
print(f"   PSA Group: Beta({alpha_prior_psa}, {beta_prior_psa})")

print(f"\n📊 Posterior Distribution:")
print(f"   Ad Group:  Beta({alpha_post_ad:.1f}, {beta_post_ad:.1f})")
print(f"   PSA Group: Beta({alpha_post_psa:.1f}, {beta_post_psa:.1f})")

# Posterior means (expected conversion rates)
post_mean_ad = alpha_post_ad / (alpha_post_ad + beta_post_ad)
post_mean_psa = alpha_post_psa / (alpha_post_psa + beta_post_psa)

print(f"\n📈 Posterior Mean Conversion Rates:")
print(f"   Ad Group:  {post_mean_ad:.6f} ({post_mean_ad*100:.4f}%)")
print(f"   PSA Group: {post_mean_psa:.6f} ({post_mean_psa*100:.4f}%)")
print(f"   Expected Lift: {(post_mean_ad - post_mean_psa) / post_mean_psa * 100:.4f}%")

# ============================================================================
# 3. POSTERIOR DISTRIBUTIONS
# ============================================================================

print("\n" + "="*80)
print("POSTERIOR DISTRIBUTION ANALYSIS")
print("="*80)

# Generate samples from posterior distributions
n_samples = 100000
posterior_ad_samples = np.random.beta(alpha_post_ad, beta_post_ad, n_samples)
posterior_psa_samples = np.random.beta(alpha_post_psa, beta_post_psa, n_samples)

# Difference distribution
posterior_diff_samples = posterior_ad_samples - posterior_psa_samples

# Calculate statistics
print(f"\n📊 Posterior Distribution Statistics:")
print(f"   Ad Group Mean: {posterior_ad_samples.mean():.6f}")
print(f"   Ad Group Std:  {posterior_ad_samples.std():.6f}")
print(f"   PSA Group Mean: {posterior_psa_samples.mean():.6f}")
print(f"   PSA Group Std:  {posterior_psa_samples.std():.6f}")
print(f"   Difference Mean: {posterior_diff_samples.mean():.6f}")
print(f"   Difference Std:  {posterior_diff_samples.std():.6f}")

# ============================================================================
# 4. CREDIBLE INTERVALS
# ============================================================================

print("\n" + "="*80)
print("CREDIBLE INTERVALS")
print("="*80)

# 95% Credible intervals
ci_level = 0.95
alpha_ci = 1 - ci_level

# For Ad group
ad_ci_lower = np.percentile(posterior_ad_samples, 100 * alpha_ci / 2)
ad_ci_upper = np.percentile(posterior_ad_samples, 100 * (1 - alpha_ci / 2))

# For PSA group
psa_ci_lower = np.percentile(posterior_psa_samples, 100 * alpha_ci / 2)
psa_ci_upper = np.percentile(posterior_psa_samples, 100 * (1 - alpha_ci / 2))

# For difference
diff_ci_lower = np.percentile(posterior_diff_samples, 100 * alpha_ci / 2)
diff_ci_upper = np.percentile(posterior_diff_samples, 100 * (1 - alpha_ci / 2))

print(f"\n📊 {ci_level*100:.0f}% Credible Intervals:")
print(f"   Ad Group Conversion Rate:")
print(f"      [{ad_ci_lower:.6f}, {ad_ci_upper:.6f}]")
print(f"      [{(ad_ci_lower*100):.4f}%, {(ad_ci_upper*100):.4f}%]")
print(f"   PSA Group Conversion Rate:")
print(f"      [{psa_ci_lower:.6f}, {psa_ci_upper:.6f}]")
print(f"      [{(psa_ci_lower*100):.4f}%, {(psa_ci_upper*100):.4f}%]")
print(f"   Difference (Ad - PSA):")
print(f"      [{diff_ci_lower:.6f}, {diff_ci_upper:.6f}]")
print(f"      [{(diff_ci_lower*100):.4f}%, {(diff_ci_upper*100):.4f}%]")

# Check if credible interval excludes zero
if diff_ci_lower > 0:
    print(f"\n✅ Credible interval excludes zero - Ad group is superior")
elif diff_ci_upper < 0:
    print(f"\n✅ Credible interval excludes zero - PSA group is superior")
else:
    print(f"\n⚠️  Credible interval includes zero - No clear superiority")

# ============================================================================
# 5. PROBABILITY OF SUPERIORITY
# ============================================================================

print("\n" + "="*80)
print("PROBABILITY OF SUPERIORITY")
print("="*80)

# Probability that Ad > PSA
prob_ad_better = np.mean(posterior_ad_samples > posterior_psa_samples)
prob_psa_better = np.mean(posterior_psa_samples > posterior_ad_samples)
prob_equal = 1 - prob_ad_better - prob_psa_better

print(f"\n📊 Probability Estimates:")
print(f"   P(Ad > PSA): {prob_ad_better:.6f} ({prob_ad_better*100:.4f}%)")
print(f"   P(PSA > Ad): {prob_psa_better:.6f} ({prob_psa_better*100:.4f}%)")
print(f"   P(Equal):    {prob_equal:.6f} ({prob_equal*100:.4f}%)")

# Probability of meaningful lift (e.g., > 1% relative lift)
min_lift = 0.01
prob_meaningful_lift = np.mean((posterior_ad_samples - posterior_psa_samples) / posterior_psa_samples > min_lift)
print(f"\n📈 Probability of >{min_lift*100:.0f}% relative lift:")
print(f"   P(Lift > {min_lift*100:.0f}%): {prob_meaningful_lift:.6f} ({prob_meaningful_lift*100:.4f}%)")

# Interpretation
if prob_ad_better > 0.95:
    interpretation = "Very Strong Evidence"
    symbol = "✅✅"
elif prob_ad_better > 0.90:
    interpretation = "Strong Evidence"
    symbol = "✅"
elif prob_ad_better > 0.75:
    interpretation = "Moderate Evidence"
    symbol = "✓"
elif prob_ad_better > 0.50:
    interpretation = "Weak Evidence"
    symbol = "⚠️"
else:
    interpretation = "No Evidence"
    symbol = "❌"

print(f"\n{symbol} Interpretation:")
print(f"   {interpretation} that Ad group is superior")

# ============================================================================
# 6. EXPECTED VALUE CALCULATIONS
# ============================================================================

print("\n" + "="*80)
print("EXPECTED VALUE CALCULATIONS")
print("="*80)

# Assume a value per conversion (e.g., $100)
value_per_conversion = 100

# Expected incremental conversions
expected_incremental_conversions = (post_mean_ad - post_mean_psa) * n_ad

# Expected incremental revenue
expected_incremental_revenue = expected_incremental_conversions * value_per_conversion

print(f"\n📊 Expected Business Impact (assuming ${value_per_conversion} per conversion):")
print(f"   Expected incremental conversion rate: {post_mean_ad - post_mean_psa:.6f}")
print(f"   Expected incremental conversions: {expected_incremental_conversions:.2f}")
print(f"   Expected incremental revenue: ${expected_incremental_revenue:,.2f}")

# Distribution of expected revenue
revenue_samples = (posterior_ad_samples - posterior_psa_samples) * n_ad * value_per_conversion
revenue_ci_lower = np.percentile(revenue_samples, 2.5)
revenue_ci_upper = np.percentile(revenue_samples, 97.5)

print(f"\n📈 Revenue Distribution:")
print(f"   Mean: ${revenue_samples.mean():,.2f}")
print(f"   95% Credible Interval: [${revenue_ci_lower:,.2f}, ${revenue_ci_upper:,.2f}]")

# ============================================================================
# 7. POSTERIOR PREDICTIVE DISTRIBUTION
# ============================================================================

print("\n" + "="*80)
print("POSTERIOR PREDICTIVE DISTRIBUTION")
print("="*80)

# For future users, what's the predicted conversion rate?
# Sample from posterior, then sample from binomial
future_n = 10000
posterior_predictive_samples = []

for _ in range(1000):
    # Sample conversion rate from posterior
    p_ad = np.random.beta(alpha_post_ad, beta_post_ad)
    p_psa = np.random.beta(alpha_post_psa, beta_post_psa)
    # Sample future conversions
    future_ad = np.random.binomial(future_n, p_ad)
    future_psa = np.random.binomial(future_n, p_psa)
    posterior_predictive_samples.append({
        'ad_rate': future_ad / future_n,
        'psa_rate': future_psa / future_n,
        'lift': (future_ad / future_n - future_psa / future_n) / (future_psa / future_n)
    })

predictive_df = pd.DataFrame(posterior_predictive_samples)

print(f"\n📊 Predicted Performance for {future_n:,} future users:")
print(f"   Expected Ad conversion rate: {predictive_df['ad_rate'].mean():.6f}")
print(f"   Expected PSA conversion rate: {predictive_df['psa_rate'].mean():.6f}")
print(f"   Expected lift: {predictive_df['lift'].mean()*100:.4f}%")
print(f"   95% CI for lift: [{predictive_df['lift'].quantile(0.025)*100:.4f}%, {predictive_df['lift'].quantile(0.975)*100:.4f}%]")

# ============================================================================
# 8. SUMMARY STATISTICS
# ============================================================================

print("\n" + "="*80)
print("SUMMARY STATISTICS")
print("="*80)

summary = {
    'ad_group_size': n_ad,
    'psa_group_size': n_psa,
    'ad_conversions': ad_conversions,
    'psa_conversions': psa_conversions,
    'ad_conversion_rate': cr_ad,
    'psa_conversion_rate': cr_psa,
    'posterior_mean_ad': post_mean_ad,
    'posterior_mean_psa': post_mean_psa,
    'expected_lift': (post_mean_ad - post_mean_psa) / post_mean_psa,
    'prob_ad_better': prob_ad_better,
    'prob_meaningful_lift': prob_meaningful_lift,
    'credible_interval_lower': diff_ci_lower,
    'credible_interval_upper': diff_ci_upper,
    'expected_incremental_conversions': expected_incremental_conversions,
    'expected_incremental_revenue': expected_incremental_revenue,
    'revenue_ci_lower': revenue_ci_lower,
    'revenue_ci_upper': revenue_ci_upper
}

print("\n📋 Key Metrics:")
for key, value in summary.items():
    if isinstance(value, float):
        print(f"   {key}: {value:.6f}")
    else:
        print(f"   {key}: {value}")

# Save summary
import json
with open('bayesian_results.json', 'w') as f:
    json.dump({k: float(v) if isinstance(v, (np.integer, np.floating)) else v 
              for k, v in summary.items()}, f, indent=2)

print("\n💾 Results saved to 'bayesian_results.json'")

print("\n" + "="*80)
print("BAYESIAN ANALYSIS COMPLETE ✓")
print("="*80)


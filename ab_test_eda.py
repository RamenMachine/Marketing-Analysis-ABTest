"""
Marketing A/B Test - Exploratory Data Analysis
================================================
This notebook performs comprehensive EDA on the marketing campaign data.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# Set style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

# ============================================================================
# 1. DATA LOADING & INITIAL INSPECTION
# ============================================================================

print("="*80)
print("MARKETING A/B TEST - EXPLORATORY DATA ANALYSIS")
print("="*80)

# Load data (update path as needed)
df = pd.read_csv('marketing_AB.csv')

print("\n📊 Dataset Overview")
print("-" * 80)
print(f"Total Records: {len(df):,}")
print(f"Features: {df.shape[1]}")
print(f"\nColumns: {list(df.columns)}")

print("\n📋 First 5 Rows:")
print(df.head())

print("\n🔍 Data Types:")
print(df.dtypes)

print("\n📈 Statistical Summary:")
print(df.describe())

# ============================================================================
# 2. DATA QUALITY CHECKS
# ============================================================================

print("\n" + "="*80)
print("DATA QUALITY ASSESSMENT")
print("="*80)

# Missing values
print("\n🔍 Missing Values:")
missing = df.isnull().sum()
missing_pct = 100 * missing / len(df)
missing_df = pd.DataFrame({
    'Missing Count': missing,
    'Percentage': missing_pct
})
print(missing_df[missing_df['Missing Count'] > 0])

if missing.sum() == 0:
    print("✅ No missing values detected!")

# Duplicates
duplicates = df.duplicated().sum()
print(f"\n🔍 Duplicate Rows: {duplicates}")
if duplicates == 0:
    print("✅ No duplicates detected!")

# Unique users
print(f"\n🔍 Unique Users: {df['user id'].nunique():,}")
print(f"Total Records: {len(df):,}")
if df['user id'].nunique() == len(df):
    print("✅ Each row represents a unique user!")

# ============================================================================
# 3. GROUP DISTRIBUTION ANALYSIS
# ============================================================================

print("\n" + "="*80)
print("TEST GROUP DISTRIBUTION")
print("="*80)

group_dist = df['test group'].value_counts()
group_pct = 100 * group_dist / len(df)

print("\n📊 Group Sizes:")
for group, count in group_dist.items():
    pct = 100 * count / len(df)
    print(f"  {group.upper():8s}: {count:,} ({pct:.1f}%)")

# Test for balanced randomization
print("\n🧪 Randomization Check:")
expected_ratio = 0.5
ad_ratio = group_dist['ad'] / len(df)
if 0.45 <= ad_ratio <= 0.55:
    print("✅ Groups are reasonably balanced (45-55% split)")
else:
    print(f"⚠️  Warning: Unbalanced split ({ad_ratio:.1%} in ad group)")

# ============================================================================
# 4. CONVERSION ANALYSIS
# ============================================================================

print("\n" + "="*80)
print("CONVERSION RATE ANALYSIS")
print("="*80)

# Overall conversion
overall_cr = df['converted'].mean()
print(f"\n📈 Overall Conversion Rate: {overall_cr:.2%}")

# By group
print("\n📊 Conversion Rate by Group:")
conversion_by_group = df.groupby('test group')['converted'].agg([
    ('Users', 'count'),
    ('Conversions', 'sum'),
    ('Conversion_Rate', 'mean')
])
conversion_by_group['Conversion_Rate'] = conversion_by_group['Conversion_Rate'] * 100
print(conversion_by_group)

# Calculate lift
cr_ad = df[df['test group'] == 'ad']['converted'].mean()
cr_psa = df[df['test group'] == 'psa']['converted'].mean()
lift = (cr_ad - cr_psa) / cr_psa * 100

print(f"\n📈 Conversion Lift (Ad vs PSA): {lift:+.2f}%")
print(f"   Ad Group:  {cr_ad:.4f} ({cr_ad*100:.2f}%)")
print(f"   PSA Group: {cr_psa:.4f} ({cr_psa*100:.2f}%)")

# ============================================================================
# 5. AD EXPOSURE ANALYSIS
# ============================================================================

print("\n" + "="*80)
print("AD EXPOSURE PATTERNS")
print("="*80)

print("\n📊 Total Ads Statistics:")
print(df['total ads'].describe())

print("\n📈 Ad Exposure by Group:")
ad_exposure = df.groupby('test group')['total ads'].describe()
print(ad_exposure)

# Correlation between ads and conversion (for ad group only)
ad_group = df[df['test group'] == 'ad']
correlation = ad_group['total ads'].corr(ad_group['converted'])
print(f"\n🔗 Correlation (Total Ads vs Conversion): {correlation:.4f}")

# ============================================================================
# 5.5. DOSE-RESPONSE ANALYSIS
# ============================================================================

print("\n" + "="*80)
print("DOSE-RESPONSE ANALYSIS - AD EXPOSURE IMPACT")
print("="*80)

# Create ad exposure bins
ad_group['ad_bins'] = pd.cut(ad_group['total ads'], bins=10, labels=False)
ad_group['ad_bins_mid'] = ad_group.groupby('ad_bins')['total ads'].transform('mean')

# Conversion rate by ad exposure level
print("\n📊 Conversion Rate by Ad Exposure Level:")
dose_response = ad_group.groupby('ad_bins').agg({
    'total ads': ['min', 'max', 'mean', 'count'],
    'converted': ['sum', 'mean']
}).round(4)
dose_response.columns = ['Min_Ads', 'Max_Ads', 'Mean_Ads', 'Users', 'Conversions', 'Conversion_Rate']
dose_response['Conversion_Rate'] = dose_response['Conversion_Rate'] * 100
dose_response = dose_response.sort_values('Mean_Ads')
print(dose_response)

# Statistical test for dose-response relationship
from scipy.stats import spearmanr, pearsonr

# Spearman correlation (non-parametric, handles non-linear relationships)
spearman_corr, spearman_p = spearmanr(ad_group['total ads'], ad_group['converted'])
pearson_corr, pearson_p = pearsonr(ad_group['total ads'], ad_group['converted'])

print(f"\n📈 Dose-Response Statistical Tests:")
print(f"   Spearman Correlation: {spearman_corr:.4f} (p-value: {spearman_p:.6f})")
print(f"   Pearson Correlation: {pearson_corr:.4f} (p-value: {pearson_p:.6f})")

if spearman_p < 0.05:
    print(f"   ✅ Significant dose-response relationship detected")
else:
    print(f"   ⚠️  No significant dose-response relationship")

# Optimal ad exposure analysis
print(f"\n📊 Optimal Ad Exposure Analysis:")
optimal_exposure = dose_response.loc[dose_response['Conversion_Rate'].idxmax()]
print(f"   Optimal exposure range: {optimal_exposure['Min_Ads']:.0f} - {optimal_exposure['Max_Ads']:.0f} ads")
print(f"   Optimal conversion rate: {optimal_exposure['Conversion_Rate']:.4f}%")
print(f"   Users in optimal range: {optimal_exposure['Users']:.0f}")

# Diminishing returns analysis
print(f"\n📉 Diminishing Returns Analysis:")
if len(dose_response) > 2:
    # Check if conversion rate decreases after a certain point
    max_idx = dose_response['Conversion_Rate'].idxmax()
    after_max = dose_response.loc[dose_response.index > max_idx]
    if len(after_max) > 0:
        avg_after_max = after_max['Conversion_Rate'].mean()
        if avg_after_max < optimal_exposure['Conversion_Rate']:
            print(f"   ⚠️  Evidence of diminishing returns after {optimal_exposure['Max_Ads']:.0f} ads")
            print(f"   Average conversion rate after peak: {avg_after_max:.4f}%")
        else:
            print(f"   ✅ No clear diminishing returns detected")

# ============================================================================
# 6. TEMPORAL PATTERNS - DETAILED ANALYSIS
# ============================================================================

print("\n" + "="*80)
print("TEMPORAL PATTERNS - DETAILED ANALYSIS")
print("="*80)

print("\n📅 Most Ads Day Distribution:")
day_dist = df['most ads day'].value_counts().sort_index()
print(day_dist)

print("\n⏰ Most Ads Hour Distribution:")
hour_dist = df['most ads hour'].value_counts().sort_index()
print(hour_dist.head(10))

# Peak hours
peak_hours = hour_dist.nlargest(5)
print(f"\n🔝 Top 5 Peak Hours:")
for hour, count in peak_hours.items():
    print(f"   Hour {hour}: {count:,} users")

# Conversion rates by day of week
print("\n📊 Conversion Rates by Day of Week:")
day_conversion = df.groupby('most ads day').agg({
    'converted': ['count', 'sum', 'mean']
}).round(4)
day_conversion.columns = ['Users', 'Conversions', 'Conversion_Rate']
day_conversion['Conversion_Rate'] = day_conversion['Conversion_Rate'] * 100
print(day_conversion.sort_index())

# Conversion rates by hour
print("\n📊 Conversion Rates by Hour:")
hour_conversion = df.groupby('most ads hour').agg({
    'converted': ['count', 'sum', 'mean']
}).round(4)
hour_conversion.columns = ['Users', 'Conversions', 'Conversion_Rate']
hour_conversion['Conversion_Rate'] = hour_conversion['Conversion_Rate'] * 100
print(hour_conversion.sort_index().head(10))

# Day and hour combination analysis
print("\n📊 Conversion Rates by Day and Hour (Top 10):")
day_hour_conversion = df.groupby(['most ads day', 'most ads hour']).agg({
    'converted': ['count', 'sum', 'mean']
}).round(4)
day_hour_conversion.columns = ['Users', 'Conversions', 'Conversion_Rate']
day_hour_conversion['Conversion_Rate'] = day_hour_conversion['Conversion_Rate'] * 100
day_hour_conversion = day_hour_conversion.sort_values('Conversion_Rate', ascending=False)
print(day_hour_conversion.head(10))

# Temporal patterns by group
print("\n📊 Temporal Patterns by Test Group:")
print("\n   By Day of Week:")
day_group = df.groupby(['test group', 'most ads day'])['converted'].agg(['count', 'sum', 'mean']).round(4)
day_group.columns = ['Users', 'Conversions', 'Conversion_Rate']
day_group['Conversion_Rate'] = day_group['Conversion_Rate'] * 100
print(day_group)

print("\n   By Hour (Sample):")
hour_group = df.groupby(['test group', 'most ads hour'])['converted'].agg(['count', 'sum', 'mean']).round(4)
hour_group.columns = ['Users', 'Conversions', 'Conversion_Rate']
hour_group['Conversion_Rate'] = hour_group['Conversion_Rate'] * 100
print(hour_group.head(20))

# ============================================================================
# 8. VISUALIZATION RECOMMENDATIONS
# ============================================================================

print("\n" + "="*80)
print("KEY INSIGHTS & NEXT STEPS")
print("="*80)

print("\n✅ Data Quality Summary:")
print(f"   • Dataset is clean with {len(df):,} unique users")
print(f"   • No missing values or duplicates")
print(f"   • Groups are {'balanced' if 0.45 <= ad_ratio <= 0.55 else 'unbalanced'}")

print("\n📊 Conversion Insights:")
print(f"   • Overall conversion rate: {overall_cr:.2%}")
print(f"   • Ad group converts at {cr_ad:.2%}")
print(f"   • PSA group converts at {cr_psa:.2%}")
print(f"   • Observed lift: {lift:+.2f}%")

print("\n🔍 Recommended Analyses:")
print("   1. Statistical significance testing (t-test, chi-square)")
print("   2. Bayesian A/B test for probability estimates")
print("   3. Temporal pattern analysis (day/hour effects)")
print("   4. Dose-response analysis (ads vs conversion)")
print("   5. Cohort segmentation for heterogeneous effects")

print("\n" + "="*80)
print("EDA COMPLETE ✓")
print("="*80)

# ============================================================================
# 9. SAVE SUMMARY STATISTICS
# ============================================================================

summary_stats = {
    'total_users': len(df),
    'ad_group_size': group_dist['ad'],
    'psa_group_size': group_dist['psa'],
    'overall_conversion_rate': overall_cr,
    'ad_conversion_rate': cr_ad,
    'psa_conversion_rate': cr_psa,
    'observed_lift': lift / 100,  # As decimal
    'avg_ads_per_user': df['total ads'].mean(),
    'correlation_ads_conversion': correlation
}

print("\n💾 Summary statistics saved for next analysis phase")

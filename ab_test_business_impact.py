"""
Marketing A/B Test - Business Impact Analysis
==============================================
This notebook calculates business metrics including:
- Incremental conversions
- Cost per incremental acquisition (CPA)
- Return on ad spend (ROAS)
- Revenue attribution
- Break-even analysis
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import json
import warnings
warnings.filterwarnings('ignore')

# Set style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

# ============================================================================
# 1. DATA LOADING & ASSUMPTIONS
# ============================================================================

print("="*80)
print("MARKETING A/B TEST - BUSINESS IMPACT ANALYSIS")
print("="*80)

# Load data
df = pd.read_csv('marketing_AB.csv')

# Load statistical results if available
try:
    with open('frequentist_results.json', 'r') as f:
        frequentist_results = json.load(f)
except FileNotFoundError:
    print("⚠️  Frequentist results not found. Calculating from data...")
    frequentist_results = None

try:
    with open('bayesian_results.json', 'r') as f:
        bayesian_results = json.load(f)
except FileNotFoundError:
    print("⚠️  Bayesian results not found. Calculating from data...")
    bayesian_results = None

# Business assumptions (can be customized)
ASSUMPTIONS = {
    'value_per_conversion': 100,  # Revenue per conversion in dollars
    'cost_per_ad_impression': 0.01,  # Cost per ad shown
    'ad_group_total_ads': None,  # Will calculate from data
    'total_campaign_cost': None,  # Will calculate
    'marginal_cost_per_conversion': 0,  # Additional cost beyond ad spend
}

# Calculate from data if not provided
if ASSUMPTIONS['ad_group_total_ads'] is None:
    ad_group = df[df['test group'] == 'ad']
    ASSUMPTIONS['ad_group_total_ads'] = ad_group['total ads'].sum()

print(f"\n📊 Business Assumptions:")
for key, value in ASSUMPTIONS.items():
    if value is not None:
        if isinstance(value, float):
            print(f"   {key}: ${value:,.2f}" if 'cost' in key or 'value' in key else f"   {key}: {value:,.2f}")
        else:
            print(f"   {key}: {value:,}")

# ============================================================================
# 2. CONVERSION METRICS
# ============================================================================

print("\n" + "="*80)
print("CONVERSION METRICS")
print("="*80)

# Separate groups
ad_group = df[df['test group'] == 'ad']
psa_group = df[df['test group'] == 'psa']

# Basic metrics
n_ad = len(ad_group)
n_psa = len(psa_group)
ad_conversions = ad_group['converted'].sum()
psa_conversions = psa_group['converted'].sum()

cr_ad = ad_conversions / n_ad
cr_psa = psa_conversions / n_psa

# Incremental conversions
incremental_conversions = ad_conversions - (n_ad * cr_psa)
incremental_conversion_rate = cr_ad - cr_psa

print(f"\n📊 Conversion Metrics:")
print(f"   Ad Group:")
print(f"      Users: {n_ad:,}")
print(f"      Conversions: {ad_conversions:,}")
print(f"      Conversion Rate: {cr_ad:.4%}")
print(f"   PSA Group (Control):")
print(f"      Users: {n_psa:,}")
print(f"      Conversions: {psa_conversions:,}")
print(f"      Conversion Rate: {cr_psa:.4%}")
print(f"\n📈 Incremental Impact:")
print(f"   Incremental Conversion Rate: {incremental_conversion_rate:.6f} ({incremental_conversion_rate*100:.4f}%)")
print(f"   Incremental Conversions: {incremental_conversions:,.2f}")

# ============================================================================
# 3. REVENUE ATTRIBUTION
# ============================================================================

print("\n" + "="*80)
print("REVENUE ATTRIBUTION")
print("="*80)

value_per_conversion = ASSUMPTIONS['value_per_conversion']

# Total revenue
total_revenue_ad = ad_conversions * value_per_conversion
total_revenue_psa = psa_conversions * value_per_conversion

# Incremental revenue (attributed to ads)
incremental_revenue = incremental_conversions * value_per_conversion

# Expected revenue (using Bayesian posterior if available)
if bayesian_results:
    expected_incremental_revenue = bayesian_results.get('expected_incremental_revenue', incremental_revenue)
    revenue_ci_lower = bayesian_results.get('revenue_ci_lower', incremental_revenue * 0.8)
    revenue_ci_upper = bayesian_results.get('revenue_ci_upper', incremental_revenue * 1.2)
else:
    expected_incremental_revenue = incremental_revenue
    revenue_ci_lower = incremental_revenue * 0.8
    revenue_ci_upper = incremental_revenue * 1.2

print(f"\n📊 Revenue Metrics (${value_per_conversion} per conversion):")
print(f"   Ad Group Total Revenue: ${total_revenue_ad:,.2f}")
print(f"   PSA Group Total Revenue: ${total_revenue_psa:,.2f}")
print(f"   Incremental Revenue: ${incremental_revenue:,.2f}")
print(f"   Expected Incremental Revenue: ${expected_incremental_revenue:,.2f}")
print(f"   95% CI: [${revenue_ci_lower:,.2f}, ${revenue_ci_upper:,.2f}]")

# ============================================================================
# 4. COST ANALYSIS
# ============================================================================

print("\n" + "="*80)
print("COST ANALYSIS")
print("="*80)

# Calculate campaign costs
cost_per_impression = ASSUMPTIONS['cost_per_ad_impression']
total_ad_impressions = ASSUMPTIONS['ad_group_total_ads']
total_campaign_cost = total_ad_impressions * cost_per_impression

# Cost per conversion
cost_per_conversion_ad = total_campaign_cost / ad_conversions if ad_conversions > 0 else float('inf')

# Cost per incremental acquisition (CPA)
cost_per_incremental_acquisition = total_campaign_cost / incremental_conversions if incremental_conversions > 0 else float('inf')

print(f"\n📊 Cost Metrics:")
print(f"   Total Ad Impressions: {total_ad_impressions:,}")
print(f"   Cost per Impression: ${cost_per_impression:.4f}")
print(f"   Total Campaign Cost: ${total_campaign_cost:,.2f}")
print(f"   Cost per Conversion (Ad Group): ${cost_per_conversion_ad:.2f}")
print(f"   Cost per Incremental Acquisition (CPA): ${cost_per_incremental_acquisition:.2f}")

# ============================================================================
# 5. RETURN ON AD SPEND (ROAS)
# ============================================================================

print("\n" + "="*80)
print("RETURN ON AD SPEND (ROAS)")
print("="*80)

# ROAS = Revenue / Ad Spend
roas_total = total_revenue_ad / total_campaign_cost if total_campaign_cost > 0 else float('inf')
roas_incremental = incremental_revenue / total_campaign_cost if total_campaign_cost > 0 else float('inf')

# ROI = (Revenue - Cost) / Cost
roi_total = (total_revenue_ad - total_campaign_cost) / total_campaign_cost if total_campaign_cost > 0 else float('inf')
roi_incremental = (incremental_revenue - total_campaign_cost) / total_campaign_cost if total_campaign_cost > 0 else float('inf')

print(f"\n📊 ROAS Metrics:")
print(f"   ROAS (Total Revenue): {roas_total:.2f}x")
print(f"      For every $1 spent, generated ${roas_total:.2f} in revenue")
print(f"   ROAS (Incremental Revenue): {roas_incremental:.2f}x")
print(f"      For every $1 spent, generated ${roas_incremental:.2f} in incremental revenue")

print(f"\n📈 ROI Metrics:")
print(f"   ROI (Total): {roi_total:.2%}")
print(f"   ROI (Incremental): {roi_incremental:.2%}")

# Interpretation
if roas_incremental > 1:
    print(f"\n✅ Campaign is profitable (ROAS > 1.0)")
elif roas_incremental > 0.5:
    print(f"\n⚠️  Campaign is marginally profitable")
else:
    print(f"\n❌ Campaign is not profitable (ROAS < 0.5)")

# ============================================================================
# 6. BREAK-EVEN ANALYSIS
# ============================================================================

print("\n" + "="*80)
print("BREAK-EVEN ANALYSIS")
print("="*80)

# Break-even point: where incremental revenue = campaign cost
# incremental_conversions * value_per_conversion = total_campaign_cost
# incremental_conversions = total_campaign_cost / value_per_conversion

break_even_conversions = total_campaign_cost / value_per_conversion if value_per_conversion > 0 else float('inf')
break_even_conversion_rate = break_even_conversions / n_ad

current_incremental = incremental_conversions
conversion_rate_needed = break_even_conversion_rate

print(f"\n📊 Break-Even Metrics:")
print(f"   Break-Even Incremental Conversions: {break_even_conversions:,.2f}")
print(f"   Current Incremental Conversions: {current_incremental:,.2f}")
print(f"   Break-Even Conversion Rate Lift: {conversion_rate_needed:.6f} ({conversion_rate_needed*100:.4f}%)")
print(f"   Current Conversion Rate Lift: {incremental_conversion_rate:.6f} ({incremental_conversion_rate*100:.4f}%)")

if current_incremental > break_even_conversions:
    margin = current_incremental - break_even_conversions
    print(f"\n✅ Campaign exceeds break-even by {margin:,.2f} conversions")
else:
    shortfall = break_even_conversions - current_incremental
    print(f"\n⚠️  Campaign needs {shortfall:,.2f} more incremental conversions to break even")

# ============================================================================
# 7. SCALING PROJECTIONS
# ============================================================================

print("\n" + "="*80)
print("SCALING PROJECTIONS")
print("="*80)

# Projections for different user volumes
scaling_scenarios = [10000, 50000, 100000, 500000, 1000000]

print(f"\n📊 Projected Impact at Different Scales:")
print(f"{'Users':>12} {'Incremental Conv.':>20} {'Incremental Revenue':>25} {'Campaign Cost':>20} {'ROAS':>10}")
print("-" * 95)

for n_users in scaling_scenarios:
    projected_incremental = n_users * incremental_conversion_rate
    projected_revenue = projected_incremental * value_per_conversion
    # Assume same cost per impression, scale impressions proportionally
    impressions_per_user = total_ad_impressions / n_ad
    projected_impressions = n_users * impressions_per_user
    projected_cost = projected_impressions * cost_per_impression
    projected_roas = projected_revenue / projected_cost if projected_cost > 0 else float('inf')
    
    print(f"{n_users:>12,} {projected_incremental:>20,.0f} ${projected_revenue:>24,.2f} ${projected_cost:>19,.2f} {projected_roas:>10.2f}x")

# ============================================================================
# 8. SENSITIVITY ANALYSIS
# ============================================================================

print("\n" + "="*80)
print("SENSITIVITY ANALYSIS")
print("="*80)

# Vary key assumptions
value_scenarios = [50, 75, 100, 125, 150]
cost_scenarios = [0.005, 0.01, 0.015, 0.02]

print(f"\n📊 Sensitivity to Value per Conversion:")
print(f"{'Value/Conv':>12} {'Incremental Revenue':>25} {'ROAS':>10}")
print("-" * 50)
for value in value_scenarios:
    rev = incremental_conversions * value
    roas = rev / total_campaign_cost if total_campaign_cost > 0 else float('inf')
    print(f"${value:>11,.0f} ${rev:>24,.2f} {roas:>10.2f}x")

print(f"\n📊 Sensitivity to Cost per Impression:")
print(f"{'Cost/Imp':>12} {'Campaign Cost':>20} {'ROAS':>10}")
print("-" * 45)
for cost in cost_scenarios:
    campaign_cost = total_ad_impressions * cost
    roas = incremental_revenue / campaign_cost if campaign_cost > 0 else float('inf')
    print(f"${cost:>11,.4f} ${campaign_cost:>19,.2f} {roas:>10.2f}x")

# ============================================================================
# 9. SUMMARY STATISTICS
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
    'incremental_conversions': incremental_conversions,
    'incremental_conversion_rate': incremental_conversion_rate,
    'value_per_conversion': value_per_conversion,
    'total_campaign_cost': total_campaign_cost,
    'total_revenue_ad': total_revenue_ad,
    'incremental_revenue': incremental_revenue,
    'expected_incremental_revenue': expected_incremental_revenue,
    'cost_per_incremental_acquisition': cost_per_incremental_acquisition,
    'roas_total': roas_total,
    'roas_incremental': roas_incremental,
    'roi_total': roi_total,
    'roi_incremental': roi_incremental,
    'break_even_conversions': break_even_conversions,
    'is_profitable': roas_incremental > 1.0
}

print("\n📋 Key Business Metrics:")
for key, value in summary.items():
    if isinstance(value, float):
        if 'rate' in key or 'roi' in key:
            print(f"   {key}: {value:.6f} ({value*100:.4f}%)")
        elif 'cost' in key or 'revenue' in key or 'value' in key:
            print(f"   {key}: ${value:,.2f}")
        else:
            print(f"   {key}: {value:.6f}")
    elif isinstance(value, bool):
        print(f"   {key}: {'Yes' if value else 'No'}")
    else:
        print(f"   {key}: {value:,}")

# Save summary
with open('business_impact_results.json', 'w') as f:
    json.dump({k: float(v) if isinstance(v, (np.integer, np.floating)) else v 
              for k, v in summary.items()}, f, indent=2)

print("\n💾 Results saved to 'business_impact_results.json'")

print("\n" + "="*80)
print("BUSINESS IMPACT ANALYSIS COMPLETE ✓")
print("="*80)


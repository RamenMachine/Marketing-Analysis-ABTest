# Statistical Methods Guide

This document provides a comprehensive overview of the statistical methods used in this A/B testing platform.

## Table of Contents

1. [Frequentist Methods](#frequentist-methods)
2. [Bayesian Methods](#bayesian-methods)
3. [Effect Size](#effect-size)
4. [Power Analysis](#power-analysis)
5. [Business Metrics](#business-metrics)

## Frequentist Methods

### Two-Sample T-Test (Welch's)

Tests whether there is a statistically significant difference between two groups.

**Null Hypothesis (H₀)**: μ_ad = μ_psa  
**Alternative Hypothesis (H₁)**: μ_ad ≠ μ_psa

**Formula**:
$$t = \frac{\bar{x}_1 - \bar{x}_2}{\sqrt{\frac{s_1^2}{n_1} + \frac{s_2^2}{n_2}}}$$

**Interpretation**:
- p < 0.05: Statistically significant difference
- p ≥ 0.05: No significant difference detected

### Chi-Square Test for Independence

Tests whether group assignment and conversion are independent.

**Formula**:
$$\chi^2 = \sum \frac{(O_{ij} - E_{ij})^2}{E_{ij}}$$

**Degrees of Freedom**:
$$df = (r-1) \times (c-1)$$

### Bootstrap Confidence Intervals

Non-parametric method using resampling with replacement.

**Procedure**:
1. Resample n₁ observations from group 1 with replacement
2. Resample n₂ observations from group 2 with replacement
3. Calculate difference in means
4. Repeat B times (typically 10,000)
5. Use percentiles for confidence intervals

## Bayesian Methods

### Beta-Binomial Model

Models conversion rates using conjugate prior for binary outcomes.

**Prior**: Beta(α, β)  
**Posterior**: Beta(α + successes, β + failures)

**Posterior Mean**:
$$E[p | \text{data}] = \frac{\alpha + \text{successes}}{\alpha + \beta + \text{total trials}}$$

### Credible Intervals

Bayesian equivalent of confidence intervals with intuitive interpretation.

**Interpretation**: "There is a 95% probability that the true value lies in this interval"

### Probability of Superiority

Direct probability statement: P(p_ad > p_psa | data)

**Advantage**: More intuitive than p-values for business stakeholders

## Effect Size

### Cohen's h (for Proportions)

$$h = 2 \times (\arcsin(\sqrt{p_1}) - \arcsin(\sqrt{p_2}))$$

**Interpretation**:
- |h| < 0.2: Negligible
- 0.2 ≤ |h| < 0.5: Small
- 0.5 ≤ |h| < 0.8: Medium
- |h| ≥ 0.8: Large

### Cohen's d (for Continuous)

$$d = \frac{\mu_1 - \mu_2}{\sigma_{\text{pooled}}}$$

## Power Analysis

Statistical power is the probability of correctly rejecting a false null hypothesis.

**Factors Affecting Power**:
- Effect size
- Sample size
- Significance level (α)
- Type of test (one-tailed vs two-tailed)

**Required Sample Size**:
$$n = \frac{2(z_{\alpha/2} + z_{\beta})^2 \sigma^2}{(\mu_1 - \mu_2)^2}$$

## Business Metrics

### Return on Ad Spend (ROAS)

$$\text{ROAS} = \frac{\text{Revenue}}{\text{Ad Spend}}$$

**Interpretation**:
- ROAS > 1.0: Profitable
- ROAS = 1.0: Break-even
- ROAS < 1.0: Losing money

### Cost per Acquisition (CPA)

$$\text{CPA} = \frac{\text{Total Campaign Cost}}{\text{Incremental Conversions}}$$

### Return on Investment (ROI)

$$\text{ROI} = \frac{\text{Revenue} - \text{Cost}}{\text{Cost}} = \text{ROAS} - 1$$

## References

- Gelman, A., et al. (2013). Bayesian Data Analysis
- Cohen, J. (1988). Statistical Power Analysis for the Behavioral Sciences
- Efron, B., & Tibshirani, R. (1994). An Introduction to the Bootstrap


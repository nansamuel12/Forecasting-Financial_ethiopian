# Task 2: Exploratory Data Analysis - Key Insights Summary

**Date:** 2025-01-20  
**Task:** Task 2 - Exploratory Data Analysis  
**Branch:** task-2

## Executive Summary

This document summarizes key insights from the exploratory data analysis of Ethiopia's financial inclusion data. The analysis reveals important patterns, identifies data gaps, and provides hypotheses for impact modeling.

---

## 1. Key Insights (Minimum 5 Required)

### Insight 1: Account Ownership Growth Has Slowed Despite Massive Mobile Money Expansion

**Evidence:**
- Account ownership grew only **+3pp (46% → 49%)** from 2021-2024
- Previous period (2017-2021) saw **+11.0pp growth** over 4 years = **+2.75pp/year**
- Slowdown period (2021-2024) saw **+3pp over 3 years = +1.0pp/year** (63% slower)
- Meanwhile, **65M+ mobile money accounts** were opened (Telebirr: 54.84M, M-Pesa: 10.8M)
- Mobile money account rate doubled from **4.7% (2021) to 9.45% (2024)**

**Implication:**
This paradox suggests several possibilities:
1. Mobile money accounts may not be fully captured in Findex "account ownership" definition
2. Many mobile money accounts may be inactive or dormant (registered but not actively used)
3. Survey timing may not capture recent mobile money growth
4. Economic factors (inflation, FX reform) may have constrained traditional account growth
5. Quality/trust issues may limit active usage and survey reporting

**Hypothesis for Modeling:**
- Need to model "registered vs active" gap separately
- Account ownership and mobile money accounts may be measuring different things
- Survey methodology differences may explain the disconnect

---

### Insight 2: Mobile Money Penetration Doubled After M-Pesa Entry, Driving Competition

**Evidence:**
- Mobile money accounts: **4.7% (2021) → 9.45% (2024)** = **+101% growth**
- **M-Pesa added 10.8M registered users** by end of 2024 (+245% growth)
- **P2P transactions grew 158% YoY** after M-Pesa launch (49.7M → 128.3M transactions)
- **P2P transaction value: ETB 577.7 billion** in FY2024/25 (+113% YoY)

**Implication:**
- Competition drives adoption: Second entrant (M-Pesa) significantly expanded market
- Choice matters: Users benefit from multiple providers
- Network effects: Interoperability (M-Pesa + EthSwitch) enables cross-network transactions

**Hypothesis for Modeling:**
- Market competition is a key driver of adoption
- Product launches have immediate and sustained impact on usage metrics
- Interoperability amplifies network effects

---

### Insight 3: Gender Gap Persists Despite Overall Growth

**Evidence:**
- Gender gap in account ownership: **20pp in 2021** (56% male vs 36% female)
- Estimated gap: **18pp in 2024** (slight improvement but still large)
- **Women hold only 14% of mobile money accounts** (far from 50% parity)
- Mobile phone gender gap: **24pp** (86% male vs 65% female)

**Implication:**
- Growth is not gender-neutral: Men benefit more from financial inclusion expansion
- Structural barriers persist: Gender-specific interventions needed
- Mobile phone access gap may be limiting factor for mobile money adoption among women

**Hypothesis for Modeling:**
- Gender gap may require separate modeling approach
- Infrastructure access (mobile phones) may be a key constraint for women
- Targeted interventions (e.g., Fayda digital ID) may help but need time to show impact

---

### Insight 4: Infrastructure Investment is a Leading Indicator of Access

**Evidence:**
- **4G coverage expanded from 37.5% (2023) to 70.8% (2025)** = **+89% growth**
- **Fayda digital ID reached 15M enrollments** by May 2025 (target: 90M by 2028)
- **Mobile subscription penetration: 61.4%** (93.7M connections / 152.7M population)
- Infrastructure investments precede access improvements

**Implication:**
- Infrastructure enables access: Better network coverage supports mobile money usage
- Digital ID simplifies KYC: Fayda may reduce barriers to account opening
- Infrastructure is a leading indicator: Continued investment should support inclusion growth

**Hypothesis for Modeling:**
- Infrastructure metrics (4G coverage, mobile penetration) should be strong predictors
- Lag structure: Infrastructure investments take 12-24 months to show impact
- Infrastructure may be necessary but not sufficient condition

---

### Insight 5: Historic Milestone: Digital Payments Surpassed Cash

**Evidence:**
- **P2P transaction count (128.3M) exceeded ATM transactions (119.3M)** in FY2024/25
- **P2P/ATM ratio: 1.08** (first time digital > cash)
- P2P transactions grew **+158% YoY** while ATM grew **+26% YoY**
- This represents a **fundamental shift** in payment behavior

**Implication:**
- Digital payments are becoming the primary transaction method
- Cash is declining in relative importance
- This signals shift to digital economy

**Hypothesis for Modeling:**
- P2P transaction growth may be a leading indicator of overall financial inclusion
- Digital payment adoption may accelerate further with infrastructure improvements
- This milestone may have positive feedback effects (more users → more utility → more users)

---

### Insight 6: Event Timing Shows Clear Impact Patterns

**Evidence:**
- **Telebirr launch (May 2021)** preceded mobile money account growth (4.7% → 9.45%)
- **M-Pesa launch (Aug 2023)** drove P2P transaction surge (158% YoY growth)
- **Safaricom market entry (Aug 2022)** broke monopoly, enabled competition
- **Fayda rollout (Jan 2024)** reached 15M enrollments by May 2025

**Implication:**
- Product launches have measurable, time-lagged impacts
- Market competition amplifies adoption
- Policy and infrastructure events create enabling conditions

**Hypothesis for Modeling:**
- Event-driven models should capture lag structures (6-24 months typical)
- Multiple events may have cumulative or interactive effects
- Event timing relative to survey dates matters for measurement

---

### Insight 7: Data Gaps Limit Robust Analysis

**Evidence:**
- Many indicators have **sparse coverage (≤2 observations)**
- Limited **regional/rural-urban disaggregation**
- **Quality and trust pillars** have minimal data (only 2 observations each)
- **No time series** for many important indicators

**Implication:**
- Forecasting models will have limited granularity
- Regional and demographic variations cannot be fully analyzed
- Quality and trust factors are under-measured despite being important

**Hypothesis for Modeling:**
- Models should focus on indicators with sufficient data
- Need to prioritize data collection for quality and trust metrics
- Regional analysis may require external data sources

---

## 2. Data Quality Assessment

### Confidence Level Distribution
- **High confidence: 40 records (55.6%)** - Primary sources, verified data
- **Medium confidence: 3 records (4.2%)** - Secondary sources, cross-referenced
- **Low confidence: 0 records** - Single source, unverified
- **Estimated: 0 records** - Calculated or interpolated

### Source Type Distribution
- **Operator data: 15 records (20.8%)** - Ethio Telecom, Safaricom, EthSwitch
- **Survey data: 10 records (13.9%)** - Global Findex
- **Regulator data: 7 records (9.7%)** - NBE, NIDP
- **Research: 4 records (5.6%)** - World Bank, GSMA, A4AI
- **Policy: 3 records (4.2%)** - NFIS-II, strategy documents
- **Calculated: 2 records (2.8%)** - Derived indicators
- **News: 2 records (2.8%)** - Press releases, announcements

### Temporal Coverage
- **Year range: 2014-2025** (11 years)
- **Earliest observation: 2014-12-31**
- **Latest observation: 2025-12-31**
- **Span: 4,018 days**

### Indicator Coverage
- **Total unique indicators: 19**
- **Indicators with sparse coverage (≤2 observations): 10 indicators**
  - ACC_MOBILE_PEN (1 observation)
  - AFF_DATA_INCOME (1 observation)
  - GEN_GAP_MOBILE (1 observation)
  - GEN_MM_SHARE (1 observation)
  - USG_ACTIVE_RATE (1 observation)
  - USG_ATM_COUNT (1 observation)
  - USG_ATM_VALUE (1 observation)
  - USG_CROSSOVER (1 observation)
  - USG_MPESA_ACTIVE (1 observation)
  - USG_MPESA_USERS (1 observation)

### Data Limitations

1. **Sparse Time Series:**
   - Most indicators have 1-3 observations
   - Difficult to establish trends or seasonality
   - Limited ability to detect structural breaks

2. **Limited Disaggregation:**
   - Minimal regional data (mostly national aggregates)
   - Limited rural-urban breakdown
   - Gender disaggregation available only for account ownership

3. **Missing Pillars:**
   - QUALITY: Only 1 observation (transaction success rate, estimated)
   - TRUST: Only 1 observation (fraud rate, estimated, low confidence)
   - DEPTH: No observations (savings, credit, insurance)

4. **Survey Timing:**
   - Findex surveys every 3 years (2014, 2017, 2021, 2024)
   - May miss rapid changes between survey waves
   - Mobile money growth may not be fully captured

5. **Definitional Differences:**
   - Findex "account ownership" may not align with operator "registered users"
   - Survey-reported usage vs. operator transaction data may differ
   - Need to reconcile these differences in modeling

---

## 3. Factors Driving Financial Inclusion

### Access Drivers (Based on Analysis)

1. **Infrastructure:**
   - 4G coverage expansion (37.5% → 70.8%)
   - Mobile penetration (61.4%)
   - Strong positive correlation with access metrics

2. **Product Launches:**
   - Telebirr launch (May 2021) → Mobile money accounts growth
   - M-Pesa launch (Aug 2023) → Doubled mobile money penetration
   - Competition drives adoption

3. **Policy Framework:**
   - NFIS-II strategy (2021-2025) sets 70% account ownership target
   - KYC regulation updates enable easier account opening
   - Policy coordination creates enabling environment

4. **Digital ID:**
   - Fayda enrollment (15M by May 2025)
   - Simplifies KYC requirements
   - May reduce barriers to account opening (lagged effect)

### Usage Drivers (Based on Analysis)

1. **Product Availability:**
   - Multiple mobile money providers (Telebirr, M-Pesa)
   - Interoperability (M-Pesa + EthSwitch integration)
   - Network effects amplify usage

2. **Transaction Growth:**
   - P2P transactions: 49.7M (2024) → 128.3M (2025) = +158% YoY
   - P2P value: ETB 577.7 billion (+113% YoY)
   - Digital payments surpassing cash

3. **Infrastructure Quality:**
   - 4G coverage enables reliable transactions
   - Real-time payment systems (EthioPay)
   - Better connectivity supports active usage

---

## 4. Why Account Ownership Stagnated Despite 65M+ Mobile Money Accounts

### Potential Explanations

1. **Definitional Mismatch:**
   - Findex "account ownership" may use different definition than operator "registered users"
   - Survey may ask about "active" accounts, not just registered
   - Mobile money accounts may not qualify as "accounts" in survey definition

2. **Inactive Accounts:**
   - Many registered users may not be active
   - M-Pesa: 10.8M registered but only 7.1M 90-day active (66% activity rate)
   - If similar rates apply to Telebirr, many accounts may be dormant

3. **Survey Timing:**
   - Findex 2024 survey conducted Oct-Nov 2024
   - M-Pesa launched Aug 2023 (only 14 months before survey)
   - May not fully capture recent growth

4. **Economic Factors:**
   - FX liberalization (July 2024) may have created uncertainty
   - Inflation may have constrained traditional account growth
   - Economic shocks may have offset mobile money gains

5. **Quality/Trust Issues:**
   - Transaction success rate: 95.5% (estimated)
   - Fraud rate: 0.15% (estimated, low confidence)
   - Quality concerns may limit active usage and survey reporting

6. **Measurement Challenges:**
   - Survey respondents may not recognize mobile money as "account"
   - Cultural or language barriers in survey administration
   - Sampling may not fully capture mobile money users

---

## 5. Hypotheses for Impact Modeling

### Access Model Hypotheses

1. **Infrastructure is a leading indicator:**
   - 4G coverage → Account ownership (12-24 month lag)
   - Mobile penetration → Account ownership (direct relationship)

2. **Product launches drive adoption:**
   - Telebirr launch → Mobile money accounts (6-12 month lag)
   - M-Pesa launch → Mobile money accounts (6-12 month lag)
   - Competition amplifies effects

3. **Policy creates enabling conditions:**
   - NFIS-II strategy → Account ownership (36 month lag)
   - KYC updates → Account ownership (12 month lag)

4. **Digital ID reduces barriers:**
   - Fayda enrollment → Account ownership (24 month lag)
   - May have gender-specific effects (36 month lag)

### Usage Model Hypotheses

1. **Product availability drives usage:**
   - Multiple providers → Higher transaction volumes
   - Interoperability → Network effects amplify usage

2. **Infrastructure enables usage:**
   - 4G coverage → P2P transaction growth (24 month lag)
   - Better connectivity → More reliable transactions

3. **Event-driven growth:**
   - M-Pesa launch → P2P transaction surge (18 month lag)
   - Interoperability launch → Cross-network transactions (3 month lag)

4. **Quality matters:**
   - Transaction success rate → Active usage
   - Trust indicators → Sustained usage

### Cross-Cutting Hypotheses

1. **Registered vs Active Gap:**
   - Need separate models for registered users vs. active users
   - Activity rate may be key intermediate outcome

2. **Gender-Specific Effects:**
   - Infrastructure may have different impacts by gender
   - Product features may affect gender gap differently

3. **Regional Variations:**
   - Urban vs. rural may have different drivers
   - Infrastructure may matter more in rural areas

4. **Time-Varying Effects:**
   - Early adoption vs. later adoption may have different drivers
   - Network effects may accelerate over time

---

## 6. Recommendations for Next Steps

1. **Data Collection Priorities:**
   - Collect more quality and trust metrics
   - Expand regional/rural-urban disaggregation
   - Track registered vs. active user gap systematically

2. **Modeling Approach:**
   - Focus on indicators with sufficient data (account ownership, mobile money accounts, P2P transactions)
   - Use event-driven models with appropriate lag structures
   - Model registered and active users separately

3. **Validation:**
   - Cross-validate with external data sources
   - Test hypotheses with out-of-sample data
   - Validate event impact estimates

4. **Sensitivity Analysis:**
   - Test robustness to data quality assumptions
   - Explore alternative lag structures
   - Assess impact of missing data

---

## 7. Files Generated

### Scripts
- `src/eda_analysis.py` - Comprehensive EDA script

### Visualizations (in `reports/figures/`)
- `01_record_type_distribution.png`
- `02_pillar_distribution.png`
- `03_source_type_distribution.png`
- `04_confidence_distribution.png`
- `05_temporal_coverage.png`
- `06_account_ownership_trajectory.png`
- `07_growth_rates.png`
- `08_gender_gap_analysis.png`
- `09_slowdown_analysis.png`
- `10_mobile_money_penetration.png`
- `11_registered_vs_active.png`
- `12_p2p_transactions.png`
- `13_infrastructure_analysis.png`
- `14_event_timeline.png`
- `15_events_overlaid_trends.png`
- `16_correlation_matrix.png`
- `17_impact_links_analysis.png`

### Documentation
- `eda_insights_summary.md` - This document

---

**Analysis completed:** 2025-01-20  
**Next step:** Task 3 - Impact Modeling

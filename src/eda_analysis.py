"""
Comprehensive Exploratory Data Analysis for Ethiopia FI Forecast
Task 2: EDA Script
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Set style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

# Create output directory
Path("reports/figures").mkdir(parents=True, exist_ok=True)

# Load data with error handling
try:
    data_path = Path("data/raw/ethiopia_fi_unified_data - ethiopia_fi_unified_data.csv")
    if not data_path.exists():
        raise FileNotFoundError(f"Data file not found: {data_path}")
    df = pd.read_csv(data_path)
except FileNotFoundError as e:
    print(f"✗ Error: {e}")
    raise
except pd.errors.EmptyDataError:
    print("✗ Error: Data file is empty")
    raise
except Exception as e:
    print(f"✗ Error loading data: {e}")
    raise

print("=" * 80)
print("ETHIOPIA FI FORECAST - EXPLORATORY DATA ANALYSIS")
print("=" * 80)
print(f"\nDataset loaded: {len(df)} records")
print(f"Columns: {len(df.columns)}\n")

# Prepare observations dataframe with error handling
try:
    obs_df = df[df['record_type'] == 'observation'].copy()
    if len(obs_df) == 0:
        raise ValueError("No observations found in dataset")
    
    obs_df['observation_date'] = pd.to_datetime(obs_df['observation_date'], errors='coerce')
    obs_df = obs_df.dropna(subset=['observation_date']).sort_values('observation_date')
    
    if len(obs_df) == 0:
        raise ValueError("No observations with valid dates found")
except Exception as e:
    print(f"✗ Error preparing observations: {e}")
    raise

# ============================================================================
# 1. DATASET OVERVIEW
# ============================================================================
print("\n" + "=" * 80)
print("1. DATASET OVERVIEW")
print("=" * 80)

# Record type distribution
print("\n1.1 Record Type Distribution:")
record_type_counts = df['record_type'].value_counts()
print(record_type_counts)

fig, axes = plt.subplots(1, 2, figsize=(14, 5))
axes[0].pie(record_type_counts.values, labels=record_type_counts.index, autopct='%1.1f%%', startangle=90)
axes[0].set_title('Distribution by Record Type')
record_type_counts.plot(kind='bar', ax=axes[1], color='steelblue')
axes[1].set_title('Record Type Counts')
axes[1].set_ylabel('Count')
axes[1].tick_params(axis='x', rotation=45)
plt.tight_layout()
plt.savefig('reports/figures/01_record_type_distribution.png', dpi=300, bbox_inches='tight')
plt.close()

# Pillar distribution
print("\n1.2 Pillar Distribution (Observations):")
obs_pillars = obs_df['pillar'].value_counts()
print(obs_pillars)

fig, ax = plt.subplots(figsize=(10, 6))
obs_pillars.plot(kind='barh', ax=ax, color='coral')
ax.set_title('Observation Counts by Pillar')
ax.set_xlabel('Count')
plt.tight_layout()
plt.savefig('reports/figures/02_pillar_distribution.png', dpi=300, bbox_inches='tight')
plt.close()

# Source type distribution
print("\n1.3 Source Type Distribution:")
source_counts = df['source_type'].value_counts()
print(source_counts)

fig, ax = plt.subplots(figsize=(10, 6))
source_counts.plot(kind='barh', ax=ax, color='teal')
ax.set_title('Records by Source Type')
ax.set_xlabel('Count')
plt.tight_layout()
plt.savefig('reports/figures/03_source_type_distribution.png', dpi=300, bbox_inches='tight')
plt.close()

# Confidence levels
print("\n1.4 Data Quality - Confidence Levels:")
confidence_counts = df['confidence'].value_counts()
print(confidence_counts)

fig, ax = plt.subplots(figsize=(8, 6))
confidence_counts.plot(kind='bar', ax=ax, color=['green', 'orange', 'red', 'gray'])
ax.set_title('Data Quality: Confidence Level Distribution')
ax.set_ylabel('Count')
ax.tick_params(axis='x', rotation=45)
plt.tight_layout()
plt.savefig('reports/figures/04_confidence_distribution.png', dpi=300, bbox_inches='tight')
plt.close()

# Temporal coverage
print("\n1.5 Temporal Coverage:")
indicators = obs_df['indicator_code'].unique()
years = sorted(obs_df['observation_date'].dt.year.unique())
print(f"Total unique indicators: {len(indicators)}")
print(f"Year range: {min(years)} - {max(years)}")

coverage_matrix = pd.DataFrame(index=indicators, columns=years, dtype=bool)
for indicator in indicators:
    indicator_data = obs_df[obs_df['indicator_code'] == indicator]
    for year in years:
        coverage_matrix.loc[indicator, year] = len(indicator_data[
            indicator_data['observation_date'].dt.year == year
        ]) > 0

fig, ax = plt.subplots(figsize=(14, 10))
sns.heatmap(coverage_matrix.astype(int), annot=False, cmap='YlOrRd', 
           cbar_kws={'label': 'Data Available'}, ax=ax)
ax.set_title('Temporal Coverage: Which Years Have Data for Which Indicators', fontsize=14, pad=20)
ax.set_xlabel('Year')
ax.set_ylabel('Indicator Code')
plt.xticks(rotation=45)
plt.yticks(rotation=0, fontsize=8)
plt.tight_layout()
plt.savefig('reports/figures/05_temporal_coverage.png', dpi=300, bbox_inches='tight')
plt.close()

# Sparse indicators
indicator_counts = obs_df['indicator_code'].value_counts()
sparse = indicator_counts[indicator_counts <= 2]
print(f"\nIndicators with sparse coverage (≤2 observations): {len(sparse)}")
print(sparse.head(10))

# ============================================================================
# 2. ACCESS ANALYSIS
# ============================================================================
print("\n" + "=" * 80)
print("2. ACCESS ANALYSIS")
print("=" * 80)

# Account ownership trajectory
acc_ownership = obs_df[
    (obs_df['indicator_code'] == 'ACC_OWNERSHIP') &
    (obs_df['gender'] == 'all') &
    (obs_df['location'] == 'national')
].copy().sort_values('observation_date')

print("\n2.1 Account Ownership Timeline:")
for _, row in acc_ownership.iterrows():
    print(f"  {row['observation_date'].strftime('%Y-%m-%d')}: {row['value_numeric']:.1f}%")

# Plot trajectory
fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(acc_ownership['observation_date'], acc_ownership['value_numeric'], 
        marker='o', linewidth=2, markersize=10, color='steelblue', label='Account Ownership')
ax.set_title('Ethiopia Account Ownership Trajectory (2014-2024)', fontsize=14, fontweight='bold')
ax.set_xlabel('Year')
ax.set_ylabel('Account Ownership Rate (%)')
ax.grid(True, alpha=0.3)
ax.legend()

# Add growth rate annotations
for i in range(1, len(acc_ownership)):
    prev_val = acc_ownership.iloc[i-1]['value_numeric']
    curr_val = acc_ownership.iloc[i]['value_numeric']
    growth = curr_val - prev_val
    years_diff = (acc_ownership.iloc[i]['observation_date'] - acc_ownership.iloc[i-1]['observation_date']).days / 365.25
    annual_growth = growth / years_diff
    
    mid_date = acc_ownership.iloc[i-1]['observation_date'] + (acc_ownership.iloc[i]['observation_date'] - acc_ownership.iloc[i-1]['observation_date']) / 2
    ax.annotate(f'+{growth:.1f}pp\n({annual_growth:.1f}pp/yr)', 
                xy=(mid_date, (prev_val + curr_val) / 2),
                xytext=(10, 10), textcoords='offset points',
                fontsize=9, bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.7))

plt.tight_layout()
plt.savefig('reports/figures/06_account_ownership_trajectory.png', dpi=300, bbox_inches='tight')
plt.close()

# Growth rates
print("\n2.2 Growth Rates Between Survey Years:")
growth_rates = []
for i in range(1, len(acc_ownership)):
    prev_date = acc_ownership.iloc[i-1]['observation_date']
    curr_date = acc_ownership.iloc[i]['observation_date']
    prev_val = acc_ownership.iloc[i-1]['value_numeric']
    curr_val = acc_ownership.iloc[i]['value_numeric']
    
    years = (curr_date - prev_date).days / 365.25
    absolute_growth = curr_val - prev_val
    pct_growth = ((curr_val / prev_val) - 1) * 100
    annual_growth = absolute_growth / years
    
    growth_rates.append({
        'period': f"{prev_date.year}-{curr_date.year}",
        'years': years,
        'absolute_growth_pp': absolute_growth,
        'pct_growth': pct_growth,
        'annual_growth_pp': annual_growth
    })
    
    print(f"  {prev_date.year}-{curr_date.year}: {absolute_growth:+.1f}pp ({pct_growth:+.1f}%) over {years:.1f} years = {annual_growth:+.2f}pp/year")

growth_df = pd.DataFrame(growth_rates)

fig, axes = plt.subplots(1, 2, figsize=(14, 5))
axes[0].bar(growth_df['period'], growth_df['absolute_growth_pp'], color='steelblue')
axes[0].set_title('Absolute Growth (percentage points)')
axes[0].set_ylabel('Growth (pp)')
axes[0].tick_params(axis='x', rotation=45)
axes[0].grid(True, alpha=0.3, axis='y')

axes[1].bar(growth_df['period'], growth_df['annual_growth_pp'], color='coral')
axes[1].set_title('Annualized Growth Rate')
axes[1].set_ylabel('Growth (pp/year)')
axes[1].tick_params(axis='x', rotation=45)
axes[1].grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig('reports/figures/07_growth_rates.png', dpi=300, bbox_inches='tight')
plt.close()

# Gender gap analysis
print("\n2.3 Gender Gap Analysis:")
acc_male = obs_df[
    (obs_df['indicator_code'] == 'ACC_OWNERSHIP') &
    (obs_df['gender'] == 'male') &
    (obs_df['location'] == 'national')
].copy().sort_values('observation_date')

acc_female = obs_df[
    (obs_df['indicator_code'] == 'ACC_OWNERSHIP') &
    (obs_df['gender'] == 'female') &
    (obs_df['location'] == 'national')
].copy().sort_values('observation_date')

gap_data = obs_df[
    (obs_df['indicator_code'] == 'GEN_GAP_ACC') &
    (obs_df['location'] == 'national')
].copy().sort_values('observation_date')

if len(acc_male) > 0 and len(acc_female) > 0:
    gender_comparison = pd.merge(
        acc_male[['observation_date', 'value_numeric']],
        acc_female[['observation_date', 'value_numeric']],
        on='observation_date',
        suffixes=('_male', '_female')
    )
    
    print("\nGender-Disaggregated Account Ownership:")
    for _, row in gender_comparison.iterrows():
        gap = row['value_numeric_male'] - row['value_numeric_female']
        print(f"  {row['observation_date'].strftime('%Y')}: Male {row['value_numeric_male']:.1f}% vs Female {row['value_numeric_female']:.1f}% (Gap: {gap:.1f}pp)")
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    axes[0].plot(acc_male['observation_date'], acc_male['value_numeric'], 
               marker='o', linewidth=2, markersize=8, label='Male', color='steelblue')
    axes[0].plot(acc_female['observation_date'], acc_female['value_numeric'], 
               marker='s', linewidth=2, markersize=8, label='Female', color='coral')
    axes[0].set_title('Account Ownership by Gender')
    axes[0].set_xlabel('Year')
    axes[0].set_ylabel('Account Ownership Rate (%)')
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)
    
    if len(gap_data) > 0:
        axes[1].plot(gap_data['observation_date'], gap_data['value_numeric'], 
                    marker='o', linewidth=2, markersize=8, color='red')
        axes[1].set_title('Gender Gap (Male - Female, percentage points)')
        axes[1].set_xlabel('Year')
        axes[1].set_ylabel('Gap (pp)')
        axes[1].grid(True, alpha=0.3)
        axes[1].axhline(y=0, color='black', linestyle='--', alpha=0.5)
    
    plt.tight_layout()
    plt.savefig('reports/figures/08_gender_gap_analysis.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print("\nGender Gap Evolution:")
    for _, row in gap_data.iterrows():
        print(f"  {row['observation_date'].strftime('%Y')}: {row['value_numeric']:.1f}pp gap")

# Investigate 2021-2024 slowdown
print("\n2.4 Investigating 2021-2024 Slowdown:")
slowdown_period = acc_ownership[
    (acc_ownership['observation_date'] >= '2021-01-01') &
    (acc_ownership['observation_date'] <= '2024-12-31')
].copy()

if len(slowdown_period) >= 2:
    prev_val = slowdown_period.iloc[0]['value_numeric']
    curr_val = slowdown_period.iloc[-1]['value_numeric']
    growth = curr_val - prev_val
    
    print(f"\nAccount Ownership Growth 2021-2024: {growth:+.1f}pp")
    print(f"Previous period (2017-2021): +11.0pp over 4 years = +2.75pp/year")
    print(f"Slowdown period (2021-2024): {growth:+.1f}pp over 3 years = {growth/3:+.2f}pp/year")
    
    # Get mobile money data
    mm_accounts = obs_df[
        (obs_df['indicator_code'] == 'ACC_MM_ACCOUNT') &
        (obs_df['gender'] == 'all') &
        (obs_df['location'] == 'national')
    ].copy().sort_values('observation_date')
    
    print("\nMobile Money Account Growth:")
    for _, row in mm_accounts.iterrows():
        print(f"  {row['observation_date'].strftime('%Y')}: {row['value_numeric']:.2f}%")
    
    # Get events
    events_df = df[df['record_type'] == 'event'].copy()
    events_df['observation_date'] = pd.to_datetime(events_df['observation_date'], errors='coerce')
    events_2021_2024 = events_df[
        (events_df['observation_date'] >= '2021-01-01') &
        (events_df['observation_date'] <= '2024-12-31')
    ].sort_values('observation_date')
    
    print("\nKey Events 2021-2024:")
    for _, event in events_2021_2024.iterrows():
        print(f"  {event['observation_date'].strftime('%Y-%m-%d')}: {event['indicator']} ({event['category']})")
    
    # Visualize paradox
    fig, axes = plt.subplots(2, 1, figsize=(12, 10))
    
    axes[0].plot(acc_ownership['observation_date'], acc_ownership['value_numeric'], 
               marker='o', linewidth=2, markersize=10, color='steelblue', label='Account Ownership')
    axes[0].axvspan(pd.Timestamp('2021-01-01'), pd.Timestamp('2024-12-31'), 
                   alpha=0.2, color='red', label='Slowdown Period')
    axes[0].set_title('Account Ownership vs Mobile Money Expansion Paradox', fontsize=14, fontweight='bold')
    axes[0].set_ylabel('Account Ownership (%)')
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)
    
    if len(mm_accounts) > 0:
        axes[1].plot(mm_accounts['observation_date'], mm_accounts['value_numeric'], 
                    marker='s', linewidth=2, markersize=10, color='green', label='Mobile Money Accounts')
        axes[1].axvspan(pd.Timestamp('2021-01-01'), pd.Timestamp('2024-12-31'), 
                       alpha=0.2, color='red')
        axes[1].set_xlabel('Year')
        axes[1].set_ylabel('Mobile Money Account Rate (%)')
        axes[1].legend()
        axes[1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('reports/figures/09_slowdown_analysis.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print("\n\nPOTENTIAL EXPLANATIONS FOR SLOWDOWN:")
    print("1. Mobile money accounts may not be counted in Findex 'account ownership' definition")
    print("2. Many mobile money accounts may be inactive or dormant")
    print("3. Survey timing may not capture recent mobile money growth")
    print("4. Economic factors (inflation, FX reform) may have constrained traditional account growth")
    print("5. Quality/trust issues may limit active usage and survey reporting")

# ============================================================================
# 3. USAGE ANALYSIS
# ============================================================================
print("\n" + "=" * 80)
print("3. USAGE (DIGITAL PAYMENTS) ANALYSIS")
print("=" * 80)

# Mobile money account penetration
mm_accounts = obs_df[
    (obs_df['indicator_code'] == 'ACC_MM_ACCOUNT') &
    (obs_df['gender'] == 'all') &
    (obs_df['location'] == 'national')
].copy().sort_values('observation_date')

print("\n3.1 Mobile Money Account Penetration:")
for _, row in mm_accounts.iterrows():
    print(f"  {row['observation_date'].strftime('%Y')}: {row['value_numeric']:.2f}%")

fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(mm_accounts['observation_date'], mm_accounts['value_numeric'], 
       marker='o', linewidth=2, markersize=10, color='green', label='Mobile Money Account Rate')
ax.set_title('Mobile Money Account Penetration (2014-2024)', fontsize=14, fontweight='bold')
ax.set_xlabel('Year')
ax.set_ylabel('Mobile Money Account Rate (%)')
ax.grid(True, alpha=0.3)
ax.legend()

if len(mm_accounts) >= 2:
    for i in range(1, len(mm_accounts)):
        prev_val = mm_accounts.iloc[i-1]['value_numeric']
        curr_val = mm_accounts.iloc[i]['value_numeric']
        growth = curr_val - prev_val
        pct_growth = ((curr_val / prev_val) - 1) * 100
        
        mid_date = mm_accounts.iloc[i-1]['observation_date'] + (mm_accounts.iloc[i]['observation_date'] - mm_accounts.iloc[i-1]['observation_date']) / 2
        ax.annotate(f'+{growth:.2f}pp\n({pct_growth:.0f}% growth)', 
                   xy=(mid_date, (prev_val + curr_val) / 2),
                   xytext=(10, 10), textcoords='offset points',
                   fontsize=9, bbox=dict(boxstyle='round,pad=0.3', facecolor='lightgreen', alpha=0.7))

plt.tight_layout()
plt.savefig('reports/figures/10_mobile_money_penetration.png', dpi=300, bbox_inches='tight')
plt.close()

# P2P transactions
p2p_count = obs_df[
    (obs_df['indicator_code'] == 'USG_P2P_COUNT') &
    (obs_df['location'] == 'national')
].copy().sort_values('observation_date')

p2p_value = obs_df[
    (obs_df['indicator_code'] == 'USG_P2P_VALUE') &
    (obs_df['location'] == 'national')
].copy().sort_values('observation_date')

print("\n3.2 P2P Transaction Growth:")
for _, row in p2p_count.iterrows():
    print(f"  {row['observation_date'].strftime('%Y')}: {row['value_numeric']:,.0f} transactions")

if len(p2p_count) >= 2:
    prev = p2p_count.iloc[-2]['value_numeric']
    curr = p2p_count.iloc[-1]['value_numeric']
    growth_pct = ((curr / prev) - 1) * 100
    print(f"  YoY Growth: {growth_pct:.1f}%")

# Registered vs Active
mpesa_users = obs_df[
    (obs_df['indicator_code'] == 'USG_MPESA_USERS') &
    (obs_df['location'] == 'national')
].copy().sort_values('observation_date')

mpesa_active = obs_df[
    (obs_df['indicator_code'] == 'USG_MPESA_ACTIVE') &
    (obs_df['location'] == 'national')
].copy().sort_values('observation_date')

print("\n3.3 Registered vs Active Users:")
if len(mpesa_users) > 0 and len(mpesa_active) > 0:
    mpesa_merged = pd.merge(
        mpesa_users[['observation_date', 'value_numeric']],
        mpesa_active[['observation_date', 'value_numeric']],
        on='observation_date',
        suffixes=('_registered', '_active')
    )
    
    if len(mpesa_merged) > 0:
        mpesa_merged['activity_rate'] = (mpesa_merged['value_numeric_active'] / mpesa_merged['value_numeric_registered']) * 100
        
        for _, row in mpesa_merged.iterrows():
            print(f"  {row['observation_date'].strftime('%Y')}:")
            print(f"    Registered: {row['value_numeric_registered']:,.0f}M")
            print(f"    90-day Active: {row['value_numeric_active']:,.0f}M")
            print(f"    Activity Rate: {row['activity_rate']:.1f}%")
        
        fig, axes = plt.subplots(1, 2, figsize=(14, 6))
        
        x = np.arange(len(mpesa_merged))
        width = 0.35
        axes[0].bar(x - width/2, mpesa_merged['value_numeric_registered'], width, label='Registered', color='steelblue')
        axes[0].bar(x + width/2, mpesa_merged['value_numeric_active'], width, label='90-day Active', color='coral')
        axes[0].set_ylabel('Users (Millions)')
        axes[0].set_title('M-Pesa: Registered vs Active Users')
        axes[0].set_xticks(x)
        axes[0].set_xticklabels([d.strftime('%Y') for d in mpesa_merged['observation_date']])
        axes[0].legend()
        axes[0].grid(True, alpha=0.3, axis='y')
        
        axes[1].bar(x, mpesa_merged['activity_rate'], color='green', alpha=0.7)
        axes[1].set_ylabel('Activity Rate (%)')
        axes[1].set_title('M-Pesa Activity Rate')
        axes[1].set_xticks(x)
        axes[1].set_xticklabels([d.strftime('%Y') for d in mpesa_merged['observation_date']])
        axes[1].axhline(y=50, color='red', linestyle='--', alpha=0.5, label='50% benchmark')
        axes[1].legend()
        axes[1].grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        plt.savefig('reports/figures/11_registered_vs_active.png', dpi=300, bbox_inches='tight')
        plt.close()

# P2P visualization
if len(p2p_count) > 0:
    fig, axes = plt.subplots(2, 1, figsize=(12, 10))
    
    axes[0].plot(p2p_count['observation_date'], p2p_count['value_numeric'] / 1e6, 
                marker='o', linewidth=2, markersize=10, color='steelblue')
    axes[0].set_title('P2P Transaction Count (Millions)', fontsize=12, fontweight='bold')
    axes[0].set_ylabel('Transactions (Millions)')
    axes[0].grid(True, alpha=0.3)
    
    if len(p2p_value) > 0:
        axes[1].plot(p2p_value['observation_date'], p2p_value['value_numeric'] / 1e9, 
                    marker='s', linewidth=2, markersize=10, color='green')
        axes[1].set_title('P2P Transaction Value (Billions ETB)', fontsize=12, fontweight='bold')
        axes[1].set_xlabel('Year')
        axes[1].set_ylabel('Value (Billions ETB)')
        axes[1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('reports/figures/12_p2p_transactions.png', dpi=300, bbox_inches='tight')
    plt.close()

# ============================================================================
# 4. INFRASTRUCTURE AND ENABLERS
# ============================================================================
print("\n" + "=" * 80)
print("4. INFRASTRUCTURE AND ENABLERS")
print("=" * 80)

coverage_4g = obs_df[
    (obs_df['indicator_code'] == 'ACC_4G_COV') &
    (obs_df['location'] == 'national')
].copy().sort_values('observation_date')

mobile_pen = obs_df[
    (obs_df['indicator_code'] == 'ACC_MOBILE_PEN') &
    (obs_df['location'] == 'national')
].copy().sort_values('observation_date')

fayda = obs_df[
    (obs_df['indicator_code'] == 'ACC_FAYDA') &
    (obs_df['location'] == 'national')
].copy().sort_values('observation_date')

print("\n4.1 Infrastructure Trends:")
print("4G Coverage:")
for _, row in coverage_4g.iterrows():
    print(f"  {row['observation_date'].strftime('%Y-%m')}: {row['value_numeric']:.1f}%")

print("\nMobile Penetration:")
for _, row in mobile_pen.iterrows():
    print(f"  {row['observation_date'].strftime('%Y')}: {row['value_numeric']:.1f}%")

print("\nFayda Digital ID Enrollment:")
for _, row in fayda.iterrows():
    print(f"  {row['observation_date'].strftime('%Y-%m')}: {row['value_numeric']:,.0f} people")

fig, axes = plt.subplots(2, 2, figsize=(14, 10))

if len(coverage_4g) > 0:
    axes[0, 0].plot(coverage_4g['observation_date'], coverage_4g['value_numeric'], 
                   marker='o', linewidth=2, markersize=8, color='steelblue')
    axes[0, 0].set_title('4G Population Coverage')
    axes[0, 0].set_ylabel('Coverage (%)')
    axes[0, 0].grid(True, alpha=0.3)

if len(mobile_pen) > 0:
    axes[0, 1].plot(mobile_pen['observation_date'], mobile_pen['value_numeric'], 
                   marker='s', linewidth=2, markersize=8, color='green')
    axes[0, 1].set_title('Mobile Subscription Penetration')
    axes[0, 1].set_ylabel('Penetration (%)')
    axes[0, 1].grid(True, alpha=0.3)

if len(fayda) > 0:
    axes[1, 0].plot(fayda['observation_date'], fayda['value_numeric'] / 1e6, 
                   marker='^', linewidth=2, markersize=8, color='purple')
    axes[1, 0].set_title('Fayda Digital ID Enrollment')
    axes[1, 0].set_xlabel('Date')
    axes[1, 0].set_ylabel('Enrollment (Millions)')
    axes[1, 0].grid(True, alpha=0.3)

if len(coverage_4g) > 0 and len(acc_ownership) > 0:
    ax_twin = axes[1, 1].twinx()
    
    line1 = axes[1, 1].plot(acc_ownership['observation_date'], acc_ownership['value_numeric'], 
                          marker='o', linewidth=2, markersize=6, color='steelblue', label='Account Ownership')
    line2 = ax_twin.plot(coverage_4g['observation_date'], coverage_4g['value_numeric'], 
                        marker='s', linewidth=2, markersize=6, color='green', label='4G Coverage')
    
    axes[1, 1].set_xlabel('Year')
    axes[1, 1].set_ylabel('Account Ownership (%)', color='steelblue')
    ax_twin.set_ylabel('4G Coverage (%)', color='green')
    axes[1, 1].set_title('Infrastructure vs Access Relationship')
    
    lines = line1 + line2
    labels = [l.get_label() for l in lines]
    axes[1, 1].legend(lines, labels, loc='upper left')
    axes[1, 1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('reports/figures/13_infrastructure_analysis.png', dpi=300, bbox_inches='tight')
plt.close()

# ============================================================================
# 5. EVENT TIMELINE AND VISUAL ANALYSIS
# ============================================================================
print("\n" + "=" * 80)
print("5. EVENT TIMELINE AND VISUAL ANALYSIS")
print("=" * 80)

events_df = df[df['record_type'] == 'event'].copy()
events_df['observation_date'] = pd.to_datetime(events_df['observation_date'], errors='coerce')
events_df = events_df.dropna(subset=['observation_date']).sort_values('observation_date')

print("\n5.1 All Cataloged Events:")
for _, event in events_df.iterrows():
    print(f"  {event['observation_date'].strftime('%Y-%m-%d')}: {event['indicator']} ({event['category']})")

# Timeline visualization
category_colors = {
    'product_launch': 'green',
    'market_entry': 'blue',
    'policy': 'purple',
    'regulation': 'orange',
    'infrastructure': 'red',
    'partnership': 'cyan',
    'milestone': 'gold',
    'economic': 'brown',
    'pricing': 'pink'
}

fig, ax = plt.subplots(figsize=(14, 8))

y_positions = {}
y_counter = 0
for _, event in events_df.iterrows():
    category = event['category']
    date = event['observation_date']
    
    if category not in y_positions:
        y_positions[category] = y_counter
        y_counter += 1
    
    y_pos = y_positions[category]
    color = category_colors.get(category, 'gray')
    
    ax.scatter(date, y_pos, s=200, c=color, alpha=0.7, edgecolors='black', linewidth=1)
    ax.annotate(event['indicator'][:30], 
               xy=(date, y_pos),
               xytext=(10, 0), textcoords='offset points',
               fontsize=8, rotation=0, ha='left', va='center')

ax.set_yticks(list(y_positions.values()))
ax.set_yticklabels(list(y_positions.keys()))
ax.set_xlabel('Date')
ax.set_title('Event Timeline: Financial Inclusion Events in Ethiopia', fontsize=14, fontweight='bold')
ax.grid(True, alpha=0.3, axis='x')

plt.tight_layout()
plt.savefig('reports/figures/14_event_timeline.png', dpi=300, bbox_inches='tight')
plt.close()

# Overlay events on trends
fig, axes = plt.subplots(2, 1, figsize=(14, 10))

axes[0].plot(acc_ownership['observation_date'], acc_ownership['value_numeric'], 
            marker='o', linewidth=2, markersize=8, color='steelblue', label='Account Ownership', zorder=2)

key_events = ['Telebirr Launch', 'M-Pesa Ethiopia Launch', 'Safaricom Ethiopia Commercial Launch', 
              'Fayda Digital ID Program Rollout', 'NFIS-II Strategy Launch']
for _, event in events_df.iterrows():
    if any(key in event['indicator'] for key in key_events):
        axes[0].axvline(x=event['observation_date'], color='red', linestyle='--', alpha=0.5, linewidth=1)
        axes[0].annotate(event['indicator'][:25], 
                       xy=(event['observation_date'], axes[0].get_ylim()[1] * 0.95),
                       rotation=90, ha='right', va='top', fontsize=7)

axes[0].set_title('Account Ownership with Key Events', fontsize=12, fontweight='bold')
axes[0].set_ylabel('Account Ownership (%)')
axes[0].legend()
axes[0].grid(True, alpha=0.3)

if len(mm_accounts) > 0:
    axes[1].plot(mm_accounts['observation_date'], mm_accounts['value_numeric'], 
                marker='s', linewidth=2, markersize=8, color='green', label='Mobile Money Accounts', zorder=2)
    
    mm_events = ['Telebirr Launch', 'M-Pesa Ethiopia Launch']
    for _, event in events_df.iterrows():
        if any(key in event['indicator'] for key in mm_events):
            axes[1].axvline(x=event['observation_date'], color='red', linestyle='--', alpha=0.5, linewidth=1)
            axes[1].annotate(event['indicator'][:25], 
                           xy=(event['observation_date'], axes[1].get_ylim()[1] * 0.95),
                           rotation=90, ha='right', va='top', fontsize=7)
    
    axes[1].set_title('Mobile Money Account Penetration with Key Events', fontsize=12, fontweight='bold')
    axes[1].set_xlabel('Year')
    axes[1].set_ylabel('Mobile Money Account Rate (%)')
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('reports/figures/15_events_overlaid_trends.png', dpi=300, bbox_inches='tight')
plt.close()

print("\n5.2 Visual Relationship Analysis:")
print("  1. Telebirr Launch (May 2021): Mobile money accounts 4.7% → 9.45%")
print("  2. M-Pesa Launch (Aug 2023): Added 10.8M users, P2P grew 158% YoY")
print("  3. Safaricom Market Entry (Aug 2022): Broke monopoly, enabled competition")

# ============================================================================
# 6. CORRELATION ANALYSIS
# ============================================================================
print("\n" + "=" * 80)
print("6. CORRELATION ANALYSIS")
print("=" * 80)

obs_pivot = obs_df.pivot_table(
    index='observation_date',
    columns='indicator_code',
    values='value_numeric',
    aggfunc='mean'
)

numeric_indicators = obs_pivot.select_dtypes(include=[np.number]).columns
indicators_with_data = [ind for ind in numeric_indicators if obs_pivot[ind].notna().sum() >= 2]

if len(indicators_with_data) > 1:
    corr_matrix = obs_pivot[indicators_with_data].corr()
    
    fig, ax = plt.subplots(figsize=(12, 10))
    sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm', center=0, 
               square=True, linewidths=0.5, cbar_kws={'label': 'Correlation'}, ax=ax)
    ax.set_title('Correlation Matrix: Financial Inclusion Indicators', fontsize=14, fontweight='bold')
    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=0)
    plt.tight_layout()
    plt.savefig('reports/figures/16_correlation_matrix.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    access_indicators = [ind for ind in indicators_with_data if 'ACC' in ind]
    usage_indicators = [ind for ind in indicators_with_data if 'USG' in ind]
    
    print("\n6.1 Strong Correlations with ACCESS Indicators:")
    for acc_ind in access_indicators:
        if acc_ind in corr_matrix.columns:
            correlations = corr_matrix[acc_ind].sort_values(ascending=False)
            strong_corr = correlations[(correlations.abs() > 0.5) & (correlations.index != acc_ind)]
            if len(strong_corr) > 0:
                print(f"\n  {acc_ind}:")
                for other_ind, corr_val in strong_corr.items():
                    print(f"    {other_ind}: {corr_val:.2f}")
    
    print("\n6.2 Strong Correlations with USAGE Indicators:")
    for usg_ind in usage_indicators:
        if usg_ind in corr_matrix.columns:
            correlations = corr_matrix[usg_ind].sort_values(ascending=False)
            strong_corr = correlations[(correlations.abs() > 0.5) & (correlations.index != usg_ind)]
            if len(strong_corr) > 0:
                print(f"\n  {usg_ind}:")
                for other_ind, corr_val in strong_corr.items():
                    print(f"    {other_ind}: {corr_val:.2f}")

# Impact link insights
print("\n6.3 Insights from Impact Links:")
impact_links = df[df['record_type'] == 'impact_link'].copy()

if len(impact_links) > 0:
    print(f"  Total impact links: {len(impact_links)}")
    
    pillar_counts = impact_links['pillar'].value_counts()
    print(f"\n  Impact Links by Pillar:")
    print(pillar_counts)
    
    direction_counts = impact_links['impact_direction'].value_counts()
    print(f"\n  Impact Links by Direction:")
    print(direction_counts)
    
    magnitude_counts = impact_links['impact_magnitude'].value_counts()
    print(f"\n  Impact Links by Magnitude:")
    print(magnitude_counts)
    
    fig, axes = plt.subplots(1, 3, figsize=(16, 5))
    
    pillar_counts.plot(kind='bar', ax=axes[0], color='steelblue')
    axes[0].set_title('Impact Links by Pillar')
    axes[0].set_ylabel('Count')
    axes[0].tick_params(axis='x', rotation=45)
    
    direction_counts.plot(kind='bar', ax=axes[1], color='coral')
    axes[1].set_title('Impact Links by Direction')
    axes[1].set_ylabel('Count')
    axes[1].tick_params(axis='x', rotation=45)
    
    magnitude_counts.plot(kind='bar', ax=axes[2], color='green')
    axes[2].set_title('Impact Links by Magnitude')
    axes[2].set_ylabel('Count')
    axes[2].tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    plt.savefig('reports/figures/17_impact_links_analysis.png', dpi=300, bbox_inches='tight')
    plt.close()

print("\n" + "=" * 80)
print("EDA ANALYSIS COMPLETE")
print("=" * 80)
print("\nAll visualizations saved to reports/figures/")
print("See eda_insights_summary.md for key findings.")

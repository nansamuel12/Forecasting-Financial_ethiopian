"""
Data exploration script for Ethiopia FI Unified Data
"""
import pandas as pd
import numpy as np
from pathlib import Path

# Load data
data_dir = Path("data/raw")
df = pd.read_csv(data_dir / "ethiopia_fi_unified_data - ethiopia_fi_unified_data.csv")
ref_codes = pd.read_csv(data_dir / "reference_codes - reference_codes.csv")

print("=" * 80)
print("ETHIOPIA FI UNIFIED DATA - EXPLORATION REPORT")
print("=" * 80)

# Basic info
print(f"\n1. DATASET OVERVIEW")
print(f"   Total records: {len(df)}")
print(f"   Total columns: {len(df.columns)}")
print(f"   Date range: {df['observation_date'].min()} to {df['observation_date'].max()}")

# Record type counts
print(f"\n2. RECORD TYPE DISTRIBUTION")
print(df['record_type'].value_counts().to_string())

# Pillar distribution
print(f"\n3. PILLAR DISTRIBUTION (by record_type)")
for rt in df['record_type'].unique():
    subset = df[df['record_type'] == rt]
    if 'pillar' in subset.columns:
        print(f"\n   {rt}:")
        print(subset['pillar'].value_counts().to_string())

# Source type distribution
print(f"\n4. SOURCE TYPE DISTRIBUTION")
print(df['source_type'].value_counts().to_string())

# Confidence distribution
print(f"\n5. CONFIDENCE DISTRIBUTION")
print(df['confidence'].value_counts().to_string())

# Temporal range of observations
print(f"\n6. TEMPORAL RANGE OF OBSERVATIONS")
obs_df = df[df['record_type'] == 'observation'].copy()
obs_df['observation_date'] = pd.to_datetime(obs_df['observation_date'], errors='coerce')
obs_df = obs_df.dropna(subset=['observation_date'])
if len(obs_df) > 0:
    print(f"   Earliest observation: {obs_df['observation_date'].min()}")
    print(f"   Latest observation: {obs_df['observation_date'].max()}")
    print(f"   Span: {(obs_df['observation_date'].max() - obs_df['observation_date'].min()).days} days")

# Unique indicators
print(f"\n7. UNIQUE INDICATORS")
indicators = df[df['record_type'] == 'observation']['indicator_code'].unique()
print(f"   Total unique indicators: {len(indicators)}")
for ind in sorted(indicators):
    count = len(df[(df['record_type'] == 'observation') & (df['indicator_code'] == ind)])
    print(f"   - {ind}: {count} observations")

# Events catalog
print(f"\n8. EVENTS CATALOG")
events = df[df['record_type'] == 'event']
print(f"   Total events: {len(events)}")
print(f"\n   Events by category:")
print(events['category'].value_counts().to_string())
print(f"\n   Events by date:")
events['observation_date'] = pd.to_datetime(events['observation_date'], errors='coerce')
events = events.sort_values('observation_date')
for _, row in events.iterrows():
    print(f"   - {row['observation_date']}: {row['indicator']} ({row['category']})")

# Impact links
print(f"\n9. IMPACT LINKS")
impacts = df[df['record_type'] == 'impact_link']
print(f"   Total impact links: {len(impacts)}")
if len(impacts) > 0:
    print(f"\n   Impact links by pillar:")
    print(impacts['pillar'].value_counts().to_string())
    print(f"\n   Impact links by direction:")
    print(impacts['impact_direction'].value_counts().to_string())
    print(f"\n   Impact links by magnitude:")
    print(impacts['impact_magnitude'].value_counts().to_string())
else:
    print("   No impact links found in dataset - need to be added during enrichment")

# Check for missing impact_links
print(f"\n10. EVENTS WITHOUT IMPACT LINKS")
all_events = set(events['record_id'].unique())
if len(impacts) > 0 and 'parent_id' in impacts.columns:
    events_with_impacts = set(impacts['parent_id'].unique())
    events_without_impacts = all_events - events_with_impacts
    print(f"   Events with impact links: {len(events_with_impacts)}")
    print(f"   Events without impact links: {len(events_without_impacts)}")
else:
    events_without_impacts = all_events
    print(f"   All {len(all_events)} events need impact links")
if events_without_impacts:
    for evt_id in sorted(events_without_impacts):
        evt = events[events['record_id'] == evt_id].iloc[0]
        print(f"   - {evt_id}: {evt['indicator']} ({evt['category']})")

print("\n" + "=" * 80)
print("EXPLORATION COMPLETE")
print("=" * 80)

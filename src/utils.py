"""
Utility functions for Ethiopia FI Forecast project
"""
import pandas as pd
from typing import Optional

def get_next_id(prefix: str, df: pd.DataFrame) -> str:
    """
    Get the next record ID in sequence based on existing IDs in the dataframe.
    
    Args:
        prefix: The ID prefix (e.g., 'EVT', 'IMP', 'ACC')
        df: The dataframe containing a 'record_id' column
        
    Returns:
        The next ID string in the format PREFIX_NNNN
    """
    if 'record_id' not in df.columns:
        return f"{prefix}_0001"
        
    existing = df[df['record_id'].str.startswith(prefix, na=False)]['record_id']
    
    if len(existing) == 0:
        return f"{prefix}_0001"
        
    try:
        # Extract numerical part and find max
        nums = [int(x.split('_')[1]) for x in existing if '_' in x and x.split('_')[1].isdigit()]
        if not nums:
            return f"{prefix}_0001"
        max_num = max(nums)
        return f"{prefix}_{max_num + 1:04d}"
    except (IndexError, ValueError):
        return f"{prefix}_0001"

import pytest
import pandas as pd
from src.utils import get_next_id

def test_get_next_id_empty_df():
    df = pd.DataFrame(columns=['record_id'])
    assert get_next_id('EVT', df) == 'EVT_0001'

def test_get_next_id_existing_records():
    df = pd.DataFrame({'record_id': ['EVT_0001', 'EVT_0002']})
    assert get_next_id('EVT', df) == 'EVT_0003'

def test_get_next_id_gap_in_sequence():
    df = pd.DataFrame({'record_id': ['EVT_0001', 'EVT_0003']})
    assert get_next_id('EVT', df) == 'EVT_0004'

def test_get_next_id_different_prefix():
    df = pd.DataFrame({'record_id': ['EVT_0001', 'IMP_0001']})
    assert get_next_id('IMP', df) == 'IMP_0002'

def test_get_next_id_no_record_id_column():
    df = pd.DataFrame({'other': [1, 2]})
    assert get_next_id('EVT', df) == 'EVT_0001'

def test_get_next_id_malformed_ids():
    df = pd.DataFrame({'record_id': ['EVT_0001', 'EVT_abc', 'EVT_0005']})
    assert get_next_id('EVT', df) == 'EVT_0006'

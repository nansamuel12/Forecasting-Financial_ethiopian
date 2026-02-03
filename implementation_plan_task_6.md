# Implementation Plan - Task 6: Refactoring for Testability & Adding Unit Tests

This task focuses on improving the code quality and maintainability of the Ethiopia FI Forecast project by refactoring existing scripts into testable modules and adding comprehensive unit testing.

## Objectives
- [ ] Refactor `src/enrich_data.py` to separate logic from implementation.
- [ ] Create `src/utils.py` for shared utility functions.
- [ ] Add unit tests for core functionality in `tests/`.
- [ ] Maintain the "Pull Request" flow as requested by the user.

## Proposed Changes

### 1. New Utility Module (`src/utils.py`)
- Extract `get_next_id` from `src/enrich_data.py`.
- Add docstrings and type hints.
- Add error handling for unexpected data formats.

### 2. Refactor `src/enrich_data.py`
- Wrap data enrichment logic in functions.
- Use `if __name__ == "__main__":` to prevent execution on import.
- Improve error handling and logging.

### 3. Add Unit Tests (`tests/test_utils.py`)
- Test `get_next_id` with various edge cases (empty df, non-sequential IDs, different prefixes).
- Use `pytest` for testing.

## Verification Plan
### Automated Tests
- Run `pytest` to ensure all tests pass.
- Verify that `src/enrich_data.py` still works as expected when run directly.

### Manual Verification
- Check that `data/raw/ethiopia_fi_unified_data_enriched.csv` is correctly generated.

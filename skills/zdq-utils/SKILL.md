---
name: zdq-utils
description: >-
  Use this skill when writing or editing Python code that fetches data via Tushare
  or needs reusable personal utilities from the pre-installed `zdq_utils` package.
---

# zdq_utils Usage Guide

The personal Python package `zdq_utils` provides reusable utility functions. Prefer reusing functions from `zdq_utils` instead of re-implementing boilerplate (such as Tushare pagination, rate limiting, and retry loops).

## Available Functions

### `tushare_query`

Fetch data from Tushare Pro API with built-in pagination, per-minute rate limiting, and automatic retries (up to 5 attempts).

- **Import**:
  ```python
  from zdq_utils import tushare_query
  ```
- **Signature**:
  ```python
  tushare_query(execute_fuc: str, **kwargs) -> pd.DataFrame
  ```
- **Parameters**:
  - `execute_fuc` (`str`): Tushare Pro API interface name (e.g., `"stock_basic"`, `"daily"`, `"trade_cal"`).
  - `ts_limit_cnt` (`int`, optional, default `4000`): Page size (`limit`) per request.
  - `ts_max_calls` (`int`, optional, default `500`): Max API calls per minute; used to compute sleep interval between pages.
  - `ts_sleep` (`int | float`, optional, default `10`): Seconds to sleep before retrying after an exception.
  - `**kwargs`: Additional query parameters passed through to `pro.query(execute_fuc, ...)`.
- **Returns**: `pandas.DataFrame` containing all concatenated pages (or an empty `DataFrame` if no rows / all retries fail).
- **Prerequisites**: Tushare token must already be configured in the environment (via `ts.set_token(...)` / `~/.tushare` / `TUSHARE_TOKEN`).

#### Examples

```python
from zdq_utils import tushare_query

# Fetch listed stock basics
df_stocks = tushare_query("stock_basic", exchange="", list_status="L")

# Fetch daily bars with custom rate limit and page size
df_daily = tushare_query(
    "daily",
    ts_code="000001.SZ",
    start_date="20250101",
    end_date="20251231",
    ts_limit_cnt=5000,
    ts_max_calls=200,
    ts_sleep=5,
)
```

## Discovering Additional Utilities

If new utilities have been added to `zdq_utils`, inspect exported symbols and docstrings directly:

```bash
python -c "import zdq_utils; print(zdq_utils.__all__); help(zdq_utils.tushare_query)"
```

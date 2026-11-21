# zdq_utils

Personal Python utility functions.

## Installation

Clone and install (editable mode recommended so `git pull` updates take effect immediately):

```bash
git clone git@github.com:zdqzyx/zdq_utils.git
cd zdq_utils
pip install -e .
```

Or install directly via SSH:

```bash
pip install "git+ssh://git@github.com/zdqzyx/zdq_utils.git"
```

## Usage

```python
from zdq_utils import tushare_query

df = tushare_query("stock_basic", exchange="", list_status="L")
```

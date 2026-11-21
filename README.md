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

## Agent Skill Integration

To let coding agents automatically discover and use `zdq_utils`, symlink `skills/zdq-utils` into your agent's global skills directory:

```bash
# Antigravity (AGY)
mkdir -p ~/.gemini/config/skills
ln -sfn "$(pwd)/skills/zdq-utils" ~/.gemini/config/skills/zdq-utils

# Claude Code
mkdir -p ~/.claude/skills
ln -sfn "$(pwd)/skills/zdq-utils" ~/.claude/skills/zdq-utils

# Codex / Generic Agents
mkdir -p ~/.agents/skills
ln -sfn "$(pwd)/skills/zdq-utils" ~/.agents/skills/zdq-utils
```

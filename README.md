# hermes-hook-task-done

Hermes Agent hook that sends a minimal status notification when an agent task finishes.

Fires on `agent:end` and reports:
- ✅/⚠️ success or failure
- Model used (short name)
- Message count
- Duration
- Tool-call count

Currently supports **Feishu** (Lark) notifications out of the box. CLI/TUI sessions print to stdout.

## Install

```bash
# Default profile
curl -fsSL https://raw.githubusercontent.com/SunneeYang/hermes-hook-task-done/main/install.sh | bash

# Specific profile
curl -fsSL https://raw.githubusercontent.com/SunneeYang/hermes-hook-task-done/main/install.sh | bash -s -- <profile-name>
```

> ⚠️ **Restart the gateway after install:**
> ```bash
> hermes gateway restart
> ```

## Uninstall

```bash
# Default profile
curl -fsSL https://raw.githubusercontent.com/SunneeYang/hermes-hook-task-done/main/uninstall.sh | bash

# Specific profile
curl -fsSL https://raw.githubusercontent.com/SunneeYang/hermes-hook-task-done/main/uninstall.sh | bash -s -- <profile-name>
```

> ⚠️ **Restart the gateway after uninstall** so the old handler is flushed from memory.

## Requirements

- `FEISHU_APP_ID` and `FEISHU_APP_SECRET` env vars (for Feishu delivery)
- `httpx` Python package (usually already present in Hermes environment)

## Files

| File | Purpose |
|------|---------|
| `HOOK.yaml` | Hook manifest (name, events) |
| `handler.py` | Event handler implementation |
| `install.sh` | One-line installer |
| `uninstall.sh` | One-line uninstaller |

## License

MIT

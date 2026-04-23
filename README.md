# hermes-hook-task-done

Hermes Agent hook that sends a minimal status notification when an agent task finishes.

Fires on `agent:end` and reports:
- ✅/⚠️ success or failure
- Model used (short name)
- Message count
- Duration
- Tool-call count

Currently supports **Feishu** (Lark) only.

## Requirements

- Hermes gateway must be running (`hermes gateway run`)
- `FEISHU_APP_ID` and `FEISHU_APP_SECRET` environment variables
- `httpx` Python package (usually already present in the Hermes environment)

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

## Notes

- This hook only works in **gateway mode**. It does **not** trigger when running `hermes` in standalone CLI/TUI mode.
- The notification is sent via Feishu OpenAPI with a 3-second delay so it appears after the main response.

## Files

| File | Purpose |
|------|---------|
| `HOOK.yaml` | Hook manifest (name, events) |
| `handler.py` | Event handler implementation |
| `install.sh` | One-line installer |
| `uninstall.sh` | One-line uninstaller |

## License

MIT

#!/bin/bash
set -e

HOOK_NAME="task_done"
PROFILE="${1:-default}"
HERMES_HOME="${HERMES_HOME:-$HOME/.hermes}"

if [ "$PROFILE" != "default" ]; then
  TARGET="$HERMES_HOME/profiles/$PROFILE/hooks/$HOOK_NAME"
else
  TARGET="$HERMES_HOME/hooks/$HOOK_NAME"
fi

mkdir -p "$TARGET"

echo "Installing task-done-notification hook to $TARGET ..."

# Download from the same repo this script is hosted in.
# We resolve the raw URL from the install script's location.
REPO_BASE="https://raw.githubusercontent.com/SunneeYang/hermes-hook-task-done/main"

curl -fsSL "$REPO_BASE/HOOK.yaml" -o "$TARGET/HOOK.yaml"
curl -fsSL "$REPO_BASE/handler.py" -o "$TARGET/handler.py"

echo "✅ Hook installed to $TARGET"
echo ""
echo "   Profile: $PROFILE"
echo "   Events:  agent:end"
echo ""
echo "⚠️  You must restart the Hermes gateway for the hook to take effect."
echo ""
echo "   hermes gateway restart      # from shell"
echo "   /restart                    # from any chat session"

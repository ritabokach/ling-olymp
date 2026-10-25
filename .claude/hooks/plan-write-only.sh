#!/usr/bin/env bash
# PreToolUse(Write|Edit) hook for the planner: it may write only its own plan file
# swarm-report/<slug>-plan.md, nothing else. Exit 2 blocks. Fail-closed.
set -uo pipefail
command -v jq >/dev/null 2>&1 || { echo "plan-write-only: jq missing" >&2; exit 2; }
F="$(jq -r '.tool_input.file_path // empty' 2>/dev/null)" || { echo "plan-write-only: bad input" >&2; exit 2; }
case "$F" in
  */swarm-report/*-plan.md|swarm-report/*-plan.md)
    case "$F" in *..*) echo "planner: no '..' in plan path" >&2; exit 2 ;; esac
    exit 0 ;;
esac
echo "planner may write only swarm-report/<slug>-plan.md (got: $F)" >&2
exit 2

#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILLS_DIR="$SCRIPT_DIR/skills"
CODEX_SKILLS_DIR="${CODEX_SKILLS_DIR:-$HOME/.codex/skills}"
AGENT_SKILLS_DIR="${AGENT_SKILLS_DIR:-$HOME/.agents/skills}"

AGENT_SKILL_NAMES=(
  lark-approval
  lark-attendance
  lark-base
  lark-calendar
  lark-contact
  lark-doc
  lark-drive
  lark-event
  lark-im
  lark-mail
  lark-minutes
  lark-openapi-explorer
  lark-shared
  lark-sheets
  lark-skill-maker
  lark-slides
  lark-task
  lark-vc
  lark-whiteboard
  lark-whiteboard-cli
  lark-wiki
  lark-workflow-meeting-summary
  lark-workflow-standup-report
)

if [[ ! -d "$SKILLS_DIR" ]]; then
  echo "skills directory not found: $SKILLS_DIR" >&2
  exit 1
fi

mkdir -p "$CODEX_SKILLS_DIR" "$AGENT_SKILLS_DIR"

install_skill() {
  local src_dir="$1"
  local skill_name
  local target_root
  local target_dir

  skill_name="$(basename "$src_dir")"

  if is_agent_skill "$skill_name"; then
    target_root="$AGENT_SKILLS_DIR"
  else
    target_root="$CODEX_SKILLS_DIR"
  fi

  target_dir="$target_root/$skill_name"

  rm -rf "$target_dir"
  cp -R "$src_dir" "$target_dir"

  echo "Installed $skill_name -> $target_dir"
}

is_agent_skill() {
  local skill_name="$1"
  local item

  for item in "${AGENT_SKILL_NAMES[@]}"; do
    if [[ "$item" == "$skill_name" ]]; then
      return 0
    fi
  done

  return 1
}

while IFS= read -r -d '' skill_dir; do
  install_skill "$skill_dir"
done < <(find "$SKILLS_DIR" -mindepth 1 -maxdepth 1 -type d -print0 | sort -z)

echo
echo "Done."
echo "Codex skills directory: $CODEX_SKILLS_DIR"
echo "Agent skills directory: $AGENT_SKILLS_DIR"

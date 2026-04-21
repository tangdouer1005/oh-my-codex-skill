# oh-my-codex-skills

A public bundle of Codex skills exported from my local environment.

This repository is meant to serve two purposes:

- a portfolio of custom skills
- a portable backup that can help migrate my skill setup to another machine

## Included skills

### General and workflow skills

- `blog-reading`
- `defuddle`
- `excalidraw-diagram`
- `invoice-request-mail`
- `json-canvas`
- `lark-weekly-report-maintainer`
- `obsidian-bases`
- `obsidian-cli`
- `obsidian-markdown`
- `paper-reading`
- `pdf`
- `pdf-report-parser`
- `pushime-interview-ops`
- `report-benchmark-groundtruth-builder`
- `report-benchmark-query-recommender`

### Lark and Feishu skills

- `lark-approval`
- `lark-attendance`
- `lark-base`
- `lark-calendar`
- `lark-contact`
- `lark-doc`
- `lark-drive`
- `lark-event`
- `lark-im`
- `lark-mail`
- `lark-minutes`
- `lark-openapi-explorer`
- `lark-shared`
- `lark-sheets`
- `lark-skill-maker`
- `lark-slides`
- `lark-task`
- `lark-vc`
- `lark-whiteboard`
- `lark-whiteboard-cli`
- `lark-wiki`
- `lark-workflow-meeting-summary`
- `lark-workflow-standup-report`

## Repository layout

All skills live under `skills/`, with one directory per skill. Each skill usually contains:

- `SKILL.md` for the skill definition
- `references/` for supporting instructions or templates
- `agents/` for agent-specific configuration when needed
- `scripts/` or `assets/` for helpers and resources

## Migration to another machine

Clone the repository, then copy or sync the skill folders you want into your local Codex skill directories.

For a full install on a new machine:

```bash
git clone https://github.com/<your-username>/oh-my-codex-skills.git
cd oh-my-codex-skills
bash install.sh
```

The script installs skills into `~/.codex/skills` and `~/.agents/skills` using an explicit mapping that matches the original local environment.

Example:

```bash
git clone https://github.com/<your-username>/oh-my-codex-skills.git

mkdir -p ~/.codex/skills ~/.agents/skills

cp -R oh-my-codex-skills/skills/blog-reading ~/.codex/skills/
cp -R oh-my-codex-skills/skills/obsidian-cli ~/.codex/skills/
cp -R oh-my-codex-skills/skills/lark-calendar ~/.agents/skills/
cp -R oh-my-codex-skills/skills/lark-mail ~/.agents/skills/
```

If your environment expects a different layout, you can still use this repository as the source of truth and selectively sync the skill directories you need.

## Notes

- This repository intentionally excludes Codex system-built-in skills such as `.system/`.
- The contents were copied from a local working environment and reorganized into a single public repository for sharing and migration.

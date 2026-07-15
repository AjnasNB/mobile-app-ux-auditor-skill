# Mobile App UX Auditor Skill

A portable Agent Skill by Ajnas NB for auditing and improving mobile app UI/UX flows across Flutter, React Native, Swift/iOS, Kotlin, Java, Android Views, and Jetpack Compose.

Use it when you want an AI coding agent to inspect a mobile app, map real user flows, find UX friction, and propose or implement improvements with evidence instead of generic "make it cleaner" advice.

## What it helps with

- Navigation, back/close behavior, tabs, drawers, deep links, and re-entry flows.
- First launch, onboarding, sign-in, permissions, paywalls, subscriptions, and settings.
- Forms, validation, keyboard behavior, autofill, empty/loading/error/offline states.
- Accessibility: labels, roles, states, screen readers, focus order, touch targets, dynamic type, contrast, reduced motion.
- Platform fit for iOS and Android, including adaptive layout for tablets, foldables, landscape, and safe areas.
- Ethical retention through saved progress, useful reminders, trust, and repeated value.
- Static code triage with a bundled Python scanner.

## Install globally

```bash
npx mobile-app-ux-auditor-skill --global
```

An interactive terminal may omit the mode and choose from a prompt. Scripts, CI, and other
noninteractive shells must pass `--global` and/or `--project`; a no-argument noninteractive run
fails without writing files.

The interactive installer asks where to install:

1. Global current user: Claude Code, Codex, and shared Agent Skills.
2. Current project: local skills plus adapter files for popular coding agents.
3. Both global and current project.
4. Custom project path.

Global install copies the skill for the current user into:

- `~/.claude/skills/mobile-app-ux-auditor`
- `~/.agents/skills/mobile-app-ux-auditor`
- `~/.codex/skills/mobile-app-ux-auditor`

Restart your agent app after installing.

## Use it

Claude Code:

```text
/mobile-app-ux-auditor
```

Codex:

```text
$mobile-app-ux-auditor
```

Example prompts:

```text
/mobile-app-ux-auditor audit the onboarding and permission flow in this React Native app
```

```text
$mobile-app-ux-auditor review this Flutter checkout flow and fix the highest-impact UX issues
```

## Install into one project

```bash
npx mobile-app-ux-auditor-skill --project .
```

Project install copies the canonical skill into `.claude/skills/` and `.agents/skills/`, then writes adapter rule files for common coding agents:

- Cursor
- Windsurf
- GitHub Copilot
- Gemini
- Continue
- Cline
- Roo Code
- Kiro
- Trae
- OpenCode

Copy only the skill folders and skip adapter files:

```bash
npx mobile-app-ux-auditor-skill --project . --no-adapters
```

Skip prompts with an explicit global destination:

```bash
npx mobile-app-ux-auditor-skill --global --yes
```

Select global destinations explicitly:

```bash
npx mobile-app-ux-auditor-skill --global --targets claude,agents,codex-legacy
```

Project installs require an existing real directory. The installer rejects unknown options,
missing values, ambiguous managed markers, and destination paths that traverse symbolic links,
junctions, or reparse points. Adapter updates preserve user content and insert or replace only
the block delimited by `<!-- mobile-app-ux-auditor:start -->` and
`<!-- mobile-app-ux-auditor:end -->`. In particular, `.opencode/AGENTS.md` is never replaced as
a whole file.

## Static scanner

The skill includes a Python scanner for static mobile UX signals:

```bash
python scripts/mobile_ux_static_scan.py /path/to/mobile-app
```

The scanner detects review signals such as unlabeled custom controls, missing image labels, permission prompts, form-label risks, safe-area risks, and platform-specific accessibility gaps.

Linked files and directories are skipped; resolved scan inputs must remain inside the selected root.

It is a triage tool, not a replacement for expert review. Confirm every finding in code, simulator/device, screenshots, accessibility tooling, or tests before changing behavior.

## Package layout

```text
mobile-app-ux-auditor/
  SKILL.md
  agents/openai.yaml
  references/mobile-ux-audit-reference.md
  scripts/mobile_ux_static_scan.py
  skills/mobile-app-ux-auditor/
  .codex-plugin/plugin.json
  .claude-plugin/plugin.json
  bin/install.js
  package.json
```

The root `SKILL.md` supports direct skill installation. The `skills/mobile-app-ux-auditor/` copy supports plugin-style discovery.

## Publish to GitHub

```bash
gh auth login
gh repo create AjnasNB/mobile-app-ux-auditor-skill --public --source . --remote origin --push
```

If the repo already exists:

```bash
git remote add origin https://github.com/AjnasNB/mobile-app-ux-auditor-skill.git
git push -u origin main
```

## Download from npm

Install and run without keeping the package:

```bash
npx mobile-app-ux-auditor-skill --global
```

Install the CLI globally:

```bash
npm install -g mobile-app-ux-auditor-skill
mobile-app-ux-auditor --global
```

## Publish to npm

Log in once:

```bash
npm adduser
```

Check the package:

```bash
npm ci
npm run release:check
```

Publish:

```bash
npm publish --access public
```

After publishing, users download and install it with:

```bash
npx mobile-app-ux-auditor-skill --global
```

Or install the CLI globally:

```bash
npm install -g mobile-app-ux-auditor-skill
mobile-app-ux-auditor --global
```

See `SECURITY.md` for vulnerability reporting. The repository-only `RELEASING.md` contains the
maintainer checklist and is intentionally excluded from the npm tarball.

## License

MIT

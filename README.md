# Mobile App UX Auditor Skill

A portable Agent Skill for auditing and improving mobile app UI/UX flows across Flutter, React Native, Swift/iOS, Kotlin, Java, Android Views, and Jetpack Compose.

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

After the npm package is published:

```bash
npx mobile-app-ux-auditor-skill
```

This installs the skill for the current user into:

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

## Static scanner

The skill includes a Python scanner for static mobile UX signals:

```bash
python scripts/mobile_ux_static_scan.py /path/to/mobile-app
```

The scanner detects review signals such as unlabeled custom controls, missing image labels, permission prompts, form-label risks, safe-area risks, and platform-specific accessibility gaps.

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

## Publish to npm

Log in once:

```bash
npm adduser
```

Check the package:

```bash
npm publish --dry-run --access public
```

Publish:

```bash
npm publish --access public
```

After publishing, users install it with:

```bash
npx mobile-app-ux-auditor-skill
```

Or install the CLI globally:

```bash
npm install -g mobile-app-ux-auditor-skill
mobile-app-ux-auditor --global
```

## License

MIT

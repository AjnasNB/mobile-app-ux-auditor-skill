# Mobile App UX Auditor Skill

Agent Skill for auditing and improving mobile app UI/UX flows across Flutter, React Native, Swift/iOS, Kotlin, Java, Android Views, and Jetpack Compose.

## Install globally

```bash
npx mobile-app-ux-auditor-skill
```

This installs the skill for the current user into:

- `~/.claude/skills/mobile-app-ux-auditor`
- `~/.agents/skills/mobile-app-ux-auditor`
- `~/.codex/skills/mobile-app-ux-auditor`

Claude Code can then invoke it as:

```text
/mobile-app-ux-auditor
```

Codex can invoke it as:

```text
$mobile-app-ux-auditor
```

Codex can also choose it automatically when the request matches the skill description.

## Install into a project

```bash
npx mobile-app-ux-auditor-skill --project .
```

Project install copies the canonical skill into `.claude/skills/` and `.agents/skills/`, then writes adapter rule files for common tools such as Cursor, Windsurf, GitHub Copilot, Gemini, Continue, Cline, Roo Code, Kiro, Trae, and OpenCode.

Use `--no-adapters` to copy only the skill folders:

```bash
npx mobile-app-ux-auditor-skill --project . --no-adapters
```

## Static scanner

The skill includes a Python scanner for static UX signals:

```bash
python scripts/mobile_ux_static_scan.py /path/to/mobile-app
```

The scanner is a triage tool. Confirm every finding in code, simulator/device, screenshots, accessibility tooling, or tests before changing behavior.

## Publish to GitHub

```bash
git init
git add .
git commit -m "Initial mobile app UX auditor skill"
gh repo create ajnasnb/mobile-app-ux-auditor-skill --public --source . --remote origin --push
```

## Publish to npm

```bash
npm adduser
npm publish --access public
```

If you want a scoped package, change `package.json` from `mobile-app-ux-auditor-skill` to `@your-scope/mobile-app-ux-auditor-skill`, then publish with `npm publish --access public`.

## Compatibility

- Claude Code: personal skills folder supports slash invocation with `/mobile-app-ux-auditor`.
- Codex: user skills folder supports `$mobile-app-ux-auditor` and implicit invocation.
- Other tools: project adapters are installed through `--project` because global rule locations vary by tool and operating system.

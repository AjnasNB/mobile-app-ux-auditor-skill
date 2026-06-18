---
name: mobile-app-ux-auditor
description: Use when reviewing, redesigning, or implementing mobile app UI/UX flows in Flutter, React Native, Swift, SwiftUI, UIKit, Kotlin, Jetpack Compose, Java, or Android Views; especially for navigation, onboarding, retention, accessibility, forms, engagement, screen hierarchy, or platform-native fit.
---

# Mobile App UX Auditor

## Overview

Audit mobile apps by mapping real user flows, finding friction with evidence, and proposing or implementing improvements that match iOS and Android platform expectations. Optimize for users reaching value quickly and returning willingly, not for manipulative time-on-device.

## Workflow

1. State the design read: app category, audience, job-to-be-done, target platforms, product maturity, visual register, and risk level. For redesigns, preserve working navigation, copy, analytics names, and accessibility wins unless there is evidence they cause harm.
2. If code is available, run the static signal scan before judging:
   ```bash
   python scripts/mobile_ux_static_scan.py <project-root>
   ```
   In Claude Code, use `python ${CLAUDE_SKILL_DIR}/scripts/mobile_ux_static_scan.py <project-root>` when the skill is installed. Treat the script as evidence-gathering, not a replacement for expert review.
3. Inspect routing, screens, design system files, navigation components, analytics events, accessibility props, platform-specific UI primitives, tests, and screenshots before recommending changes.
4. Build a compact screen and flow map: first launch, onboarding, sign-in, home, primary task, search/discovery, settings, error states, empty states, permission requests, purchase/subscription, and re-entry flows.
5. Audit flows against platform conventions, accessibility, clarity, effort, trust, feedback, performance, adaptive layout, and ethical retention. Load `references/mobile-ux-audit-reference.md` for the detailed checklist and framework-specific code signals.
6. Rank issues by user impact:
   - P0: Blocks core task, causes data loss, or creates severe accessibility failure.
   - P1: Breaks navigation, trust, comprehension, or completion for many users.
   - P2: Adds avoidable friction, inconsistency, or weak platform fit.
   - P3: Polish, delight, or instrumentation improvement.
7. When editing code, preserve the app's existing architecture and design system. Prefer native platform components and established navigation/accessibility APIs over custom controls unless the product has a clear reason.
8. Verify with the best available evidence: emulator/simulator walkthrough, screenshots, accessibility scanner, VoiceOver/TalkBack, widget/UI tests, route tests, or static inspection. State any verification that could not be run.

## Quality Bar

Hold the output to a senior mobile product design engineer standard:

- The primary user can understand where they are, what changed, what to do next, and how to recover from mistakes.
- Core flows handle loading, empty, error, partial, disabled, offline, slow-network, auth-expired, permission-denied, interrupted, and resumed states.
- The UI has one coherent design system: typography scale, spacing rhythm, radius rules, color roles, interaction states, motion, density, and platform adaptation.
- Accessibility is built into labels, roles, states, focus order, target size, screen reader output, dynamic type/font scaling, contrast, and reduced-motion behavior.
- Mobile performance is UX: launch time, route transitions, jank, unnecessary re-renders, heavy images, blocked gestures, keyboard latency, and battery cost all matter.
- Retention comes from saved progress, useful reminders, reduced effort, trust, and repeated value. Do not optimize for addiction.

## Output Format

Start with findings, not praise. Include:

- A prioritized findings table: severity, screen/flow, evidence, user impact, recommended fix.
- A before/after flow summary when navigation or onboarding changes.
- Framework-specific implementation notes for Flutter, React Native, Swift/iOS, or Android as applicable.
- Static scan findings from `scripts/mobile_ux_static_scan.py` when code is available.
- Accessibility and adaptive-layout checks.
- Verification performed and remaining risks.

When asked to improve the app directly, implement the smallest high-impact changes first, then report changed files and validation.

## Non-Negotiables

- Do not recommend "make users stay longer" tactics that rely on confusion, forced continuity, hidden exits, guilt, dark patterns, or notification spam.
- Do not replace platform conventions with custom UI only for novelty.
- Do not audit from static screenshots alone when code or an app build is available.
- Do not give generic advice like "improve onboarding" without naming the exact screen, problem, and change.

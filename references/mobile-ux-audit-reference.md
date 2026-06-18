# Mobile UX Audit Reference

Use this reference when auditing or improving mobile apps across Flutter, React Native, Swift/iOS, Kotlin, Java, Android Views, or Jetpack Compose.

## Current Research Anchors

Prefer current official docs when the user's request depends on latest platform behavior.

- Apple Human Interface Guidelines: navigation, layout, tab bars, accessibility, toolbars, search, Dynamic Type, VoiceOver, platform adaptation.
- Android app quality: core quality, adaptive quality, Material 3 layout/navigation pairings, accessibility principles, TalkBack, Switch Access, Android vitals.
- Flutter docs: adaptive/responsive design, `SafeArea`, `MediaQuery`, `LayoutBuilder`, accessibility testing, `Semantics`.
- React Native docs: `accessible`, `accessibilityLabel`, `accessibilityHint`, `accessibilityRole`, `accessibilityState`, `AccessibilityInfo`, focus order.
- W3C WCAG 2.2: mobile-relevant criteria including target size, dragging alternatives, redundant entry, focus visibility, consistent help, accessible authentication.
- Product quality and retention: treat retention as a result of clear value, trust, speed, and useful re-entry. Avoid dark patterns.
- Public agent-skill patterns such as UI/UX Pro Max and Taste Skill show a useful structure: concise `SKILL.md`, deeper reference files, search/scanner scripts, anti-generic design constraints, and explicit quality gates. Use the structure, not copied prose or persona imitation.

## Cross-Agent Compatibility

This skill is portable when it stays inside the open skill shape:

- `SKILL.md` with YAML frontmatter and Markdown instructions.
- Optional `references/`, `scripts/`, and `assets/`.
- Optional `agents/openai.yaml` for Codex UI metadata; Claude Code ignores it.
- Install locations:
  - Codex: `~/.codex/skills/mobile-app-ux-auditor/`
  - Claude Code personal: `~/.claude/skills/mobile-app-ux-auditor/`
  - Project-local Claude Code: `<repo>/.claude/skills/mobile-app-ux-auditor/`

Avoid relying on platform-specific frontmatter unless the skill is intentionally platform-specific. Put platform-specific execution notes in the body.

## UX Engineer Operating Model

Use this order before proposing changes:

1. **Design read**: category, audience, job, usage environment, platform mix, trust level, density, maturity, visual register, constraints.
2. **User journey**: first value, primary task, recovery, re-entry, expansion, cancellation/delete.
3. **Evidence capture**: code scan, screen map, screenshots, simulator/device walkthrough, screen-reader walkthrough, performance/jank signals.
4. **Friction diagnosis**: confusion, too many choices, too many fields, hidden state, slow feedback, inaccessible control, broken recovery, trust gap.
5. **Design response**: remove, reorder, relabel, disclose progressively, add feedback, make state visible, improve defaults, strengthen affordance.
6. **Implementation response**: smallest code changes that improve completion and preserve platform conventions.
7. **Verification**: prove the new flow works with at least one realistic path and one failure/interruption path.

Do not invent a celebrity-designer persona. Adopt the discipline: evidence, taste, consistency, accessibility, and verification.

## Scorecard

Score each area from 0 to 5. A production app should have no area below 3 and critical flows should average 4+.

| Area | 0-1 | 3 | 5 |
| --- | --- | --- | --- |
| Task success | User cannot finish or loses data | Main path works with friction | Main, edge, interruption, and recovery paths are clear |
| Orientation | User cannot tell where they are | Titles/nav mostly work | Location, state, and next action are always obvious |
| Navigation | Back/close/deep links are broken | Common paths work | Platform-native, predictable, resumable, and deep-linkable |
| Forms/input | Placeholder labels, late errors, keyboard issues | Basic labels/errors | Autofill, correct keyboard, persistence, inline recovery |
| Accessibility | Mouse/touch-only or unlabeled controls | Basic labels | Screen reader, focus order, targets, contrast, dynamic type verified |
| Adaptive layout | Breaks on devices or keyboard | Common phone sizes pass | Phones, tablets, foldables, landscape, RTL/long text considered |
| Performance | Slow launch, janky scroll, blocked gestures | Acceptable local feel | Launch, transition, image, render, battery, and gesture latency optimized |
| System states | Only happy path designed | Loading/error exist | Empty, loading, error, offline, partial, disabled, success are complete |
| Design consistency | Random styles and components | Repeated components | Tokens, spacing, radius, type, color, motion, and platform fit are coherent |
| Trust and retention | Dark patterns or unclear consequences | Honest but minimal | Clear value, privacy, pricing, cancellation, and useful return loops |

## Design Consistency Gates

Before calling a redesign good, check:

- **Platform fit**: iOS feels like iOS and Android feels like Android unless the product intentionally owns a cross-platform system.
- **Typography**: scalable type, readable line lengths, clear hierarchy, no clipping under dynamic type/font scaling.
- **Spacing**: repeated rhythm and density; controls do not crowd gesture areas, keyboards, or system UI.
- **Color**: semantic palette with accessible contrast; color is not the only signal.
- **Shape**: one radius system; buttons, inputs, cards, sheets, tabs, and tags follow a rule.
- **Elevation**: shadows, surfaces, sheets, and overlays communicate hierarchy rather than decoration.
- **Iconography**: one icon family and consistent stroke/fill logic; ambiguous icons have labels.
- **Motion**: purposeful transitions with reduced-motion fallback; no animation that delays task completion.
- **Copy**: labels are specific, buttons say what happens, errors tell users how to fix the problem.
- **Aesthetic fit**: style follows audience and product job, not generic AI gradients, repeated cards, or trend imitation.

## Discovery Pass

Inspect before judging. Search for:

```bash
rg -n "MaterialApp|CupertinoApp|go_router|AutoRoute|Navigator|NavigationBar|BottomNavigationBar|Drawer|TabBar|Semantics|Tooltip|SafeArea|MediaQuery|LayoutBuilder" .
rg -n "NavigationContainer|createNativeStackNavigator|createBottomTabNavigator|accessibilityLabel|accessibilityHint|accessibilityRole|accessibilityState|SafeAreaView|KeyboardAvoidingView" .
rg -n "NavigationStack|NavigationView|TabView|toolbar|sheet|accessibilityLabel|accessibilityHint|accessibilityValue|DynamicType|isAccessibilityElement|UIAccessibility|UITabBarController|UINavigationController" .
rg -n "NavHost|NavController|NavigationBar|NavigationRail|ModalNavigationDrawer|Scaffold|semantics|contentDescription|stateDescription|Role\\.|importantForAccessibility|labelFor" .
rg -n "onboarding|signup|sign-up|login|auth|permission|notification|paywall|subscribe|checkout|empty|error|loading|offline|analytics|track" .
```

Run the bundled scanner when available:

```bash
python scripts/mobile_ux_static_scan.py .
```

Then produce:

- App type and likely primary user job.
- Screen inventory and top-level destinations.
- First-run flow from install/open to first value.
- Primary task flow with tap count, waits, account gates, permissions, and error paths.
- Return flow: push/deep link/open from recents/resume state.

## Audit Checklist

### First Launch and Onboarding

- Show value before asking for account creation, payment, contacts, location, camera, photos, notifications, or tracking.
- Ask permissions only at the moment they support a user action; use a clear pre-permission rationale only when it reduces confusion.
- Replace static carousel onboarding with interactive setup when possible.
- Let users skip nonessential setup and return later.
- Preserve progress if auth, payment, permissions, or network interrupts the flow.
- Keep copy concrete: what the user can do now, what happens next, and why information is needed.

### Navigation and Information Architecture

- Use bottom navigation/tab bars for a small set of persistent top-level destinations. Keep labels short and destinations stable.
- Avoid hiding primary destinations behind a drawer on phones when there are only a few key areas.
- Do not mix multiple primary navigation systems unless one clearly adapts by screen size.
- Keep the current section visible during lateral navigation.
- Use platform-native back/up/close behavior: reverse chronological back for Android, hierarchy-aware back/close on iOS modals.
- Every screen needs an obvious next action, back path, and recovery path.
- Deep links and notifications should land users at the relevant content with context, not just the home screen.

### Core Task Flow

- Identify the user's main job and count unnecessary taps, repeated fields, modal interruptions, waits, and context switches.
- Make one primary action visually dominant per state.
- Use sensible defaults, remembered choices, autofill, recent items, and progressive disclosure.
- Avoid blocking the task with education, upsells, ratings, or permissions before value.
- Keep destructive, purchase, and privacy-sensitive actions explicit and reversible where possible.

### Forms, Input, and Errors

- Use visible labels, not placeholder-only labels.
- Set correct keyboard/input types, autofill hints, capitalization, validation, and password manager compatibility.
- Validate inline after the user can reasonably correct the field; do not fail only after submit.
- Keep error messages close to fields, specific, and action-oriented.
- Avoid redundant entry. Reuse known profile, shipping, billing, and account data when appropriate.
- On mobile checkout or subscription flows, reduce fields before reducing steps; long unnecessary forms are high-friction.

### Feedback, Loading, Empty, and Offline States

- Show immediate feedback for taps, form submission, saving, syncing, and long-running actions.
- Use skeletons/progress only when they reflect actual state; avoid fake delays.
- Empty states should explain what is missing and offer a next action.
- Error states should say what happened, what the user can do, and whether data is safe.
- Offline states should preserve read/write where feasible and sync later.
- Confirm critical success states; do not leave users guessing after payment, booking, upload, or submission.

### Visual Hierarchy and Interaction

- Design for scan order: the most important content/action appears where the platform and reading direction make it easiest to find.
- Keep text legible under Dynamic Type/font scaling and avoid clipped labels.
- Maintain safe areas around notches, system bars, home indicators, gesture regions, keyboards, and fold/hinge areas.
- Use spacing to group related controls and separate unrelated actions.
- Use familiar iconography and always label ambiguous icons.
- Motion should clarify state changes, not slow task completion. Respect Reduce Motion.
- Use haptics sparingly for confirmation, warning, or physical-feeling controls.

### Accessibility

- Test with VoiceOver and TalkBack for all critical flows.
- Every interactive custom control needs role, name/label, value/state, hint when needed, and action.
- Focus order must match visual/task order and must not trap users.
- Touch targets should meet platform expectations: Flutter's guideline API checks 48 by 48 for Android and 44 by 44 for iOS; WCAG 2.2 adds target-size criteria for broader accessibility review.
- Do not communicate meaning with color alone. Add text, icons, position, shape, pattern, audio, or haptic cues.
- Support dynamic text, bold text, high contrast, reduced motion, screen readers, switch access, keyboard/external input where relevant, captions/transcripts for media, and accessible authentication.
- Decorative images should be hidden from assistive technologies; meaningful images need useful labels.

### Adaptive Layout

- Audit compact phone, large phone, tablet, foldable, landscape, split-screen, and keyboard-open states when supported.
- Switch navigation patterns by size class where appropriate: bottom navigation on compact phones, navigation rail or sidebar/drawer on larger surfaces.
- Avoid stretching phone layouts across tablets. Use extra width for supporting panes, sidebars, multi-column content, or detail views.
- Preserve state across rotation, resize, split-screen, process death, and app resume.
- Test RTL languages and long localized strings if the app is localized.

### Ethical Retention and Engagement

- Define the valuable return reason: unfinished task, fresh content, useful reminder, social response, saved progress, personal insight, or recurring real-world need.
- Make the home screen answer "what should I do now?" within a few seconds.
- Use personalization to reduce effort, not to bury controls or create anxiety.
- Ask for notification permission after the user sees value; provide granular controls and quiet defaults.
- Use streaks, rewards, and progress indicators only when they support the user's goal. Add forgiveness, pause, and recovery.
- Make settings, privacy, cancellation, logout, and delete paths findable.
- Instrument friction: first value time, task completion, abandon points, retry loops, error rates, permission acceptance, uninstall causes, DAU/MAU only when meaningful for the app category.

## Framework-Specific Fix Map

### Flutter

- Navigation: prefer `NavigationBar`, `NavigationRail`, `TabBar`, `Navigator`, `go_router`, or existing app routing. Use `Drawer` only when it fits the hierarchy.
- Adaptation: use `SafeArea`, `MediaQuery`, `LayoutBuilder`, `OrientationBuilder`, breakpoints, and Material/Cupertino widgets intentionally.
- Accessibility: add `Semantics`, `MergeSemantics`, `ExcludeSemantics`, `Tooltip` for icon-only controls, semantic labels for meaningful images, and accessibility guideline widget tests.
- Verification: run widget tests using `meetsGuideline(androidTapTargetGuideline)`, `meetsGuideline(iOSTapTargetGuideline)`, `labeledTapTargetGuideline`, and `textContrastGuideline` when test setup exists.

### React Native

- Navigation: inspect React Navigation/native stack/bottom tabs/drawer usage. Preserve native-stack behavior where possible.
- Layout: use safe-area handling, `KeyboardAvoidingView` or platform-specific keyboard strategy, responsive spacing, and platform conditionals only where behavior differs.
- Accessibility: use `accessible`, `accessibilityLabel`, `accessibilityHint`, `accessibilityRole`, `accessibilityState`, `accessibilityActions`, and `importantForAccessibility`. Avoid production reliance on experimental APIs unless the project already accepted that risk.
- Verification: use simulator/device walkthroughs, VoiceOver/TalkBack, Detox/Appium/accessibility IDs where present.

### Swift, SwiftUI, and UIKit

- Navigation: prefer `NavigationStack`, `TabView`, `sheet`, `toolbar`, `UINavigationController`, `UITabBarController`, and standard Back/Close behavior.
- Platform fit: use SF Symbols, Dynamic Type, safe areas, system controls, native sheets, confirmation dialogs, and standard search patterns before custom UI.
- Accessibility: use SwiftUI accessibility modifiers (`accessibilityLabel`, `accessibilityValue`, `accessibilityHint`, actions) or UIKit `UIAccessibility` properties (`isAccessibilityElement`, `accessibilityLabel`, `accessibilityValue`, `accessibilityHint`, traits).
- Verification: use Accessibility Inspector, VoiceOver, Dynamic Type sizes, Reduce Motion, high contrast, and different device classes.

### Kotlin, Java, Android Views, and Jetpack Compose

- Navigation: inspect Navigation Component, Compose Navigation, `NavHost`, `NavController`, `NavigationBar`, `NavigationRail`, `ModalNavigationDrawer`, `Scaffold`, and XML navigation graphs.
- Platform fit: use Material 3 components, Android back behavior, edge-to-edge/safe insets, keyboard handling, and adaptive layouts for tablets/foldables.
- Accessibility in Compose: rely on built-in Material semantics where possible; add `Modifier.semantics`, `contentDescription`, `stateDescription`, `role`, and custom actions for custom components.
- Accessibility in Views: use `android:contentDescription`, `android:labelFor`, `importantForAccessibility`, proper focus order, and concise labels.
- Verification: use TalkBack, Accessibility Scanner, Layout Inspector semantics, UIAutomator/Espresso/Compose UI tests where available.

## Report Template

```markdown
## Findings

| Severity | Flow/Screen | Evidence | User Impact | Fix |
| --- | --- | --- | --- | --- |
| P1 | Onboarding step 2 | `path/file.ext:42`, screenshot, or route name | Users must grant notifications before seeing value | Move notification ask after first successful action; add in-app reminder settings |

## Flow Map

Current: Open -> carousel -> permission -> sign in -> blank home
Recommended: Open -> value preview -> optional setup -> first action -> account save prompt

## Implementation Notes

- Framework-specific files/components to change.
- Native component or accessibility API to use.
- Analytics/events to add or inspect.

## Verification

- What was run.
- What could not be run.
- Remaining UX risks.
```

## Common Failure Modes

- Auditing only visuals and missing task completion, permissions, errors, empty states, and return flows.
- Copying iOS patterns into Android or Material patterns into iOS without adapting navigation, gestures, and accessibility.
- Recommending more screens instead of removing decisions and fields.
- Treating retention as addiction instead of repeated successful value.
- Adding custom buttons, tabs, switches, sliders, or sheets without semantics, focus order, hit targets, and native behavior.
- Ignoring large text, screen readers, keyboard overlap, safe areas, tablets, foldables, RTL, and slow networks.

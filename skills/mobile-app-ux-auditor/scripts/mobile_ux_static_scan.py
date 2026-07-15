#!/usr/bin/env python3
"""Static mobile UX signal scanner.

This script detects review signals in Flutter, React Native, Swift/iOS, and
Android projects. It is evidence gathering, not a full accessibility audit.
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


EXCLUDE_DIRS = {
    ".git",
    "node_modules",
    "Pods",
    "DerivedData",
    ".gradle",
    "build",
    ".dart_tool",
    ".expo",
    "coverage",
    "ios/Pods",
    "android/build",
}

EXTENSIONS = {
    ".dart",
    ".jsx",
    ".tsx",
    ".js",
    ".ts",
    ".swift",
    ".kt",
    ".kts",
    ".java",
    ".xml",
}


@dataclass
class Finding:
    severity: str
    platform: str
    category: str
    title: str
    path: str
    line: int
    evidence: str
    fix: str


PATTERNS = [
    (
        "P1",
        "React Native",
        "Accessibility",
        "Touchable/Pressable likely missing role or label",
        re.compile(r"<(?:Pressable|TouchableOpacity|TouchableHighlight|TouchableWithoutFeedback)\b(?![^>\n]*accessibility(?:Role|Label))", re.I),
        "Add accessibilityRole, accessibilityLabel, accessibilityState, and keyboard/screen-reader behavior.",
    ),
    (
        "P2",
        "React Native",
        "Forms",
        "TextInput placeholder-label risk",
        re.compile(r"<TextInput\b[^>\n]*placeholder\s*=", re.I),
        "Verify a persistent visible label and accessibilityLabel are present.",
    ),
    (
        "P1",
        "React Native",
        "Images",
        "Image likely missing accessibility label",
        re.compile(r"<Image\b(?![^>\n]*(?:accessibilityLabel|alt)\s*=)", re.I),
        "Add accessibilityLabel for meaningful images or mark decorative images inaccessible.",
    ),
    (
        "P2",
        "Flutter",
        "Accessibility",
        "IconButton likely missing tooltip",
        re.compile(r"\bIconButton\s*\(", re.I),
        "Verify tooltip/semanticLabel exists so screen readers and long-press hints are useful.",
    ),
    (
        "P1",
        "Flutter",
        "Images",
        "Image likely missing semantic label",
        re.compile(r"\bImage\.(?:asset|network|file|memory)\s*\((?![^;\n]*semanticLabel\s*:)", re.I),
        "Add semanticLabel for meaningful images or exclude decorative images from semantics.",
    ),
    (
        "P2",
        "Flutter",
        "Forms",
        "Text field needs persistent labeling",
        re.compile(r"\bText(?:Form)?Field\s*\(", re.I),
        "Verify InputDecoration has labelText/semantic labeling, helper/error text, and keyboard/autofill hints.",
    ),
    (
        "P1",
        "Swift/iOS",
        "Accessibility",
        "Image likely missing accessibility label",
        re.compile(r"\bImage\s*\([^)]+\)(?![^\n]*accessibilityLabel)", re.I),
        "Add accessibilityLabel for meaningful images or mark decorative images hidden.",
    ),
    (
        "P2",
        "Swift/iOS",
        "Layout",
        "Broad ignoresSafeArea risk",
        re.compile(r"\.ignoresSafeArea\s*\(\s*\)", re.I),
        "Constrain ignored safe areas to intentional background layers, not interactive content.",
    ),
    (
        "P2",
        "Swift/iOS",
        "Permissions",
        "Permission request needs value-first timing",
        re.compile(r"requestAuthorization|requestWhenInUseAuthorization|requestAlwaysAuthorization", re.I),
        "Verify permission is requested at the moment of user intent and has a clear rationale.",
    ),
    (
        "P1",
        "Android Compose",
        "Accessibility",
        "Icon likely missing contentDescription",
        re.compile(r"\bIcon\s*\((?![^)\n]*contentDescription\s*=)", re.I),
        "Set contentDescription for meaningful icons or null for decorative icons.",
    ),
    (
        "P1",
        "Android Compose",
        "Accessibility",
        "Clickable modifier may need role/state semantics",
        re.compile(r"\.clickable\s*\(", re.I),
        "Verify role, stateDescription, custom actions, and target size for custom clickable UI.",
    ),
    (
        "P2",
        "Android Compose",
        "Forms",
        "TextField needs explicit label/error support",
        re.compile(r"\b(?:OutlinedTextField|TextField)\s*\(", re.I),
        "Verify label, supportingText/error state, keyboardOptions, and autofill behavior.",
    ),
    (
        "P1",
        "Android Views",
        "Accessibility",
        "ImageView likely missing contentDescription",
        re.compile(r"<ImageView\b(?![^>\n]*android:contentDescription\s*=)", re.I),
        "Add android:contentDescription for meaningful images or @null for decorative images.",
    ),
    (
        "P2",
        "Android Views",
        "Forms",
        "EditText likely missing hint/label relationship",
        re.compile(r"<EditText\b(?![^>\n]*android:hint\s*=)", re.I),
        "Use hint/labelFor or Material TextInputLayout with clear errors and keyboard input type.",
    ),
    (
        "P2",
        "All",
        "Retention",
        "Notification or permission ask found",
        re.compile(r"requestPermissions?|POST_NOTIFICATIONS|UNUserNotificationCenter|notifications?\b", re.I),
        "Check this is value-timed, optional when possible, and paired with granular settings.",
    ),
]


def contained_path(root: Path, candidate: Path) -> Path | None:
    """Resolve a non-linked path only when it remains under the scan root."""
    try:
        if candidate.is_symlink():
            return None
        resolved = candidate.resolve(strict=True)
        resolved.relative_to(root)
        return resolved
    except (OSError, RuntimeError, ValueError):
        return None


def iter_files(root: Path) -> Iterable[Path]:
    for path in root.rglob("*"):
        resolved = contained_path(root, path)
        if resolved is None or not resolved.is_file():
            continue
        relative = resolved.relative_to(root)
        if any(part in EXCLUDE_DIRS for part in relative.parts):
            continue
        if resolved.suffix.lower() not in EXTENSIONS:
            continue
        if resolved.stat().st_size > 1_000_000:
            continue
        yield resolved


def detect_stack(root: Path, files: list[Path]) -> list[str]:
    stack: list[str] = []
    if contained_path(root, root / "pubspec.yaml") is not None:
        stack.append("Flutter")
    package_json = root / "package.json"
    safe_package_json = contained_path(root, package_json)
    if safe_package_json is not None and safe_package_json.is_file():
        try:
            data = json.loads(safe_package_json.read_text(encoding="utf-8"))
            deps = " ".join(
                list((data.get("dependencies") or {}).keys())
                + list((data.get("devDependencies") or {}).keys())
            )
            if "react-native" in deps:
                stack.append("React Native")
            if "expo" in deps:
                stack.append("Expo")
        except Exception:
            stack.append("package.json present, unreadable")
    if any(path.suffix.lower() == ".swift" for path in files):
        stack.append("Swift/iOS")
    if any(path.suffix.lower() in {".kt", ".java"} for path in files):
        stack.append("Android Kotlin/Java")
    if (safe_android := contained_path(root, root / "android")) is not None and safe_android.is_dir():
        stack.append("Android project")
    if (safe_ios := contained_path(root, root / "ios")) is not None and safe_ios.is_dir():
        stack.append("iOS project")
    return sorted(set(stack)) or ["Unknown mobile stack"]


def global_findings(root: Path, stack: list[str], all_text: str) -> list[Finding]:
    findings: list[Finding] = []
    if "Flutter" in stack and "SafeArea" not in all_text:
        findings.append(
            Finding("P2", "Flutter", "Layout", "SafeArea not found", ".", 0, "No SafeArea token found", "Verify content avoids notches, system bars, keyboards, and gesture areas.")
        )
    if "React Native" in stack and "SafeAreaView" not in all_text and "useSafeAreaInsets" not in all_text:
        findings.append(
            Finding("P2", "React Native", "Layout", "Safe-area handling not found", ".", 0, "No SafeAreaView/useSafeAreaInsets token found", "Verify content avoids notches, system bars, and gesture areas.")
        )
    if ("Android Kotlin/Java" in stack or "Android project" in stack) and "WindowInsets" not in all_text and "safeDrawing" not in all_text:
        findings.append(
            Finding("P2", "Android", "Adaptive layout", "Inset handling not found", ".", 0, "No WindowInsets/safeDrawing token found", "Verify edge-to-edge layouts account for system bars and IME.")
        )
    return findings


def scan(root: Path) -> tuple[list[str], list[Finding], int]:
    findings: list[Finding] = []
    files = list(iter_files(root))
    stack = detect_stack(root, files)
    snippets: list[str] = []
    for file_path in files:
        rel = file_path.relative_to(root).as_posix()
        try:
            lines = file_path.read_text(encoding="utf-8", errors="ignore").splitlines()
        except Exception:
            continue
        snippets.extend(lines[:2000])
        for idx, line in enumerate(lines, start=1):
            stripped = line.strip()
            if not stripped:
                continue
            for severity, platform, category, title, pattern, fix in PATTERNS:
                if pattern.search(stripped):
                    findings.append(
                        Finding(
                            severity=severity,
                            platform=platform,
                            category=category,
                            title=title,
                            path=rel,
                            line=idx,
                            evidence=stripped[:180],
                            fix=fix,
                        )
                    )
    findings = global_findings(root, stack, "\n".join(snippets)) + findings
    return stack, findings, len(files)


def render_markdown(root: Path, stack: list[str], findings: list[Finding], file_count: int) -> str:
    counts = {key: sum(1 for item in findings if item.severity == key) for key in ("P0", "P1", "P2", "P3")}
    out = [
        "# Mobile UX Static Scan",
        "",
        f"Root: `{root}`",
        f"Files scanned: `{file_count}`",
        f"Detected stack: {', '.join(stack)}",
        f"Findings: P0={counts['P0']} P1={counts['P1']} P2={counts['P2']} P3={counts['P3']}",
        "",
        "> Static scan output is a triage signal. Confirm every finding in the app or code before changing behavior.",
        "",
    ]
    if not findings:
        out.append("No matching static UX signals found.")
        return "\n".join(out)

    out.extend(["| Severity | Platform | Category | Location | Signal | Evidence | Fix |", "| --- | --- | --- | --- | --- | --- | --- |"])
    for item in findings[:140]:
        location = item.path if item.line == 0 else f"{item.path}:{item.line}"
        evidence = item.evidence.replace("|", "\\|")
        out.append(
            f"| {item.severity} | {item.platform} | {item.category} | `{location}` | {item.title} | `{evidence}` | {item.fix} |"
        )
    if len(findings) > 140:
        out.append(f"\nTruncated to 140 findings out of {len(findings)}. Narrow the scan path for more detail.")
    return "\n".join(out)


def main() -> int:
    parser = argparse.ArgumentParser(description="Scan a mobile app for static UX review signals.")
    parser.add_argument("root", nargs="?", default=".", help="Project root or subdirectory to scan")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    if not root.exists():
        raise SystemExit(f"Path does not exist: {root}")
    if not root.is_dir():
        raise SystemExit(f"Path is not a directory: {root}")
    stack, findings, file_count = scan(root)
    print(render_markdown(root, stack, findings, file_count))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

God - Local AI assistant for iOS (final package)
================================================

This package contains the app source for "God" - a local AI assistant designed
for jailbroken iOS devices (iOS 16.6, rootHide-aware).

Contents:
- app/: Flask server + web UI (templates + static)
- requirements.txt, pyproject.toml, VERSION
- .github/workflows/build-ios.yml (Briefcase-based macOS build workflow)

Build:
1. Push this repository to GitHub.
2. Use GitHub Actions (macOS runner) with Briefcase to build the iOS app.
3. Download artifacts (God.app.zip or God.ipa).

Install (jailbroken device recommended):
- Copy God.app to /Applications, set permissions, ldid -S, uicache, respring.
- Or rename God.ipa -> God.tipa and install via TrollStore (may work depending on device).

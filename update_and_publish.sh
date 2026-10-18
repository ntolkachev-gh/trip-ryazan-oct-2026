#!/usr/bin/env bash
# Daily: fetch weather, rebuild, commit+push only if changed.
set -e; cd "$(dirname "$0")"
python3 update_weather.py && python3 build.py
git add -A . && git reset -q img/food/raw 2>/dev/null || true
if git diff --cached --quiet; then echo "no changes"; exit 0; fi
git commit -qm "weather: $(TZ=Europe/Moscow date '+%Y-%m-%d %H:%M')"
git push -q "https://x-access-token:${GITHUB_TOKEN}@github.com/ntolkachev-gh/trip-ryazan-oct-2026.git" HEAD 2>&1 | sed "s/${GITHUB_TOKEN}/***/g"
echo pushed

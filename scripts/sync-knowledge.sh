#!/usr/bin/env bash
# Copies the single-source knowledge files (knowledge/, editable in Obsidian)
# into each skill's references/ folder. Run after editing anything in knowledge/.
set -euo pipefail
cd "$(dirname "$0")/.."

declare -A MAP=(
  [master-shifu]="principles disagreements sources hevy video-index muscle-ladder"
  [intake]="intake hevy"
  [programme-design]="principles exercise-tiers training-science goals-strength-athletic intake hevy workout-templates muscle-ladder programme-patterns"
  [specialisation]="training-science exercise-tiers workout-templates muscle-ladder programme-patterns"
  [progression]="training-science principles hevy muscle-ladder nutrition"
  [exercise-swaps]="exercise-tiers principles hevy"
  [nutrition]="nutrition training-science"
)

for skill in "${!MAP[@]}"; do
  dest="skills/$skill/references"
  rm -rf "$dest" && mkdir -p "$dest"
  for f in ${MAP[$skill]}; do
    cp "knowledge/$f.md" "$dest/$f.md"
  done
done
echo "Synced knowledge into ${#MAP[@]} skills."

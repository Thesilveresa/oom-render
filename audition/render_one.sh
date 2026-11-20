#!/bin/bash
# render_one.sh <slug>: one 30 s audition clip (3 s settle first) + labelled reel segments
set -euo pipefail
cd "$(dirname "$0")"
S="$1"; GRID="${GRID:-1800}"; HEAP="${HEAP:-12g}"
mkdir -p out seg
java -Xmx"$HEAP" -jar oom-render.jar --project "projects/$S.lxp" --automation empty_automation.json --channels 1,2 \
  --start 0 --record 6 --end 66 --grid "$GRID" --sim 165 --size "$GRID" --fps 30 --crf 16 --video "out/$S.mp4"
while pgrep -x ffmpeg >/dev/null; do sleep 2; done
python3 segment.py "$S" "$GRID"
ls -la out seg

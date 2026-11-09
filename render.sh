#!/bin/bash
# render.sh <movement>   e.g. ./render.sh VI
# Renders one movement of Orders of Magnitude to out/OOM_<movement>_<grid>.mp4 (picture only).
# GRID (default 1800) and HEAP (default 12g) can be overridden from the environment.
set -euo pipefail
cd "$(dirname "$0")"
M="$1"; GRID="${GRID:-1800}"; HEAP="${HEAP:-12g}"; FROM="${FROM:-0}"; LIMIT="${LIMIT:-0}"
read -r ST REC END < <(python3 -c "import json;w=json.load(open('windows.json'))['$M'];print(w['start'],w['record'],w['end'])")
mkdir -p out
NAME="OOM_${M}_${GRID}"; [ "$FROM" != "0" ] && NAME="${NAME}_from${FROM}"
# LIMIT (minutes): stop cleanly before a hard time limit; the movie written so far is kept and finalized
TO=(); [ "$LIMIT" != "0" ] && TO=(timeout -s TERM "${LIMIT}m")
echo "Movement $M: beats $REC -> $END at ${GRID} x ${GRID}"
"${TO[@]}" java -Xmx"$HEAP" -jar oom-render.jar \
  --project project/OOM2D_Revised.lxp --automation "automation/m${M}_automation.json" \
  --start "$ST" --record "$REC" --end "$END" \
  --grid "$GRID" --sim 165 --size "$GRID" --fps 30 --crf 16 --from-frame "$FROM" --no-skip \
  --video "out/${NAME}.mp4" || echo "Stopped early (time limit) - the movie so far is in out/${NAME}.mp4; render the rest with FROM=<next frame>"
while pgrep -x ffmpeg >/dev/null; do sleep 2; done   # let ffmpeg finish writing the movie
ls -la out

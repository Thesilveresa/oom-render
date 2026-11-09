# Orders of Magnitude — offline render (Movements II–VII, 1800 × 1800, picture only)

Renders the revised score (OOM2D_Revised) straight from the Chromatik project + Ableton automation,
one GitHub job per movement in parallel, then joins them into one movie.

| Movement | Length | Frames |
|---|---|---|
| II | 2:41 | 4,818 |
| III | 3:45 | 6,738 |
| IV | 3:15 | 5,847 |
| V | 3:05 | 5,536 |
| VI | 6:09 | 11,062 |
| VII | 4:31 | 8,132 |

Full piece ≈ 22:05 on the timeline (overlaps between movements are blended where both are playing).

## One-time setup (all in the browser)

1. GitHub → **New repository** → name it e.g. `oom-render` → **Public** (public = free machines) → Create.
2. On the empty repo page click **uploading an existing file**, drag in everything from this folder
   (oom-render.jar, render.sh, assemble.py, windows.json, README.md, the `project` and `automation` folders) → Commit.
3. The workflow files live in a hidden folder that Finder won't drag, so add them by hand:
   **Add file → Create new file**, name it exactly `.github/workflows/render.yml`,
   paste in the contents of `workflow-render.yml.txt` → Commit.
   Repeat with `.github/workflows/assemble.yml` and `workflow-assemble.yml.txt`.

## Rendering

**Actions** tab → **Render Orders of Magnitude** → **Run workflow** → leave the defaults → **Run workflow**.

- Six movement jobs start at once. Each one is capped at about 5h40m and stops cleanly if it gets there,
  keeping everything rendered so far.
- When they finish, an **assemble** job joins them. Tick **Also make a 3600 x 3600 upscaled copy** when starting
  the run if you want the wall-size version too (adds a few hours).
- Download from the bottom of the run page, under **Artifacts**: `OrdersOfMagnitude_FULL` is the finished piece;
  `OOM_<movement>_1800_from0` are the individual movements. Artifacts stay up for 30 days.

## If a movement stops at the time limit

Its log ends with "Stopped early". Its movie is still there, just short. Download that movement's artifact and
note how many frames it has (or the last "frame N/…" line in the log). Then:

1. **Run workflow** again with *movements* = just that one (e.g. `VI`) and *from_frame* = that frame count.
   Picking up mid-movement replays everything before it without writing, so the join is seamless (tested to match a
   continuous render).
2. Run **Assemble full piece from earlier runs** with the run IDs of both runs (the number at the end of each
   run page's URL, separated by a space).

## Notes

- Movement I isn't in the piece, and the Movement VIII channels are ignored.
- The "----------------" placeholder in VII is forced off.
- The muted OSC tracks are treated like any other track.
- Two automation lanes (on the "----------------" slot) are switched off in Ableton, so they're left out, the same as
  live. Seven lanes still pointed at a second Galaxy that no longer exists inside the Island Universe rack, so they
  were dropped (Chromatik ignores them too).
- Simulations run at Chromatik's size (165), so physics and pacing match what you composed. Pixels are drawn at 1800.
- Device code: your current (Nov 5) devices including Detail Scale, plus the render-only changes from the earlier
  renders (field sizes, Murmuration/Stigmergy/Topology display layers, Data Topology edge fix, soft crystal edges in
  Dendritic Snow).

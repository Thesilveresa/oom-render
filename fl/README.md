# Form Language: offline render (1800 x 1800, picture only)

One GitHub job per chapter and look, all in parallel (`.github/workflows/formlanguage.yml`, triggered by pushes to
`fl/` on the `previews` branch). Each chapter is one continuous take, from its group switching on to switching off.

- `project/FormLanguage_2D.lxp`: Theresa's project as sent (Nov 28). `_new.lxp` adds the OoM master Soften +
  Sparkle (render copy only), held at the median of the OoM master lanes, for the "New" look.
- `automation*/chN_automation.json`: Ableton lanes per chapter (`tools/extract_automation.py` with chapter groups
  of three channels: group, Cube, Cyl). `windows.json`: chapter on/off times in beats (120 bpm).
- `media/`: images the Slideshow / Image patterns use, found by file name. Chapter 5's stills (1.jpg ... 10.png)
  go here too.
- Jar: after24 (OoM "New") plus the Slideshow fix: the GIF covers the face edge to edge at its true aspect,
  full resolution, bilinear; the back face shows the same picture as the front (one image, as in an
  orthographic front view) rather than a mirrored double.
- Looks: `new` (DXV3 .mov made too) and `plain` (project exactly as composed, no added master effects).

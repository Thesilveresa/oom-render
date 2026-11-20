# segment.py <slug> <grid>: 2 s title card + the clip, at full size and at 900, encoded identically so the reel can be joined without re-encoding
import json, subprocess, sys, os
s, grid = sys.argv[1], int(sys.argv[2])
os.makedirs('seg', exist_ok=True)
c = next(c for c in json.load(open('candidates.json')) if c['slug'] == s)
num, name = s.split('_', 1)
same = ('same as ' + ', '.join(f[:-4] for f in c['same_as'])) if c['same_as'] else ''
font = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
def esc(t): return t.replace('\\', '\\\\').replace(':', '\\:').replace("'", "’").replace('%', '\\%')
for size, crf, tag in ((grid, 16, 'full'), (min(grid, 900), 20, '900')):
    fs = size // 12
    txt = f"drawtext=fontfile={font}:text='{esc(num)}':fontsize={fs // 2}:fontcolor=0x888888:x=(w-tw)/2:y=h/2-{int(fs * 1.6)}," \
          f"drawtext=fontfile={font}:text='{esc(c['file'][:-4])}':fontsize={fs}:fontcolor=white:x=(w-tw)/2:y=(h-th)/2"
    if same: txt += f",drawtext=fontfile={font}:text='{esc(same)}':fontsize={fs // 3}:fontcolor=0x888888:x=(w-tw)/2:y=h/2+{int(fs * 1.1)}"
    fc = f"[0:v]{txt},format=yuv420p[t];[1:v]scale={size}:{size}:flags=lanczos,fps=30,format=yuv420p,setsar=1[v];[t][v]concat=n=2:v=1[o]"
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'lavfi', '-i', f'color=black:s={size}x{size}:d=2:r=30', '-i', f'out/{s}.mp4',
                    '-filter_complex', fc, '-map', '[o]', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', str(crf),
                    '-profile:v', 'high', '-pix_fmt', 'yuv420p', '-g', '60', '-video_track_timescale', '15360', '-an',
                    f'seg/{tag}_{s}.mp4'], check=True)

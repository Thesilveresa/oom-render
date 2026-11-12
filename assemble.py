#!/usr/bin/env python3
# assemble.py <dir with OOM_<M>_<grid>.mp4 files> <output.mp4> [size]
# Lays each movement on the piece's timeline (from windows.json) and joins them into one movie.
# Where two movements overlap (one fading out while the next starts) they are screen-blended,
# everywhere else the movement is copied through untouched. Gaps, if any, are black.
import json, subprocess, sys, os, glob
src, out = sys.argv[1], sys.argv[2]
size = int(sys.argv[3]) if len(sys.argv) > 3 else None
here = os.path.dirname(os.path.abspath(__file__))
win = json.load(open(os.path.join(here, 'windows.json')))
order = ['II', 'III', 'IV', 'V', 'VI', 'VII']
mov = []
for m in order:
    fs = glob.glob(os.path.join(src, '**', f'OOM_{m}_*.mp4'), recursive=True)
    if not fs:
        sys.exit(f'missing movie for Movement {m} in {src}')
    # a movement may come in parts (OOM_VI_1800.mp4 + OOM_VI_1800_from5000.mp4): later parts win
    def part(p):
        b = os.path.basename(p)          # folder names (artifact names) also contain '_from'
        return int(b.rsplit('_from', 1)[1][:-4]) if '_from' in b else 0
    fs.sort(key=part)
    S = round(win[m]['record'] / 2 * 30)          # 120 bpm: beats / 2 = seconds; 30 fps
    parts = []
    for p in fs:
        n = int(subprocess.check_output(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-count_packets',
            '-show_entries', 'stream=nb_read_packets', '-of', 'csv=p=0', p]).decode().strip().split(',')[0])
        w = int(subprocess.check_output(['ffprobe', '-v', 'error', '-select_streams', 'v:0',
            '-show_entries', 'stream=width', '-of', 'csv=p=0', p]).decode().strip())
        s = S + part(p)
        if parts and parts[-1]['e'] > s: parts[-1]['e'] = s
        parts.append(dict(m=m, file=p, s=s, e=s + n, w=w))
    for x in parts:
        print(f"Movement {m}: frames {x['s']} - {x['e']}  ({x['file']})")
    mov += parts
W = mov[0]['w']
cuts = sorted({0} | {x['s'] for x in mov} | {x['e'] for x in mov})
segs = []
for a, b in zip(cuts, cuts[1:]):
    segs.append((a, b, [i for i, x in enumerate(mov) if x['s'] <= a and x['e'] >= b]))
uses = [sum(1 for _, _, act in segs if i in act) for i in range(len(mov))]
fc = []
for i, u in enumerate(uses):
    fc.append(f'[{i}:v]format=gbrp,split={max(u,1)}' + ''.join(f'[i{i}_{k}]' for k in range(max(u,1))))
nxt = [0] * len(mov); outs = []
for j, (a, b, act) in enumerate(segs):
    if not act:
        fc.append(f'color=c=black:s={W}x{W}:r=30:d={(b-a)/30:.6f},format=gbrp[s{j}]'); outs.append(f'[s{j}]'); continue
    labels = []
    for i in act:
        x = mov[i]; lab = f'i{i}_{nxt[i]}'; nxt[i] += 1
        fc.append(f'[{lab}]trim=start_frame={a-x["s"]}:end_frame={b-x["s"]},setpts=PTS-STARTPTS[t{j}_{i}]')
        labels.append(f't{j}_{i}')
    cur = labels[0]
    for k, l in enumerate(labels[1:]):
        fc.append(f'[{cur}][{l}]blend=all_mode=screen[b{j}_{k}]'); cur = f'b{j}_{k}'
    outs.append(f'[{cur}]')
for i, u in enumerate(uses):
    if u == 0: fc.append(f'[i{i}_0]nullsink')
scale = f',scale={size}:{size}:flags=lanczos' if size and size != W else ''
fc.append(''.join(outs) + f'concat=n={len(outs)}:v=1:a=0{scale},format=yuv420p[v]')
cmd = ['ffmpeg', '-y', '-hide_banner', '-loglevel', 'error', '-stats']
for x in mov: cmd += ['-i', x['file']]
cmd += ['-filter_complex', ';'.join(fc), '-map', '[v]', '-r', '30', '-c:v', 'libx264', '-preset', os.environ.get('PRESET', 'medium'),
        '-crf', os.environ.get('CRF', '16'), '-profile:v', 'high', '-movflags', '+faststart', out]
print(f'{len(segs)} segments, {cuts[-1]} frames ({cuts[-1]/30/60:.1f} min) -> {out}')
subprocess.run(cmd, check=True)
print('Wrote', out)

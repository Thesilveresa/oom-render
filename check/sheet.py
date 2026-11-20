# sheet.py <reel900> <chapters> <reel1800>: contact sheet of every candidate (mid + end of clip) and a few full-size crops
import subprocess, sys, os
from PIL import Image, ImageDraw
r9, chap, r18 = sys.argv[1:4]
rows = [l.split(' ', 2) for l in open(chap).read().splitlines() if l.strip()]
def t(s): m, x = s.split(':'); return int(m) * 60 + int(x)
def grab(src, ts, out, vf=None):
    cmd = ['ffmpeg', '-v', 'error', '-y', '-ss', f'{ts:.2f}', '-i', src, '-frames:v', '1']
    if vf: cmd += ['-vf', vf]
    subprocess.run(cmd + [out], check=True)
os.makedirs('check/out', exist_ok=True)
T = 180; sheet = Image.new("RGB", (4 * 2 * T, ((len(rows) + 3) // 4) * (T + 16)), (16, 16, 16)); d = ImageDraw.Draw(sheet)
for i, (ts, num, name) in enumerate(rows):
    s = t(ts)
    for k, off in enumerate((2 + 15, 2 + 29.5)):
        grab(r9, s + off, '/tmp/g.png')
        x, y = (i % 4) * 2 * T + k * T, (i // 4) * (T + 16)
        sheet.paste(Image.open('/tmp/g.png').convert('RGB').resize((T, T)), (x, y + 16))
    d.text(((i % 4) * 2 * T + 3, (i // 4) * (T + 16) + 2), f'{num} {name}', fill=(235, 235, 235))
sheet.save('check/out/contact_900.png')
for num in ('04', '21', '33', '46'):
    r = next(r for r in rows if r[1] == num)
    grab(r18, t(r[0]) + 2 + 20, f'check/out/crop1800_{num}.png', 'crop=600:600:600:600')
print('ok')

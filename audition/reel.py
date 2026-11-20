# reel.py <segdir> <tag> <out.mp4>: join the labelled segments in order, and write YouTube-style chapters
import glob, os, subprocess, sys, json
d, tag, out = sys.argv[1:4]
segs = sorted(glob.glob(f'{d}/**/{tag}_*.mp4', recursive=True), key=os.path.basename)
with open('list.txt', 'w') as f:
    for s in segs: f.write(f"file '{os.path.abspath(s)}'\n")
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', 'list.txt', '-c', 'copy', '-movflags', '+faststart', out], check=True)
t, lines = 0.0, []
names = {c['slug']: c['file'][:-4] for c in json.load(open('candidates.json'))}
for s in segs:
    slug = os.path.basename(s)[len(tag) + 1:-4]
    lines.append(f"{int(t // 60)}:{int(t % 60):02d} {slug.split('_')[0]} {names.get(slug, slug)}")
    t += float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', s], capture_output=True, text=True).stdout)
open(out[:-4] + '_chapters.txt', 'w').write('\n'.join(lines) + '\n')
print(len(segs), 'segments', f'{t:.1f}s')

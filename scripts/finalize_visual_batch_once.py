from pathlib import Path

# Match the personal-security radar shell to the working article radar.
p = Path('assets/css/ohrana-fizicheskih-lic.css')
s = p.read_text(encoding='utf-8')
block = '''\n/* personal-radar-reference-shell-v1 */
.steps-radar .radar-wrapper{
  position:relative;width:100%;max-width:420px;aspect-ratio:1/1;
  border-radius:16px;overflow:hidden;
  border:1px solid var(--line);background:var(--bg);
  box-shadow:0 0 60px rgba(240,178,74,.15);margin:0 auto
}
.steps-radar .radar-wrapper canvas{width:100%!important;height:100%!important;display:block;background:transparent}
'''
if 'personal-radar-reference-shell-v1' not in s:
    s += block
p.write_text(s, encoding='utf-8')

# Cache-bust the homepage visual fixes so hosting/browser cannot keep the old yin-yang/card/city styles.
p = Path('index.html')
s = p.read_text(encoding='utf-8')
old = '/assets/css/home-light-fix.css?v=20260921-2'
new = '/assets/css/home-light-fix.css?v=20260921-3'
if old in s:
    s = s.replace(old, new, 1)
elif new not in s:
    raise SystemExit('homepage light-fix stylesheet link not found')
p.write_text(s, encoding='utf-8')

if 'personal-radar-reference-shell-v1' not in Path('assets/css/ohrana-fizicheskih-lic.css').read_text(encoding='utf-8'):
    raise SystemExit('radar shell override missing')
if new not in Path('index.html').read_text(encoding='utf-8'):
    raise SystemExit('homepage cache buster missing')

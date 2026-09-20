from pathlib import Path

files = [
    Path('assets/css/site-shell.css'),
    Path('site-src/assets/site-shell.css'),
    Path('index.html'),
]

for p in files:
    s = p.read_text(encoding='utf-8')
    old = 'width:24px!important;height:24px!important;background:url("/images/schit.png")'
    new = 'width:30px!important;height:30px!important;background:url("/images/schit.png")'
    if old in s:
        s = s.replace(old, new)
    else:
        old2 = 'width:24px;height:24px;background:url("/images/schit.png")'
        new2 = 'width:30px;height:30px;background:url("/images/schit.png")'
        if old2 not in s:
            raise SystemExit(f'shield size pattern not found in {p}')
        s = s.replace(old2, new2)
    p.write_text(s, encoding='utf-8')
    print('updated', p)

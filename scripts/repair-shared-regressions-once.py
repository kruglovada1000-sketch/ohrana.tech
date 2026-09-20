from pathlib import Path

# 1) Contacts-only emergency visual rules must never leak to other pages.
old = """/* contacts-visual-restore-v1 */
var contactStyle=document.createElement('style');
contactStyle.textContent='.qi-msgr{display:flex;gap:8px;align-items:center}.qi-msgr a{width:34px!important;height:34px!important;flex:0 0 34px!important;display:flex!important;align-items:center!important;justify-content:center!important;border-radius:50%!important}.qi-msgr a svg{width:16px!important;height:16px!important;max-width:16px!important;max-height:16px!important}.hero-video-frame>.fig-chip{display:none!important}';
document.head.appendChild(contactStyle);"""
new = """/* contacts-visual-restore-v2: scope emergency contact fixes to the Contacts page only. */
var cleanPath=location.pathname.replace(/\\/+$/,'')||'/';
if(cleanPath==='/kontakty'){
  var contactStyle=document.createElement('style');
  contactStyle.textContent='.qi-msgr{display:flex;gap:8px;align-items:center}.qi-msgr a{width:34px!important;height:34px!important;flex:0 0 34px!important;display:flex!important;align-items:center!important;justify-content:center!important;border-radius:50%!important}.qi-msgr a svg{width:16px!important;height:16px!important;max-width:16px!important;max-height:16px!important}.hero-video-frame>.fig-chip{display:none!important}';
  document.head.appendChild(contactStyle);
}"""
for rel in ['assets/js/site.js','site-src/assets/site.js']:
    p=Path(rel); s=p.read_text(encoding='utf-8')
    if 'contacts-visual-restore-v2' not in s:
        if old not in s: raise SystemExit(f'contacts block not found in {rel}')
        s=s.replace(old,new,1)
        p.write_text(s,encoding='utf-8')

# 2) Keep generator sources aligned with published, repaired modules.
for published, source in [
    ('assets/js/ohrana-fizicheskih-lic.js','site-src/custom-js/ohrana-fizicheskih-lic.js'),
    ('assets/js/dogovor.js','site-src/custom-js/dogovor.js'),
]:
    Path(source).write_text(Path(published).read_text(encoding='utf-8'),encoding='utf-8')

# 3) Keep shared shell source identical to the repaired published shell.
Path('site-src/assets/site-shell.css').write_text(Path('assets/css/site-shell.css').read_text(encoding='utf-8'),encoding='utf-8')

# 4) The custom-page generator extracts CSS from the source HTML; preserve the repaired radar shell there too.
p=Path('site-src/pages/ohrana-fizicheskih-lic.source.html')
s=p.read_text(encoding='utf-8')
block='''\n/* personal-radar-reference-shell-v1 */
.steps-radar .radar-wrapper{
  position:relative;width:100%;max-width:420px;aspect-ratio:1/1;
  border-radius:16px;overflow:hidden;
  border:1px solid var(--line);background:var(--bg);
  box-shadow:0 0 60px rgba(240,178,74,.15);margin:0 auto
}
.steps-radar .radar-wrapper canvas{width:100%!important;height:100%!important;display:block;background:transparent}
'''
if 'personal-radar-reference-shell-v1' not in s:
    pos=s.find('</style>')
    if pos<0: raise SystemExit('style closing tag missing in personal-security source')
    s=s[:pos]+block+s[pos:]
    p.write_text(s,encoding='utf-8')

# Guardrails.
assert "if(cleanPath==='/kontakty')" in Path('assets/js/site.js').read_text(encoding='utf-8')
assert Path('assets/js/ohrana-fizicheskih-lic.js').read_text(encoding='utf-8') == Path('site-src/custom-js/ohrana-fizicheskih-lic.js').read_text(encoding='utf-8')
assert Path('assets/js/dogovor.js').read_text(encoding='utf-8') == Path('site-src/custom-js/dogovor.js').read_text(encoding='utf-8')
assert Path('assets/css/site-shell.css').read_text(encoding='utf-8') == Path('site-src/assets/site-shell.css').read_text(encoding='utf-8')
assert 'personal-radar-reference-shell-v1' in Path('site-src/pages/ohrana-fizicheskih-lic.source.html').read_text(encoding='utf-8')

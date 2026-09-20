from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')

# 1) Remove the obsolete sun/moon theme block entirely.
start = s.find('/* site-theme-toggle-v1 */')
end = s.find('/* site-theme-yinyang-v2 */')
if start == -1 or end == -1 or end <= start:
    raise SystemExit('obsolete theme block markers not found')
s = s[:start] + s[end:]

# 2) Replace the remaining yin-yang block with one high-contrast nav-only control.
start = s.find('/* site-theme-yinyang-v2 */')
end = s.find('/* Light theme: white/cream surfaces and genuinely dark copy. */', start)
if start == -1 or end == -1:
    raise SystemExit('yin-yang block markers not found')
new_block = '''/* site-theme-yinyang-v3 */
/* Single high-contrast theme control beside Contacts. */
.theme-yinyang{
  display:block;font-size:1.62rem;line-height:1;
  font-family:Georgia,'Times New Roman',serif;
  color:inherit;transform:translateY(-1px)
}
nav.nav .theme-toggle{
  display:inline-grid!important;place-items:center;
  width:38px;height:38px;flex:0 0 38px;margin:4px 0 4px 6px;align-self:center;
  border:1.5px solid rgba(232,200,122,.86);border-radius:50%;
  background:#090b0f!important;color:#fff!important;
  box-shadow:0 0 0 2px rgba(232,200,122,.12),0 8px 22px rgba(0,0,0,.28);
  transition:transform .3s var(--ease),border-color .3s,box-shadow .3s
}
nav.nav .theme-toggle:hover{
  transform:translateY(-2px) rotate(8deg);
  border-color:#F5E3B3;
  box-shadow:0 0 0 3px rgba(232,200,122,.18),0 10px 26px rgba(0,0,0,.30)
}
html[data-theme="light"] nav.nav .theme-toggle{
  background:#090b0f!important;color:#fff!important;
  border-color:#A97F2F!important;
  box-shadow:0 0 0 2px rgba(169,127,47,.22),0 7px 20px rgba(0,0,0,.20)!important
}
html[data-theme="light"] nav.nav .theme-toggle:hover{
  border-color:#745015!important;
  box-shadow:0 0 0 3px rgba(169,127,47,.26),0 9px 24px rgba(0,0,0,.22)!important
}
@media(max-width:1100px){
  nav.nav .theme-toggle{width:44px;height:44px;flex-basis:44px;margin:10px 4px 4px;align-self:flex-start}
  .theme-yinyang{font-size:1.7rem}
}
@media(max-width:420px){
  nav.nav .theme-toggle{width:42px;height:42px;flex-basis:42px}
  .theme-yinyang{font-size:1.62rem}
}

'''
s = s[:start] + new_block + s[end:]

# 3) Remove dead header-location rules left from when the toggle lived by the phone.
dead_lines = [
    'html[data-theme="light"] .hd-right .theme-toggle{background:#fff;color:#0c0c0c;border-color:rgba(169,127,47,.42);box-shadow:0 8px 22px rgba(83,61,25,.12)}\n',
    '  .hd-right .theme-toggle{width:42px;height:42px;flex-basis:42px}\n',
    '  .hd-right .theme-toggle{display:inline-grid}\n',
    '  .hd-right .theme-toggle{width:40px;height:40px;flex-basis:40px}\n',
]
for line in dead_lines:
    s = s.replace(line, '')

# Remove now-empty media block if present.
s = s.replace('@media(max-width:960px){\n}\n', '')

# 4) Guardrails: no sun/moon zombies and exactly one toggle in markup.
for zombie in ('theme-icon-sun', 'theme-icon-moon', 'site-theme-toggle-v1'):
    if zombie in s:
        raise SystemExit(f'zombie remains: {zombie}')
if s.count('id="themeToggle"') != 1:
    raise SystemExit('themeToggle id must occur exactly once')
if '<a href="/kontakty/">Контакты</a>\n      <button class="theme-toggle nav-theme-toggle" id="themeToggle"' not in s:
    raise SystemExit('theme toggle is not immediately after Contacts')
if 'html[data-theme="light"] nav.nav .theme-toggle' not in s:
    raise SystemExit('light-theme high-contrast rule missing')

p.write_text(s, encoding='utf-8')

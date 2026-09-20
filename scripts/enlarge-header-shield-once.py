from pathlib import Path

for name in ['assets/css/site-shell.css','site-src/assets/site-shell.css']:
    p=Path(name)
    s=p.read_text(encoding='utf-8')
    old='''/* brand-shield-match-home-v1 */\n.site-header .brand-ic{width:46px!important;height:46px!important;min-width:46px!important;flex:0 0 46px!important;border-radius:50%!important;background:var(--gold-grad)!important;display:grid!important;place-items:center!important}\n.site-header .brand-ic>img,.site-header .brand-ic>svg{display:none!important}\n.site-header .brand-ic::after{content:""!important;width:24px!important;height:24px!important;background:url("/images/schit.png") center/contain no-repeat!important;display:block!important}\n'''
    new='''/* brand-shield-match-home-v2 */\n.site-header .brand-ic{width:46px!important;height:46px!important;min-width:46px!important;flex:0 0 46px!important;border-radius:50%!important;background:var(--gold-grad)!important;display:grid!important;place-items:center!important}\n.site-header .brand-ic>img,.site-header .brand-ic>svg{display:none!important}\n.site-header .brand-ic::after{content:""!important;width:42px!important;height:42px!important;background:url("/images/schit.png") center/contain no-repeat!important;display:block!important}\n@media(max-width:420px){.site-header .brand-ic::after{width:36px!important;height:36px!important}}\n'''
    if old not in s:
        raise SystemExit(f'expected shield block not found in {name}')
    p.write_text(s.replace(old,new),encoding='utf-8')
    print('updated',name)

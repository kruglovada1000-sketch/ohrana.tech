from pathlib import Path

MARK='/* brand-shield-match-home-v1 */'
BLOCK='''\n\n/* brand-shield-match-home-v1 */\n.site-header .brand-ic{width:46px!important;height:46px!important;min-width:46px!important;flex:0 0 46px!important;border-radius:50%!important;background:var(--gold-grad)!important;display:grid!important;place-items:center!important}\n.site-header .brand-ic>img,.site-header .brand-ic>svg{display:none!important}\n.site-header .brand-ic::after{content:""!important;width:24px!important;height:24px!important;background:url("/images/schit.png") center/contain no-repeat!important;display:block!important}\n'''
for name in ['assets/css/site-shell.css','site-src/assets/site-shell.css']:
    p=Path(name)
    s=p.read_text(encoding='utf-8')
    if MARK not in s:
        p.write_text(s.rstrip()+BLOCK+'\n',encoding='utf-8')
        print('updated',name)
    else:
        print('already',name)

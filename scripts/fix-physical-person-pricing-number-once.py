from pathlib import Path

MARK='/* pricing-section-number-align-v1 */'
RULE='''\n\n/* pricing-section-number-align-v1 */\n#pricing .sec-head.center .sec-num{right:0!important;left:auto!important;top:-58px!important;transform:none!important}\n'''

css=Path('assets/css/ohrana-fizicheskih-lic.css')
s=css.read_text(encoding='utf-8')
if MARK not in s:
    css.write_text(s.rstrip()+RULE,encoding='utf-8')
    print('updated',css)
else:
    print('already',css)

src=Path('site-src/pages/ohrana-fizicheskih-lic.source.html')
s=src.read_text(encoding='utf-8')
if MARK not in s:
    if '</style>' not in s:
        raise SystemExit('style close not found in source')
    s=s.replace('</style>',RULE+'\n</style>',1)
    src.write_text(s,encoding='utf-8')
    print('updated',src)
else:
    print('already',src)

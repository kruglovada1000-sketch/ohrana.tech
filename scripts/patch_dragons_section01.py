from pathlib import Path

path = Path('site-src/pages/fizicheskaya-ohrana.source.html')
text = path.read_text(encoding='utf-8')

marker = '/* guard-dragons-real-v3 */'
if marker not in text:
    anchor = '.flip-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;position:relative}'
    if anchor not in text:
        raise SystemExit('CSS anchor not found')
    css = '''/* guard-dragons-real-v3 */
#guard>.wrap::after{display:none!important}
#guard .guard-intro{display:grid;grid-template-columns:minmax(0,1fr) minmax(300px,440px);gap:48px;align-items:center;position:relative;z-index:2;margin-bottom:48px}
#guard .guard-intro .sec-head{max-width:none!important;min-height:0!important;display:block!important;padding-right:0!important;margin-bottom:0}
#guard .guard-visual{margin:0;min-width:0;width:100%;padding:1px;background:linear-gradient(135deg,#F5E3B3,#E8C87A 45%,#A97F2F);clip-path:polygon(14px 0,calc(100% - 14px) 0,100% 14px,100% calc(100% - 14px),calc(100% - 14px) 100%,14px 100%,0 calc(100% - 14px),0 14px);filter:drop-shadow(0 18px 34px rgba(0,0,0,.35))}
#guard .guard-visual img{display:block;width:100%;height:auto;object-fit:contain;clip-path:polygon(13px 0,calc(100% - 13px) 0,100% 13px,100% calc(100% - 13px),calc(100% - 13px) 100%,13px 100%,0 calc(100% - 13px),0 13px)}
@media(max-width:960px){#guard .guard-intro{grid-template-columns:1fr;gap:28px;margin-bottom:40px}#guard .guard-visual{width:min(100%,620px);margin:0 auto}}
@media(max-width:640px){#guard .guard-intro{gap:20px;margin-bottom:34px}#guard .guard-visual{width:100%}}
'''
    text = text.replace(anchor, css + anchor, 1)

if 'class="guard-visual"' not in text:
    old = '''      <div class="sec-head" data-reveal>
        <span class="sec-num">01</span>
        <span class="eyebrow">Совет от практиков</span>
        <h2>Как выбрать ЧОО и <em>не ошибиться</em></h2>
        <p>Цены на охрану различаются в разы, а защищать приходится реальные деньги, товар и людей. Шесть пунктов, которые нужно проверить до подписания договора — любой компании, не только нам. Наведите курсор или коснитесь карточки, чтобы увидеть, как обстоит дело у нас.</p>
      </div>

      <div class="flip-grid" data-reveal>'''
    new = '''      <div class="guard-intro">
        <div class="sec-head" data-reveal>
          <span class="sec-num">01</span>
          <span class="eyebrow">Совет от практиков</span>
          <h2>Как выбрать ЧОО и <em>не ошибиться</em></h2>
          <p>Цены на охрану различаются в разы, а защищать приходится реальные деньги, товар и людей. Шесть пунктов, которые нужно проверить до подписания договора — любой компании, не только нам. Наведите курсор или коснитесь карточки, чтобы увидеть, как обстоит дело у нас.</p>
        </div>
        <figure class="guard-visual" data-reveal>
          <img src="/images/dragons.png" alt="Физическая охрана ЧОО «Рускорпорация»" loading="lazy" decoding="async">
        </figure>
      </div>

      <div class="flip-grid" data-reveal>'''
    if old not in text:
        raise SystemExit('section 01 anchor not found')
    text = text.replace(old, new, 1)

path.write_text(text.rstrip() + '\n', encoding='utf-8')

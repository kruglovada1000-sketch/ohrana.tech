from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
old='<img src="/images/kompleksnaja-ohrana.jpg" alt="Комплексная безопасность ЧОО «Рускорпорация»" loading="lazy" decoding="async">'
new='<img src="/images/3-sektora.png" alt="Три сектора комплексной безопасности ЧОО «Рускорпорация»" loading="lazy" decoding="async">'
if old not in s:
    raise SystemExit('replacement image markup not found')
s=s.replace(old,new,1)
p.write_text(s,encoding='utf-8')
assert '/images/3-sektora.png' in s

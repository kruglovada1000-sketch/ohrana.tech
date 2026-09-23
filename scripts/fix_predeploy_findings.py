from pathlib import Path


def replace(path: str, mapping: dict[str, str]) -> None:
    p = Path(path)
    text = p.read_text(encoding="utf-8")
    original = text
    for old, new in mapping.items():
        text = text.replace(old, new)
    if text != original:
        p.write_text(text, encoding="utf-8")


replace("index.html", {
    "/images/3-sektora.png": "/images/ceny-hero.svg",
    "Три сектора комплексной безопасности ЧОО «Рускорпорация»": "Комплексная безопасность ЧОО «Рускорпорация»",
})

image_map = {
    "/images/tarif-post-fizicheskoy-ohrany.webp": "/images/fizicheskaya-ohrana.jpg",
    "/images/tarif-usilennyy-post.webp": "/images/security-1.jpg",
    "/images/tarif-ohrana-s-oruzhiem.webp": "/images/security.jpg",
    "/images/tarif-mobilnoe-patrulirovanie.webp": "/images/ohrana-tehniki.jpg",
    "/images/tarif-pultovaya-ohrana-gbr.webp": "/images/pultovaya-ohrana.jpg",
    "/images/tarif-ohrana-meropriyatiya.webp": "/images/ohrana-meropriyatiy.jpg",
    "/images/tarif-lichnaya-ohrana.webp": "/images/lichka-ohrana.jpg",
}
replace("site-src/pricing.json", image_map)
replace("ceny/index.html", image_map)

shared_fix = """

/* predeploy-mobile-containment-v1
   Targeted safety net for legacy content: keep wide tables/cards/decorations
   inside the viewport without changing desktop presentation. */
@media(max-width:960px){
  main .cards-grid.crit7{grid-template-columns:repeat(2,minmax(0,1fr))!important}
  main .cards-grid.crit7 .sign-card{grid-column:auto!important}
  main .radar{display:none!important}
}
@media(max-width:640px){
  main .cards-grid.crit7,main .cards-grid.b2x2{grid-template-columns:minmax(0,1fr)!important}
  main .cards-grid.crit7 .sign-card{grid-column:auto!important}
  main .price-table{display:block!important;width:100%!important;max-width:100%!important;min-width:0!important;overflow-x:auto!important;-webkit-overflow-scrolling:touch}
  main img,main video,main iframe{max-width:100%}
}
"""
for filename in ("site-src/assets/site-shell.css", "css/site-shell.css"):
    p = Path(filename)
    text = p.read_text(encoding="utf-8")
    if "predeploy-mobile-containment-v1" not in text:
        p.write_text(text.rstrip() + shared_fix + "\n", encoding="utf-8")

service_fix = """

/* predeploy-service-mobile-wrap-v1 */
@media(max-width:640px){
  .service-hero>*{min-width:0}
  .service-hero h1,.service-lead{overflow-wrap:anywhere;word-break:normal}
}
"""
p = Path("css/service-pages.css")
text = p.read_text(encoding="utf-8")
if "predeploy-service-mobile-wrap-v1" not in text:
    p.write_text(text.rstrip() + service_fix + "\n", encoding="utf-8")

print("Targeted predeploy fixes applied")

from __future__ import annotations

import html
import urllib.parse
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WHATSAPP = (
    "https://api.whatsapp.com/send?phone=8615908080040&text="
    "Hello%20Pratt%20Oil%2C%20I%20need%20quotation%20for%20oilfield%20spare%20parts"
)


PRODUCTS = [
    ("kolenval-burovogo-nasosa-v-sbore", "kolenval-burovogo-nasosa-v-sbore-main.webp", "Mud Pump Crankshaft Assembly", "مجموعة عمود مرفق مضخة الطين"),
    ("burovyh-nasosov-gidravlicheskiy-tsilindr-v-sbore", "burovyh-nasosov-gidravlicheskiy-tsilindr-v-sbore-main.webp", "Mud Pump Hydraulic Cylinder Assembly", "مجموعة الأسطوانة الهيدروليكية لمضخة الطين"),
    ("burovyh-nasosov-vypusknoy-kompensator-v-sbore", "burovyh-nasosov-vypusknoy-kompensator-v-sbore-main.webp", "Mud Pump Discharge Pulsation Dampener Assembly", "مخمد نبضات التفريغ لمضخة الطين"),
    ("vtulki-burovogo-nasosa", "vtulki-burovogo-nasosa-main.webp", "Mud Pump Liners", "بطانات مضخة الطين"),
    ("porshen-burovogo-nasosa", "porshen-burovogo-nasosa-main.webp", "Mud Pump Piston", "مكبس مضخة الطين"),
    ("klapany-burovyh-nasosov", "klapany-burovyh-nasosov-main.webp", "Mud Pump Valves", "صمامات مضخة الطين"),
    ("udlinitel-porshnevogo-shtoka", "udlinitel-porshnevogo-shtoka-main.webp", "Piston Rod Extension", "وصلة تمديد قضيب المكبس"),
    ("burovoy-nasos-udlinitel-sterzhnya", "burovoy-nasos-udlinitel-sterzhnya-main.webp", "Mud Pump Rod Extension", "وصلة تمديد قضيب مضخة الطين"),
    ("polzun-burovogo-nasosa", "polzun-burovogo-nasosa-main.webp", "Mud Pump Crosshead", "رأس التوصيل لمضخة الطين"),
    ("burovye-nasosy-iznos-plastiny", "burovye-nasosy-iznos-plastiny-main.webp", "Mud Pump Wear Plate", "صفيحة التآكل لمضخة الطين"),
    ("pruzhinnyy-predohranitelnyy-klapan", "pruzhinnyy-predohranitelnyy-klapan-main.webp", "Spring Safety Valve", "صمام أمان نابضي"),
    ("uplotnenie-vtulki", "uplotnenie-vtulki-main.webp", "Liner Seal", "مانع تسرب البطانة"),
]


def esc(value: str) -> str:
    return html.escape(value, quote=True)


def card(slug: str, image: str, title: str, category: str, quote: str) -> str:
    quoted = urllib.parse.quote(title)
    return f'''            <article class="ru-product-card">
              <a href="../{slug}/">
                <div class="ru-product-card-media"><img src="../../../assets/images/ru-products/{image}" alt="{esc(title)}" title="{esc(title)}" width="900" height="650" loading="lazy" decoding="async"></div>
                <div class="ru-product-card-body"><span>{esc(category)}</span><h3>{esc(title)}</h3><p>{esc(category)}</p></div>
              </a>
              <a class="mini-btn dark" href="{WHATSAPP}%3A%20{quoted}" rel="nofollow">{esc(quote)}</a>
            </article>'''


def section(lang: str) -> str:
    if lang == "en":
        eyebrow = "BOMCO F Series"
        heading = "BOMCO F Series Mud Pump Spare Parts"
        intro = (
            "This product range follows the BOMCO F series category page from the Russian website. "
            "Buyers can open each product for image, name, quotation support and specification matching."
        )
        category = "BOMCO F Series Mud Pumps"
        quote = "Request Quote"
        cards = "\n".join(card(slug, image, en, category, quote) for slug, image, en, _ar in PRODUCTS)
    else:
        eyebrow = "سلسلة BOMCO F"
        heading = "قطع غيار مضخات الطين BOMCO F"
        intro = (
            "يعتمد هذا النطاق على صفحة فئة BOMCO F في الموقع الروسي. "
            "يمكن للمشتري فتح كل منتج لعرض الصورة والاسم ودعم عرض السعر ومطابقة المواصفات."
        )
        category = "مضخات الطين BOMCO F"
        quote = "طلب عرض سعر"
        cards = "\n".join(card(slug, image, ar, category, quote) for slug, image, _en, ar in PRODUCTS)
    return f'''      <section class="section ru-bomco-product-range" id="bomco-f-products">
        <div class="section-heading"><p class="eyebrow">{esc(eyebrow)}</p><h2>{esc(heading)}</h2><p>{esc(intro)}</p></div>
        <div class="ru-product-grid">
{cards}
        </div>
      </section>
'''


def update(path: Path, lang: str) -> None:
    text = path.read_text(encoding="utf-8")
    marker = '      <section class="section ru-model-table-section">'
    start_existing = text.find('      <section class="section ru-bomco-product-range"')
    if start_existing != -1:
        end_existing = text.find(marker, start_existing)
        text = text[:start_existing] + text[end_existing:]
    insert_at = text.index(marker)
    text = text[:insert_at] + section(lang) + text[insert_at:]
    path.write_text(text, encoding="utf-8")


def main() -> None:
    update(ROOT / "en" / "products" / "bomco-f-series-mud-pumps" / "index.html", "en")
    update(ROOT / "ar" / "products" / "bomco-f-series-mud-pumps" / "index.html", "ar")
    print("BOMCO F category product range updated for English and Arabic")


if __name__ == "__main__":
    main()

from __future__ import annotations

import html
import json
import re
import urllib.parse
import urllib.request
from pathlib import Path

from PIL import Image, ImageOps


ROOT = Path(__file__).resolve().parents[1]
SITE = "https://jilinzan9-droid.github.io/-"
WHATSAPP = (
    "https://api.whatsapp.com/send?phone=8615908080040&text="
    "Hello%20Pratt%20Oil%2C%20I%20need%20quotation%20for%20oilfield%20spare%20parts"
)


PRODUCTS = [
    {
        "slug": "bomco-f-series-mud-pumps",
        "source": "https://ecdn.cnyandex.com/pratt-oil/uploads/1.буровой-насос-нефти.jpg",
        "ru": "буровых насосов серии BOMCO F",
        "en": "BOMCO F Series Mud Pumps and Spare Parts",
        "ar": "مضخات الطين BOMCO F وقطع الغيار",
        "category_en": "Mud Pumps and Spare Parts",
        "category_ar": "مضخات الطين وقطع الغيار",
        "desc_en": "BOMCO F series drilling mud pump equipment and spare parts for oilfield pumping, fluid end maintenance and replacement support.",
        "desc_ar": "معدات مضخات الطين BOMCO F وقطع الغيار لدعم الضخ في حقول النفط وصيانة نهاية السائل والاستبدال.",
        "common_en": ["F-series mud pump", "fluid end parts", "power end parts", "liners", "pistons"],
        "common_ar": ["مضخة طين F-series", "قطع نهاية السائل", "قطع نهاية القدرة", "بطانات", "مكابس"],
        "application_en": "Used in drilling mud circulation systems, rig maintenance projects and replacement part procurement for drilling contractors.",
        "application_ar": "تستخدم في أنظمة تدوير طين الحفر ومشاريع صيانة الحفارات وشراء قطع الغيار لشركات الحفر.",
    },
    {
        "slug": "spm-tws-drilling-mud-pump",
        "source": "https://ecdn.cnyandex.com/pratt-oil/uploads/2.Плунжерный-насос.jpg",
        "ru": "Буровой насос SPM TWS",
        "en": "SPM TWS Drilling Mud Pump",
        "ar": "مضخة الطين SPM TWS",
        "category_en": "Mud Pumps and Spare Parts",
        "category_ar": "مضخات الطين وقطع الغيار",
        "desc_en": "SPM TWS drilling mud pump supply support for oilfield pumping systems, high-pressure service and spare part matching.",
        "desc_ar": "دعم توريد مضخة الطين SPM TWS لأنظمة الضخ في حقول النفط والخدمة عالية الضغط ومطابقة قطع الغيار.",
        "common_en": ["SPM TWS pump", "plunger pump", "mud pump parts", "pump modules", "seals"],
        "common_ar": ["مضخة SPM TWS", "مضخة مكبسية", "قطع مضخة الطين", "وحدات المضخة", "أختام"],
        "application_en": "Suitable for drilling mud transfer, high-pressure pumping and field maintenance operations.",
        "application_ar": "مناسبة لنقل طين الحفر والضخ عالي الضغط وعمليات الصيانة الميدانية.",
    },
    {
        "slug": "drawworks-brake-band-system-parts",
        "source": "https://ecdn.cnyandex.com/pratt-oil/uploads/3.Лебедка-буровой-установки.jpg",
        "ru": "Тормоз буровой лебедки-Лента тормозная",
        "en": "Drawworks Brake Band and Brake System Parts",
        "ar": "شريط فرامل الونش وقطع نظام الفرامل",
        "category_en": "Drawworks Brake System Parts",
        "category_ar": "قطع نظام فرامل الونش",
        "desc_en": "Drawworks brake band and brake system parts for drilling rig hoisting systems, field maintenance and modernization projects.",
        "desc_ar": "شريط فرامل الونش وقطع نظام الفرامل لأنظمة الرفع في حفارات النفط ومشاريع الصيانة والتحديث.",
        "common_en": ["brake band", "brake blocks", "drawworks brake", "brake drum", "brake system parts"],
        "common_ar": ["شريط فرامل", "بلوكات فرامل", "فرامل الونش", "أسطوانة الفرامل", "قطع نظام الفرامل"],
        "application_en": "Used for drawworks braking, hoisting control and rig safety maintenance.",
        "application_ar": "تستخدم في فرملة الونش والتحكم بالرفع وصيانة سلامة الحفار.",
    },
    {
        "slug": "drilling-rigs-and-drawworks-accessories",
        "source": "https://ecdn.cnyandex.com/pratt-oil/uploads/4.Буровые-установки-и-принадлежности-для-лебедок.jpg",
        "ru": "Буровые установки и принадлежности для лебедок",
        "en": "Drilling Rigs and Drawworks Accessories",
        "ar": "حفارات النفط وملحقات الونش",
        "category_en": "Drilling Rigs and Drawworks Accessories",
        "category_ar": "حفارات النفط وملحقات الونش",
        "desc_en": "Drilling rig and drawworks accessories for hoisting systems, field replacement and oilfield maintenance projects.",
        "desc_ar": "ملحقات حفارات النفط والونش لأنظمة الرفع والاستبدال الميداني ومشاريع صيانة حقول النفط.",
        "common_en": ["drilling rig parts", "drawworks accessories", "hoisting parts", "winch parts", "field service parts"],
        "common_ar": ["قطع الحفار", "ملحقات الونش", "قطع نظام الرفع", "قطع الونش", "قطع الخدمة الميدانية"],
        "application_en": "Used for land rigs, workover rigs, hoisting systems and drilling site maintenance.",
        "application_ar": "تستخدم في الحفارات البرية وحفارات صيانة الآبار وأنظمة الرفع وصيانة مواقع الحفر.",
    },
    {
        "slug": "hydraulic-disc-brake-system",
        "source": "https://ecdn.cnyandex.com/pratt-oil/uploads/5.гидравлический-дисковый-тормоз-PS.jpg",
        "ru": "Гидравлическое дисковое тормозное устройство",
        "en": "Hydraulic Disc Brake System",
        "ar": "نظام الفرامل القرصية الهيدروليكية",
        "category_en": "Hydraulic Disc Brake System",
        "category_ar": "نظام الفرامل القرصية الهيدروليكية",
        "desc_en": "Hydraulic disc brake system parts for drilling rig drawworks, braking upgrades and field maintenance support.",
        "desc_ar": "قطع نظام الفرامل القرصية الهيدروليكية لونش الحفار ودعم تحديث الفرامل والصيانة الميدانية.",
        "common_en": ["hydraulic disc brake", "brake caliper", "brake disc", "hydraulic brake station", "friction pads"],
        "common_ar": ["فرامل قرصية هيدروليكية", "كاليبر فرامل", "قرص فرامل", "محطة فرامل هيدروليكية", "بطانات احتكاك"],
        "application_en": "Used for drawworks braking modernization, rig hoisting safety and maintenance replacement.",
        "application_ar": "تستخدم لتحديث فرامل الونش وسلامة الرفع في الحفار والاستبدال أثناء الصيانة.",
    },
    {
        "slug": "wcb-eaton-auxiliary-brake",
        "source": "https://ecdn.cnyandex.com/pratt-oil/uploads/6.вспомогательный-тормоз.jpg",
        "ru": "WCB Eaton вспомогательного тормоза",
        "en": "WCB Eaton Auxiliary Brake",
        "ar": "فرامل WCB Eaton المساعدة",
        "category_en": "Drawworks Brake System Parts",
        "category_ar": "قطع نظام فرامل الونش",
        "desc_en": "WCB Eaton auxiliary brake and related spare parts for drilling drawworks cooling, braking and maintenance projects.",
        "desc_ar": "فرامل WCB Eaton المساعدة وقطع الغيار المرتبطة بها لمشاريع تبريد وفرملة وصيانة ونش الحفر.",
        "common_en": ["WCB brake", "Eaton auxiliary brake", "friction plate", "water cooled brake", "brake hub"],
        "common_ar": ["فرامل WCB", "فرامل Eaton المساعدة", "قرص احتكاك", "فرامل مبردة بالماء", "محور الفرامل"],
        "application_en": "Used as an auxiliary brake for drawworks and hoisting equipment in drilling rigs.",
        "application_ar": "تستخدم كفرامل مساعدة للونش ومعدات الرفع في حفارات النفط.",
    },
    {
        "slug": "wellhead-tools",
        "source": "https://ecdn.cnyandex.com/pratt-oil/uploads/7.устьевой-инструмент.jpg",
        "ru": "Устьевой инструмент",
        "en": "Wellhead Tools",
        "ar": "أدوات رأس البئر",
        "category_en": "Wellhead Tools",
        "category_ar": "أدوات رأس البئر",
        "desc_en": "Wellhead tools for drilling, workover and field service operations, with quotation support by model, photo or drawing.",
        "desc_ar": "أدوات رأس البئر لعمليات الحفر وصيانة الآبار والخدمة الميدانية مع دعم التسعير حسب الموديل أو الصورة أو الرسم الفني.",
        "common_en": ["wellhead tools", "pipe handling tools", "slips", "elevators", "hydraulic tongs"],
        "common_ar": ["أدوات رأس البئر", "أدوات مناولة الأنابيب", "سلبسات", "مصاعد أنابيب", "ملاقط هيدروليكية"],
        "application_en": "Used around the wellhead for pipe handling, drilling support and workover service.",
        "application_ar": "تستخدم حول رأس البئر لمناولة الأنابيب ودعم الحفر وخدمة صيانة الآبار.",
    },
    {
        "slug": "drilling-rig-accessories-valves-pumps",
        "source": "https://ecdn.cnyandex.com/pratt-oil/uploads/8.Принадлежности-для-буровых-установок-клапаны-насосы.jpg",
        "ru": "Принадлежности для буровых установок (клапаны, насосы)",
        "en": "Drilling Rig Accessories, Valves and Pumps",
        "ar": "ملحقات الحفارات والصمامات والمضخات",
        "category_en": "Hydraulic Components and Maintenance Parts",
        "category_ar": "المكونات الهيدروليكية وقطع الصيانة",
        "desc_en": "Drilling rig accessories, valves, pumps and hydraulic components for oilfield equipment maintenance and replacement.",
        "desc_ar": "ملحقات حفارات النفط والصمامات والمضخات والمكونات الهيدروليكية لصيانة معدات حقول النفط والاستبدال.",
        "common_en": ["hydraulic pump", "oilfield valves", "rig accessories", "maintenance parts", "hydraulic components"],
        "common_ar": ["مضخة هيدروليكية", "صمامات حقول النفط", "ملحقات الحفار", "قطع صيانة", "مكونات هيدروليكية"],
        "application_en": "Used for drilling rig hydraulic systems, equipment repair and fast replacement procurement.",
        "application_ar": "تستخدم في أنظمة الهيدروليك للحفارات وإصلاح المعدات وشراء قطع الاستبدال السريع.",
    },
]


def escape(value: str) -> str:
    return html.escape(value, quote=True)


def download_and_convert_images() -> None:
    out_dir = ROOT / "assets" / "images" / "home-products"
    raw_dir = ROOT / "work" / "home-product-source"
    out_dir.mkdir(parents=True, exist_ok=True)
    raw_dir.mkdir(parents=True, exist_ok=True)
    for product in PRODUCTS:
        src = product["source"]
        quoted = urllib.parse.quote(src, safe=":/%?=&.")
        raw_path = raw_dir / f"{product['slug']}.jpg"
        webp_path = out_dir / f"{product['slug']}.webp"
        if not raw_path.exists():
            req = urllib.request.Request(quoted, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=30) as response:
                raw_path.write_bytes(response.read())
        with Image.open(raw_path) as im:
            im = im.convert("RGB")
            im = ImageOps.contain(im, (900, 650), method=Image.Resampling.LANCZOS)
            canvas = Image.new("RGB", (900, 650), "white")
            x = (900 - im.width) // 2
            y = (650 - im.height) // 2
            canvas.paste(im, (x, y))
            canvas.save(webp_path, "WEBP", quality=82, method=6)


def card_html(product: dict[str, object], lang: str, context: str) -> str:
    if lang == "en":
        title = product["en"]
        desc = product["desc_en"]
        category = product["category_en"]
        view = "View Details"
        quote = "Request Quote"
        whats = "WhatsApp"
        img_prefix = {
            "home": "assets/images/home-products/",
            "catalog": "../../assets/images/home-products/",
        }[context]
        href_prefix = {
            "home": "en/products/",
            "catalog": "",
        }[context]
    else:
        title = product["ar"]
        desc = product["desc_ar"]
        category = product["category_ar"]
        view = "عرض التفاصيل"
        quote = "طلب عرض سعر"
        whats = "واتساب"
        img_prefix = {
            "home": "../assets/images/home-products/",
            "catalog": "../../assets/images/home-products/",
        }[context]
        href_prefix = {
            "home": "products/",
            "catalog": "",
        }[context]
    slug = product["slug"]
    image = f"{img_prefix}{slug}.webp"
    href = f"{href_prefix}{slug}/"
    return f'''          <article class="product-card">
            <a class="card-detail-link" href="{href}">
              <div class="product-card-media has-image"><img class="product-card-image" src="{image}" alt="{escape(title)}" title="{escape(title)}" width="900" height="650" loading="lazy" decoding="async"></div>
              <h3>{escape(title)}</h3>
              <p>{escape(desc)}</p>
            </a>
            <div class="card-actions">
              <a class="mini-btn" href="{href}">{view}</a>
              <a class="mini-btn" href="#contact">{quote}</a>
              <a class="mini-btn dark" href="{WHATSAPP}%3A%20{urllib.parse.quote(str(title))}" rel="nofollow">{whats}</a>
            </div>
          </article>'''


def home_product_section(lang: str) -> str:
    if lang == "en":
        eyebrow = "Product categories"
        h2 = "Core oilfield spare parts categories"
        intro = "Featured oilfield equipment products from the Russian product layout, localized for Middle East buyers and linked to dedicated quotation pages."
        more = "View Product Page"
        more_href = "en/products/"
    else:
        eyebrow = "فئات المنتجات"
        h2 = "فئات قطع غيار معدات حقول النفط الأساسية"
        intro = "منتجات معدات حقول النفط المختارة من تخطيط الموقع الروسي، مع صفحات تفاصيل مخصصة للاستفسارات وطلبات الأسعار."
        more = "عرض صفحة المنتجات"
        more_href = "products/"
    cards = "\n".join(card_html(p, lang, "home") for p in PRODUCTS)
    return f'''<section class="section product-entry-section" id="products">
        <div class="section-heading">
          <p class="eyebrow">{escape(eyebrow)}</p>
          <h2>{escape(h2)}</h2>
          <p>{escape(intro)}</p>
        </div>
        <div class="product-grid">
{cards}
        </div>
        <div class="product-more-row">
          <a class="btn product-more-btn" href="{more_href}">{escape(more)}</a>
        </div>
      </section>
      '''


def replace_home_sections() -> None:
    replacements = {
        ROOT / "index.html": home_product_section("en"),
        ROOT / "ar" / "index.html": home_product_section("ar"),
    }
    for path, replacement in replacements.items():
        text = path.read_text(encoding="utf-8")
        start = text.index('<section class="section product-entry-section" id="products">')
        end = text.index('<section class="section company-presence-section"', start)
        path.write_text(text[:start] + replacement + text[end:], encoding="utf-8")


def catalog_feature_section(lang: str) -> str:
    if lang == "en":
        eyebrow = "Our products"
        h2 = "Featured Oilfield Equipment Products"
        intro = "Eight key product entrances aligned with the Russian homepage product layout. Click a card to view the product name, image, application and quotation support."
        id_value = "featured-products"
    else:
        eyebrow = "منتجاتنا"
        h2 = "منتجات معدات حقول النفط المختارة"
        intro = "ثمانية مداخل رئيسية للمنتجات متوافقة مع تخطيط صفحة المنتجات الروسية. اضغط على البطاقة لعرض الاسم والصورة والاستخدام ودعم التسعير."
        id_value = "featured-products"
    cards = "\n".join(card_html(p, lang, "catalog") for p in PRODUCTS)
    return f'''<section class="section product-entry-section featured-products-section" id="{id_value}">
        <div class="section-heading"><p class="eyebrow">{escape(eyebrow)}</p><h2>{escape(h2)}</h2><p>{escape(intro)}</p></div>
        <div class="product-grid">
{cards}
        </div>
      </section>
      '''


def replace_catalog_overview() -> None:
    for lang, rel_path in [("en", "en/products/index.html"), ("ar", "ar/products/index.html")]:
        path = ROOT / rel_path
        text = path.read_text(encoding="utf-8")
        start = text.index('<section class="section ru-category-overview" id="catalog">')
        end = text.index('<section class="section ru-catalog-sections">', start)
        text = text[:start] + catalog_feature_section(lang) + text[end:]
        text = text.replace('href="#catalog"', 'href="#featured-products"')
        path.write_text(text, encoding="utf-8")


def header(lang: str, slug: str, title: str, desc: str, image: str) -> str:
    is_ar = lang == "ar"
    lang_attr = 'lang="ar" dir="rtl"' if is_ar else 'lang="en"'
    locale = "ar_AR" if is_ar else "en_US"
    canonical = f"{SITE}/{lang}/products/{slug}/"
    stylesheet = "../../../styles.css?v=featured-products-20260616"
    ar_link = f"{SITE}/ar/products/{slug}/"
    en_link = f"{SITE}/en/products/{slug}/"
    ru_link = f"{SITE}/ru/products/"
    org = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "Organization",
                "@id": f"{SITE}/#organization",
                "name": "Jinan Prite Petroleum Equipment Co., Ltd.",
                "alternateName": "Pratt Oil",
                "url": f"{SITE}/",
            },
            {
                "@type": "Product",
                "name": title,
                "brand": {"@type": "Brand", "name": "Pratt Oil"},
                "image": f"{SITE}/assets/images/home-products/{image}",
                "description": desc,
            },
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{SITE}/"},
                    {"@type": "ListItem", "position": 2, "name": "Products", "item": f"{SITE}/{lang}/products/"},
                    {"@type": "ListItem", "position": 3, "name": title, "item": canonical},
                ],
            },
        ],
    }
    return f'''<!doctype html>
<html {lang_attr}>
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{escape(title)} | Pratt Oil</title>
    <meta name="description" content="{escape(desc)}">
    <meta name="robots" content="index, follow, max-image-preview:large">
    <link rel="canonical" href="{canonical}">
    <link rel="alternate" hreflang="en" href="{en_link}">
    <link rel="alternate" hreflang="ar" href="{ar_link}">
    <link rel="alternate" hreflang="ru" href="{ru_link}">
    <link rel="alternate" hreflang="x-default" href="{en_link}">
    <meta property="og:type" content="website">
    <meta property="og:title" content="{escape(title)} | Pratt Oil">
    <meta property="og:description" content="{escape(desc)}">
    <meta property="og:url" content="{canonical}">
    <meta property="og:site_name" content="Jinan Prite Petroleum Equipment Co., Ltd.">
    <meta property="og:locale" content="{locale}">
    <meta property="og:image" content="{SITE}/assets/images/home-products/{image}">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{escape(title)} | Pratt Oil">
    <meta name="twitter:description" content="{escape(desc)}">
    <meta name="twitter:image" content="{SITE}/assets/images/home-products/{image}">
    <link rel="stylesheet" href="{stylesheet}">
    <script type="application/ld+json">{json.dumps(org, ensure_ascii=False, separators=(',', ':'))}</script>
  </head>
'''


def nav(lang: str, slug: str) -> str:
    if lang == "en":
        labels = {
            "menu": "Menu",
            "home": "Home",
            "about": "About Us",
            "products": "Products",
            "news": "News",
            "services": "Services",
            "contact": "Contact",
            "language": "Language",
        }
        lang_opts = '<a class="language-option active" href="./">English</a><a class="language-option" href="../../../ar/products/{}/">Arabic</a><a class="language-option" href="../../../ru/products/">Russian</a>'.format(slug)
    else:
        labels = {
            "menu": "القائمة",
            "home": "الرئيسية",
            "about": "من نحن",
            "products": "المنتجات",
            "news": "الأخبار",
            "services": "الخدمات",
            "contact": "اتصل بنا",
            "language": "اللغة",
        }
        lang_opts = '<a class="language-option" href="../../../en/products/{}/">English</a><a class="language-option active" href="./">Arabic</a><a class="language-option" href="../../../ru/products/">Russian</a>'.format(slug)
    return f'''  <body class="ru-product-detail-page {'ar-product-detail-page' if lang == 'ar' else 'en-product-detail-page'}">
    <header class="site-header">
      <div class="topbar">
        <a href="{WHATSAPP}" rel="nofollow">WhatsApp: +86 159 0808 0040</a>
        <a href="mailto:2000@pratt-oil.com">2000@pratt-oil.com</a>
        <a href="tel:+8615908080040">Phone: +86 159 0808 0040</a>
      </div>
      <nav class="nav" aria-label="Primary navigation">
        <a class="brand" href="../../../" aria-label="Jinan Prite Petroleum Equipment">
          <img class="brand-logo" src="../../../assets/images/logo/logo-pratt-oil.webp" alt="Pratt Oil logo" title="Pratt Oil logo" width="300" height="150" loading="eager" decoding="async">
          <span><strong>PRATT OIL</strong><small>Jinan Prite Petroleum Equipment</small></span>
        </a>
        <button class="menu-toggle" type="button" aria-label="{labels['menu']}" aria-expanded="false">{labels['menu']}</button>
        <div class="nav-links" id="navLinks">
          <a class="nav-main-link" href="../../../">{labels['home']}</a>
          <a class="nav-main-link" href="../../../en/about-us/">{labels['about']}</a>
          <a class="nav-main-link" href="../">{labels['products']}</a>
          <a class="nav-main-link" href="../../../en/news/">{labels['news']}</a>
          <a class="nav-main-link" href="../../../en/services/">{labels['services']}</a>
          <a class="nav-main-link" href="../../../en/contact/">{labels['contact']}</a>
        </div>
        <div class="nav-actions">
          <div class="language-dropdown" data-nav-dropdown><button class="language-button" type="button" data-nav-toggle aria-label="{labels['language']}" aria-expanded="false">{labels['language']}</button><div class="dropdown-panel language-panel" data-nav-panel>{lang_opts}</div></div>
          <a class="nav-quick-link" href="{WHATSAPP}" rel="nofollow">WhatsApp</a>
        </div>
      </nav>
    </header>
'''


def detail_page(product: dict[str, object], lang: str) -> str:
    title = str(product["ar" if lang == "ar" else "en"])
    desc = str(product["desc_ar" if lang == "ar" else "desc_en"])
    category = str(product["category_ar" if lang == "ar" else "category_en"])
    common = product["common_ar" if lang == "ar" else "common_en"]
    application = str(product["application_ar" if lang == "ar" else "application_en"])
    slug = str(product["slug"])
    image = f"{slug}.webp"
    if lang == "en":
        bc_home, bc_products = "Home", "Products"
        common_h, app_h, quote_h, spec_h = "Common Part Names", "Application", "Request a Quotation", "Basic Supply Information"
        quote_text = "Send part number, pump model, rig model, product photo or technical drawing. We will check specification matching and reply with quotation details."
        whatsapp_text = "Request Quote on WhatsApp"
        email_text = "Send Email"
        table = [
            ("Product category", category),
            ("Quotation support", "Part number, model, product photo or drawing"),
            ("Supply support", "Specification matching and export packaging"),
            ("Communication", "English, Arabic and Russian"),
        ]
    else:
        bc_home, bc_products = "الرئيسية", "المنتجات"
        common_h, app_h, quote_h, spec_h = "أسماء القطع الشائعة", "الاستخدام", "طلب عرض سعر", "معلومات التوريد الأساسية"
        quote_text = "أرسل رقم القطعة أو موديل المضخة أو موديل الحفار أو صورة المنتج أو الرسم الفني. سنراجع مطابقة المواصفات ونرد بتفاصيل عرض السعر."
        whatsapp_text = "طلب عرض سعر عبر واتساب"
        email_text = "إرسال بريد إلكتروني"
        table = [
            ("فئة المنتج", category),
            ("دعم التسعير", "رقم القطعة أو الموديل أو صورة المنتج أو الرسم الفني"),
            ("دعم التوريد", "مطابقة المواصفات وتغليف التصدير"),
            ("التواصل", "الإنجليزية والعربية والروسية"),
        ]
    items = "".join(f"<li>{escape(str(item))}</li>" for item in common)
    rows = "".join(f"<tr><th>{escape(k)}</th><td>{escape(v)}</td></tr>" for k, v in table)
    return header(lang, slug, title, desc, image) + nav(lang, slug) + f'''    <main>
      <nav class="ru-breadcrumb" aria-label="Breadcrumb"><a href="../../../">{bc_home}</a><span>/</span><a href="../">{bc_products}</a><span>/</span><strong>{escape(title)}</strong></nav>
      <section class="section ru-product-detail-hero">
        <div class="ru-product-detail-copy">
          <p class="eyebrow">{escape(category)}</p>
          <h1>{escape(title)}</h1>
          <p>{escape(desc)}</p>
          <div class="ru-product-meta"><span>{escape(category)}</span><span>{escape(product['ru'])}</span><span>{escape(title)}</span></div>
          <div class="hero-actions"><a class="btn primary" href="{WHATSAPP}%3A%20{urllib.parse.quote(title)}" rel="nofollow">{whatsapp_text}</a><a class="btn secondary dark-text" href="mailto:2000@pratt-oil.com">{email_text}</a></div>
        </div>
        <div class="ru-product-detail-image"><img src="../../../assets/images/home-products/{image}" alt="{escape(title)}" title="{escape(title)}" width="900" height="650" loading="eager" decoding="async"></div>
      </section>
      <section class="section ru-product-info-grid">
        <article><h2>{common_h}</h2><ul>{items}</ul></article>
        <article><h2>{app_h}</h2><p>{escape(application)}</p></article>
        <article><h2>{quote_h}</h2><p>{escape(quote_text)}</p></article>
      </section>
      <section class="section ru-model-table-section">
        <div class="section-heading"><p class="eyebrow">{escape(category)}</p><h2>{spec_h}</h2></div>
        <div class="ru-table-scroll"><table class="ru-model-table"><tbody>{rows}</tbody></table></div>
      </section>
      <section class="section contact-section" id="contact">
        <div><p class="eyebrow">Inquiry</p><h2>{quote_h}</h2><p>{escape(quote_text)}</p></div>
        <div class="contact-grid"><a href="mailto:2000@pratt-oil.com"><span>Email</span><strong>2000@pratt-oil.com</strong></a><a href="mailto:2001@pratt-oil.com"><span>Email</span><strong>2001@pratt-oil.com</strong></a><a href="{WHATSAPP}" rel="nofollow"><span>WhatsApp</span><strong>+86 159 0808 0040</strong></a><a href="tel:+8618063410221"><span>Phone</span><strong>+86 180 6341 0221</strong></a></div>
        <address>Building 11, Zhigu Industrial Park, High-tech Zone, Jinan, Shandong Province, China</address>
      </section>
    </main>
    <footer class="footer">
      <div class="footer-brand"><img class="footer-logo" src="../../../assets/images/logo/logo-pratt-oil.webp" alt="Pratt Oil logo" title="Pratt Oil logo" width="300" height="150" loading="lazy" decoding="async"><div><strong>Jinan Prite Petroleum Equipment Co., Ltd.</strong><p>Professional supplier of oil drilling equipment and spare parts for international oil and gas markets.</p></div></div>
      <div class="footer-links"><a href="../">Products</a><a href="#contact">Contact</a><a href="{WHATSAPP}" rel="nofollow">WhatsApp</a></div>
      <div class="footer-social" aria-label="Social media channels"><span>Facebook</span><span>Instagram</span><span>YouTube</span></div>
    </footer>
    <a class="floating-whatsapp" href="{WHATSAPP}" rel="nofollow" aria-label="WhatsApp inquiry">WhatsApp</a>
    <script src="../../../script.js"></script>
  </body>
</html>
'''


def write_detail_pages() -> None:
    for product in PRODUCTS:
        for lang in ["en", "ar"]:
            out_dir = ROOT / lang / "products" / str(product["slug"])
            out_dir.mkdir(parents=True, exist_ok=True)
            (out_dir / "index.html").write_text(detail_page(product, lang), encoding="utf-8")


def update_sitemap() -> None:
    path = ROOT / "sitemap.xml"
    text = path.read_text(encoding="utf-8")
    urls = []
    for product in PRODUCTS:
        slug = product["slug"]
        urls.append(f"{SITE}/en/products/{slug}/")
        urls.append(f"{SITE}/ar/products/{slug}/")
    insert = []
    for url in urls:
        if f"<loc>{url}</loc>" not in text:
            insert.append(f"  <url><loc>{url}</loc></url>")
    if insert:
        text = text.replace("</urlset>", "\n" + "\n".join(insert) + "\n</urlset>")
        path.write_text(text, encoding="utf-8")


def main() -> None:
    download_and_convert_images()
    replace_home_sections()
    replace_catalog_overview()
    write_detail_pages()
    update_sitemap()
    print("updated featured products for English and Arabic only")


if __name__ == "__main__":
    main()

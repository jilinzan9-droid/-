from __future__ import annotations

import html
import json
import re
from pathlib import Path
from urllib.parse import quote


ROOT = Path(__file__).resolve().parents[1]
BASE = "https://www.pratt-oil.com"
PHONE = "8615908080040"
EMAIL = "2000@pratt-oil.com"
TODAY = "2026-06-17"

CONTACTS = {
    "email_primary": "2000@pratt-oil.com",
    "email_secondary": "2001@pratt-oil.com",
    "whatsapp_primary": "+86 159 0808 0040",
    "whatsapp_secondary": "+86 132 2534 0118",
    "phone": "+86 159 0808 0040 / +86 180 6341 0221",
    "wechat": "15908080040",
    "address": "Building 11, Zhigu Industrial Park, High-tech Zone, Jinan, Shandong Province, China",
}

RELATED_PRODUCTS = [
    ("Mud Pump Spare Parts", "/en/mud-pump-spare-parts/", "Fluid end expendables, liners, pistons, valves, seats, seals and modules for F-series and compatible mud pumps."),
    ("Mud Pump Liners, Pistons, Valves & Seats", "/en/mud-pump-liners-pistons-valves-seats/", "High-wear mud pump consumables for daily rig maintenance and fast replacement."),
    ("Drilling Rig Spare Parts", "/en/drilling-rig-spare-parts/", "Replacement parts for drilling rigs, workover rigs, hoisting systems and field maintenance."),
    ("Drawworks Brake System Parts", "/en/drawworks-brake-system-parts/", "Brake bands, brake blocks, auxiliary brake parts and hydraulic disc brake support."),
    ("Wellhead Equipment & Oilfield Valves", "/en/wellhead-equipment-valves/", "Wellhead tools, oilfield valves and pressure-control components for drilling and production."),
    ("Hydraulic Components & Maintenance Parts", "/en/oilfield-hydraulic-components/", "Hydraulic valves, cylinders, hoses, fittings, seals and maintenance parts."),
    ("Fast-Wearing Oilfield Parts & Consumables", "/en/fast-wearing-oilfield-parts/", "Seals, gaskets, brake parts, valves, seats and routine drilling consumables."),
]

NEWS = [
    {
        "slug": "how-to-select-mud-pump-spare-parts-by-part-number",
        "category": "Industry News",
        "title": "How to Select Mud Pump Spare Parts by Part Number",
        "meta_title": "How to Select Mud Pump Spare Parts by Part Number | Pratt Oil",
        "description": "Procurement guide for selecting mud pump spare parts by part number, pump model, product photo or technical drawing for Middle East drilling maintenance.",
        "image": "/assets/images/products/mud-pump-spare-parts.webp",
        "image_alt": "Mud pump spare parts selection by part number for drilling maintenance",
        "sections": [
            ("Why part numbers matter", "Mud pump spare parts may look similar while using different dimensions, materials or connection details. A clear part number helps suppliers check compatibility before quotation."),
            ("Information to send", "For a faster quotation, send the part number, pump model, quantity, application, product photo and technical drawing when available. These details help reduce mismatch risk."),
            ("Common mud pump items", "Common inquiry items include liners, pistons, valves, seats, modules, seals, gaskets, rods, clamps and fluid end expendables."),
            ("Quotation workflow", "The buyer shares the available information, the supplier checks the category and compatibility, then confirms price, packing details and delivery discussion by WhatsApp or email."),
        ],
    },
    {
        "slug": "mud-pump-liners-pistons-valves-seats-guide",
        "category": "Industry News",
        "title": "Mud Pump Liners, Pistons, Valves and Seats Guide",
        "meta_title": "Mud Pump Liners, Pistons, Valves and Seats Guide | Pratt Oil",
        "description": "Guide for mud pump liners, pistons, valves and seats used in drilling mud pump maintenance and daily replacement planning.",
        "image": "/assets/images/products/mud-pump-liners-pistons-valves-seats.webp",
        "image_alt": "Mud pump liners pistons valves and seats procurement guide",
        "sections": [
            ("Fast-wearing consumables", "Liners, pistons, valves and seats are high-wear mud pump consumables. They are often purchased for routine maintenance and emergency replacement."),
            ("Compatibility checks", "Buyers should confirm pump model, liner size, piston type, valve type, seat size, rubber material and expected drilling fluid conditions."),
            ("Packing and identification", "Clear labeling, export packing and part number reference can help warehouse teams and rig crews identify spare parts before use."),
            ("Inquiry checklist", "Send quantity, destination, pump model, part number and product photos. If the old part is available, photos from multiple angles are helpful."),
        ],
    },
    {
        "slug": "drawworks-brake-system-parts-rig-maintenance",
        "category": "Industry News",
        "title": "Drawworks Brake System Parts for Rig Maintenance",
        "meta_title": "Drawworks Brake System Parts for Rig Maintenance | Pratt Oil",
        "description": "Procurement guide for drawworks brake system parts, brake bands, brake blocks and auxiliary brake maintenance components.",
        "image": "/assets/images/products/drawworks-brake-system-parts.webp",
        "image_alt": "Drawworks brake system parts for rig maintenance",
        "sections": [
            ("Brake system maintenance", "Drawworks brake system parts are selected by rig model, brake type, installation dimensions and operating condition. Matching the wrong brake component can delay maintenance."),
            ("Common requested parts", "Common inquiry parts include brake bands, brake blocks, auxiliary brake parts, hydraulic disc brake components, friction plates and seals."),
            ("Technical information", "Useful information includes rig model, drawworks model, old part number, product photo, drawing and the operating environment."),
            ("Quotation support", "A clear inquiry helps confirm whether the part is for replacement, overhaul or modernization support before quotation."),
        ],
    },
    {
        "slug": "fast-wearing-oilfield-parts-desert-drilling",
        "category": "Industry News",
        "title": "Fast-Wearing Oilfield Parts for Desert Drilling Operations",
        "meta_title": "Fast-Wearing Oilfield Parts for Desert Drilling Operations | Pratt Oil",
        "description": "Guide to fast-wearing oilfield parts and drilling consumables for desert drilling operation maintenance and replacement planning.",
        "image": "/assets/images/hero/hero-desert-drilling-operation-middle-east.webp",
        "image_alt": "Fast-wearing oilfield parts for desert drilling operations",
        "sections": [
            ("Desert drilling maintenance", "Desert drilling operations require practical spare parts planning because consumables and maintenance parts may need replacement during active field work."),
            ("Parts often prepared", "Common parts include mud pump consumables, seals, gaskets, valves, seats, brake parts, hydraulic seals, hoses and pressure gauges."),
            ("How to reduce mismatch", "Buyers can send the part number, pump model, rig model, product photo or technical drawing before confirming the quotation."),
            ("Procurement planning", "For regular maintenance, buyers may group fast-wearing items by equipment type and keep clear part number records for future inquiries."),
        ],
    },
    {
        "slug": "middle-east-oilfield-spare-parts-inquiry-support",
        "category": "Company News",
        "title": "Middle East Oilfield Spare Parts Inquiry Support",
        "meta_title": "Middle East Oilfield Spare Parts Inquiry Support | Pratt Oil",
        "description": "Inquiry support workflow for Middle East buyers sending part number, pump model, rig model, product photo or technical drawing for quotation.",
        "image": "/assets/images/company/jinan-pratt-office-oilfield-spare-parts-quotation-support.webp",
        "image_alt": "Office team supporting oilfield spare parts inquiry and quotation",
        "sections": [
            ("Inquiry support scope", "Jinan Prite Petroleum Equipment supports inquiry communication for mud pump spare parts, drilling rig spare parts, wellhead tools, oilfield valves and hydraulic components."),
            ("Information buyers can send", "Buyers can send part number, pump model, rig model, quantity, product photo, drawing and destination for quotation checking."),
            ("Communication channels", "WhatsApp and email are used for product matching, specification confirmation, quotation discussion and follow-up communication."),
            ("No unsupported claims", "This service note describes inquiry workflow only. It does not claim specific customer projects, certifications, exhibition attendance or guaranteed stock."),
        ],
    },
    {
        "slug": "oilfield-spare-parts-export-packaging-quotation-support",
        "category": "Company News",
        "title": "Export Packaging and Quotation Support for Oilfield Spare Parts",
        "meta_title": "Export Packaging and Quotation Support for Oilfield Spare Parts | Pratt Oil",
        "description": "B2B quotation and export packaging support notes for oilfield spare parts buyers sending models, drawings, photos and destination information.",
        "image": "/assets/images/company/jinan-prite-petroleum-company-entrance.webp",
        "image_alt": "Jinan Prite Petroleum Equipment export support for oilfield spare parts",
        "sections": [
            ("Quotation preparation", "A quotation usually depends on confirmed product name, part number, model, quantity, destination and available technical information."),
            ("Export packing discussion", "Packing can be discussed according to part size, weight, sensitivity, transport route and buyer documentation requirements."),
            ("Specification confirmation", "For oilfield spare parts, specification matching is more important than relying on appearance alone. Photos and drawings help avoid wrong replacement."),
            ("Commercial confirmation", "Final price, delivery time, packing and specifications are based on written confirmation, email communication or formal quotation documents."),
        ],
    },
]

REQUESTED_NEWS_SLUGS = {item["slug"] for item in NEWS}
NEWS_BY_CATEGORY = {
    "Industry News": [item for item in NEWS if item["category"] == "Industry News"],
    "Company News": [item for item in NEWS if item["category"] == "Company News"],
}


def rel_prefix(path: Path) -> str:
    parent = path.parent.relative_to(ROOT)
    if str(parent) == ".":
        return ""
    return "../" * len(parent.parts)


def page_url(path: Path) -> str:
    rel = path.relative_to(ROOT).as_posix()
    if rel == "index.html":
        return f"{BASE}/"
    if rel == "404.html":
        return f"{BASE}/404.html"
    if rel.endswith("/index.html"):
        return f"{BASE}/{rel[:-10].rstrip('/')}/"
    return f"{BASE}/{rel}"


def wa_link(title: str, url: str) -> str:
    message = (
        f"Hello, I want to request a quote for {title}. Page: {url}. "
        "I can send part number, pump model, rig model, product photo or technical drawing."
    )
    return f"https://wa.me/{PHONE}?text={quote(message)}"


def email_link(title: str, url: str) -> str:
    subject = f"Oilfield Spare Parts Inquiry - {title}"
    body = (
        f"Hello Pratt Oil,\r\n\r\nI want to request a quote for {title}.\r\n"
        f"Page: {url}\r\n\r\nI can send part number, pump model, rig model, product photo or technical drawing."
    )
    return f"mailto:{EMAIL}?subject={quote(subject)}&body={quote(body)}"


def root_relative(path: str, prefix: str) -> str:
    return prefix + path.lstrip("/")


def schema_json(obj: dict) -> str:
    return json.dumps(obj, ensure_ascii=False, separators=(",", ":"))


def organization_schema() -> dict:
    return {
        "@type": "Organization",
        "@id": f"{BASE}/#organization",
        "name": "Jinan Prite Petroleum Equipment Co., Ltd.",
        "alternateName": "Pratt Oil",
        "url": f"{BASE}/",
        "email": [CONTACTS["email_primary"], CONTACTS["email_secondary"]],
        "telephone": ["+86-15908080040", "+86-18063410221"],
        "address": {
            "@type": "PostalAddress",
            "streetAddress": "Building 11, Zhigu Industrial Park, High-tech Zone",
            "addressLocality": "Jinan",
            "addressRegion": "Shandong",
            "addressCountry": "CN",
        },
        "areaServed": ["UAE", "Saudi Arabia", "Iraq", "Qatar", "Oman", "Kuwait", "Bahrain"],
    }


def header(prefix: str, title: str, description: str, canonical: str, og_type: str = "website", schema: dict | None = None) -> str:
    graph = [organization_schema()]
    if schema:
        graph.extend(schema.get("@graph", []))
    ld = {"@context": "https://schema.org", "@graph": graph}
    return f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{html.escape(title)}</title>
    <meta name="description" content="{html.escape(description)}">
    <meta name="robots" content="index, follow, max-image-preview:large">
    <link rel="canonical" href="{canonical}">
    <link rel="alternate" hreflang="en" href="{canonical}">
    <link rel="alternate" hreflang="x-default" href="{canonical}">
    <meta property="og:type" content="{og_type}">
    <meta property="og:title" content="{html.escape(title)}">
    <meta property="og:description" content="{html.escape(description)}">
    <meta property="og:url" content="{canonical}">
    <meta property="og:site_name" content="Jinan Prite Petroleum Equipment Co., Ltd.">
    <meta property="og:locale" content="en_US">
    <meta property="og:image" content="{BASE}/assets/images/hero/hero-oilfield-equipment-spare-parts-middle-east.webp">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{html.escape(title)}">
    <meta name="twitter:description" content="{html.escape(description)}">
    <meta name="twitter:image" content="{BASE}/assets/images/hero/hero-oilfield-equipment-spare-parts-middle-east.webp">
    <link rel="stylesheet" href="{prefix}styles.css">
    <script type="application/ld+json">{schema_json(ld)}</script>
  </head>
  <body>
    <header class="site-header">
      <div class="topbar">
        <a href="{wa_link(title, canonical)}" rel="nofollow">WhatsApp: +86 159 0808 0040</a>
        <a href="mailto:2000@pratt-oil.com">2000@pratt-oil.com</a>
        <a href="tel:+8615908080040">Phone: +86 159 0808 0040</a>
      </div>
      <nav class="nav" aria-label="Primary navigation">
        <a class="brand" href="{prefix}index.html" aria-label="Jinan Prite Petroleum Equipment">
          <img class="brand-logo" src="{prefix}assets/images/logo/logo-pratt-oil.webp" alt="Pratt Oil logo" title="Pratt Oil logo" width="300" height="150" loading="eager" decoding="async">
          <span><strong>PRATT OIL</strong><small>Jinan Prite Petroleum Equipment</small></span>
        </a>
        <button class="menu-toggle" type="button" aria-label="Open navigation" aria-expanded="false">Menu</button>
        <div class="nav-links" id="navLinks">
          <a class="nav-main-link" href="{prefix}index.html">Home</a>
          <a class="nav-main-link" href="{prefix}en/about-us/">About Us</a>
          <a class="nav-main-link" href="{prefix}index.html#products">Products</a>
          <a class="nav-main-link" href="{prefix}en/news/">News</a>
          <a class="nav-main-link" href="{prefix}en/services/">Services</a>
          <a class="nav-main-link" href="{prefix}en/contact/">Contact</a>
        </div>
        <div class="nav-actions">
          <div class="language-dropdown" data-nav-dropdown>
            <button class="language-button" type="button" data-nav-toggle aria-label="Open language menu" aria-expanded="false">Language</button>
            <div class="dropdown-panel language-panel" data-nav-panel><a class="language-option active" href="https://www.pratt-oil.com/">English</a><a class="language-option" href="https://www.pratt-oil.com/ar/">Arabic</a><a class="language-option" href="https://www.pratt-oil.ru/">Russian</a></div>
          </div>
          <a class="nav-quick-link" href="{wa_link(title, canonical)}" rel="nofollow">WhatsApp</a>
        </div>
      </nav>
    </header>
"""


def footer(prefix: str, title: str, url: str) -> str:
    return f"""    <footer class="footer">
      <div class="footer-brand"><img class="footer-logo" src="{prefix}assets/images/logo/logo-pratt-oil.webp" alt="Pratt Oil logo" title="Pratt Oil logo" width="300" height="150" loading="lazy" decoding="async"><div><strong>Jinan Prite Petroleum Equipment Co., Ltd.</strong><p>Professional supplier of oil drilling equipment and spare parts for international oil and gas markets.</p></div></div>
      <div class="footer-links">
        <a href="{prefix}index.html#products">Products</a>
        <a href="{prefix}index.html#company-presence">Capability</a>
        <a href="{prefix}index.html#contact">Contact</a>
        <a href="{prefix}en/privacy-policy/">Privacy Policy</a>
        <a href="{prefix}en/terms-and-conditions/">Terms &amp; Conditions</a>
      </div>
    </footer>
    <a class="floating-whatsapp" href="{wa_link(title, url)}" rel="nofollow" aria-label="WhatsApp inquiry">WhatsApp</a>
    <script src="{prefix}script.js"></script>
  </body>
</html>
"""


def breadcrumb_schema(items: list[tuple[str, str]]) -> dict:
    return {
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": index + 1, "name": name, "item": url}
            for index, (name, url) in enumerate(items)
        ],
    }


def related_products_html(prefix: str) -> str:
    links = []
    for name, url, desc in RELATED_PRODUCTS:
        links.append(
            f'<a href="{root_relative(url, prefix)}"><strong>{html.escape(name)}</strong><span>{html.escape(desc)}</span></a>'
        )
    return "".join(links)


def news_card(item: dict, prefix: str) -> str:
    href = root_relative(f"/en/news/{item['slug']}/", prefix)
    img = root_relative(item["image"], prefix)
    return f"""<article class="news-card">
              <a class="news-card-link" href="{href}">
                <div class="news-card-media"><img src="{img}" alt="{html.escape(item['image_alt'])}" title="{html.escape(item['title'])}" width="1200" height="675" loading="lazy" decoding="async"></div>
                <span class="news-badge">{html.escape(item['category'])}</span>
                <h3>{html.escape(item['title'])}</h3>
                <p>{html.escape(item['description'])}</p>
                <span class="read-more">Read More</span>
              </a>
            </article>"""


def article_page(item: dict) -> str:
    path = ROOT / "en" / "news" / item["slug"] / "index.html"
    prefix = rel_prefix(path)
    url = f"{BASE}/en/news/{item['slug']}/"
    breadcrumb = [
        ("Home", f"{BASE}/"),
        ("News", f"{BASE}/en/news/"),
        (item["category"], f"{BASE}/en/news/{'industry-news' if item['category'] == 'Industry News' else 'company-news'}/"),
        (item["title"], url),
    ]
    schema = {
        "@graph": [
            breadcrumb_schema(breadcrumb),
            {
                "@type": "BlogPosting",
                "@id": f"{url}#article",
                "mainEntityOfPage": {"@type": "WebPage", "@id": url},
                "headline": item["title"],
                "description": item["description"],
                "datePublished": TODAY,
                "dateModified": TODAY,
                "articleSection": item["category"],
                "inLanguage": "en",
                "author": {"@id": f"{BASE}/#organization"},
                "publisher": {"@id": f"{BASE}/#organization"},
                "about": ["oilfield spare parts", "mud pump spare parts", "drilling consumables", "Middle East procurement"],
            },
        ]
    }
    sections = "\n".join(
        f'          <section class="article-section"><h2>{html.escape(h2)}</h2><p>{html.escape(text)}</p></section>'
        for h2, text in item["sections"]
    )
    breadcrumb_html = '<span>/</span>'.join(
        f'<a href="{url}">{html.escape(name)}</a>' if idx < len(breadcrumb) - 1 else f'<span>{html.escape(name)}</span>'
        for idx, (name, url) in enumerate(breadcrumb)
    )
    return f"""{header(prefix, item["meta_title"], item["description"], url, "article", schema)}    <main>
      <section class="page-hero">
        <nav class="breadcrumb">{breadcrumb_html}</nav>
        <p class="eyebrow">{html.escape(item["category"])}</p>
        <h1>{html.escape(item["title"])}</h1>
        <p>{html.escape(item["description"])}</p>
        <div class="hero-actions">
          <a class="btn primary" href="{wa_link(item['title'], url)}" rel="nofollow">WhatsApp Inquiry</a>
          <a class="btn secondary dark-text" href="{email_link(item['title'], url)}">Email Inquiry</a>
        </div>
      </section>
      <section class="section article-layout">
        <div class="news-detail-media"><img src="{root_relative(item['image'], prefix)}" alt="{html.escape(item['image_alt'])}" title="{html.escape(item['title'])}" width="1200" height="675" loading="lazy" decoding="async"></div>
        <article class="article-content">
          <p class="article-lead">{html.escape(item["description"])}</p>
{sections}
          <section class="article-section inquiry-cta-panel">
            <h2>Request quotation support</h2>
            <p>Send part number, pump model, rig model, product photo or technical drawing. Include quantity and destination when available so the quotation discussion can be checked more efficiently.</p>
            <div class="hero-actions">
              <a class="btn primary" href="{wa_link(item['title'], url)}" rel="nofollow">Request Quote on WhatsApp</a>
              <a class="btn secondary dark-text" href="{email_link(item['title'], url)}">Email Inquiry</a>
            </div>
          </section>
        </article>
      </section>
      <section class="section compact-section" id="related-products">
        <div class="section-heading"><p class="eyebrow">Related Products</p><h2>Oilfield spare parts pages</h2></div>
        <div class="page-link-grid">{related_products_html(prefix)}</div>
      </section>
    </main>
{footer(prefix, item['title'], url)}"""


def news_index_page(kind: str | None = None) -> str:
    if kind == "Industry News":
        title = "Industry News for Oilfield Spare Parts Buyers"
        meta = "Industry News | Oilfield Spare Parts Procurement Guides"
        description = "Procurement guide articles for mud pump spare parts, liners, pistons, valves, seats, drawworks brake parts and drilling consumables."
        items = NEWS_BY_CATEGORY["Industry News"]
        url_path = "/en/news/industry-news/"
        eyebrow = "Industry News"
    elif kind == "Company News":
        title = "Company News and Inquiry Support"
        meta = "Company News | Oilfield Spare Parts Inquiry Support"
        description = "Company service updates for oilfield spare parts inquiry support, quotation communication and export packaging discussion."
        items = NEWS_BY_CATEGORY["Company News"]
        url_path = "/en/news/company-news/"
        eyebrow = "Company News"
    else:
        title = "Oilfield Spare Parts News and Procurement Guides"
        meta = "Oilfield Spare Parts News and Procurement Guides | Pratt Oil"
        description = "Procurement guide articles and company inquiry support notes for Middle East oilfield spare parts buyers."
        items = NEWS
        url_path = "/en/news/"
        eyebrow = "News Events"

    path = ROOT / url_path.strip("/") / "index.html"
    prefix = rel_prefix(path)
    url = f"{BASE}{url_path}"
    schema = {
        "@graph": [
            breadcrumb_schema([("Home", f"{BASE}/"), ("News", f"{BASE}/en/news/"), (title, url)]),
            {
                "@type": "CollectionPage",
                "@id": f"{url}#webpage",
                "url": url,
                "name": title,
                "description": description,
                "inLanguage": "en",
            },
        ]
    }
    cards = "\n            ".join(news_card(item, prefix) for item in items)
    return f"""{header(prefix, meta, description, url, "website", schema)}    <main>
      <section class="page-hero">
        <nav class="breadcrumb"><a href="{BASE}/">Home</a><span>/</span><a href="{BASE}/en/news/">News</a><span>/</span><span>{html.escape(title)}</span></nav>
        <p class="eyebrow">{html.escape(eyebrow)}</p>
        <h1>{html.escape(title)}</h1>
        <p>{html.escape(description)}</p>
        <div class="hero-actions">
          <a class="btn primary" href="{wa_link(title, url)}" rel="nofollow">WhatsApp Inquiry</a>
          <a class="btn secondary dark-text" href="{email_link(title, url)}">Email Inquiry</a>
        </div>
      </section>
      <section class="section news-list-section" id="news-list">
        <div class="section-heading">
          <p class="eyebrow">Procurement guides</p>
          <h2>{html.escape(title)}</h2>
          <p>Guidance is written for B2B procurement, model matching, part number confirmation and quotation communication. It does not describe unverified customer projects or market events.</p>
        </div>
        <div class="news-grid">{cards}</div>
      </section>
      <section class="section compact-section">
        <div class="section-heading"><p class="eyebrow">Related Products</p><h2>Product pages for quotation</h2></div>
        <div class="page-link-grid">{related_products_html(prefix)}</div>
      </section>
    </main>
{footer(prefix, title, url)}"""


def obsolete_news_page(path: Path) -> str:
    prefix = rel_prefix(path)
    url = page_url(path)
    title = "Oilfield Spare Parts Procurement Guide"
    description = "This archived news URL now points buyers to procurement guide content for oilfield spare parts quotation and model matching."
    return f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{title} | Pratt Oil</title>
    <meta name="description" content="{description}">
    <meta name="robots" content="noindex, follow">
    <link rel="canonical" href="{BASE}/en/news/">
    <meta http-equiv="refresh" content="0; url={prefix}en/news/">
    <link rel="stylesheet" href="{prefix}styles.css">
  </head>
  <body>
    <main>
      <section class="page-hero">
        <p class="eyebrow">Procurement guides</p>
        <h1>{title}</h1>
        <p>{description}</p>
        <div class="hero-actions">
          <a class="btn primary" href="{wa_link(title, url)}" rel="nofollow">WhatsApp Inquiry</a>
          <a class="btn secondary dark-text" href="{prefix}en/news/">View News Guides</a>
        </div>
      </section>
    </main>
  </body>
</html>
"""


def homepage_news_section(prefix: str, lang: str) -> str:
    if lang == "ar":
        heading = "أخبار قطع غيار حقول النفط وأدلة الشراء"
        desc = "محتوى إرشادي للمشترين حول اختيار قطع الغيار، مطابقة أرقام القطع، إرسال الصور والرسومات الفنية وطلب عروض الأسعار."
        industry_label = "أخبار الصناعة"
        company_label = "أخبار الشركة"
        eyebrow = "أخبار وأدلة"
        read_more = "اقرأ المزيد"
        all_news = "عرض كل الأخبار"
        industry_cards = [
            ("كيفية اختيار قطع غيار مضخات الطين حسب رقم القطعة", "دليل عملي لإرسال رقم القطعة، موديل المضخة، الصورة أو الرسم الفني قبل طلب السعر.", NEWS[0]),
            ("دليل بطانات ومكابس وصمامات ومقاعد مضخات الطين", "إرشادات لقطع مضخات الطين سريعة التآكل المستخدمة في الصيانة اليومية.", NEWS[1]),
            ("قطع نظام فرامل الونش لصيانة الحفارات", "ملاحظات شراء لأشرطة الفرامل وبلوكات الفرامل وقطع أنظمة الفرامل.", NEWS[2]),
            ("قطع حقول النفط سريعة التآكل لعمليات الحفر الصحراوية", "دليل لتجهيز قطع الاستهلاك والصيانة المستخدمة في مواقع الحفر الصحراوية.", NEWS[3]),
        ]
        company_cards = [
            ("دعم استفسارات قطع غيار حقول النفط في الشرق الأوسط", "طريقة إرسال رقم القطعة وموديل المضخة أو الحفارة والصور للحصول على عرض سعر.", NEWS[4]),
            ("دعم التغليف والتسعير لقطع غيار حقول النفط", "ملاحظات حول بيانات الطلب والتغليف ومطابقة المواصفات قبل التأكيد التجاري.", NEWS[5]),
        ]
    else:
        heading = "Oilfield Spare Parts News & Industry Updates"
        desc = "Procurement guide content for mud pump parts, drilling rig spares, drawworks brake systems, wellhead equipment and Middle East drilling maintenance buyers."
        industry_label = "Industry News"
        company_label = "Company News"
        eyebrow = "News events"
        read_more = "Read More"
        all_news = "View all news"
        industry_cards = [
            (NEWS[0]["title"], NEWS[0]["description"], NEWS[0]),
            (NEWS[1]["title"], NEWS[1]["description"], NEWS[1]),
            (NEWS[2]["title"], NEWS[2]["description"], NEWS[2]),
            (NEWS[3]["title"], NEWS[3]["description"], NEWS[3]),
        ]
        company_cards = [
            (NEWS[4]["title"], NEWS[4]["description"], NEWS[4]),
            (NEWS[5]["title"], NEWS[5]["description"], NEWS[5]),
        ]

    def cards(items: list[tuple[str, str, dict]], badge: str) -> str:
        return "\n".join(
            f"""            <article class="news-card">
              <a class="news-card-link" href="{root_relative('/en/news/' + item['slug'] + '/', prefix)}">
                <div class="news-card-media"><img src="{root_relative(item['image'], prefix)}" alt="{html.escape(item['image_alt'])}" title="{html.escape(title)}" width="1200" height="675" loading="lazy" decoding="async"></div>
                <span class="news-badge">{html.escape(badge)}</span>
                <h3>{html.escape(title)}</h3>
                <p>{html.escape(description)}</p>
                <span class="read-more">{html.escape(read_more)}</span>
              </a>
            </article>"""
            for title, description, item in items
        )

    return f"""      <section class="section news-events-section" id="news-events" data-news-tabs>
        <div class="section-heading">
          <p class="eyebrow">{html.escape(eyebrow)}</p>
          <h2>{html.escape(heading)}</h2>
          <p>{html.escape(desc)}</p>
        </div>
        <div class="news-tabs" role="tablist" aria-label="{html.escape(heading)}">
          <button class="news-tab is-active" type="button" data-news-tab="industry" role="tab" aria-selected="true">{html.escape(industry_label)}</button>
          <button class="news-tab" type="button" data-news-tab="company" role="tab" aria-selected="false">{html.escape(company_label)}</button>
        </div>
        <div class="news-tab-panel is-active" data-news-panel="industry" role="tabpanel">
          <div class="news-grid">
{cards(industry_cards, industry_label)}
          </div>
        </div>
        <div class="news-tab-panel" data-news-panel="company" role="tabpanel">
          <div class="news-grid">
{cards(company_cards, company_label)}
          </div>
        </div>
        <div class="news-more-row"><a class="btn secondary dark-text" href="{root_relative('/en/news/', prefix)}">{html.escape(all_news)}</a></div>
      </section>"""


def legal_page(kind: str) -> str:
    if kind == "privacy":
        title = "Privacy Policy"
        meta = "Privacy Policy | Pratt Oil"
        description = "Privacy policy for B2B oilfield spare parts inquiries, quotation communication, WhatsApp, email and technical drawing submissions."
        url_path = "/en/privacy-policy/"
        panels = [
            ("Information we may collect", "When buyers contact us, we may receive name, company, email, WhatsApp number, phone number, inquiry content, product photos, part numbers, pump models, rig models, technical drawings and attachment information."),
            ("How information is used", "Inquiry information is used for quotation, specification matching, technical communication, export packing discussion and follow-up service communication."),
            ("Data sharing", "We do not sell customer inquiry data. Information may be used internally to check product compatibility and prepare quotation communication."),
            ("Contact", "For privacy questions or data requests, contact 2000@pratt-oil.com."),
        ]
    else:
        title = "Terms & Conditions"
        meta = "Terms & Conditions | Pratt Oil"
        description = "Terms for B2B oilfield spare parts website information, quotation communication, product specifications, delivery time and final commercial confirmation."
        url_path = "/en/terms-and-conditions/"
        panels = [
            ("Website information", "Website product information, images, model references and descriptions are provided for general inquiry and specification matching only."),
            ("Quotation confirmation", "Final price, lead time, packing method, product specification and delivery details are based on final email communication or formal quotation documents."),
            ("No unsupported commitments", "The website does not make unsupported promises about stock, certification, delivery time or manufacturer status. Buyers should confirm requirements before ordering."),
            ("Product matching", "Buyers should provide part number, pump model, rig model, product photo or technical drawing so specifications can be checked before quotation."),
        ]
    path = ROOT / url_path.strip("/") / "index.html"
    prefix = rel_prefix(path)
    url = f"{BASE}{url_path}"
    schema = {"@graph": [breadcrumb_schema([("Home", f"{BASE}/"), (title, url)])]}
    panel_html = "".join(f'<div class="info-panel"><h3>{html.escape(h)}</h3><p>{html.escape(p)}</p></div>' for h, p in panels)
    return f"""{header(prefix, meta, description, url, "website", schema)}    <main>
      <section class="page-hero">
        <nav class="breadcrumb"><a href="{BASE}/">Home</a><span>/</span><span>{html.escape(title)}</span></nav>
        <p class="eyebrow">Legal</p>
        <h1>{html.escape(title)}</h1>
        <p>{html.escape(description)}</p>
      </section>
      <section class="section detail-grid">
        {panel_html}
      </section>
      <section class="section compact-section">
        <div class="section-heading"><p class="eyebrow">Inquiry support</p><h2>Contact Pratt Oil</h2><p>For product or policy questions, contact us by WhatsApp or email.</p></div>
        <div class="hero-actions">
          <a class="btn primary" href="{wa_link(title, url)}" rel="nofollow">WhatsApp Inquiry</a>
          <a class="btn secondary dark-text" href="{email_link(title, url)}">Email Inquiry</a>
        </div>
      </section>
    </main>
{footer(prefix, title, url)}"""


def not_found_page() -> str:
    path = ROOT / "404.html"
    prefix = rel_prefix(path)
    title = "Page Not Found"
    url = f"{BASE}/404.html"
    description = "The requested page could not be found. Use product category links or WhatsApp inquiry to request oilfield spare parts support."
    product_links = related_products_html(prefix)
    return f"""{header(prefix, "404 Page Not Found | Pratt Oil", description, url, "website", {"@graph": []})}    <main>
      <section class="page-hero not-found-hero">
        <p class="eyebrow">404</p>
        <h1>Page Not Found</h1>
        <p>The page may have moved or the link may be incorrect. You can return to the homepage, browse product categories or send a WhatsApp inquiry.</p>
        <div class="hero-actions">
          <a class="btn primary" href="{prefix}index.html">Return Home</a>
          <a class="btn secondary dark-text" href="{wa_link(title, url)}" rel="nofollow">WhatsApp CTA</a>
        </div>
      </section>
      <section class="section compact-section">
        <div class="section-heading"><p class="eyebrow">Product categories</p><h2>Find oilfield spare parts</h2></div>
        <div class="page-link-grid">{product_links}</div>
      </section>
    </main>
{footer(prefix, title, url)}"""


def replace_home_news(path: Path, lang: str) -> None:
    text = path.read_text(encoding="utf-8")
    prefix = rel_prefix(path)
    new_section = homepage_news_section(prefix, lang)
    pattern = r'\s*<section class="section news-events-section" id="news-events" data-news-tabs>.*?</section>'
    if not re.search(pattern, text, flags=re.S):
        raise RuntimeError(f"News section not found in {path}")
    text2 = re.sub(
        pattern,
        "\n" + new_section,
        text,
        count=1,
        flags=re.S,
    )
    if text2 != text:
        path.write_text(text2, encoding="utf-8", newline="\n")


def extract_title(text: str, fallback: str) -> str:
    match = re.search(r"<h1[^>]*>(.*?)</h1>", text, re.S | re.I)
    if not match:
        match = re.search(r"<title[^>]*>(.*?)</title>", text, re.S | re.I)
    if not match:
        return fallback
    cleaned = re.sub(r"<.*?>", "", match.group(1))
    cleaned = html.unescape(cleaned).strip()
    return cleaned or fallback


def direct_inquiry_block(prefix: str, title: str, url: str, lang: str) -> str:
    if lang == "ar":
        intro = "استخدم واتساب أو البريد الإلكتروني لإرسال رقم القطعة، موديل المضخة، موديل الحفارة، صورة المنتج أو الرسم الفني."
        wa_text = "طلب عرض عبر واتساب"
        email_text = "Email Inquiry"
    else:
        intro = "Use WhatsApp or email to send part number, pump model, rig model, product photo or technical drawing. There is no fake form submission on this page."
        wa_text = "Request Quote on WhatsApp"
        email_text = "Email Inquiry"
    return f"""<div class="quote-form quote-direct-actions" aria-label="Direct inquiry options">
          <p>{html.escape(intro)}</p>
          <a class="btn primary" href="{wa_link(title, url)}" rel="nofollow">{html.escape(wa_text)}</a>
          <a class="btn secondary dark-text" href="{email_link(title, url)}">{html.escape(email_text)}</a>
        </div>"""


def normalize_non_ru_page(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    original = text
    prefix = rel_prefix(path)
    url = page_url(path)
    lang = "ar" if path.relative_to(ROOT).parts[:1] == ("ar",) else "en"
    title = extract_title(text, "Oilfield Spare Parts")

    # Remove placeholder social labels when real URLs are not available.
    text = re.sub(r"\s*<div class=\"footer-social\"[^>]*>.*?</div>", "", text, flags=re.S)

    # Replace fake form submission with direct WhatsApp/email actions.
    text = re.sub(
        r"<form class=\"quote-form\"[^>]*>.*?</form>",
        direct_inquiry_block(prefix, title, url, lang),
        text,
        flags=re.S,
    )

    # Page-aware WhatsApp inquiry links for the main inquiry number.
    text = re.sub(
        r'href="https://api\.whatsapp\.com/send\?phone=8615908080040[^"]*"',
        f'href="{wa_link(title, url)}"',
        text,
    )

    def anchor_repl(match: re.Match[str]) -> str:
        attrs_before, href, attrs_after, inner = match.groups()
        visible = re.sub(r"<.*?>", "", inner)
        visible = html.unescape(visible).strip()
        keywords = [
            "Request Quote",
            "Send Inquiry",
            "Contact Sales",
            "WhatsApp Inquiry",
            "WhatsApp CTA",
            "Request quote",
            "Send Part Number",
            "طلب عرض",
            "استفسار",
            "إرسال رقم",
        ]
        if href.startswith("#") and any(word.lower() in visible.lower() for word in keywords):
            return f'<a{attrs_before}href="{wa_link(title, url)}"{attrs_after}>{inner}</a>'
        if visible.lower() == "email inquiry":
            return f'<a{attrs_before}href="{email_link(title, url)}"{attrs_after}>{inner}</a>'
        return match.group(0)

    text = re.sub(r'<a([^>]*?)href="([^"]*)"([^>]*)>(.*?)</a>', anchor_repl, text, flags=re.S | re.I)

    def footer_links_repl(match: re.Match[str]) -> str:
        inner = match.group(1)
        without_legal = re.sub(r'\s*<a[^>]+href="[^"]*(?:privacy-policy|terms-and-conditions|/terms/)[^"]*"[^>]*>.*?</a>', "", inner, flags=re.S | re.I)
        legal = (
            f'\n        <a href="{prefix}en/privacy-policy/">Privacy Policy</a>'
            f'\n        <a href="{prefix}en/terms-and-conditions/">Terms &amp; Conditions</a>'
        )
        return f'<div class="footer-links">{without_legal}{legal}\n      </div>'

    text = re.sub(r'<div class="footer-links">(.*?)</div>', footer_links_repl, text, count=1, flags=re.S)

    if text != original:
        path.write_text(text, encoding="utf-8", newline="\n")


def update_sitemap() -> None:
    urls: list[tuple[str, str, str]] = [
        (f"{BASE}/", "1.0", "weekly"),
        (f"{BASE}/ar/", "0.9", "weekly"),
    ]

    allowed_news = REQUESTED_NEWS_SLUGS | {"index", "industry-news", "company-news"}
    for path in sorted((ROOT / "en").rglob("index.html")):
        rel_parts = path.relative_to(ROOT).parts
        if len(rel_parts) >= 3 and rel_parts[1] == "news":
            slug = rel_parts[2] if len(rel_parts) > 3 else "index"
            if slug not in allowed_news:
                continue
        loc = page_url(path)
        priority = "0.8"
        if "/en/news/" in loc:
            priority = "0.7"
        if "/en/privacy-policy/" in loc or "/en/terms-and-conditions/" in loc:
            priority = "0.4"
        urls.append((loc, priority, "weekly"))

    seen = set()
    unique = []
    for loc, priority, freq in urls:
        if loc not in seen:
            seen.add(loc)
            unique.append((loc, priority, freq))

    entries = []
    for loc, priority, freq in unique:
        entries.append(
            f"  <url>\n    <loc>{loc}</loc>\n    <lastmod>{TODAY}</lastmod>\n    <changefreq>{freq}</changefreq>\n    <priority>{priority}</priority>\n  </url>"
        )
    sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "\n".join(entries) + "\n</urlset>\n"
    (ROOT / "sitemap.xml").write_text(sitemap, encoding="utf-8", newline="\n")


def append_css() -> None:
    path = ROOT / "styles.css"
    text = path.read_text(encoding="utf-8")
    marker = "/* Final deployment fix 3: direct inquiry, legal, and 404 polish. */"
    if marker in text:
        return
    text += f"""

{marker}
.quote-direct-actions {{
  display: grid;
  align-content: start;
  gap: 14px;
}}

.quote-direct-actions p {{
  margin: 0;
  color: var(--muted);
  line-height: 1.65;
}}

.inquiry-cta-panel {{
  padding: 24px;
  border: 1px solid rgba(0, 70, 58, 0.14);
  background: #f4f8f6;
}}

.not-found-hero {{
  min-height: 420px;
}}
"""
    path.write_text(text, encoding="utf-8", newline="\n")


def main() -> None:
    for item in NEWS:
        path = ROOT / "en" / "news" / item["slug"] / "index.html"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(article_page(item), encoding="utf-8", newline="\n")

    for kind, path in [
        (None, ROOT / "en" / "news" / "index.html"),
        ("Industry News", ROOT / "en" / "news" / "industry-news" / "index.html"),
        ("Company News", ROOT / "en" / "news" / "company-news" / "index.html"),
    ]:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(news_index_page(kind), encoding="utf-8", newline="\n")

    for path in (ROOT / "en" / "news").glob("*/index.html"):
        slug = path.parent.name
        if slug not in REQUESTED_NEWS_SLUGS and slug not in {"industry-news", "company-news"}:
            path.write_text(obsolete_news_page(path), encoding="utf-8", newline="\n")

    (ROOT / "en" / "privacy-policy").mkdir(parents=True, exist_ok=True)
    (ROOT / "en" / "privacy-policy" / "index.html").write_text(legal_page("privacy"), encoding="utf-8", newline="\n")
    (ROOT / "en" / "terms-and-conditions").mkdir(parents=True, exist_ok=True)
    (ROOT / "en" / "terms-and-conditions" / "index.html").write_text(legal_page("terms"), encoding="utf-8", newline="\n")
    (ROOT / "404.html").write_text(not_found_page(), encoding="utf-8", newline="\n")

    replace_home_news(ROOT / "index.html", "en")
    if (ROOT / "ar" / "index.html").exists():
        replace_home_news(ROOT / "ar" / "index.html", "ar")

    public_html = [
        path
        for path in ROOT.rglob("*.html")
        if "work" not in path.relative_to(ROOT).parts
        and path.relative_to(ROOT).parts[:1] != ("ru",)
    ]
    for path in public_html:
        normalize_non_ru_page(path)

    append_css()
    update_sitemap()


if __name__ == "__main__":
    main()

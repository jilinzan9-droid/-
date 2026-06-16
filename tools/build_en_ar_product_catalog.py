# -*- coding: utf-8 -*-
"""Sync the Russian product catalog into English and Arabic product catalogs.

Input:
  ru/products/index.html and ru/products/<slug>/index.html

Output:
  en/products/index.html
  en/products/<slug>/index.html
  ar/products/index.html
  ar/products/<slug>/index.html

This script intentionally does not write to ru/ or assets/.
"""

from __future__ import annotations

import html
import json
import re
import shutil
from dataclasses import dataclass, field
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import quote


ROOT = Path.cwd()
RU_PRODUCTS = ROOT / "ru" / "products"
SITE = "https://jilinzan9-droid.github.io/-/"
DATE = "2026-06-16"
WHATSAPP_PHONE = "8615908080040"


EN_CATEGORY = {
    "Буровые насосы и запасные части": "Mud Pumps and Spare Parts",
    "Буровые установки и принадлежности для лебедок": "Drilling Rigs and Drawworks Accessories",
    "Гидравлическое дисковое тормозное устройство серии PS": "PS Series Hydraulic Disc Brake System",
    "WPT пневматическое фрикционное сцепление": "WPT Pneumatic Friction Clutch",
    "Устьевой инструмент": "Wellhead Tools",
    "Клапаны, насосы и гидравлические компоненты": "Valves, Pumps and Hydraulic Components",
}

AR_CATEGORY = {
    "Буровые насосы и запасные части": "مضخات الحفر وقطع الغيار",
    "Буровые установки и принадлежности для лебедок": "الحفارات وملحقات الونش",
    "Гидравлическое дисковое тормозное устройство серии PS": "نظام الفرامل القرصية الهيدروليكية سلسلة PS",
    "WPT пневматическое фрикционное сцепление": "قابض احتكاك هوائي WPT",
    "Устьевой инструмент": "أدوات رأس البئر",
    "Клапаны, насосы и гидравлические компоненты": "الصمامات والمضخات والمكونات الهيدروليكية",
}

EN_NAME = {
    "Коленвал бурового насоса в сборе": "Mud Pump Crankshaft Assembly",
    "буровых насосов Гидравлический цилиндр в сборе": "Mud Pump Hydraulic Cylinder Assembly",
    "буровых насосов выпускной компенсатор в сборе": "Mud Pump Discharge Pulsation Dampener Assembly",
    "Втулки бурового насоса": "Mud Pump Liners",
    "Поршень бурового насоса": "Mud Pump Piston",
    "Клапаны буровых насосов": "Mud Pump Valves",
    "удлинитель поршневого штока": "Piston Rod Extension",
    "буровой насос Удлинитель стержня": "Mud Pump Rod Extension",
    "Ползун бурового насоса": "Mud Pump Crosshead",
    "Буровые насосы Износ пластины": "Mud Pump Wear Plate",
    "Пружинный предохранительный клапан": "Spring Safety Valve",
    "уплотнение втулки": "Liner Seal",
    "Вал-шестерня для Бурового насоса": "Mud Pump Pinion Shaft",
    "Гидравлический цилиндр в сборе": "Hydraulic Cylinder Assembly",
    "Втулка бурового насоса": "Mud Pump Liner",
    "Клапан для буровых насосов": "Mud Pump Valve",
    "Компенсатор в сборе насоса KB45 KB75": "KB45 KB75 Pump Pulsation Dampener Assembly",
    "Диафрагма Компенсатора KB75 KB45": "KB75 KB45 Pulsation Dampener Diaphragm",
    "буровой насос Износ пластины": "Mud Pump Wear Plate",
    "Буровой насос Удлинитель стержня": "Mud Pump Rod Extension",
    "Шток поршня бурового насоса": "Mud Pump Piston Rod",
    "Хомут штока в сборе буровго насоса": "Mud Pump Rod Clamp Assembly",
    "Предохранительный клапан со срезным штифтом": "Shear Pin Safety Valve",
    "Клапан Набор Инструмент Съемник": "Valve Puller Tool Set",
    "буровым насосам серии унбт Гидравлический цилиндр в сборе": "UNBT Series Mud Pump Hydraulic Cylinder Assembly",
    "буровым насосам серии унбт- втулка бурового насоса": "UNBT Series Mud Pump Liner",
    "буровым насосам серии унбт-поршень бурового насоса": "UNBT Series Mud Pump Piston",
    "клапан для бурового насоса": "Mud Pump Valve",
    "буровым насосам серии унбт-шток бурового насоса": "UNBT Series Mud Pump Rod",
    "буровым насосам серии унбт-Вал-шестерня для Бурового насоса": "UNBT Series Mud Pump Pinion Shaft",
    "Хомут втулки для насоса": "Pump Liner Clamp",
    "Гидравлический корпус (Гидрокоробка)": "Fluid End Module",
    "Плунжерный насос-коленчатый вал": "Plunger Pump Crankshaft",
    "Плунжер бурового насоса": "Mud Pump Plunger",
    "Клапан в сборе для насоса": "Pump Valve Assembly",
    "Плунжерный насос-большой шток": "Plunger Pump Large Rod",
    "Плунжерный насос-Уплотнительная гайка": "Plunger Pump Sealing Nut",
    "Плунжерный насос-пробковый кран": "Plunger Pump Plug Valve",
    "Уплотнение плунжерного насоса": "Plunger Pump Seal",
    "Вертикальная заглушка": "Vertical Plug",
    "Гидрокоробка": "Fluid End Module",
    "Коленчатый вал": "Crankshaft",
    "Уплотнение плунжера": "Plunger Seal",
    "буровые Вертлюг SL": "SL Drilling Swivel",
    "ротора буровой установки ZP": "ZP Drilling Rig Rotary Table",
    "Кронблок серии TC": "TC Series Crown Block",
    "Крюк талевого блока бурового оборудования": "Drilling Equipment Traveling Block Hook",
    "ATD продвигающая муфта": "ATD Advancing Clutch",
    "WPT Тормоз с водяным охлаждением": "WPT Water-Cooled Brake",
    "EatonAirflex WCB водоохладительный тормоз вспомогательный тормоз": "Eaton Airflex WCB Water-Cooled Auxiliary Brake",
    "тормоз буровой лебедки-Лента тормозная": "Drawworks Brake Band",
    "шинно-пневматическая муфта": "Pneumatic Tire Clutch",
    "CB шинно-пневматическая муфта": "CB Pneumatic Tire Clutch",
    "Цилиндр гидроусилителя руля Z02030900002AA": "Power Steering Hydraulic Cylinder Z02030900002AA",
    "Двойной направляющий кран SD-00E": "Double Directional Valve SD-00E",
    "Медный диск вспомогательного тормоза буровой установки": "Drilling Rig Auxiliary Brake Copper Disc",
    "большая передача P3100007AA": "Large Gear P3100007AA",
    "выходной вал": "Output Shaft",
    "Промежуточный вал": "Intermediate Shaft",
    "Шестерня": "Gear",
    "PS серия устанока гидравлическое дисковое тормозное устройство": "PS Series Hydraulic Disc Brake Unit",
    "Гидравлический дисковый тормозной ротор": "Hydraulic Disc Brake Rotor",
    "Рабочий цилиндр в сборе": "Working Cylinder Assembly",
    "Узел предохранительного цилиндра": "Safety Cylinder Unit",
    "Предохранительный цилиндр": "Safety Cylinder",
    "Рабочий цилиндр": "Working Cylinder",
    "ручка тормоза": "Brake Handle",
    "Фрикционные накладки гидравлического дискового тормоза": "Hydraulic Disc Brake Friction Pads",
    "Плунжерный насос BKD-Z3": "BKD-Z3 Plunger Pump",
    "Клапан реверсивный электромагнитный взрывозащищенный BKD-Z-X1": "BKD-Z-X1 Explosion-Proof Reversing Solenoid Valve",
    "парковочный клапан BK-F-Z": "BK-F-Z Parking Valve",
    "Распределитель соленоидный BK-F-W3": "BK-F-W3 Solenoid Distributor",
    "тормозной клапан BK-F-S": "BK-F-S Brake Valve",
    "WPT сцепление продвигающего диска": "WPT Advancing Disc Clutch",
    "WPT Сцепление трения Отбор мощности-WPT Type 1 PTO": "WPT Type 1 PTO Friction Clutch",
    "Буровой гидравлический ключ серии TQ": "TQ Series Drilling Hydraulic Tong",
    "Буровой гидравлический ключ серии ZQ": "ZQ Series Drilling Hydraulic Tong",
    "Элеватор бурильной трубы CD": "CD Drill Pipe Elevator",
    "Элеватор бурильной трубы CDZ": "CDZ Drill Pipe Elevator",
    "Гидравлические силовые установки серии YZB (YZC)": "YZB (YZC) Series Hydraulic Power Units",
    "Роторные клинья SDS, SDML, SDXL": "SDS, SDML, SDXL Rotary Slips",
    "Штроп одноплечный серии DH": "DH Series Single-Arm Elevator Link",
    "Буровые гидравлический ключ TQ178-16 TQ178-16Y TQ340-35 TQ356-55 Гидравлический ключ серии": "TQ178-16, TQ178-16Y, TQ340-35, TQ356-55 Hydraulic Tong Series",
    "Корпус в сборе ПКР-560": "PKR-560 Body Assembly",
    "гидравлический насос MS35-AVA": "MS35-AVA Hydraulic Pump",
    "плунжерный насос A10VSO10DR52R-PPA14N00": "A10VSO10DR52R-PPA14N00 Plunger Pump",
    "Привод отбора мощности 852ХВАКР-F6XS": "Power Take-Off Drive 852HVAKR-F6XS",
    "парковочный клапан DG17V-3-2N-60": "DG17V-3-2N-60 Parking Valve",
    "реверсивный клапан GDFW-02-2B2-D24A52": "GDFW-02-2B2-D24A52 Reversing Valve",
    "Шестеренчатый насос 7049112042": "Gear Pump 7049112042",
    "тормозной клапан LT07MKA-2X": "LT07MKA-2X Brake Valve",
    "Клапан противозатаскивателя FP-L6": "FP-L6 Anti-Drag Valve",
    "Гидравлический насос P25X378BEIU25-7": "P25X378BEIU25-7 Hydraulic Pump",
    "Распределитель соленоидный AK4Z60a 149119425": "AK4Z60a 149119425 Solenoid Distributor",
    "Регулирующий клапан HD-2-FX": "HD-2-FX Control Valve",
    "Воздушный клапан XJ-15": "XJ-15 Air Valve",
}


def e(value: object) -> str:
    return html.escape(str(value), quote=True)


def whatsapp_link(product: str = "", lang: str = "en") -> str:
    if lang == "ar":
        message = "Hello Pratt Oil, I need quotation for oilfield spare parts"
    else:
        message = "Hello Pratt Oil, I need quotation for oilfield spare parts"
    if product:
        message += f": {product}"
    return f"https://api.whatsapp.com/send?phone={WHATSAPP_PHONE}&text={quote(message)}"


def safe_delete_dir(path: Path) -> None:
    resolved = path.resolve()
    allowed = [ROOT / "en" / "products", ROOT / "ar" / "products"]
    if resolved not in [item.resolve() for item in allowed]:
        raise RuntimeError(f"Refusing to delete unexpected directory: {resolved}")
    if path.exists():
        shutil.rmtree(path)
    path.mkdir(parents=True, exist_ok=True)


def clean_text(value: str) -> str:
    return re.sub(r"\s+", " ", value or "").strip()


def inner_without_heading(section_html: str, fallback: str) -> str:
    if not section_html:
        return fallback
    return re.sub(r"\s*<div class=\"section-heading\">.*?</div>\s*", "", section_html, count=1, flags=re.S).strip() or fallback


def extract_section(html_text: str, class_name: str) -> str:
    start_match = re.search(rf'<section class="section {re.escape(class_name)}[^"]*">', html_text)
    if not start_match:
        return ""
    start = start_match.start()
    pos = start_match.end()
    depth = 1
    section_re = re.compile(r"</?section\b[^>]*>", re.I)
    for match in section_re.finditer(html_text, pos):
        token = match.group(0)
        if token.startswith("</"):
            depth -= 1
            if depth == 0:
                return html_text[start_match.end():match.start()]
        else:
            depth += 1
    return ""


def asset_for(path: str, depth: int) -> str:
    if not path:
        return ""
    clean = path.replace("../../../", "").replace("../../", "").replace("../", "")
    return ("../" * depth) + clean


def en_title(ru_name: str) -> str:
    return EN_NAME.get(ru_name, ru_name)


def ar_title(ru_name: str) -> str:
    return f"قطع غيار {en_title(ru_name)}"


def en_category(ru_category: str) -> str:
    return EN_CATEGORY.get(ru_category, ru_category)


def ar_category(ru_category: str) -> str:
    return AR_CATEGORY.get(ru_category, ru_category)


def en_subcategory(ru_sub: str) -> str:
    return EN_CATEGORY.get(ru_sub, EN_NAME.get(ru_sub, ru_sub))


def ar_subcategory(ru_sub: str) -> str:
    return AR_CATEGORY.get(ru_sub, f"مجموعة {en_subcategory(ru_sub)}")


@dataclass
class Product:
    slug: str
    href: str
    img: str
    name_ru: str
    category_ru: str
    secondary_ru: str
    description_images: list[str] = field(default_factory=list)
    model_tables_html: str = ""

    @property
    def name_en(self) -> str:
        return en_title(self.name_ru)

    @property
    def name_ar(self) -> str:
        return ar_title(self.name_ru)


@dataclass
class Subcategory:
    id: str
    name_ru: str
    products: list[Product] = field(default_factory=list)


@dataclass
class Category:
    id: str
    name_ru: str
    subcategories: list[Subcategory] = field(default_factory=list)


class CatalogParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.categories: list[Category] = []
        self.products: list[Product] = []
        self.current_category: Category | None = None
        self.current_subcategory: Subcategory | None = None
        self.in_category_heading = False
        self.in_category_h2 = False
        self.in_subcategory_h3 = False
        self.in_card = False
        self.in_card_body = False
        self.in_card_span = False
        self.in_card_title = False
        self.in_card_p = False
        self.card: dict[str, str] | None = None

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        data = {key: value or "" for key, value in attrs}
        classes = data.get("class", "")
        if tag == "section" and "ru-category-section" in classes:
            self.current_category = Category(id=data.get("id", ""), name_ru="")
            self.categories.append(self.current_category)
        elif self.current_category and tag == "div" and "ru-category-heading" in classes:
            self.in_category_heading = True
        elif self.in_category_heading and tag == "h2":
            self.in_category_h2 = True
        elif self.current_category and tag == "div" and "ru-subcategory-block" in classes:
            self.current_subcategory = Subcategory(id=data.get("id", ""), name_ru="")
            self.current_category.subcategories.append(self.current_subcategory)
        elif self.current_subcategory and tag == "h3" and not self.in_card and not self.in_card_body:
            self.in_subcategory_h3 = True
        elif tag == "article" and "ru-product-card" in classes:
            self.in_card = True
            self.card = {"href": "", "img": "", "name": "", "secondary": "", "category": ""}
        elif self.in_card and tag == "a" and self.card is not None and not self.card["href"]:
            self.card["href"] = data.get("href", "")
        elif self.in_card and tag == "img" and self.card is not None:
            self.card["img"] = data.get("src", "")
        elif self.in_card and tag == "div" and "ru-product-card-body" in classes:
            self.in_card_body = True
        elif self.in_card_body and tag == "span":
            self.in_card_span = True
        elif self.in_card_body and tag == "h3":
            self.in_card_title = True
        elif self.in_card_body and tag == "p":
            self.in_card_p = True

    def handle_endtag(self, tag: str) -> None:
        if tag == "h2":
            self.in_category_h2 = False
        elif tag == "h3":
            self.in_subcategory_h3 = False
            self.in_card_title = False
        elif tag == "span":
            self.in_card_span = False
        elif tag == "p":
            self.in_card_p = False
        elif tag == "div":
            if self.in_card_body:
                self.in_card_body = False
            elif self.in_category_heading:
                self.in_category_heading = False
        elif tag == "article" and self.in_card and self.card:
            slug = self.card["href"].strip("/").split("/")[-1]
            product = Product(
                slug=slug,
                href=self.card["href"],
                img=self.card["img"],
                name_ru=clean_text(self.card["name"]),
                category_ru=self.current_category.name_ru if self.current_category else clean_text(self.card["category"]),
                secondary_ru=self.current_subcategory.name_ru if self.current_subcategory else clean_text(self.card["secondary"]),
            )
            if self.current_subcategory:
                self.current_subcategory.products.append(product)
            self.products.append(product)
            self.in_card = False
            self.in_card_body = False
            self.card = None

    def handle_data(self, data: str) -> None:
        data = clean_text(data)
        if not data:
            return
        if self.in_category_h2 and self.current_category:
            self.current_category.name_ru = clean_text(self.current_category.name_ru + " " + data)
        elif self.in_subcategory_h3 and self.current_subcategory:
            self.current_subcategory.name_ru = clean_text(self.current_subcategory.name_ru + " " + data)
        elif self.in_card_span and self.card is not None:
            self.card["secondary"] = clean_text(self.card["secondary"] + " " + data)
        elif self.in_card_title and self.card is not None:
            self.card["name"] = clean_text(self.card["name"] + " " + data)
        elif self.in_card_p and self.card is not None:
            self.card["category"] = clean_text(self.card["category"] + " " + data)


def parse_catalog() -> tuple[list[Category], list[Product]]:
    parser = CatalogParser()
    parser.feed((RU_PRODUCTS / "index.html").read_text(encoding="utf-8"))
    product_by_slug = {product.slug: product for product in parser.products}
    for product in parser.products:
        detail = RU_PRODUCTS / product.slug / "index.html"
        if not detail.exists():
            continue
        text = detail.read_text(encoding="utf-8")
        product.description_images = sorted(
            re.findall(r'src="../../../(assets/images/ru-products/[^"]+-description-\d+\.webp)"', text)
        )
        model_section = extract_section(text, "ru-model-table-section")
        product.model_tables_html = inner_without_heading(
            model_section,
            '<p class="ru-muted">No model table is currently available. Send part number, model or product photo for quotation.</p>',
        )
    # keep category product objects aligned with enriched product list
    for category in parser.categories:
        for subcategory in category.subcategories:
            subcategory.products = [product_by_slug[item.slug] for item in subcategory.products]
    return parser.categories, parser.products


def language_panel(lang: str, depth: int, slug: str | None = None, is_index: bool = False) -> str:
    if slug:
        en_href = ("../" * depth) + f"en/products/{slug}/"
        ar_href = ("../" * depth) + f"ar/products/{slug}/"
        ru_href = ("../" * depth) + f"ru/products/{slug}/"
        active_href = "./"
    else:
        en_href = ("../" * depth) + "en/products/"
        ar_href = ("../" * depth) + "ar/products/"
        ru_href = ("../" * depth) + "ru/products/"
        active_href = "./"
    if lang == "en":
        en_href = active_href
    elif lang == "ar":
        ar_href = active_href
    panel = {
        "en": f'<a class="language-option active" href="{en_href}">English</a><a class="language-option" href="{ar_href}">Arabic</a><a class="language-option" href="{ru_href}">Russian</a>',
        "ar": f'<a class="language-option" href="{en_href}">English</a><a class="language-option active" href="{ar_href}">Arabic</a><a class="language-option" href="{ru_href}">Russian</a>',
    }[lang]
    label = "Language" if lang == "en" else "اللغة"
    aria = "Open language menu" if lang == "en" else "فتح قائمة اللغة"
    return f'<button class="language-button" type="button" data-nav-toggle aria-label="{aria}" aria-expanded="false">{label}</button><div class="dropdown-panel language-panel" data-nav-panel>{panel}</div>'


def header(lang: str, categories: list[Category], depth: int, slug: str | None = None) -> str:
    root = "../" * depth
    if lang == "en":
        home = root
        products_href = "./" if slug is None else "../"
        nav = {
            "aria": "Primary navigation",
            "menu": "Menu",
            "home": "Home",
            "about": "About Us",
            "products": "Products",
            "news": "News",
            "services": "Services",
            "contact": "Contact",
            "company": "Company Profile",
            "factory": "Factory Photos",
            "export": "Export Support",
            "company_news": "Company News",
            "industry_news": "Industry News",
        }
        category_links = "".join(f'<a href="{products_href}#{e(cat.id)}">{e(en_category(cat.name_ru))}</a>' for cat in categories)
        about_href, news_href, services_href, contact_href = f"{root}en/about-us/", f"{root}en/news/", f"{root}en/services/", f"{root}en/contact/"
    else:
        home = "../../" if depth == 3 else "../"
        products_href = "./" if slug is None else "../"
        nav = {
            "aria": "التنقل الرئيسي",
            "menu": "القائمة",
            "home": "الرئيسية",
            "about": "من نحن",
            "products": "المنتجات",
            "news": "الأخبار",
            "services": "الخدمات",
            "contact": "اتصل بنا",
            "company": "ملف الشركة",
            "factory": "صور المصنع",
            "export": "دعم التصدير",
            "company_news": "أخبار الشركة",
            "industry_news": "أخبار الصناعة",
        }
        category_links = "".join(f'<a href="{products_href}#{e(cat.id)}">{e(ar_category(cat.name_ru))}</a>' for cat in categories)
        about_href, news_href, services_href, contact_href = f"{root}en/about-us/", f"{root}en/news/", f"{root}en/services/", f"{root}en/contact/"
    return f"""<header class="site-header">
      <div class="topbar">
        <a href="{whatsapp_link(lang=lang)}" rel="nofollow">WhatsApp: +86 159 0808 0040</a>
        <a href="mailto:2000@pratt-oil.com">2000@pratt-oil.com</a>
        <a href="tel:+8615908080040">Phone: +86 159 0808 0040</a>
      </div>
      <nav class="nav" aria-label="{nav['aria']}">
        <a class="brand" href="{home}" aria-label="Jinan Prite Petroleum Equipment">
          <img class="brand-logo" src="{root}assets/images/logo/logo-pratt-oil.webp" alt="Pratt Oil logo" title="Pratt Oil logo" width="300" height="150" loading="eager" decoding="async">
          <span><strong>PRATT OIL</strong><small>Jinan Prite Petroleum Equipment</small></span>
        </a>
        <button class="menu-toggle" type="button" aria-label="{nav['menu']}" aria-expanded="false">{nav['menu']}</button>
        <div class="nav-links" id="navLinks">
          <a class="nav-main-link" href="{home}">{nav['home']}</a>
          <div class="nav-dropdown" data-nav-dropdown>
            <div class="nav-dropdown-row"><a class="nav-main-link" href="{about_href}" aria-haspopup="true">{nav['about']}</a><button class="nav-dropdown-toggle" type="button" data-nav-toggle aria-label="{nav['about']}" aria-expanded="false">v</button></div>
            <div class="dropdown-panel" data-nav-panel><a href="{about_href}">{nav['company']}</a><a href="{root}en/factory-photos/">{nav['factory']}</a><a href="{root}en/export-support/">{nav['export']}</a></div>
          </div>
          <div class="nav-dropdown" data-nav-dropdown>
            <div class="nav-dropdown-row"><a class="nav-main-link" href="{products_href}" aria-haspopup="true">{nav['products']}</a><button class="nav-dropdown-toggle" type="button" data-nav-toggle aria-label="{nav['products']}" aria-expanded="false">v</button></div>
            <div class="dropdown-panel" data-nav-panel>{category_links}</div>
          </div>
          <div class="nav-dropdown" data-nav-dropdown>
            <div class="nav-dropdown-row"><a class="nav-main-link" href="{news_href}" aria-haspopup="true">{nav['news']}</a><button class="nav-dropdown-toggle" type="button" data-nav-toggle aria-label="{nav['news']}" aria-expanded="false">v</button></div>
            <div class="dropdown-panel" data-nav-panel><a href="{root}en/news/company-news/">{nav['company_news']}</a><a href="{root}en/news/industry-news/">{nav['industry_news']}</a></div>
          </div>
          <a class="nav-main-link" href="{services_href}">{nav['services']}</a>
          <a class="nav-main-link" href="{contact_href}">{nav['contact']}</a>
        </div>
        <div class="nav-actions">
          <div class="language-dropdown" data-nav-dropdown>{language_panel(lang, depth, slug)}</div>
          <a class="nav-quick-link" href="{whatsapp_link(lang=lang)}" rel="nofollow">WhatsApp</a>
        </div>
      </nav>
    </header>"""


def head(lang: str, title: str, description: str, canonical: str, image: str, depth: int, schema: dict) -> str:
    root = "../" * depth
    html_lang = "ar" if lang == "ar" else "en"
    dir_attr = ' dir="rtl"' if lang == "ar" else ""
    locale = "ar_AR" if lang == "ar" else "en_US"
    return f"""<!doctype html>
<html lang="{html_lang}"{dir_attr}>
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{e(title)}</title>
    <meta name="description" content="{e(description)}">
    <meta name="robots" content="index, follow, max-image-preview:large">
    <link rel="canonical" href="{e(canonical)}">
    <link rel="alternate" hreflang="en" href="{e(canonical.replace('/ar/', '/en/') if '/ar/' in canonical else canonical)}">
    <link rel="alternate" hreflang="ar" href="{e(canonical.replace('/en/', '/ar/') if '/en/' in canonical else canonical)}">
    <link rel="alternate" hreflang="ru" href="{e(canonical.replace('/en/', '/ru/').replace('/ar/', '/ru/'))}">
    <link rel="alternate" hreflang="x-default" href="{e(canonical.replace('/ar/', '/en/'))}">
    <meta property="og:type" content="website">
    <meta property="og:title" content="{e(title)}">
    <meta property="og:description" content="{e(description)}">
    <meta property="og:url" content="{e(canonical)}">
    <meta property="og:site_name" content="Jinan Prite Petroleum Equipment Co., Ltd.">
    <meta property="og:locale" content="{locale}">
    <meta property="og:image" content="{e(SITE + image)}">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{e(title)}">
    <meta name="twitter:description" content="{e(description)}">
    <meta name="twitter:image" content="{e(SITE + image)}">
    <link rel="stylesheet" href="{root}styles.css?v=en-ar-products-20260616">
    <script type="application/ld+json">{json.dumps(schema, ensure_ascii=False, separators=(",", ":"))}</script>
  </head>"""


def product_description(product: Product, lang: str) -> str:
    if lang == "ar":
        return f"{product.name_ar} لعمليات الصيانة والاستبدال في معدات حقول النفط. يمكن للمشترين إرسال رقم القطعة أو موديل المعدة أو صورة المنتج أو الرسم الفني للحصول على عرض سعر."
    return f"{product.name_en} for oilfield equipment maintenance and replacement projects. Buyers can send part number, equipment model, product photo or technical drawing for quotation."


def build_catalog(lang: str, categories: list[Category], products: list[Product]) -> None:
    out_dir = ROOT / lang / "products"
    safe_delete_dir(out_dir)
    body_class = "ru-catalog-page en-product-catalog-page" if lang == "en" else "ru-catalog-page ar-product-catalog-page"
    dir_attr = ' dir="rtl"' if lang == "ar" else ""
    title = (
        "Oilfield Equipment Product Catalog | Pratt Oil"
        if lang == "en"
        else "كتالوج منتجات معدات حقول النفط | Pratt Oil"
    )
    desc = (
        "Product catalog synchronized from the Russian product library, including oilfield spare parts images, product categories, description photos and model tables for quotation support."
        if lang == "en"
        else "كتالوج منتجات متزامن من مكتبة المنتجات الروسية، يتضمن صور قطع غيار حقول النفط والتصنيفات وصور الوصف وجداول الموديلات لدعم عروض الأسعار."
    )
    canonical = SITE + f"{lang}/products/"
    first_img = next((product.img for product in products if product.img), "../../assets/images/hero/hero-oilfield-equipment-spare-parts-middle-east.webp")
    first_img_clean = first_img.replace("../../", "").replace("../", "")
    schema = {
        "@context": "https://schema.org",
        "@graph": [
            {"@type": "Organization", "@id": SITE + "#organization", "name": "Jinan Prite Petroleum Equipment Co., Ltd.", "alternateName": "Pratt Oil", "url": SITE},
            {"@type": "CollectionPage", "@id": canonical + "#webpage", "url": canonical, "name": title, "description": desc, "inLanguage": lang},
            {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": 1, "name": "Home" if lang == "en" else "الرئيسية", "item": SITE + ("" if lang == "en" else "ar/")}, {"@type": "ListItem", "position": 2, "name": "Products" if lang == "en" else "المنتجات", "item": canonical}]},
        ],
    }

    def cat_name(cat: Category) -> str:
        return en_category(cat.name_ru) if lang == "en" else ar_category(cat.name_ru)

    category_cards = []
    for category in categories:
        thumb = next((p.img for sub in category.subcategories for p in sub.products if p.img), "")
        image_html = (
            f'<img src="{asset_for(thumb, 2)}" alt="{e(cat_name(category))}" title="{e(cat_name(category))}" width="900" height="650" loading="lazy" decoding="async">'
            if thumb
            else f'<span>{"Category image placeholder" if lang == "en" else "موضع صورة التصنيف"}</span>'
        )
        count = sum(len(sub.products) for sub in category.subcategories)
        count_text = f"{count} products" if lang == "en" else f"{count} منتج"
        category_cards.append(f'<a class="ru-category-card" href="#{e(category.id)}"><div class="ru-category-card-media">{image_html}</div><strong>{e(cat_name(category))}</strong><span>{count_text}</span></a>')

    sections = []
    for category in categories:
        sub_links = "".join(
            f'<a href="#{e(sub.id)}">{e(en_subcategory(sub.name_ru) if lang == "en" else ar_subcategory(sub.name_ru))}</a>'
            for sub in category.subcategories
        )
        sub_blocks = []
        for sub in category.subcategories:
            cards = []
            for product in sub.products:
                title_text = product.name_en if lang == "en" else product.name_ar
                category_text = cat_name(category)
                sub_text = en_subcategory(sub.name_ru) if lang == "en" else ar_subcategory(sub.name_ru)
                image_html = (
                    f'<img src="{asset_for(product.img, 2)}" alt="{e(title_text)}" title="{e(title_text)}" width="900" height="650" loading="lazy" decoding="async">'
                    if product.img
                    else f'<span>{"Product image placeholder" if lang == "en" else "موضع صورة المنتج"}</span>'
                )
                cards.append(
                    f"""<article class="ru-product-card">
              <a href="{e(product.slug)}/">
                <div class="ru-product-card-media">{image_html}</div>
                <div class="ru-product-card-body"><span>{e(sub_text)}</span><h3>{e(title_text)}</h3><p>{e(category_text)}</p></div>
              </a>
              <a class="mini-btn dark" href="{whatsapp_link(title_text, lang)}" rel="nofollow">{"Request Quote" if lang == "en" else "طلب عرض سعر"}</a>
            </article>"""
                )
            sub_blocks.append(f"""<div class="ru-subcategory-block" id="{e(sub.id)}">
            <h3>{e(en_subcategory(sub.name_ru) if lang == "en" else ar_subcategory(sub.name_ru))}</h3>
            <div class="ru-product-grid">{''.join(cards)}</div>
          </div>""")
        section_intro = (
            "Oilfield equipment spare parts synchronized from the Russian product library. Send part number, model or product photo for quotation and compatibility support."
            if lang == "en"
            else "قطع غيار معدات حقول النفط متزامنة من مكتبة المنتجات الروسية. أرسل رقم القطعة أو الموديل أو صورة المنتج للحصول على عرض سعر ودعم المطابقة."
        )
        sections.append(f"""<section class="ru-category-section" id="{e(category.id)}">
          <div class="ru-category-heading"><p class="eyebrow">{"Product Category" if lang == "en" else "تصنيف المنتجات"}</p><h2>{e(cat_name(category))}</h2><p>{e(section_intro)}</p></div>
          <div class="ru-subcategory-links">{sub_links}</div>
          {''.join(sub_blocks)}
        </section>""")

    hero_title = (
        "Oilfield Equipment Products and Spare Parts Catalog"
        if lang == "en"
        else "كتالوج منتجات ومعدات وقطع غيار حقول النفط"
    )
    hero_text = (
        "This catalog synchronizes the uploaded Russian product library into the English website. Product images, description photos and model tables are preserved for quotation support."
        if lang == "en"
        else "يقوم هذا الكتالوج بمزامنة مكتبة المنتجات الروسية المرفوعة إلى الموقع العربي. تم الحفاظ على صور المنتجات وصور الوصف وجداول الموديلات لدعم عروض الأسعار."
    )
    view_text = "View Products" if lang == "en" else "عرض المنتجات"
    quote_text = "Request Quote on WhatsApp" if lang == "en" else "طلب عرض عبر واتساب"
    product_label = "Products" if lang == "en" else "المنتجات"
    category_heading = "Product Categories" if lang == "en" else "تصنيفات المنتجات"
    category_intro = (
        "Choose a category below. All product images use the already processed WebP files from the uploaded product library."
        if lang == "en"
        else "اختر تصنيفا أدناه. جميع صور المنتجات تستخدم ملفات WebP التي تمت معالجتها مسبقا من مكتبة المنتجات المرفوعة."
    )
    html_text = head(lang, title, desc, canonical, first_img_clean, 2, schema) + f"""
  <body class="{body_class}"{dir_attr}>
    {header(lang, categories, 2)}
    <main>
      <section class="ru-catalog-hero">
        <p class="eyebrow">{product_label}</p>
        <h1>{hero_title}</h1>
        <p>{hero_text}</p>
        <div class="hero-actions"><a class="btn primary" href="{whatsapp_link(lang=lang)}" rel="nofollow">{quote_text}</a><a class="btn secondary light" href="#catalog">{view_text}</a></div>
      </section>
      <section class="section ru-category-overview" id="catalog">
        <div class="section-heading"><p class="eyebrow">{product_label}</p><h2>{category_heading}</h2><p>{category_intro}</p></div>
        <div class="ru-category-card-grid">{''.join(category_cards)}</div>
      </section>
      <section class="section ru-catalog-sections">
        {''.join(sections)}
      </section>
      {contact_section(lang)}
    </main>
    {footer(lang, 2)}
    <script src="../../script.js"></script>
  </body>
</html>
"""
    (out_dir / "index.html").write_text(html_text, encoding="utf-8", newline="\n")


def contact_section(lang: str) -> str:
    if lang == "ar":
        return f"""<section class="section contact-section" id="contact">
        <div><p class="eyebrow">استفسار</p><h2>أرسل رقم القطعة أو صورة المنتج</h2><p>للتسعير السريع، أرسل رقم القطعة أو موديل المضخة أو موديل الحفارة أو صورة المنتج أو الرسم الفني.</p></div>
        <div class="contact-grid"><a href="mailto:2000@pratt-oil.com"><span>Email</span><strong>2000@pratt-oil.com</strong></a><a href="mailto:2001@pratt-oil.com"><span>Email</span><strong>2001@pratt-oil.com</strong></a><a href="{whatsapp_link(lang='ar')}" rel="nofollow"><span>WhatsApp</span><strong>+86 159 0808 0040</strong></a><a href="tel:+8618063410221"><span>Phone</span><strong>+86 180 6341 0221</strong></a></div>
        <address>Building 11, Zhigu Industrial Park, High-tech Zone, Jinan, Shandong Province, China</address>
      </section>"""
    return f"""<section class="section contact-section" id="contact">
        <div><p class="eyebrow">Inquiry</p><h2>Send Part Number or Product Photo</h2><p>For fast quotation, send part number, pump model, rig model, product photo or technical drawing.</p></div>
        <div class="contact-grid"><a href="mailto:2000@pratt-oil.com"><span>Email</span><strong>2000@pratt-oil.com</strong></a><a href="mailto:2001@pratt-oil.com"><span>Email</span><strong>2001@pratt-oil.com</strong></a><a href="{whatsapp_link()}" rel="nofollow"><span>WhatsApp</span><strong>+86 159 0808 0040</strong></a><a href="tel:+8618063410221"><span>Phone</span><strong>+86 180 6341 0221</strong></a></div>
        <address>Building 11, Zhigu Industrial Park, High-tech Zone, Jinan, Shandong Province, China</address>
      </section>"""


def footer(lang: str, depth: int) -> str:
    root = "../" * depth
    if lang == "ar":
        brand_text = "مورد محترف لمعدات حفر النفط وقطع الغيار لأسواق النفط والغاز الدولية."
        links = f'<a href="#catalog">المنتجات</a><a href="#contact">اتصل بنا</a><a href="{whatsapp_link(lang="ar")}" rel="nofollow">WhatsApp</a>'
    else:
        brand_text = "Professional supplier of oil drilling equipment and spare parts for international oil and gas markets."
        links = f'<a href="#catalog">Products</a><a href="#contact">Contact</a><a href="{whatsapp_link()}" rel="nofollow">WhatsApp</a>'
    return f"""<footer class="footer">
      <div class="footer-brand"><img class="footer-logo" src="{root}assets/images/logo/logo-pratt-oil.webp" alt="Pratt Oil logo" title="Pratt Oil logo" width="300" height="150" loading="lazy" decoding="async"><div><strong>Jinan Prite Petroleum Equipment Co., Ltd.</strong><p>{brand_text}</p></div></div>
      <div class="footer-links">{links}</div>
      <div class="footer-social" aria-label="Social media channels"><span>Facebook</span><span>Instagram</span><span>YouTube</span></div>
    </footer>
    <a class="floating-whatsapp" href="{whatsapp_link(lang=lang)}" rel="nofollow" aria-label="WhatsApp inquiry">WhatsApp</a>"""


def build_detail(lang: str, categories: list[Category], products: list[Product]) -> None:
    out_root = ROOT / lang / "products"
    product_by_slug = {p.slug: p for p in products}
    for product in products:
        out_dir = out_root / product.slug
        out_dir.mkdir(parents=True, exist_ok=True)
        title_text = product.name_en if lang == "en" else product.name_ar
        category_text = en_category(product.category_ru) if lang == "en" else ar_category(product.category_ru)
        sub_text = en_subcategory(product.secondary_ru) if lang == "en" else ar_subcategory(product.secondary_ru)
        desc = product_description(product, lang)
        canonical = SITE + f"{lang}/products/{product.slug}/"
        image = product.img.replace("../../", "").replace("../", "") if product.img else "assets/images/hero/hero-oilfield-equipment-spare-parts-middle-east.webp"
        schema = {
            "@context": "https://schema.org",
            "@graph": [
                {"@type": "Organization", "@id": SITE + "#organization", "name": "Jinan Prite Petroleum Equipment Co., Ltd.", "alternateName": "Pratt Oil", "url": SITE},
                {"@type": "Product", "name": title_text, "category": category_text, "brand": {"@type": "Brand", "name": "Pratt Oil"}, "image": SITE + image, "description": desc},
                {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": 1, "name": "Home" if lang == "en" else "الرئيسية", "item": SITE + ("" if lang == "en" else "ar/")}, {"@type": "ListItem", "position": 2, "name": "Products" if lang == "en" else "المنتجات", "item": SITE + f"{lang}/products/"}, {"@type": "ListItem", "position": 3, "name": title_text, "item": canonical}]},
            ],
        }
        body_class = "ru-product-detail-page en-product-detail-page" if lang == "en" else "ru-product-detail-page ar-product-detail-page"
        dir_attr = ' dir="rtl"' if lang == "ar" else ""
        image_html = (
            f'<img src="{asset_for(product.img, 3)}" alt="{e(title_text)}" title="{e(title_text)}" width="900" height="650" loading="eager" decoding="async">'
            if product.img
            else f'<span>{"Product image placeholder" if lang == "en" else "موضع صورة المنتج"}</span>'
        )
        description_figures = "".join(
            f'<figure><img src="{asset_for(src, 3)}" alt="{e(title_text)} description image {idx}" title="{e(title_text)} description image {idx}" width="1200" height="800" loading="lazy" decoding="async"><figcaption>{e(title_text)} - {"description image" if lang == "en" else "صورة وصف"} {idx}</figcaption></figure>'
            for idx, src in enumerate(product.description_images, 1)
        )
        if not description_figures:
            description_figures = f'<p class="ru-muted">{"No description image has been uploaded for this product yet." if lang == "en" else "لم يتم رفع صورة وصف لهذا المنتج حتى الآن."}</p>'
        table_html = product.model_tables_html.replace("../../../assets/", "../../../assets/")
        if lang == "ar":
            table_intro = "إذا كان ملف المنتج الأصلي يحتوي على جدول موديلات أو مواصفات، فسيظهر هنا لدعم اختيار المنتج وطلب عرض السعر."
            table_title = "الموديلات والمواصفات الفنية"
            table_eyebrow = "المواصفات"
            desc_title = "صور الوصف ومواد المنتج"
            quote_title = "كيفية طلب عرض سعر"
            quote_items = ["أرسل رقم القطعة أو موديل المعدة.", "يمكنك إرفاق صورة المنتج أو الرسم الفني.", "سنراجع المطابقة ونجهز عرض السعر."]
            app_title = "الاستخدام"
            supply_title = "دعم التوريد"
            detail_intro = f"{category_text}. {desc}"
            meta1, meta2, meta3 = "التصنيف الأول", "التصنيف الثاني", "المنتج"
            quote_btn, email_btn = "طلب عرض عبر واتساب", "إرسال بريد إلكتروني"
            related_title = "منتجات ذات صلة"
            contact_title = "تواصل مع Pratt Oil"
        else:
            table_intro = "If the original product folder includes a model or specification table, it is displayed here for product selection and quotation support."
            table_title = "Models and Technical Specifications"
            table_eyebrow = "Specifications"
            desc_title = "Description Photos and Product Materials"
            quote_title = "How to Request a Quotation"
            quote_items = ["Send part number or equipment model.", "Attach product photo or technical drawing if available.", "We will check compatibility and prepare quotation details."]
            app_title = "Application"
            supply_title = "Supply Support"
            detail_intro = f"{category_text}. {desc}"
            meta1, meta2, meta3 = "Primary category", "Secondary category", "Product"
            quote_btn, email_btn = "Request Quote on WhatsApp", "Send Email"
            related_title = "Related Products"
            contact_title = "Contact Pratt Oil"
        related = [p for p in products if p.category_ru == product.category_ru and p.slug != product.slug][:6]
        related_links = "".join(
            f'<a href="../{e(item.slug)}/">{e(item.name_en if lang == "en" else item.name_ar)}</a>'
            for item in related
        )
        quote_list = "".join(f"<li>{item}</li>" for item in quote_items)
        html_text = head(lang, f"{title_text} | Pratt Oil", desc, canonical, image, 3, schema) + f"""
  <body class="{body_class}"{dir_attr}>
    {header(lang, categories, 3, product.slug)}
    <main>
      <nav class="ru-breadcrumb" aria-label="Breadcrumb"><a href="../../">{"Home" if lang == "en" else "الرئيسية"}</a><span>/</span><a href="../">{"Products" if lang == "en" else "المنتجات"}</a><span>/</span><strong>{e(title_text)}</strong></nav>
      <section class="section ru-product-detail-hero">
        <div class="ru-product-detail-copy">
          <p class="eyebrow">{e(category_text)}</p>
          <h1>{e(title_text)}</h1>
          <p>{e(detail_intro)}</p>
          <div class="ru-product-meta"><span>{meta1}: {e(category_text)}</span><span>{meta2}: {e(sub_text)}</span><span>{meta3}: {e(title_text)}</span></div>
          <div class="hero-actions"><a class="btn primary" href="{whatsapp_link(title_text, lang)}" rel="nofollow">{quote_btn}</a><a class="btn secondary dark-text" href="mailto:2000@pratt-oil.com">{email_btn}</a></div>
        </div>
        <div class="ru-product-detail-image">{image_html}</div>
      </section>
      <section class="section ru-product-info-grid">
        <article><h2>{quote_title}</h2><ul>{quote_list}</ul></article>
        <article><h2>{app_title}</h2><p>{e(desc)}</p></article>
        <article><h2>{supply_title}</h2><p>{"Specification matching, export packaging, WhatsApp and email communication support for oilfield buyers." if lang == "en" else "دعم مطابقة المواصفات وتغليف التصدير والتواصل عبر واتساب والبريد الإلكتروني لمشتري حقول النفط."}</p></article>
      </section>
      <section class="section ru-description-images">
        <div class="section-heading"><p class="eyebrow">{"Description" if lang == "en" else "الوصف"}</p><h2>{desc_title}</h2><p>{"Images marked as description materials are placed here and are not used as the product card thumbnail." if lang == "en" else "الصور المخصصة للوصف تظهر هنا ولا تستخدم كصورة بطاقة المنتج الرئيسية."}</p></div>
        <div class="ru-description-grid">{description_figures}</div>
      </section>
      <section class="section ru-model-table-section">
        <div class="section-heading"><p class="eyebrow">{table_eyebrow}</p><h2>{table_title}</h2><p>{table_intro}</p></div>
        {table_html}
      </section>
      <section class="section ru-related-products"><div class="section-heading"><p class="eyebrow">{"Related" if lang == "en" else "ذات صلة"}</p><h2>{related_title}</h2></div><div class="ru-related-links">{related_links}</div></section>
      {contact_section(lang)}
    </main>
    {footer(lang, 3)}
    <script src="../../../script.js"></script>
  </body>
</html>
"""
        (out_dir / "index.html").write_text(html_text, encoding="utf-8", newline="\n")


def main() -> None:
    categories, products = parse_catalog()
    if len(products) != 99:
        raise RuntimeError(f"Expected 99 Russian products, found {len(products)}")
    for lang in ("en", "ar"):
        build_catalog(lang, categories, products)
        build_detail(lang, categories, products)
    print(f"Generated {len(products)} products for English and Arabic catalogs.")


if __name__ == "__main__":
    main()

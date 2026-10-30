#!/usr/bin/env python3
"""SEO helpers for PDC docs (canonical, Open Graph, JSON-LD, sitemap, robots)."""

from __future__ import annotations

import html
import json
from pathlib import Path
from typing import Iterable
from xml.sax.saxutils import escape as xml_escape

SITE = "https://docs.privacydatacoin.com"
SITE_NAME = "PDC Docs"
ORG_NAME = "Privacy Data Coin"
ORG_URL = "https://privacydatacoin.com/"
OG_IMAGE = f"{SITE}/graphics/pdc-logo.png"
LOGO = f"{SITE}/graphics/pdc-logo.png"


def esc(value: str) -> str:
    return html.escape(value or "", quote=True)


def page_path(slug: str) -> str:
    if slug == "index":
        return ""
    return f"{slug}.html"


def page_url(slug: str) -> str:
    path = page_path(slug)
    return f"{SITE}/{path}" if path else f"{SITE}/"


def description_for(slug: str, title: str, summaries: dict[str, str]) -> str:
    raw = summaries.get(slug) or title
    text = " ".join(raw.split())
    if "Privacy Data Coin" not in text and "PDC" not in text:
        text = f"{text} Privacy Data Coin (PDC) documentation."
    if len(text) > 160:
        cut = text[:157].rsplit(" ", 1)[0]
        text = cut + "…"
    return text


def breadcrumb_items(slug: str, title: str, section: str) -> list[tuple[str, str]]:
    items = [("Docs", f"{SITE}/")]
    if slug == "index":
        return items
    if section and section != "Privacy Data Coin":
        items.append((section, f"{SITE}/"))
    items.append((title, page_url(slug)))
    return items


def json_ld_blocks(slug: str, title: str, section: str, description: str) -> str:
    url = page_url(slug)
    website = {
        "@context": "https://schema.org",
        "@type": "WebSite",
        "name": SITE_NAME,
        "alternateName": ["Privacy Data Coin Docs", "PDC Documentation"],
        "url": f"{SITE}/",
        "description": "Official documentation for Privacy Data Coin (PDC): wallets, Matrix Messenger, Trade, Oracle, mining, staking, TIP Bot, and Funding.",
        "publisher": {"@type": "Organization", "name": ORG_NAME, "url": ORG_URL, "logo": LOGO},
        "inLanguage": "en",
    }
    organization = {
        "@context": "https://schema.org",
        "@type": "Organization",
        "name": ORG_NAME,
        "alternateName": "PDC",
        "url": ORG_URL,
        "logo": LOGO,
        "email": "privacydatacoin@proton.me",
        "sameAs": [
            "https://github.com/PrivacyDataCoin-Project/PDC",
            "https://x.com/PrivacyDataCoin",
            "https://www.reddit.com/r/PrivacyDataCoinPDC/",
            "https://t.me/privacydatacoin",
            "https://medium.com/@privacydatacoin",
            "https://matrix.privacydatacoin.com/",
            SITE + "/",
        ],
    }
    crumbs = breadcrumb_items(slug, title, section)
    breadcrumb = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": name, "item": item}
            for i, (name, item) in enumerate(crumbs)
        ],
    }
    if slug == "index":
        page = {
            "@context": "https://schema.org",
            "@type": "CollectionPage",
            "name": title,
            "description": description,
            "url": url,
            "isPartOf": {"@type": "WebSite", "name": SITE_NAME, "url": f"{SITE}/"},
            "about": {"@type": "SoftwareApplication", "name": "Privacy Data Coin", "applicationCategory": "FinanceApplication"},
            "inLanguage": "en",
        }
    else:
        page = {
            "@context": "https://schema.org",
            "@type": "TechArticle",
            "headline": title,
            "name": title,
            "description": description,
            "url": url,
            "mainEntityOfPage": url,
            "isPartOf": {"@type": "WebSite", "name": SITE_NAME, "url": f"{SITE}/"},
            "author": {"@type": "Organization", "name": ORG_NAME, "url": ORG_URL},
            "publisher": {"@type": "Organization", "name": ORG_NAME, "url": ORG_URL, "logo": {"@type": "ImageObject", "url": LOGO}},
            "image": OG_IMAGE,
            "inLanguage": "en",
            "articleSection": section,
            "about": "Privacy Data Coin",
            "keywords": ", ".join(
                filter(None, ["Privacy Data Coin", "PDC", section, title, "documentation", "cryptocurrency"])
            ),
        }
    blocks = [website, organization, page, breadcrumb]
    return "\n".join(
        f'<script type="application/ld+json">\n{json.dumps(block, ensure_ascii=False, indent=2)}\n</script>'
        for block in blocks
    )


def head_meta(
    *,
    slug: str,
    title: str,
    section: str,
    description: str,
    prefix: str,
    indexable: bool = True,
) -> str:
    url = page_url(slug)
    path = page_path(slug)
    full_title = f"{title} · {SITE_NAME}" if slug != "index" else f"{title} · {SITE_NAME}"
    robots = (
        "index,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1"
        if indexable
        else "noindex,nofollow"
    )
    og_type = "website" if slug == "index" else "article"
    return f"""  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(full_title)}</title>
  <meta name="description" content="{esc(description)}">
  <meta name="robots" content="{robots}">
  <meta name="author" content="{esc(ORG_NAME)}">
  <meta name="theme-color" content="#05060d">
  <meta name="color-scheme" content="dark">
  <link rel="canonical" href="{esc(url)}">
  <link rel="alternate" hreflang="en" href="{esc(url)}">
  <link rel="alternate" hreflang="x-default" href="{esc(url)}">
  <meta property="og:type" content="{og_type}">
  <meta property="og:site_name" content="{esc(SITE_NAME)}">
  <meta property="og:locale" content="en_US">
  <meta property="og:title" content="{esc(full_title)}">
  <meta property="og:description" content="{esc(description)}">
  <meta property="og:url" content="{esc(url)}">
  <meta property="og:image" content="{esc(OG_IMAGE)}">
  <meta property="og:image:alt" content="Privacy Data Coin">
  <meta name="twitter:card" content="summary">
  <meta name="twitter:title" content="{esc(full_title)}">
  <meta name="twitter:description" content="{esc(description)}">
  <meta name="twitter:image" content="{esc(OG_IMAGE)}">
  <link rel="icon" href="{prefix}favicon.png" type="image/png">
  <link rel="apple-touch-icon" href="{prefix}graphics/pdc-logo.png">
{json_ld_blocks(slug, title, section, description)}"""


def breadcrumb_nav(slug: str, title: str, section: str, prefix: str) -> str:
    if slug == "index":
        return ""
    home = prefix + "index.html"
    parts = [f'<a href="{home}">Docs</a>']
    if section and section != "Privacy Data Coin":
        parts.append(f"<span>{esc(section)}</span>")
    parts.append(f"<span aria-current=\"page\">{esc(title)}</span>")
    inner = '<span class="bc-sep" aria-hidden="true">/</span>'.join(parts)
    return f'<nav class="breadcrumbs" aria-label="Breadcrumb">{inner}</nav>'


def write_robots(out_dir: Path) -> None:
    (out_dir / "robots.txt").write_text(
        "User-agent: *\n"
        "Allow: /\n"
        f"Sitemap: {SITE}/sitemap.xml\n",
        encoding="utf-8",
    )


def write_sitemap(out_dir: Path, slugs: Iterable[str]) -> None:
    urls = []
    for slug in slugs:
        loc = page_url(slug)
        # Home first / highest priority
        priority = "1.0" if slug == "index" else "0.8"
        changefreq = "weekly" if slug == "index" else "monthly"
        urls.append(
            "  <url>\n"
            f"    <loc>{xml_escape(loc)}</loc>\n"
            f"    <changefreq>{changefreq}</changefreq>\n"
            f"    <priority>{priority}</priority>\n"
            "  </url>"
        )
    body = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "\n".join(urls)
        + "\n</urlset>\n"
    )
    (out_dir / "sitemap.xml").write_text(body, encoding="utf-8")

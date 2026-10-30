#!/usr/bin/env python3
"""Render content markdown into the static PDC documentation site."""

from pathlib import Path
import re
import sys

import markdown

ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "content"
sys.path.insert(0, str(ROOT / "tools"))
import seo  # noqa: E402

NAV = [
    ("Learn", [
        ("learn/what-is-pdc", "What PDC is"),
        ("learn/how-it-works", "How PDC works"),
        ("learn/faq", "FAQ"),
    ]),
    ("Use", [
        ("use/getting-started", "Getting started"),
        ("use/security", "Security and privacy"),
        ("use/troubleshooting", "Troubleshooting"),
    ]),
    ("Wallets", [
        ("wallets/gui", "GUI"),
        ("wallets/ios", "iOS"),
    ]),
    ("Matrix", [
        ("matrix/messenger", "PDC Messenger"),
    ]),
    ("Trade", [
        ("trade/trade", "Trade"),
        ("trade/bridge", "Bridge"),
        ("trade/api", "Trade API"),
        ("trade/companion", "PDC Companion"),
    ]),
    ("Oracle", [
        ("oracle/oracle", "Oracle"),
        ("oracle/paid-attestation", "Paid attestation"),
        ("oracle/api", "Oracle API"),
    ]),
    ("Build", [
        ("build/from-source", "Build from source"),
        ("build/rpc", "Node RPC"),
        ("build/assets", "Confidential assets"),
        ("build/aliases", "Aliases"),
        ("build/services", "Escrow, swaps, and offers"),
    ]),
    ("Mine", [
        ("mine/mining", "Mining"),
    ]),
    ("Stake", [
        ("stake/staking", "Staking"),
        ("stake/proof-of-stake", "Proof of stake"),
    ]),
    ("Tools", [
        ("tools/tipbot", "TIP Bot"),
        ("tools/funding", "Funding"),
    ]),
    ("Code", [
        ("code/parameters", "Network parameters"),
        ("code/source-map", "Source map"),
    ]),
]

FLAT = [item for _, group in NAV for item in group]
SUMMARIES = {
    "learn/what-is-pdc": "The chain, the release, and what a transfer hides.",
    "learn/how-it-works": "Addresses, proofs, consensus, and the block reward.",
    "learn/faq": "Short answers grounded in the source tree.",
    "use/getting-started": "Install the current release, sync, and make a wallet.",
    "use/security": "What stays private, and what you still have to protect.",
    "use/troubleshooting": "Genesis, ports, and sync.",
    "wallets/gui": "Desktop Qt Pdc GUI, staking, Companion, and simplewallet.",
    "wallets/ios": "Official PDC Wallet on iOS — remote node, non-custodial.",
    "wallets/overview": "Legacy pointer — use GUI or iOS.",
    "wallets/desktop": "Legacy pointer — moved to GUI.",
    "use/wallets": "Moved to the Wallets section (legacy URL).",
    "matrix/messenger": "Claim a Matrix account with your PDC alias, sign in on matrix.privacydatacoin.com, and use E2EE chat with the Telegram bridge.",
    "use/messenger": "Moved to the Matrix section (legacy URL).",
    "trade/trade": "Exchange, hub fees, Easy Swap, Matches, and firmer order-book offers.",
    "trade/bridge": "Wrap BTC→BTCX and ARQ→ARQX; custody and safety.",
    "trade/api": "Public Trade HTTP API — ticker, fees, bridge routes.",
    "trade/companion": "Browser extension that connects Trade to a local PDC wallet.",
    "oracle/oracle": "Signed USD feed — CEX quorum, trade_book PDC, methodology links.",
    "oracle/paid-attestation": "Paid CA tip → EVM attestation — how it works and how to pay.",
    "oracle/api": "Oracle HTTP API — prices, methodology, verify schema v1.",
    "build/from-source": "Clone, dependencies, and the daemon build.",
    "build/rpc": "JSON-RPC on port 19211, bound to localhost.",
    "build/assets": "Issue a token without revealing transfer amounts.",
    "build/aliases": "Human-readable names. The fee is burned.",
    "build/services": "Escrow, ionic swaps, and marketplace offers.",
    "mine/mining": "RandomARQ, XMRig, and the stratum port.",
    "stake/staking": "Keep a synced wallet online and stake PDC.",
    "stake/proof-of-stake": "Zarcanum, coinstake age, and the PoS run limit.",
    "tools/tipbot": "Telegram and Matrix tip bot: tips, rain, deposits, and withdraw.",
    "tools/funding": "Community crowdfunding: proposals, escrow donations, milestone payouts.",
    "code/parameters": "The numbers a node boots with.",
    "code/source-map": "Where each subsystem lives in the tree.",
}


def parse(path: Path):
    text = path.read_text(encoding="utf-8")
    title = path.stem
    if text.startswith("---\n"):
        _, meta, body = text.split("---", 2)
        for line in meta.strip().splitlines():
            if line.startswith("title:"):
                title = line.split(":", 1)[1].strip()
        return title, body.strip()
    return title, text.strip()


def prefix_for(slug: str) -> str:
    if slug == "index":
        return ""
    return "../" * slug.count("/")


def render_nav(current: str, prefix: str) -> str:
    parts = []
    for section, items in NAV:
        links = []
        for slug, label in items:
            href = prefix + slug + ".html"
            current_attr = ' aria-current="page"' if slug == current else ""
            links.append(f'<a href="{href}"{current_attr}>{label}</a>')
        parts.append(f'<div class="nav-group"><h2>{section}</h2>{"".join(links)}</div>')
    return "\n".join(parts)


def page(slug: str, title: str, section: str, body_html: str, toc_html: str):
    prefix = prefix_for(slug)
    description = seo.description_for(slug, title, SUMMARIES)
    idx = next((i for i, (s, _) in enumerate(FLAT) if s == slug), None)
    pager = ""
    if idx is not None:
        prev_html = ""
        next_html = ""
        if idx > 0:
            ps, pl = FLAT[idx - 1]
            prev_html = f'<a href="{prefix}{ps}.html" rel="prev">← {pl}</a>'
        if idx + 1 < len(FLAT):
            ns, nl = FLAT[idx + 1]
            next_html = f'<a href="{prefix}{ns}.html" rel="next">{nl} →</a>'
        pager = f'<nav class="pager" aria-label="Page">{prev_html}{next_html}</nav>'
    home = prefix + "index.html"
    crumbs = seo.breadcrumb_nav(slug, title, section, prefix)
    html = f"""<!DOCTYPE html>
<html lang="en" data-theme="brand">
<head>
{seo.head_meta(slug=slug, title=title, section=section, description=description, prefix=prefix, indexable=True)}
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500;700&family=Space+Grotesk:wght@500;600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="{prefix}css/docs.css">
</head>
<body>
  <div class="dot-matrix" aria-hidden="true"></div>
  <div class="noise" aria-hidden="true"></div>
  <header class="site-nav">
    <div class="site-nav-inner">
      <a class="brand" href="{home}">
        <img src="{prefix}graphics/pdc-logo.png" width="36" height="36" alt="Privacy Data Coin">
        <span><strong>Privacy Data Coin</strong></span>
      </a>
      <nav class="site-links" aria-label="Primary">
        <a href="https://privacydatacoin.com/">Home</a>
        <a href="https://privacydatacoin.com/news.html">News</a>
        <a href="https://trade.privacydatacoin.com/">Trade</a>
        <a href="https://privacydatacoin.com/oracle.html">Oracle</a>
        <a href="https://privacydatacoin.com/protocol.html">Protocol</a>
        <a href="{home}" aria-current="page">Docs</a>
      </nav>
      <div class="site-cta">
        <button class="docs-menu" type="button" data-docs-menu aria-expanded="false">Topics</button>
        <button class="menu-btn" type="button" data-menu aria-expanded="false">Menu</button>
        <a class="btn" href="https://privacydatacoin.com/download.html">Download</a>
        <a class="btn" href="https://explorer.privacydatacoin.com/">Explorer</a>
      </div>
    </div>
    <div class="mobile-panel" data-mobile>
      <a href="https://privacydatacoin.com/">Home</a>
      <a href="https://privacydatacoin.com/news.html">News</a>
      <a href="https://trade.privacydatacoin.com/">Trade</a>
      <a href="https://privacydatacoin.com/oracle.html">Oracle</a>
      <a href="https://privacydatacoin.com/protocol.html">Protocol</a>
      <a href="{home}" aria-current="page">Docs</a>
      <a href="https://privacydatacoin.com/download.html">Download</a>
      <a href="https://explorer.privacydatacoin.com/">Explorer</a>
      <button type="button" data-docs-menu-mobile>Browse topics</button>
    </div>
  </header>
  <div class="backdrop" data-backdrop hidden></div>
  <div class="shell">
    <aside class="sidebar" aria-label="Documentation topics">
      <a class="release-chip" data-doc-release href="https://github.com/PrivacyDataCoin-Project/PDC/releases/latest"><span data-doc-version>v3.0.0</span></a>
      <input class="search" type="search" placeholder="Filter topics" aria-label="Filter topics">
      {render_nav(slug, prefix)}
    </aside>
    <div class="content-grid">
      <main>
        <article{'' if slug == 'index' else ' itemscope itemtype="https://schema.org/TechArticle"'}>
          {crumbs}
          <p class="kicker">{section}</p>
          <h1{'' if slug == 'index' else ' itemprop="headline"'}>{title}</h1>
          <div{'' if slug == 'index' else ' itemprop="articleBody"'}>
          {body_html}
          </div>
          {pager}
          <p class="footer">Edition <a data-doc-release href="https://github.com/PrivacyDataCoin-Project/PDC/releases/latest"><span data-doc-version>v3.0.0</span></a> follows the latest release of <a href="https://github.com/PrivacyDataCoin-Project/PDC">PrivacyDataCoin-Project/PDC</a>. The manual is <a href="https://docs.privacydatacoin.com/">docs.privacydatacoin.com</a>. The public site is <a href="https://privacydatacoin.com/">privacydatacoin.com</a>. The block explorer is <a href="https://explorer.privacydatacoin.com/">explorer.privacydatacoin.com</a>.</p>
        </article>
      </main>
      <aside class="toc" aria-label="On this page">
        <h2>On this page</h2>
        {toc_html or "<p>This page is short.</p>"}
      </aside>
    </div>
  </div>
  <script src="{prefix}js/docs.js" defer></script>
  <script src="{prefix}js/release.js" defer></script>
</body>
</html>
"""
    out = ROOT / "index.html" if slug == "index" else ROOT / f"{slug}.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")


def main():
    converter = markdown.Markdown(extensions=["tables", "fenced_code", "sane_lists", "toc"])
    built_slugs = ["index"]
    home_title, home_body = parse(CONTENT / "index.md")
    cards = ['<div class="cards">']
    for section, items in NAV:
        slug, label = items[0]
        cards.append(
            f'<a class="card" href="{slug}.html"><span>{section}</span><strong>{label}</strong><p>{SUMMARIES[slug]}</p></a>'
        )
    cards.append("</div>")
    home_html = re.sub(r"\.md(?=[\"#)])", ".html", converter.convert(home_body))
    home_toc = "<ul>" + "".join(
        f'<li><a href="{items[0][0]}.html">{section}</a></li>' for section, items in NAV
    ) + "</ul>"
    page("index", home_title, "Privacy Data Coin", home_html + "\n" + "\n".join(cards), home_toc)
    for section, items in NAV:
        for slug, _label in items:
            path = CONTENT / f"{slug}.md"
            title, body = parse(path)
            converter.reset()
            html = re.sub(r"\.md(?=[\"#)])", ".html", converter.convert(body))
            page(slug, title, section, html, converter.toc)
            built_slugs.append(slug)
    # Preserve old bookmarks outside the primary nav
    legacy_pages = 0
    for slug, section in (
        ("use/wallets", "Use"),
        ("use/messenger", "Use"),
        ("wallets/overview", "Wallets"),
        ("wallets/desktop", "Wallets"),
    ):
        path = CONTENT / f"{slug}.md"
        if not path.is_file():
            continue
        title, body = parse(path)
        converter.reset()
        html = re.sub(r"\.md(?=[\"#)])", ".html", converter.convert(body))
        page(slug, title, section, html, converter.toc)
        built_slugs.append(slug)
        legacy_pages += 1
    seo.write_robots(ROOT)
    seo.write_sitemap(ROOT, built_slugs)
    print("built", len(built_slugs), "pages + sitemap/robots")


if __name__ == "__main__":
    main()

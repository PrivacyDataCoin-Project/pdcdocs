# PDC documentation

English manual for Privacy Data Coin. The section order follows a full-chain manual: learn the protocol, use a wallet, build and integrate, mine, stake, and read the source. The colors, the logo, and the facts are PDC.

Protocol numbers come from the PDC source, especially `src/currency_core/currency_config.h`. The edition number and the install files follow the latest GitHub release of [PrivacyDataCoin-Project/PDC](https://github.com/PrivacyDataCoin-Project/PDC). The published manual reads that release on each page load. The release current at the time of this writing is [v3.0.0](https://github.com/PrivacyDataCoin-Project/PDC/releases/tag/v3.0.0) (19 October 2026).

## Read it

The rendered manual is published at https://docs.privacydatacoin.com/.

The markdown sources are in `content/`. The HTML next to this README is what that address serves. The layout matches [privacydatacoin.com](https://privacydatacoin.com/) (Space Grotesk / Inter / JetBrains Mono). Regenerate after an edit:

```text
python3 -m pip install markdown
python3 tools/build.py
```

`tools/build.py` also writes `robots.txt` and `sitemap.xml` for search engines.

Public references used in the manual:

- Site: https://privacydatacoin.com/
- Explorer: https://explorer.privacydatacoin.com/
- Trade: https://trade.privacydatacoin.com/
- Trade API: https://api.trade.privacydatacoin.com/
- Oracle: https://oracle.privacydatacoin.com/
- Asset whitelist: https://api.privacydatacoin.com/assets_whitelist.json
- Current binaries: https://github.com/PrivacyDataCoin-Project/PDC/releases/latest

## Sections

- Learn: what PDC is, how a transfer works, FAQ
- Use: install the current release, security, troubleshooting
- Wallets: GUI and iOS (`content/wallets/`)
- Matrix: PDC Messenger (`content/matrix/`) — [matrix.privacydatacoin.com](https://matrix.privacydatacoin.com)
- Trade: exchange, Bridge (BTCX / ARQX / PDCX), Trade API, PDC Companion (`content/trade/`)
- Oracle: signed USD feed, paid attestation, and API (`content/oracle/`)
- Build: compile the tree, node RPC, assets, aliases, escrow and swaps
- Mine: RandomARQ and stratum port 19777
- Stake: online staking and the Zarcanum rules
- Tools: TIP Bot (Telegram + Matrix) and Funding (community crowdfunding)
- Code: the parameter table and a map of the source tree

---
title: Trade API
---

Public HTTP API for [Trade](https://trade.privacydatacoin.com/). Base URL:

```text
https://api.trade.privacydatacoin.com
```

No API key is required for the market, fee-schedule, and bridge **read** endpoints below. Creating deposits, withdrawals, and orders requires a JWT from Companion (`verify_message`) or a bot key (operators).

User flows: [Trade](trade.md) (exchange) and [Bridge](bridge.md) (wrap / unwrap).

## Price monitors (ticker)

Exchange-style human floats for third-party monitors:

```bash
curl -s 'https://api.trade.privacydatacoin.com/api/ticker?symbol=PDC-BTCX'
curl -s 'https://api.trade.privacydatacoin.com/api/ticker?symbol=ARQX-BTCX'
```

| Field | Meaning |
| --- | --- |
| `symbol` | e.g. `PDC-BTCX`, `ARQX-BTCX` |
| `last` | Last fill price (null if no trades yet) |
| `bid` / `ask` | Best open book prices |
| `high24h` / `low24h` / `volume24hBase` / `change24hPct` | 24h stats when fills exist |
| `lastUsd` | Last fill converted with the USD reference feed (null if no fill) |
| `timestamp` | Unix seconds |

Also accepted: `symbol=PDC/BTCX`, or `offer=PDC&want=BTCX`, or full `offerAssetId` / `wantAssetId` hex. Without query parameters the response is `{ "tickers": [ … ] }` for known pairs.

USD reference (spot-style, not necessarily last trade):

```bash
curl -s 'https://api.trade.privacydatacoin.com/api/prices/usd'
```

Example shape: `{ "updatedAt": …, "prices": { "PDC": …, "BTCX": …, "ARQX": …, "ETH": …, … }, "source": "oracle", "status": "verified", "sequence": … }` — when Trade consumes the signed [Oracle](../oracle/oracle.md) feed, `source` is `oracle`. `BTCX` tracks Bitcoin USD from primary CEX (quorum 3); `PDC` comes from the Trade book path via Oracle; majors/privacy (ETH, BNB, SOL, ZEC, XMR, DASH) appear when published. Direct publisher: `https://oracle.privacydatacoin.com/api/prices/usd` ([Oracle API](../oracle/api.md)); methodology: [oracle.privacydatacoin.com/methodology](https://oracle.privacydatacoin.com/methodology).

## Market data (public)

| Method | Path | Notes |
| --- | --- | --- |
| GET | `/api/ticker` | Human ticker (preferred for monitors) |
| GET | `/api/prices/usd` | USD reference map |
| GET | `/api/tokens` | Trade allowlist (`scope=trade` default) |
| GET | `/api/dex/pairs` | Listed pairs |
| GET | `/api/book` | Open book snapshot (scaled internal prices) |
| GET | `/api/orders?status=open&…` | Open orders (filter by asset ids) |
| GET | `/api/orders/get-pair-stats?offerAssetId=&wantAssetId=` | 24h OHLC / volume (scaled integers) |
| GET | `/api/orders/get-trades?offerAssetId=&wantAssetId=&limit=` | Recent fills |
| GET | `/api/orders/get-candles?…&period=3600` | Candles (`period` in seconds) |

Asset ids (mainnet, from Trade allowlist):

| Ticker | Decimals | Asset id |
| --- | --- | --- |
| PDC | 12 | `d6329b5b1f7c0805b5c345f4957554002a2f557845f64d7645dae0e051a6498a` |
| BTCX | 8 | `c2bf0410873b49ec7e7dd19d62bca9625d80cd3123670a67b48d997d3127426d` |
| ARQX | 9 | `d59ca1b363d5f44e0f087d9549b734815fbc2a6ab49ef0a877ccd910b1a1b9c3` |
| PDCX | 8 | `5292b7984565b21d47e456c381973b700738b9819f9e96b841f68cfa116774bd` |

Prefer `/api/ticker` when you need human floats. Pair-stats and book still use the internal quote-per-base scale (×10¹² with decimal adjustment).

## Trading fees (public)

| Method | Path | Notes |
| --- | --- | --- |
| GET | `/api/trade-fees` | Schedule: flat + bps, treasury, mint sweep policy |
| GET | `/api/trade-fees/quote` | Preview fee for an offer/want slice |

Hub wrap markets (e.g. `ARQX-BTCX`): taker pays **0.01 PDC flat + 0.10%** of PDC notional to the fee treasury; maker **0**. Native `*/PDC` markets: trading fee **0**. Ionic gas (~0.01 PDC) is separate. User flow: [Trade](trade.md#trading-fees).

Authenticated: `GET/POST /api/matches/:id/fee` after the taker transfers PDC and submits `feeTxId`.

## Bridge (public reads)

Catalog and BTCX (unprefixed paths stay first-class):

| Method | Path | Notes |
| --- | --- | --- |
| GET | `/api/bridge/assets` | Registry tabs: slug, native/wrap tickers, decimals, `bridgeEnabled`, asset id |
| GET | `/api/bridge/status` | BTCX: mins, fees, pause flags, peg, TSS summary, bitcoind / Esplora sync |
| GET | `/api/bridge/history?limit=&type=mint\|burn\|all` | Redacted BTCX mint/burn list |
| GET | `/api/bridge/deposit/by-txid/:txid` | Redacted BTCX deposit lookup |

Universal wrap slug API (`slug` from assets, e.g. `arqx`; `btcx` aliases BTCX):

| Method | Path | Notes |
| --- | --- | --- |
| GET | `/api/bridge/:slug/status` | Per-wrap status (ARQX: confirmations, pool/liability, watcher) |
| GET | `/api/bridge/:slug/history` | Redacted mint/burn for that wrap |
| POST | `/api/bridge/:slug/deposit` | JWT — create invoice |
| GET | `/api/bridge/:slug/deposits` | JWT — list |
| POST | `/api/bridge/:slug/withdraw` | JWT — start withdraw |
| GET | `/api/bridge/:slug/withdrawals` | JWT — list |
| GET | `/api/bridge/pdcx/status` | PDC↔PDCX same-L1 wrap (Oracle fee CA) |

BTCX also keeps the legacy unprefixed write paths (`POST /api/bridge/deposit`, `…/withdraw`, `…/withdrawals/:id/burn`). PDCX uses `/api/bridge/pdcx/*`.

Always treat Bridge status as the source of truth for deposit/withdraw availability. User steps: [Bridge](bridge.md).

## Auth and writes (summary)

| Area | Auth | Examples |
| --- | --- | --- |
| Market reads | none | ticker, prices, book, pair-stats |
| Fee schedule | none | `/api/trade-fees`, quote |
| Bridge reads | none | assets, status, history |
| Bridge deposit / withdraw / burn | JWT | slug routes or BTCX unprefixed |
| Orders / matches / fee attach | JWT or bot key | `POST /api/orders`, take / fill / cancel, `POST /api/matches/:id/fee` |
| Token / alias sync | admin key (or true local peer) | `POST /api/tokens/sync` — spoofed `X-Forwarded-For` is **not** enough |

Wallet JWT: [PDC Companion](companion.md) signs a challenge; Trade verifies via wallet RPC `verify_message`. Bot keys: see the Trade backend `docs/bot-api.md` in [pdc_trade_backend](https://github.com/PrivacyDataCoin-Project/pdc_trade_backend).

There is **no** public `emit_asset` / mint endpoint. Wrap mint happens only in the bridge worker after a confirmed native deposit (and custody rules).

## Health

```bash
curl -s 'https://api.trade.privacydatacoin.com/api/health'
```

## Related

- [Trade](trade.md) — exchange, fees, Easy Swap
- [Bridge](bridge.md) — BTCX + ARQX + PDCX wrap flows
- [Oracle](../oracle/oracle.md) — signed USD publisher
- [Confidential assets](../build/assets.md) — on-chain tokens
- [Node RPC](../build/rpc.md) — local `pdcd` JSON-RPC (not the Trade HTTP API)

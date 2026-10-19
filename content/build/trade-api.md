---
title: Trade API
---

Public HTTP API for [Trade](https://trade.privacydatacoin.com/). Base URL:

```text
https://api.trade.privacydatacoin.com
```

No API key is required for the market and bridge **read** endpoints below. Creating deposits, withdrawals, and orders requires a JWT from Companion (`verify_message`) or a bot key (operators).

User-facing bridge steps: [Trade and BTC bridge](../use/trade.md).

## Price monitors (ticker)

Exchange-style human floats for third-party monitors:

```bash
curl -s 'https://api.trade.privacydatacoin.com/api/ticker?symbol=PDC-BTCX'
```

| Field | Meaning |
| --- | --- |
| `symbol` | e.g. `PDC-BTCX` |
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

Example shape: `{ "updatedAt": …, "prices": { "PDC": 0.99…, "BTCX": 80881 } }` — `BTCX` tracks Bitcoin USD; `PDC` is derived for monitoring.

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

Asset ids for mainnet PDC and BTCX:

| Ticker | Decimals | Asset id |
| --- | --- | --- |
| PDC | 12 | `d6329b5b1f7c0805b5c345f4957554002a2f557845f64d7645dae0e051a6498a` |
| BTCX | 8 | `c2bf0410873b49ec7e7dd19d62bca9625d80cd3123670a67b48d997d3127426d` |

Prefer `/api/ticker` when you need human floats. Pair-stats and book still use the internal quote-per-base scale (×10¹² with decimal adjustment).

## Bridge (public reads)

| Method | Path | Notes |
| --- | --- | --- |
| GET | `/api/bridge/status` | Live mins, fees, pause flags, peg (`pegOk`, supplies), TSS summary, bitcoind sync |
| GET | `/api/bridge/history?limit=&type=mint\|burn\|all` | Redacted mint/burn list |
| GET | `/api/bridge/deposit/by-txid/:txid` | Redacted deposit lookup |

Always treat Bridge status as the source of truth for deposit/withdraw availability (including hard-block while Bitcoin is in IBD).

## Auth and writes (summary)

| Area | Auth | Examples |
| --- | --- | --- |
| Market reads | none | ticker, prices, book, pair-stats |
| Bridge reads | none | status, history |
| Bridge deposit / withdraw / burn | JWT | `POST /api/bridge/deposit`, `…/withdraw`, `…/withdrawals/:id/burn` |
| Orders / matches | JWT or bot key | `POST /api/orders`, take / fill / cancel |
| Token / alias sync | admin key (or true local peer) | `POST /api/tokens/sync` — spoofed `X-Forwarded-For` is **not** enough |

Wallet JWT: [PDC Companion](../use/companion.md) signs a challenge; Trade verifies via wallet RPC `verify_message`. Bot keys: see the Trade backend `docs/bot-api.md` in [pdc_trade_backend](https://github.com/PrivacyDataCoin-Project/pdc_trade_backend).

There is **no** public `emit_asset` / mint endpoint. BTCX mint happens only in the bridge worker after a confirmed Bitcoin deposit (and custody rules).

## Health

```bash
curl -s 'https://api.trade.privacydatacoin.com/api/health'
```

## Related

- [Trade and BTC bridge](../use/trade.md) — user flow
- [Confidential assets](assets.md) — on-chain tokens
- [Node RPC](rpc.md) — local `pdcd` JSON-RPC (not the Trade HTTP API)

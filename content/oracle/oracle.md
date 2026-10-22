---
title: Oracle
---

[PDC Oracle](https://oracle.privacydatacoin.com/) is the signed **USD price publisher** for Privacy Data Coin. Trade and other clients can read a Trade-compatible price book and verify that it was signed by the pinned Oracle public key.

Oracle is **off-chain**. It is not a Solidity contract on PDC L1 (the chain has no EVM). Native on-chain `oracle_update` is a future daemon track, not required to use the feed today.

Dashboard and JSON live at **https://oracle.privacydatacoin.com**. Integrators: [Oracle API](api.md). Trade USD path: [Trade API](../trade/api.md). **Paid** CA tip → EVM attestation: [Paid attestation](paid-attestation.md).

## Two products

| Product | Cost | Start here |
| --- | --- | --- |
| Signed USD book (`/api/prices/usd`) | Free to read | This page + [API](api.md) |
| CA tip → EVM attestation (`/api/sidechain/*` + on-chain fee) | **Paid** (0.01 fee token / update) | [Paid attestation](paid-attestation.md) |

## What it is for

| Audience | Use |
| --- | --- |
| Traders | USD subtitles and reference prices on [Trade](https://trade.privacydatacoin.com/) (via Trade’s `/api/prices/usd`) |
| Monitors / bots | Pull `GET https://oracle.privacydatacoin.com/api/prices/usd` and verify the signature |
| Integrators / bridges | Optional **paid** tip attestation — signed CA tip + supply for EVM ([Paid attestation](paid-attestation.md)) |
| Operators | Run or consume the publisher; pin the public key; never trust unsigned books as “verified” |

Oracle aggregates external spot venues (median), applies bounds and freshness rules, then **Ed25519-signs** each successful publish. Consumers trust the **signature + pinned pubkey**, not the HTTPS path alone.

Full public methodology: [oracle.privacydatacoin.com/methodology](https://oracle.privacydatacoin.com/methodology) (also `GET /api/methodology`).

## Quick start (users)

1. Open [oracle.privacydatacoin.com](https://oracle.privacydatacoin.com/) — dashboard shows the latest feed status and sequence.
2. Or open prices directly: [Prices API](https://oracle.privacydatacoin.com/api/prices/usd).
3. Read how prices are built: [Methodology](https://oracle.privacydatacoin.com/methodology).
4. On Trade, USD figures come from Trade’s own `/api/prices/usd`, which can consume this Oracle when enabled (`source=oracle` in the JSON).

You do **not** need Companion or a wallet to read Oracle prices. Companion is only for Trade login, Bridge, and swaps.

## Price book (what you see)

Typical tickers in `prices` (human USD) and related `pairs`:

| Key / pair | Meaning | How it is priced |
| --- | --- | --- |
| `BTC` / `BTCX` (`BTC_USD`, `BTCX_USD`) | Bitcoin / wrapped BTC USD | Median of **primary CEX** (below); Gecko/CMC only if that pair’s primary count is 0 |
| `ETH` / `BNB` / `SOL` | Major spot USD | Same primary CEX median (+ per-pair backup when primary=0) |
| `ZEC` / `XMR` / `DASH` | Privacy cohort USD | Same pattern; soft-skip delisted/geofenced venues |
| `PDC` (`PDC_USD`) | Privacy Data Coin USD | **Trade open book** BTCX↔PDC × `BTCX_USD` (`trade_book`) — not a fixed env default |
| `ARQX` (`ARQX_USD`) | Wrapped Arqma USD | Median of CoinGecko + CoinMarketCap + Trade book BTCX↔ARQX when available |
| `PDCX` / `PDCx` | Oracle fee CA | 1:1 with PDC when published (fee wrap, not a CEX spot) |

Cross rates also appear under `pairs` (e.g. `PDC_BTCX`, `ARQX_BTCX`). Prefer live JSON over any number hard-coded in this page.

### Primary venues and quorum

**Primary exchanges** (authoritative samples for BTC/BTCX and the major/privacy USD pairs):

Binance, Kraken, Coinbase, Bitstamp, OKX, Bybit.

| Rule | Default |
| --- | --- |
| Feed `status=verified` | BTC **primary** quorum ≥ **3** venues (`ORACLE_MIN_SOURCES`) |
| Majors pair quorum (ETH/BNB/SOL) | **3** (diagnostics; missing majors alone do not degrade the feed) |
| Privacy pair quorum (ZEC/XMR/DASH) | **2** (`ORACLE_MIN_SOURCES_PRIVACY`) |
| CoinGecko / CoinMarketCap | **Backup only** when that pair’s `primarySucceeded === 0` (do not count toward BTC verified quorum) |

### Status

| `status` | Meaning |
| --- | --- |
| `verified` | Required pairs present and BTC primary quorum met; signature present |
| `degraded` | Published with reduced source quality (e.g. BTC backup-only, optional ARQX miss) — still signed; treat with care |
| `unavailable` | Do not treat as a usable verified book |

Also check `sequence` (monotonic), `updatedAt` (unix seconds), and `maxAgeSec` (default **120**). Stale feeds must be rejected by clients.

## How Trade uses Oracle

```text
Primary CEX (Binance, Kraken, Coinbase, Bitstamp, OKX, Bybit)
  → Oracle publisher (median + quorum + Ed25519 sign)
  → Trade backend (verify) → Trade UI USD labels
```

1. Oracle publishes `GET /api/prices/usd` with `signature` + `publicKey`.
2. Trade (when `ORACLE_FEED_ENABLED`) fetches that URL, verifies Ed25519 against a **pinned** `ORACLE_PUBLIC_KEY_HEX`, checks age and sequence.
3. Trade re-exposes `GET https://api.trade.privacydatacoin.com/api/prices/usd` with additive `source=oracle` (and `status` / `sequence` when present).
4. Order-book **mark / last** on the exchange still comes from the book itself — Oracle is for USD reference, not for replacing Ionic Swap fill prices.

If Oracle verification fails and legacy fallback is off, Trade should fail closed (e.g. **503**), not invent zeros.

## PDCx — fee asset for oracle attestation

Some Oracle / sidechain attestation flows charge fees in **PDCX** (on-chain ticker **PDCx**), a confidential asset on PDC. This is a **same-L1** wrap of native PDC (not Bitcoin / Arqma).

| Item | Value |
| --- | --- |
| Wrap | Native **PDC ↔ PDCX** 1:1 on Trade Bridge (`/bridge`, tab PDC→PDCX) |
| Asset id (mainnet) | `5292b7984565b21d47e456c381973b700738b9819f9e96b841f68cfa116774bd` |
| Decimals | PDC 12 · PDCX 8 (human rate stays 1:1) |
| Status | `GET https://api.trade.privacydatacoin.com/api/bridge/pdcx/status` |
| Mainnet (2026-10-22) | `mode=live`, `emitBurnEnabled=true`, mint and burn E2E verified |

`feeRecipient` for EVM attestation token fees is the **treasury / @dev** pool wallet — not the wrap mint/custody address. See the publisher repo docs under `oracle-sidechain-evm`.

### User steps (get PDCX)

1. Install [PDC Companion](../trade/companion.md) and unlock your wallet (desktop `Pdc` from the [current release](https://github.com/PrivacyDataCoin-Project/PDC/releases/latest)).
2. Open [Bridge](https://trade.privacydatacoin.com/bridge) → **PDC→PDCX**.
3. Create a deposit invoice and send **native PDC** to the custody address shown (confirmations from status — currently **10**).
4. When mint completes, PDCX appears in the wallet (whitelist / Companion balances).
5. To unwrap: burn PDCX on Bridge → attach the burn tx → receive native PDC (worker pays after on-chain verify).

Confirm `depositEnabled` / `withdrawEnabled` on status before sending funds. Details: [Bridge](../trade/bridge.md).

### Sidechain tip attestation (paid, live)

Mainnet Oracle exposes disclosable CA tip attestation over HTTP and a signed EVM report. That path is **additive** — it does not replace the signed USD book.

| Item | Mainnet (2026-10-22) |
| --- | --- |
| Status | Enabled (`sidechainAttestation` on `/api/health`) |
| Fee | `1000000` atomic = **0.01** (8 decimals) |
| L1 fee CA | PDCx (wrap above) |
| Payment gate | EVM `PdcSidechainAttestationTokenFee` (`transferFrom` after `approve`) — not a deduction on bare HTTP `GET` |
| Contract | Unpaused on private Clique soak (operator host; not a public L2) |

Full flow, user wrap steps, and integrator `curl` + contract calls: **[Paid attestation](paid-attestation.md)**. Endpoints: [Oracle API](api.md#paid-sidechain-attestation).

## Safety

- Pin the Oracle **public key** in any production consumer. Do not rotate trust to whatever `publicKey` field appears in a random response without an out-of-band pin.
- Reject feeds older than `maxAgeSec` (or your stricter limit).
- Reject non-increasing `sequence` (replay).
- External venues can be wrong even when `status=verified` — multi-venue median reduces, but does not eliminate, source risk.
- Never paste seed phrases into the Oracle site or Trade.
- Admin refresh (`POST /api/admin/refresh`) is operator-only and must not be public.

## Related

- Live site: [oracle.privacydatacoin.com](https://oracle.privacydatacoin.com/)
- [Methodology](https://oracle.privacydatacoin.com/methodology) — venues, quorum, pair rules (`GET /api/methodology`)
- [Paid attestation](paid-attestation.md) — how the paid path works and how to use it
- [Oracle API](api.md) — endpoints, fields, verification checklist
- [Trade](../trade/trade.md) — exchange UI
- [Trade API](../trade/api.md) — Trade `/api/prices/usd`
- [Bridge](../trade/bridge.md) — wraps including PDC→PDCX
- Publisher repo: [PrivacyDataCoin-Project/oracle](https://github.com/PrivacyDataCoin-Project/oracle)

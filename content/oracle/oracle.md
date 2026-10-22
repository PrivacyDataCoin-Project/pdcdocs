---
title: Oracle
---

[PDC Oracle](https://oracle.privacydatacoin.com/) is the signed **USD price publisher** for Privacy Data Coin. Trade and other clients can read a Trade-compatible price book and verify that it was signed by the pinned Oracle public key.

Oracle is **off-chain**. It is not a Solidity contract on PDC L1 (the chain has no EVM). Native on-chain `oracle_update` is a future daemon track, not required to use the feed today.

Dashboard and JSON live at **https://oracle.privacydatacoin.com**. Integrators: [Oracle API](api.md). Trade USD path: [Trade API](../trade/api.md).

## What it is for

| Audience | Use |
| --- | --- |
| Traders | USD subtitles and reference prices on [Trade](https://trade.privacydatacoin.com/) (via Trade’s `/api/prices/usd`) |
| Monitors / bots | Pull `GET https://oracle.privacydatacoin.com/api/prices/usd` and verify the signature |
| Operators | Run or consume the publisher; pin the public key; never trust unsigned books as “verified” |

Oracle aggregates external spot venues (median), applies bounds and freshness rules, then **Ed25519-signs** each successful publish. Consumers trust the **signature + pinned pubkey**, not the HTTPS path alone.

## Quick start (users)

1. Open [oracle.privacydatacoin.com](https://oracle.privacydatacoin.com/) — dashboard shows the latest feed status and sequence.
2. Or open prices directly: [Prices API](https://oracle.privacydatacoin.com/api/prices/usd).
3. On Trade, USD figures come from Trade’s own `/api/prices/usd`, which can consume this Oracle when enabled (`source=oracle` in the JSON).

You do **not** need Companion or a wallet to read Oracle prices. Companion is only for Trade login, Bridge, and swaps.

## Price book (what you see)

Typical tickers in `prices` (human USD):

| Key | Meaning |
| --- | --- |
| `BTCX` | Wrapped Bitcoin USD (tracks BTC) |
| `PDC` | Privacy Data Coin USD |
| `ARQX` | Wrapped Arqma USD |
| `PDCX` / `PDCx` | Oracle fee CA (1:1 with PDC when published) |

Cross rates also appear under `pairs` (e.g. `PDC_BTCX`, `BTC_USD`). Prefer live JSON over any fixed number in this page.

### Status

| `status` | Meaning |
| --- | --- |
| `verified` | Quorum / multi-venue rules passed; signature present |
| `degraded` | Published but with reduced source quality — still signed; treat with care |
| `unavailable` | Do not treat as a usable verified book |

Also check `sequence` (monotonic), `updatedAt` (unix seconds), and `maxAgeSec` (default **120**). Stale feeds must be rejected by clients.

## How Trade uses Oracle

```text
Venues (Binance, Kraken, …) → Oracle publisher (sign) → Trade backend (verify) → Trade UI USD labels
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

### Sidechain tip attestation (optional)

When enabled, Oracle also exposes disclosable CA tip attestation over HTTP (`GET /api/sidechain/attestation`) and related EVM reports. That path is **additive** — it does not replace the signed USD book. Fee payment for those flows uses **PDCX** (see above). Endpoints: [Oracle API](api.md).

## Safety

- Pin the Oracle **public key** in any production consumer. Do not rotate trust to whatever `publicKey` field appears in a random response without an out-of-band pin.
- Reject feeds older than `maxAgeSec` (or your stricter limit).
- Reject non-increasing `sequence` (replay).
- External venues can be wrong even when `status=verified` — multi-venue median reduces, but does not eliminate, source risk.
- Never paste seed phrases into the Oracle site or Trade.
- Admin refresh (`POST /api/admin/refresh`) is operator-only and must not be public.

## Related

- [Oracle API](api.md) — endpoints, fields, verification checklist
- [Trade](../trade/trade.md) — exchange UI
- [Trade API](../trade/api.md) — Trade `/api/prices/usd`
- [Bridge](../trade/bridge.md) — wraps including PDC→PDCX
- Publisher repo: [PrivacyDataCoin-Project/oracle](https://github.com/PrivacyDataCoin-Project/oracle)

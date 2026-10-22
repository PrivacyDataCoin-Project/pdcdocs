---
title: Oracle API
---

Public HTTP API for [PDC Oracle](https://oracle.privacydatacoin.com/). Base URL:

```text
https://oracle.privacydatacoin.com
```

User overview and PDCx fee wrap: [Oracle](oracle.md). **Paid** tip path: [Paid attestation](paid-attestation.md). Trade’s mirrored USD book: [Trade API](../trade/api.md).

## Endpoints

| Method | Path | Auth | Notes |
| --- | --- | --- | --- |
| GET | `/api/health` | none | Liveness, sequence, status, feature flags |
| GET | `/api/prices/usd` | none | Trade-compatible book + signature envelope (**schemaVersion 1**) |
| GET | `/api/prices/feed` | none | Full signed document (same schema family as `/usd`) |
| GET | `/api/prices/streams` | none | Additive Streams-style report (schema v2) — not a replacement for `/usd` |
| GET | `/api/prices/evm` | none | Optional EVM Aggregator-style report — additive |
| GET | `/api/sidechain/attestation` | optional Bearer | CA tip attestation (when enabled) |
| GET | `/api/sidechain/evm` | optional Bearer | Sidechain→EVM report (when enabled) |
| POST | `/api/admin/refresh` | admin token | Force refresh — must stay private |

Trade consumers should use **`/api/prices/usd` (schema v1)** only for signature verification. Streams / EVM / sidechain are optional extras.

## Prices USD (schema v1)

```bash
curl -sS 'https://oracle.privacydatacoin.com/api/prices/usd'
```

| Field | Meaning |
| --- | --- |
| `schemaVersion` | `1` for the Trade feed |
| `updatedAt` | Unix seconds of the publish |
| `prices` | Map of ticker → USD float (`BTCX`, `PDC`, `ARQX`, …) |
| `pairs` | Explicit pair keys (`BTC_USD`, `PDC_BTCX`, …) |
| `status` | `verified` \| `degraded` \| `unavailable` |
| `sequence` | Monotonic publish counter |
| `maxAgeSec` | Soft freshness window (often `120`) |
| `signature` | Ed25519 signature (URL-safe base64) |
| `publicKey` | Publisher pubkey hex (pin out-of-band; do not blindly trust) |

### Live public key (pin this)

Current production publisher key (also returned in feed JSON):

```text
cc0e662c6d757856cda001744fbaa819d86aff26e1407695d90249c1a455c21e
```

Rotate only with an explicit ops process. Trade pins the same value as `ORACLE_PUBLIC_KEY_HEX`.

## Health

```bash
curl -sS 'https://oracle.privacydatacoin.com/api/health'
```

Useful fields: `ok`, `hasFeed`, `sequence`, `status`, `updatedAt`, `adminProtected`, optional `sidechainAttestation` / `sidechainRound`.

## Verification checklist (integrators)

1. Fetch `/api/prices/usd` over HTTPS.
2. Confirm `schemaVersion === 1`.
3. Verify Ed25519 `signature` over the **canonical payload** (field order / sorted maps as in the publisher `sign` module) with your **pinned** public key — not merely equality of the `publicKey` string in the body.
4. Reject if age `now - updatedAt` exceeds `maxAgeSec` (or your stricter `ORACLE_CONSUMER_MAX_AGE_SEC`).
5. Reject if `sequence` is not greater than the last accepted sequence.
6. Prefer `status=verified`; decide policy for `degraded`.

Reference consumer: Trade `oracle-feed` module in [pdc_trade_backend](https://github.com/PrivacyDataCoin-Project/pdc_trade_backend) (`docs/oracle-feed-integration.md`).

## Trade consumer flags (operators)

When Trade points at Oracle:

| Variable | Role |
| --- | --- |
| `ORACLE_FEED_ENABLED` | Prefer signed Oracle |
| `ORACLE_FEED_URL` | Default `https://oracle.privacydatacoin.com/api/prices/usd` |
| `ORACLE_PUBLIC_KEY_HEX` | Required pin (64 hex chars) |
| `ORACLE_LEGACY_FALLBACK` | If `1`, fall back to unsigned legacy on failure; else fail closed |
| `ORACLE_FEED_TIMEOUT_MS` | Fetch timeout (default 8000) |

Rollback: disable `ORACLE_FEED_ENABLED` and restart Trade.

## Additive APIs (optional)

| Path | Role |
| --- | --- |
| `/api/prices/streams` | Quorum + per-venue observations (schema v2) |
| `/api/prices/evm` | Optional secp256k1 Aggregator-style report for EVM tip contracts |
| `/api/sidechain/attestation` | Disclosable CA tip attestation (**paid** product; may require Bearer) |
| `/api/sidechain/evm` | Sidechain→EVM tip report for `updateAttestation` |

These must not replace schema v1 verification for Trade USD labels.

## Paid sidechain attestation

Narrative and user/integrator checklist: [Paid attestation](paid-attestation.md).

### Read (no L1 debit on GET)

```bash
curl -sS 'https://oracle.privacydatacoin.com/api/sidechain/attestation'
curl -sS 'https://oracle.privacydatacoin.com/api/sidechain/evm'
```

| Field (typical) | Meaning |
| --- | --- |
| `schemaVersion` | `ca-1` (attestation) / `ca-evm-1` (EVM report) |
| `height` / `roundId` | Tip height and publish round |
| `feeAmount` | Atomic fee (`1000000` = 0.01 @ 8 decimals on mainnet) |
| `feeAssetId` | L1 PDCx asset id (64 hex) |
| `feeRecipient` | EVM treasury / @dev — **not** wrap mint custody |
| `feeTreasuryPdcAddress` | L1 Px hint for treasury |
| `ethSignature` / `reportHash` | Inputs for on-chain `updateAttestation` |
| `signerAddress` | secp256k1 reporter |

Optional: `Authorization: Bearer <SIDECHAIN_API_TOKEN>` when the operator enabled a token.

### Pay (on-chain)

1. Acquire PDCx on L1 if needed: [Bridge PDC→PDCX](../trade/bridge.md#pdc--pdcx-oracle-fee-ca).
2. On the attestation EVM (private Clique soak for operators): `approve` the fee token, then `updateAttestation(...)`.
3. Confirm `latestTip()` on `PdcSidechainAttestationTokenFee`.

HTTP alone does **not** pull L1 PDCx. The contract `transferFrom` is the hard fee gate. Mainnet fee amount and go-live notes: publisher `docs/oracle-attestation-fee-go-live.md`.

## Related

- [Oracle](oracle.md) — user guide, status, PDCx fees
- [Paid attestation](paid-attestation.md) — how payment works end-to-end
- [Trade API](../trade/api.md) — Trade HTTP including `/api/prices/usd`
- [Bridge](../trade/bridge.md) — PDC→PDCX wrap
- Architecture / threat model: [oracle repo docs](https://github.com/PrivacyDataCoin-Project/oracle/tree/main/docs)

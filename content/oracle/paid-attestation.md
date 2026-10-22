---
title: Paid attestation
---

PDC Oracle has **two products**. Only the second is paid.

| Product | Endpoint | Payment |
| --- | --- | --- |
| Signed USD price book | `GET /api/prices/usd` | Free to read (verify the signature) |
| CA tip → EVM attestation | `GET /api/sidechain/*` + on-chain update | **Paid** — fee in PDCx / ERC-20 fee token |

This page describes the **paid** path: how it works, how to get PDCx, and how an integrator pays and publishes a tip on the attestation contract.

Overview of the free feed: [Oracle](oracle.md). HTTP fields: [Oracle API](api.md). Wrap native PDC: [Bridge](../trade/bridge.md#pdc--pdcx-oracle-fee-ca).

## How it works

```text
pdcd (tip height + CA current_supply)
        │
        ▼
  Oracle HTTP
  /api/sidechain/attestation   ← Ed25519 (ca-1), fee meta
  /api/sidechain/evm           ← secp256k1 report + ethSignature
        │
        ▼
  Caller pays fee on EVM (approve + updateAttestation)
        │
        ▼
  PdcSidechainAttestationTokenFee
  latestTip updated; fee → feeRecipient (treasury / @dev)
```

What is attested (privacy-safe, disclosable only):

- Tip `height` and tip hash
- Per-asset `current_supply` from `get_asset_info` (e.g. BTCX)

Private balances and confidential outs are **never** requested.

### Important: where the fee is enforced

| Layer | Role |
| --- | --- |
| Oracle HTTP | Returns a **signed report** and advertises `feeAmount` / `feeRecipient` / `feeAssetId`. A bare `GET` does **not** deduct L1 PDCx. |
| EVM contract | **Hard gate** — `updateAttestation` pulls the fee via ERC-20 `transferFrom` after you `approve`. |

Mainnet fee amount (atomic, 8 decimals): **`1000000` = 0.01** of the fee token. L1 payment asset id (PDCx):

```text
5292b7984565b21d47e456c381973b700738b9819f9e96b841f68cfa116774bd
```

`feeRecipient` is the **treasury / @dev** EVM wallet — **not** the PDCx wrap mint/custody address (`Px1wcg5…`).

Soak / private Clique (operator host): chainId **97421001**, RPC localhost only. There is **no public EVM L2** for PDC. See [Node RPC](../build/rpc.md).

## Get PDCx (users)

You need PDCx on PDC L1 if you will hold or trade the fee CA, or prepare for fee workflows that use that asset.

1. Install [PDC Companion](../trade/companion.md) and unlock a wallet ([current release](https://github.com/PrivacyDataCoin-Project/PDC/releases/latest)).
2. Open [Bridge](https://trade.privacydatacoin.com/bridge) → **PDC→PDCX**.
3. Check status first:

```bash
curl -sS 'https://api.trade.privacydatacoin.com/api/bridge/pdcx/status'
```

Expect `mode=live`, `ready=true`, `depositEnabled=true`. Note `depositAddress` and `minConfirmations` (currently **10**).

4. Create a deposit (Companion / Trade UI) and send **native PDC** to custody.
5. When mint completes, PDCx appears in the wallet.
6. Unwrap later: burn PDCx → attach burn tx → receive native PDC.

Explorer status page: [Bridge PDCx](https://explorer.privacydatacoin.com/bridge-pdcx). Details: [Bridge](../trade/bridge.md#pdc--pdcx-oracle-fee-ca).

## Integrator steps (pay + publish tip)

1. **Read health** — confirm sidechain attestation is on:

```bash
curl -sS 'https://oracle.privacydatacoin.com/api/health'
```

Look for `sidechainAttestation: true`.

2. **Fetch fee meta + signed report:**

```bash
curl -sS 'https://oracle.privacydatacoin.com/api/sidechain/attestation'
curl -sS 'https://oracle.privacydatacoin.com/api/sidechain/evm'
```

Useful fields on the EVM report: `roundId`, `height`, `assetIdHash`, `currentSupply`, `observedAt`, `reportHash`, `ethSignature`, `feeAmount`, `feeRecipient`, `signerAddress`.

Optional Bearer: if the operator set `SIDECHAIN_API_TOKEN`, send `Authorization: Bearer <token>`.

3. **On the attestation EVM** (private Clique for soak / operator deployment):

   - Hold enough of the contract’s `feeToken` (ERC-20; soak uses MockPdcx).
   - `approve(attestationContract, feeAmount)`.
   - Call `updateAttestation(roundId, height, assetId, currentSupply, observedAt, ethSignature)`.

4. **Verify** `latestTip()` on the contract matches the report you paid for.

Operator go-live / rollback scripts live in the publisher repo: `ops/attestation-fee/` and `docs/oracle-attestation-fee-go-live.md` in [PrivacyDataCoin-Project/oracle](https://github.com/PrivacyDataCoin-Project/oracle).

## What you get

- **Monetized tip attestation** for bridges and integrators that need a signed CA tip + supply on EVM.
- **Demand for PDCx** — wrap on Trade, optional book volume on PDC↔PDCX.
- **Treasury revenue** — fees go to `feeRecipient` (@dev / pool fee wallet).
- The **USD book stays free** and separately signed (schema v1).

## Safety

- Do not send seed phrases to Oracle, Trade, or Explorer.
- Pin Oracle’s Ed25519 pubkey for `/api/prices/usd`; treat sidechain signatures as a separate trust path (Ed25519 ca-1 / secp256k1 ca-evm-1).
- Never point `feeRecipient` at wrap mint custody.
- Reject stale `roundId` / height; the contract rejects non-increasing rounds (`StaleRound`).
- Private Clique RPC must stay localhost — not on the public IP.

## Related

- [Oracle](oracle.md) — free USD feed
- [Oracle API](api.md) — endpoints and fields
- [Bridge](../trade/bridge.md) — PDC→PDCX wrap
- Publisher docs: [oracle-sidechain-evm.md](https://github.com/PrivacyDataCoin-Project/oracle/blob/main/docs/oracle-sidechain-evm.md)

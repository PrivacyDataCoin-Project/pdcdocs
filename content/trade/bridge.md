---
title: Bridge
---

The Trade **Bridge** (`/bridge` on [trade.privacydatacoin.com](https://trade.privacydatacoin.com/)) wraps native coins into confidential assets on PDC and unwraps them again. Sign-in uses [PDC Companion](companion.md). Exchange trading after mint is on [Trade](trade.md).

Live limits, fees, pause flags, and confirmation counts always come from Bridge status JSON — prefer that over any fixed number here if they disagree. HTTP reads: [Trade API](api.md#bridge-public-reads).

## Wrap assets

Trade uses a **markets registry**: one Bridge portal, tabs from `GET /api/bridge/assets`. Adding a wrap does not require a new UI page.

| Native L1 | Wrap CA on PDC | Decimals | Bridge | Listed markets |
| --- | --- | --- | --- | --- |
| BTC | **BTCX** | 8 (sats) | Live (Bitcoin + TSS) | `PDC-BTCX` |
| ARQ | **ARQX** | 9 | Live (Arqma wallet-rpc) | `ARQX-BTCX` |
| PDC | **PDCX** | 8 | Live (same-L1 wrap) | Oracle fee CA |

Ordinary transfers of wrap assets hide amounts the same way other confidential assets do. Mint and burn keep the native reserve and circulating wrap matched **1:1** (per asset).

CA mint authority for cross-chain wraps shares the existing BTCX mint / remote mint-signer path. Users never call `emit_asset` from Trade.

## How the Bridge works

```text
Deposit:  native coin on L1  →  watcher + custody rules  →  mint wrap CA to your Px
Withdraw: burn wrap CA on PDC →  verify burn on-chain     →  pay native on L1
```

1. Connect Companion and open **Bridge**.
2. Pick a tab (**BTC→BTCX**, **ARQ→ARQX**, or **PDC→PDCX**).
3. Create a deposit invoice (or start a withdraw).
4. After mint, trade on [Trade](trade.md) Exchange / Easy Swap. Hub pairs may require a PDC taker fee before Accept.

## BTC → BTCX (Bitcoin)

### Peg and fees

| Direction | Peg | Who pays the Bitcoin miner fee |
| --- | --- | --- |
| Deposit BTC → mint BTCX | 1 sat received → 1 sat of BTCX minted | You, on the Bitcoin send |
| Withdraw BTCX → BTC | Burn amount **A** → pool outflows **A** | Taken from the burn: you receive **A − fee** |

The withdraw network fee is `withdrawFeeSats` on status (currently **800** sats). Example: burn `0.001` BTCX → receive `0.001 BTC − 800 sats` on Bitcoin L1. The reserve stays peg-neutral.

### Deposit

1. Create a **deposit invoice**. Note the Bitcoin address and the **OP_RETURN** hex for that invoice.
2. From your own Bitcoin wallet, send BTC to that address **and include the OP_RETURN memo**. Shared TSS deposit addresses require the memo so the invoice can be matched. Fiat on-ramps usually cannot attach OP_RETURN — buy to a personal wallet first, then send with the memo.
3. Wait for the confirmation count on Bridge status (mainnet currently uses **6** confirmations).
4. When the deposit is confirmed and the custody ceremony finishes, BTCX is minted to your PDC address.

**Minimums and maximums** come from status (`depositMinSats`, optional `depositMinUsd`, `depositMaxSats`). A typical floor is **10 000 sats** (0.0001 BTC) plus any USD floor shown as `depositMinUsd`.

**Fees on deposit:** you pay the normal Bitcoin network fee on your send. The bridge does not take an extra deposit cut.

### Withdraw

1. Enter a Bitcoin payout address and the BTCX amount (human units, 8 decimals).
2. Burn the BTCX on-chain (self-burn is preferred). Submit the burn transaction id in the UI — Trade verifies `burn_asset` / PUBLIC_BURN against your amount before any payout.
3. After the burn is verified, the TSS custody ceremony signs a Bitcoin payout and broadcasts it.

**Minimum withdraw** is `withdrawMinSats` on status — currently **10 000 sats** (**0.0001 BTCX**). Max and daily caps, when set, also appear on status. There is currently **no fixed withdraw delay** (`withdrawDelaySeconds` is **0**).

### Custody and sync

Live BTC custody uses a **threshold signature (TSS)** deposit address (status reports 2-of-3 Bridgeless-class controls). No single process holds a full spend key. Users only use the Trade UI and their own wallets; they do not run TSS nodes.

Production today is still an **operator-hosted** deployment (Trade + ceremony agents + bitcoind + pdcd). Public status exposes whether TSS is ready, `withdrawFeeSats`, peg fields (`tssPoolSats`, liability, `currentSupplySats`, `pegOk`), and bitcoind sync progress.

While Bitcoin is in initial block download (IBD), deposits and withdrawals can still proceed when the operator enables **Esplora** watch and broadcast fallback. Status may show IBD progress; treat pause flags and `depositEnabled` / `withdrawEnabled` as authoritative.

Status: `GET /api/bridge/status`. History: `GET /api/bridge/history`.

## ARQ → ARQX (Arqma wrap)

ARQX is wrapped Arqma on PDC (9 decimals). The Bridge tab **ARQ→ARQX** is live when `GET /api/bridge/arqx/status` shows `depositEnabled` / `withdrawEnabled`.

### Deposit

1. Create an invoice on the ARQX tab. The bridge allocates a **unique Arqma subaddress** (or integrated address) for that invoice — not a shared memo like Bitcoin OP_RETURN.
2. Send native **ARQ** from your Arqma wallet to that deposit address. Addresses are single-use; do not reuse a retired invoice address.
3. Wait for confirmations (`minConfirmations` on ARQX status — currently **10**). The UI shows confirmation progress.
4. After the watcher confirms the transfer and mint rules pass, **ARQX** is minted to your PDC address.

### Withdraw

1. Enter an Arqma payout address and the ARQX amount.
2. Burn ARQX on PDC and complete the Bridge withdraw flow (same burn-verify idea as BTCX; follow the UI for the wrap slug).
3. Native ARQ is paid out from the wrap custody wallet when reserves and status allow.

Pool / liability fields on ARQX status (`poolAtomic`, `liabilityAtomic`, `reservesOk`) are the peg check for this wrap. Public history: `GET /api/bridge/arqx/history`.

After minting ARQX, trade it on [Trade](trade.md) against **BTCX** (`ARQX-BTCX`).

## PDC → PDCX (oracle fee CA)

**PDCX** (on-chain ticker **PDCx**) is a 1:1 wrap of native PDC used as the Oracle attestation fee asset. It is **same-L1** (not Bitcoin / Arqma).

1. Open Bridge → **PDC→PDCX** (status: `GET /api/bridge/pdcx/status`).
2. Create a deposit and send **native PDC** to the custody address in the UI.
3. Wait for confirmations (`minConfirmations` on status — currently **10**). PDCX is minted 1:1 in human units.
4. Unwrap: burn PDCX on Bridge → receive native PDC.

Asset id: `5292b7984565b21d47e456c381973b700738b9819f9e96b841f68cfa116774bd`. Why it exists: [Oracle](../oracle/oracle.md#pdcx--fee-asset-for-oracle-attestation).

## Safety

- Never paste seed phrases into Trade or any website.
- BTC deposits: always use the invoice **OP_RETURN**. A plain send to the shared TSS address without the memo may not mint.
- ARQ deposits: send only to the **invoice subaddress** shown for that deposit; do not reuse old addresses.
- Prefer Bridge status for live mins, maxes, fees, and pause flags before sending funds.
- There is no public mint RPC — only the bridge worker mints wrap CAs after a confirmed native deposit (and custody rules).

## Related

- [Trade](trade.md) — order book, fees, Easy Swap
- [Trade API](api.md) — bridge HTTP routes
- [Oracle](../oracle/oracle.md) — signed USD feed and PDCx fees
- [PDC Companion](companion.md) — connect a local wallet
- [Confidential assets](../build/assets.md) — how tokens work on PDC

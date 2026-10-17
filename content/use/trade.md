---
title: Trade and BTC bridge
---

[Trade](https://trade.privacydatacoin.com/) is the PDC exchange surface for confidential assets, including wrapped Bitcoin (**BTCX**). The public site talks to the Trade API at `https://api.trade.privacydatacoin.com/`. Sign-in uses the PDC Companion wallet (same `Px` addresses as the desktop wallet).

This page is for users. Operator runbooks for TSS custody live in the Trade backend repository, not in this manual.

## What you can do

| Action | Where |
| --- | --- |
| Open the UI | [trade.privacydatacoin.com](https://trade.privacydatacoin.com/) |
| Deposit BTC → mint BTCX | **Bridge** page after login |
| Withdraw BTCX → BTC | **Bridge** page after login |
| Trade BTCX against PDC | Order book / pair pages when the market is listed |
| Public bridge status | `GET https://api.trade.privacydatacoin.com/api/bridge/status` |

BTCX is a confidential asset on PDC (8 decimals, satoshi-aligned). Ordinary transfers of BTCX hide amounts the same way other confidential assets do. Bridge mint and burn keep the BTC reserve and circulating BTCX matched **1:1**.

Live limits, fees, pause flags, and confirmation counts are always on Bridge status — prefer that JSON over any fixed number in this page if they disagree.

## Peg and fees (BTC ↔ BTCX)

| Direction | Peg | Who pays the Bitcoin miner fee |
| --- | --- | --- |
| Deposit BTC → mint BTCX | 1 sat received → 1 sat of BTCX minted | You, on the Bitcoin send |
| Withdraw BTCX → BTC | Burn amount **A** → pool outflows **A** | Taken from the burn: you receive **A − fee** |

The withdraw network fee is `withdrawFeeSats` on status (currently **800** sats). Example: burn `0.001` BTCX → receive `0.001 BTC − 800 sats` on Bitcoin L1. The reserve stays peg-neutral; operators do not need a separate fee float for normal withdrawals.

## Deposit BTC (mint BTCX)

1. Connect Companion and open **Bridge**.
2. Create a **deposit invoice**. Note the Bitcoin address and the **OP_RETURN** hex shown for that invoice.
3. From your own Bitcoin wallet, send BTC to that address **and include the OP_RETURN memo**. Shared TSS deposit addresses require the memo so the invoice can be matched. Fiat on-ramps usually cannot attach OP_RETURN — buy to a personal wallet first, then send with the memo.
4. Wait for the confirmation count on Bridge status (mainnet currently uses **6** confirmations).
5. When the deposit is confirmed and the custody ceremony finishes, BTCX is minted to your PDC address.

**Minimums and maximums** come from status (`depositMinSats`, optional `depositMinUsd`, `depositMaxSats`). They are operator-configured. A typical floor is **10 000 sats** (0.0001 BTC) plus any USD floor shown as `depositMinUsd`.

**Fees on deposit:** you pay the normal Bitcoin network fee on your send. The bridge does not take an extra deposit cut. Minted BTCX matches the satoshis received (1:1).

Operators are notified as deposits move through statuses. Manual Accept / Refuse review for large or structured deposits is **not** a live user-facing gate in the current bridge — do not expect a Telegram-style approve step before mint.

## Withdraw BTCX (payout BTC)

1. On **Bridge**, enter a Bitcoin payout address and the BTCX amount (human units, 8 decimals; the UI converts to atomic sats).
2. Complete the burn step the UI / status expects: either burn the BTCX yourself, or send the BTCX to the bridge mint wallet when auto-burn is enabled so the worker can burn from that wallet.
3. After the burn is recorded, the TSS custody ceremony signs a Bitcoin payout and broadcasts it.

**Minimum withdraw** is `withdrawMinSats` on status — currently **10 000 sats** (**0.0001 BTCX**). Max and daily caps, when set, also appear on status.

**Delay:** there is currently **no fixed withdraw delay** (`withdrawDelaySeconds` is **0** on status) — processing starts as soon as burn + custody rules allow. Status may still show optional max sizes, daily caps, or a review threshold for larger amounts; follow the live flags on Bridge.

You receive **A − withdrawFeeSats** in BTC (fee currently **800** sats). The pool outflows exactly **A**.

Operators receive status notifications for every withdrawal. Large withdrawals can raise an ops **ALERT** when the amount is above a share of current reserves (default **30%**) or at/above an absolute size (default **0.1 BTC**). Those alerts are **notify-only** — they do not require a Telegram Accept click to pay out.

## Custody model (short)

Live BTC custody for this bridge uses a **threshold signature (TSS)** deposit address (Bridgeless-class flow). No single process holds a full spend key. Users still only interact with the Trade UI and their own wallets; they do not run TSS nodes.

Public status fields include whether TSS is ready, `withdrawFeeSats`, and (when available) peg snapshot fields such as pool balance (`tssPoolSats`), liability, and bitcoind sync progress.

## Safety

- Never paste seed phrases into Trade or any website.
- Verify you are on `trade.privacydatacoin.com` and that Companion is talking to your own wallet.
- For deposits, always use the invoice OP_RETURN from the UI. A plain send to the shared address without the memo may not mint.
- Bridge pause flags appear on status when deposits or withdrawals are temporarily disabled.
- Prefer Bridge status for live mins, maxes, fee, and confirmations before sending funds.

## Related

- [Confidential assets](../build/assets.md) — how tokens work on PDC
- [Wallets](wallets.md) — Companion and desktop wallet
- [Getting started](getting-started.md) — install and sync a node

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

BTCX is a confidential asset on PDC. Ordinary transfers of BTCX hide amounts the same way other confidential assets do. Bridge mint and burn are separate, operator-visible steps that keep the BTC reserve and the circulating BTCX matched.

## Deposit BTC (mint BTCX)

1. Connect Companion and open **Bridge**.
2. Create a **deposit invoice**. Note the Bitcoin address and the **OP_RETURN** hex shown for that invoice.
3. From your own Bitcoin wallet, send BTC to that address **and include the OP_RETURN memo**. Shared TSS deposit addresses require the memo so the invoice can be matched. Fiat on-ramps (MoonPay, Ramp, and similar) usually cannot attach OP_RETURN — buy to a personal wallet first, then send with the memo.
4. Wait for the confirmation count shown on the Bridge status (mainnet bridge uses several confirmations).
5. When the deposit is confirmed and the custody ceremony finishes, BTCX is minted to your PDC address.

**Minimums** are published on Bridge status (`depositMinSats`, optional `depositMinUsd`). They are operator-configured. A common production floor is about **$100** of BTC. Lab deployments may temporarily use a lower USD floor.

**Fees on deposit:** you pay the normal Bitcoin network (miner) fee on your send. The bridge does not take an extra deposit cut. Minted BTCX matches the satoshis received (1:1).

## Withdraw BTCX (payout BTC)

1. On **Bridge**, enter a Bitcoin payout address and the BTCX amount to burn (atomic units, 8 decimals).
2. After delay / review rules (if any) and the custody ceremony, a Bitcoin payout is broadcast.
3. You receive **A − network fee** in BTC, where **A** is the burned amount. The fee (shown as `withdrawFeeSats` on status, often 800 sats) is taken from that amount so the reserve stays peg-neutral: the pool outflows exactly **A**.

The bridge does not need an operator top-up for miner fees when deposits already back the peg.

## Custody model (short)

Live BTC custody for this bridge uses a **threshold signature (TSS)** deposit address (Bridgeless-class flow). No single process holds a full spend key. Users still only interact with the Trade UI and their own wallets; they do not run TSS nodes.

Public status fields include whether TSS is ready, the withdraw fee, and (when available) peg snapshot fields such as pool balance and bitcoind sync progress.

## Safety

- Never paste seed phrases into Trade or any website.
- Verify you are on `trade.privacydatacoin.com` and that Companion is talking to your own wallet.
- For deposits, always use the invoice OP_RETURN from the UI. A plain send to the shared address without the memo may not mint.
- Bridge pause flags appear on status when deposits or withdrawals are temporarily disabled.

## Related

- [Confidential assets](../build/assets.md) — how tokens work on PDC
- [Wallets](wallets.md) — Companion and desktop wallet
- [Getting started](getting-started.md) — install and sync a node

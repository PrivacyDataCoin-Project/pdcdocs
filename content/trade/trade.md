---
title: Trade
---

[Trade](https://trade.privacydatacoin.com/) is the PDC exchange for confidential assets. Sign-in uses [PDC Companion](companion.md) with the same `Px` addresses as the desktop wallet. The site talks to `https://api.trade.privacydatacoin.com/`.

Wrap and unwrap native coins on the [Bridge](bridge.md). HTTP endpoints for monitors and integrators: [Trade API](api.md).

## What you can do

| Action | Where |
| --- | --- |
| Open the UI | [trade.privacydatacoin.com](https://trade.privacydatacoin.com/) |
| Connect a wallet | [PDC Companion](companion.md) → **Connect Wallet** |
| Wrap / unwrap BTCX or ARQX | [Bridge](bridge.md) (`/bridge`) |
| Trade pairs (Ionic Swap order book) | Exchange / pair pages |
| Easy Swap | `/swap` — rate from the live ticker mid/last |
| Public ticker / USD prices | [Trade API](api.md) |

## Markets

| Pair | Notes |
| --- | --- |
| `PDC-BTCX` | Native PDC vs wrapped Bitcoin |
| `ARQX-BTCX` | Wrapped Arqma vs BTCX |

Wrap assets (BTCX, ARQX) are confidential assets on PDC. Ordinary transfers hide amounts. How mint and burn work: [Bridge](bridge.md).

## Trading fees

Platform trading fees are paid in **native PDC**, separate from Ionic **network gas** (~0.01 PDC on-chain).

| Market | Taker trading fee | Maker |
| --- | --- | --- |
| Native PDC pairs (e.g. `PDC-BTCX`) | **0** | **0** |
| Wrap hubs (e.g. `ARQX-BTCX`) | **0.01 PDC flat + 0.10%** of PDC notional | **0** |

Live schedule: `GET /api/trade-fees`. Quote before take: `GET /api/trade-fees/quote`.

On a fee-enabled take:

1. Match response includes a `fee` quote (`feeDueAtomic`, treasury address).
2. Taker transfers PDC to the fee treasury (Companion).
3. Attach the fee tx with `POST /api/matches/:id/fee` (`feeTxId`).
4. Maker Apply / taker Accept stay gated until the fee is recorded.

Collected fees sit in escrow; a **daily sweep** (23:59 Europe/Warsaw by default) moves them to the mint wallet only when unswept total ≥ **5 PDC**. Ionic gas never goes to mint.

## Easy Swap and Matches

- **Easy Swap** (`/swap`) builds a simple swap UX; the displayed rate uses the live ticker mid/last (not a hardcoded 1:1).
- **Matches** shows offer/want amounts, price, and the escrow trading-fee plus gas hints when a hub fee applies.

## Clearer, safer trade offers

Trade improved how offers appear in the order book so you can better tell which ones are real and ready to trade.

### Two kinds of offers

| Kind | What it means |
| --- | --- |
| **Indicative** | Someone says they want to trade, but the swap proposal is not fully prepared yet. |
| **Firm** | The offer includes a real Ionic Swap proposal from their wallet and is checked more carefully before it goes live. |

In the API and UI these map to `liquidityClass`: `indicative` (open intent) and `firm` (directed proposal with hex).

### Stronger checks for firm offers

A firm offer can no longer be posted with a fake or incomplete proposal. Trade checks that the proposal looks valid and that the amounts match what the order shows.

### Offers do not stay forever

Indicative offers must expire within a set time (about **15 minutes** on the live site), so old or abandoned quotes do not clutter the book.

### Failed swaps clean themselves up

If someone tries to complete a trade and the wallet **accept** fails (for example the seller no longer has the funds), Companion can report that failure. After a few failures, Trade removes the bad offer automatically.

### What this means for you

- The book should have **fewer empty or misleading offers**.
- **Firm** offers are more trustworthy than **indicative** ones.
- Completing a trade still happens in your wallet — Ionic Swap works as before. Trade does **not** hold your money and does **not** lock funds on-chain until the other party accepts.

Live book-quality flags (for monitors): `GET /api/health` → `proposalVerify` (mode, open-order TTL, accept-failure threshold).

## Safety

- Never paste seed phrases into Trade or any website.
- Verify you are on `trade.privacydatacoin.com` and that Companion is talking to your own wallet.
- Prefer live `/api/trade-fees` and Bridge status before sending size that depends on mins or pause flags.
- Prefer **firm** offers when you care about fill quality; treat **indicative** quotes as intent until a proposal is attached.

## Related

- [Bridge](bridge.md) — BTC→BTCX, ARQ→ARQX, custody
- [Trade API](api.md) — ticker, fees, bridge HTTP routes
- [PDC Companion](companion.md) — browser extension
- [Confidential assets](../build/assets.md) — how tokens work on PDC
- [GUI](../wallets/gui.md) — desktop wallet and simplewallet
- [iOS](../wallets/ios.md) — phone wallet

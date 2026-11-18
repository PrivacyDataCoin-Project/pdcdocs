---
title: Funding
---

[PDC Funding](https://funding.privacydatacoin.com/) is the community **crowdfunding** site for Privacy Data Coin. Authors open proposals, donors send **PDC**, **BTCX**, or **BTC** into escrow, and admins release milestone payouts when work lands.

It follows the same idea as classic CryptoNote FFS (Wownero / AEON style), rebuilt for PDC. PDC and BTCX sit in one hot `simplewallet`. One proposal gets one **integrated address** (`payment_id`, 8 bytes / 16 hex characters) for both of those assets — not Monero subaccounts. Native BTC sits in a separate Bitcoin Core wallet. The default wallet name is `funding` (`BTC_WALLET_NAME`). That wallet is not the Trade bridge wallet.

| Piece | Address |
| --- | --- |
| Live site | [funding.privacydatacoin.com](https://funding.privacydatacoin.com/) |
| About | [funding.privacydatacoin.com/about](https://funding.privacydatacoin.com/about) |
| Source | [PrivacyDataCoin-Project/pdc-funding](https://github.com/PrivacyDataCoin-Project/pdc-funding) |
| Public API | `GET /api/v1/proposals`, `GET /api/v1/health` |

Related: [TIP Bot](tipbot.md) (chat tips), [Trade](../trade/trade.md) (USD display quotes), [Bridge](../trade/bridge.md) (BTCX on PDC), [Aliases](../build/aliases.md) (L1 payout destinations).

## Supported assets

A proposal lists one or more of these. Each selected asset has its own target, donation address, received total, and paid total.

| Asset | Chain | Atomic unit | Shown in the UI | Deposit address |
| --- | --- | --- | --- | --- |
| **PDC** | PDC L1, native | `1 PDC = 10^12` | about `0.001 PDC` (3 decimal places) | Integrated address, shared with BTCX on the same proposal |
| **BTCX** | PDC L1, confidential asset | `1 BTCX = 10^8` | 8 decimal places | The same integrated address as PDC |
| **BTC** | Bitcoin | `1 BTC = 10^8` satoshis | 8 decimal places | A new bech32 address from the `funding` Bitcoin Core wallet |

Default asset ids (override with `PDC_ASSET_ID` and `BTCX_ASSET_ID`):

| Asset | Default id |
| --- | --- |
| PDC | `d6329b5b1f7c0805b5c345f4957554002a2f557845f64d7645dae0e051a6498a` |
| BTCX | `c2bf0410873b49ec7e7dd19d62bca9625d80cd3123670a67b48d997d3127426d` |

The scanner credits an L1 payment only when its `asset_id` matches one of those ids **and** that asset is on the proposal. Any other id is left uncredited. A payment that omits `asset_id` is credited as PDC only when the proposal’s L1 assets are PDC without BTCX. If the proposal accepts both PDC and BTCX, a payment with an empty `asset_id` is left uncredited, because both assets share the payment id.

## What it is for

| You are… | You can… |
| --- | --- |
| A donor | Browse proposals and send PDC, BTCX, or BTC to the address shown for that asset while the proposal is in **funding**, **WIP**, or **completed** |
| An author | Register, submit a proposal (scope, per-asset targets, payout address per asset) |
| An admin | Open funding, comment, pay milestones from that proposal’s escrow, mark completed |

USD figures on the page are **display only**. They come from Trade `GET /api/prices/usd` (oracle when Trade enables it). A donation credit does not depend on them. The same feed is read only when a BTCX payout has to size an L1 fee shortfall (see [Fees](#fees)).

## Custodial escrow (read this)

Escrow sits in operator hot wallets: one PDC `simplewallet` for PDC and BTCX, and one Bitcoin Core wallet for BTC. Admins can release funds. Prefer a thin wallet and clear accountability.

- Send each asset only to the address the proposal shows for that asset, after funding is opened. PDC and BTCX use the integrated address. BTC uses the bech32 address.
- Prefer your own wallet for long-term holdings — Funding is for campaigns, not a vault.
- Never send seeds, spend keys, or wallet passwords to the site or admins.
- Loss of a hot-wallet key or a compromised admin session is loss of that escrow. There is no on-chain multisig in this service.

## Status flow

```text
proposal → funding → wip → completed
```

(`disabled` exists for moderation.)

| Status | Meaning |
| --- | --- |
| **proposal** | Submitted; not yet accepting donations |
| **funding** | Admin opened funding; deposit addresses assigned; scanner credits confirmed payments |
| **wip** | Work in progress; donations can still credit; comments track updates |
| **completed** | Archive; the scanner still credits late donations; payouts remain allowed |
| **disabled** | Hidden / stopped; the scanner does not credit it |

When an admin sets a proposal to **funding** or any later open status (`funding`, **WIP**, **completed**), the app assigns deposit addresses once. The scanner credits those three statuses only.

## How to donate

1. Open [funding.privacydatacoin.com](https://funding.privacydatacoin.com/) and pick a proposal whose status is **funding**, **WIP**, or **completed**. The donate block appears once the status is **funding** or later.
2. Send the asset that proposal lists:
   - **PDC** or **BTCX** — the shared integrated address. The payment id is inside that address. The scanner reads `get_bulk_payments` and credits the asset whose chain id matches.
   - **BTC** — the proposal’s bech32 address. The scanner reads `getreceivedbyaddress` on the `funding` wallet and credits only the increase since the last credited total.
3. Wait for confirmations, and on PDC or BTCX for unlock, before the site adds the payment to that asset’s **received** total.
4. Each asset has its own progress bar: `received / target` for that asset, capped at 100%. Available escrow for that asset is `received − paid` (paid includes pending payout reservations).

### Confirmations

| Asset | Setting | Default | When a deposit counts |
| --- | --- | --- | --- |
| PDC, BTCX | `DEPOSIT_MIN_CONFIRMATIONS` | **10** | Confirmations are daemon `getinfo` height minus the payment’s `block_height`. A transaction in the tip has 1 confirmation when `height == block_height + 1`. If that height is unknown, the L1 scan credits nothing. The payment must also be unlocked: `unlock_time` of `0` is unlocked; a value below `500000000` is a block height and unlocks when `height >= unlock_time`; a larger value is a unix timestamp. |
| BTC | `BTC_MIN_CONFIRMATIONS` | **3** | Passed as `minconf` to Bitcoin Core `getreceivedbyaddress`. The ledger stores the delta of that confirmed total. There is no separate unlock-time check in this service. |

The scanner loops every `DEPOSIT_SCAN_INTERVAL_SEC` seconds (default **30**). The L1 watermark stays at least `DEPOSIT_MIN_CONFIRMATIONS + 5` blocks behind the tip, and behind any payment that is still locked, so a payment that was not ready on the first pass is queried again. L1 credits are unique on `(tx_hash, payment_id, asset)`.

An empty `BTC_RPC_URL` leaves BTC in dry-run: the page can show a placeholder address, and the BTC scanner does not credit. An empty `WALLET_RPC_URL` does the same for PDC and BTCX.

## How to propose work

1. **Register** / **Log in** on the Funding site.
2. Submit a proposal: headline, category, description, and at least one asset. Each selected asset has a target and a payout address. PDC and BTCX payout destinations may be an address or `@alias` (resolved with the daemon `get_alias_details`). A BTC payout destination is a Bitcoin address.
3. Selecting **BTCX** without **PDC** adds a PDC lane automatically. Its default target is one L1 network fee (`TRANSFER_FEE_ATOMIC`, default **0.01 PDC**). If the author sets a PDC target on a proposal that also has BTCX, that target must be at least that fee. Selecting **BTC** alone does not add a PDC lane.
4. Wait for an admin to move the proposal to **funding**. That assigns the integrated address and, when BTC is selected, the bech32 address.
5. Share the proposal link. Donors pay the address for the asset they send.
6. Post updates in comments while status is **WIP**.
7. An admin releases a milestone for one asset at a time, to that asset’s payout address unless the payout form names another destination. The milestone is the payout note (the proposal body describes the stages; there is no separate milestone table). Payouts are allowed in **funding**, **WIP**, and **completed**, and only from the primary admin account.

Categories in the UI include wallets, marketing, core, design, docs, and misc.

## Fees

Fees are taken when funds leave escrow (a milestone payout). The scanner credits the amount it sees on the deposit. This service does not take a percentage of donations.

The chain fee is paid from **that proposal’s escrow**. Defaults below are the code defaults. Operators can change the environment values; the 2% shortfall buffer and the 546 sat dust floor are constants in the source.

| Payout | Who pays | What is sent | Fee |
| --- | --- | --- | --- |
| **PDC** | This proposal’s PDC escrow | Recipient receives `A − fee`. The ledger debits the full amount `A`. | `TRANSFER_FEE_ATOMIC`, default `10000000000` atomic units = **0.01 PDC**. The amount must be greater than the fee. Passed as the L1 `transfer` fee. |
| **BTCX** | This proposal’s escrow, not a cut of the BTCX the recipient receives | Recipient receives the full BTCX amount. The L1 fee is an extra debit. | Same `TRANSFER_FEE_ATOMIC` (default **0.01 PDC**), paid in PDC on the L1 transfer. Cover order: PDC escrow on this proposal, then leftover BTCX (after the milestone), then leftover BTC on this proposal. `BTCX_TRANSFER_FEE_ATOMIC` defaults to **0** and is not used for this fee. |
| **BTC** | This proposal’s BTC escrow | The ledger debits the full reserved amount. Bitcoin Core sends it with `subtractfeefromamount`, so the recipient receives that amount minus the miner fee. | The miner fee is the fee Bitcoin Core chooses for that send. `BTC_TRANSFER_FEE_SATS` (default **1000**) is not that fee. The payout must be greater than `max(BTC_TRANSFER_FEE_SATS, 546)` satoshis (default floor **1000** sats, **0.00001000 BTC**). |

BTCX fee cover (`funding/fee_convert.py`):

- PDC already credited to this proposal is used first, up to the L1 fee.
- A shortfall is reserved from leftover BTCX, then leftover BTC, on the same proposal.
- The reserved size is the fee measured with the Trade USD feed (`PRICES_USD_URL`, default `https://api.trade.privacydatacoin.com/api/prices/usd`), plus **2%** (`_SLIP_BPS = 200`), rounded up. That 2% is not an environment setting. It is a buffer on the shortfall reservation, not a percentage charged on the donation.
- Those rows are ledger reservations (`l1-network-fee` on PDC, `l1-fee-convert` on BTCX or BTC). They count in that asset’s **paid** total and share the payout transaction id after the send. The service does not broadcast a second conversion transaction.
- The hot L1 wallet must already have at least `TRANSFER_FEE_ATOMIC` unlocked PDC, or the payout is refused. A BTCX or BTC reservation does not replace that unlocked PDC on the chain.
- If this proposal cannot cover the fee, or the Trade feed is unavailable while PDC escrow is short, the payout is refused.

A payout is **reserved in SQLite before** the wallet RPC call. An uncertain RPC result keeps the reservation so the same balance cannot be sent twice. Pending rows count toward **paid** until an operator reconciles them.

## Money model (short)

Totals are per asset, on `proposal_assets`. They are sums of rows, not a cached balance.

| Term | Meaning |
| --- | --- |
| Received | Sum of credited deposits for that asset on that proposal |
| Paid | Sum of payout rows for that asset, including **pending** reservations and any BTCX fee-cover rows in that asset |
| Available | `received − paid` — what admins can still release for that asset |
| Target | The target stored for that asset |
| Progress | `received / target` for that asset, capped at 100% |
| Hot wallets | One pooled L1 wallet for PDC and BTCX, and one pooled Bitcoin wallet for BTC. Per-proposal numbers are an application ledger, not a chain partition |

`GET /api/v1/proposals` still returns one `funds_target_atomic`, `received_atomic`, and `paid_atomic` per proposal. `funds_target_atomic` is the PDC target when the proposal has PDC, otherwise the first selected asset. `received_atomic` and `paid_atomic` add raw atomic units across every asset and do not convert between `10^12` and `10^8`. `addr_donation` is the integrated address copied onto the proposal header when the PDC row is assigned. Per-asset totals and the BTC address are on the proposal page.

## Public API

| Method | Path | Notes |
| --- | --- | --- |
| `GET` | `/api/v1/proposals` | Public list (status, header target, summed atomics, integrated address when the PDC row has one) |
| `GET` | `/api/v1/health` | `wallet` and `btc_wallet` are each `live` or `dry-run`. `assets` lists `PDC`, `BTCX`, `BTC` |

JSON `/api/v1` is read-only. Example: [https://funding.privacydatacoin.com/api/v1/proposals](https://funding.privacydatacoin.com/api/v1/proposals).

## What this is not

- Not an on-chain smart contract (PDC L1 has no EVM).
- Not multisig escrow and not view-key deposit proofs for donors.
- Not a tip bot — for chat tips use [TIP Bot](tipbot.md).
- Not Trade — for exchange and Bridge see [Trade](../trade/trade.md).

## Related

- Live UI: [funding.privacydatacoin.com](https://funding.privacydatacoin.com/)
- Operator docs in the repo: [architecture](https://github.com/PrivacyDataCoin-Project/pdc-funding/blob/main/docs/architecture.md), [deployment](https://github.com/PrivacyDataCoin-Project/pdc-funding/blob/main/docs/DEPLOYMENT.md), [security audit](https://github.com/PrivacyDataCoin-Project/pdc-funding/blob/main/docs/security-audit.md)
- Source of the multi-asset fee rules: [commit `01c84936`](https://github.com/PrivacyDataCoin-Project/pdc-funding/commit/01c84936211f44e6c614b85242e38d6f584ea1f5) (`funding/assets.py`, `funding/scanner.py`, `funding/service.py`, `funding/fee_convert.py`, `funding/config.py`)
- [TIP Bot](tipbot.md) · [Aliases](../build/aliases.md) · [Oracle](../oracle/oracle.md)

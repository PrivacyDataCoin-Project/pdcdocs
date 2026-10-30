---
title: Funding
---

[PDC Funding](https://funding.privacydatacoin.com/) is the community **crowdfunding** site for Privacy Data Coin. Authors open proposals, donors send PDC into escrow, and admins release milestone payouts when work lands.

It follows the same idea as classic CryptoNote FFS (Wownero / AEON style), rebuilt for PDC. Escrow uses the tipbot wallet pattern: one hot `simplewallet` and per-proposal **integrated addresses** (`payment_id`) — not Monero subaccounts.

| Piece | Address |
| --- | --- |
| Live site | [funding.privacydatacoin.com](https://funding.privacydatacoin.com/) |
| About | [funding.privacydatacoin.com/about](https://funding.privacydatacoin.com/about) |
| Source | [PrivacyDataCoin-Project/pdc-funding](https://github.com/PrivacyDataCoin-Project/pdc-funding) |
| Public API | `GET /api/v1/proposals`, `GET /api/v1/health` |

Related: [TIP Bot](tipbot.md) (chat tips), [Trade](../trade/trade.md) (USD display prices), [Aliases](../build/aliases.md) (payout destinations).

## What it is for

| You are… | You can… |
| --- | --- |
| A donor | Browse proposals, send PDC to a proposal’s donation address while it is in **funding** or **WIP** |
| An author | Register, submit a proposal (scope, target, milestones, payout address) |
| An admin | Open funding, comment, pay milestones from escrow, mark completed |

USD amounts on the page are **display only**. They come from Trade `GET /api/prices/usd` (oracle when Trade enables it). They do not gate donations or payouts.

## Custodial escrow (read this)

Escrow sits in an operator hot wallet. Admins can release funds. Prefer a thin wallet and clear accountability.

- Donate only to the **integrated address shown on that proposal** after funding is opened.
- Prefer your own wallet for long-term holdings — Funding is for campaigns, not a vault.
- Never send seeds, spend keys, or wallet passwords to the site or admins.
- Loss of the hot-wallet keys or a compromised admin session is loss of escrow. There is no on-chain multisig in this service.

## Status flow

```text
proposal → funding → wip → completed
```

(`disabled` exists for moderation.)

| Status | Meaning |
| --- | --- |
| **proposal** | Submitted; not yet accepting donations |
| **funding** | Admin opened funding; donation address assigned; scanner credits confirmed payments |
| **wip** | Work in progress; donations can still credit; comments track updates |
| **completed** | Archive; payouts may already have been made |
| **disabled** | Hidden / stopped |

When an admin moves a proposal into **funding**, the app assigns `payment_id` and `integrated_address` once. The deposit scanner credits proposals in **funding** or **WIP** only.

## How to donate

1. Open [funding.privacydatacoin.com](https://funding.privacydatacoin.com/) and pick a proposal in **funding** (or **WIP** if still raising).
2. Copy the proposal’s **integrated donation address**.
3. Send **PDC** (native) from any wallet to that address.
4. Wait for confirmations and unlock. The site credits only after the payment is unlocked and has enough confirmations against daemon height.
5. Progress bars use `received / target`. Available escrow is `received − paid` (including pending payout reservations).

Do not send a different confidential asset. Wrong asset ids are ignored by the scanner.

## How to propose work

1. **Register** / **Log in** on the Funding site.
2. Submit a proposal: headline, category, description, funding target, milestones, and a payout address or `@alias` when ready.
3. Wait for an admin to move it to **funding** (that assigns the donation address).
4. Share the proposal link; donors pay the integrated address.
5. Post updates in comments while status is **WIP**.
6. Admins release milestone amounts to the author payout address. A payout of amount `A` sends `A − network fee` on-chain; the fee is taken from the same escrow debit.

Categories in the UI include wallets, marketing, core, design, docs, and misc.

## Money model (short)

| Term | Meaning |
| --- | --- |
| Received | Sum of credited deposits for that proposal |
| Paid | Sum of payout rows (including **pending** reservations) |
| Available | `received − paid` — what admins can still release |
| Hot wallet | One pooled balance; per-proposal numbers are an app ledger, not a chain partition |

A payout is **reserved in SQLite before** the wallet RPC call. An uncertain RPC result keeps the reservation so the same balance cannot be sent twice. Pending rows show until an operator reconciles them.

Atomic unit: `1 PDC = 10^12`. UI amounts are shown to about `0.001 PDC`.

## Public API

| Method | Path | Notes |
| --- | --- | --- |
| `GET` | `/api/v1/proposals` | Public list (status, targets, received, paid, donation address when assigned) |
| `GET` | `/api/v1/health` | `wallet` is `live` or `dry-run` |
| `POST` | `/api/v1/scan` | Admin session — force one deposit scan |

Example: [https://funding.privacydatacoin.com/api/v1/proposals](https://funding.privacydatacoin.com/api/v1/proposals).

## What this is not

- Not an on-chain smart contract (PDC L1 has no EVM).
- Not multisig escrow and not view-key deposit proofs for donors.
- Not a tip bot — for chat tips use [TIP Bot](tipbot.md).
- Not Trade — for exchange and Bridge see [Trade](../trade/trade.md).

## Related

- Live UI: [funding.privacydatacoin.com](https://funding.privacydatacoin.com/)
- Operator docs in the repo: [architecture](https://github.com/PrivacyDataCoin-Project/pdc-funding/blob/master/docs/architecture.md), [deployment](https://github.com/PrivacyDataCoin-Project/pdc-funding/blob/master/docs/DEPLOYMENT.md), [security audit](https://github.com/PrivacyDataCoin-Project/pdc-funding/blob/master/docs/security-audit.md)
- [TIP Bot](tipbot.md) · [Aliases](../build/aliases.md) · [Oracle](../oracle/oracle.md)

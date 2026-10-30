---
title: TIP Bot
---

PDC TipBot is the official **custodial tip bot** for Privacy Data Coin. It keeps a shared off-chain ledger so tips and giveaways settle instantly, and uses one hot wallet for on-chain deposits and withdrawals.

| Surface | How to reach it |
| --- | --- |
| Telegram | [@PDCTip_Bot](https://t.me/PDCTip_Bot) |
| Matrix | `@pdctipbot:privacydatacoin.com` on [PDC Messenger](../matrix/messenger.md) |
| Hot-wallet alias (informational) | `@pdctipbot` on-chain |

Telegram uses `/…` commands. Matrix accepts `!` or `/` (for example `!tip @alice:privacydatacoin.com 1`).

Source and ops docs for operators: [PrivacyDataCoin-Project/pdc-tipbot](https://github.com/PrivacyDataCoin-Project/pdc-tipbot).

## What it is for

| You want to… | Use |
| --- | --- |
| Tip someone in Telegram or Matrix | `/tip` (ledger — no chain fee) |
| Run a group giveaway | `/giveaway` |
| Claim from the communal rain pool | `/rain` in an allowed chat |
| Move coins on-chain out of the bot | `/withdraw` or `/send` |
| Top up your tipbot balance | `/deposit` → send PDC to your integrated address |

Telegram and Matrix identities are **separate** ledger accounts. There is no automatic link between them in the current release.

## Custodial model (read this)

The operator holds the hot-wallet keys. When you deposit, those coins sit in that wallet until you tip, rain-fund, withdraw, or send.

- Prefer a **small** tipbot balance. Sweep surplus with `/withdraw` to your own wallet.
- Tips, giveaways, and rain claims move ledger balances only — fast, no network fee.
- `/withdraw` and `/send` create a real chain transfer and debit the network fee from your tipbot balance.
- Never send seeds, spend keys, or wallet passwords to the bot.

## First steps

1. Open a **private chat** with [@PDCTip_Bot](https://t.me/PDCTip_Bot) (or DM `@pdctipbot:privacydatacoin.com` on Matrix).
2. Send `/start` — the bot creates your ledger account and an integrated deposit address.
3. Send `/deposit` and copy the address (prefer DM so the address is not public).
4. Send PDC to that address from any wallet. Wait for confirmations and unlock before the ledger credits.
5. Check with `/balance` in DM.

In groups, private payloads such as `/balance` stay silent — open a DM.

## Commands

| Command | Description |
| --- | --- |
| `/start` | Create ledger account + deposit address |
| `/balance` | DM: spendable balance and pending deposit status |
| `/deposit` | Your integrated deposit address (prefer DM) |
| `/tip <@user\|reply> <amount> [msg]` | Instant ledger tip |
| `/giveaway <amount>` | Group/room giveaway (Claim / Cancel) |
| `/claim <id>` | Claim a Matrix giveaway by id |
| `/cancel <id>` | Cancel your open giveaway |
| `/rain` | Claim from the rain pool (allowed chats only) |
| `/rain info` | Pool size, next claim size, your cooldown |
| `/rain fund <amount>` | Move tipbot balance into the rain pool |
| `/rain deposit` | On-chain address that credits the rain pool |
| `/withdraw <address\|@alias>` | Sweep unlocked balance minus network fee |
| `/send <address\|@alias> <amount>` | On-chain send (max = unlocked − fee) |
| `/help` | Help text |

Telegram tip-by-reply: reply to a message with `/tip 0.5 thanks`.

## Tips and giveaways

**Tips** debit your tipbot balance and credit the recipient’s tipbot balance immediately. No chain fee. The recipient must have used `/start` (or otherwise have an account) so they can receive.

**Giveaways** lock an amount from your tipbot balance in a public chat. Others claim until the pot is empty or you cancel. On Matrix you may need `/claim <id>` when the UI does not attach buttons.

## Rain (communal faucet)

`/rain` is a shared pool that anyone can top up. Claims are only allowed in **configured** Telegram groups and Matrix rooms.

| Rule | Detail |
| --- | --- |
| Cooldown | One successful claim per identity per **24 hours** (rolling) |
| Claim size | Dynamic from pool size (bounded min/max) |
| Bots | Rejected |
| Funding | `/rain fund <amount>` from tipbot balance, or on-chain to `/rain deposit` (credited after unlock) |

Typical claim reply:

```text
Rain claimed: 1 PDC.
Pool left: 106 PDC
Next claim after 24h.
```

Use `/rain info` to see pool size, the next claim amount, and whether you are still on cooldown. Full operator rules: [RAIN.md in the tipbot repo](https://github.com/PrivacyDataCoin-Project/pdc-tipbot/blob/master/docs/RAIN.md).

## Deposits, withdraw, and send

| Action | What happens |
| --- | --- |
| Deposit | You pay to your `/deposit` integrated address. Mempool deposits can show as pending; the ledger credits only after inclusion, confirmations, and unlock. |
| Withdraw | Sweeps **all** unlocked tipbot balance minus the network fee to an address or `@alias`. |
| Send | On-chain transfer of a chosen amount (max = unlocked − fee). |

If the hot wallet cannot cover liabilities, on-chain payouts are refused until the operator restores solvency. That protects other users’ balances.

## Safety checklist

- Tipbot is convenient for chat — not a long-term vault.
- Confirm the bot username: Telegram **@PDCTip_Bot**, Matrix **@pdctipbot:privacydatacoin.com**.
- Deposit only to the address from **your** `/deposit` reply.
- Keep daily withdraw habits modest; the bot may enforce daily limits.
- Report abuse or stuck payouts to the project channels (Telegram / Matrix General), not by pasting keys.

## Related

- [Funding](funding.md) — community proposals and escrow crowdfunding
- [PDC Messenger](../matrix/messenger.md) — Matrix homeserver and alias claim
- [Aliases](../build/aliases.md) — `@name` destinations for withdraw / send
- [Getting started](../use/getting-started.md) — your own wallet for long-term holdings
- TipBot source: [github.com/PrivacyDataCoin-Project/pdc-tipbot](https://github.com/PrivacyDataCoin-Project/pdc-tipbot)

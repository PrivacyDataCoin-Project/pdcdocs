---
title: Aliases
---

An alias is a public name for an address. People can send to the name instead of a long `Px` string. The wallet resolves the name before it builds the transaction.

The name is not private. `get_alias_details`, `get_all_alias_details`, `get_aliases`, and `get_alias_by_address` all return it. The transfers that use the alias are still confidential.

## Name rules

| Rule | Value in the source |
| --- | --- |
| Minimum public length | 6 characters (`ALIAS_MINIMUM_PUBLIC_SHORT_NAME_ALLOWED`) |
| Maximum length | 255 |
| Allowed characters | `0123456789abcdefghijklmnopqrstuvwxyz-.` |
| Comment size | 400 bytes |
| Registrations in one block | At most 1,000 |

Shorter names are gated by `ALIAS_SHORT_NAMES_VALIDATION_PUB_KEY`. A normal registration uses a name of at least 6 characters.

## The fee is burned

The alias reward account is three zero keys:

```text
ALIAS_REWARDS_ACCOUNT_SPEND_PUB_KEY
ALIAS_REWARDS_ACCOUNT_VIEW_PUB_KEY
ALIAS_REWARDS_ACCOUNT_VIEW_SEC_KEY
```

The comment on those constants says the alias money is burned. There is no spendable rewards address in this configuration.

The price is not a single constant for the life of the chain. The node keeps a median over `ALIAS_COAST_PERIOD` (7 days of blocks) and looks at a recent window of 8 days (`ALIAS_COAST_RECENT_PERIOD`). The median is recalculated about once a day (`ALIAS_MEDIAN_RECALC_INTERWAL`). The bootstrap value `ALIAS_VERY_INITAL_COAST` is 10,000 atomic units, which is 0.00000001 PDC, so the first registrations are not stuck on a large hardcoded price.

Ask a synced node for the figure it will actually charge:

```text
curl -s http://127.0.0.1:19211/json_rpc \
  -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","id":"0","method":"get_alias_reward","params":{}}'
```

Register from the desktop wallet's alias screen, or build the alias transaction from a wallet that implements the attachment. The daemon will reject a registration that does not burn the current fee. The chain checks that burn in `check_native_coins_amount_burnt_in_outs`.

After the alias is on-chain, claim Matrix chat as `@alias:privacydatacoin.com` in [PDC Messenger](../matrix/messenger.md).

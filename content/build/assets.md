---
title: Confidential assets
---

PDC can carry more than the native coin. A maintainer registers an asset descriptor. Later wallet transfers of that asset hide the amount and the asset id the same way a PDC transfer does.

Administration is not hidden. Deploying, minting, burning, updating metadata, and transferring ownership are their own transactions. Anyone watching the chain can see that an asset operation happened. They still cannot read an ordinary subsequent transfer.

## Who is allowed to do what

The wallet that deploys the asset is the maintainer.

| Action | Command | Rule in the wallet |
| --- | --- | --- |
| Create | `deploy_new_asset <json_filename>` | Current wallet becomes the maintainer |
| Mint | `emit_asset <asset_id> <amount>` | Maintainer only |
| Burn | `burn_asset <asset_id> <amount>` | Maintainer, and the wallet must hold the units it burns |
| Edit metadata | `update_asset <asset_id> <path_to_metadata_file>` | Maintainer only |
| Change owner | `transfer_asset_ownership <asset_id> <new_owner_public_key>` | Replaces the owner field |

Hard fork 4 is where these operations take their Zarcanum-era form. After height 1199, hard fork 5 switches asset operations onto `validate_asset_operation_hf5` in `blockchain_storage.cpp` (hard forks 6 and 7 activate at the same height).

## The public whitelist

Wallets download:

```text
https://api.privacydatacoin.com/assets_whitelist.json
```

The file is checked against `WALLET_ASSETS_WHITELIST_VALIDATION_PUBLIC_KEY` in `currency_config.h`. Testnet builds use `assets_whitelist_testnet.json` on the same host.

`balance` shows assets on that list. `balance raw` shows everything the wallet can recognize. `add_custom_asset_id` is the local approval for an asset the public list does not name yet. Removing it with `remove_custom_asset_id` hides it again. Neither command changes the chain.

## Reading assets from a node

`get_asset_info` returns one asset by id. `get_assets_list` returns the registered set. Both are JSON-RPC methods on the daemon. They return the public descriptor, not someone else's balance.

## Sending a token

In `simplewallet` the transfer form accepts an asset id in front of the address:

```text
transfer <mixin_count> <asset_id>:<address> <amount>
```

Omit the asset id to send native PDC. The ring size and the fee rules are the same. The fee is paid in PDC: `TX_MINIMUM_FEE` is 0.01 PDC.

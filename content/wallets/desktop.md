---
title: Desktop and CLI
---

Two wallets ship in the [PDC](https://github.com/PrivacyDataCoin-Project/PDC) release archives: the Qt GUI (`Pdc`) and the command-line wallet (`simplewallet`). For phones, see the [iOS wallet](ios.md). For a short comparison, see [Wallets overview](overview.md).

For [trade.privacydatacoin.com](https://trade.privacydatacoin.com/), also install the [PDC Companion](../trade/companion.md) browser extension so the site can talk to a local wallet without ever seeing your seed.

## Desktop wallet (GUI)

The desktop wallet is the `Pdc` executable from release <a data-doc-release href="https://github.com/PrivacyDataCoin-Project/PDC/releases/latest"><span data-doc-version>v3.0.0</span></a>. Release builds use **Qt 6.8**. The app runs a local `pdcd` node and one or more wallets in the same process. That is what staking needs: the wallet has to stay online and synced.

Download the GUI package for your platform from [Getting started](../use/getting-started.md) (AppImage, Windows installer/zip, or macOS DMG). Prefer the current GitHub release over an older archive.

### First run

1. Install or unpack the GUI package.
2. Start `Pdc`. On first launch the app creates a data directory and starts the embedded node.
3. Create a new wallet, or restore one from the 24-word phrase.
4. Write the phrase down offline. The wallet cannot recover funds from the phrase if you never saved it.
5. Wait until the sidebar shows the node online and the wallet height matches the chain.

Default data directories:

| OS | Path |
| --- | --- |
| Linux | `~/.PDC` |
| macOS | `~/Library/Application Support/PDC` |
| Windows (64-bit) | Roaming application data folder named `PDC` |

Override the location with `--data-dir` when you start the binary from a shell.

### Layout

| Area | What it does |
| --- | --- |
| Sidebar | Open wallets, sync status, portfolio value, update notices |
| Assets | Balances for native PDC and whitelisted confidential assets |
| Send | Build a transfer (address or alias, amount, asset, fee) |
| Receive | Show your `Px` address and QR |
| History | Confirmed transfers for the active wallet |
| Staking | Online staking controls (wallet must be unlocked and synced) |
| Settings | Themes, Companion JWT, wallet options |

You can keep several wallets open. The active wallet in the sidebar is the one Send, Receive, and Companion use.

### Assets and portfolio

The Assets list shows balances for assets on the public whitelist (and any you added locally). Typical mainnet tickers include:

| Ticker | Meaning |
| --- | --- |
| PDC | Native coin |
| BTCX | Wrapped Bitcoin (Bridge) |
| ARQX | Wrapped Arqma (Bridge) |
| PDCX | Wrapped / fee-token PDC (display name in GUI) |

The sidebar can show a USD portfolio mark. The GUI loads marks from the explorer `pdc_market` feed (Trade-backed prices with CORS allowed for the desktop WebEngine). Direct Trade `/api/prices/usd` is allow-listed and is not the path the GUI uses.

Add a non-whitelisted asset only if you trust its asset id. Unknown assets can appear after you approve them locally; that does not make them part of the public whitelist.

### Sync and updates

The sidebar reports daemon state: offline, syncing, online, or error. During sync it shows block progress. Wait until the wallet is online before staking or relying on balances for large sends.

When maintainers publish a signed version notice on the P2P network, the sidebar can show an update button:

| Level | Meaning |
| --- | --- |
| Update available | Newer build exists |
| Important update | Upgrade soon |
| Critical update | Upgrade strongly recommended |

The button opens the downloads page. The notice carries a version and alert level only — not free-form text.

### Companion (Trade)

Settings → **Pdc Companion** turns on the JWT wallet RPC (default port **19211**) for the browser extension. Copy the Secret into Companion, then use [PDC Companion](../trade/companion.md) to connect Trade. The GUI never sends your seed to the site.

### Seed and keys in the GUI

Use the wallet details / seed screens in the app to view the 24-word phrase and keys after unlock. Treat them like the `simplewallet` commands below: anyone with the seed or spend key can spend the funds.

## Command-line wallet (`simplewallet`)

`simplewallet` talks to a `daemon` over RPC. Use it on a server, in scripts, and when you want the full command list. Companion can also relay to `simplewallet` RPC on port **19212**.

Against a local daemon:

```text
./simplewallet --wallet-file=mywallet --daemon-address=127.0.0.1:19211
```

`help` lists every command. The handlers live in `src/simplewallet/simplewallet.cpp`.

## Secrets

| Command | What it prints |
| --- | --- |
| `show_seed` | The 24-word recovery phrase |
| `spendkey` | The secret spend key |
| `viewkey` | The secret view key |
| `tracking_seed` | For an auditable wallet, the seed a reviewer can use |
| `address` | The public `Px` address |
| `integrated_address` | Encode or decode an `iP` address and a payment id |

Anyone with the seed or the spend key can spend the funds. Anyone with the view key can recognize incoming outputs. Treat all three as secrets. The tracking seed is a deliberate exception: you give it to an auditor and to nobody else.

## Everyday commands

| Command | Purpose |
| --- | --- |
| `refresh` | Pull new transfers and recompute the balance |
| `balance` | Show balances for whitelisted assets. `balance raw` also shows assets outside the whitelist |
| `transfer` | Send. The form is `transfer <mixin_count> [asset_id:]<address> <amount> ... [payment_id]` |
| `incoming_transfers` | List incoming outputs, optionally `available` or `unavailable` |
| `list_recent_transfers` | The latest transfers, up to 1,000, with offset and count |
| `payments` | Find transfers by payment id |
| `save` | Write the wallet file |
| `resync` | Forget cached transfers and scan again |
| `bc_height` | Node height |
| `wallet_bc_height` | Height the wallet has scanned |

`transfer` still takes a mixin count. After hard fork 4 the protocol requires 15 decoys. Passing a smaller count does not make the transfer public. The node enforces the mandatory set.

A payment id is an optional hex string. An integrated address carries one inside the `iP` string so the sender does not have to paste it separately.

## Watch-only and offline signing

`save_watch_only <filename> <password>` writes a wallet that can see funds and prepare transactions. It cannot sign them.

The signing flow is:

1. The watch-only wallet prepares an unsigned transaction.
2. `sign_transfer <unsigned_tx_file> <signed_tx_file>` signs it on the machine that holds the spend key.
3. `submit_transfer <signed_tx_file>` broadcasts the signed transaction.

## Assets from the command line

| Command | Who can run it |
| --- | --- |
| `deploy_new_asset <json>` | Creates an asset. This wallet becomes the maintainer |
| `emit_asset <asset_id> <amount>` | Mints more units. Maintainer only |
| `burn_asset <asset_id> <amount>` | Burns units the maintainer holds |
| `update_asset <asset_id> <metadata>` | Updates the descriptor metadata |
| `transfer_asset_ownership <asset_id> <new_owner_public_key>` | Hands the maintainer role to another key |
| `add_custom_asset_id` | Show an asset even if it is not on the public whitelist |
| `remove_custom_asset_id` | Drop that local approval |

Deploying, minting, and burning are explicit chain operations. They are not hidden the way a later wallet transfer of that asset is hidden.

## Tor relay

`tor_enable` and `tor_disable` switch relaying of transactions over Tor. The wallet registers this relay as enabled by default. Disabling it changes the path your transaction takes to the network. It does not change what the chain stores.

## Files

Wallet files use signature `WALLET_FILE_SIGNATURE_V2`. The serialization version in this tree is 168, and the oldest supported version is 165. Copy the wallet file and keep the seed. The file without the password is not a backup you can restore on an empty machine if you also lost the phrase and the password.

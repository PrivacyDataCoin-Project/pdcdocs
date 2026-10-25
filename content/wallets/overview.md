---
title: Wallets overview
---

Official wallets for Privacy Data Coin. Pick the one that matches how you run the network.

| Wallet | Platform | Node | Best for |
| --- | --- | --- | --- |
| [Desktop GUI (`Pdc`)](desktop.md) | Linux, Windows, macOS | Embedded local `pdcd` | Everyday use, staking, [Trade](../trade/trade.md) via [Companion](../trade/companion.md) |
| [Command-line (`simplewallet`)](desktop.md#command-line-wallet-simplewallet) | Same release archives | Remote or local daemon RPC | Servers, scripts, offline signing |
| [iOS wallet](ios.md) | iOS | Remote PDC node only | Phone: send, receive, history (no local full node) |

Install desktop and CLI binaries from [Getting started](../use/getting-started.md). The iOS app is published separately as **PDC Wallet** (`com.privacydatacoin.pdcwallet`).

All of these are **non-custodial**: the seed and spend key stay on your device. The publisher never holds your funds. Write the 24-word phrase down offline before you rely on a balance.

For Trade, Bridge, and Ionic Swap you need a desktop or `simplewallet` RPC session plus [PDC Companion](../trade/companion.md). The iOS wallet does not expose Companion RPC.

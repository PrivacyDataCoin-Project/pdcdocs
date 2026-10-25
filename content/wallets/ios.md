---
title: iOS
---

**PDC Wallet** is the official non-custodial wallet for Privacy Data Coin on iOS. This page is only about the phone app. For the desktop Qt wallet, see [GUI](gui.md).

It is published by PrivacyDataCoin Project for **one chain and one asset: PDC**. Keys and the seed stay on the device. The app talks to a **remote PDC node** over RPC; it does not run a full node on the phone and does not stake.

| Item | Value |
| --- | --- |
| App name | PDC Wallet |
| Bundle ID | `com.privacydatacoin.pdcwallet` |
| Current app version | **3.1.0** (build 12) |
| Source | [PrivacyDataCoin-Project/pdcwallet_ios](https://github.com/PrivacyDataCoin-Project/pdcwallet_ios) |
| Product site | [privacydatacoin.com](https://privacydatacoin.com/) |
| Privacy policy | [privacydatacoin.com/privacy.html](https://privacydatacoin.com/privacy.html) |
| App Store | [PDC Wallet](https://apps.apple.com/app/id6818298023) (listing goes live when App Review approves) |
| TestFlight | [Join the public beta](https://testflight.apple.com/join/NwmhAhfi) |

## What you can do

- Create a new PDC wallet or restore one from the 24-word seed
- See balance, locked balance, and transaction history for PDC
- Send and receive PDC on the PrivacyDataCoin network
- Optional biometric unlock after you turn it on in settings (system Face ID / Touch ID)
- Save the wallet, change the password, and show the seed after the password
- Rescan the account from the start of the chain
- See PoW mining rewards and PoS staking rewards labeled separately in history (rewards earned elsewhere; the phone app does not stake)

## What it does not do

- No local daemon / full node on the device
- No online staking from the phone
- No in-app exchange and no service-node registrar
- No publisher account and no in-app purchases
- No [PDC Companion](../trade/companion.md) RPC — use the [GUI](gui.md) wallet for Trade

## Get the beta (TestFlight)

Install via the public TestFlight link: [testflight.apple.com/join/NwmhAhfi](https://testflight.apple.com/join/NwmhAhfi).

1. Install [TestFlight](https://apps.apple.com/app/testflight/id899247664) from the App Store if you do not already have it.
2. Open the invite link on your device and accept **PDC Wallet** / PDC Mobile.
3. Install the latest available beta build (currently aligned with app version **3.1.0**).

Builds expire 90 days after upload. When the App Store listing is live, prefer the production app for everyday use.

## First launch

1. Install **PDC Wallet** from [TestFlight](https://testflight.apple.com/join/NwmhAhfi), or from the App Store when the listing is available.
2. Create a wallet or restore from seed. Choose a wallet password on the device.
3. Write the seed down offline. The app cannot recover funds if you never saved the phrase.
4. Wait until sync against the selected remote node catches up before sending large amounts.

Biometric unlock is optional and can be skipped. Reviewers and users can create an empty wallet without a demo seed.

## Remote node

The wallet syncs through a remote PDC node you select (default public nodes use plain HTTP JSON-RPC). The node sees your connection IP and any transaction you broadcast. Prefer a node you trust, or run your own daemon and point the app at it when the UI allows a custom remote.

The app allows non-HTTPS connections for node RPC because public nodes often speak plain HTTP. Wallet file encryption on device uses ordinary mass-market cryptography.

## Seed and security

Anyone with the seed or the spend key can spend the funds. Treat them like the desktop `show_seed` / `spendkey` secrets described in [GUI](gui.md#secrets). The publisher never receives your seed.

Back up the seed offline. Uninstalling the app without a backup means those funds are gone from that device.

## Network release alignment

Desktop/daemon releases follow [PrivacyDataCoin-Project/PDC](https://github.com/PrivacyDataCoin-Project/PDC). The iOS app version **3.1.0** is aligned with the PrivacyDataCoin **3.1.0** network line and PDC-only branding (bundle id, FFI, and product name). Keep the phone wallet and any node you rely on on a compatible network release.

## Source and builds

| Path | Role |
| --- | --- |
| [pdcwallet_ios](https://github.com/PrivacyDataCoin-Project/pdcwallet_ios) | Flutter iOS/Android shell + native plain-wallet FFI |
| `flutter-mobile/arqma_wallet_mobile/` | App project (version in `pubspec.yaml`) |
| `native/pdc_plain_wallet_ffi/` | C++ FFI (`pdc_wallet_ffi_*`, `libpdc_wallet_flutter_ffi`) |

Maintainers build and upload App Store / TestFlight packages from that tree. End users should install the signed App Store (or TestFlight) build, not an unsigned sideload.

## Related

- [GUI](gui.md) — desktop Qt wallet and `simplewallet`
- [Getting started](../use/getting-started.md) — desktop/CLI install files
- [Security and privacy](../use/security.md)

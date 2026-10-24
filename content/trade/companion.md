---
title: PDC Companion
---

[PDC Companion](https://trade.privacydatacoin.com/api/companion/download) is the browser extension that connects [trade.privacydatacoin.com](https://trade.privacydatacoin.com/) to a wallet running on your machine. Trade never receives your seed or spend key. Companion relays approved JSON-RPC calls to a local wallet and exposes `window.pdcExtension` so the site can read the address, sign a login challenge, pay hub trading fees in PDC, and build or accept Ionic Swap proposals.

The published version signal is [trade.privacydatacoin.com/companion/latest.json](https://trade.privacydatacoin.com/companion/latest.json) (also `/api/companion/info`). Prefer those URLs over a fixed version number in this page.

## What you need

| Piece | Role |
| --- | --- |
| Desktop wallet `Pdc` (release <a data-doc-release href="https://github.com/PrivacyDataCoin-Project/PDC/releases/latest"><span data-doc-version>v3.0.0</span></a>, build **3.0.0.11+** recommended) **or** `simplewallet` with RPC | Holds keys and signs |
| Chrome, Edge, Brave, or Firefox | Hosts the extension |
| Companion zip from Trade | Install as unpacked / temporary add-on |
| Synced node | Wallet must see the chain |

Companion does not replace the desktop wallet. Install the wallet first from [Getting started](getting-started.md), unlock it, then install the extension.

## Install the extension

### Chrome, Edge, Brave

1. Download the Chrome zip from Trade: [Companion (latest)](https://trade.privacydatacoin.com/api/companion/download), or use the **Companion** link on the Trade home page.
2. Unzip the archive to a folder you will keep (the browser loads that folder).
3. Open `chrome://extensions` (or `edge://extensions` / `brave://extensions`).
4. Enable **Developer mode** → **Load unpacked** → select the unzipped folder.
5. Reload [trade.privacydatacoin.com](https://trade.privacydatacoin.com/) and click **Connect Wallet**.

### Firefox

1. Download the Firefox source zip: [Companion (Firefox)](https://trade.privacydatacoin.com/api/companion/download?variant=firefox).
2. Open `about:debugging#/runtime/this-firefox` → **Load Temporary Add-on…** → select `manifest.json` inside the unzipped folder.
3. Temporary add-ons unload when Firefox restarts — reload them after a restart until a signed AMO build is listed.

Trade auto-approves origin `https://trade.privacydatacoin.com` in Companion’s Approved dApps list on install and update. Other origins need an explicit approve in Companion Settings before balance, transfer, or swap methods work.

## Point Companion at your wallet

Companion talks only to a wallet RPC on localhost. Pick one path.

### Path A — Qt desktop wallet (recommended for Trade)

1. Open `Pdc`, unlock the wallet you will use on Trade.
2. Settings → turn **Pdc Companion** **ON**.
3. Copy the **Secret** (regenerate if needed). This is the JWT secret for Companion RPC.
4. In the Companion extension: **Settings** → preset **Qt GUI Companion · 19211**.
5. Paste the Secret into the JWT secret field. Companion sends it as `Pdc-Access-Token` (HS256 over body hash). Port **19211** requires this secret.
6. Use **Test connection**. The popup should show your `Px` address and unlocked balances (PDC and whitelisted assets such as BTCX).

While the Qt wallet stays unlocked with Companion **ON**, the extension keeps the stored secret and probes RPC about once a minute (access tokens are minted per request, `exp` ~30 minutes). The secret is cleared only after wallet RPC has been unreachable for about **60 minutes** (Companion OFF or wallet closed), or when you clear it in Options.

With several wallets open in the GUI, Companion’s **Active wallet** dropdown (and the GUI sidebar) select which wallet dApps use. Switching the wallet publishes `accountsChanged` so Trade picks up the new address.

### Path B — simplewallet RPC

Start wallet RPC on the usual port (not the Qt Companion JWT port):

```text
simplewallet --wallet-file <path> --password <pass> \
  --daemon-address 127.0.0.1:19211 \
  --rpc-bind-ip 127.0.0.1 --rpc-bind-port 19212 \
  --rpc-login user:pass
```

In Companion Settings use preset **simplewallet · 19212** and the same RPC login. Do not paste a Qt JWT secret against port 19212, and do not point the extension at 19211 without the matching GUI Secret.

## Connect on Trade

1. Confirm the wallet is unlocked and Companion’s popup shows online / an address.
2. Open [trade.privacydatacoin.com](https://trade.privacydatacoin.com/).
3. Click **Connect Wallet**. Trade uses the `pdcExtension` bridge (`ExtensionBridge` from `@privacydatacoin/pdc_web3`).
4. Trade asks for a challenge, Companion signs it (`sign_message`), and the Trade API verifies with wallet RPC `verify_message`. A session JWT (default **24 h**) is stored for orders, bridge deposit/withdraw, and other authenticated calls.

Public market and bridge **read** endpoints do not need Companion. Creating deposits, withdrawals, and orders does.

## Matrix claim (Messenger web)

[matrix.privacydatacoin.com](https://matrix.privacydatacoin.com) uses the same `window.pdcExtension.signMessage` bridge — no Trade DevTools console:

1. Unlock Qt wallet + Companion (RPC e.g. **19211**).
2. Companion **0.1.17+** pre-approves `matrix.privacydatacoin.com` and `messenger.privacydatacoin.com`.
3. Claim → alias → **Request challenge** → **Sign with Companion** → set Matrix password → submit.

Older Companion: add those origins under Options → Approved dApps, then reload the Messenger tab.

## What Companion does on Trade

| Action | How |
| --- | --- |
| Sign in | Challenge → `sign_message` → Trade JWT |
| Show address / balances | Relayed `getaddress` / `getbalance` (origin must be approved for spend-class methods) |
| Bridge | Same login; Bitcoin invoice / burn flows stay in the Trade UI |
| Place / take Ionic Swap orders | `createSwapProposal` / `acceptSwapProposal` → wallet `ionic_swap_*` |
| Switch wallet | Popup **Active wallet** (Qt multi-wallet) → Trade re-reads the address |

Keys never leave the wallet process. The extension stores RPC credentials in `chrome.storage.local` for the background worker only; pages do not see them.

## Updates

Companion compares its `manifest.json` version to the Trade latest signal. When older:

- In the popup, **Update** can download the published zip and, via the File System Access picker, write into the unpacked install folder, then reload.
- On Trade, a banner can **Replace extension** the same way when the browser allows folder access.
- Fallback: download the zip from `/api/companion/download`, replace files manually, then **Reload** on `chrome://extensions`.

Release notes and tagged builds: [PrivacyDataCoin-Project/pdc_web3 releases](https://github.com/PrivacyDataCoin-Project/pdc_web3/releases) (`extension-v*` tags).

## Security notes

- Never paste a seed phrase into Trade or into a website. Companion does not ask for the seed.
- Keep the Qt Companion **Secret** private. Anyone with the secret and access to `127.0.0.1:19211` can call wallet RPC as that wallet. RPC still requires Companion **ON** in the unlocked wallet; the extension does not force-rotate the secret on a short timer while the wallet is up.
- Bind wallet RPC to `127.0.0.1` only. Do not expose 19211/19212 to the internet.
- Verify the site origin is `https://trade.privacydatacoin.com` before approving connection prompts for other dApps.
- Unapproved origins receive error `-32010` on privileged methods.

## Troubleshooting

| Symptom | What to check |
| --- | --- |
| Trade: Companion not detected | Extension enabled; reload the Trade tab; confirm `window.pdcExtension` after install |
| Matrix claim: Companion not detected / `-32010` | Reload Messenger; update Companion to **0.1.17+** or approve Matrix origins in Options |
| Popup: unreachable / HTTP 401 | Wrong port or credentials; Qt needs Secret on **19211**; simplewallet uses **19212** + `--rpc-login` |
| Connect works, login fails | Wallet unlocked; build **3.0.0.11+** for JWT/`verify_message`; daemon synced |
| Take / swap stuck on wrong address | Active wallet in Companion popup matches the wallet you intend; reconnect on Trade after switch |
| Accept swap fails after update | Reload Companion on `chrome://extensions`; update from Trade if the banner offers Replace |
| Firefox add-on gone | Temporary add-ons reset on quit — load `manifest.json` again |

## Related

- [Trade](trade.md) — exchange, fees, Easy Swap
- [Bridge](bridge.md) — BTCX and ARQX wrap flows
- [Trade API](api.md) — JWT auth and public endpoints
- [Wallets](../use/wallets.md) — desktop wallet and `simplewallet`
- [Getting started](../use/getting-started.md) — install and sync
- [Escrow, swaps, and offers](../build/services.md) — Ionic Swap context in the protocol

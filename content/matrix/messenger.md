---
title: PDC Messenger
---

PDC Messenger is the first-party Matrix chat for Privacy Data Coin. Your Matrix user is your on-chain [alias](../build/aliases.md): `@alias:privacydatacoin.com`. Ownership is proven with a wallet signature. Public Synapse registration is disabled — accounts are created only through the claim flow.

| Piece | Address |
| --- | --- |
| Web app + homeserver | [matrix.privacydatacoin.com](https://matrix.privacydatacoin.com) |
| Matrix user | `@youralias:privacydatacoin.com` |
| Claim API | `https://matrix.privacydatacoin.com/claim/` |
| Health check | [matrix.privacydatacoin.com/claim/health](https://matrix.privacydatacoin.com/claim/health) |

## How it works

1. You register a PDC alias on-chain (GUI / simplewallet). The name is public; transfers that use it stay confidential.
2. On Messenger you open **Claim**, enter the alias, and request a challenge (`PDC-MATRIX-CLAIM/v1` …).
3. The unlocked desktop wallet signs that message (spend key) via [PDC Companion](../trade/companion.md), or you paste a Schnorr signature from wallet RPC `sign_message`.
4. The claim service checks the alias on-chain, verifies the signature, and creates (or resets) `@alias:privacydatacoin.com` on Synapse with the Matrix password you chose.
5. You sign in. Room messages use Matrix E2EE (Megolm). Wallet private keys never leave the wallet process.

The homeserver name is the apex `privacydatacoin.com`. Clients discover it through well-known at that domain and talk to Synapse on `matrix.privacydatacoin.com`.

## What you need before claiming

| Piece | Role |
| --- | --- |
| PDC alias (≥ 7 characters for a **new** Matrix account) | Becomes the Matrix localpart |
| Desktop wallet unlocked ([Getting started](../use/getting-started.md)) | Holds the alias owner spend key |
| [PDC Companion](../trade/companion.md) **0.1.18+** | Signs the challenge in the browser (`window.pdcExtension.signMessage`) |
| Browser on [matrix.privacydatacoin.com](https://matrix.privacydatacoin.com) | Claim UI (Companion signing is web-only) |

Short aliases (≤ 6 characters) cannot create a Matrix account through the public claim form. Those names are reserved / pre-provisioned. If such an account already exists, a valid wallet signature can still **reset the Matrix password**.

## Register (claim) a Matrix account

1. Unlock the Qt wallet. Turn **Pdc Companion** **ON** and copy the Companion **Secret** into the extension (preset **Qt GUI Companion · 19211**). Details: [PDC Companion](../trade/companion.md).
2. Install or update Companion to **0.1.18+**. That build pre-approves `https://matrix.privacydatacoin.com`. Older builds: add the origin under Options → Approved dApps, then reload the Messenger tab.
3. Open [matrix.privacydatacoin.com](https://matrix.privacydatacoin.com) → **Claim**.
4. Enter your alias (for example `alice12`, `@alice12`, or `@alice12:privacydatacoin.com`) → **Request challenge**.
5. Click **Sign with Companion**. The Signature field fills with a Schnorr signature (128 hex chars, or base64 of 64 bytes). Do not paste a seed, spend key, or Companion JWT secret.
6. Choose a Matrix password → **Claim / reset password & sign in**. Messenger logs you in as `@alice12:privacydatacoin.com`.

Without Companion you can still copy the challenge text, sign it with wallet RPC `sign_message`, and paste the signature. Prefer Companion on web.

Claim again with a valid signature when you need to **reset** the Matrix password for an existing account.

## Sign in (existing account)

On the login screen enter your alias (or full `@alias:privacydatacoin.com`) and the Matrix password you set at claim time. No wallet signature is required for ordinary login.

## Encryption keys between devices

Matrix cannot decrypt history on a new device without keys. PDC Messenger follows the same model as Element:

1. On a device that already works, open **Settings**.
2. **Create & export recovery key** (or **Export recovery key**). Store it offline — never share it.
3. On the new device, **Settings** → paste under **Import** → **Import recovery key**.
4. Leave **Sync history across my devices** enabled so online devices can answer key requests.

**Sign out other sessions** removes old logins. Prefer a fresh message after fixing sessions rather than expecting every historical “Cannot decrypt” bubble to recover.

## Rooms and Telegram

Community rooms include `#general`, `#announcements`, `#community`, and `#trade` on `privacydatacoin.com`. Prefer encrypted rooms; the UI shows a lock when E2EE is active.

`#general` can bridge both ways with Telegram `@privacydatacoin` (bot `@PDCNetworkBot`). Bridge user on Matrix: `@tgbridge:privacydatacoin.com`. Messages use prefixes `[TG]` / `[Matrix]` to avoid loops.

| Direction | Requirement |
| --- | --- |
| Telegram → Matrix | Bot can read group messages; bot is admin in the Telegram group |
| Matrix → Telegram | Your client shares Megolm session keys with `@tgbridge` (recovery import + sync, or send a **new** message after sessions are cleaned) |

If a bubble says **Cannot decrypt — missing Megolm session key**, tap **Request keys** while another of your devices (or the bridge, for bridge-sent messages) is online.

## Clients

| Surface | How to run |
| --- | --- |
| Web | [matrix.privacydatacoin.com](https://matrix.privacydatacoin.com) |
| Desktop (macOS / Linux / Windows) | **PDC Matrix Messenger** release builds (GPG `FAB8833900C876FF`) |
| iOS / Android | **PDC Messenger** (iOS signed; Android scaffold / local APK) |

Desktop claim still needs a browser + Companion for one-click signing, or a pasted `sign_message` signature. Companion is not available inside the native desktop shell.

## Troubleshooting

| Symptom | What to check |
| --- | --- |
| Companion not detected / `-32010` | Extension enabled; reload Messenger; Companion **0.1.18+** or approve `matrix.privacydatacoin.com` in Options |
| Signature rejected | Wallet unlocked; active wallet owns the alias; challenge not expired; signature is 128 hex or base64 of 64 bytes |
| `create_not_allowed` | Alias ≤ 6 characters — public create blocked; use a longer alias, or reset only if the Matrix user already exists |
| Login fails after claim | Use the Matrix password you just set; user id is `@alias:privacydatacoin.com` |
| Cannot decrypt | Export/import recovery key; keep another session online; send a new message after key share |
| Claim health down | Check [claim/health](https://matrix.privacydatacoin.com/claim/health) and [client versions](https://matrix.privacydatacoin.com/_matrix/client/versions) |

## Security notes

- Wallet keys never leave the wallet. Only a challenge signature and a Matrix password go to the claim service.
- The Matrix password is separate from the wallet password. Treat it like any chat login secret.
- Alias names are public on-chain. Chat content in E2EE rooms is not readable by the homeserver in cleartext when encryption works as designed.
- Bind wallet RPC to `127.0.0.1` only. Do not expose Companion ports to the internet.

## Related

- [Aliases](../build/aliases.md) — on-chain names and fees
- [PDC Companion](../trade/companion.md) — signing bridge for Trade and Matrix claim
- [Getting started](../use/getting-started.md) — install the desktop wallet
- [Security and privacy](../use/security.md) — what the chain hides vs what you protect
- [Troubleshooting](../use/troubleshooting.md) — node and sync issues

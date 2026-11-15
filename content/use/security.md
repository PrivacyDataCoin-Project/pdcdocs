---
title: Security and privacy
---

PDC hides wallet fields by default. That is a property of the transaction, not a switch you remember to turn on. Several other things stay visible, and several secrets stay entirely in your hands.

## Hidden on a wallet transfer

The published address, the amount, and the asset type do not appear in the clear. The real input is one member of a ring of 10 decoys, or 15 after hard fork 4. The range proof shows the amounts are valid. It does not show the amounts.

## Not hidden

- **The alias directory.** A registered name points at an address. Anyone can resolve it with `get_alias_details` or `get_alias_by_address`. The transfers to that address are still confidential. The name itself is a public record.
- **Asset administration.** Creating an asset, minting, burning, and changing its owner are explicit transactions. Only the later ordinary transfers of the token are blinded.
- **Your node's network address.** Peer-to-peer traffic uses port 19121. The protocol does not hide the IP address of a node you run in the clear. Transaction relay can go over Tor. The node's own listener is still a normal TCP port.
- **Proof of work.** A mined block shows that someone did RandomARQ work. It does not show a miner's PDC balance.
- **Stake timing, not the stake size.** After height 100, Zarcanum keeps the staked amount sealed. The fact that a proof-of-stake block exists is public. An observer still cannot read the balance from that block.

## What you must store

The 26-word seed and the spend key spend the funds. The view key recognizes incoming outputs. The wallet password encrypts the local file. Lose the seed and the password together and the funds are not recoverable from the chain. There is no custodian account in the protocol.

Write the seed on paper or stamp it into metal. A screenshot in a cloud photo library is a copy you do not control.

## The node RPC

`daemon` binds RPC to `127.0.0.1:19211` unless you set `--rpc-bind-ip`. Methods such as `decrypt_tx_details` are documented in the source as something to run only against your own daemon. Do not publish port 19211 on a public interface so that a website can call it.

`start_mining` on that RPC starts CPU mining toward an address you pass in. On a shared host, a reachable RPC is a way for someone else to point your CPUs at their address.

## Auditable wallets

An auditable address (`aPx` or `aiPX`) and `tracking_seed` exist so you can show a reviewer what the wallet received and spent. Hand that seed only to the reviewer. It is not required for ordinary use.

## Confirmations

Spend mined coins after 10 blocks. Stake an output after it is 10 blocks old. A transaction can remain in the mempool for up to 4 days. If it expires or the fee is below 0.01 PDC, it will not confirm.

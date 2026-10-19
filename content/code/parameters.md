---
title: Network parameters
---

Mainnet values from `src/currency_core/currency_config.h` unless a row says otherwise. Testnet builds redefine ports and hard-fork heights. Do not mix the two columns on one node.

| Parameter | Mainnet |
| --- | --- |
| Ticker | `PDC` |
| Formation version | 100 |
| Genesis | `df35cba557c857756f20612ce3c9d2aa315d0ae8fc2aaffe6c5c59d37e00b10a` |
| Premine | 0 |
| Base block reward after genesis | 1 PDC |
| Decimals | 12 |
| Default and minimum fee | 0.01 PDC |
| Block target | 60 seconds |
| Proof-of-work target | 120 seconds |
| Proof-of-stake target | 120 seconds |
| Proof of work | RandomARQ, epoch 2,048, 43-byte blob, nonce at byte 39 |
| Proof of stake | From height 0. Coinstake age 10. Zarcanum after height 100 |
| Longest proof-of-stake run | 21 blocks |
| Decoys | 10 default, 15 mandatory after hard fork 4 |
| Minimum outputs after hard fork 4 | 2 |
| Maximum inputs | 256 |
| Maximum outputs | 2,000 |
| Coinbase unlock | 10 blocks |
| Full reward zone | 125,000 bytes |
| Peer-to-peer port | 19121 |
| RPC port | 19211, bound to `127.0.0.1` |
| Stratum port | 19777 |
| Seed | `169.58.142.131:19121` |
| Default peer connections | 8 |
| Mempool lifetime | 4 days |
| Hard fork 1 | after height 20 |
| Hard fork 2 | after height 40 |
| Hard fork 3 | after height 60 |
| Hard fork 4 | after height 100 |
| Hard forks 5, 6, and 7 | after height 1199 (activate together) |
| Alias minimum public length | 6 |
| Alias fee | Burned. Cost follows a 7-day median |
| Asset whitelist | `https://api.privacydatacoin.com/assets_whitelist.json` |
| Data directory | `~/.PDC` on Linux |

## Testnet differences

A binary configured with `-D TESTNET=TRUE` uses:

| Parameter | Testnet |
| --- | --- |
| Peer-to-peer port | 19311 (`19211 + formation version`) |
| RPC port | 19111 |
| Stratum port | 19888 |
| Hard forks 1, 2, and 3 | after height 0 |
| Hard fork 4 | after height 100 |
| Hard forks 5, 6, and 7 | after height 1199 (same as mainnet) |
| Asset whitelist | `https://api.privacydatacoin.com/assets_whitelist_testnet.json` |

The testnet seed line in `net_node.inl` points at the same host with the testnet peer port. The network id flag `P2P_NETWORK_ID_TESTNET_FLAG` is 1, so a testnet node will not handshake as mainnet.

## Emission arithmetic

`CURRENCY_BLOCKS_PER_DAY` is `86400 / 60 = 1440`. At 1 PDC per block that is 1,440 PDC a day and `1440 * 365 = 525600` PDC in a 365-day year, before any blocks that took a size penalty and before the zero genesis reward. Nothing in `get_base_block_reward` stops this issuance.

---
title: Node RPC
---

The daemon serves JSON on port 19211. The bind address defaults to `127.0.0.1` (`--rpc-bind-ip`). Calls go to `/json_rpc` unless a legacy path is listed below.

```text
curl -s http://127.0.0.1:19211/json_rpc \
  -H 'Content-Type: application/json' \
  -d '{"jsonrpc":"2.0","id":"0","method":"getinfo","params":{"flags":0}}'
```

`getinfo` always returns a base set of fields. Heavier fields are included only when you set `flags` to a bitwise OR of the constants in `core_rpc_server_commands_defs.h`.

| Flag constant | Bit |
| --- | --- |
| `COMMAND_RPC_GET_INFO_FLAG_POS_DIFFICULTY` | `0x1` |
| `COMMAND_RPC_GET_INFO_FLAG_POW_DIFFICULTY` | `0x2` |
| `COMMAND_RPC_GET_INFO_FLAG_NET_TIME_DELTA_MEDIAN` | `0x4` |
| `COMMAND_RPC_GET_INFO_FLAG_CURRENT_NETWORK_HASHRATE_50` | `0x8` |
| `COMMAND_RPC_GET_INFO_FLAG_CURRENT_NETWORK_HASHRATE_350` | `0x10` |
| `COMMAND_RPC_GET_INFO_FLAG_SECONDS_FOR_10_BLOCKS` | `0x20` |
| `COMMAND_RPC_GET_INFO_FLAG_SECONDS_FOR_30_BLOCKS` | `0x40` |
| `COMMAND_RPC_GET_INFO_FLAG_TRANSACTIONS_DAILY_STAT` | `0x80` |
| `COMMAND_RPC_GET_INFO_FLAG_LAST_POS_TIMESTAMP` | `0x100` |
| `COMMAND_RPC_GET_INFO_FLAG_LAST_POW_TIMESTAMP` | `0x200` |
| `COMMAND_RPC_GET_INFO_FLAG_TOTAL_COINS` | `0x400` |
| `COMMAND_RPC_GET_INFO_FLAG_LAST_BLOCK_SIZE` | `0x800` |
| `COMMAND_RPC_GET_INFO_FLAG_TX_COUNT_IN_LAST_BLOCK` | `0x1000` |
| `COMMAND_RPC_GET_INFO_FLAG_POS_SEQUENCE_FACTOR` | `0x2000` |
| `COMMAND_RPC_GET_INFO_FLAG_POW_SEQUENCE_FACTOR` | `0x4000` |
| `COMMAND_RPC_GET_INFO_FLAG_OUTS_STAT` | `0x8000` |
| `COMMAND_RPC_GET_INFO_FLAG_PERFORMANCE` | `0x10000` |
| `COMMAND_RPC_GET_INFO_FLAG_POS_BLOCK_TS_SHIFT_VS_ACTUAL` | `0x20000` |
| `COMMAND_RPC_GET_INFO_FLAG_MARKET` | `0x40000` |
| `COMMAND_RPC_GET_INFO_FLAG_EXPIRATIONS_MEDIAN` | `0x80000` |

`0xffffffffffffffff` requests every flag. That call is heavier. Use the bits you need.

## JSON-RPC methods

These names are the strings in `BEGIN_JSON_RPC_MAP("/json_rpc")`. Descriptions are shortened from the `DOC_COMMAND` text in the same header.

| Method | What it returns or does |
| --- | --- |
| `getblockcount` | Height of the top block, plus one |
| `on_getblockhash` | Block hash at a height |
| `getblocktemplate` | A mining template for proof of work or proof of stake |
| `submitblock` | Submit one hex-encoded block blob |
| `submitblock2` | Submit a new block |
| `getlastblockheader` | Header of the tip |
| `getblockheaderbyhash` | Header for a hash |
| `getblockheaderbyheight` | Header for a height |
| `get_alias_details` | One alias |
| `get_alias_by_address` | Aliases registered to an address |
| `get_alias_reward` | Current alias registration cost |
| `get_est_height_from_date` | A height estimate for a date |
| `find_outs_in_recent_blocks` | Outputs in recent blocks for an address plus its secret view key. Run this against your own node |
| `get_blocks_details` | Block details from a starting height |
| `get_tx_details` | One transaction's public details |
| `search_by_id` | Search blocks, transactions, key images, multisig outputs, and alternative blocks |
| `getinfo` | Node and chain summary. See the flags above |
| `get_out_info` | Transaction id and local output index for an amount and a global index |
| `get_multisig_info` | A multisig output by its hash |
| `get_all_alias_details` | Every alias |
| `get_aliases` | A page of aliases |
| `get_pool_txs_details` | Full pool entries by id |
| `get_pool_txs_brief_details` | Short pool entries by id |
| `get_all_pool_tx_list` | Every pool transaction id |
| `get_pool_info` | Pool summary |
| `getrandom_outs` | Legacy decoys |
| `getrandom_outs1` | Decoy outputs for mixing |
| `getrandom_outs3` | Decoys, choosing the pre-Zarcanum or post-Zarcanum zone from the amount |
| `get_votes` | Vote totals over a block range |
| `get_asset_info` | One asset by id |
| `get_assets_list` | Assets registered on the chain |
| `decrypt_tx_details` | Decrypt private transaction fields. The source says to use this only on your local daemon |
| `get_main_block_details` | One main-chain block by hash |
| `get_alt_block_details` | One alternative block by hash |
| `get_alt_blocks_details` | Alternative blocks, paged |
| `reset_transaction_pool` | Clear the pool |
| `remove_tx_from_pool` | Drop specific pool transactions |
| `get_current_core_tx_expiration_median` | The median the core uses for transaction expiration |
| `marketplace_global_get_offers_ex` | Marketplace offers that match a filter |
| `validate_signature` | Check a Schnorr signature. The public key can be passed directly or loaded from an alias |

## Legacy HTTP paths

These are separate from `/json_rpc`. A wallet still uses several of the binary ones.

| Path | Role |
| --- | --- |
| `POST /getheight` | Height |
| `POST /gettransactions` | Transactions by id |
| `POST /sendrawtransaction` | Broadcast one raw transaction |
| `POST /force_relay` | Relay a list of raw transactions |
| `POST /start_mining` | Start CPU proof-of-work mining. Body includes `miner_address` and `threads_count` |
| `POST /stop_mining` | Stop that miner |
| `POST /getinfo` | Same info call as the JSON-RPC method |
| `POST /getblocks.bin` | Binary block sync |
| `POST /get_o_indexes.bin` | Global output indexes |
| `POST /getrandom_outs.bin`, `/getrandom_outs1.bin`, `/getrandom_outs3.bin` | Binary decoy selection |
| `POST /get_tx_pool.bin` | Binary pool fetch |
| `POST /check_keyimages.bin` | Spent status of key images |
| `POST /get_pos_details.bin` | Proof-of-stake mining details |

The `.bin` routes are the wallet's sync protocol. Integrate with the JSON methods unless you are writing a wallet and are prepared to match the binary layout in `core_rpc_server_commands_defs.h`.

Field-level schemas live in that header as `KV_SERIALIZE` entries. This page names the surface so you can find the struct. It does not duplicate every field.

## Public remote node (allowlist)

Mainnet host `169.58.142.131:19211` is a **filtered** public endpoint for iOS / remote wallets (sync + `sendrawtransaction`). Full RPC (including mining) stays on **localhost** for the pool and operators.

- HTTP allow: `getinfo`, `getheight`, `gettransactions`, `sendrawtransaction`, selected `.bin` sync routes
- HTTP deny: `start_mining`, `stop_mining`, …
- `/json_rpc`: method allowlist via `pdcd-json-rpc-filter` (mining methods → 403)

There is **no public EVM L2** RPC. Oracle attestation may use a private Clique geth on localhost only. Policy and ops files: [PDC `docs/PDCD_PUBLIC_RPC_POLICY.md`](https://github.com/PrivacyDataCoin-Project/PDC/blob/dev/docs/PDCD_PUBLIC_RPC_POLICY.md) and `ops/pdcd-public-rpc/`.

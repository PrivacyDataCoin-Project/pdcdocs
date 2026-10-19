---
title: How PDC works
---

A PDC transaction is a proof that value moved, plus the minimum data a wallet needs to find its own outputs. Observers can check the proof. They cannot read the wallet fields.

## Addresses

The published address is for people you give it to. It does not appear on the chain as the receiver of a transfer.

| Prefix | Kind | Source constant |
| --- | --- | --- |
| `Px` | Standard address | `CURRENCY_PUBLIC_ADDRESS_BASE58_PREFIX` (`0x1989`) |
| `iP` | Integrated address, carries a payment id | `CURRENCY_PUBLIC_INTEG_ADDRESS_BASE58_PREFIX` |
| `aPx` | Auditable address | `CURRENCY_PUBLIC_AUDITABLE_ADDRESS_BASE58_PREFIX` |
| `aiPX` | Auditable integrated address | `CURRENCY_PUBLIC_AUDITABLE_INTEG_ADDRESS_BASE58_PREFIX` |

An integrated address lets a sender attach a payment id without a separate field. An auditable wallet can hand a tracking seed to a reviewer. That seed is for the reviewer you choose. It is not published by a normal transfer.

The wallet recovery phrase is 24 words. `simplewallet` prints it with `show_seed`. The spend key and the view key are separate secrets (`spendkey`, `viewkey`).

## The privacy stack

1. **Stealth outputs.** Each output pays a one-time address derived for that transfer.
2. **d/v-CLSAG.** The signature proves you own one input in a ring. It does not tell an observer which one. Decoys default to 10 and become 15 after hard fork 4.
3. **Commitments and Bulletproofs+.** Pedersen commitments hide the value. The `bpp` range proof shows the hidden values are consistent.
4. **Blinded asset ids.** A wallet transfer does not announce whether the output is native PDC or a token issued on the chain.
5. **Zarcanum.** After height 100, proof of stake uses Zarcanum. The chance of producing a stake block follows the coins you stake. The amount stays sealed.

Transaction version 2 is the post-hard-fork-4 version. From that fork, a transaction has at least 2 outputs. Inputs are capped at 256, mainly by the asset surjection proof. Outputs are capped at 2,000.

## Fees and unlock

The default fee and the minimum fee are both 0.01 PDC (`TX_DEFAULT_FEE` and `TX_MINIMUM_FEE`). Coinbase outputs unlock after 10 blocks (`CURRENCY_MINED_MONEY_UNLOCK_WINDOW`). A coinstake must also be at least 10 blocks old before it can stake.

## Blocks and emission

`get_base_block_reward` returns `PREMINE_AMOUNT` at height 0 and `CURRENCY_BLOCK_REWARD` at every later height. Those values are 0 and 1 PDC. There is no supply cap in this function.

Difficulty is adjusted over a window of 720 blocks, with a lag of 15 and a cut of 60 timestamps. The proof-of-work target and the proof-of-stake target are 120 seconds each. `DIFFICULTY_TOTAL_TARGET` is their sum divided by 4, which is 60 seconds. `CURRENCY_BLOCKS_PER_DAY` is therefore 1,440.

Proof-of-stake blocks cannot run forever in a row. `BLOCK_POS_STRICT_SEQUENCE_LIMIT` is 20, so the longest allowed run is 21 sequential proof-of-stake blocks.

## Hard forks

Mainnet heights are fixed in `currency_config.h`. Hard forks 5, 6, and 7 share one height and activate together after block 1199.

| Fork | Active after height | What changes for a user |
| --- | --- | --- |
| 1 | 20 | Early consensus rules |
| 2 | 40 | Early consensus rules |
| 3 | 60 | Block version moves forward |
| 4 Zarcanum | 100 | Mandatory 15 decoys, minimum coin age 10, transaction version 2, Zarcanum stake, confidential assets in their post-fork form |
| 5–7 | 1199 | HF5 asset-operation validation path (`validate_asset_operation_hf5`); HF6 and HF7 share the same height. Nodes need min build 4 |

The comments next to the mainnet heights record historical timestamps from the code's lineage. On this network the heights are the rules that matter: fork 4 is already active past block 100, and forks 5–7 are active past block 1199.

## Mempool and reorgs

A transaction can sit in the pool for 345,600 seconds (4 days) before the lifetime rule drops it. Alternative blocks are kept for a limited time: the live window is about 2 hours of blocks (`CURRENCY_ALT_BLOCK_LIVETIME_COUNT`), and the stored set is capped at 43,200 entries.

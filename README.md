# CAT Snapshot Generator

Generates a snapshot of CAT balances for every address at a target block height.

Runs within a docker image that contains a running full node, making this easy to run anywhere without needing to connect to a remote full node.

## Configuration

Environment variables should be passed to configure the behavior of the tool:

* `START_HEIGHT` - The height of the blockchain to start creating the snapshot from (default: `0`)
* `TARGET_HEIGHT` - The height of the blockchain to end the snapshot (no default - must be set)


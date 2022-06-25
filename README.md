# CAT Snapshot Generator

Generates a snapshot of all CAT coins at a target block height.

## Configuration

Environment variables should be passed to configure the behavior of the tool:

* `TESTNET` - Whether to run against testnet or mainnet. true=testnet, false=mainnet
* `FULL_NODE_HOSTNAME` - Hostname of full node to call RPCs against
* `DB_SOURCE_DIR` - Location of full node database on host machine
* `START_HEIGHT` - The height of the blockchain to start creating the snapshot from (default: `0`)
* `TARGET_HEIGHT` - The height of the blockchain to end the snapshot (no default - must be set)

These can be set by creating a `.env` file in the root of this project. Example:

```
TESTNET=false
FULL_NODE_HOSTNAME=localhost
DB_SOURCE_DIR=/home/freddie/chia-mount/db/
START_HEIGHT=1146800
TARGET_HEIGHT=1149800
```

## Commands

First you need to setup the database with the following command:

```
python3 setup_database.py 
```

Then you can run the snapshot generator with the following command:

```bash
python3 start.py 
```

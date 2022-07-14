# CAT Snapshot Generator

Generates a snapshot of all CAT coins at a target block height.

## Configuration

Environment variables should be passed to configure the behavior of the tool:

* `FULL_NODE_HOSTNAME` - Hostname of full node to call RPCs against
* `DB_SOURCE_DIR` - Location of full node database on host machine
* `START_HEIGHT` - The height of the blockchain to start creating the snapshot from (default: `0`)
* `TARGET_HEIGHT` - The height of the blockchain to end the snapshot (no default - must be set)

These can be set by creating a `.env` file in the root of this project. Example:

```
FULL_NODE_HOSTNAME=localhost
DB_SOURCE_DIR=/home/freddie/chia-mount/db/
START_HEIGHT=1146800
TARGET_HEIGHT=1149800
```

## Commands

First you need to install dependencies:

```bash
python3 setup.py install
```

Then setup the database:

```bash
python3 setup_database.py 
```

Now you can run the snapshot generator with the following command:

```bash
python3 start.py 
```

## Queries

Once you have populated the database with a snapshot you can run a data export with the following commands.

### Balance of Spacebucks

To generate a CSV containing all Spacebucks inner puzzle hashes and amounts:

```
python3 export.py --output-dir /Users/freddiecoleman/code/CAT-addresses/results/ --tail-hash 78ad32a8c9ea70f27d73e9306fc467bab2a6b15b30289791e37ab6e8612212b1
```

### Balance of all CATs in one file

To generate a CSV containing all CATs TAIL hashes, inner puzzle hashes and amounts:

```
python3 export.py --output-dir /Users/freddiecoleman/code/CAT-addresses/results/
```

### Balance of all CATs in seperate files

To generate multiple CSVs with each containing a specific CATs inner puzzle hashes and amounts:

```
python3 export.py --output-dir /Users/freddiecoleman/code/CAT-addresses/results/ --explode
```

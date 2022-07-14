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

## Data export

Once you have populated the database with a snapshot you can run a data export with the following commands.

### Balance of Spacebucks

To generate a CSV containing all Spacebucks inner puzzle hashes and amounts:

```
python3 export.py --output-dir /Users/freddiecoleman/code/CAT-addresses/results/ --tail-hash 78ad32a8c9ea70f27d73e9306fc467bab2a6b15b30289791e37ab6e8612212b1
```

To get individual coins:

```
python3 export.py --output-dir /Users/freddiecoleman/code/CAT-addresses/results/ --tail-hash 78ad32a8c9ea70f27d73e9306fc467bab2a6b15b30289791e37ab6e8612212b1 --coins
```

### Balance of all CATs in one file

To generate a CSV containing all CATs TAIL hashes, inner puzzle hashes and amounts:

```
python3 export.py --output-dir /Users/freddiecoleman/code/CAT-addresses/results/
```

To get individual coins:

```
python3 export.py --output-dir /Users/freddiecoleman/code/CAT-addresses/results/ --coins
```

### Balance of all CATs in seperate files

To generate multiple CSVs with each containing a specific CATs inner puzzle hashes and amounts:

```
python3 export.py --output-dir /Users/freddiecoleman/code/CAT-addresses/results/ --explode
```

To get individual coins:

```
python3 export.py --output-dir /Users/freddiecoleman/code/CAT-addresses/results/ --explode --coins
```

### Data cleanup

Data cleanup should only be required if the application exits half-way through a run meaning it only imports some blocks at a particular height.

This could happen if the computer crashes or there is a power cut.

The command will delete records from the database at and above a provided height.

```
python3 clean.py --height 2232000
```

## Secure the bag with CAT-admin-tool

If you want to feed data into the CAT-admin-tool for use with Secure the bag you should run the following command:

```
python3 export.py --output-dir /Users/freddiecoleman/code/CAT-addresses/results/ --tail-hash 78ad32a8c9ea70f27d73e9306fc467bab2a6b15b30289791e37ab6e8612212b1
```

The order of this data is important so don't change it. This is because your wallet will increase the range of keys used for puzzle hash discovery as puzzle hashes at greater offsets come in. If you import data in a different order you may need to change your config to increase the range of keys that your wallet is checking.

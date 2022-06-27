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

Once you have populated the database with a snapshot you can run queries, some examples follow.

### Entire balance of Spacebucks

This queries the total amount of Spacebucks at the height of the snapshot.

```
sqlite> select sum(coin_create.amount) from coin_create left join coin_spend on coin_create.coin_name = coin_spend.coin_name where coin_create.tail_hash = '78ad32a8c9ea70f27d73e9306fc467bab2a6b15b30289791e37ab6e8612212b1' and coin_spend.coin_name is null;
1000000000000
```

There are 1,000 mojos to a CAT so the result of this query indicates that the total supply of Spacebucks is 1,000,000,000.
from collections import defaultdict
import click
import csv
import sqlite3

from datetime import datetime
from sqlite3 import Cursor
from typing import List
from src.database import get_all_cat_balances, get_cat_balance

"""
Runs SQL queries and export as CSV.
"""

def seperate_by_tail_hash(rows: List[any], coins: bool):
    tail_data = defaultdict(list)

    if coins:
        for (tail_hash, coin_name, inner_puzzle_hash, amount) in rows:
            tail_data[tail_hash].append((coin_name, inner_puzzle_hash, amount))
    else:
        for (tail_hash, inner_puzzle_hash, amount) in rows:
            tail_data[tail_hash].append((inner_puzzle_hash, amount))

    return tail_data


@click.command()
@click.pass_context
@click.option(
    "-t",
    "--tail-hash",
    required=False,
    help="The TAIL hash of CAT to export data for",
)
@click.option(
    "-e",
    "--explode",
    required=True,
    is_flag=True,
    default=False,
    help="Generate a CSV for every TAIL",
)
@click.option(
    "-o",
    "--output-dir",
    required=True,
    help="Directory to write CSV output",
)
@click.option(
    "-c",
    "--coins",
    required=True,
    is_flag=True,
    default=False,
    help="Show individual coins in output rather than collapsing on puzzle hash",
)
def cli(
    ctx: click.Context,
    tail_hash: str,
    explode: bool,
    output_dir: str,
    coins: bool
):
    ctx.ensure_object(dict)
    now = datetime.now()
    file_name = f"{now.timestamp()}.csv"
    data = None

    if tail_hash:
        # Run export for specific CAT
        data = get_cat_balance(tail_hash, coins)
        file_name = f"{tail_hash}." + file_name
    else:
        data = get_all_cat_balances(coins)
        file_name = "all." + file_name
    
    if explode:
        tail_data = seperate_by_tail_hash(data, coins)

        for (tail_hash, rows) in tail_data.items():
            with open(output_dir + f"{tail_hash}" + f".{file_name}", 'w') as f:
                writer = csv.writer(f)
                writer.writerows(rows)
    else:
        with open(output_dir + file_name, 'w') as f:
            writer = csv.writer(f)
            writer.writerows(data)

def main():
    cli()


if __name__ == "__main__":
    main()
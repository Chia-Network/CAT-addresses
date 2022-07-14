from collections import defaultdict
import click
import csv
import sqlite3

from datetime import datetime
from sqlite3 import Cursor
from typing import List
from src.database import delete_coins_above, get_all_cat_balances, get_cat_balance

"""
Deletes data from database above a specified height.

Should only be used if the tool crashes or exits mid-way through a run e.g. due to a power cut.
"""

def seperate_by_tail_hash(rows: List[any]):
    tail_data = defaultdict(list)

    for (tail_hash, inner_puzzle_hash, amount) in rows:
        tail_data[str(tail_hash)].append((str(inner_puzzle_hash), int(amount)))

    return tail_data


@click.command()
@click.pass_context
@click.option(
    "-h",
    "--height",
    required=False,
    help="Data at and above this height will be wiped from the database",
)
def cli(
    ctx: click.Context,
    height: int
):
    ctx.ensure_object(dict)
    
    print(f"Deleting coin records created or spent at and above block {height}")
    
    delete_coins_above(height)

    print("Data cleanup complete")

def main():
    cli()


if __name__ == "__main__":
    main()
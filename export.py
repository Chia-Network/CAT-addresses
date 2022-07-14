import click
import csv
import sqlite3

from sqlite3 import Cursor
from datetime import datetime
from src.database import get_all_cat_balances, get_cat_balance

"""
Runs SQL queries and export as CSV.
"""


@click.command()
@click.pass_context
@click.option(
    "-t",
    "--tail-hash",
    required=False,
    help="The TAIL hash of CAT to export data for",
)
@click.option(
    "-o",
    "--output-file-path",
    required=True,
    help="Path to file to write CSV output",
)
def cli(
    ctx: click.Context,
    tail_hash: str,
    output_file_path: str
):
    ctx.ensure_object(dict)
    now = datetime.now()
    data = None

    if tail_hash:
        # Run export for specific CAT
        data = get_cat_balance(tail_hash)
    else:
        data = get_all_cat_balances()
    
    with open(output_file_path + f".{now.timestamp()}", 'w') as f:
        writer = csv.writer(f)
        writer.writerows(data)

def main():
    cli()


if __name__ == "__main__":
    main()
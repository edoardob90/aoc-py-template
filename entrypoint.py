#!/usr/bin/env python3
from datetime import datetime

import click

from copier import run_copy


@click.command()
@click.argument("year", type=int, default=datetime.now().year)
@click.argument("day", type=int, default=1)
@click.option(
    "--year-dir/--no-year-dir",
    show_default=True,
    default=False,
    help="Whether the output path will contain the year folder",
)
@click.option(
    "--src",
    "-s",
    type=click.Path(file_okay=False, dir_okay=True),
    default="template/",
    show_default=True,
    help="Source path",
)
@click.option(
    "--output",
    "-o",
    type=click.Path(file_okay=False, dir_okay=True),
    default="output/",
    show_default=True,
    help="Destination path",
)
def entry_point(year: int, day: int, year_dir: bool, src: str, output: str) -> None:
    run_copy(
        src_path=src,
        dst_path=output,
        data={"year": year, "day": day, "year_dir": year_dir, "puzzle_name": ""},
        unsafe=True,
    )


if __name__ == "__main__":
    entry_point()

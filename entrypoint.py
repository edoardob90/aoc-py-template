#!/usr/bin/env python3
from datetime import datetime

import click
import requests
from bs4 import BeautifulSoup
from requests.exceptions import HTTPError

from copier import run_copy


def fetch_puzzle_name(year: int, day: int) -> str:
    try:
        response = requests.get(f"https://adventofcode.com/{year}/day/{day}")
        response.raise_for_status()
    except HTTPError:
        pass
    else:
        soup = BeautifulSoup(response.text, "html.parser")
        if title := soup.find("h2"):
            return title.text.replace("---", "").split(":", 1)[1].strip()
    return ""


@click.command()
@click.argument("year", type=int, default=datetime.now().year)
@click.argument("day", type=int, default=1)
@click.argument(
    "year_dir",
    type=bool,
    default=False,
)
@click.argument(
    "src",
    type=click.Path(file_okay=False, dir_okay=True),
    default="/app/template/",
)
@click.argument(
    "output",
    type=click.Path(file_okay=False, dir_okay=True),
    default=".",
)
def entry_point(year: int, day: int, year_dir: bool, src: str, output: str) -> None:
    run_copy(
        src_path=src,
        dst_path=output,
        data={
            "year": year,
            "day": day,
            "year_dir": year_dir,
            "puzzle_name": fetch_puzzle_name(year, day),
        },
        unsafe=True,
    )


if __name__ == "__main__":
    entry_point()

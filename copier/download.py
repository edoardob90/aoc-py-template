#!/usr/bin/env python3
import pathlib as pl
import re
import sys

import click
import pypandoc
import requests
from aocd.exceptions import DeadTokenError
from bs4 import BeautifulSoup
from requests.exceptions import HTTPError

try:
    from download_input import download as download_input
except SystemExit:
    download_input = None


@click.command()
@click.argument("year", type=int)
@click.argument("day", type=int)
@click.option(
    "--year-dir/--no-year-dir",
    show_default=True,
    default=False,
    help="Whether the output path will contain the year folder",
)
def download(year: int, day: int, year_dir: bool) -> None:
    try:
        response = requests.get(f"https://adventofcode.com/{year}/day/{day}")
        response.raise_for_status()
    except HTTPError as err:
        print(
            f"Download of input for day {day}, year {year} failed: {err}",
            file=sys.stderr,
        )
        raise SystemExit() from err

    soup = BeautifulSoup(response.content, "html.parser")
    body = soup.find("article", class_="day-desc")

    markdown = pypandoc.convert_text(
        str(body), "gfm", format="html", extra_args=["--wrap=none"]
    )

    # Fix external links to other AoC days
    markdown = re.sub(
        r"\[(.*)\]\(/([^)]*)\)", r"[\1](https://adventofcode.com/\2)", markdown
    )

    output_dir = pl.Path.cwd() / (f"{day:02d}" if not year_dir else f"{year}/{day:02d}")

    output_dir.mkdir(parents=True, exist_ok=True)

    with (output_dir / "readme.md").open("w", encoding="utf-8") as f:
        f.write(markdown)

    # Download input file
    if callable(download_input):
        try:
            download_input(year, day, output_dir)
        except DeadTokenError as err:
            print(
                f"Downloading input for year {year}, day {day} failed because auth is expired: {err}",
                file=sys.stderr,
            )


if __name__ == "__main__":
    download()

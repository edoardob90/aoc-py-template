#!/usr/bin/env python3
import pathlib as pl
import sys

import click
import pypandoc
import requests
from bs4 import BeautifulSoup
from requests.exceptions import HTTPError

try:
    from download_input import download as download_input
except SystemExit:
    download_input = False


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

    output_dir = pl.Path.cwd() / (f"{day:02d}" if not year_dir else f"{year}/{day:02d}")
    output_dir.mkdir(parents=True, exist_ok=True)
    with (output_dir / "prompt.txt").open("w", encoding="utf-8") as f:
        f.write(markdown)

    # Download input file
    if callable(download_input):
        download_input(year, day, output_dir)


if __name__ == "__main__":
    download()

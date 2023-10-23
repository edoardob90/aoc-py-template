import pathlib as pl
import sys
from datetime import datetime

import click
import pypandoc
import requests
from bs4 import BeautifulSoup


@click.command()
@click.option(
    "--day", "-d", type=int, default=1, help="Day of the puzzle. Defaults to '1'"
)
@click.option(
    "--year",
    "-y",
    type=int,
    default=datetime.now().year,
    help="Year of the puzzle. Defaults to current year",
)
def main(day: int, year: int) -> None:
    try:
        response = requests.get(f"https://adventofcode.com/{year}/day/{day}")
        response.raise_for_status()
    except Exception as err:
        print(f"Download of input {day}-{year} failed: {err}", file=sys.stderr)
        raise SystemExit() from err

    soup = BeautifulSoup(response.content, "html.parser")
    body = soup.find("article", class_="day-desc")

    markdown = pypandoc.convert_text(
        str(body), "gfm", format="html", extra_args=["--wrap=none"]
    )

    with pl.Path(f"{year}/{day:02d}/input.txt").open("w", encoding="utf-8") as f:
        f.write(markdown)


if __name__ == "__main__":
    main()

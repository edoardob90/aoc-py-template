"""Download input for one Advent of Code puzzle if possible

Uses https://pypi.org/project/advent-of-code-data/ if it's available.
Otherwise, does nothing.
"""

# Standard library imports
import pathlib
import sys

# Third party imports
try:
    from aocd.models import Puzzle
except ImportError as err:
    print("Install 'advent-of-code-data' with pip to autodownload input files")
    raise SystemExit() from err


def download(year, day):
    """Get input and write it to input.txt inside the puzzle folder"""
    puzzle = Puzzle(year=year, day=day)

    # Download input
    path = pathlib.Path(__file__).parent / f"{year}/{day}"
    path.mkdir(parents=True, exist_ok=True)
    input_file = path / "input.txt"
    input_file.write_text(puzzle.input_data)

    # Download example data, if any
    example_file = path / "example_data.txt"
    example_file.write_text(puzzle.example_data)


if __name__ == "__main__":
    try:
        # Read year and day from command line
        download(year=int(sys.argv[1]), day=int(sys.argv[2]))
    except Exception as err:
        # Catch exceptions so that Copier doesn't clean up directories
        print(f"Download of input failed: {err}")
        raise SystemExit() from err

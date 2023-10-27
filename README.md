# aoc-py-template

Copier template for an Advent of Code puzzle solved in Python.

## Usage

First, you must set a GitHub repository secret named `AOC_SESSION_TOKEN` with the value of your `session` cookie. Then, the bare minimum to use this action in your workflow is the following:

```yaml
name: Advent of Code update

on: push

jobs:
  update_puzzle_input:
    runs-on: ubuntu-latest
    steps:
      - name: Get current day/year
        shell: bash
        run: |
          echo "day=$(date +%-d)" >> $GITHUB_ENV
          echo "year=$(date +%Y)" >> $GITHUB_ENV
      - name: Fetch puzzle input
        uses: edoardob90/aoc-py-template@latest
        with:
          aoc_session_token: ${{ secrets.AOC_SESSION_TOKEN }}
          day: ${{ env.day }}
          year: ${{ env.year }}
          # output: .         # default
          # year_dir: false   # default
```

By default, the output folder is the repository folder, but you can change it with the `output` input. Also, it assumes that the repository contains the puzzles of the current year. You can force the creation of a `year` subdirectory by passing the input `year_dir` to `true`.

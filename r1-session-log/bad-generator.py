import argparse
import sys
from pathlib import Path
from typing import TextIO


def generate(n: int, out: TextIO) -> None:
    for i in range(n):
        out.write(f"LOGIN u{i} {i}\n")
    for i in range(n):
        out.write(f"LOGOUT u{i} {n + i}\n")


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate a worst-case R1 session log.")
    parser.add_argument("n", type=int, help="number of distinct sessions (positive integer)")
    parser.add_argument("output_file", nargs="?", help="path to write; defaults to stdout")
    args = parser.parse_args()

    if args.n <= 0:
        parser.error("n must be a positive integer")

    if args.output_file:
        with Path(args.output_file).open("w", encoding="utf-8", newline="\n") as out:
            generate(args.n, out)
    else:
        generate(args.n, sys.stdout)


if __name__ == "__main__":
    main()
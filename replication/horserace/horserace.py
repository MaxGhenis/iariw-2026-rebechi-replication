#!/usr/bin/env python3
"""Compatibility driver for the packaged partisan-control horse race."""

from cu_replication.horserace import run_horserace, write_horserace_outputs


def main() -> None:
    """Run the packaged specifications and write their core CSV outputs."""
    paths = write_horserace_outputs(run_horserace())
    for path in paths:
        print(f"Wrote {path}")


if __name__ == "__main__":
    main()

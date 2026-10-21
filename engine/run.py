"""Entry point; run with `python3 -I engine/run.py` (isolated mode) or bin/kinetic."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from kinetic.cli import main  # noqa: E402

if __name__ == "__main__":
    sys.exit(main())

# Setup

1. Pull down latest master
2. Install [python3](https://www.python.org/downloads/) (if not already installed)
3. (Optional) Setup python3 virtual environment by running `python -m venv c:\path\to\myenv`
4. Install the chess package by running `pip install -e ./app` (you must be in root directory)
5. Run `main.py`

## Outstanding issues

- Potential bug with \_\_get_move_selection() in Game where a recursion error can occur if the user makes an invalid selection (clicks something other than their piece) ~1000 times (max recursion depth depending). In practice this isn't an issue and probably isn't worth fixing.

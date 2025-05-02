# mazejmp
A pygame based visualization of a jumping maze solved using uninformed
search methods.

## Installation
First create a virtual environment by running:
```bash
python3 -m venv .venv
```

Activate it by:
```bash
source .venv/bin/activate
```

Then, install the required package (`pygame`) directly from the
[requirements.txt](./requirements.txt) file by running
```bash
pip install -r requirements.txt
```

## Execution
To execute with a set of example mazes run
```bash
python main.py example_input.txt
```

## Input file format
An input file is a set of mazes specified, first by a header line that
contains height (`m`), width (`n`), coordinates of starting cell ((`sx`,
`sy`)) and coordinates of target cell ((`tx`, `ty`)); like so:
```
m n sx sy tx ty
```

Then `m` lines follow, each with `n` space separated non-negative integers
indicating the jump size from each cell.

Many mazes can be described in one file. There must be no blank lines as
the current parser does not ignore these. Finally, end of input can be
described by a line containing a single `0`.

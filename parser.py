# Author: LELE
# Parses input file of mazes

def parse_input(input_dir):
    """Parses input file located in input_dir.

    Returns a list of tuples (header, grid, cell_type) where header is a list
    containing [m, n, sx, sy, tx, ty], grid is a matrix with
    the contents of the maze and cell_type is a matrix indicating
    the type of each cell on the grid ('at-goal', 'start', 'target', None).

    Raises a ValueError if input file does not have an appropriate format.
    Format is:
      1. A header line: 'm, n, sx, sy, tx, ty' or a single '0',
      2. 'm' lines each with 'n' non-negative integers,
      3. There are no empty lines.

    Allows for file to not end in a single '0' line if EOF comes first.

    It ignores all input that comes after a header line containing '0'.
    """

    input_data = []

    with open(input_dir) as input_file:
        while True:
            # Begin processing maze header
            try:
                line = next(input_file)
            except StopIteration:
                break

            # Parse maze header
            header = list(map(int, line.split()))

            # Check that header has correct length (1 or 6)
            if len(header) != 1 and len(header) != 6:
                raise ValueError(f"invalid header length: {len(header)}")

            # If header has only one element, it must be a 0, this means EOF
            if len(header) == 1:
                if header[0] != 0:
                    raise ValueError(f"invalid header content: has length 1 but a value of {header[0]}")
                else:
                    break

            # All elements must be non-negative
            if min(header) < 0:
                raise ValueError("invalid header content: contains negative values")

            m, n, sx, sy, tx, ty = header

            # Number of columns and rows must be positive
            if m == 0 or n == 0:
                raise ValueError(f"invalid header content: maze dimensions are empty ({m}, {n})")

            # Start and end coordinates must be within rectangle bounds
            if sx >= m:
                raise ValueError(f"invalid header content: sx is out of bounds {sx} >= {m}")
            if sy >= n:
                raise ValueError(f"invalid header content: sy is out of bounds {sy} >= {n}")
            if tx >= m:
                raise ValueError(f"invalid header content: tx is out of bounds {tx} >= {m}")
            if ty >= n:
                raise ValueError(f"invalid header content: ty is out of bounds {ty} >= {n}")

            # Begin processing maze
            grid = []

            for _ in range(m):
                try:
                    line = next(input_file)
                except StopIteration:
                    raise ValueError("invalid maze content: reached EOF before reading whole maze")

                # Parse maze row
                row = list(map(int, line.split()))

                # If row does not have n elements, it is incomplete
                if len(row) != n:
                    raise ValueError(f"invalid maze content: row should have length {n} but it has length {len(row)}")

                # All jump sizes must be non-negative since negative jumps
                # make no sense (even if they jump to the other direction,
                # that would be the same as just jumping a positive amount)
                if min(row) < 0:
                    raise ValueError("invalid maze content: contains negative values")

                # Add row to maze
                grid.append(row)

            # Begin processing cell_type
            cell_type = [[None for _ in range(n)] for _ in range(m)]

            cell_type[sx][sy] = "start"
            cell_type[tx][ty] = "at-goal" if cell_type[tx][ty] == "start" else "target"

            # Add read maze to input_data
            input_data.append((header, grid, cell_type))

    return input_data

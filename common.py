from typing import NewType, Union, Optional

from pieces.pieces import Piece

Coords = NewType("Coords", Union[str, tuple[int, int]])


def translate(key: Coords) -> tuple[int, int]:
    mapping = {
        'a': 0,
        'b': 1,
        'c': 2,
        'd': 3,
        'e': 4,
        'f': 5,
        'g': 6,
        'h': 7
    }

    if isinstance(key, tuple):
        return key[0], key[1]
    if isinstance(key, str):
        return int(key[1]) - 1, mapping[key[0]]


class BoardField:
    def __init__(self):
        self.board: list[list[Optional[Piece]]] = [
            [None for _ in range(8)] for _ in range(8)
        ]

    def __getitem__(self, item: Coords) -> Optional[Piece]:
        row, col = translate(item)
        return self.board[row][col]

    def __setitem__(self, key: Coords, value) -> None:
        row, col = translate(key)
        self.board[row][col] = value

    def clear(self):
        self.board: list[list[Optional[Piece]]] = [
            [None for _ in range(8)] for _ in range(8)
        ]

    def is_between(self, start: Coords, end: Coords):
        row_start, col_start = translate(start)
        row_end, col_end = translate(end)

        if row_start == row_end:
            min_col, max_col = min(col_start, col_end), max(col_start, col_end)
            for i in range(min_col + 1, max_col):
                if self.board[row_start][i]:
                    return True
            return False
        if col_start == col_end and row_start > row_end:
            min_row, max_row = min(row_start, row_end), max(row_start, row_end)
            for i in range(min_row + 1, max_row):
                if self.board[row_start][i]:
                    return True
            return False
        if abs(row_start - row_end) == abs(col_start - col_end):
            min_row = min(row_start, row_end)
            if row_end == min_row:
                row_start, row_end = row_end, row_start
                col_start, col_end = col_end, col_start

            for i in range(1, abs(row_start - row_end)):
                if (col_start < col_end
                        and self.board[row_start + i][col_start + i]):
                    return True
                elif (col_start > col_end
                      and self.board[row_start + i][col_start - i]):
                    return True

    def move(self, start: Coords, end: Coords):
        row_start, col_start = translate(start)
        row_end, col_end = translate(end)

        self.board[row_end][col_end] = self.board[row_start][col_start]
        self.board[row_start][col_start] = None

    def promote(self, position: Coords, new_piece: Piece):
        row, col = translate(position)
        self.board[row][col] = new_piece

    def en_passant(self, start: Coords, end: Coords):
        row_start, _ = translate(start)
        _, col_end = translate(end)

        self.move(start, end)
        self.board[row_start][col_end] = None

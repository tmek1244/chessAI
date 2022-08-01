from typing import NewType, Optional, Union
from enum import Enum

import logging
log = logging.getLogger(__name__)

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
        self.board: list[list[Optional['Piece']]] = [
            [None for _ in range(8)] for _ in range(8)
        ]
        self.pieces: set['Piece'] = set()
        self.move_counter = 0

    def __getitem__(self, item: Coords) -> Optional['Piece']:
        row, col = translate(item)
        return self.board[row][col]

    def __setitem__(self, key: Coords, value: 'Piece') -> None:
        row, col = translate(key)
        self.pieces.add(value)
        self.board[row][col] = value

    def clear(self):
        self.board: list[list[Optional['Piece']]] = [
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
        if col_start == col_end:
            min_row, max_row = min(row_start, row_end), max(row_start, row_end)
            for i in range(min_row + 1, max_row):
                if self.board[i][col_start]:
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

    def move(self, start: Coords, end: Coords, move_counter: int):
        row_start, col_start = translate(start)
        row_end, col_end = translate(end)

        log.info(f"Moving from {row_start}:{col_start} to {row_end}:{col_end}")

        if self.board[row_end][col_end]:
            self.pieces.remove(self.board[row_end][col_end])
        
        self.board[row_end][col_end] = self.board[row_start][col_start]
        self.board[row_start][col_start] = None
        self.board[row_end][col_end].position = (row_end, col_end)
        self.board[row_end][col_end].when_moved.append(move_counter)
        self.move_counter = move_counter

    def promote(self, position: Coords, new_piece: 'Piece'):
        row, col = translate(position)
        self.board[row][col] = new_piece

    def en_passant(self, start: Coords, end: Coords, move_counter: int):
        row_start, _ = translate(start)
        _, col_end = translate(end)

        self.move(start, end, move_counter)
        self.pieces.remove(self.board[row_start][col_end])
        self.board[row_start][col_end] = None


class PieceType(Enum):
    PAWN = 1
    KNIGHT = 2
    BISHOP = 3
    ROOK = 4
    QUEEN = 5
    KING = 6


class PieceColor(Enum):
    WHITE = 1
    BLACK = 2


class Piece:
    def __init__(
            self,
            piece_type: PieceType,
            piece_color: PieceColor,
            position: str | tuple[int, int]
    ):
        self.type = piece_type
        self.color = piece_color
        self.position = position
        self.when_moved = []

    def __str__(self):
        return f"{self.type}:{self.color} [{self.position}]"
        # match self.type:
        #     case PieceType.PAWN:
        #         return "P"
        #     case PieceType.ROOK:
        #         return "R"
        #     case PieceType.KNIGHT:
        #         return "N"
        #     case PieceType.BISHOP:
        #         return "B"
        #     case PieceType.QUEEN:
        #         return "Q"
        #     case PieceType.KING:
        #         return "K"

    def __repr__(self):
        return self.__str__()

    def can_move(
            self,
            end: str | tuple[int, int],
            board: BoardField
    ) -> tuple[bool, str]:
        if board[end] and board[end].color == self.color:
            return False, "Cannot take own piece"

        output = self._can_move(end, board)
        return (output, "") if type(output) == bool else output

    def _can_move(
            self,
            end: Coords,
            board: BoardField
    ) -> bool | tuple[bool, str]:
        ...
    
    def get_all_moves(self, board: BoardField) -> list[tuple[int, int]]:
        result = []
        for i in range(8):
            for j in range(8):
                can_move, _ = self.can_move((i, j), board)
                if can_move:
                    result.append((i, j))
        return result

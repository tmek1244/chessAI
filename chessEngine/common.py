from typing import NewType, Optional, Union
from enum import Enum, IntEnum

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


class PieceType(Enum):
    PAWN = 1
    KNIGHT = 2
    BISHOP = 3
    ROOK = 4
    QUEEN = 5
    KING = 6


class PieceColor(IntEnum):
    WHITE = 0
    BLACK = 1


class BoardField:
    def __init__(self):
        self.board: list[list[Optional['Piece']]] = [
            [None for _ in range(8)] for _ in range(8)
        ]
        self.pieces: set['Piece'] = set()
        self.move_counter = 0
        self.kings: list[Optional('Piece')] = [None, None]
        self.under_check: list[Optional('Piece')] = [None, None]

    def __getitem__(self, item: Coords) -> Optional['Piece']:
        row, col = translate(item)
        if row < 0 or row > 7 or col < 0 or col > 7:
            return None
        return self.board[row][col]

    def __setitem__(self, key: Coords, piece: 'Piece') -> None:
        row, col = translate(key)
        if piece.type == PieceType.KING:
            self.kings[piece.color] = piece
        self.pieces.add(piece)
        self.board[row][col] = piece

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
        self.move_counter = move_counter #TODO
        if self.board[row_end][col_end].enemy_king_under_check():
            self.under_check[(self.board[row_end][col_end].color + 2)%2] = self.board[row_end][col_end].color

    def promote(self, position: Coords, new_piece: 'Piece'):
        row, col = translate(position)
        self.board[row][col] = new_piece

    def en_passant(self, start: Coords, end: Coords, move_counter: int):
        row_start, _ = translate(start)
        _, col_end = translate(end)

        self.move(start, end, move_counter)
        self.pieces.remove(self.board[row_start][col_end])
        self.board[row_start][col_end] = None


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
    
    def get_all_moves(
        self, board: BoardField, whose_move: Optional[PieceColor] = None) -> list[tuple[int, int]]:
        result = []
        if whose_move and whose_move != self.color:
            return []
        for i in range(8):
            for j in range(8):
                can_move, _ = self.can_move((i, j), board)
                if can_move:
                    result.append((i, j))
        return result
    
    # def king_not_under_check(self, next_position, board: BoardField):
    #     resutl = self._king_not_under_check(next_position, board)
    #     if resutl == False:
    #         print(self.position, next_position, self.type)
    #     return resutl

    def king_not_under_check(self, next_position, board: BoardField):
        row, col = translate(self.position)
        next_row, next_col = translate(next_position)
        king_row, king_col = translate(board.kings[self.color].position)

        if (enemy_piece := board.under_check[self.color]):
            enemy_row, enemy_col = translate(enemy_piece.position)
            
            if enemy_piece.type in [PieceType.BISHOP, PieceType.QUEEN]:
                if abs(next_row - king_row) == abs(next_col - king_col):
                    if (
                        not (
                            (enemy_row >= next_row > king_row or enemy_row <= next_row < king_row) and 
                            (enemy_col >= next_col > king_col or enemy_col <= next_col < king_col))
                        ):
                        return False
                else:
                    return False
            
            if enemy_piece.type in [PieceType.QUEEN, PieceType.ROOK]:
                if enemy_row == king_row:
                    if next_row != enemy_row:
                        return False
                    if not (enemy_col >= next_col > king_col or enemy_col <= next_col < king_col):
                        return False
                elif enemy_col == king_col:
                    if next_col != enemy_col:
                        return False
                    if not (enemy_row >= next_row > king_row or enemy_row <= next_row < king_row):
                        return False
                else:
                    return False
            
            if enemy_piece.type in [PieceType.PAWN, PieceType.KNIGHT]:
                if (enemy_row, enemy_col) != (next_row, next_col):
                    return False


        if row != king_row and col != king_col and abs(row - king_row) != abs(col - king_col):
            return True

        if row == king_row and next_row != row and not board.is_between(self.position, board.kings[self.color].position):
            if col > king_col:
                for i in range(col+1, 8):
                    if board[(row, i)]:
                        return (
                            board[(row, i)].type not in [PieceType.QUEEN, PieceType.ROOK] 
                            or board[(row, i)].color == self.color)
            else:
                for i in range(col-1, 0, -1):
                    if board[(row, i)]:
                        return (
                            board[(row, i)].type not in [PieceType.QUEEN, PieceType.ROOK] 
                            or board[(row, i)].color == self.color)
        if col == king_row and next_col != col and not board.is_between(self.position, board.kings[self.color].position):
            if row > king_row:
                for i in range(row+1, 8):
                    if board[(i, col)]:
                        return (
                            board[(i, col)].type not in [PieceType.QUEEN, PieceType.ROOK] 
                            or board[(i, col)].color == self.color)
            else:
                for i in range(row-1, 0, -1):
                    if board[(i, col)]:
                        return (
                            board[(i, col)].type not in [PieceType.QUEEN, PieceType.ROOK] 
                            or board[(i, col)].color == self.color)
        
        if abs(row - king_row) == abs(col - king_col) and not board.is_between(self.position, board.kings[self.color].position):
            if abs(row - next_row) == abs(col - next_col) and abs(next_row - king_row) == abs(next_col - king_col):
                return True
            row_inc = 1 if row > king_row else -1
            col_inc = 1 if col > king_col else -1

            row_it, col_it = row + row_inc, col + col_inc
            while row_it > -1 and row_it < 8 and col_it > -1 and col_it < 8:
                if board[(row_it, col_it)]:
                    return (
                        board[(row_it, col_it)].type not in [PieceType.QUEEN, PieceType.BISHOP] 
                        or board[(row_it, col_it)].color == self.color)

                row_it += row_inc
                col_it += col_inc
        return True

    def enemy_king_under_check(self, board: BoardField, position = None):
        ...

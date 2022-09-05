import logging
from enum import Enum, IntEnum
from typing import NewType, Optional, Union, cast
import numpy as np

log = logging.getLogger(__name__)


class Coords:
    row: int
    col: int

    def __init__(self, coords: str | tuple[int, int]) -> None:
        self._set(coords)

    def _set(self, key: str | tuple[int, int]) -> None:
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
            self.row = key[0]
            self.col = key[1]
        if isinstance(key, str):
            self.row = int(key[1]) - 1
            self.col = mapping[key[0]]
    
    def is_correct(self) -> bool:
        return 0 <= self.row < 8 and 0 <= self.col < 8
    
    def diagonal(self, other: 'Coords') -> bool:
        return abs(self.row - other.row) == abs(self.col - other.col)
    
    def in_line(self, other: 'Coords') -> bool:
        return self.row == other.row or self.col == other.col
    
    def same_row(self, other: 'Coords') -> bool:
        return self.row == other.row
    
    def same_col(self, other: 'Coords') -> bool:
        return self.col == other.col
        


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

    def __getitem__(self, item: Coords | tuple[int, int] | str) -> Optional['Piece']:        
        if not isinstance(item, Coords):
            item = Coords(item)
        return self.board[item.row][item.col] if item.is_correct() else None

    def __setitem__(self, key: Coords, piece: 'Piece') -> None:
        if not isinstance(key, Coords):
            key = Coords(key)
        
        if not key.is_correct():
            return
        if piece.type == PieceType.KING:
            self.kings[piece.color] = piece
        self.pieces.add(piece)
        self.board[key.row][key.col] = piece

    def clear(self):
        self.board: list[list[Optional['Piece']]] = [
            [None for _ in range(8)] for _ in range(8)
        ]

    def is_between(self, start: Coords, end: Coords):
        if start.same_row(end):
            min_col, max_col = min(start.col, end.col), max(start.col, end.col)
            for i in range(min_col + 1, max_col):
                if self.board[start.row][i]:
                    return True
            return False
        if start.same_col(end):
            min_row, max_row = min(start.row, end.row), max(start.row, end.row)
            for i in range(min_row + 1, max_row):
                if self.board[i][start.col]:
                    return True
            return False
        if start.diagonal(end):
            min_row = min(start.row, end.row)
            if end.row == min_row:
                start, end = Coords((end.row, end.col)), Coords((start.row, start.col))

            for i in range(1, abs(start.row - end.row)):
                if (start.col < end.col
                        and self.board[start.row + i][start.col + i]):
                    return True
                elif (start.col > end.col
                      and self.board[start.row + i][start.col - i]):
                    return True

    def move(self, start: Coords, end: Coords, move_counter: int):
        log.info(f"Moving from {start.row}:{start.col} to {end.row}:{end.col}")
        piece = self.board[start.row][start.col]
        assert piece
        if enemy:=self.board[end.row][end.col]:
            self.pieces.remove(enemy)
            if self.under_check[piece.color] == enemy:
                self.under_check[piece.color] = None
        
        self.board[end.row][end.col] = piece
        self.board[start.row][start.col] = None
        piece.position = Coords((end.row, end.col))
        piece.when_moved.append(move_counter)
        self.move_counter = move_counter #TODO
        if piece.enemy_king_under_check(self):
            self.under_check[(piece.color + 1)%2] = piece

    def promote(self, position: Coords, new_piece: 'Piece'):
        self.board[position.row][position.col] = new_piece

    def en_passant(self, start: Coords, end: Coords, move_counter: int):
        self.move(start, end, move_counter)
        enemy_pawn = self.board[start.row][end.col]
        assert enemy_pawn
        self.pieces.remove(enemy_pawn)
        self.board[start.row][end.col] = None

    def to_array(self) -> np.array:
        result = np.zeros((2, 6, 8, 8))
        for row in range(0, 8):
            for col in range(0, 8):
                piece = self.board[row][col]
                if not piece:
                    continue
                
                color = 1 if piece.color == PieceColor.BLACK else 0
                piece_id = None
                if piece.type == PieceType.KING:
                    piece_id = 0
                elif piece.type == PieceType.QUEEN:
                    piece_id = 1
                elif piece.type == PieceType.ROOK:
                    piece_id = 2
                elif piece.type == PieceType.BISHOP:
                    piece_id = 3
                elif piece.type == PieceType.KNIGHT:
                    piece_id = 4
                elif piece.type == PieceType.PAWN:
                    piece_id = 5
                result[color, piece_id, row, col] = 1
        return result
    
    # def get_castling_rights()


class Piece:
    def __init__(
            self,
            piece_type: PieceType,
            piece_color: PieceColor,
            position: Coords
    ) -> None:
        self.type = piece_type
        self.color = piece_color
        self.position = position
        self.when_moved: list[int] = []

    def __str__(self):
        return f"{self.type}:{self.color} [{self.position}]"

    def __repr__(self):
        return self.__str__()

    def can_move(
            self,
            end: Coords,
            board: BoardField
    ) -> tuple[bool, str]:
        if not isinstance(end, Coords):
            end = Coords(end)
        if not end.is_correct():
            return False, f"No field {end}"
        if (enemy:=board[end]) and enemy.color == self.color:
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
        ...

    def king_not_under_check(self, next_position: Coords, board: BoardField) -> bool:
        king = cast(Coords, board.kings[self.color].position)
        
        if (enemy := board.under_check[self.color]):
            enemy = cast(Piece, enemy)
            if enemy.position.diagonal(king):
                if next_position.diagonal(king):
                    if (
                        not (
                            (enemy.position.row >= next_position.row > king.row or 
                            enemy.position.row <= next_position.row < king.row) and 
                            (enemy.position.col >= next_position.col > king.col or 
                            enemy.position.col <= next_position.col < king.col))
                        ):
                        return False
                else:
                    return False
            
            # if enemy.type in [PieceType.QUEEN, PieceType.ROOK]:
            if enemy.position.col == king.col or enemy.position.row == king.row:
                if enemy.position.row == king.row:
                    if next_position.row != enemy.position.row:
                        return False
                    if not (enemy.position.col >= next_position.col > king.col or enemy.position.col <= next_position.col < king.col):
                        return False
                elif enemy.position.col == king.col:
                    if next_position.col != enemy.position.col:
                        return False
                    if not (enemy.position.row >= next_position.row > king.row or enemy.position.row <= next_position.row < king.row):
                        return False
                else:
                    return False
            
            if enemy.type in [PieceType.PAWN, PieceType.KNIGHT]:
                if (enemy.position.row, enemy.position.col) != (next_position.row, next_position.col):
                    return False


        if not self.position.same_row(king) and not self.position.same_col(king) and not self.position.diagonal(king):
            return True

        if self.position.same_row(king) and not next_position.same_row(self.position) and not board.is_between(self.position, board.kings[self.color].position):
            if self.position.same_col(king):
                for i in range(self.position.col+1, 8):
                    if piece:=board[(self.position.row, i)]:
                        return (
                            piece.type not in [PieceType.QUEEN, PieceType.ROOK] 
                            or piece.color == self.color)
            else:
                for i in range(self.position.col-1, 0, -1):
                    if piece:=board[(self.position.row, i)]:
                        return (
                            piece.type not in [PieceType.QUEEN, PieceType.ROOK] 
                            or piece.color == self.color)
        if self.position.same_col(king) and next_position.same_col(self.position) and not board.is_between(self.position, board.kings[self.color].position):
            if self.position.row > king.row:
                for i in range(self.position.row+1, 8):
                    if piece:=board[(i, self.position.col)]:
                        return (
                            piece.type not in [PieceType.QUEEN, PieceType.ROOK] 
                            or piece.color == self.color)
            else:
                for i in range(self.position.row-1, 0, -1):
                    if piece:=board[(i, self.position.col)]:
                        return (
                            piece.type not in [PieceType.QUEEN, PieceType.ROOK] 
                            or piece.color == self.color)
        
        if self.position.diagonal(king) and not board.is_between(self.position, board.kings[self.color].position):
            if self.position.diagonal(next_position) and next_position.diagonal(king):
                return True
            row_inc = 1 if self.position.row > king.row else -1
            col_inc = 1 if self.position.col > king.col else -1

            row_it, col_it = self.position.row + row_inc, self.position.col + col_inc
            while row_it > -1 and row_it < 8 and col_it > -1 and col_it < 8:
                if piece:=board[(row_it, col_it)]:
                    return (
                        piece.type not in [PieceType.QUEEN, PieceType.BISHOP] 
                        or piece.color == self.color)

                row_it += row_inc
                col_it += col_inc
        return True

    def enemy_king_under_check(self, board: BoardField, position = None):
        ...

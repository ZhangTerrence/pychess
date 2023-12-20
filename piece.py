from __future__ import annotations
from abc import abstractmethod, ABC
import typing

if typing.TYPE_CHECKING:
    from board import Board


class Piece():
    def __init__(self, color: str):
        self.color = color

    @abstractmethod
    def __repr__(self) -> str:
        pass

    @abstractmethod
    def moves(self, board: Board, row: int, column: int) -> list[tuple[int, int]]:
        pass

class King(Piece, ABC):
    def __init__(self, color):
        super().__init__(color)

    def __repr__(self):
        return "W_King" if self.color == "W" else "B_King"


class Queen(Piece, ABC):
    def __init__(self, color):
        super().__init__(color)

    def __repr__(self):
        return "W_Queen" if self.color == "W" else "B_Queen"

    def moves(self, board: Board, row: int, column: int) -> list[tuple[int, int]]:
        moves = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]

        for dir_row, dir_column in directions:
            current_row, current_column = row + dir_row, column + dir_column
            while board.valid_tile(current_row, current_column):
                current_piece = board.get_piece(current_row, current_column)
                if current_piece == None:
                    moves.append((current_row, current_column))
                elif current_piece.color != self.color:
                    moves.append((current_row, current_column))
                    break
                else:
                    break
                current_row += dir_row
                current_column += dir_column

        return moves


class Rook(Piece, ABC):
    def __init__(self, color):
        super().__init__(color)

    def __repr__(self):
        return "W_Rook" if self.color == "W" else "B_Rook"

    def moves(self, board: Board, row: int, column: int) -> list[tuple[int, int]]:
        moves = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        for dir_row, dir_column in directions:
            current_row, current_column = row + dir_row, column + dir_column
            while board.valid_tile(current_row, current_column):
                position = board.get_piece(current_row, current_column)
                if position == None:
                    moves.append((current_row, current_column))
                elif position.color != self.color:
                    moves.append((current_row, current_column))
                    break
                else:
                    break
                current_row += dir_row
                current_column += dir_column

        return moves


class Bishop(Piece, ABC):
    def __init__(self, color):
        super().__init__(color)

    def __repr__(self):
        return "W_Bishop" if self.color == "W" else "B_Bishop"

    def moves(self, board: Board, row: int, column: int) -> list[tuple[int, int]]:
        moves = []
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

        for dir_row, dir_column in directions:
            current_row, current_column = row + dir_row, column + dir_column
            while board.valid_tile(current_row, current_column):
                position = board.get_piece(current_row, current_column)
                if position == None:
                    moves.append((current_row, current_column))
                elif position.color != self.color:
                    moves.append((current_row, current_column))
                    break
                else:
                    break
                current_row += dir_row
                current_column += dir_column

        return moves

class Knight(Piece, ABC):
    def __init__(self, color):
        super().__init__(color)

    def __repr__(self):
        return "W_Knight" if self.color == "W" else "B_Knight"

    def moves(self, board: Board, row: int, column: int) -> list[tuple[int, int]]:
        moves = []
        directions = [(-1, -2), (1, -2), (-1, 2), (1, 2), (-2, -1), (2, -1), (-2, 1), (2, 1)]

        for dir_row, dir_column in directions:
            if board.valid_tile(row + dir_row, column + dir_column):
                position = board.get_piece(row + dir_row, column + dir_column)
                if position == None:
                    moves.append((row + dir_row, column + dir_column))
                elif self.color != position.color:
                    moves.append((row + dir_row, column + dir_column))

        return moves


class Pawn(Piece, ABC):
    def __init__(self, color):
        super().__init__(color)

    def __repr__(self):
        return "W_Pawn" if self.color == "W" else "B_Pawn"


    def moves(self, board: Board, row: int, column: int) -> list[tuple[int, int]]:
        moves = []
        forward = -1 if self.color == "W" else 1

        if board.get_piece(row + forward, column) == None:
            moves.append((row + forward, column))
            if (row == 1 and self.color == "B") or (row == 6 and self.color == "W"):
                if not board.get_piece(row + 2 * forward, column):
                    moves.append((row + 2 * forward, column))
        if column > 0 and board.get_piece(row + forward, column - 1) and board.get_piece(row + forward, column - 1).color != self.color:
            moves.append((row + forward, column - 1))
        if column < 7 and board.get_piece(row + forward, column + 1) and board.get_piece(row + forward, column + 1).color != self.color:
            moves.append((row + forward, column + 1))

        return moves
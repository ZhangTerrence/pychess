from __future__ import annotations
from abc import abstractmethod, ABC
import typing

if typing.TYPE_CHECKING:
    from board import Board


class Piece:
    def __init__(self, color: str):
        self.color = color

    @abstractmethod
    def __repr__(self) -> str:
        pass

    @abstractmethod
    def moves(self, board: Board, row: int, column: int, check_check: bool) -> list[tuple[int, int]]:
        pass

    def filter_moves(self, board: Board, moves: list[tuple[int, int]], old_row: int, old_column: int) -> list[tuple[int, int]]:
        filtered_moves = []

        for new_row, new_column in moves:
            temp_piece = board.get_piece(new_row, new_column)
            board.move_piece(old_row, old_column, new_row, new_column)

            if not board.is_checked():
                filtered_moves.append((new_row, new_column))

            board.set_piece(self, old_row, old_column)
            board.set_piece(temp_piece, new_row, new_column)

        return filtered_moves


class King(Piece, ABC):
    def __init__(self, color):
        super().__init__(color)
        self.has_moved = False
        
    def __repr__(self):
        return "W_King" if self.color == "W" else "B_King"

    def moved(self):
        self.has_moved = True

    def moves(self, board: Board, row: int, column: int, check_check: bool) -> list[tuple[int, int]]:
        moves = []
        directions = [(-1, -1), (0, -1), (-1, 1), (-1, 0), (0, 1), (1, -1), (1, 0), (1, 1)]

        for dir_row, dir_column in directions:
            new_row, new_column = row + dir_row, column + dir_column
            if board.is_valid_tile(new_row, new_column):
                current_piece = board.get_piece(new_row, new_column)
                if current_piece is None or current_piece.color != self.color:
                    temp_piece = board.get_piece(new_row, new_column)
                    board.move_piece(row, column, new_row, new_column)

                    if not board.is_checked():
                        moves.append((new_row, new_column))

                    board.set_piece(self, row, column)
                    board.set_piece(temp_piece, new_row, new_column)

        if not board.is_checked() and not self.has_moved:
            if board.can_castle("king"):
                moves.append((row, 6))
            if board.can_castle("queen"):
                moves.append((row, 2))
        
        return self.filter_moves(board, moves, row, column)


class Queen(Piece, ABC):
    def __init__(self, color):
        super().__init__(color)

    def __repr__(self):
        return "W_Queen" if self.color == "W" else "B_Queen"

    def moves(self, board: Board, row: int, column: int, check_check: bool) -> list[tuple[int, int]]:
        moves = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]

        for dir_row, dir_column in directions:
            current_row, current_column = row + dir_row, column + dir_column
            while board.is_valid_tile(current_row, current_column):
                current_piece = board.get_piece(current_row, current_column)
                if current_piece is None:
                    moves.append((current_row, current_column))
                elif current_piece.color != self.color:
                    moves.append((current_row, current_column))
                    break
                else:
                    break
                current_row += dir_row
                current_column += dir_column

        if check_check:
            return self.filter_moves(board, moves, row, column)
        return moves


class Rook(Piece, ABC):
    def __init__(self, color):
        super().__init__(color)
        self.has_moved = False

    def __repr__(self):
        return "W_Rook" if self.color == "W" else "B_Rook"

    def moved(self):
        self.has_moved = True        

    def moves(self, board: Board, row: int, column: int, check_check: bool) -> list[tuple[int, int]]:
        moves = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        for dir_row, dir_column in directions:
            current_row, current_column = row + dir_row, column + dir_column
            while board.is_valid_tile(current_row, current_column):
                current_piece = board.get_piece(current_row, current_column)
                if current_piece is None:
                    moves.append((current_row, current_column))
                elif current_piece.color != self.color:
                    moves.append((current_row, current_column))
                    break
                else:
                    break
                current_row += dir_row
                current_column += dir_column

        if check_check:
            return self.filter_moves(board, moves, row, column)
        return moves


class Bishop(Piece, ABC):
    def __init__(self, color):
        super().__init__(color)

    def __repr__(self):
        return "W_Bishop" if self.color == "W" else "B_Bishop"

    def moves(self, board: Board, row: int, column: int, check_check: bool) -> list[tuple[int, int]]:
        moves = []
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

        for dir_row, dir_column in directions:
            current_row, current_column = row + dir_row, column + dir_column
            while board.is_valid_tile(current_row, current_column):
                current_piece = board.get_piece(current_row, current_column)
                if current_piece is None:
                    moves.append((current_row, current_column))
                elif current_piece.color != self.color:
                    moves.append((current_row, current_column))
                    break
                else:
                    break
                current_row += dir_row
                current_column += dir_column

        if check_check:
            return self.filter_moves(board, moves, row, column)
        return moves


class Knight(Piece, ABC):
    def __init__(self, color):
        super().__init__(color)

    def __repr__(self):
        return "W_Knight" if self.color == "W" else "B_Knight"

    def moves(self, board: Board, row: int, column: int, check_check: bool) -> list[tuple[int, int]]:
        moves = []
        directions = [(-1, -2), (1, -2), (-1, 2), (1, 2), (-2, -1), (2, -1), (-2, 1), (2, 1)]

        for dir_row, dir_column in directions:
            if board.is_valid_tile(row + dir_row, column + dir_column):
                current_piece = board.get_piece(row + dir_row, column + dir_column)
                if current_piece is None:
                    moves.append((row + dir_row, column + dir_column))
                elif self.color != current_piece.color:
                    moves.append((row + dir_row, column + dir_column))

        if check_check:
            return self.filter_moves(board, moves, row, column)
        return moves


class Pawn(Piece, ABC):
    def __init__(self, color):
        super().__init__(color)
        self.double_moved = False

    def __repr__(self):
        return "W_Pawn" if self.color == "W" else "B_Pawn"
    
    def update(self, foo: bool):
        self.double_moved = foo

    def moves(self, board: Board, row: int, column: int, check_check: bool) -> list[tuple[int, int]]:
        moves = []
        forward = -1 if self.color == "W" else 1

        if board.get_piece(row + forward, column) is None:
            moves.append((row + forward, column))
            if (row == 1 and self.color == "B") or (row == 6 and self.color == "W"):
                if not board.get_piece(row + 2 * forward, column):
                    moves.append((row + 2 * forward, column))
   
        if column > 0:
            left_piece = board.get_piece(row + forward, column - 1) 
            if left_piece and left_piece.color != self.color:
                moves.append((row + forward, column - 1))
            if board.can_en_passant(row, column, "left"):
                moves.append((row + forward, column - 1))
        
        if column < 7:
            right_piece = board.get_piece(row + forward, column + 1) 
            if right_piece and right_piece.color != self.color:
                moves.append((row + forward, column + 1))
            if board.can_en_passant(row, column, "right"):
                moves.append((row + forward, column + 1))
                
        if check_check:
            return self.filter_moves(board, moves, row, column)
        return moves

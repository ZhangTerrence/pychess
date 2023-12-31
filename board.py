from pickletools import int4
from piece import Piece, King, Queen, Rook, Bishop, Knight, Pawn
import pygame


class Board:
    LIGHT = (255, 255, 255)
    DARK = (68, 68, 68)

    def __init__(self, tile_size: int, screen: pygame.SurfaceType, pieces: dict[str, pygame.SurfaceType], current_player: str):
        self.tile_size = tile_size
        self.screen = screen
        self.pieces = pieces
        self.current_player = current_player
        self.board: list[list[Piece | None]] = [[None for _ in range(8)] for _ in range(8)]

        self.init_board()

    def __repr__(self) -> list[list[Piece | None]]:
        return self.board

    def create_background(self) -> pygame.Surface:
        background = pygame.Surface((self.tile_size * 8, self.tile_size * 8))

        light = True
        for x in range(8):
            for y in range(8):
                tile = pygame.Rect(self.tile_size * x, self.tile_size * y, self.tile_size, self.tile_size)
                pygame.draw.rect(background, pygame.Color(self.LIGHT if light else self.DARK), tile)
                light = not light
            light = not light

        return background

    def draw_pieces(self) -> None:
        for x in range(8):
            for y in range(8):
                current_piece = self.get_piece(y, x)
                if current_piece is not None:
                    self.screen.blit(self.pieces[current_piece.__repr__()], (self.tile_size * x + 17.5, self.tile_size * y + 12.5))

    def init_board(self) -> None:
        self.board[7][0] = Rook("W")
        self.board[7][1] = Knight("W")
        self.board[7][2] = Bishop("W")
        self.board[7][3] = Queen("W")
        self.board[7][4] = King("W")
        self.board[7][5] = Bishop("W")
        self.board[7][6] = Knight("W")
        self.board[7][7] = Rook("W")
        for i in range(8):
            self.board[6][i] = Pawn("W")

        self.board[0][0] = Rook("B")
        self.board[0][1] = Knight("B")
        self.board[0][2] = Bishop("B")
        self.board[0][3] = Queen("B")
        self.board[0][4] = King("B")
        self.board[0][5] = Bishop("B")
        self.board[0][6] = Knight("B")
        self.board[0][7] = Rook("B")
        for i in range(8):
            self.board[1][i] = Pawn("B")

    def get_piece(self, row: int, column: int) -> Piece | None:
        return self.board[row][column]

    def set_piece(self, piece: Piece | None, row: int, column: int) -> None:
        self.board[row][column] = piece

    def move_piece(self, old_row: int | None, old_column: int | None, new_row: int | None, new_column: int | None) -> None:
        if old_row is not None and old_column is not None:
            if new_row is not None and new_column is not None:
                piece = self.get_piece(old_row, old_column)
                self.set_piece(None, old_row, old_column)
                self.set_piece(piece, new_row, new_column)

    def show_moves(self, moves: list[tuple[int, int]]) -> None:
        if moves != []:
            for move in moves:
                tile = (self.tile_size * move[1] + self.tile_size / 2, self.tile_size * move[0] + self.tile_size / 2)
                pygame.draw.circle(self.screen, pygame.Color("White"), tile, 7)
                pygame.draw.circle(self.screen, pygame.Color("Black"), tile, 5)

    def change_player(self) -> str:
        if self.current_player == "W":
            self.current_player = "B"
        else:
            self.current_player = "W"

        return self.current_player

    def get_king_position(self) -> tuple[int, int] | tuple[None, None]:
        for x in range(8):
            for y in range(8):
                piece = self.get_piece(y, x)
                if isinstance(piece, King) and piece.color == self.current_player:
                    return y, x

        return None, None

    def is_checked(self) -> bool:
        king_position = self.get_king_position()
        for x in range(8):
            for y in range(8):
                current_piece = self.get_piece(y, x)
                if current_piece is not None and current_piece.color != self.current_player:
                    if isinstance(current_piece, King):
                        options = [(-1, -1), (0, -1), (-1, 1), (-1, 0), (0, 1), (1, -1), (1, 0), (1, 1)]
                        for dir_row, dir_column in options:
                            if Board.is_valid_tile(y + dir_row, x + dir_column) and king_position == (y + dir_row, x + dir_column):
                                return True
                    else:
                        if king_position in current_piece.moves(self, y, x, False):
                            return True

        return False
    
    def moves_out_of_check(self) -> dict[str, list[tuple[int, int]]]:
        king_row, king_column = self.get_king_position()
        moves = {}
        if not self.is_checked():
            return moves
        if king_row is not None and king_column is not None:
            king = self.get_piece(king_row, king_column)
            if king is None:
                return moves
            moves[king.__repr__()] = king.moves(self, king_row, king_column, True)
            for x in range(8):
                for y in range(8):
                    piece = self.get_piece(y, x)
                    if piece is not None and piece.color == self.current_player:
                        piece_moves = piece.moves(self, y, x, True)
                        for row, column in piece_moves:
                            temp_piece = self.get_piece(row, column)
                            self.move_piece(y, x, row, column)

                            if not self.is_checked():
                                if piece not in moves:
                                    moves[piece.__repr__()] = [(row, column)]
                                else:
                                    moves[piece.__repr__()].append((row, column))

                            self.set_piece(piece, y, x)
                            self.set_piece(temp_piece, row, column)
        return moves
    
    def is_checkmated(self) -> bool:
        king_row, king_column = self.get_king_position()
        if king_row is None or king_column is None:
            return True
        if self.is_checked() and list(self.moves_out_of_check().values()) == [[]]:
            return True
        return False
    
    def can_pass(self, king: King, row: int, old_column: int, column: int) -> bool:
        result = True
        
        self.set_piece(king, row, column)
        self.set_piece(None, row, old_column)

        if not self.is_checked():
            result = False

        self.set_piece(king, row, old_column)
        self.set_piece(None, row, column)

        return result
    
    def can_castle(self, side: str):
        row = 7 if self.current_player == "W" else 0
        king = self.get_piece(row, 4)
        
        if side == "king":
            right_rook = self.get_piece(row, 7)
            
            if self.get_piece(row, 5) is not None or self.get_piece(row, 6) is not None:
                return False
            
            if king is not None and right_rook is not None:
                if not isinstance(king, King) or not isinstance(right_rook, Rook):
                    return False
                if king.has_moved or right_rook.has_moved:
                    return False
            else:
                return False
            
            if self.can_pass(king, row, 4, 4) or self.can_pass(king, row, 4, 5) or self.can_pass(king, row, 4, 6):
                return False
            
            return True
        else:
            left_rook = self.get_piece(row, 0)
            
            if self.get_piece(row, 1) is not None or self.get_piece(row, 2) is not None or self.get_piece(row, 3) is not None:
                return False
            
            if king is not None and left_rook is not None:
                if not isinstance(king, King) or not isinstance(left_rook, Rook):
                    return False
                if king.has_moved or left_rook.has_moved:
                    return False
            else:
                return False
            
            if self.can_pass(king, row, 4, 4) or self.can_pass(king, row, 4, 3) or self.can_pass(king, row, 4, 2):
                return False
            
            return True    

    @staticmethod
    def is_valid_tile(row: int, column: int) -> bool:
        return 0 <= row <= 7 and 0 <= column <= 7

from piece import Piece, King, Queen, Rook, Bishop, Knight, Pawn
import pygame


class Board():
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

    def get_piece(self, row: int, column: int) -> Piece:
        return self.board[row][column]

    def set_piece(self, piece: Piece | None, row: int, column: int) -> None:
        self.board[row][column] = piece

    def move_piece(self, old_row: int | None, old_column: int | None, new_row: int | None, new_column: int| None) -> None:
        if old_row != None and old_column != None and new_row != None and new_column != None:
            piece = self.get_piece(old_row, old_column)
            self.set_piece(None, old_row, old_column)
            self.set_piece(piece, new_row, new_column)

    def show_moves(self, moves: list[tuple[int, int]]) -> None:
        if moves != None and moves != []:
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

    @staticmethod
    def valid_tile(row: int, column: int) -> bool:
        return 0 <= row <= 7 and 0 <= column <= 7

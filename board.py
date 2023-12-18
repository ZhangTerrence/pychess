import pygame
import piece


class Board:
    LIGHT = (255, 255, 255)
    DARK = (68, 68, 68)

    def __init__(self, tile_size: int, screen: pygame.SurfaceType, pieces: dict[str, pygame.SurfaceType], current_player: str):
        self.tile_size = tile_size
        self.screen = screen
        self.pieces = pieces
        self.current_player = current_player
        self.board: list[list[piece.Piece | None]] = [[None for _ in range(8)] for _ in range(8)]

        self.init_board()

    def __repr__(self) -> list[list[piece.Piece | None]]:
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
        self.board[7][0] = piece.Rook("W")
        self.board[7][1] = piece.Knight("W")
        self.board[7][2] = piece.Bishop("W")
        self.board[7][3] = piece.Queen("W")
        self.board[7][4] = piece.King("W")
        self.board[7][5] = piece.Bishop("W")
        self.board[7][6] = piece.Knight("W")
        self.board[7][7] = piece.Rook("W")
        for i in range(8):
            self.board[6][i] = piece.Pawn("W")

        self.board[0][0] = piece.Rook("B")
        self.board[0][1] = piece.Knight("B")
        self.board[0][2] = piece.Bishop("B")
        self.board[0][3] = piece.Queen("B")
        self.board[0][4] = piece.King("B")
        self.board[0][5] = piece.Bishop("B")
        self.board[0][6] = piece.Knight("B")
        self.board[0][7] = piece.Rook("B")
        for i in range(8):
            self.board[1][i] = piece.Pawn("B")

    def get_piece(self, row: int, column: int) -> piece.Piece:
        return self.board[row][column]

    def set_piece(self, piece: piece.Piece | None, row: int, column: int) -> None:
        self.board[row][column] = piece

    def move_piece(self, old_row: int | None, old_column: int | None, new_row: int | None, new_column: int| None) -> None:
        if old_row and old_column and new_row and new_column:
            piece = self.get_piece(old_row, old_column)
            self.set_piece(None, old_row, old_column)
            self.set_piece(piece, new_row, new_column)
import pygame


class Board:
    LIGHT = (255, 255, 255)
    DARK = (68, 68, 68)

    def __init__(self, tile_size: int, screen: pygame.SurfaceType, pieces: dict[str, pygame.SurfaceType], player: str):
        self.tile_size = tile_size
        self.screen = screen
        self.pieces = pieces
        self.current_player = player
        self.board = [[None for _ in range(8)] for _ in range(8)]

    def __repr__(self):
        return self.board

    def create_background(self):
        background = pygame.Surface((self.tile_size * 8, self.tile_size * 8))

        light = True
        for x in range(8):
            for y in range(8):
                tile = pygame.Rect(self.tile_size * x, self.tile_size * y, self.tile_size, self.tile_size)
                pygame.draw.rect(background, pygame.Color(self.LIGHT if light else self.DARK), tile)
                light = not light
            light = not light

        return background

    def get_piece(self, row: int, column: int):
        return self.board[row][column]

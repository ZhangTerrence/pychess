import pygame
import board


class Chess:
    TILE_SIZE = 100

    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Pychess")
        pygame.display.set_icon(pygame.image.load("assets/B_Pawn.png"))

        self.screen = pygame.display.set_mode((self.TILE_SIZE * 8, self.TILE_SIZE * 8))
        self.pieces = {
            "W_King": pygame.image.load("assets/W_King.png"),
            "W_Queen": pygame.image.load("assets/W_Queen.png"),
            "W_Rook": pygame.image.load("assets/W_Rook.png"),
            "W_Bishop": pygame.image.load("assets/W_Bishop.png"),
            "W_Knight": pygame.image.load("assets/W_Knight.png"),
            "W_Pawn": pygame.image.load("assets/W_Pawn.png"),
            "B_King": pygame.image.load("assets/B_King.png"),
            "B_Queen": pygame.image.load("assets/B_Queen.png"),
            "B_Rook": pygame.image.load("assets/B_Rook.png"),
            "B_Bishop": pygame.image.load("assets/B_Bishop.png"),
            "B_Knight": pygame.image.load("assets/B_Knight.png"),
            "B_Pawn": pygame.image.load("assets/B_Pawn.png")
        }
        self.current_player = "W"
        self.winner = None
        self.board = board.Board(self.TILE_SIZE, self.screen, self.pieces, self.current_player)

        self.run()

    def run(self) -> None:
        background = self.board.create_background()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return

            self.screen.fill(pygame.Color("Black"))
            self.screen.blit(background, (0, 0))

            pygame.display.flip()


if __name__ == "__main__":
    chess = Chess()

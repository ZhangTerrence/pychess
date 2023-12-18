import pygame
import board
import piece


class Chess:
    TILE_SIZE = 100

    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Pychess")
        pygame.display.set_icon(pygame.image.load("assets/B_Pawn.png"))

        self.screen = pygame.display.set_mode((self.TILE_SIZE * 8, self.TILE_SIZE * 8))
        self.pieces = {
            "W_King": pygame.transform.scale(pygame.image.load("assets/W_King.png"), (64, 64)),
            "W_Queen": pygame.transform.scale(pygame.image.load("assets/W_Queen.png"), (64, 64)),
            "W_Rook": pygame.transform.scale(pygame.image.load("assets/W_Rook.png"), (64, 64)),
            "W_Bishop": pygame.transform.scale(pygame.image.load("assets/W_Bishop.png"), (64, 64)),
            "W_Knight": pygame.transform.scale(pygame.image.load("assets/W_Knight.png"), (64, 64)),
            "W_Pawn": pygame.transform.scale(pygame.image.load("assets/W_Pawn.png"), (64, 64)),
            "B_King": pygame.transform.scale(pygame.image.load("assets/B_King.png"), (64, 64)),
            "B_Queen": pygame.transform.scale(pygame.image.load("assets/B_Queen.png"), (64, 64)),
            "B_Rook": pygame.transform.scale(pygame.image.load("assets/B_Rook.png"), (64, 64)),
            "B_Bishop": pygame.transform.scale(pygame.image.load("assets/B_Bishop.png"), (64, 64)),
            "B_Knight": pygame.transform.scale(pygame.image.load("assets/B_Knight.png"), (64, 64)),
            "B_Pawn": pygame.transform.scale(pygame.image.load("assets/B_Pawn.png"), (64, 64))
        }
        self.current_player = "W"
        self.winner = None
        self.board = board.Board(self.TILE_SIZE, self.screen, self.pieces, self.current_player)

        self.run()

    def run(self) -> None:
        background = self.board.create_background()

        selected_piece = None
        selected_position = None, None

        drop_position = None, None

        while True:
            cursor_piece, cursor_row, cursor_column = self.cursor_details()
            print(selected_piece, selected_position)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return

                if event.type == pygame.MOUSEBUTTONDOWN:
                    selected_position = cursor_row, cursor_column
                    if cursor_piece is not None and cursor_piece.color == self.current_player:
                        selected_piece = cursor_piece
                    else:
                        selected_piece = None
                        selected_position = None, None

                if event.type == pygame.MOUSEBUTTONUP:
                    self.board.move_piece(selected_position[0], selected_position[1], drop_position[0], drop_position[1])

                    selected_piece = None
                    selected_position = None, None


            self.screen.fill(pygame.Color("Black"))
            self.screen.blit(background, (0, 0))

            self.board.draw_pieces()

            self.highlight_piece(cursor_piece, cursor_row, cursor_column)

            drop_position = self.drag(selected_piece)

            pygame.display.flip()

    def cursor_details(self) -> tuple[piece.Piece, int, int] | tuple[None, None, None]:
        position = pygame.Vector2(pygame.mouse.get_pos())
        column, row = [int(x // 100) for x in position]

        try:
            if row >= 0 and column >= 0:
                return self.board.get_piece(row, column), row, column
        except IndexError:
            pass

        return None, None, None

    def highlight_piece(self, cursor_piece: piece.Piece | None, cursor_row: int, cursor_column: int) -> None:
        if cursor_piece:
            tile = (self.TILE_SIZE * cursor_column, self.TILE_SIZE * cursor_row, self.TILE_SIZE, self.TILE_SIZE)
            pygame.draw.rect(self.screen, pygame.Color("Black"), tile, 5)

    def drag(self, selected_piece: piece.Piece | None) -> tuple[int, int] | tuple[None, None]:
        if selected_piece:
            piece, row, column = self.cursor_details()
            piece_image = self.pieces[selected_piece.__repr__()]

            if row is not None:
                tile = (self.TILE_SIZE * column, self.TILE_SIZE * row, self.TILE_SIZE, self.TILE_SIZE)
                pygame.draw.rect(self.screen, pygame.Color("White"), tile, 5)

            position = pygame.Vector2(pygame.mouse.get_pos())
            self.screen.blit(piece_image, piece_image.get_rect(center = position))

            return row, column

        return None, None

if __name__ == "__main__":
    chess = Chess()

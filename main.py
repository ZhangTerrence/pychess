from board import Board
from piece import Piece
import pygame


class Chess:
    def __init__(self, tile_size):
        pygame.init()
        pygame.display.set_caption("Pychess")
        pygame.display.set_icon(pygame.image.load("assets/B_Pawn.png"))

        self.tile_size = tile_size
        self.screen = pygame.display.set_mode((self.tile_size * 8, self.tile_size * 8))
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
        self.board = Board(self.tile_size, self.screen, self.pieces, self.current_player)

        self.run()

    def run(self) -> None:
        background = self.board.create_background()

        selected_piece = None
        selected_position = None, None

        moves = None

        drop_position = None, None

        while True:
            cursor_piece, cursor_row, cursor_column = self.cursor_details()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return

                if event.type == pygame.MOUSEBUTTONDOWN:
                    selected_position = cursor_row, cursor_column
                    if cursor_piece is not None and cursor_piece.color == self.current_player:
                        selected_piece = cursor_piece
                        moves = selected_piece.moves(self.board, cursor_row, cursor_column, True)
                    else:
                        selected_piece = None
                        selected_position = None, None

                if event.type == pygame.MOUSEBUTTONUP:
                    if moves is not None and drop_position in moves:
                        self.board.move_piece(selected_position[0], selected_position[1], drop_position[0], drop_position[1])
                        self.current_player = self.board.change_player()

                    selected_piece = None
                    selected_position = None, None

            self.screen.fill(pygame.Color("Black"))
            self.screen.blit(background, (0, 0))

            self.board.draw_pieces()

            self.highlight_piece(cursor_piece, cursor_row, cursor_column)
            if selected_piece is not None:
                self.board.show_moves(moves)

            drop_position = self.track_drag(selected_piece)

            pygame.display.flip()

    def cursor_details(self) -> tuple[Piece, int, int] | tuple[None, None, None]:
        position_vector = pygame.Vector2(pygame.mouse.get_pos())
        column, row = [int(position // self.tile_size) for position in position_vector]

        try:
            if row >= 0 and column >= 0:
                return self.board.get_piece(row, column), row, column
        except IndexError:
            pass

        return None, None, None

    def highlight_piece(self, cursor_piece: Piece | None, cursor_row: int, cursor_column: int) -> None:
        if cursor_piece is not None:
            tile = (self.tile_size * cursor_column, self.tile_size * cursor_row, self.tile_size, self.tile_size)
            pygame.draw.rect(self.screen, pygame.Color("Dark Gray"), tile, 5)

    def track_drag(self, selected_piece: Piece | None) -> tuple[int, int] | tuple[None, None]:
        if selected_piece is not None:
            _, tracked_row, tracked_column = self.cursor_details()
            selected_piece_image = self.pieces[selected_piece.__repr__()]

            if tracked_row is not None and tracked_column is not None:
                tile = (self.tile_size * tracked_column, self.tile_size * tracked_row, self.tile_size, self.tile_size)
                pygame.draw.rect(self.screen, pygame.Color("Dark Gray"), tile, 5)

            position_vector = pygame.Vector2(pygame.mouse.get_pos())
            self.screen.blit(selected_piece_image, selected_piece_image.get_rect(center=position_vector))

            return tracked_row, tracked_column

        return None, None


if __name__ == "__main__":
    chess = Chess(100)

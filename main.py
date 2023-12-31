from board import Board
from piece import Piece, King, Queen, Rook, Knight, Bishop, Pawn
import pygame


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
        self.board = Board(self.TILE_SIZE, self.screen, self.pieces, self.current_player)

        self.run()

    def run(self) -> None:
        background = self.board.create_background()

        selected_piece = None
        selected_position = None, None

        moves = None

        drop_position = None, None
        
        can_castle = {
            "king": True,
            "queen": True
        }

        while not self.board.is_checkmated():
            cursor_piece, cursor_row, cursor_column = self.cursor_details()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return

                if event.type == pygame.MOUSEBUTTONDOWN:
                    selected_position = cursor_row, cursor_column
                    if cursor_piece is not None and cursor_row is not None and cursor_column is not None:
                        if cursor_piece.color == self.current_player:
                            selected_piece = cursor_piece
                            moves = selected_piece.moves(self.board, cursor_row, cursor_column, True)
                            if isinstance(selected_piece, King):
                                can_castle["king"] = self.board.can_castle("king")
                                can_castle["queen"] = self.board.can_castle("queen")
                    else:
                        selected_piece = None
                        selected_position = None, None

                if event.type == pygame.MOUSEBUTTONUP:
                    if moves is not None and drop_position in moves:
                        self.board.move_piece(selected_position[0], selected_position[1], drop_position[0], drop_position[1])
                        
                        if can_castle["king"] and (drop_position[0], drop_position[1]) == (drop_position[0], 6):
                            self.board.move_piece(drop_position[0], 7, drop_position[0], 5)
                        if can_castle["queen"] and (drop_position[0], drop_position[1]) == (drop_position[0], 2):
                            self.board.move_piece(drop_position[0], 0, drop_position[0], 3)
                    
                        if isinstance(selected_piece, King) or isinstance(selected_piece, Rook):
                            selected_piece.moved()
                            
                        if isinstance(selected_piece, Pawn) and not self.board.is_checked():
                            if selected_piece.color == "W" and drop_position[0] == 0 and drop_position[1] is not None:
                                self.promotion_screen(drop_position[0], drop_position[1])
                            elif selected_piece.color == "B" and drop_position[0] == 7 and drop_position[1] is not None:
                                self.promotion_screen(drop_position[0], drop_position[1])

                        self.current_player = self.board.change_player()
                        
                    selected_piece = None
                    selected_position = None, None

            self.screen.fill(pygame.Color("Black"))
            self.screen.blit(background, (0, 0))

            self.board.draw_pieces()

            if cursor_piece is not None and cursor_row is not None and cursor_column is not None:
                self.highlight_piece(cursor_row, cursor_column)
            if selected_piece is not None and moves is not None:
                self.board.show_moves(moves)

            drop_position = self.track_drag(selected_piece)

            pygame.display.flip()

    def cursor_details(self) -> tuple[Piece | None, int | None, int | None]:
        position_vector = pygame.Vector2(pygame.mouse.get_pos())
        column, row = [int(position // self.TILE_SIZE) for position in position_vector]

        try:
            if row >= 0 and column >= 0:
                return self.board.get_piece(row, column), row, column
        except IndexError:
            pass

        return None, None, None

    def highlight_piece(self, cursor_row: int, cursor_column: int) -> None:
        tile = (self.TILE_SIZE * cursor_column, self.TILE_SIZE * cursor_row, self.TILE_SIZE, self.TILE_SIZE)
        pygame.draw.rect(self.screen, pygame.Color("Dark Gray"), tile, 5)

    def track_drag(self, selected_piece: Piece | None) -> tuple[int | None, int | None]:
        if selected_piece is not None:
            _, tracked_row, tracked_column = self.cursor_details()
            selected_piece_image = self.pieces[selected_piece.__repr__()]

            if tracked_row is not None and tracked_column is not None:
                tile = (self.TILE_SIZE * tracked_column, self.TILE_SIZE * tracked_row, self.TILE_SIZE, self.TILE_SIZE)
                pygame.draw.rect(self.screen, pygame.Color("Dark Gray"), tile, 5)

            position_vector = pygame.Vector2(pygame.mouse.get_pos())
            self.screen.blit(selected_piece_image, selected_piece_image.get_rect(center=position_vector))

            return tracked_row, tracked_column

        return None, None

    def promotion_screen(self, row: int, column: int) -> None:
        while True:
            promotion_screen = pygame.Surface((850, 850))
            promotion_screen.fill((255, 255, 255))

            button_font = pygame.font.SysFont("Arial", 30)

            queen_button = pygame.Rect(300, 300, 100, 50)
            queen_text = button_font.render("Queen", True, pygame.Color("Black"))
            promotion_screen.blit(queen_text, queen_button)

            bishop_button = pygame.Rect(450, 300, 100, 50)
            bishop_text = button_font.render("Bishop", True, pygame.Color("Black"))
            promotion_screen.blit(bishop_text, bishop_button)
        
            rook_button = pygame.Rect(300, 450, 100, 50)
            rook_text = button_font.render("Rook", True, pygame.Color("Black"))
            promotion_screen.blit(rook_text, rook_button)

            knight_button = pygame.Rect(450, 450, 100, 50)
            knight_text = button_font.render("Knight", True, pygame.Color("Black"))
            promotion_screen.blit(knight_text, knight_button)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    
                    if queen_button.collidepoint(event.pos):
                        self.board.set_piece(Queen(self.current_player), row, column)
                        return
                    if bishop_button.collidepoint(event.pos):
                        self.board.set_piece(Bishop(self.current_player), row, column)
                        return
                    if rook_button.collidepoint(event.pos):
                        self.board.set_piece(Rook(self.current_player), row, column)
                        rook = self.board.get_piece(row, column)
                        return
                    if knight_button.collidepoint(event.pos):
                        self.board.set_piece(Knight(self.current_player), row, column)
                        return
                    
            self.screen.blit(promotion_screen, (0, 0))
            pygame.display.flip()

if __name__ == "__main__":
    chess = Chess()

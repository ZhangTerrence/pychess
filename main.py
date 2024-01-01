from types import NoneType
from board import Board
from piece import Piece, King, Queen, Rook, Bishop, Knight, Pawn
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
        self.board = Board(self.TILE_SIZE, self.screen, self.pieces, self.current_player)

        self.run()

    def run(self) -> None:
        background = self.board.create_background()
        winner: str | NoneType = None
        piece_history: dict[str, list[tuple[Piece | None, tuple[int, int]]]] = {
            "W": [],
            "B": []
        }
        
        selected_piece: Piece | None = None
        selected_position: tuple[int, int] = -1, -1 
        moves: list[tuple[int, int]] = []
        drop_position: tuple[int, int] = -1, -1

        while not self.board.is_checkmated():
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
                        selected_position = -1, -1
                        moves = []

                if event.type == pygame.MOUSEBUTTONUP:
                    if len(moves) > 0 and drop_position in moves:              
                        if isinstance(selected_piece, King): # Castle
                            castle_row = drop_position[0]
                            if self.board.can_castle("king") and drop_position == (castle_row, 6):
                                self.board.move_piece(castle_row, 7, castle_row, 5)
                            if self.board.can_castle("queen") and drop_position == (drop_position[0], 2):
                                self.board.move_piece(castle_row, 0, castle_row, 3)
                        
                        if isinstance(selected_piece, Pawn): # En Passant
                            old_row, old_column = selected_position
                            new_row, new_column = drop_position
                            forward = -1 if self.current_player == "W" else 1
                            if old_column > 0 and self.board.can_en_passant(old_row, old_column, "left"):
                                if (new_row, new_column) == (old_row + forward, old_column - 1):
                                    self.board.set_piece(None, old_row, old_column - 1)
                            if old_column < 7 and self.board.can_en_passant(old_row, old_column, "right"):
                                if (new_row, new_column) == (old_row + forward, old_column + 1):
                                    self.board.set_piece(None, old_row, old_column + 1)
                    
                        if isinstance(selected_piece, King) or isinstance(selected_piece, Rook):
                            selected_piece.moved()
                            
                        if isinstance(selected_piece, Pawn):
                            if selected_piece.color == "W" and drop_position[0] == selected_position[0] - 2:
                                selected_piece.update(True)
                            elif selected_piece.color == "B" and drop_position[0] == selected_position[0] + 2:
                                selected_piece.update(True)
                            else:
                                selected_piece.update(False)  
                        
                        self.board.move_piece(selected_position[0], selected_position[1], drop_position[0], drop_position[1])
                        
                        if isinstance(selected_piece, Pawn) and not self.board.is_checked():
                            if selected_piece.color == "W" and drop_position[0] == 0:
                                self.promotion_screen(0, drop_position[1])
                                piece_history[self.current_player].append((selected_piece, drop_position))
                                self.current_player = self.board.change_player()
                                break
                            elif selected_piece.color == "B" and drop_position[0] == 7:
                                self.promotion_screen(7, drop_position[1])
                                piece_history[self.current_player].append((selected_piece, drop_position))
                                self.current_player = self.board.change_player()
                                break
                        
                        piece_history[self.current_player].append((selected_piece, drop_position))
                        history = piece_history[self.current_player]
                        if len(history) > 1 and isinstance(history[-2][0], Pawn):
                            previous_pawn_piece = history[-2][0]
                            previous_pawn_piece.update(False)
                                
                        self.current_player = self.board.change_player()
                        
                    selected_piece = None
                    selected_position = -1, -1
                    
            self.screen.fill(pygame.Color("Black"))
            self.screen.blit(background, (0, 0))
            self.board.draw_pieces()

            if cursor_piece is not None:
                self.highlight_piece(cursor_row, cursor_column)
                
            if selected_piece is not None:
                self.board.show_moves(moves)
                drop_position = self.track_drag(selected_piece)

            pygame.display.flip()
        
        winner = "White" if self.current_player == "B" else "Black"
        
        while winner is not None:
            end_screen = pygame.Surface((self.TILE_SIZE * 8, self.TILE_SIZE * 8))
            end_screen.set_alpha(5)
            end_screen.fill((255, 255, 255))

            winner_font = pygame.font.SysFont("Arial", 50)
            button_font = pygame.font.SysFont("Arial", 30)

            winner_container = pygame.Rect(300, 300, 300, 50)
            winner_text = winner_font.render(winner + " wins!", True, pygame.Color("Black"))
            end_screen.blit(winner_text, winner_container)

            restart_button = pygame.Rect(300, 450, 100, 50)
            restart_text = button_font.render("Restart", True, pygame.Color("Black"))
            end_screen.blit(restart_text, restart_button)

            quit_button = pygame.Rect(475, 450, 100, 50)
            quit_text = button_font.render("Quit", True, pygame.Color("Black"))
            end_screen.blit(quit_text, quit_button)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if restart_button.collidepoint(event.pos):
                        self.reset()
                    if quit_button.collidepoint(event.pos):
                        return

            self.screen.blit(end_screen, (0, 0))
            
            pygame.display.flip()

    def cursor_details(self) -> tuple[Piece | None, int, int]:
        position_vector = pygame.Vector2(pygame.mouse.get_pos())
        column, row = [int(position // self.TILE_SIZE) for position in position_vector]
        if 0 <= row <= 7 and 0 <= column <= 7:
            return self.board.get_piece(row, column), row, column
        else:
            return None, -1, -1

    def highlight_piece(self, cursor_row: int, cursor_column: int) -> None:
        tile = (self.TILE_SIZE * cursor_column, self.TILE_SIZE * cursor_row, self.TILE_SIZE, self.TILE_SIZE)
        pygame.draw.rect(self.screen, pygame.Color("Dark Gray"), tile, 5)

    def track_drag(self, selected_piece: Piece) -> tuple[int, int]:
        _, tracked_row, tracked_column = self.cursor_details()
        selected_piece_image = self.pieces[selected_piece.__repr__()]
        
        tile = (self.TILE_SIZE * tracked_column, self.TILE_SIZE * tracked_row, self.TILE_SIZE, self.TILE_SIZE)
        pygame.draw.rect(self.screen, pygame.Color("Dark Gray"), tile, 5)
        
        position_vector = pygame.Vector2(pygame.mouse.get_pos())
        self.screen.blit(selected_piece_image, selected_piece_image.get_rect(center=position_vector))
        
        return tracked_row, tracked_column

    def promotion_screen(self, row: int, column: int) -> None:
        while True:
            promotion_screen = pygame.Surface((self.TILE_SIZE * 8, self.TILE_SIZE * 8))
            promotion_screen.set_alpha(5)
            promotion_screen.fill((255, 255, 255))

            button_font = pygame.font.SysFont("Arial", 30)

            queen_button = pygame.Rect(300, 300, 100, 50)
            queen_text = button_font.render("Queen", True, pygame.Color("Black"))
            promotion_screen.blit(queen_text, queen_button)

            rook_button = pygame.Rect(300, 450, 100, 50)
            rook_text = button_font.render("Rook", True, pygame.Color("Black"))
            promotion_screen.blit(rook_text, rook_button)

            bishop_button = pygame.Rect(450, 300, 100, 50)
            bishop_text = button_font.render("Bishop", True, pygame.Color("Black"))
            promotion_screen.blit(bishop_text, bishop_button)

            knight_button = pygame.Rect(450, 450, 100, 50)
            knight_text = button_font.render("Knight", True, pygame.Color("Black"))
            promotion_screen.blit(knight_text, knight_button)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.board.set_piece(Queen(self.current_player), row, column)
                    return
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if queen_button.collidepoint(event.pos):
                        self.board.set_piece(Queen(self.current_player), row, column)
                        return
                    if rook_button.collidepoint(event.pos):
                        self.board.set_piece(Rook(self.current_player), row, column)
                        return
                    if bishop_button.collidepoint(event.pos):
                        self.board.set_piece(Bishop(self.current_player), row, column)
                        return
                    if knight_button.collidepoint(event.pos):
                        self.board.set_piece(Knight(self.current_player), row, column)
                        return
                    
            self.screen.blit(promotion_screen, (0, 0))
            
            pygame.display.flip()
            
    def reset(self) -> None:
        self.current_player = "W"
        self.board = Board(self.TILE_SIZE, self.screen, self.pieces, self.current_player)
        self.run()

if __name__ == "__main__":
    chess = Chess()

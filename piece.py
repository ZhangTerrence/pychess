from abc import abstractmethod, ABC


class Piece:
    def __init__(self, color: str):
        self.color = color

    @abstractmethod
    def __repr__(self):
        pass


class King(Piece, ABC):
    def __init__(self, color):
        super().__init__(color)

    def __repr__(self):
        return "W_King" if self.color == "W" else "B_King"


class Queen(Piece, ABC):
    def __init__(self, color):
        super().__init__(color)

    def __repr__(self):
        return "W_Queen" if self.color == "W" else "B_Queen"


class Rook(Piece, ABC):
    def __init__(self, color):
        super().__init__(color)

    def __repr__(self):
        return "W_Rook" if self.color == "W" else "B_Rook"


class Bishop(Piece, ABC):
    def __init__(self, color):
        super().__init__(color)

    def __repr__(self):
        return "W_Bishop" if self.color == "W" else "B_Bishop"


class Knight(Piece, ABC):
    def __init__(self, color):
        super().__init__(color)

    def __repr__(self):
        return "W_Knight" if self.color == "W" else "B_Knight"


class Pawn(Piece, ABC):
    def __init__(self, color):
        super().__init__(color)

    def __repr__(self):
        return "W_Pawn" if self.color == "W" else "B_Pawn"

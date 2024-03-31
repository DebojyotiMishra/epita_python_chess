from typing import List
from abc import ABC, abstractmethod
from dataclasses import dataclass

# class Position():
#     x: int
#     y: int

@dataclass
class Piece(ABC):
    color: str
    
    @abstractmethod
    def __str__(self) -> str:
        pass

class Pawn(Piece):
    def __str__(self) -> str:
        return "♙" if self.color == "white" else "♟"

class Rook(Piece):
    def __str__(self) -> str:
        return "♖" if self.color == "white" else "♜"

class Knight(Piece):
    def __str__(self) -> str:
        return "♘" if self.color == "white" else "♞"

class Bishop(Piece):
    def __str__(self) -> str:
        return "♗" if self.color == "white" else "♝"

class Queen(Piece):
    def __str__(self) -> str:
        return "♕" if self.color == "white" else "♛"

class King(Piece):
    def __str__(self) -> str:
        return "♔" if self.color == "white" else "♚"

class Game():
    board: List[List[Piece]]
    
    def __init__(self):
        Q = Queen
        K = King
        B = Bishop
        N = Knight
        R = Rook
        P = Pawn
        w = "white"
        b = "black"
        
        self.board = [
            [R(w), N(w), B(w), Q(w), K(w), B(w), N(w), R(w)],
            [P(w), P(w), P(w), P(w), P(w), P(w), P(w), P(w)],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [P(b), P(b), P(b), P(b), P(b), P(b), P(b), P(b)],
            [R(b), N(b), B(b), Q(b), K(b), B(b), N(b), R(b)]
        ]
        
    def print_board(self):
        output = ""
        for row in self.board:
            for piece in row:
                if piece is not None:
                    output += str(piece) + " "
                else:
                    output += "  "
            output += "\n"
        print(output, end="")
            
class Chessboard():
    def __init__(self):
        self.game = Game()
        
    def print_board(self):
        self.game.print_board()
    
    def move_piece(self, start: str, end: str):
        pass
    
    def is_check(self, color: str) -> bool:
        pass
    
    def is_checkmate(self, color: str) -> bool:
        pass
    
    def is_stalemate(self, color: str) -> bool:
        pass
    
    def is_draw(self) -> bool:
        pass
    
    def is_game_over(self) -> bool:
        pass
    
    def get_winner(self) -> str:
        pass
    
    def get_piece(self, position: str) -> Piece:
        pass
    
    def get_color(self, position: str) -> str:
        pass
    
    def get_valid_moves(self, position: str) -> List[str]:
        pass
    
    def get_all_valid_moves(self, color: str) -> List[str]:
        pass
    

class ChessboardFactory():
    def create_chessboard(self) -> Chessboard:
        return Chessboard()
    
    def create_chessboard_from_fen(self, fen: str) -> Chessboard:
        pass
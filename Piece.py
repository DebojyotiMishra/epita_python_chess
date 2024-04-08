from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List
from Chessboard import *

@dataclass
class Position:
    x: int
    y: int

@dataclass
class Piece(ABC):
    color: str
    p: Position
        
    @abstractmethod
    def __str__(self) -> str:
        pass

    @abstractmethod
    def get_possible_moves(self):
        pass
    
class Pawn(Piece):
    def __str__(self) -> str:
        return "♙" if self.color == "white" else "♟"

    def get_possible_moves(self) -> List[Position]:
        possible_moves = []
        if self.color == "white":
            # ===== Case: White pawn is blocked by another piece =====
            # if self.board[self.p.y + 1][self.p.x] is not None:
            #     return possible_moves
            # elif self.board[self.p.y + 1][self.p.x] is None:
            #     possible_moves = []
                
            # ===== Case: White pawn is at the last row =====
            if self.p.y == 7:
                possible_moves = []
                
            # ===== Case: White pawn is at the starting row =====
            elif self.p.y == 1:
                # Move forward by 1 or 2 squares
                possible_moves.append(Position(self.p.x, self.p.y + 1))
                possible_moves.append(Position(self.p.x, self.p.y + 2))
            else:
                # Move forward by 1 square
                possible_moves.append(Position(self.p.x, self.p.y + 1))
        else:
            # ===== Case: Black pawn is at the last row =====
            if self.p.y == 1:
                possible_moves = []
                
            # ===== Case: Black pawn is at the starting row =====
            elif self.p.y == 6:
                # Move forward by 1 or 2 squares
                possible_moves.append(Position(self.p.x, self.p.y - 1))
                possible_moves.append(Position(self.p.x, self.p.y - 2))
            else:
            # Move forward by 1 square
                possible_moves.append(Position(self.p.x, self.p.y - 1))
        return possible_moves
    # TODO: check to see if it can take a piece on a diagonal
    # TODO: en passant
    # TODO: promotion


class Rook(Piece):
    def __str__(self) -> str:
        return "♖" if self.color == "white" else "♜"

    def get_possible_moves(self) -> List[Position]:
        # Move horizontally
        possible_moves = []
        for i in range(self.x + 1, 8):
            if self.board[self.y][i] is None:
                possible_moves.append(Position(i, self.y))
            else:
                if self.board[self.y][i].color != self.color:
                    possible_moves.append(Position(i, self.y))
                break
        for i in range(self.x - 1, -1, -1):
            if self.board[self.y][i] is None:
                possible_moves.append(Position(i, self.y))
            else:
                if self.board[self.y][i].color != self.color:
                    possible_moves.append(Position(i, self.y))
                break
        # Move vertically
        for i in range(self.y + 1, 8):
            if self.board[i][self.x] is None:
                possible_moves.append(Position(self.x, i))
            else:
                if self.board[i][self.x].color != self.color:
                    possible_moves.append(Position(self.x, i))
                break
        for i in range(self.y - 1, -1, -1):
            if self.board[i][self.x] is None:
                possible_moves.append(Position(self.x, i))
            else:
                if self.board[i][self.x].color != self.color:
                    possible_moves.append(Position(self.x, i))
                break
            
p1 = Pawn("white", Position(1, 1))
print(p1.p.y)



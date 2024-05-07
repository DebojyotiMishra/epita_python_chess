from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List
import svgwrite
import os


@dataclass
class Position:
    x: int
    y: int

    def to_chess_notation(self) -> str:
        return f"{chr(self.x + 97)}{self.y + 1}"

    def __repr__(self) -> str:
        return f"Position({self.x}, {self.y})"

    def __str__(self) -> str:
        return f"({self.x}, {self.y})"


@dataclass
class Piece(ABC):
    color: str
    position: Position = None
    game: "Game" = None  # type: ignore
    
    @abstractmethod
    def get_possible_moves(self) -> List[Position]:
        pass
    
    @abstractmethod
    def move(self, end: Position) -> None:
        pass
    
    @abstractmethod
    def asText(self) -> str:
        pass
    
    @abstractmethod
    def to_svg(self):
        pass


class Pawn(Piece):
    def __str__(self) -> str:
        return "♙" if self.color == "white" else "♟"

    def get_possible_moves(self) -> List[Position]:
        possible_moves = []

        if self.color == "white":
            # On first square
            if self.position.y == 1:
                if self.game.board[self.position.y + 1][self.position.x] is None:
                    if self.game.board[self.position.y + 2][self.position.x] is None:
                        possible_moves.append(Position(self.position.x, self.position.y + 2))
            
            if self.position.y < 7 and self.game.board[self.position.y + 1][self.position.x] is None:
                possible_moves.append(Position(self.position.x, self.position.y + 1))
                
            if self.position.y == 7:
                return possible_moves
                       
            # Check if the pawn can capture diagonally
            if self.position.x + 1 < 8 and self.position.y + 1 < 8:
                if self.game.board[self.position.y + 1][self.position.x + 1] is not None:
                    if self.game.board[self.position.y + 1][self.position.x + 1].color != self.color:
                            possible_moves.append(Position(self.position.x + 1, self.position.y + 1))
                if self.game.board[self.position.y + 1][self.position.x - 1] is not None:
                    if self.game.board[self.position.y + 1][self.position.x - 1].color != self.color:
                            possible_moves.append(Position(self.position.x - 1, self.position.y + 1))

        else:
            # On first square
            if self.position.y == 6:
                    if self.game.board[self.position.y - 2][self.position.x] is None:
                        possible_moves.append(Position(self.position.x, self.position.y - 2))
            
            if self.position.y > 0 and self.game.board[self.position.y - 1][self.position.x] is None:
                possible_moves.append(Position(self.position.x, self.position.y - 1))
                
            if self.position.y == 0:
                return possible_moves
                       
            # Check if the pawn can capture diagonally
            if self.position.x + 1 < 8 and self.position.y + 1 < 8:
                if self.game.board[self.position.y - 1][self.position.x + 1] is not None:
                    if self.game.board[self.position.y - 1][self.position.x + 1].color != self.color:
                            possible_moves.append(Position(self.position.x + 1, self.position.y - 1))
                if self.game.board[self.position.y - 1][self.position.x - 1] is not None:
                    if self.game.board[self.position.y - 1][self.position.x - 1].color != self.color:
                            possible_moves.append(Position(self.position.x - 1, self.position.y - 1))

        possible_moves = sorted(possible_moves, key=lambda pos: (pos.x, pos.y))
        return possible_moves
    
    def move(self, end: Position) -> None:
        if self.color == "white" and end.y == 7:
            self.game.board[self.position.y][self.position.x] = Queen("white", self.position, self.game)
        elif self.color == "black" and end.y == 0:
            self.game.board[self.position.y][self.position.x] = Queen("black", self.position, self.game)
        else:
            self.game.board[self.position.y][self.position.x] = None
        self.position = end
        self.game.board[end.y][end.x] = self
        
    def asText(self):
        return "Pawn"
    
    def to_svg(self, dwg: svgwrite.Drawing, x: int, y: int):
        # Drawing a pawn
        image_path = os.path.join("src", "images", f"{self.color}_pawn.svg")
        dwg.add(dwg.image(image_path, insert=(x * 50 + 8, y * 50 + 7), size=(35, 35)))
        
        
class Rook(Piece):
    def __str__(self) -> str:
        return "♖" if self.color == "white" else "♜"

    def get_possible_moves(self) -> List[Position]:
        # Move horizontally
        possible_moves = []
        for i in range(self.position.x + 1, 8):
            if self.game.board[self.position.y][i] is None:
                possible_moves.append(Position(i, self.position.y))
            else:
                if self.game.board[self.position.y][i].color != self.color:
                    possible_moves.append(Position(i, self.position.y))
                break
        for i in range(self.position.x - 1, -1, -1):
            if self.game.board[self.position.y][i] is None:
                possible_moves.append(Position(i, self.position.y))
            else:
                if self.game.board[self.position.y][i].color != self.color:
                    possible_moves.append(Position(i, self.position.y))
                break
        # Move vertically
        for i in range(self.position.y + 1, 8):
            if self.game.board[i][self.position.x] is None:
                possible_moves.append(Position(self.position.x, i))
            else:
                if self.game.board[i][self.position.x].color != self.color:
                    possible_moves.append(Position(self.position.x, i))
                break
        for i in range(self.position.y - 1, -1, -1):
            if self.game.board[i][self.position.x] is None:
                possible_moves.append(Position(self.position.x, i))
            else:
                if self.game.board[i][self.position.x].color != self.color:
                    possible_moves.append(Position(self.position.x, i))
                break
            
        possible_moves = sorted(possible_moves, key=lambda pos: (pos.x, pos.y))
        return possible_moves
    
    def move(self, end: Position) -> None:
        self.game.board[self.position.y][self.position.x] = None
        self.position = end
        self.game.board[end.y][end.x] = self
        
    def asText(self):
        return "Rook"
    
    def to_svg(self, dwg: svgwrite.Drawing, x: int, y: int):
        # Drawing a rook
        image_path = os.path.join("src", "images", f"{self.color}_rook.svg")
        dwg.add(dwg.image(image_path, insert=(x * 50 + 8, y * 50 + 7), size=(35, 35)))


class Knight(Piece):
    def __str__(self) -> str:
        return "♘" if self.color == "white" else "♞"

    def get_possible_moves(self) -> List[Position]:
        possible_moves = []
        for dx, dy in [
            (1, 2),
            (2, 1),
            (-1, 2),
            (-2, 1),
            (-1, -2),
            (-2, -1),
            (1, -2),
            (2, -1),
        ]:
            x = self.position.x + dx
            y = self.position.y + dy
            if 0 <= x < 8 and 0 <= y < 8:
                if self.game.board[y][x] is None or self.game.board[y][x].color != self.color:
                    possible_moves.append(Position(x, y))
        
        possible_moves = sorted(possible_moves, key=lambda pos: (pos.x, pos.y))
        return possible_moves
    
    def move(self, end: Position) -> None:
        self.game.board[self.position.y][self.position.x] = None
        self.position = end
        self.game.board[end.y][end.x] = self
        
    def asText(self):
        return "Knight"
    
    def to_svg(self, dwg: svgwrite.Drawing, x: int, y: int):
        # Drawing a knight
        image_path = os.path.join("src", "images", f"{self.color}_knight.svg")
        dwg.add(dwg.image(image_path, insert=(x * 50 + 7, y * 50 + 7), size=(35, 35)))



class Bishop(Piece):
    def __str__(self) -> str:
        return "♗" if self.color == "white" else "♝"

    def get_possible_moves(self) -> List[Position]:
        possible_moves = []
        for dx, dy in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
            x = self.position.x + dx
            y = self.position.y + dy
            while 0 <= x < 8 and 0 <= y < 8:
                if self.game.board[y][x] is None:
                    possible_moves.append(Position(x, y))
                else:
                    if self.game.board[y][x].color != self.color:
                        possible_moves.append(Position(x, y))
                    break
                x += dx
                y += dy
        
        possible_moves = sorted(possible_moves, key=lambda pos: (pos.x, pos.y))
        return possible_moves
    
    def move(self, end: Position) -> None:
        self.game.board[self.position.y][self.position.x] = None
        self.position = end
        self.game.board[end.y][end.x] = self
        
    def asText(self):
        return "Bishop"
    
    def to_svg(self, dwg: svgwrite.Drawing, x: int, y: int):
        # Drawing a bishop
        image_path = os.path.join("src", "images", f"{self.color}_bishop.svg")
        dwg.add(dwg.image(image_path, insert=(x * 50 + 8, y * 50 + 7), size=(35, 35)))


class Queen(Piece):
    def __str__(self) -> str:
        return "♕" if self.color == "white" else "♛"

    def get_possible_moves(self) -> List[Position]:
        possible_moves = []
        for dx, dy in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
            x = self.position.x + dx
            y = self.position.y + dy
            while 0 <= x < 8 and 0 <= y < 8:
                if self.game.board[y][x] is None:
                    possible_moves.append(Position(x, y))
                else:
                    if self.game.board[y][x].color != self.color:
                        possible_moves.append(Position(x, y))
                    break
                x += dx
                y += dy
        for i in range(self.position.x + 1, 8):
            if self.game.board[self.position.y][i] is None:
                possible_moves.append(Position(i, self.position.y))
            else:
                if self.game.board[self.position.y][i].color != self.color:
                    possible_moves.append(Position(i, self.position.y))
                break
        for i in range(self.position.x - 1, -1, -1):
            if self.game.board[self.position.y][i] is None:
                possible_moves.append(Position(i, self.position.y))
            else:
                if self.game.board[self.position.y][i].color != self.color:
                    possible_moves.append(Position(i, self.position.y))
                break
        for i in range(self.position.y + 1, 8):
            if self.game.board[i][self.position.x] is None:
                possible_moves.append(Position(self.position.x, i))
            else:
                if self.game.board[i][self.position.x].color != self.color:
                    possible_moves.append(Position(self.position.x, i))
                break
        for i in range(self.position.y - 1, -1, -1):
            if self.game.board[i][self.position.x] is None:
                possible_moves.append(Position(self.position.x, i))
            else:
                if self.game.board[i][self.position.x].color != self.color:
                    possible_moves.append(Position(self.position.x, i))
                break
        
        possible_moves = sorted(possible_moves, key=lambda pos: (pos.x, pos.y))
        return possible_moves
    
    def move(self, end: Position) -> None:
        self.game.board[self.position.y][self.position.x] = None
        self.position = end
        self.game.board[end.y][end.x] = self
        
    def asText(self):
        return "Queen"
    
    def to_svg(self, dwg: svgwrite.Drawing, x: int, y: int):
        # Drawing a queen
        image_path = os.path.join("src", "images", f"{self.color}_queen.svg")
        dwg.add(dwg.image(image_path, insert=(x * 50 + 8, y * 50 + 7), size=(35, 35)))



class King(Piece):
    def __str__(self) -> str:
        return "♔" if self.color == "white" else "♚"

    def get_possible_moves(self) -> List[Position]:
        possible_moves = []
        for dx, dy in [
            (1, 1),
            (1, -1),
            (-1, 1),
            (-1, -1),
            (1, 0),
            (-1, 0),
            (0, 1),
            (0, -1),
        ]:
            x = self.position.x + dx
            y = self.position.y + dy
            if 0 <= x < 8 and 0 <= y < 8:
                if self.game.board[y][x] is None or self.game.board[y][x].color != self.color:
                        possible_moves.append(Position(x, y))
                
        possible_moves = sorted(possible_moves, key=lambda pos: (pos.x, pos.y))
        return possible_moves
    
    def move(self, end: Position) -> None:
        self.game.board[self.position.y][self.position.x] = None
        self.position = end
        self.game.board[end.y][end.x] = self
        
    def asText(self):
        return "King"
    
    def to_svg(self, dwg: svgwrite.Drawing, x: int, y: int):
        # Drawing a king
        image_path = os.path.join("src", "images", f"{self.color}_king.svg")
        dwg.add(dwg.image(image_path, insert=(x * 50 + 8, y * 50 + 7), size=(35, 35)))

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List
from Chessboard import Game


@dataclass
class Position:
    x: int
    y: int


@dataclass
class Piece(ABC):
    color: str
    p: Position
    g: "Game"

    @abstractmethod
    def __str__(self) -> str:
        pass

    @abstractmethod
    def get_possible_moves(self) -> list[Position]:
        pass


@dataclass
class Pawn(Piece):

    def __str__(self) -> str:
        return "♙" if self.color == "white" else "♟"

    def get_possible_moves(self) -> list[Position]:
        positions = []
        # Check if the piece is white
        if self.color == "white":
            # Check if the pawn is in its starting position
            if self.p.y == 1:
                if (
                    self.g.board[self.p.y + 1][self.p.x] is None
                    and self.g.board[self.p.y + 2][self.p.x] is None
                ):
                    # Add two possible moves: one step forward and two steps forward
                    positions.extend(
                        [
                            Position(self.p.x, self.p.y + 1),
                            Position(self.p.x, self.p.y + 2),
                        ]
                    )
                elif self.g.board[self.p.y + 1][self.p.x] is None:
                    # Add one possible move: one step forward
                    positions.append(Position(self.p.x, self.p.y + 1))

            if self.p.y != 1:
                if (
                    self.g.board[self.p.y + 1][self.p.x] is None
                ):  # One square in front of the pawn is empty
                    # Add one possible move: one step forward
                    positions.append(Position(self.p.x, self.p.y + 1))

            # ==================== White Pawn Diagonal Capture Checks ====================
            # Check for captures on both diagonals
            for dx in [-1, 1]:
                x = self.p.x + dx
                y = self.p.y + 1
                if 0 <= x < 8 and 0 <= y < 8 and self.g.board[y][x] is not None:
                    positions.append(Position(x, y))

        else:
            # Check if the pawn is in its starting position
            if self.p.y == 6:
                if (
                    self.g.board[self.p.y - 1][self.p.x] is None
                    and self.g.board[self.p.y - 2][self.p.x] is None
                ):
                    # Add two possible moves: one step forward and two steps forward
                    positions.extend(
                        [
                            Position(self.p.x, self.p.y - 1),
                            Position(self.p.x, self.p.y - 2),
                        ]
                    )
                elif self.g.board[self.p.y - 1][self.p.x] is None:
                    # Add one possible move: one step forward
                    positions.append(Position(self.p.x, self.p.y - 1))

            if self.p.y != 6:
                if self.g.board[self.p.y - 1][self.p.x] is None:
                    # Add one possible moves: one step forward
                    positions.append(Position(self.p.x, self.p.y - 1))

            # ==================== Black Pawn Diagonal Capture Checks ====================
            # Check for captures on both diagonals
            for dx in [-1, 1]:
                x = self.p.x + dx
                y = self.p.y - 1
                if 0 <= x < 8 and 0 <= y < 8 and self.g.board[y][x] is not None:
                    positions.append(Position(x, y))

        empty_positions = []
        # Check if the positions are within the chessboard boundaries and if they are empty
        for p in positions:
            if not (0 <= p.x <= 7 and 0 <= p.y <= 7):
                continue
            if self.g.board[p.y][p.x] is None:
                empty_positions.append(p)

        return empty_positions

    # TODO: check to see if it can take a piece on a diagonal ✅
    # TODO: en passant
    # TODO: promotion


class Rook(Piece):
    def __str__(self) -> str:
        return "♖" if self.color == "white" else "♜"

    def get_possible_moves(self) -> List[Position]:
        # Move horizontally
        possible_moves = []
        for i in range(self.p.x + 1, 8):
            if self.g.board[self.p.y][i] is None:
                possible_moves.append(Position(i, self.p.y))
            else:
                if self.g.board[self.p.y][i].color != self.color:
                    possible_moves.append(Position(i, self.p.y))
                break
        for i in range(self.p.x - 1, -1, -1):
            if self.g.board[self.p.y][i] is None:
                possible_moves.append(Position(i, self.p.y))
            else:
                if self.g.board[self.p.y][i].color != self.color:
                    possible_moves.append(Position(i, self.p.y))
                break
        # Move vertically
        for i in range(self.p.y + 1, 8):
            if self.g.board[i][self.p.x] is None:
                possible_moves.append(Position(self.p.x, i))
            else:
                if self.g.board[i][self.p.x].color != self.color:
                    possible_moves.append(Position(self.p.x, i))
                break
        for i in range(self.p.y - 1, -1, -1):
            if self.g.board[i][self.p.x] is None:
                possible_moves.append(Position(self.p.x, i))
            else:
                if self.g.board[i][self.p.x].color != self.color:
                    possible_moves.append(Position(self.p.x, i))
                break
        return possible_moves


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
            x = self.p.x + dx
            y = self.p.y + dy
            if 0 <= x < 8 and 0 <= y < 8:
                if self.g.board[y][x] is None:
                    possible_moves.append(Position(x, y))
                elif self.g.board[y][x].color != self.color:
                    possible_moves.append(Position(x, y))
        return possible_moves


class Bishop(Piece):
    def __str__(self) -> str:
        return "♗" if self.color == "white" else "♝"

    def get_possible_moves(self) -> List[Position]:
        possible_moves = []
        for dx, dy in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
            x = self.p.x + dx
            y = self.p.y + dy
            while 0 <= x < 8 and 0 <= y < 8:
                if self.g.board[y][x] is None:
                    possible_moves.append(Position(x, y))
                else:
                    if self.g.board[y][x].color != self.color:
                        possible_moves.append(Position(x, y))
                    break
                x += dx
                y += dy
        return possible_moves


class Queen(Piece):
    def __str__(self) -> str:
        return "♕" if self.color == "white" else "♛"

    def get_possible_moves(self) -> List[Position]:
        possible_moves = []
        for dx, dy in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
            x = self.p.x + dx
            y = self.p.y + dy
            while 0 <= x < 8 and 0 <= y < 8:
                if self.g.board[y][x] is None:
                    possible_moves.append(Position(x, y))
                else:
                    if self.g.board[y][x].color != self.color:
                        possible_moves.append(Position(x, y))
                    break
                x += dx
                y += dy
        for i in range(self.p.x + 1, 8):
            if self.g.board[self.p.y][i] is None:
                possible_moves.append(Position(i, self.p.y))
            else:
                if self.g.board[self.p.y][i].color != self.color:
                    possible_moves.append(Position(i, self.p.y))
                break
        for i in range(self.p.x - 1, -1, -1):
            if self.g.board[self.p.y][i] is None:
                possible_moves.append(Position(i, self.p.y))
            else:
                if self.g.board[self.p.y][i].color != self.color:
                    possible_moves.append(Position(i, self.p.y))
                break
        for i in range(self.p.y + 1, 8):
            if self.g.board[i][self.p.x] is None:
                possible_moves.append(Position(self.p.x, i))
            else:
                if self.g.board[i][self.p.x].color != self.color:
                    possible_moves.append(Position(self.p.x, i))
                break
        for i in range(self.p.y - 1, -1, -1):
            if self.g.board[i][self.p.x] is None:
                possible_moves.append(Position(self.p.x, i))
            else:
                if self.g.board[i][self.p.x].color != self.color:
                    possible_moves.append(Position(self.p.x, i))
                break
        return possible_moves


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
            x = self.p.x + dx
            y = self.p.y + dy
            if 0 <= x < 8 and 0 <= y < 8:
                if self.g.board[y][x] is None:
                    possible_moves.append(Position(x, y))
                elif self.g.board[y][x].color != self.color:
                    possible_moves.append(Position(x, y))
        return possible_moves


class Empty(Piece):
    def __str__(self) -> str:
        return " "

    def get_possible_moves(self) -> List[Position]:
        return []


# Test the code
g = Game()
p1 = King("white", Position(4, 4), g)
print(p1.get_possible_moves())

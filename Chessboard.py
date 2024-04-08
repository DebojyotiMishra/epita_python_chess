from typing import List

class Position:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

class ChessPiece:
    def __init__(self, color: str):
        self.color = color

    def __str__(self) -> str:
        pass

    def get_possible_moves(self) -> List[Position]:
        pass

class Pawn(ChessPiece):
    def __str__(self) -> str:
        return "♙" if self.color == "white" else "♟"

    def get_possible_moves(self) -> List[Position]:
        # Implement the logic to calculate possible moves for a pawn
        possible_moves = []
        if self.color == "white":
            if self.y == 1:
                # Move forward by 1 or 2 squares
                possible_moves.append(Position(self.x, self.y + 1))
                possible_moves.append(Position(self.x, self.y + 2))
            else:
                # Move forward by 1 square
                possible_moves.append(Position(self.x, self.y + 1))
        else:
            if self.y == 6:
                # Move forward by 1 or 2 squares
                possible_moves.append(Position(self.x, self.y - 1))
                possible_moves.append(Position(self.x, self.y - 2))
            else:
            # Move forward by 1 square
                possible_moves.append(Position(self.x, self.y - 1))
        return possible_moves

class Rook(ChessPiece):
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

class Knight(ChessPiece):
    def __str__(self) -> str:
        return "♘" if self.color == "white" else "♞"

    def get_possible_moves(self) -> List[Position]:
        # Implement the logic to calculate possible moves for a knight
        pass

class Bishop(ChessPiece):
    def __str__(self) -> str:
        return "♗" if self.color == "white" else "♝"

    def get_possible_moves(self) -> List[Position]:
        # Implement the logic to calculate possible moves for a bishop
        pass

class Queen(ChessPiece):
    def __str__(self) -> str:
        return "♕" if self.color == "white" else "♛"

    def get_possible_moves(self) -> List[Position]:
        # Implement the logic to calculate possible moves for a queen
        pass

class King(ChessPiece):
    def __str__(self) -> str:
        return "♔" if self.color == "white" else "♚"

    def get_possible_moves(self) -> List[Position]:
        # Implement the logic to calculate possible moves for a king
        pass

class Game:
    board: List[List[ChessPiece]]
    
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

g = Game()
g.print_board()


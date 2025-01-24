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
    def __init__(self, color: str, position: Position = None, game: "Game" = None):
        super().__init__(color, position, game)
        self.has_moved = False
        self.en_passant_vulnerable = False  # Track if pawn just made a two-square move

    def __str__(self) -> str:
        return "♙" if self.color == "white" else "♟"

    def get_possible_moves(self) -> List[Position]:
        possible_moves = []

        if self.color == "white":
            # Normal moves
            if self.position.y < 7:
                if self.game.board[self.position.y + 1][self.position.x] is None:
                    possible_moves.append(Position(self.position.x, self.position.y + 1))
                    # First move - two squares
                    if not self.has_moved and self.position.y == 1:
                        if self.game.board[self.position.y + 2][self.position.x] is None:
                            possible_moves.append(Position(self.position.x, self.position.y + 2))
            
            # Diagonal captures and en passant
            if self.position.y < 7:  # Can capture forward
                # Right diagonal capture
                if self.position.x + 1 < 8:
                    # Normal capture
                    target = self.game.board[self.position.y + 1][self.position.x + 1]
                    if target is not None and target.color != self.color:
                        possible_moves.append(Position(self.position.x + 1, self.position.y + 1))
                    # En passant
                    if self.position.y == 4:  # White pawns can only en passant from rank 5
                        target = self.game.board[self.position.y][self.position.x + 1]
                        if (isinstance(target, Pawn) and 
                            target.color != self.color and 
                            target.en_passant_vulnerable):
                            possible_moves.append(Position(self.position.x + 1, self.position.y + 1))
                
                # Left diagonal capture
                if self.position.x - 1 >= 0:
                    # Normal capture
                    target = self.game.board[self.position.y + 1][self.position.x - 1]
                    if target is not None and target.color != self.color:
                        possible_moves.append(Position(self.position.x - 1, self.position.y + 1))
                    # En passant
                    if self.position.y == 4:  # White pawns can only en passant from rank 5
                        target = self.game.board[self.position.y][self.position.x - 1]
                        if (isinstance(target, Pawn) and 
                            target.color != self.color and 
                            target.en_passant_vulnerable):
                            possible_moves.append(Position(self.position.x - 1, self.position.y + 1))

        else:  # Black pawn
            # Normal moves
            if self.position.y > 0:
                if self.game.board[self.position.y - 1][self.position.x] is None:
                    possible_moves.append(Position(self.position.x, self.position.y - 1))
                    # First move - two squares
                    if not self.has_moved and self.position.y == 6:
                        if self.game.board[self.position.y - 2][self.position.x] is None:
                            possible_moves.append(Position(self.position.x, self.position.y - 2))
            
            # Diagonal captures and en passant
            if self.position.y > 0:  # Can capture forward
                # Right diagonal capture
                if self.position.x + 1 < 8:
                    # Normal capture
                    target = self.game.board[self.position.y - 1][self.position.x + 1]
                    if target is not None and target.color != self.color:
                        possible_moves.append(Position(self.position.x + 1, self.position.y - 1))
                    # En passant
                    if self.position.y == 3:  # Black pawns can only en passant from rank 4
                        target = self.game.board[self.position.y][self.position.x + 1]
                        if (isinstance(target, Pawn) and 
                            target.color != self.color and 
                            target.en_passant_vulnerable):
                            possible_moves.append(Position(self.position.x + 1, self.position.y - 1))
                
                # Left diagonal capture
                if self.position.x - 1 >= 0:
                    # Normal capture
                    target = self.game.board[self.position.y - 1][self.position.x - 1]
                    if target is not None and target.color != self.color:
                        possible_moves.append(Position(self.position.x - 1, self.position.y - 1))
                    # En passant
                    if self.position.y == 3:  # Black pawns can only en passant from rank 4
                        target = self.game.board[self.position.y][self.position.x - 1]
                        if (isinstance(target, Pawn) and 
                            target.color != self.color and 
                            target.en_passant_vulnerable):
                            possible_moves.append(Position(self.position.x - 1, self.position.y - 1))

        # Filter moves that would put own king in check
        possible_moves = [move for move in possible_moves if not self._would_be_in_check(move)]
        return sorted(possible_moves, key=lambda pos: (pos.x, pos.y))

    def move(self, end: Position) -> None:
        # Handle en passant capture
        if abs(end.x - self.position.x) == 1 and self.game.board[end.y][end.x] is None:
            # This must be an en passant capture
            captured_pawn_y = self.position.y
            self.game.board[captured_pawn_y][end.x] = None

        # Reset en passant vulnerability for all pawns
        for row in self.game.board:
            for piece in row:
                if isinstance(piece, Pawn):
                    piece.en_passant_vulnerable = False

        # Set en passant vulnerability if moving two squares
        if abs(end.y - self.position.y) == 2:
            self.en_passant_vulnerable = True

        # Handle promotion
        if (self.color == "white" and end.y == 7) or (self.color == "black" and end.y == 0):
            self.game.board[self.position.y][self.position.x] = None
            self.game.board[end.y][end.x] = Queen(self.color, end, self.game)
        else:
            self.game.board[self.position.y][self.position.x] = None
            self.position = end
            self.game.board[end.y][end.x] = self
            
        self.has_moved = True

    def _would_be_in_check(self, end: Position) -> bool:
        # Create a copy of the game state
        original_position = self.position
        original_board = [row[:] for row in self.game.board]
        
        # Make the move
        self.game.board[self.position.y][self.position.x] = None
        self.position = end
        self.game.board[end.y][end.x] = self
        
        # Check if the move would put own king in check
        in_check = self.game.is_check(self.color)
        
        # Restore the original state
        self.position = original_position
        self.game.board = original_board
        
        return in_check

    def asText(self):
        return "Pawn"
    
    def to_svg(self, dwg: svgwrite.Drawing, x: int, y: int):
        # Drawing a pawn
        image_path = os.path.join("src", "images", f"{self.color}_pawn.svg")
        dwg.add(dwg.image(image_path, insert=(x * 50 + 8, y * 50 + 7), size=(35, 35)))
        
        
class Rook(Piece):
    def __init__(self, color: str, position: Position = None, game: "Game" = None):
        super().__init__(color, position, game)
        self.has_moved = False

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
        self.has_moved = True
        
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
        # Normal moves
        for dx, dy in [
            (1, 1), (1, -1), (-1, 1), (-1, -1),
            (1, 0), (-1, 0), (0, 1), (0, -1),
        ]:
            x = self.position.x + dx
            y = self.position.y + dy
            if 0 <= x < 8 and 0 <= y < 8:
                if self.game.board[y][x] is None or self.game.board[y][x].color != self.color:
                    if not self._would_square_be_attacked(Position(x, y)):
                        possible_moves.append(Position(x, y))
        
        # Castling moves
        if not hasattr(self, 'has_moved'):
            self.has_moved = False
            
        if not self.has_moved:
            # Only check castling if the king is not in check
            king_pos = Position(self.position.x, self.position.y)
            if not self._would_square_be_attacked(king_pos):
                # Kingside castling
                if (self.position.x == 4 and 
                    (self.position.y == 0 if self.color == "white" else self.position.y == 7)):
                    if (self.game.board[self.position.y][7] is not None and 
                        isinstance(self.game.board[self.position.y][7], Rook) and
                        not getattr(self.game.board[self.position.y][7], 'has_moved', True)):
                        if (self.game.board[self.position.y][5] is None and 
                            self.game.board[self.position.y][6] is None):
                            # Check if squares are under attack
                            if (not self._would_square_be_attacked(Position(5, self.position.y)) and
                                not self._would_square_be_attacked(Position(6, self.position.y))):
                                possible_moves.append(Position(6, self.position.y))
                        
                # Queenside castling
                if (self.position.x == 4 and 
                    (self.position.y == 0 if self.color == "white" else self.position.y == 7)):
                    if (self.game.board[self.position.y][0] is not None and 
                        isinstance(self.game.board[self.position.y][0], Rook) and
                        not getattr(self.game.board[self.position.y][0], 'has_moved', True)):
                        if (self.game.board[self.position.y][1] is None and 
                            self.game.board[self.position.y][2] is None and
                            self.game.board[self.position.y][3] is None):
                            # Check if squares are under attack
                            if (not self._would_square_be_attacked(Position(2, self.position.y)) and
                                not self._would_square_be_attacked(Position(3, self.position.y))):
                                possible_moves.append(Position(2, self.position.y))
                
        return sorted(possible_moves, key=lambda pos: (pos.x, pos.y))

    def _would_square_be_attacked(self, pos: Position) -> bool:
        """Check if a square would be attacked by any opponent piece without recursion"""
        for row in self.game.board:
            for piece in row:
                if piece is not None and piece.color != self.color:
                    # For pawns, check their attack pattern directly
                    if isinstance(piece, Pawn):
                        if piece.color == "white":
                            if (piece.position.y + 1 == pos.y and 
                                abs(piece.position.x - pos.x) == 1):
                                return True
                        else:
                            if (piece.position.y - 1 == pos.y and 
                                abs(piece.position.x - pos.x) == 1):
                                return True
                        continue

                    # For knights, check their movement pattern directly
                    if isinstance(piece, Knight):
                        dx = abs(piece.position.x - pos.x)
                        dy = abs(piece.position.y - pos.y)
                        if (dx == 2 and dy == 1) or (dx == 1 and dy == 2):
                            return True
                        continue

                    # For other pieces, check if there's a clear path
                    dx = pos.x - piece.position.x
                    dy = pos.y - piece.position.y

                    # Rook-like movements (horizontal/vertical)
                    if isinstance(piece, (Rook, Queen)):
                        if dx == 0 or dy == 0:
                            step_x = 0 if dx == 0 else dx // abs(dx)
                            step_y = 0 if dy == 0 else dy // abs(dy)
                            x, y = piece.position.x + step_x, piece.position.y + step_y
                            clear_path = True
                            while (x, y) != (pos.x, pos.y):
                                if self.game.board[y][x] is not None:
                                    clear_path = False
                                    break
                                x += step_x
                                y += step_y
                            if clear_path:
                                return True

                    # Bishop-like movements (diagonal)
                    if isinstance(piece, (Bishop, Queen)):
                        if abs(dx) == abs(dy):
                            step_x = dx // abs(dx)
                            step_y = dy // abs(dy)
                            x, y = piece.position.x + step_x, piece.position.y + step_y
                            clear_path = True
                            while (x, y) != (pos.x, pos.y):
                                if self.game.board[y][x] is not None:
                                    clear_path = False
                                    break
                                x += step_x
                                y += step_y
                            if clear_path:
                                return True

                    # King attacks (one square in any direction)
                    if isinstance(piece, King):
                        if abs(dx) <= 1 and abs(dy) <= 1:
                            return True

        return False

    def move(self, end: Position) -> None:
        # Handle castling
        if not self.has_moved and abs(end.x - self.position.x) == 2:
            # Kingside castling
            if end.x == 6:
                rook = self.game.board[self.position.y][7]
                self.game.board[self.position.y][7] = None
                self.game.board[self.position.y][5] = rook
                rook.position = Position(5, self.position.y)
                rook.has_moved = True
            # Queenside castling
            elif end.x == 2:
                rook = self.game.board[self.position.y][0]
                self.game.board[self.position.y][0] = None
                self.game.board[self.position.y][3] = rook
                rook.position = Position(3, self.position.y)
                rook.has_moved = True
                
        self.game.board[self.position.y][self.position.x] = None
        self.position = end
        self.game.board[end.y][end.x] = self
        self.has_moved = True
        
    def asText(self):
        return "King"
    
    def to_svg(self, dwg: svgwrite.Drawing, x: int, y: int):
        # Drawing a king
        image_path = os.path.join("src", "images", f"{self.color}_king.svg")
        dwg.add(dwg.image(image_path, insert=(x * 50 + 8, y * 50 + 7), size=(35, 35)))

import copy
from typing import List
from Piece import Queen, Rook, Knight, Bishop, King, Pawn, Position, Piece
import svgwrite


class Game:
    board: List[List[Piece]]

    def __init__(self):
        self.board = [
            [
                Rook("white"),
                Knight("white"),
                Bishop("white"),
                King("white"),
                Queen("white"),
                Bishop("white"),
                Knight("white"),
                Rook("white"),
            ],
            [
                Pawn("white"),
                Pawn("white"),
                Pawn("white"),
                Pawn("white"),
                Pawn("white"),
                Pawn("white"),
                Pawn("white"),
                Pawn("white"),
            ],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [
                Pawn("black"),
                Pawn("black"),
                Pawn("black"),
                Pawn("black"),
                Pawn("black"),
                Pawn("black"),
                Pawn("black"),
                Pawn("black"),
            ],
            [
                Rook("black"),
                Knight("black"),
                Bishop("black"),
                King("black"),
                Queen("black"),
                Bishop("black"),
                Knight("black"),
                Rook("black"),
            ],
        ]

        for y in range(8):
            for x in range(8):
                if self.board[y][x] is not None:
                    piece = self.board[y][x]
                    if isinstance(piece, Piece):
                        piece.position = Position(x, y)
                        piece.game = self

        self.move_log = []
        self.current_turn = "white"

    def print_board(self) -> None:
        for row in self.board:
            for piece in row:
                print(piece if piece else " ", end=" ")
            print()

    def get_piece_at(self, position: Position) -> Piece:
        return self.board[position.y][position.x]

    def chess_notation_to_position(self, notation: str) -> Position:
        column_to_letter = {
            7: "a",
            6: "b",
            5: "c",
            4: "d",
            3: "e",
            2: "f",
            1: "g",
            0: "h",
        }
        row = int(notation[1]) - 1

        column = list(column_to_letter.keys())[
            list(column_to_letter.values()).index(notation[0])
        ]
        return Position(column, row)

    def full_chess_notation_to_position(self, notation: str) -> Position:
        # takes in input like a1-a2 and returns the start and end positions
        # start position is the letters before the dash and the end position is the letters after the dash
        # start = self.chess_notation_to_position(notation[:2])
        # end = self.chess_notation_to_position(notation[3:])
        # return start, end

        # Handle moves like "Ra1-a2", "Nf3-f4", "e2-e4", "Rd1xd8", "Qd1xd4"
        if "x" in notation or "X" in notation:
            moves = notation.split("x") if "x" in notation else notation.split("X")
            # checking start moves
            if len(moves[0]) == 3:
                start = self.chess_notation_to_position(moves[0][1:])
            if len(moves[0]) == 2:
                start = self.chess_notation_to_position(moves[0])
            # checking end moves
            if len(moves[1]) == 2:
                end = self.chess_notation_to_position(moves[1])
            if len(moves[1]) == 3:
                end = self.chess_notation_to_position(moves[1][1:])

            return start, end

        elif "-" in notation:
            moves = notation.split("-")
            if len(moves[0]) == 2:
                start = self.chess_notation_to_position(moves[0])
            if len(moves[1]) == 2:
                end = self.chess_notation_to_position(moves[1])
            if len(moves[0]) == 3:
                start = self.chess_notation_to_position(moves[0][1:])
            if len(moves[1]) == 3:
                end = self.chess_notation_to_position(moves[1][1:])
            return start, end

        else:
            raise ValueError("Invalid move")

    def make_move(self, start: Position, end: Position) -> None:
        if not (0 <= start.x < 8 and 0 <= start.y < 8 and 0 <= end.x < 8 and 0 <= end.y < 8):
            raise ValueError("Invalid position")

        piece = self.board[start.y][start.x]
        if piece is None:
            raise ValueError("No piece at start position")
            
        if piece.color != self.current_turn:
            raise ValueError("Not your turn")

        valid_moves = piece.get_possible_moves()
        if end not in valid_moves:
            raise ValueError("Invalid move")

        # Make the move
        captured_piece = self.board[end.y][end.x]
        piece.move(end)
        
        # Log the move
        self.move_log.append({
            'piece': piece.asText(),
            'color': piece.color,
            'start': start,
            'end': end,
            'captured': captured_piece.asText() if captured_piece else None
        })
        
        # Switch turns
        self.current_turn = "black" if self.current_turn == "white" else "white"

    def is_valid_move(self, start: Position, end: Position) -> bool:
        if not (
            0 <= start.x < 8 and 0 <= start.y < 8 and 0 <= end.x < 8 and 0 <= end.y < 8
        ):
            return False

        piece = self.board[start.y][start.x]

        if piece is None:
            return False

        valid_moves = piece.get_possible_moves()

        if end not in valid_moves:
            return False

        return True

    def is_check(self, color: str) -> bool:
        # Find the position of the king
        for row in self.board:
            for piece in row:
                if isinstance(piece, King) and piece.color == color:
                    king_position = piece.position
                    break

        # Check if any opponent piece can attack the king
        for row in self.board:
            for piece in row:
                if isinstance(piece, Piece) and piece.color != color:
                    valid_moves = piece.get_possible_moves()
                    if king_position in valid_moves:
                        return True

        return False

    def is_checkmate(self, color: str) -> bool:
        if not self.is_check(color):
            return False

        for row in self.board:
            for piece in row:
                if isinstance(piece, Piece) and piece.color == color:
                    valid_moves = piece.get_possible_moves()
                    for move in valid_moves:
                        # Make a copy of the game and simulate the move
                        copy_game = copy.deepcopy(self)
                        copy_game.make_move(piece.position, move)
                        # Check if the opponent's king is still in check after the move
                        if not copy_game.is_check(color):
                            return False

        return True

    def is_stalemate(self, color: str) -> bool:
        if self.is_check(color):
            return False

        for row in self.board:
            for piece in row:
                if isinstance(piece, Piece) and piece.color == color:
                    valid_moves = piece.get_possible_moves()
                    for move in valid_moves:
                        # Make a copy of the game and simulate the move
                        copy_game = copy.deepcopy(self)
                        copy_game.make_move(piece.position, move)
                        # Check if the opponent's king is still in check after the move
                        if not copy_game.is_check(color):
                            return False

        return True

    def is_draw(self) -> bool:
        return self.is_stalemate("white") or self.is_stalemate("black")

    def to_svg(self) -> str:
        dwg = svgwrite.Drawing(profile="tiny", size=("450px", "450px"))

        # Drawing the squares
        for y in range(8):
            for x in range(8):
                color = "#ffffff" if (x + y) % 2 == 0 else "#bfbfbf"
                dwg.add(
                    dwg.rect(
                        (50 * x, 50 * y),
                        (50, 50),
                        fill=color,
                        stroke="#000000",
                        stroke_width=0.2,
                    )
                )

        # Drawing the pieces
        for y in range(8):
            for x in range(8):
                piece = self.board[y][x]
                if piece:
                    piece.to_svg(dwg, x, y)

        # Drawing the notations
        for i in range(8):
            # Add numbers
            dwg.add(
                dwg.text(
                    str(8 - i),
                    insert=(415, (7 - i) * 50 + 30),
                    fill="#3d3d3d",
                    font_size=20,
                    font_family="serif",
                    text_anchor="middle",
                )
            )

            # Add letters
            dwg.add(
                dwg.text(
                    chr(104 - i),
                    insert=(i * 50 + 25, 425),
                    fill="#3d3d3d",
                    font_size=20,
                    font_family="serif",
                    text_anchor="middle",
                )
            )

        return dwg.tostring()


# Test
if __name__ == "__main__":
    game = Game()
    svg_content = game.to_svg()
    with open("chessboard.svg", "w") as f:
        f.write(svg_content)

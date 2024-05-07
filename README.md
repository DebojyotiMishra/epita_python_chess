# Chess Game

This is a simple chess game implemented in Python. It allows two players to play chess through the console. The graphical representation of the board is generated and saved as an SVG file.

## Files

The game consists of the following files:
1. Chessboard.py
2. Piece.py
3. main.py

<br>
<hr>

### Chessboard.py

This file contains the classes necessary to define the chessboard, make moves on the board, and implement game logic.


#### Game class

- `board: List[List[Union[Piece, None]]]`: Represents the chessboard.
- `white_king: King`: Represents the white king.
- `black_king: King`: Represents the black king.
- `white_king_position: Position`: Represents the position of the white king.
- `black_king_position: Position`: Represents the position of the black king.

**Methods:**

- `__init__(self)`: Initializes the chessboard and the pieces.
- `full_chess_notation_to_position(self, move: str) -> Tuple[Position, Position]`: Converts the chess notation to a position.
- `is_valid_move(self, start: Position, end: Position) -> bool`: Checks if the move is valid.
- `make_move(self, start: Position, end: Position) -> None`: Moves a piece on the chessboard.
- `can_castle_kingside(self, color: str) -> bool`: Checks if the specified color can castle kingside.
- `castle_kingside(self, color: str) -> None`: Castles kingside for the specified color.
- `can_castle_queenside(self, color: str) -> bool`: Checks if the specified color can castle queenside.
- `castle_queenside(self, color: str) -> None`: Castles queenside for the specified color.
- `update_valid_moves(self, color: str) -> None`: Updates the valid moves for the specified color.
- `is_check(self, color: str) -> bool`: Checks if the specified color is in check.
- `is_checkmate(self, color: str) -> bool`: Checks if the specified color is in checkmate.
- `is_draw(self) -> bool`: Checks if the game is a draw.
- `to_svg(self) -> str`: Generates the SVG representation of the chessboard.

<br>
<hr>

### Piece.py

This file contains the definition of each piece type used in the game.

#### Position class

- `x: int`: Represents the x-coordinate of the position.
- `y: int`: Represents the y-coordinate of the position.

    **Methods:**

    - `to_chess_notation(self) -> str`: Returns the chess notation for the position.
    - `__repr__(self) -> str`: Returns the string representation of the position.
    - `__str__(self) -> str`: Returns the formatted string representation of the position.

#### Piece class

- `color: str`: Represents the color of the piece.
- `position: Position = None`: Represents the position of the piece.
- `game: "Game" = None`: Represents the current game.

    **Methods:**

    - `get_possible_moves(self) -> List[Position]`: Abstract method to get possible moves for a piece.
    - `move(self, end: Position) -> None`: Abstract method to move a piece.
    - `asText(self) -> str`: Abstract method to represent the piece as text.
    - `to_svg(self)`: Abstract method to generate the SVG representation of the piece.

#### Pawn class (inherits from Piece)

- `get_possible_moves(self) -> List[Position]`: Returns the list of possible moves for the pawn.
- `move(self, end: Position) -> None`: Moves the pawn to the specified position.
- `asText(self)`: Returns the text representation of the pawn.
- `to_svg(self, dwg: svgwrite.Drawing, x: int, y: int)`: Generates the SVG representation of the pawn.

#### Rook class (inherits from Piece)

- `get_possible_moves(self) -> List[Position]`: Returns the list of possible moves for the rook.
- `move(self, end: Position) -> None`: Moves the rook to the specified position.
- `asText(self)`: Returns the text representation of the rook.
- `to_svg(self, dwg: svgwrite.Drawing, x: int, y: int)`: Generates the SVG representation of the rook.

#### Knight class (inherits from Piece)

- `get_possible_moves(self) -> List[Position]`: Returns the list of possible moves for the knight.
- `move(self, end: Position) -> None`: Moves the knight to the specified position.
- `asText(self)`: Returns the text representation of the knight.
- `to_svg(self, dwg: svgwrite.Drawing, x: int, y: int)`: Generates the SVG representation of the knight.

#### Bishop class (inherits from Piece)

- `get_possible_moves(self) -> List[Position]`: Returns the list of possible moves for the bishop.
- `move(self, end: Position) -> None`: Moves the bishop to the specified position.
- `asText(self)`: Returns the text representation of the bishop.
- `to_svg(self, dwg: svgwrite.Drawing, x: int, y: int)`: Generates the SVG representation of the bishop.

#### Queen class (inherits from Piece)

- `get_possible_moves(self) -> List[Position]`: Returns the list of possible moves for the queen.
- `move(self, end: Position) -> None`: Moves the queen to the specified position.
- `asText(self)`: Returns the text representation of the queen.
- `to_svg(self, dwg: svgwrite.Drawing, x: int, y: int)`: Generates the SVG representation of the queen.

#### King class (inherits from Piece)

- `get_possible_moves(self) -> List[Position]`: Returns the list of possible moves for the king.
- `move(self, end: Position) -> None`: Moves the king to the specified position.
- `asText(self)`: Returns the text representation of the king.
- `to_svg(self, dwg: svgwrite.Drawing, x: int, y: int)`: Generates the SVG representation of the king.

<br>
<hr>

### main.py

This file contains the main function to run the chess game.

#### Functions:

- `clear_console()`: Clears the console.
- `print_board(game)`: Prints the chessboard.
- `main()`: Main function to run the chess game.

<br>
<hr>

## How to Run

To run the chess game, execute the `main.py` file.

```bash
python main.py
```

<br>
<hr>

## How to play
After running ```python main.py```, the following is printed on the terminal: <br>
White pieces at the top and black pieces at the bottom
<br>
<img src="readme-images/Screenshot 2024-05-03 at 17.09.42.png" width="50%">
<br><br>
After playing a move, the board is updated on the terminal:
For example, after playing the following game:
```bash
1. e2-e4   e7-e5
2. Ng1-f3  Nb8-c6
```
The following board will be displayed on the terminal:
<br>
<img src='readme-images/Screenshot 2024-05-03 at 17.16.31.png' width="50%">
<br>
And the Board SVG is updated as well:
<br>
<img src='readme-images/Group 16.png' width='70%'>
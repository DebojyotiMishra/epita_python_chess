from Chessboard import Game, Position
import os


def clear_console():
    """Clears the console."""
    os.system('cls' if os.name == 'nt' else 'clear')


def print_board(game):
    """Prints the chessboard."""
    print("  h g f e d c b a")
    for y in range(8):
        print(y + 1, end=" ")
        for x in range(8):
            piece = game.board[y][x]
            if piece:
                print(piece, end=" ")
            else:
                print(".", end=" ")
        print()


def main():
    """Main function to run the chess game."""
    game = Game()
    turn = "white"

    while True:
        clear_console()
        print_board(game)
        svg = game.to_svg()
        with open("chessboard.svg", "w") as f:
            f.write(svg)

        if game.is_check(turn):
            print(f"Check for {turn}!")
            

        if game.is_checkmate(turn):
            print(f"Checkmate! {turn} wins!")
            break

        if game.is_draw():
            print("It's a draw!")
            break

        move_input = input(f"{turn.capitalize()}'s move (e.g., e2-e4, d7-d5): ")

        try:
            start, end = game.full_chess_notation_to_position(move_input)
        except (ValueError, KeyError, IndexError, TypeError, AttributeError, NameError, SyntaxError):
            print("Invalid move. Please try again.")
            continue

        if not game.is_valid_move(start, end):
            print("Invalid move. Please try again.")
            continue
        
        piece = game.get_piece_at(start)
        if piece.color != turn:
            print("Invalid move. Please try again.")
            continue

        game.make_move(start, end)

        turn = "black" if turn == "white" else "white"


if __name__ == "__main__":
    main()

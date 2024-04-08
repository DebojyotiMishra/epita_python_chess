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
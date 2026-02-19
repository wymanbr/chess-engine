from chess_piece import ChessPiece
from player import Player
from move import Move
from typing import List

class Pawn(ChessPiece):
    """Chess pawn piece implementation."""
    
    def __init__(self, player: Player):
        """Initialize a pawn with the given player color."""
        super().__init__(player)
    
    def type(self) -> str:
        """Return the type name of this piece."""
        return "Pawn"
    
    def is_valid_move(self, move: Move, board: List[List['ChessPiece']]) -> bool:
        """Check if the move is valid for a pawn."""
        if not super().is_valid_move(move, board):
            return False

        start_row, start_col = move.from_row, move.from_col
        to_row, to_col = move.to_row, move.to_col

        if self.player == Player.WHITE:
            direction = -1  # White moves up
            starting_row = 6
        else:
            direction = 1   # Black moves down
            starting_row = 1

        row_diff = to_row - start_row
        col_diff = abs(to_col - start_col)

        if col_diff == 0 and row_diff == direction:
            return board[to_row][to_col] is None

        if (col_diff == 0 and row_diff == 2 * direction and
            start_row == starting_row):
            return (board[to_row][to_col] is None and
                    board[start_row + direction][start_col] is None)
        
        if col_diff == 1 and row_diff == direction:
            return board[to_row][to_col] is not None

        return False
from chess_piece import ChessPiece
from player import Player
from move import Move
from typing import List

class Queen(ChessPiece):
    """Chess queen piece implementation."""
    
    def __init__(self, player: Player):
        """Initialize a queen with the given player color."""
        super().__init__(player)
    
    def type(self) -> str:
        """Return the type name of this piece."""
        return "Queen"

    def is_valid_move(self, move: Move, board: List[List['ChessPiece']]) -> bool:
        """Check if the move is valid for a queen."""
        if not super().is_valid_move(move, board):
            return False

        start_row, start_col = move.from_row, move.from_col
        end_row, end_col = move.to_row, move.to_col

        row_diff = abs(end_row - start_row)
        col_diff = abs(end_col - start_col)
        
        is_straight = start_row == end_row or start_col == end_col
        is_diagonal = row_diff == col_diff
        
        if not (is_straight or is_diagonal):
            return False
        
        row_step = 0 if start_row == end_row else (1 if end_row > start_row else -1)
        col_step = 0 if start_col == end_col else (1 if end_col > start_col else -1)
        
        row, col = start_row + row_step, start_col + col_step
        while row != end_row or col != end_col:
            if board[row][col] is not None:
                return False
            row += row_step
            col += col_step
        
        return True
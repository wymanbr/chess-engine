from chess_piece import ChessPiece
from player import Player
from move import Move
from typing import List

class Bishop(ChessPiece):
    """Chess bishop piece implementation."""
    
    def __init__(self, player: Player):
        """Initialize a bishop with the given player color."""
        super().__init__(player)
    
    def type(self) -> str:
        """Return the type name of this piece."""
        return "Bishop"

    def is_valid_move(self, move: Move, board: List[List['ChessPiece']]) -> bool:
        """Check if the move is valid for a bishop."""
        if not super().is_valid_move(move, board):
            return False
        
        start_row, start_col = move.from_row, move.from_col
        end_row, end_col = move.to_row, move.to_col

        row_diff = abs(end_row - start_row)
        col_diff = abs(end_col - start_col)
        
        # Bishop moves diagonally
        if row_diff != col_diff:
            return False
        
        # Check diagonal path is clear
        row_step = 1 if end_row > start_row else -1
        col_step = 1 if end_col > start_col else -1
        
        row, col = start_row + row_step, start_col + col_step
        while row != end_row and col != end_col:
            if board[row][col] is not None:
                return False
            row += row_step
            col += col_step
        
        return True
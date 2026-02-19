from chess_piece import ChessPiece
from player import Player
from move import Move
from typing import List

class Knight(ChessPiece):
    """Chess knight piece implementation."""
    
    def __init__(self, player: Player):
        """Initialize a knight with the given player color."""
        super().__init__(player)
    
    def type(self) -> str:
        """Return the type name of this piece."""
        return "Knight"

    def is_valid_move(self, move: Move, board: List[List['ChessPiece']]) -> bool:
        """Check if the move is valid for a knight."""
        if not super().is_valid_move(move, board):
            return False
        
        start_row, start_col = move.from_row, move.from_col
        end_row, end_col = move.to_row, move.to_col

        row_diff = abs(end_row - start_row)
        col_diff = abs(end_col - start_col)
        
        return (row_diff == 2 and col_diff == 1) or (row_diff == 1 and col_diff == 2)
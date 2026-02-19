from chess_piece import ChessPiece
from player import Player
from move import Move
from typing import List

class Rook(ChessPiece):
    """Chess rook piece implementation."""
    
    def __init__(self, player: Player):
        """Initialize a rook with the given player color."""
        super().__init__(player)
    
    def type(self) -> str:
        """Return the type name of this piece."""
        return "Rook"
    
    def is_valid_move(self, move: Move, board: List[List['ChessPiece']]) -> bool:
        """Check if the move is valid for a rook."""
        if not super().is_valid_move(move, board):
            return False
        
        start_row, start_col = move.from_row, move.from_col
        end_row, end_col = move.to_row, move.to_col

        if start_row != end_row and start_col != end_col:
            return False
        
        if start_row == end_row:  # Horizontal movement
            step = 1 if end_col > start_col else -1
            for col in range(start_col + step, end_col, step):
                if board[start_row][col] is not None:
                    return False
        else:  # Vertical movement
            step = 1 if end_row > start_row else -1
            for row in range(start_row + step, end_row, step):
                if board[row][start_col] is not None:
                    return False
        
        return True
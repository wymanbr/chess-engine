from abc import ABC, abstractmethod
from typing import List
from player import Player  
from move import Move     

class ChessPiece(ABC):
    """Abstract base class for all chess pieces."""
    
    def __init__(self, player: Player):
        """Initialize chess piece with a player color."""
        self.__player = player
    
    @property
    def player(self) -> Player:
        """Get the player color of this chess piece."""
        return self.__player
    
    def __str__(self) -> str:
        """Return string representation of the chess piece."""
        return f"{self.player.name} {self.type()}"
    
    @abstractmethod
    def type(self) -> str:
        """Return the type of chess piece as a string."""
        pass
    
    def is_valid_move(self, move: Move, board: List[List['ChessPiece']]) -> bool:
        """
        Verify that a move is valid according to basic chess rules.
        
        Verifies:
        - Indices associated with move are in bounds
        - Starting and ending locations are different  
        - Self piece is located at starting location in move
        - Ending location does not contain a piece belonging to same player as self piece
        """
        # Verify indices are in bounds
        if not (0 <= move.from_row < 8 and 0 <= move.from_col < 8 and
                0 <= move.to_row < 8 and 0 <= move.to_col < 8):
            return False
        
        # Verify starting and ending locations are different
        if move.from_row == move.to_row and move.from_col == move.to_col:
            return False
        
        # Verify that self piece is located at starting location
        if board[move.from_row][move.from_col] != self:
            return False
        
        # Verify ending location doesn't contain piece of same player
        end_piece = board[move.to_row][move.to_col]
        if end_piece is not None and end_piece.player == self.player:
            return False
        
        return True
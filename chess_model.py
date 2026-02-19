from enum import Enum
from typing import List
from player import Player
from move import Move
from chess_piece import ChessPiece
from pawn import Pawn
from rook import Rook
from knight import Knight
from bishop import Bishop
from queen import Queen
from king import King

class MoveValidity(Enum):
    """Enumeration for move validity status."""
    Valid = 1
    Invalid = 2
    MovingIntoCheck = 3
    StayingInCheck = 4

    def __str__(self):
        """Return string representation of move validity."""
        if self.value == 2:
            return 'Invalid move.'

        if self.value == 3:
            return 'Invalid -- cannot move into check.'

        if self.value == 4:
            return 'Invalid -- must move out of check.'


class UndoException(Exception):
    """Exception raised when undo is called with no moves to undo."""
    pass


class ChessModel:
    """Model class for chess game logic and board state."""
    
    def __init__(self):
        """Initialize the chess model with default 8x8 board."""
        # Required instance variables
        self.board: List[List[ChessPiece]] = [[None for _ in range(8)] for _ in range(8)]
        self.__player: Player = Player.WHITE
        self.__nrows: int = 8
        self.__ncols: int = 8
        self.__message_code: MoveValidity = MoveValidity.Valid
        self.__move_history: List[tuple] = []
        
        # Set up initial chess board layout
        self._setup_initial_board()
    
    def _setup_initial_board(self):
        """Set up the initial chess board with pieces in starting positions."""
        # Set up Black pieces (row 0 and 1)
        self.board[0][0] = Rook(Player.BLACK)
        self.board[0][1] = Knight(Player.BLACK)
        self.board[0][2] = Bishop(Player.BLACK)
        self.board[0][3] = Queen(Player.BLACK)
        self.board[0][4] = King(Player.BLACK)
        self.board[0][5] = Bishop(Player.BLACK)
        self.board[0][6] = Knight(Player.BLACK)
        self.board[0][7] = Rook(Player.BLACK)
        
        # Black pawns
        for col in range(8):
            self.board[1][col] = Pawn(Player.BLACK)
        
        # Set up White pieces (row 6 and 7)
        # White pawns
        for col in range(8):
            self.board[6][col] = Pawn(Player.WHITE)
        
        self.board[7][0] = Rook(Player.WHITE)
        self.board[7][1] = Knight(Player.WHITE)
        self.board[7][2] = Bishop(Player.WHITE)
        self.board[7][3] = Queen(Player.WHITE)
        self.board[7][4] = King(Player.WHITE)
        self.board[7][5] = Bishop(Player.WHITE)
        self.board[7][6] = Knight(Player.WHITE)
        self.board[7][7] = Rook(Player.WHITE)
    
    @property
    def nrows(self) -> int:
        """Get the number of rows on the chessboard."""
        return self.__nrows
    
    @property
    def ncols(self) -> int:
        """Get the number of columns on the chessboard."""
        return self.__ncols
    
    @property
    def current_player(self) -> Player:
        """Get the current player."""
        return self.__player
    
    @property
    def message_code(self) -> MoveValidity:
        """Get the current message code indicating move validity status."""
        return self.__message_code

    def is_complete(self) -> bool:
        """
        Check if the game is complete (current player has no valid moves).
        Returns True for both checkmate and stalemate.
        """
        in_check = self.in_check(self.__player)

        for row in range(self.__nrows):
            for col in range(self.__ncols):
                piece = self.board[row][col]
                
                if piece is None or piece.player != self.__player:
                    continue
                for to_row in range(self.__nrows):
                    for to_col in range(self.__ncols):
                        move = Move(row, col, to_row, to_col)
                        if self.is_valid_move(move):
                            return False
        if in_check:
            self.__message_code = MoveValidity.StayingInCheck  # Checkmate
        else:
            self.__message_code = MoveValidity.movin  # Stalemate
        return True
        
    def is_valid_move(self, move: Move) -> bool:
        """
        Check if a move is valid at the game level.
        Sets message_code appropriately for GUI feedback.
        """
        self.__message_code = MoveValidity.Valid
        
        if not (0 <= move.from_row < self.__nrows and 0 <= move.from_col < self.__ncols and
                0 <= move.to_row < self.__nrows and 0 <= move.to_col < self.__ncols):
            self.__message_code = MoveValidity.Invalid
            return False
        
        piece = self.board[move.from_row][move.from_col]
        if piece is None:
            self.__message_code = MoveValidity.Invalid
            return False
        
        if piece.player != self.__player:
            self.__message_code = MoveValidity.Invalid
            return False
        
        if not piece.is_valid_move(move, self.board):
            self.__message_code = MoveValidity.Invalid
            return False
        
        # Check if player is in check BEFORE the move
        was_in_check_before = self.in_check(self.__player)
        
        # Make temporary move
        original_piece = self.board[move.to_row][move.to_col]
        self.board[move.to_row][move.to_col] = piece
        self.board[move.from_row][move.from_col] = None
        
        # Check if player is in check AFTER the move
        in_check_after = self.in_check(self.__player)
        
        # Undo temporary move
        self.board[move.from_row][move.from_col] = piece
        self.board[move.to_row][move.to_col] = original_piece
        
        if in_check_after:
            if was_in_check_before:
                self.__message_code = MoveValidity.StayingInCheck
            else:
                self.__message_code = MoveValidity.MovingIntoCheck
            return False
        
        self.__message_code = MoveValidity.Valid
        return True

    def move(self, move: Move):
        """Execute the given move on the board."""
        piece = self.board[move.from_row][move.from_col]
        captured_piece = self.board[move.to_row][move.to_col]
        
        # Store ORIGINAL piece that moved (before promotion)
        self.__move_history.append((move, captured_piece, piece))
        
        # Handle pawn promotion
        if isinstance(piece, Pawn):
            if piece.player == Player.WHITE and move.to_row == 0:
                piece = Queen(Player.WHITE)  # Promote to Queen
            elif piece.player == Player.BLACK and move.to_row == 7:
                piece = Queen(Player.BLACK)  # Promote to Queen
        
        self.board[move.to_row][move.to_col] = piece
        self.board[move.from_row][move.from_col] = None
        
        self.set_next_player()

    def in_check(self, p: Player) -> bool:
        """Check if the given player is currently in check."""
        king_row, king_col = None, None
        for row in range(self.__nrows):
            for col in range(self.__ncols):
                piece = self.board[row][col]
                if (piece is not None and 
                    piece.player == p and 
                    isinstance(piece, King)):
                    king_row, king_col = row, col
                    break
            if king_row is not None:
                break
        
        if king_row is None:
            return False 
        
        opponent = Player.BLACK if p == Player.WHITE else Player.WHITE
        
        for row in range(self.__nrows):
            for col in range(self.__ncols):
                piece = self.board[row][col]
                if piece is not None and piece.player == opponent:
                    attack_move = Move(row, col, king_row, king_col)
                    if piece.is_valid_move(attack_move, self.board):
                        return True
        
        return False

    def piece_at(self, row: int, col: int) -> ChessPiece:
        """Return the piece at the given board position."""
        if 0 <= row < self.__nrows and 0 <= col < self.__ncols:
            return self.board[row][col]
        return None

    def set_next_player(self):
        """Switch to the next player's turn."""
        if self.__player == Player.WHITE:
            self.__player = Player.BLACK
        else:
            self.__player = Player.WHITE

    def set_piece(self, row: int, col: int, piece: ChessPiece):
        """Set a piece at the given position with bounds and type checking."""
        if not (0 <= row < self.__nrows and 0 <= col < self.__ncols):
            raise ValueError(f"Position ({row}, {col}) is out of bounds")
        
        if piece is not None and not isinstance(piece, ChessPiece):
            raise TypeError("piece must be None or a ChessPiece instance")
        
        self.board[row][col] = piece

    def undo(self):
        """Undo the most recent move."""
        if not self.__move_history:
            raise UndoException("No moves to undo")
        
        last_move, captured_piece, original_piece = self.__move_history.pop()
        
        self.board[last_move.from_row][last_move.from_col] = original_piece
        self.board[last_move.to_row][last_move.to_col] = captured_piece
        
        self.set_next_player()
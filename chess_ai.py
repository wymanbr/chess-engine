import random
from typing import List, Optional
from chess_model import ChessModel
from move import Move
from player import Player
from chess_piece import ChessPiece
from king import King
from pawn import Pawn

class ChessAI:
    """Simple AI for chess game following priority-based decision making."""
    
    def __init__(self, player: Player, difficulty: str = "easy"):
        """Initialize AI with player color and difficulty level."""
        self.player = player
        self.difficulty = difficulty
    
    def get_best_move(self, model: ChessModel) -> Optional[Move]:
        """Get the best move for the AI player following priority rules."""
        if model.current_player != self.player:
            return None
        
        # Get all possible legal moves
        all_moves = self._get_all_possible_moves(model)
        if not all_moves:
            return None
        
        # Priority 1: Get out of check if in check
        if model.in_check(self.player):
            escape_moves = self._get_escape_check_moves(model, all_moves)
            if escape_moves:
                return random.choice(escape_moves)
        
        # Priority 2: Checkmate opponent if possible
        checkmate_moves = self._get_checkmate_moves(model, all_moves)
        if checkmate_moves:
            return checkmate_moves[0]
        
        # Priority 3: Put opponent in check (safely)
        safe_check_moves = self._get_safe_check_moves(model, all_moves)
        if safe_check_moves:
            return random.choice(safe_check_moves)
        
        # Priority 4: Capture opponent pieces (safely)
        safe_capture_moves = self._get_safe_capture_moves(model, all_moves)
        if safe_capture_moves:
            return random.choice(safe_capture_moves)
        
        # Priority 5: Protect pieces in danger
        protection_moves = self._get_protection_moves(model, all_moves)
        if protection_moves:
            return random.choice(protection_moves)
        
        # Priority 6: Move pawns forward (safely)
        safe_pawn_moves = self._get_safe_pawn_advances(model, all_moves)
        if safe_pawn_moves:
            return random.choice(safe_pawn_moves)
        
        # Priority 7: Any safe move
        safe_moves = self._get_safe_moves(model, all_moves)
        if safe_moves:
            return random.choice(safe_moves)
        
        # Fallback: Random legal move
        return random.choice(all_moves)
    
    def _get_all_possible_moves(self, model: ChessModel) -> List[Move]:
        """Get all possible legal moves for the AI player."""
        moves = []
        for row in range(8):
            for col in range(8):
                piece = model.piece_at(row, col)
                if piece and piece.player == self.player:
                    for to_row in range(8):
                        for to_col in range(8):
                            if row == to_row and col == to_col:
                                continue
                            move = Move(row, col, to_row, to_col)
                            if model.is_valid_move(move):
                                moves.append(move)
        return moves
    
    def _get_escape_check_moves(self, model: ChessModel, moves: List[Move]) -> List[Move]:
        """Get moves that get the king out of check."""
        escape_moves = []
        for move in moves:
            # Simulate move
            captured = model.piece_at(move.to_row, move.to_col)
            piece = model.piece_at(move.from_row, move.from_col)
            
            # Make temporary move
            model.board[move.to_row][move.to_col] = piece
            model.board[move.from_row][move.from_col] = None
            
            # Check if still in check
            still_in_check = model.in_check(self.player)
            
            # Undo move
            model.board[move.from_row][move.from_col] = piece
            model.board[move.to_row][move.to_col] = captured
            
            if not still_in_check:
                escape_moves.append(move)
        
        return escape_moves
    
    def _get_checkmate_moves(self, model: ChessModel, moves: List[Move]) -> List[Move]:
        """Get moves that put opponent in checkmate."""
        opponent = Player.BLACK if self.player == Player.WHITE else Player.WHITE
        checkmate_moves = []
        
        for move in moves:
            # Simulate move
            captured = model.piece_at(move.to_row, move.to_col)
            piece = model.piece_at(move.from_row, move.from_col)
            
            # Make temporary move
            model.board[move.to_row][move.to_col] = piece
            model.board[move.from_row][move.from_col] = None
            
            # Temporarily switch to opponent to check their moves
            original_player = model._ChessModel__player
            model._ChessModel__player = opponent
            
            # Check if opponent is in checkmate
            if model.in_check(opponent) and model.is_completed():
                checkmate_moves.append(move)
            
            # Restore board and player
            model.board[move.from_row][move.from_col] = piece
            model.board[move.to_row][move.to_col] = captured
            model._ChessModel__player = original_player
        
        return checkmate_moves
    
    def _get_safe_check_moves(self, model: ChessModel, moves: List[Move]) -> List[Move]:
        """Get moves that put opponent in check without losing the piece."""
        opponent = Player.BLACK if self.player == Player.WHITE else Player.WHITE
        safe_check_moves = []
        
        for move in moves:
            # Simulate move
            captured = model.piece_at(move.to_row, move.to_col)
            piece = model.piece_at(move.from_row, move.from_col)
            
            # Make temporary move
            model.board[move.to_row][move.to_col] = piece
            model.board[move.from_row][move.from_col] = None
            
            # Check if opponent is in check and our piece is safe
            opponent_in_check = model.in_check(opponent)
            piece_safe = not self._is_piece_in_danger(model, move.to_row, move.to_col)
            
            # Undo move
            model.board[move.from_row][move.from_col] = piece
            model.board[move.to_row][move.to_col] = captured
            
            if opponent_in_check and piece_safe:
                safe_check_moves.append(move)
        
        return safe_check_moves
    
    def _get_safe_capture_moves(self, model: ChessModel, moves: List[Move]) -> List[Move]:
        """Get moves that capture opponent pieces safely."""
        capture_moves = []
        
        for move in moves:
            target = model.piece_at(move.to_row, move.to_col)
            if target and target.player != self.player:
                # Check if the capturing piece will be safe
                piece = model.piece_at(move.from_row, move.from_col)
                
                # Make temporary move
                model.board[move.to_row][move.to_col] = piece
                model.board[move.from_row][move.from_col] = None
                
                piece_safe = not self._is_piece_in_danger(model, move.to_row, move.to_col)
                
                # Undo move
                model.board[move.from_row][move.from_col] = piece
                model.board[move.to_row][move.to_col] = target
                
                if piece_safe:
                    capture_moves.append(move)
        
        return capture_moves
    
    def _get_protection_moves(self, model: ChessModel, moves: List[Move]) -> List[Move]:
        """Get moves that protect pieces in danger."""
        protection_moves = []
        
        # Find pieces in danger
        endangered_pieces = []
        for row in range(8):
            for col in range(8):
                piece = model.piece_at(row, col)
                if piece and piece.player == self.player:
                    if self._is_piece_in_danger(model, row, col):
                        endangered_pieces.append((row, col))
        
        if not endangered_pieces:
            return []
        
        # Find moves that protect endangered pieces
        for move in moves:
            piece = model.piece_at(move.from_row, move.from_col)
            captured = model.piece_at(move.to_row, move.to_col)
            
            # Make temporary move
            model.board[move.to_row][move.to_col] = piece
            model.board[move.from_row][move.from_col] = None
            
            # Check if any endangered piece is now safe
            protection_provided = False
            for e_row, e_col in endangered_pieces:
                if not self._is_piece_in_danger(model, e_row, e_col):
                    protection_provided = True
                    break
            
            # Undo move
            model.board[move.from_row][move.from_col] = piece
            model.board[move.to_row][move.to_col] = captured
            
            if protection_provided:
                protection_moves.append(move)
        
        return protection_moves
    
    def _get_safe_pawn_advances(self, model: ChessModel, moves: List[Move]) -> List[Move]:
        """Get safe pawn advancement moves."""
        pawn_moves = []
        
        for move in moves:
            piece = model.piece_at(move.from_row, move.from_col)
            if isinstance(piece, Pawn):
                # Check if pawn will be safe after moving
                captured = model.piece_at(move.to_row, move.to_col)
                
                # Make temporary move
                model.board[move.to_row][move.to_col] = piece
                model.board[move.from_row][move.from_col] = None
                
                piece_safe = not self._is_piece_in_danger(model, move.to_row, move.to_col)
                
                # Undo move
                model.board[move.from_row][move.from_col] = piece
                model.board[move.to_row][move.to_col] = captured
                
                if piece_safe:
                    pawn_moves.append(move)
        
        return pawn_moves
    
    def _get_safe_moves(self, model: ChessModel, moves: List[Move]) -> List[Move]:
        """Get moves where the piece will be safe after moving."""
        safe_moves = []
        
        for move in moves:
            captured = model.piece_at(move.to_row, move.to_col)
            piece = model.piece_at(move.from_row, move.from_col)
            
            # Make temporary move
            model.board[move.to_row][move.to_col] = piece
            model.board[move.from_row][move.from_col] = None
            
            piece_safe = not self._is_piece_in_danger(model, move.to_row, move.to_col)
            
            # Undo move
            model.board[move.from_row][move.from_col] = piece
            model.board[move.to_row][move.to_col] = captured
            
            if piece_safe:
                safe_moves.append(move)
        
        return safe_moves
    
    def _is_piece_in_danger(self, model: ChessModel, row: int, col: int) -> bool:
        """Check if a piece at given position is in danger of being captured."""
        piece = model.piece_at(row, col)
        if not piece:
            return False
        
        opponent = Player.BLACK if piece.player == Player.WHITE else Player.WHITE
        
        # Check if any opponent piece can attack this position
        for r in range(8):
            for c in range(8):
                enemy = model.piece_at(r, c)
                if enemy and enemy.player == opponent:
                    attack_move = Move(r, c, row, col)
                    if enemy.is_valid_move(attack_move, model.board):
                        return True
        
        return False
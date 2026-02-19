import unittest
from chess_model import ChessModel, MoveValidity, UndoException
from chess_piece import ChessPiece
from pawn import Pawn
from rook import Rook
from knight import Knight
from bishop import Bishop
from queen import Queen
from king import King
from move import Move
from player import Player


class TestChessModel(unittest.TestCase):
    """Test ChessModel class functionality."""
    
    def setUp(self):
        """Set up a fresh chess model for each test."""
        self.model = ChessModel()
    
    def test_initial_board_setup(self):
        """Test that the initial board is set up correctly."""
        # Test Black pieces setup (row 0)
        self.assertIsInstance(self.model.piece_at(0, 0), Rook)
        self.assertEqual(self.model.piece_at(0, 0).player, Player.BLACK)
        self.assertIsInstance(self.model.piece_at(0, 1), Knight)
        self.assertIsInstance(self.model.piece_at(0, 2), Bishop)
        self.assertIsInstance(self.model.piece_at(0, 3), Queen)
        self.assertIsInstance(self.model.piece_at(0, 4), King)
        self.assertIsInstance(self.model.piece_at(0, 5), Bishop)
        self.assertIsInstance(self.model.piece_at(0, 6), Knight)
        self.assertIsInstance(self.model.piece_at(0, 7), Rook)
        
        # Test Black pawns (row 1)
        for col in range(8):
            self.assertIsInstance(self.model.piece_at(1, col), Pawn)
            self.assertEqual(self.model.piece_at(1, col).player, Player.BLACK)
        
        # Test empty squares (rows 2-5)
        for row in range(2, 6):
            for col in range(8):
                self.assertIsNone(self.model.piece_at(row, col))
        
        # Test White pawns (row 6)
        for col in range(8):
            self.assertIsInstance(self.model.piece_at(6, col), Pawn)
            self.assertEqual(self.model.piece_at(6, col).player, Player.WHITE)
        
        # Test White pieces setup (row 7)
        self.assertIsInstance(self.model.piece_at(7, 0), Rook)
        self.assertEqual(self.model.piece_at(7, 0).player, Player.WHITE)
        self.assertIsInstance(self.model.piece_at(7, 1), Knight)
        self.assertIsInstance(self.model.piece_at(7, 2), Bishop)
        self.assertIsInstance(self.model.piece_at(7, 3), Queen)
        self.assertIsInstance(self.model.piece_at(7, 4), King)
        self.assertIsInstance(self.model.piece_at(7, 5), Bishop)
        self.assertIsInstance(self.model.piece_at(7, 6), Knight)
        self.assertIsInstance(self.model.piece_at(7, 7), Rook)
    
    def test_initial_state(self):
        """Test initial game state."""
        self.assertEqual(self.model.current_player, Player.WHITE)
        self.assertEqual(self.model.nrows, 8)
        self.assertEqual(self.model.ncols, 8)
        self.assertEqual(self.model.message_code, MoveValidity.Valid)
        self.assertFalse(self.model.is_complete())
    
    def test_piece_at_bounds(self):
        """Test piece_at with out of bounds coordinates."""
        self.assertIsNone(self.model.piece_at(-1, 0))
        self.assertIsNone(self.model.piece_at(0, -1))
        self.assertIsNone(self.model.piece_at(8, 0))
        self.assertIsNone(self.model.piece_at(0, 8))
        self.assertIsNone(self.model.piece_at(10, 10))
    
    def test_set_piece_valid(self):
        """Test setting pieces on valid positions."""
        new_pawn = Pawn(Player.WHITE)
        self.model.set_piece(3, 3, new_pawn)
        self.assertEqual(self.model.piece_at(3, 3), new_pawn)
        
        # Test setting None (removing piece)
        self.model.set_piece(3, 3, None)
        self.assertIsNone(self.model.piece_at(3, 3))
    
    def test_set_piece_invalid_bounds(self):
        """Test setting pieces on invalid positions."""
        new_pawn = Pawn(Player.WHITE)
        with self.assertRaises(ValueError):
            self.model.set_piece(-1, 0, new_pawn)
        with self.assertRaises(ValueError):
            self.model.set_piece(0, -1, new_pawn)
        with self.assertRaises(ValueError):
            self.model.set_piece(8, 0, new_pawn)
        with self.assertRaises(ValueError):
            self.model.set_piece(0, 8, new_pawn)
    
    def test_set_piece_invalid_type(self):
        """Test setting invalid piece types."""
        with self.assertRaises(TypeError):
            self.model.set_piece(0, 0, "not a piece")
        with self.assertRaises(TypeError):
            self.model.set_piece(0, 0, 123)
    
    def test_set_next_player(self):
        """Test player switching."""
        self.assertEqual(self.model.current_player, Player.WHITE)
        self.model.set_next_player()
        self.assertEqual(self.model.current_player, Player.BLACK)
        self.model.set_next_player()
        self.assertEqual(self.model.current_player, Player.WHITE)
    
    def test_valid_pawn_moves(self):
        """Test valid pawn moves."""
        # White pawn single move
        move = Move(6, 4, 5, 4)
        self.assertTrue(self.model.is_valid_move(move))
        
        # White pawn double move from starting position
        move = Move(6, 4, 4, 4)
        self.assertTrue(self.model.is_valid_move(move))
    
    def test_invalid_moves_out_of_bounds(self):
        """Test moves with out of bounds coordinates."""
        move = Move(-1, 0, 0, 0)
        self.assertFalse(self.model.is_valid_move(move))
        self.assertEqual(self.model.message_code, MoveValidity.Invalid)
        
        move = Move(0, 0, 8, 0)
        self.assertFalse(self.model.is_valid_move(move))
        self.assertEqual(self.model.message_code, MoveValidity.Invalid)
    
    def test_invalid_moves_no_piece(self):
        """Test moves from empty squares."""
        move = Move(3, 3, 4, 4)  # Empty square
        self.assertFalse(self.model.is_valid_move(move))
        self.assertEqual(self.model.message_code, MoveValidity.Invalid)
    
    def test_invalid_moves_wrong_player(self):
        """Test moves with wrong player's pieces."""
        # Try to move black piece when it's white's turn
        move = Move(1, 0, 2, 0)  # Black pawn
        self.assertFalse(self.model.is_valid_move(move))
        self.assertEqual(self.model.message_code, MoveValidity.Invalid)
    
    def test_move_execution(self):
        """Test move execution and player switching."""
        move = Move(6, 4, 4, 4)  # White pawn double move
        self.assertTrue(self.model.is_valid_move(move))
        
        self.model.move(move)
        self.assertIsNone(self.model.piece_at(6, 4))
        self.assertIsInstance(self.model.piece_at(4, 4), Pawn)
        self.assertEqual(self.model.current_player, Player.BLACK)
    
    def test_pawn_promotion(self):
        """Test pawn promotion to queen."""
        # Set up a white pawn about to promote
        self.model.set_piece(1, 0, Pawn(Player.WHITE))
        self.model.set_piece(0, 0, None)  # Remove black rook
        
        move = Move(1, 0, 0, 0)
        self.model.move(move)
        
        promoted_piece = self.model.piece_at(0, 0)
        self.assertIsInstance(promoted_piece, Queen)
        self.assertEqual(promoted_piece.player, Player.WHITE)
    
    def test_capture_move(self):
        """Test capturing opponent pieces."""
        # Move white pawn forward
        self.model.move(Move(6, 4, 4, 4))
        # Move black pawn forward
        self.model.move(Move(1, 3, 3, 3))
        # White pawn captures black pawn
        move = Move(4, 4, 3, 3)
        self.assertTrue(self.model.is_valid_move(move))
        
        self.model.move(move)
        captured_piece = self.model.piece_at(3, 3)
        self.assertIsInstance(captured_piece, Pawn)
        self.assertEqual(captured_piece.player, Player.WHITE)
    
    def test_in_check_detection(self):
        """Test check detection."""
        # Set up a simple check scenario
        self.model.set_piece(4, 4, King(Player.WHITE))
        self.model.set_piece(4, 0, Rook(Player.BLACK))
        
        self.assertTrue(self.model.in_check(Player.WHITE))
        self.assertFalse(self.model.in_check(Player.BLACK))
    
    def test_cannot_move_into_check(self):
        """Test that moves into check are invalid."""
        # Set up scenario where king would move into check
        self.model.set_piece(4, 4, King(Player.WHITE))
        self.model.set_piece(3, 0, Rook(Player.BLACK))
        self.model._ChessModel__player = Player.WHITE
        
        move = Move(4, 4, 3, 4)  # King moves into rook's line of attack
        self.assertFalse(self.model.is_valid_move(move))
        self.assertEqual(self.model.message_code, MoveValidity.MovingIntoCheck)
    
    def test_must_move_out_of_check(self):
        """Test that moves that leave king in check are invalid."""
        # Set up scenario where king is in check
        self.model.set_piece(4, 4, King(Player.WHITE))
        self.model.set_piece(4, 0, Rook(Player.BLACK))
        self.model.set_piece(3, 4, Pawn(Player.WHITE))
        self.model._ChessModel__player = Player.WHITE
        
        # Try to move pawn (doesn't resolve check)
        move = Move(3, 4, 2, 4)
        self.assertFalse(self.model.is_valid_move(move))
        self.assertEqual(self.model.message_code, MoveValidity.StayingInCheck)
    
    def test_undo_functionality(self):
        """Test undo moves."""
        original_piece = self.model.piece_at(6, 4)
        move = Move(6, 4, 4, 4)
        self.model.move(move)
        
        # Verify move was made
        self.assertIsNone(self.model.piece_at(6, 4))
        self.assertIsInstance(self.model.piece_at(4, 4), Pawn)
        self.assertEqual(self.model.current_player, Player.BLACK)
        
        # Undo move
        self.model.undo()
        self.assertEqual(self.model.piece_at(6, 4), original_piece)
        self.assertIsNone(self.model.piece_at(4, 4))
        self.assertEqual(self.model.current_player, Player.WHITE)
    
    def test_undo_capture(self):
        """Test undo of capture moves."""
        # Set up capture scenario
        self.model.set_piece(4, 4, Pawn(Player.WHITE))
        self.model.set_piece(3, 3, Pawn(Player.BLACK))
        self.model._ChessModel__player = Player.WHITE
        
        captured_piece = self.model.piece_at(3, 3)
        move = Move(4, 4, 3, 3)
        self.model.move(move)
        
        # Undo capture
        self.model.undo()
        
        # Verify original state restored
        self.assertIsInstance(self.model.piece_at(4, 4), Pawn)
        self.assertEqual(self.model.piece_at(4, 4).player, Player.WHITE)
        self.assertEqual(self.model.piece_at(3, 3), captured_piece)
    
    def test_undo_exception(self):
        """Test undo exception when no moves to undo."""
        with self.assertRaises(UndoException):
            self.model.undo()
    
    def test_multiple_undo(self):
        """Test multiple undo operations."""
        # Make two moves
        self.model.move(Move(6, 4, 4, 4))  # White pawn
        self.model.move(Move(1, 4, 3, 4))  # Black pawn
        
        # Undo both moves
        self.model.undo()  # Undo black move
        self.assertEqual(self.model.current_player, Player.BLACK)
        self.assertIsInstance(self.model.piece_at(1, 4), Pawn)
        
        self.model.undo()  # Undo white move
        self.assertEqual(self.model.current_player, Player.WHITE)
        self.assertIsInstance(self.model.piece_at(6, 4), Pawn)


class TestChessPieces(unittest.TestCase):
    """Test individual chess piece behavior."""
    
    def setUp(self):
        """Set up empty board for piece testing."""
        self.board = [[None for _ in range(8)] for _ in range(8)]
    
    def test_pawn_basic_move(self):
        """Test basic pawn moves."""
        white_pawn = Pawn(Player.WHITE)
        self.board[6][4] = white_pawn
        
        # Single move forward
        move = Move(6, 4, 5, 4)
        self.assertTrue(white_pawn.is_valid_move(move, self.board))
        
        # Double move from starting position
        move = Move(6, 4, 4, 4)
        self.assertTrue(white_pawn.is_valid_move(move, self.board))
        
        # Invalid backward move
        move = Move(6, 4, 7, 4)
        self.assertFalse(white_pawn.is_valid_move(move, self.board))
    
    def test_pawn_capture(self):
        """Test pawn capture moves."""
        white_pawn = Pawn(Player.WHITE)
        black_pawn = Pawn(Player.BLACK)
        self.board[6][4] = white_pawn
        self.board[5][3] = black_pawn
        
        # Valid diagonal capture
        move = Move(6, 4, 5, 3)
        self.assertTrue(white_pawn.is_valid_move(move, self.board))
        
        # Invalid diagonal move without capture
        move = Move(6, 4, 5, 5)
        self.assertFalse(white_pawn.is_valid_move(move, self.board))
    
    def test_pawn_blocked(self):
        """Test pawn blocked by other pieces."""
        white_pawn = Pawn(Player.WHITE)
        black_pawn = Pawn(Player.BLACK)
        self.board[6][4] = white_pawn
        self.board[5][4] = black_pawn  # Blocking piece
        
        # Single move blocked
        move = Move(6, 4, 5, 4)
        self.assertFalse(white_pawn.is_valid_move(move, self.board))
        
        # Double move blocked
        move = Move(6, 4, 4, 4)
        self.assertFalse(white_pawn.is_valid_move(move, self.board))
    
    def test_rook_movement(self):
        """Test rook movement patterns."""
        rook = Rook(Player.WHITE)
        self.board[4][4] = rook
        
        # Valid horizontal moves
        self.assertTrue(rook.is_valid_move(Move(4, 4, 4, 7), self.board))
        self.assertTrue(rook.is_valid_move(Move(4, 4, 4, 0), self.board))
        
        # Valid vertical moves
        self.assertTrue(rook.is_valid_move(Move(4, 4, 0, 4), self.board))
        self.assertTrue(rook.is_valid_move(Move(4, 4, 7, 4), self.board))
        
        # Invalid diagonal move
        self.assertFalse(rook.is_valid_move(Move(4, 4, 6, 6), self.board))
    
    def test_rook_blocked(self):
        """Test rook movement blocked by pieces."""
        rook = Rook(Player.WHITE)
        blocking_piece = Pawn(Player.BLACK)
        self.board[4][4] = rook
        self.board[4][6] = blocking_piece
        
        # Move to blocking piece (capture) - valid
        self.assertTrue(rook.is_valid_move(Move(4, 4, 4, 6), self.board))
        
        # Move past blocking piece - invalid
        self.assertFalse(rook.is_valid_move(Move(4, 4, 4, 7), self.board))
    
    def test_bishop_movement(self):
        """Test bishop movement patterns."""
        bishop = Bishop(Player.WHITE)
        self.board[4][4] = bishop
        
        # Valid diagonal moves
        self.assertTrue(bishop.is_valid_move(Move(4, 4, 6, 6), self.board))
        self.assertTrue(bishop.is_valid_move(Move(4, 4, 2, 2), self.board))
        self.assertTrue(bishop.is_valid_move(Move(4, 4, 6, 2), self.board))
        self.assertTrue(bishop.is_valid_move(Move(4, 4, 2, 6), self.board))
        
        # Invalid straight moves
        self.assertFalse(bishop.is_valid_move(Move(4, 4, 4, 7), self.board))
        self.assertFalse(bishop.is_valid_move(Move(4, 4, 7, 4), self.board))
    
    def test_knight_movement(self):
        """Test knight movement patterns."""
        knight = Knight(Player.WHITE)
        self.board[4][4] = knight
        
        # Valid L-shaped moves
        valid_moves = [
            (2, 3), (2, 5), (3, 2), (3, 6),
            (5, 2), (5, 6), (6, 3), (6, 5)
        ]
        
        for to_row, to_col in valid_moves:
            self.assertTrue(knight.is_valid_move(Move(4, 4, to_row, to_col), self.board))
        
        # Invalid moves
        invalid_moves = [(4, 5), (5, 5), (3, 3), (4, 6)]
        for to_row, to_col in invalid_moves:
            self.assertFalse(knight.is_valid_move(Move(4, 4, to_row, to_col), self.board))
    
    def test_queen_movement(self):
        """Test queen movement patterns."""
        queen = Queen(Player.WHITE)
        self.board[4][4] = queen
        
        # Valid moves (combination of rook and bishop)
        valid_moves = [
            (4, 7),  # Horizontal
            (7, 4),  # Vertical
            (6, 6),  # Diagonal
            (2, 2),  # Diagonal
        ]
        
        for to_row, to_col in valid_moves:
            self.assertTrue(queen.is_valid_move(Move(4, 4, to_row, to_col), self.board))
        
        # Invalid knight-like move
        self.assertFalse(queen.is_valid_move(Move(4, 4, 6, 5), self.board))
    
    def test_king_movement(self):
        """Test king movement patterns."""
        king = King(Player.WHITE)
        self.board[4][4] = king
        
        # Valid one-square moves in all directions
        valid_moves = [
            (3, 3), (3, 4), (3, 5),
            (4, 3),         (4, 5),
            (5, 3), (5, 4), (5, 5)
        ]
        
        for to_row, to_col in valid_moves:
            self.assertTrue(king.is_valid_move(Move(4, 4, to_row, to_col), self.board))
        
        # Invalid multi-square moves
        invalid_moves = [(4, 6), (6, 4), (6, 6), (2, 2)]
        for to_row, to_col in invalid_moves:
            self.assertFalse(king.is_valid_move(Move(4, 4, to_row, to_col), self.board))
    
    def test_piece_cannot_capture_same_color(self):
        """Test that pieces cannot capture same color pieces."""
        white_pawn1 = Pawn(Player.WHITE)
        white_pawn2 = Pawn(Player.WHITE)
        self.board[4][4] = white_pawn1
        self.board[3][4] = white_pawn2
        
        # Cannot move to square occupied by same color
        self.assertFalse(white_pawn1.is_valid_move(Move(4, 4, 3, 4), self.board))
    
    def test_piece_string_representation(self):
        """Test string representation of pieces."""
        white_pawn = Pawn(Player.WHITE)
        black_king = King(Player.BLACK)
        
        self.assertEqual(str(white_pawn), "WHITE Pawn")
        self.assertEqual(str(black_king), "BLACK King")
    
    def test_piece_type_methods(self):
        """Test piece type method returns."""
        pieces = [
            (Pawn(Player.WHITE), "Pawn"),
            (Rook(Player.WHITE), "Rook"),
            (Knight(Player.WHITE), "Knight"),
            (Bishop(Player.WHITE), "Bishop"),
            (Queen(Player.WHITE), "Queen"),
            (King(Player.WHITE), "King"),
        ]
        
        for piece, expected_type in pieces:
            self.assertEqual(piece.type(), expected_type)


class TestMove(unittest.TestCase):
    """Test Move class."""
    
    def test_move_creation(self):
        """Test move object creation."""
        move = Move(1, 2, 3, 4)
        self.assertEqual(move.from_row, 1)
        self.assertEqual(move.from_col, 2)
        self.assertEqual(move.to_row, 3)
        self.assertEqual(move.to_col, 4)
    
    def test_move_string_representation(self):
        """Test move string representation."""
        move = Move(1, 2, 3, 4)
        expected = "Move [from_row=1, from_col=2, to_row=3, to_col=4]"
        self.assertEqual(str(move), expected)


class TestPlayer(unittest.TestCase):
    """Test Player enum."""
    
    def test_player_values(self):
        """Test player enum values."""
        self.assertEqual(Player.BLACK.value, 0)
        self.assertEqual(Player.WHITE.value, 1)
    
    def test_player_next(self):
        """Test player switching."""
        self.assertEqual(Player.WHITE.next(), Player.BLACK)
        self.assertEqual(Player.BLACK.next(), Player.WHITE)


class TestMoveValidity(unittest.TestCase):
    """Test MoveValidity enum."""
    
    def test_move_validity_string(self):
        """Test MoveValidity string representations."""
        self.assertEqual(str(MoveValidity.Invalid), "Invalid move.")
        self.assertEqual(str(MoveValidity.MovingIntoCheck), "Invalid -- cannot move into check.")
        self.assertEqual(str(MoveValidity.StayingInCheck), "Invalid -- must move out of check.")


class TestComplexScenarios(unittest.TestCase):
    """Test complex game scenarios."""
    
    def setUp(self):
        """Set up chess model for complex tests."""
        self.model = ChessModel()
    
    def test_pawn_promotion_scenario(self):
        """Test complete pawn promotion scenario."""
        # Clear the board and set up promotion scenario
        for row in range(8):
            for col in range(8):
                self.model.set_piece(row, col, None)
        
        # Place white pawn on 2nd rank, about to promote
        self.model.set_piece(1, 0, Pawn(Player.WHITE))
        self.model._ChessModel__player = Player.WHITE
        
        # Promote pawn
        move = Move(1, 0, 0, 0)
        self.model.move(move)
        
        # Check promotion occurred
        promoted_piece = self.model.piece_at(0, 0)
        self.assertIsInstance(promoted_piece, Queen)
        self.assertEqual(promoted_piece.player, Player.WHITE)
    
    def test_stalemate_scenario(self):
        """Test stalemate detection."""
        # Clear board and set up stalemate position
        for row in range(8):
            for col in range(8):
                self.model.set_piece(row, col, None)
        
        # Place kings in stalemate position
        self.model.set_piece(0, 0, King(Player.BLACK))
        self.model.set_piece(2, 1, King(Player.WHITE))
        self.model.set_piece(1, 2, Queen(Player.WHITE))
        self.model._ChessModel__player = Player.BLACK
        
        # Black king has no legal moves but is not in check
        self.assertFalse(self.model.in_check(Player.BLACK))
        self.assertTrue(self.model.is_complete())  # Should be stalemate
    
    def test_pin_scenario(self):
        """Test that pieces cannot move when it would leave king in check."""
        # Set up scenario where moving a piece exposes king to check
        for row in range(8):
            for col in range(8):
                self.model.set_piece(row, col, None)
        
        self.model.set_piece(4, 4, King(Player.WHITE))
        self.model.set_piece(4, 3, Bishop(Player.WHITE))  # Protecting king
        self.model.set_piece(4, 0, Rook(Player.BLACK))   # Attacking along rank
        self.model._ChessModel__player = Player.WHITE
        
        # Bishop cannot move as it would expose king
        move = Move(4, 3, 5, 4)
        self.assertFalse(self.model.is_valid_move(move))


if __name__ == '__main__':
    unittest.main()
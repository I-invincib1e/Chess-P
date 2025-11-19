import chess
import math

import json
import os

# Default weights if file not found
DEFAULT_WEIGHTS = {
    "PAWN": 100,
    "KNIGHT": 320,
    "BISHOP": 330,
    "ROOK": 500,
    "QUEEN": 900,
    "KING": 20000,
    "DRAW_PENALTY": 0
}

CURRENT_WEIGHTS = DEFAULT_WEIGHTS.copy()

# Piece-Square Tables (Restored)
PAWN_TABLE = [
    0,  0,  0,  0,  0,  0,  0,  0,
    50, 50, 50, 50, 50, 50, 50, 50,
    10, 10, 20, 30, 30, 20, 10, 10,
    5,  5, 10, 25, 25, 10,  5,  5,
    0,  0,  0, 20, 20,  0,  0,  0,
    5, -5,-10,  0,  0,-10, -5,  5,
    5, 10, 10,-20,-20, 10, 10,  5,
    0,  0,  0,  0,  0,  0,  0,  0
]

KNIGHT_TABLE = [
    -50,-40,-30,-30,-30,-30,-40,-50,
    -40,-20,  0,  0,  0,  0,-20,-40,
    -30,  0, 10, 15, 15, 10,  0,-30,
    -30,  5, 15, 20, 20, 15,  5,-30,
    -30,  0, 15, 20, 20, 15,  0,-30,
    -30,  5, 10, 15, 15, 10,  5,-30,
    -40,-20,  0,  5,  5,  0,-20,-40,
    -50,-40,-30,-30,-30,-30,-40,-50,
]

BISHOP_TABLE = [
    -20,-10,-10,-10,-10,-10,-10,-20,
    -10,  0,  0,  0,  0,  0,  0,-10,
    -10,  0,  5, 10, 10,  5,  0,-10,
    -10,  5,  5, 10, 10,  5,  5,-10,
    -10,  0, 10, 10, 10, 10,  0,-10,
    -10, 10, 10, 10, 10, 10, 10,-10,
    -10,  5,  0,  0,  0,  0,  5,-10,
    -20,-10,-10,-10,-10,-10,-10,-20,
]

ROOK_TABLE = [
    0,  0,  0,  0,  0,  0,  0,  0,
    5, 10, 10, 10, 10, 10, 10,  5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    0,  0,  0,  5,  5,  0,  0,  0
]

QUEEN_TABLE = [
    -20,-10,-10, -5, -5,-10,-10,-20,
    -10,  0,  0,  0,  0,  0,  0,-10,
    -10,  0,  5,  5,  5,  5,  0,-10,
    -5,  0,  5,  5,  5,  5,  0, -5,
    0,  0,  5,  5,  5,  5,  0, -5,
    -10,  5,  5,  5,  5,  5,  0,-10,
    -10,  0,  5,  0,  0,  0,  0,-10,
    -20,-10,-10, -5, -5,-10,-10,-20
]

KING_TABLE_MID = [
    -30,-40,-40,-50,-50,-40,-40,-30,
    -30,-40,-40,-50,-50,-40,-40,-30,
    -30,-40,-40,-50,-50,-40,-40,-30,
    -30,-40,-40,-50,-50,-40,-40,-30,
    -20,-30,-30,-40,-40,-30,-30,-20,
    -10,-20,-20,-20,-20,-20,-20,-10,
    20, 20,  0,  0,  0,  0, 20, 20,
    20, 30, 10,  0,  0, 10, 30, 20
]

KING_TABLE_END = [
    -50,-40,-30,-20,-20,-30,-40,-50,
    -30,-20,-10,  0,  0,-10,-20,-30,
    -30,-10, 20, 30, 30, 20,-10,-30,
    -30,-10, 30, 40, 40, 30,-10,-30,
    -30,-10, 30, 40, 40, 30,-10,-30,
    -30,-10, 20, 30, 30, 20,-10,-30,
    -30,-30,  0,  0,  0,  0,-30,-30,
    -50,-30,-30,-30,-30,-30,-30,-50
]

def load_weights(file_path="model.json"):
    global CURRENT_WEIGHTS
    try:
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                data = json.load(f)
                CURRENT_WEIGHTS = data.get("weights", DEFAULT_WEIGHTS)
                print(f"Loaded weights from {file_path} (Rating: {data.get('rating', 1000)})")
        else:
            print(f"Weight file {file_path} not found. Using defaults.")
            CURRENT_WEIGHTS = DEFAULT_WEIGHTS.copy()
    except Exception as e:
        print(f"Error loading weights: {e}")

import src.openings as openings

# Transposition Table
# Key: FEN string (or hash)
# Value: {'score': score, 'depth': depth, 'flag': 'exact'|'lower'|'upper'}
TRANSPOSITION_TABLE = {}

def evaluate_board(board, weights=None):
    if weights is None:
        weights = CURRENT_WEIGHTS

    if board.is_checkmate():
        if board.turn:
            return -99999 # Black wins (White is checkmated)
        else:
            return 99999 # White wins

    # Draw awareness
    if board.is_stalemate() or board.is_insufficient_material() or board.is_fivefold_repetition() or board.is_seventyfive_moves():
        return weights.get("DRAW_PENALTY", 0)
    
    # Can claim draw? (3-fold or 50-move)
    if board.can_claim_draw():
        return weights.get("DRAW_PENALTY", 0)

    score = 0
    
    # Determine game phase (simple heuristic based on queen count)
    white_queens = len(board.pieces(chess.QUEEN, chess.WHITE))
    black_queens = len(board.pieces(chess.QUEEN, chess.BLACK))
    minor_pieces = len(board.pieces(chess.KNIGHT, chess.WHITE)) + len(board.pieces(chess.BISHOP, chess.WHITE)) + \
                   len(board.pieces(chess.KNIGHT, chess.BLACK)) + len(board.pieces(chess.BISHOP, chess.BLACK))
    
    is_endgame = (white_queens == 0 and black_queens == 0) or (white_queens == 1 and black_queens == 1 and minor_pieces <= 4)

    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            # Dynamic value lookup
            ptype = chess.piece_name(piece.piece_type).upper()
            value = weights.get(ptype, 0)
            
            # Position score
            pst_score = 0
            if piece.piece_type == chess.PAWN:
                pst_score = PAWN_TABLE[chess.square_mirror(square)] if piece.color == chess.BLACK else PAWN_TABLE[square]
            elif piece.piece_type == chess.KNIGHT:
                pst_score = KNIGHT_TABLE[chess.square_mirror(square)] if piece.color == chess.BLACK else KNIGHT_TABLE[square]
            elif piece.piece_type == chess.BISHOP:
                pst_score = BISHOP_TABLE[chess.square_mirror(square)] if piece.color == chess.BLACK else BISHOP_TABLE[square]
            elif piece.piece_type == chess.ROOK:
                pst_score = ROOK_TABLE[chess.square_mirror(square)] if piece.color == chess.BLACK else ROOK_TABLE[square]
            elif piece.piece_type == chess.QUEEN:
                pst_score = QUEEN_TABLE[chess.square_mirror(square)] if piece.color == chess.BLACK else QUEEN_TABLE[square]
            elif piece.piece_type == chess.KING:
                table = KING_TABLE_END if is_endgame else KING_TABLE_MID
                pst_score = table[chess.square_mirror(square)] if piece.color == chess.BLACK else table[square]

            if piece.color == chess.WHITE:
                score += value + pst_score
            else:
                score -= value + pst_score
    
    return score

def minimax(board, depth, alpha, beta, maximizing_player, weights=None):
    # Transposition Table Lookup
    fen = board.fen()
    if fen in TRANSPOSITION_TABLE:
        entry = TRANSPOSITION_TABLE[fen]
        if entry['depth'] >= depth:
            return entry['score']

    if board.is_checkmate():
        return -99999 + depth if maximizing_player else 99999 - depth

    if depth == 0 or board.is_game_over():
        score = evaluate_board(board, weights)
        # Store in TT
        TRANSPOSITION_TABLE[fen] = {'score': score, 'depth': depth}
        return score

    if maximizing_player:
        max_eval = -math.inf
        moves = sorted(board.legal_moves, key=lambda move: board.is_capture(move), reverse=True)
        
        for move in moves:
            board.push(move)
            eval = minimax(board, depth - 1, alpha, beta, False, weights)
            board.pop()
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        
        # Store in TT
        TRANSPOSITION_TABLE[fen] = {'score': max_eval, 'depth': depth}
        return max_eval
    else:
        min_eval = math.inf
        moves = sorted(board.legal_moves, key=lambda move: board.is_capture(move), reverse=True)
        
        for move in moves:
            board.push(move)
            eval = minimax(board, depth - 1, alpha, beta, True, weights)
            board.pop()
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        
        # Store in TT
        TRANSPOSITION_TABLE[fen] = {'score': min_eval, 'depth': depth}
        return min_eval

def get_best_move(board, depth=3, weights=None):
    # Check Opening Book
    book_move_san = openings.get_opening_move(board)
    if book_move_san:
        print(f"Book Move: {book_move_san}")
        return board.parse_san(book_move_san)

    best_move = None
    max_eval = -math.inf
    min_eval = math.inf
    
    maximizing_player = board.turn == chess.WHITE
    
    # print(f"Thinking... (Depth {depth})") # Silence for training
    
    moves = sorted(board.legal_moves, key=lambda move: board.is_capture(move), reverse=True)
    
    alpha = -math.inf
    beta = math.inf
    
    for move in moves:
        board.push(move)
        eval = minimax(board, depth - 1, alpha, beta, not maximizing_player, weights)
        board.pop()
        
        if maximizing_player:
            if eval > max_eval:
                max_eval = eval
                best_move = move
            alpha = max(alpha, eval)
        else:
            if eval < min_eval:
                min_eval = eval
                best_move = move
            beta = min(beta, eval)
            
    return best_move

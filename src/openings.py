# Standard Chess Openings
# Maps FEN (Forsyth-Edwards Notation) to the best move (SAN).
# We use a simplified FEN (board part only) or full FEN if needed.
# For simplicity, we'll use the full FEN of the starting position for each line.

OPENING_BOOK = {
    # Starting Position -> e4 (King's Pawn)
    "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1": "e4",
    
    # King's Pawn Game (1. e4)
    "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq - 0 1": "e5", # e5 (Open Game) or c5 (Sicilian)
    
    # Open Game (1. e4 e5) -> Nf3
    "rnbqkbnr/pppp1ppp/8/4p3/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 2": "Nf3",
    
    # Sicilian Defense (1. e4 c5) -> Nf3
    "rnbqkbnr/pp1ppppp/8/2p5/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 2": "Nf3",
    
    # Queen's Pawn Game (1. d4)
    # If we want to vary, we can't easily do it with a static dict unless we randomize in engine.
    # For now, let's stick to e4 as white.
    
    # French Defense (1. e4 e6) -> d4
    "rnbqkbnr/pppp1ppp/4p3/8/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 2": "d4",
    
    # Caro-Kann (1. e4 c6) -> d4
    "rnbqkbnr/pp1ppppp/2p5/8/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 2": "d4",
    
    # Ruy Lopez (1. e4 e5 2. Nf3 Nc6 3. Bb5)
    "r1bqkbnr/pppp1ppp/2n5/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq - 2 3": "Bb5",
    
    # Italian Game (1. e4 e5 2. Nf3 Nc6 3. Bc4)
    # "r1bqkbnr/pppp1ppp/2n5/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq - 2 3": "Bc4", # Alternate to Ruy Lopez
}

def get_opening_move(board):
    # Get FEN
    fen = board.fen()
    if fen in OPENING_BOOK:
        return OPENING_BOOK[fen]
    return None

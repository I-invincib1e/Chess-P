import os
import chess
import src.personality as personality

# ANSI Colors
RESET = "\033[0m"
BOLD = "\033[1m"
WHITE_BG = "\033[47m"
BLACK_BG = "\033[40m" # Actually dark grey for visibility
DARK_SQUARE = "\033[48;5;238m" # Dark Grey
LIGHT_SQUARE = "\033[48;5;250m" # Light Grey
WHITE_PIECE = "\033[38;5;15m" # Bright White
BLACK_PIECE = "\033[38;5;0m"  # Black
COMMENT_COLOR = "\033[38;5;51m" # Cyan for comments

# Unicode Pieces
PIECES = {
    'P': '♙', 'N': '♘', 'B': '♗', 'R': '♖', 'Q': '♕', 'K': '♔',
    'p': '♟', 'n': '♞', 'b': '♝', 'r': '♜', 'q': '♛', 'k': '♚',
    '.': ' '
}

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_board_visual(board):
    print("\n   " + " A  B  C  D  E  F  G  H ")
    
    for rank in range(7, -1, -1):
        line = f" {rank+1} "
        for file in range(8):
            square = chess.square(file, rank)
            piece = board.piece_at(square)
            
            # Determine square color
            if (rank + file) % 2 == 0:
                bg = DARK_SQUARE
            else:
                bg = LIGHT_SQUARE
                
            # Determine piece symbol and color
            if piece:
                symbol = PIECES[piece.symbol()]
                fg = WHITE_PIECE if piece.color == chess.WHITE else BLACK_PIECE
            else:
                symbol = " "
                fg = ""
                
            line += f"{bg}{fg} {symbol} {RESET}"
            
        print(line + f" {rank+1}")
        
    print("   " + " A  B  C  D  E  F  G  H \n")

def get_difficulty():
    print("\nSelect Difficulty Level:")
    print("1. Easy (Depth 1) - Fast, makes mistakes.")
    print("2. Medium (Depth 3) - Decent play, good balance.")
    print("3. Hard (Depth 4) - Stronger, takes a few seconds.")
    print("4. Expert (Depth 5) - Very strong, can take 10-20s.")
    
    while True:
        try:
            choice = input("Enter choice (1-4): ").strip()
            if choice == '1': return 1
            if choice == '2': return 3
            if choice == '3': return 4
            if choice == '4': return 5
            print("Invalid choice. Please enter 1, 2, 3, or 4.")
        except ValueError:
            print("Invalid input.")

def get_user_color():
    print("\nSelect Your Side:")
    print("1. Play as White (You move first)")
    print("2. Play as Black (Bot moves first)")
    print("3. Spectator / Both (Manual input for both)")
    
    while True:
        choice = input("Enter choice (1-3): ").strip()
        if choice == '1': return chess.WHITE
        if choice == '2': return chess.BLACK
        if choice == '3': return None
        print("Invalid choice. Please enter 1, 2, or 3.")

def get_persona():
    print("\nSelect Bot Personality:")
    print("1. The Gentleman (Polite)")
    print("2. The Troll (Rude)")
    print("3. The Coward (Scared)")
    
    while True:
        choice = input("Enter choice (1-3): ").strip()
        if choice == '1': return personality.GENTLEMAN
        if choice == '2': return personality.TROLL
        if choice == '3': return personality.COWARD
        print("Invalid choice.")

def print_comment(comment):
    if comment:
        print(f"{COMMENT_COLOR}Bot: {comment}{RESET}")

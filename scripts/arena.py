import sys
import os
import time
import chess
import chess.pgn

# Add parent directory to path to import src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import src.engine as engine
import src.rival_engine as rival_engine

def run_match(white_engine, black_engine, depth=3):
    board = chess.Board()
    game = chess.pgn.Game()
    game.headers["Event"] = "Python Chess Bot Arena"
    game.headers["White"] = white_engine.__name__
    game.headers["Black"] = black_engine.__name__
    
    node = game
    
    white_time = 0
    black_time = 0
    white_moves = 0
    black_moves = 0
    
    print(f"Starting Match: {white_engine.__name__} (White) vs {black_engine.__name__} (Black)")
    print(f"Depth: {depth}")
    print("-" * 40)
    
    while not board.is_game_over():
        start_time = time.time()
        
        try:
            if board.turn == chess.WHITE:
                move = white_engine.get_best_move(board, depth=depth)
                duration = time.time() - start_time
                white_time += duration
                white_moves += 1
                player = "White"
            else:
                move = black_engine.get_best_move(board, depth=depth)
                duration = time.time() - start_time
                black_time += duration
                black_moves += 1
                player = "Black"
                
            if move is None:
                print(f"Error: {player} returned None move. Game Over.")
                break
                
            san_move = board.san(move)
            board.push(move)
            node = node.add_variation(move)
            
            print(f"{board.fullmove_number}. {player} plays {san_move} ({duration:.2f}s)")
        except Exception as e:
            print(f"CRASH during {player}'s turn: {e}")
            import traceback
            traceback.print_exc()
            break
        # print(board) # Optional: Print board every move (can be spammy)
        
    print("-" * 40)
    print("Game Over")
    print("Result: " + board.result())
    
    if white_moves > 0:
        print(f"White ({white_engine.__name__}) Average Time: {white_time / white_moves:.2f}s")
    if black_moves > 0:
        print(f"Black ({black_engine.__name__}) Average Time: {black_time / black_moves:.2f}s")
        
    print(f"Total Moves: {board.fullmove_number}")
    
    return board.result()

if __name__ == "__main__":
    # You can swap engines here to test fairness
    # Match 1: Standard vs Rival
    print("\n=== MATCH 1 ===")
    run_match(engine, rival_engine, depth=2) # Lower depth for faster test
    
    # Match 2: Rival vs Standard
    print("\n=== MATCH 2 ===")
    run_match(rival_engine, engine, depth=2)

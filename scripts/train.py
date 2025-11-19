import sys
import os
import json
import random
import time
import copy
import chess

# Add parent directory to path to import src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import src.engine as engine

MODEL_FILE = "model.json"

def load_model(filepath):
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            return json.load(f)
    return None

def save_model(filepath, data):
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=4)

def mutate_weights(weights):
    new_weights = weights.copy()
    keys = list(new_weights.keys())
    if "KING" in keys: keys.remove("KING")
    
    key_to_mutate = random.choice(keys)
    mutation = random.randint(-50, 50)
    
    new_val = new_weights[key_to_mutate] + mutation
    if new_val < 0 and key_to_mutate != "DRAW_PENALTY":
        new_val = 0
        
    new_weights[key_to_mutate] = new_val
    print(f"  -> Mutation: {key_to_mutate} {weights[key_to_mutate]} -> {new_val}")
    return new_weights

def play_match(white_weights, black_weights, depth=2):
    board = chess.Board()
    
    while not board.is_game_over():
        if board.turn == chess.WHITE:
            move = engine.get_best_move(board, depth=depth, weights=white_weights)
        else:
            move = engine.get_best_move(board, depth=depth, weights=black_weights)
            
        if move is None:
            break
        board.push(move)
        
    return board.result()

def main():
    print("=== CHESS BOT GYM ===")
    
    # Load Base Model
    model = load_model(MODEL_FILE)
    if not model:
        print("Error: model.json not found. Run engine.py first or create it.")
        return

    print(f"Current Rating: {model.get('rating', 1000)}")
    print(f"Generation: {model.get('generation', 0)}")
    
    generations = 5 # Run 5 generations per execution
    
    for gen in range(generations):
        print(f"\n--- Generation {model.get('generation', 0) + 1} ---")
        
        base_weights = model["weights"]
        mutant_weights = mutate_weights(base_weights)
        
        # Play Match: Base (White) vs Mutant (Black)
        print("  Match 1: Base (White) vs Mutant (Black)...")
        result1 = play_match(base_weights, mutant_weights, depth=1) # Low depth for speed
        print(f"  Result: {result1}")
        
        # Play Match: Mutant (White) vs Base (Black)
        print("  Match 2: Mutant (White) vs Base (Black)...")
        result2 = play_match(mutant_weights, base_weights, depth=1)
        print(f"  Result: {result2}")
        
        # Scoring
        mutant_score = 0
        if result1 == "0-1": mutant_score += 1 # Mutant won as Black
        elif result1 == "1/2-1/2": mutant_score += 0.5
        
        if result2 == "1-0": mutant_score += 1 # Mutant won as White
        elif result2 == "1/2-1/2": mutant_score += 0.5
        
        print(f"  Mutant Score: {mutant_score}/2")
        
        if mutant_score >= 1.5:
            print("  >>> MUTATION SUCCESS! Updating model.")
            model["weights"] = mutant_weights
            model["rating"] = model.get("rating", 1000) + 5
        elif mutant_score <= 0.5:
            print("  >>> MUTATION FAILED. Keeping base.")
            model["rating"] = model.get("rating", 1000) - 2
        else:
            print("  >>> DRAW/EQUAL. Keeping base.")
            
        model["generation"] = model.get("generation", 0) + 1
        save_model(MODEL_FILE, model)

if __name__ == "__main__":
    main()

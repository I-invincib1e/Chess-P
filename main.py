import sys
import os
import time
import chess

import src.engine as engine
import src.personality as personality
import src.ui as ui

def main():
    # Load weights
    engine.load_weights("model.json")
    
    board = chess.Board()
    
    ui.clear_screen()
    print(f"{ui.BOLD}Welcome to the Enhanced Python Chess Bot!{ui.RESET}")
    
    depth = ui.get_difficulty()
    print(f"Difficulty set to Depth {depth}.")
    
    user_color = ui.get_user_color()
    if user_color == chess.WHITE:
        print("You are playing as WHITE.")
    elif user_color == chess.BLACK:
        print("You are playing as BLACK.")
    else:
        print("Mode: Spectator / Manual Control.")
    
    persona = ui.get_persona()
    personality.set_persona(persona)
    print(f"Bot Personality set to: {persona}")
    
    print("\nEnter moves in standard algebraic notation (e.g., e4, Nf3).")
    print("Type 'quit' or 'exit' to stop.")
    
    input("Press ENTER to start...")
    
    # Game Start Comment
    comment = personality.get_comment("GAME_START")
    ui.print_comment(comment)
    
    while not board.is_game_over():
        ui.clear_screen()
        ui.print_board_visual(board)
        
        if board.turn == chess.WHITE:
            turn_name = "White"
        else:
            turn_name = "Black"
            
        print(f"Current Turn: {turn_name}")
        
        # Check if it's Bot's turn
        is_bot_turn = (user_color is not None) and (board.turn != user_color)
        
        if is_bot_turn:
            print(f"Bot is thinking for {turn_name}...")
            best_move = engine.get_best_move(board, depth=depth)
            
            if best_move:
                print(f"Bot plays: {board.san(best_move)}")
                board.push(best_move)
                
                # Bot Move Comment
                event = "BOT_MOVE"
                if board.is_check(): event = "BOT_CHECK"
                elif board.is_capture(best_move): event = "BOT_CAPTURE"
                
                comment = personality.get_comment(event, board)
                ui.print_comment(comment)
            else:
                print("No moves available (Game Over?)")
        else:
            # User turn
            prompt = f"Enter move for {turn_name}"
            if user_color is None:
                prompt += " (or press ENTER for bot suggestion)"
            
            user_input = input(f"{prompt}: ").strip()
            
            if user_input.lower() in ['quit', 'exit']:
                break
                
            if user_input:
                try:
                    move = board.parse_san(user_input)
                    board.push(move)
                    
                    # User Move Comment
                    event = "USER_MOVE"
                    if board.is_check(): event = "USER_CHECK"
                    
                    comment = personality.get_comment(event, board)
                    ui.print_comment(comment)
                        
                except ValueError:
                    print(f"Invalid move: {user_input}.")
                    input("Press ENTER to continue...")
                    continue
            else:
                if user_color is None:
                    print(f"Bot is thinking for {turn_name}...")
                    best_move = engine.get_best_move(board, depth=depth)
                    if best_move:
                        board.push(best_move)
                else:
                    print("Please enter a move.")
                    input("Press ENTER to continue...")
                
    print("Game Over")
    result = board.result()
    print(result)
    
    # Game End Comment
    if result == "1-0":
        if user_color == chess.WHITE: event = "LOSS" # Bot lost
        elif user_color == chess.BLACK: event = "WIN" # Bot won
        else: event = "WIN"
    elif result == "0-1":
        if user_color == chess.WHITE: event = "WIN" # Bot won
        elif user_color == chess.BLACK: event = "LOSS" # Bot lost
        else: event = "WIN"
    else:
        event = "LOSS" # Draw is kinda a loss for a bot? Or add DRAW event.
        
    comment = personality.get_comment(event)
    ui.print_comment(comment)

if __name__ == "__main__":
    main()

import sys
import os
import time
import chess
from rich.live import Live

import src.engine as engine
import src.personality as personality
import src.ui as ui
import src.tui as tui

def main():
    # Load weights
    engine.load_weights("model.json")
    
    board = chess.Board()
    
    ui.clear_screen()
    print(f"{ui.BOLD}Welcome to RoastChess!{ui.RESET}")
    
    depth = ui.get_difficulty()
    print(f"Difficulty set to Depth {depth}.")
    
    user_color = ui.get_user_color()
    
    persona = ui.get_persona()
    personality.set_persona(persona)
    print(f"Bot Personality set to: {persona}")
    
    input("Press ENTER to start...")
    
    # Initialize Rich TUI
    game_tui = tui.RichGame()
    game_tui.set_status(f"Game Started! You are {user_color if user_color is not None else 'Spectator'}")
    
    # Game Start Comment
    comment = personality.get_comment("GAME_START")
    if comment: game_tui.add_chat(comment)
    
    with Live(game_tui.layout, refresh_per_second=4, screen=True) as live:
        while not board.is_game_over():
            game_tui.update(board)
            
            if board.turn == chess.WHITE:
                turn_name = "White"
            else:
                turn_name = "Black"
                
            game_tui.set_status(f"Current Turn: {turn_name}")
            
            # Check if it's Bot's turn
            is_bot_turn = (user_color is not None) and (board.turn != user_color)
            
            if is_bot_turn:
                game_tui.set_status(f"Bot ({persona}) is thinking...")
                live.refresh() # Force update status
                
                best_move = engine.get_best_move(board, depth=depth)
                
                if best_move:
                    game_tui.add_move(board.san(best_move))
                    board.push(best_move)
                    
                    # Bot Move Comment
                    event = "BOT_MOVE"
                    if board.is_check(): event = "BOT_CHECK"
                    elif board.is_capture(best_move): event = "BOT_CAPTURE"
                    
                    comment = personality.get_comment(event, board)
                    if comment: game_tui.add_chat(comment)
                else:
                    game_tui.set_status("No moves available (Game Over?)")
            else:
                # User turn
                game_tui.set_status(f"Your Turn ({turn_name}). Enter move in console below:")
                live.stop() # Pause live display to get input
                
                prompt = f"Enter move for {turn_name}"
                if user_color is None:
                    prompt += " (or press ENTER for bot suggestion)"
                
                print(game_tui.update(board)) # Print static board for context
                user_input = input(f"{prompt}: ").strip()
                
                live.start() # Resume live display
                
                if user_input.lower() in ['quit', 'exit']:
                    break
                    
                if user_input:
                    try:
                        move = board.parse_san(user_input)
                        game_tui.add_move(user_input)
                        board.push(move)
                        
                        # User Move Comment
                        event = "USER_MOVE"
                        if board.is_check(): event = "USER_CHECK"
                        
                        comment = personality.get_comment(event, board)
                        if comment: game_tui.add_chat(comment)
                            
                    except ValueError:
                        game_tui.set_status(f"Invalid move: {user_input}")
                        time.sleep(1)
                        continue
                else:
                    if user_color is None:
                        game_tui.set_status("Bot is thinking for you...")
                        live.refresh()
                        best_move = engine.get_best_move(board, depth=depth)
                        if best_move:
                            game_tui.add_move(board.san(best_move))
                            board.push(best_move)
                    else:
                        pass
                    
        result = board.result()
        game_tui.set_status(f"Game Over! Result: {result}")
        
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
            event = "LOSS" 
            
        comment = personality.get_comment(event)
        if comment: game_tui.add_chat(comment)
        
        game_tui.update(board)
        input("Press ENTER to exit...")

if __name__ == "__main__":
    main()

# ♟️ Python Chess Bot

A sophisticated terminal-based chess AI written in Python. It features a custom Minimax engine with Alpha-Beta pruning, a personality system, and an evolutionary training arena.

![Chess Bot Terminal Interface](C:/Users/neore/.gemini/antigravity/brain/b926e032-cb3f-4e61-a0ce-fc653d363195/chess_bot_terminal_screenshot_1763584675878.png)

## ✨ Features

- **Custom Engine**: Built from scratch using Minimax and Alpha-Beta pruning.
- **Personality Engine**: Play against different personas (Gentleman, Troll, Coward) that comment on your moves.
- **Bot Arena**: Simulate matches between different engine versions.
- **Evolutionary Training**: Train the bot to improve its piece valuation weights over time.
- **Opening Book**: Integrated opening book for instant early-game moves.
- **Transposition Table**: Optimized search using Zobrist hashing (simulated).
- **Visuals**: Beautiful terminal interface with ANSI colors and Unicode pieces.

## 🚀 Getting Started

### Prerequisites
- Python 3.x
- `python-chess` library

```bash
pip install python-chess
```

### 🎮 How to Play

Run the main script to start a game:

```bash
python main.py
```

Follow the on-screen prompts to:
1. Select Difficulty (Depth 1-5)
2. Choose your side (White, Black, or Spectator)
3. Select the Bot's Personality

### ⚔️ Bot Arena

Watch two engines battle it out:

```bash
python scripts/arena.py
```

### 🏋️ Training Gym

Train the bot to improve its strategy:

```bash
python scripts/train.py
```

## 📂 Project Structure

- `main.py`: Entry point for the game.
- `src/`: Core source code (Engine, UI, Personality).
- `scripts/`: Utility scripts for testing and training.
- `model.json`: Stores the bot's learned weights and rating.

## 📝 License

Open source. Feel free to fork and improve!

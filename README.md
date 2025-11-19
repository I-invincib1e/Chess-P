# ♟️ RoastChess: The AI That Judges You

A **Trash-Talking, Evolutionary Chess Bot** that learns from its mistakes and roasts you for yours. Built from scratch in Python.

![RoastChess Dashboard](C:/Users/neore/.gemini/antigravity/brain/b926e032-cb3f-4e61-a0ce-fc653d363195/roast_chess_dashboard_screenshot_1763584675878.png)

## ✨ Features

- **Pro Dashboard UI**: A hacker-style terminal interface with split panels for board, chat, and history.
- **Trash-Talking Persona**: The bot roasts you in real-time.
- **Custom Engine**: Built from scratch using Minimax and Alpha-Beta pruning.
- **Evolutionary Training**: Train the bot to improve its piece valuation weights over time.

## 🚀 Getting Started

### Prerequisites
- Python 3.x
- `python-chess` library
- `rich` library

```bash
pip install python-chess rich
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

from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.live import Live
from rich.align import Align
import chess
import src.personality as personality

console = Console()

# ANSI Colors (mapped to Rich styles where possible, but we use hex for board)
DARK_SQUARE_STYLE = "on #404040"
LIGHT_SQUARE_STYLE = "on #808080"
WHITE_PIECE_STYLE = "bold white"
BLACK_PIECE_STYLE = "bold black"

PIECES = {
    'P': '♙', 'N': '♘', 'B': '♗', 'R': '♖', 'Q': '♕', 'K': '♔',
    'p': '♟', 'n': '♞', 'b': '♝', 'r': '♜', 'q': '♛', 'k': '♚',
    '.': ' '
}

class RichGame:
    def __init__(self):
        self.layout = Layout()
        self.layout.split_row(
            Layout(name="left", ratio=2),
            Layout(name="right", ratio=1)
        )
        self.layout["left"].split_column(
            Layout(name="header", size=3),
            Layout(name="board", ratio=1),
            Layout(name="status", size=3)
        )
        self.layout["right"].split_column(
            Layout(name="chat", ratio=2),
            Layout(name="history", ratio=1)
        )
        
        self.chat_log = []
        self.move_history = []
        self.status_text = "Welcome to RoastChess!"
        self.header_text = "♟️ RoastChess: The AI That Judges You"

    def update(self, board):
        # Header
        self.layout["left"]["header"].update(
            Panel(Align.center(Text(self.header_text, style="bold cyan")), style="cyan")
        )
        
        # Board
        board_table = Table.grid()
        for _ in range(8): board_table.add_column()
        
        for rank in range(7, -1, -1):
            row_cells = []
            for file in range(8):
                square = chess.square(file, rank)
                piece = board.piece_at(square)
                
                bg = DARK_SQUARE_STYLE if (rank + file) % 2 == 0 else LIGHT_SQUARE_STYLE
                
                if piece:
                    symbol = PIECES[piece.symbol()]
                    style = f"{WHITE_PIECE_STYLE} {bg}" if piece.color == chess.WHITE else f"{BLACK_PIECE_STYLE} {bg}"
                else:
                    symbol = " "
                    style = bg
                    
                row_cells.append(Text(f" {symbol} ", style=style))
            board_table.add_row(*row_cells)
            
        self.layout["left"]["board"].update(
            Panel(Align.center(board_table), title="Chess Board", border_style="green")
        )
        
        # Status
        self.layout["left"]["status"].update(
            Panel(Text(self.status_text, justify="center"), title="Status", border_style="yellow")
        )
        
        # Chat
        chat_text = Text()
        for msg in self.chat_log[-10:]: # Show last 10 messages
            chat_text.append(msg + "\n")
        self.layout["right"]["chat"].update(
            Panel(chat_text, title="Trash Talk", border_style="red")
        )
        
        # History
        hist_text = ""
        for i, move in enumerate(self.move_history[-10:]):
            hist_text += f"{len(self.move_history)-9+i}. {move}\n"
        self.layout["right"]["history"].update(
            Panel(hist_text, title="Move History", border_style="blue")
        )
        
        return self.layout

    def add_chat(self, message, speaker="Bot"):
        color = "cyan" if speaker == "Bot" else "green"
        self.chat_log.append(Text(f"{speaker}: {message}", style=color))

    def add_move(self, move_san):
        self.move_history.append(move_san)
        
    def set_status(self, status):
        self.status_text = status

game_ui = RichGame()

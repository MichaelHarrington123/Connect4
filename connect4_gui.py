"""Connect 4 with a clickable Tkinter window.

Run this file to play with a graphical interface:
    python connect4_gui.py


"""

import tkinter as tk
from tkinter import messagebox

import boardPos
import connect4


# Colors for the interface.
BG = "#101827"
PANEL = "#1c2940"
BLUE = "#3266ce"
RED = "#f05262"
YELLOW = "#f6c94e"
WHITE = "#f4f7fd"
MUTED = "#a9bad3"

CELL_SIZE = 66
BOARD_LEFT = 70
BOARD_TOP = 57


class GameSession:
    """Keeps track of turns and uses the group's existing game rules."""

    def __init__(self):
        self.new_game("Red")

    def new_game(self, first_color):
        connect4.createBoard()
        self.colors = {1: first_color,
                       2: "Yellow" if first_color == "Red" else "Red"}
        self.current_player = 1
        self.moves = 0
        self.game_over = False
        self.winner = None

    def drop_piece(self, column):
        """Place a disc in a column (0 to 6) and return the result."""
        if self.game_over:
            return "finished"
        if column < 0 or column > 6:
            return "invalid"

        # Work upward from the bottom of the selected column.
        for row in range(5, -1, -1):
            if boardPos.board[column][row] == 0:
                boardPos.board[column][row] = self.current_player
                break
        else:
            return "full"

        self.moves += 1

        if connect4.checkConnect4(column, row, self.current_player) > 0:
            self.game_over = True
            self.winner = self.current_player
            return "win"

        if self.moves == 42:
            self.game_over = True
            return "draw"

        self.current_player = 3 - self.current_player
        return "move"


class Connect4Window:
    """Draws the board and handles mouse clicks."""

    def __init__(self, root):
        self.root = root
        self.game = GameSession()
        self.hover_column = None
        self.first_color = tk.StringVar(value="Red")
        self.build_window()
        self.draw_board()
        self.show_turn()

    def build_window(self):
        self.root.title("Connect 4 | CPSC 118")
        self.root.geometry("730x760")
        self.root.minsize(680, 720)
        self.root.configure(bg=BG)

        tk.Label(self.root, text="CONNECT 4", bg=BG, fg=WHITE,
                 font=("Arial", 28, "bold")).pack(pady=(14, 0))
        tk.Label(self.root, text="TWO PLAYER  |  CLICK TO DROP",
                 bg=BG, fg=MUTED, font=("Arial", 10, "bold")).pack(pady=(2, 8))

        controls = tk.Frame(self.root, bg=PANEL, padx=17, pady=10)
        controls.pack(fill="x", padx=40)
        tk.Label(controls, text="PLAYER 1 COLOR", bg=PANEL, fg=MUTED,
                 font=("Arial", 10, "bold")).pack(side="left", padx=(0, 10))

        for color in ("Red", "Yellow"):
            tk.Radiobutton(
                controls, text=color, value=color, variable=self.first_color,
                command=self.start_new_game, bg=PANEL, fg=WHITE,
                activebackground=PANEL, activeforeground=WHITE,
                selectcolor=BG, font=("Arial", 11), cursor="hand2"
            ).pack(side="left", padx=4)

        tk.Button(controls, text="Rules", command=self.show_rules,
                  bg="#334766", fg=WHITE, activebackground="#466186",
                  activeforeground=WHITE, relief="flat", padx=12,
                  pady=6, cursor="hand2").pack(side="right")

        self.status = tk.Label(self.root, bg=BG, fg=WHITE,
                               font=("Arial", 16, "bold"))
        self.status.pack(pady=(12, 0))
        self.detail = tk.Label(self.root, bg=BG, fg=MUTED,
                               font=("Arial", 10))
        self.detail.pack(pady=(3, 2))

        # The numbered columns and all 42 spaces are drawn on this canvas.
        self.canvas = tk.Canvas(self.root, width=600, height=468,
                                bg=BG, highlightthickness=0, cursor="hand2")
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.handle_click)
        self.canvas.bind("<Motion>", self.handle_motion)
        self.canvas.bind("<Leave>", self.handle_leave)

        bottom = tk.Frame(self.root, bg=BG)
        bottom.pack(pady=(1, 0))
        tk.Button(bottom, text="NEW GAME / PLAY AGAIN",
                  command=self.start_new_game, bg=BLUE, fg=WHITE,
                  activebackground="#2453b5", activeforeground=WHITE,
                  relief="flat", font=("Arial", 11, "bold"),
                  padx=19, pady=10, cursor="hand2").pack(side="left", padx=7)
        tk.Button(bottom, text="QUIT", command=self.root.destroy,
                  bg=PANEL, fg=WHITE, activebackground="#334766",
                  activeforeground=WHITE, relief="flat", padx=18,
                  pady=10, cursor="hand2").pack(side="left", padx=7)

    def draw_board(self):
        self.canvas.delete("all")

        # Numbers at the top make the seven columns clear.
        for column in range(7):
            x = BOARD_LEFT + column * CELL_SIZE + CELL_SIZE / 2
            selected = column == self.hover_column and not self.game.game_over
            color = WHITE if selected else MUTED
            self.canvas.create_text(x, 26, text=str(column + 1),
                                    fill=color, font=("Arial", 14, "bold"))
            if selected:
                self.canvas.create_line(x - 20, 45, x + 20, 45,
                                        fill=YELLOW, width=3)

        # Blue board with a dark round slot for every empty space.
        right = BOARD_LEFT + 7 * CELL_SIZE
        bottom = BOARD_TOP + 6 * CELL_SIZE
        self.canvas.create_rectangle(BOARD_LEFT - 9, BOARD_TOP - 9,
                                     right + 9, bottom + 9,
                                     fill=BLUE, outline="#5988eb", width=3)

        for row in range(6):
            for column in range(7):
                x = BOARD_LEFT + column * CELL_SIZE
                y = BOARD_TOP + row * CELL_SIZE
                space = boardPos.board[column][row]
                if space == 0:
                    fill_color = "#122441"
                elif self.game.colors[space] == "Red":
                    fill_color = RED
                else:
                    fill_color = YELLOW

                self.canvas.create_oval(x + 7, y + 7,
                                        x + CELL_SIZE - 7,
                                        y + CELL_SIZE - 7,
                                        fill=fill_color, outline="#214a9f",
                                        width=2)

    def column_at(self, x, y):
        """Return the clicked column, or None if outside the board."""
        if x < BOARD_LEFT or x >= BOARD_LEFT + 7 * CELL_SIZE:
            return None
        if y < 0 or y >= BOARD_TOP + 6 * CELL_SIZE:
            return None
        return (x - BOARD_LEFT) // CELL_SIZE

    def handle_click(self, event):
        column = self.column_at(event.x, event.y)
        if column is None:
            return

        result = self.game.drop_piece(column)
        self.draw_board()

        if result == "full":
            self.status.config(text="That column is full!", fg=YELLOW)
            self.detail.config(text="Click a different column.")
        elif result == "win":
            winner = self.game.winner
            color = self.game.colors[winner]
            self.status.config(text=f"PLAYER {winner} WINS!", fg=RED if color == "Red" else YELLOW)
            self.detail.config(text=f"{color} connected four. Select Play Again for another round.")
        elif result == "draw":
            self.status.config(text="IT'S A TIE!", fg=WHITE)
            self.detail.config(text="No empty spaces left. Select Play Again.")
        elif result == "move":
            self.show_turn()

    def handle_motion(self, event):
        column = self.column_at(event.x, event.y)
        if column != self.hover_column:
            self.hover_column = column
            self.draw_board()

    def handle_leave(self, event):
        self.hover_column = None
        self.draw_board()

    def show_turn(self):
        player = self.game.current_player
        color = self.game.colors[player]
        self.status.config(text=f"PLAYER {player}'S TURN", fg=RED if color == "Red" else YELLOW)
        self.detail.config(text=f"Player 1: {self.game.colors[1]}    |    "
                                f"Player 2: {self.game.colors[2]}    |    Click a column")

    def start_new_game(self):
        self.game.new_game(self.first_color.get())
        self.hover_column = None
        self.draw_board()
        self.show_turn()

    def show_rules(self):
        messagebox.showinfo(
            "How to Play Connect 4",
            "Two players take turns clicking a column.\n\n"
            "Your piece drops to the lowest open spot.\n\n"
            "Connect four pieces in a row horizontally, vertically, "
            "or diagonally to win.\n\n"
            "If all 42 spaces fill up without four in a row, it's a tie.\n\n"
            "Use New Game / Play Again to start over.",
            parent=self.root
        )


def main():
    root = tk.Tk()
    Connect4Window(root)
    root.mainloop()


if __name__ == "__main__":
    main()

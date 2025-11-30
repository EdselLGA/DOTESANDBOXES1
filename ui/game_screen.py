# ui/game_screen.py
from tkinter import Frame, Canvas, Label, Button
from utils.constants import BG_COLOR, BORDER_COLOR
import numpy as np

class GameScreen(Frame):
    def __init__(self, parent, manager):
        super().__init__(parent, bg=BG_COLOR,
                         highlightbackground=BORDER_COLOR,
                         highlightthickness=6)

        self.manager = manager

        # Canvas
        self.canvas = Canvas(self, width=600, height=600, bg="white")
        self.canvas.pack(side="left", padx=30, pady=30)

        self.engine = None
        self.canvas.bind("<Button-1>", self._placeholder_click)

        # Right panel
        self.right = Frame(self, bg=BG_COLOR)
        self.right.pack(side="right", fill="y", padx=10, pady=10)
        self.right.configure(highlightbackground=BORDER_COLOR, highlightthickness=4)

        self.title = Label(self.right, text="Player vs Player",
                           fg="white", bg=BG_COLOR, font=("Comic Sans MS", 26))
        self.title.pack(pady=15)

        self.turn_label = Label(self.right, text="", fg="white",
                                bg=BG_COLOR, font=("Comic Sans MS", 20))
        self.turn_label.pack(pady=15)

        # ========================
        # LIVE SCORE SECTION
        # ========================
        score_frame = Frame(self.right, bg=BG_COLOR)
        score_frame.pack(pady=10)

        self.p1_score_label = Label(score_frame, text="P1: 0",
                                    fg="white", bg=BG_COLOR,
                                    font=("Comic Sans MS", 20))
        self.p1_score_label.pack(pady=5)

        self.p2_score_label = Label(score_frame, text="P2: 0",
                                    fg="white", bg=BG_COLOR,
                                    font=("Comic Sans MS", 20))
        self.p2_score_label.pack(pady=5)

        # ========================
        # BUTTONS
        # ========================
        Button(self.right, text="HINT", font=("Comic Sans MS", 18), width=12,
               command=self.show_hint).pack(pady=10)

        Button(self.right, text="UNDO", font=("Comic Sans MS", 18), width=12).pack(pady=10)

        Button(self.right, text="BACK", font=("Comic Sans MS", 18), width=12,
               command=lambda: manager.show_screen("ModeSelect")).pack(pady=40)

        self.mode = None
        self.difficulty = None

    def _placeholder_click(self, event):
        return "no-engine"

    # ========================
    # LOAD SCREEN
    # ========================
    def load(self, mode=None, difficulty=None, **kwargs):
        # Lazy load engine
        if self.engine is None:
            try:
                from core.game_engine import GameEngine
                self.engine = GameEngine(self.canvas)
            except Exception as e:
                print("[GameScreen] Error creating GameEngine:", e)
                self.engine = None

        if self.engine:
            self.canvas.unbind("<Button-1>")
            self.canvas.bind("<Button-1>", self.on_click)

        self.mode = mode
        self.difficulty = difficulty

        self.place(relwidth=1, relheight=1)

        # Reset engine
        if self.engine and hasattr(self.engine, "reset_game_state"):
            try:
                self.engine.reset_game_state()
            except Exception as e:
                print("[GameScreen] reset_game_state error:", e)

        # Update title
        if mode == "PVP" or mode is None:
            self.title.config(text="Player vs Player")
        else:
            self.title.config(text=f"AI Mode: {difficulty.upper() if difficulty else 'EASY'}")

        self.update_turn_label()
        self.update_score_display()

    def unload(self):
        self.place_forget()

    # ========================
    # UPDATE LIVE SCORE
    # ========================
    def update_score_display(self):
        if not self.engine:
            return

        p1 = int(np.count_nonzero(self.engine.box_owner == 1))
        p2 = int(np.count_nonzero(self.engine.box_owner == 2))

        self.p1_score_label.config(text=f"P1: {p1}")
        self.p2_score_label.config(text=f"P2: {p2}")

    # ========================
    # UPDATE TURN TEXT
    # ========================
    def update_turn_label(self):
        if self.engine and hasattr(self.engine, "display_turn_text"):
            try:
                self.engine.display_turn_text()
            except:
                pass

    # ========================
    # HINT BUTTON
    # ========================
    def show_hint(self):
        if not self.engine:
            return

        move = self.engine.get_hint()
        if move is None:
            return

        edge_type, pos = move
        self.engine.highlight_edge(edge_type, pos)

    # ========================
    # CLICK HANDLER
    # ========================
    def on_click(self, event):
        if not self.engine:
            return

        try:
            result = self.engine.click(event)
        except Exception as e:
            print("[GameScreen] engine.click error:", e)
            result = None

        # UPDATE LIVE SCORE AFTER EACH CLICK
        self.update_score_display()

        # GAME OVER
        if isinstance(result, dict):
            winner = result.get("result_text", "")
            p1 = int(result.get("player1_score", 0))
            p2 = int(result.get("player2_score", 0))

            self.manager.show_screen(
                "ResultScreen",
                result_text=winner,
                p1_score=p1,
                p2_score=p2
            )
            return

        # Still playing
        self.update_turn_label()

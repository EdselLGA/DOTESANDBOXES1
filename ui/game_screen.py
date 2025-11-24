# ui/game_screen.py
from tkinter import Frame, Canvas, Label, Button
from utils.constants import BG_COLOR, BORDER_COLOR

# import GameEngine lazily inside load to avoid engine executing at import-time
# from core.game_engine import GameEngine


class GameScreen(Frame):
    def __init__(self, parent, manager):
        super().__init__(parent, bg=BG_COLOR,
                         highlightbackground=BORDER_COLOR,
                         highlightthickness=6)

        self.manager = manager

        # create canvas widget but do NOT attach engine yet
        self.canvas = Canvas(self, width=600, height=600, bg="white")
        self.canvas.pack(side="left", padx=30, pady=30)

        # engine will be created in load()
        self.engine = None

        # Bind a placeholder click handler that does nothing until engine exists
        self.canvas.bind("<Button-1>", self._placeholder_click)

        # Right: UI panel
        self.right = Frame(self, bg=BG_COLOR)
        self.right.pack(side="right", fill="y", padx=10, pady=10)
        self.right.configure(highlightbackground=BORDER_COLOR, highlightthickness=4)

        self.title = Label(self.right, text="Player vs Player",
                           fg="white", bg=BG_COLOR, font=("Comic Sans MS", 26))
        self.title.pack(pady=15)

        self.turn_label = Label(self.right, text="", fg="white",
                                bg=BG_COLOR, font=("Comic Sans MS", 20))
        self.turn_label.pack(pady=15)

        Button(self.right, text="HINT", font=("Comic Sans MS", 18), width=12).pack(pady=10)
        Button(self.right, text="UNDO", font=("Comic Sans MS", 18), width=12).pack(pady=10)

        Button(self.right, text="BACK", font=("Comic Sans MS", 18), width=12,
               command=lambda: manager.show_screen("ModeSelect")).pack(pady=40)

        self.mode = None
        self.difficulty = None

    def _placeholder_click(self, event):
        # Do nothing until engine is created
        return "no-engine"

    def load(self, mode=None, difficulty=None):
        # Lazy import and engine creation to avoid engine running on import
        if self.engine is None:
            try:
                from core.game_engine import GameEngine
            except Exception as e:
                print("[GameScreen] Failed to import GameEngine:", e)
                GameEngine = None

            if GameEngine:
                # create engine passing canvas
                try:
                    self.engine = GameEngine(self.canvas)
                except Exception as e:
                    print("[GameScreen] Error creating GameEngine:", e)
                    self.engine = None

        # Replace click handler with engine-aware handler
        if self.engine:
            self.canvas.unbind("<Button-1>")
            self.canvas.bind("<Button-1>", self.on_click)

        self.mode = mode
        self.difficulty = difficulty

        # Place UI
        self.place(relwidth=1, relheight=1)

        # Reset engine state now that screen is visible
        if self.engine:
            if hasattr(self.engine, "reset_game_state"):
                try:
                    self.engine.reset_game_state()
                except Exception as e:
                    print("[GameScreen] engine.reset_game_state error:", e)
            elif hasattr(self.engine, "reset"):
                try:
                    self.engine.reset()
                except Exception as e:
                    print("[GameScreen] engine.reset error:", e)

        # Update UI title
        if mode == "PVP" or mode is None:
            self.title.config(text="Player vs Player")
        else:
            self.title.config(text=f"AI Mode: {difficulty.upper() if difficulty else 'EASY'}")

        self.update_turn_label()

    def unload(self):
        # Hide UI
        self.place_forget()

    def update_turn_label(self):
        if self.engine:
            if hasattr(self.engine, "current_player"):
                self.turn_label.config(text=f"Turn: {self.engine.current_player}")
            elif hasattr(self.engine, "turn_text"):
                self.turn_label.config(text=self.engine.turn_text)
            else:
                self.turn_label.config(text="")

    def on_click(self, event):
        # route event to engine; engine.click may accept event or coordinates
        if not self.engine:
            return

        try:
            result = self.engine.click(event)
        except Exception:
            try:
                result = self.engine.click(event.x, event.y)
            except Exception as e:
                print("[GameScreen] engine.click raised:", e)
                result = None

        if result:
            self.manager.show_screen("ResultScreen", result_text=result)
        else:
            self.update_turn_label()

from tkinter import Frame, Label, Button
from utils.constants import BG_COLOR, BORDER_COLOR

class MainMenu(Frame):
    def __init__(self, parent, manager):
        super().__init__(
            parent, 
            bg=BG_COLOR,
            highlightbackground=BORDER_COLOR,
            highlightthickness=6
        )
        self.manager = manager
        self.place(relwidth=1, relheight=1)

        Label(
            self,
            text="DOTS AND BOXES",
            font=("Comic Sans MS", 44, "bold"),
            fg="white",
            bg=BG_COLOR
        ).pack(pady=80)

        Button(
            self,
            text="START",
            font=("Comic Sans MS", 22),
            width=15,
            command=lambda: manager.show_screen("ModeSelect")
        ).pack(pady=15)

        Button(
            self,
            text="EXIT",
            font=("Comic Sans MS", 22),
            width=15,
            command=self.quit
        ).pack(pady=10)

    def load(self):
        pass

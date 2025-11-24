from tkinter import Button

class BackButton(Button):
    def __init__(self, parent, command=None, text="BACK", **kwargs):
        super().__init__(
            parent,
            text=text,
            command=command,
            font=("Comic Sans MS", 18),
            width=12,
            **kwargs
        )

from tkinter import Button

class RoundedButton(Button):
    def __init__(self, parent, text="", command=None, width=15, **kwargs):
        super().__init__(
            parent,
            text=text,
            command=command,
            font=("Comic Sans MS", 18),
            width=width,
            **kwargs
        )

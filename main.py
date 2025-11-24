from tkinter import Tk
from ui.main_menu import MainMenu
from ui.mode_select import ModeSelect
from ui.difficulty_select import DifficultySelect
from ui.game_screen import GameScreen
from ui.result_screen import ResultScreen


class ScreenManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Dots and Boxes")
        self.root.geometry("1000x700")   # Window size
        self.root.configure(bg="black")

        # Storage for all screens
        self.screens = {}

        # Create all screens
        self.register_screens()

        # Show the first screen
        self.show_screen("MainMenu")

    def register_screens(self):
        """Create all screens and store them."""
        self.screens["MainMenu"] = MainMenu(self.root, self)
        self.screens["ModeSelect"] = ModeSelect(self.root, self)
        self.screens["DifficultySelect"] = DifficultySelect(self.root, self)
        self.screens["GameScreen"] = GameScreen(self.root, self)
        self.screens["ResultScreen"] = ResultScreen(self.root, self)

    def show_screen(self, name, **kwargs):
        """Switch to the selected screen."""
        screen = self.screens[name]
        screen.tkraise()       # Bring frame to front
        screen.load(**kwargs)  # Refresh screen data


def main():
    root = Tk()
    app = ScreenManager(root)
    root.mainloop()


if __name__ == "__main__":
    main()

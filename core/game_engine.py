# core/game_engine.py
from tkinter import *
import numpy as np

# -------------------------------------------------------
# CONFIG / CONSTANTS
# -------------------------------------------------------
size_of_board = 600
number_of_dots = 6
symbol_size = (size_of_board / 3 - size_of_board / 8) / 2
symbol_thickness = 50
dot_color = '#7BC043'
player1_color = '#0492CF'
player1_color_light = '#67B0CF'
player2_color = '#EE4035'
player2_color_light = '#EE7E77'
Green_color = '#7BC043'
dot_width = 0.25 * size_of_board / number_of_dots
edge_width = 0.1 * size_of_board / number_of_dots
distance_between_dots = size_of_board / number_of_dots

# -------------------------------------------------------
# Game engine (public API: GameEngine.reset_game_state, .click)
# -------------------------------------------------------
class GameEngine:
    def __init__(self, canvas):
        """
        canvas: Tkinter Canvas object from UI (GameScreen).
        """
        self.canvas = canvas

        # preserve original first-turn behaviour
        self.player1_starts = True

        # core arrays (will be reset properly in reset_game_state)
        self.board_status = np.zeros((number_of_dots - 1, number_of_dots - 1))
        self.row_status = np.zeros((number_of_dots, number_of_dots - 1))
        self.col_status = np.zeros((number_of_dots - 1, number_of_dots))

        # state flags
        self.pointsScored = False
        self.reset_board = False
        self.turntext_handle = None
        self.already_marked_boxes = []

        # draw initial static grid/dots
        self.refresh_board()

    # -----------------------
    # Public reset function used by UI
    # -----------------------
    def reset_game_state(self):
        """
        Reset the logical game state and redraw board grid/dots.
        Called by GameScreen.load().
        """
        # Clear only dynamic items (edges/boxes/turn), keep grid/dots redrawn
        self.canvas.delete("edge")
        self.canvas.delete("box")
        self.canvas.delete("turn")

        # redraw grid/dots (they will be redrawn and kept above edges/boxes)
        self.refresh_board()

        self.board_status = np.zeros(shape=(number_of_dots - 1, number_of_dots - 1))
        self.row_status = np.zeros(shape=(number_of_dots, number_of_dots - 1))
        self.col_status = np.zeros(shape=(number_of_dots - 1, number_of_dots))

        self.pointsScored = False

        # toggle starting player (original behaviour)
        self.player1_starts = not self.player1_starts
        self.player1_turn = not self.player1_starts

        self.reset_board = False
        self.turntext_handle = None
        self.already_marked_boxes = []

        # draw turn text
        self.display_turn_text()

    # -----------------------
    # Core game logic (kept similar to original)
    # -----------------------
    def is_grid_occupied(self, logical_position, type):
        r = logical_position[0]
        c = logical_position[1]
        occupied = True

        if type == 'row' and self.row_status[c][r] == 0:
            occupied = False
        if type == 'col' and self.col_status[c][r] == 0:
            occupied = False

        return occupied

    def convert_grid_to_logical_position(self, grid_position):
        grid_position = np.array(grid_position)
        position = (grid_position - distance_between_dots / 4) // (distance_between_dots / 2)

        type = False
        logical_position = []

        if position[1] % 2 == 0 and (position[0] - 1) % 2 == 0:
            # horizontal edge
            r = int((position[0] - 1) // 2)
            c = int(position[1] // 2)
            logical_position = [r, c]
            type = 'row'
        elif position[0] % 2 == 0 and (position[1] - 1) % 2 == 0:
            # vertical edge
            c = int((position[1] - 1) // 2)
            r = int(position[0] // 2)
            logical_position = [r, c]
            type = 'col'

        return logical_position, type

    def pointScored(self):
        self.pointsScored = True

    def mark_box(self):
        # Player 1 boxes (-4)
        boxes = np.argwhere(self.board_status == -4)
        for box in boxes:
            if list(box) not in self.already_marked_boxes and list(box) != []:
                self.already_marked_boxes.append(list(box))
                self.shade_box(box, player1_color_light)

        # Player 2 boxes (4)
        boxes = np.argwhere(self.board_status == 4)
        for box in boxes:
            if list(box) not in self.already_marked_boxes and list(box) != []:
                self.already_marked_boxes.append(list(box))
                self.shade_box(box, player2_color_light)

    def update_board(self, type, logical_position):
        r = logical_position[0]
        c = logical_position[1]
        val = 1
        playerModifier = -1 if self.player1_turn else 1

        if c < (number_of_dots - 1) and r < (number_of_dots - 1):
            self.board_status[c][r] = (abs(self.board_status[c][r]) + val) * playerModifier
            if abs(self.board_status[c][r]) == 4:
                self.pointScored()

        if type == 'row':
            self.row_status[c][r] = 1
            if c >= 1:
                self.board_status[c - 1][r] = (abs(self.board_status[c - 1][r]) + val) * playerModifier
                if abs(self.board_status[c - 1][r]) == 4:
                    self.pointScored()
        elif type == 'col':
            self.col_status[c][r] = 1
            if r >= 1:
                self.board_status[c][r - 1] = (abs(self.board_status[c][r - 1]) + val) * playerModifier
                if abs(self.board_status[c][r - 1]) == 4:
                    self.pointScored()

    def is_gameover(self):
        return (self.row_status == 1).all() and (self.col_status == 1).all()

    # -----------------------
    # Drawing functions (layer-safe)
    # -----------------------
    def refresh_board(self):
        # Remove only grid/dot layers (so edges/boxes persist until cleared explicitly)
        try:
            self.canvas.delete("grid")
            self.canvas.delete("dot")
        except:
            pass

        # Draw dashed grid lines (tagged)
        for i in range(number_of_dots):
            x = i * distance_between_dots + distance_between_dots / 2
            self.canvas.create_line(
                x, distance_between_dots / 2,
                x, size_of_board - distance_between_dots / 2,
                fill='gray', dash=(2, 2), tags=("grid",)
            )
            self.canvas.create_line(
                distance_between_dots / 2, x,
                size_of_board - distance_between_dots / 2, x,
                fill='gray', dash=(2, 2), tags=("grid",)
            )

        # Draw dots (tagged "dot")
        for i in range(number_of_dots):
            for j in range(number_of_dots):
                cx = i * distance_between_dots + distance_between_dots / 2
                cy = j * distance_between_dots + distance_between_dots / 2
                self.canvas.create_oval(
                    cx - dot_width / 2, cy - dot_width / 2,
                    cx + dot_width / 2, cy + dot_width / 2,
                    fill=dot_color, outline=dot_color, tags=("dot",)
                )

        # Make sure dots are above edges and boxes
        self.canvas.tag_raise("dot")

    def make_edge(self, type, logical_position):
        if type == 'row':
            start_x = distance_between_dots / 2 + logical_position[0] * distance_between_dots
            end_x = start_x + distance_between_dots
            start_y = distance_between_dots / 2 + logical_position[1] * distance_between_dots
            end_y = start_y
        else:
            start_y = distance_between_dots / 2 + logical_position[1] * distance_between_dots
            end_y = start_y + distance_between_dots
            start_x = distance_between_dots / 2 + logical_position[0] * distance_between_dots
            end_x = start_x

        color = player1_color if self.player1_turn else player2_color

        # Draw the edge and tag it
        self.canvas.create_line(
            start_x, start_y, end_x, end_y,
            fill=color, width=edge_width, tags=("edge",)
        )

        # Ensure edges are below dots
        self.canvas.tag_lower("edge", "dot")

    def shade_box(self, box, color):
        start_x = distance_between_dots / 2 + box[1] * distance_between_dots + edge_width / 2
        start_y = distance_between_dots / 2 + box[0] * distance_between_dots + edge_width / 2
        end_x = start_x + distance_between_dots - edge_width
        end_y = start_y + distance_between_dots - edge_width

        self.canvas.create_rectangle(
            start_x, start_y, end_x, end_y,
            fill=color, outline='', tags=("box",)
        )

        # Ensure boxes are below dots
        self.canvas.tag_lower("box", "dot")

    def display_turn_text(self):
        text = 'Next turn: '
        if getattr(self, 'player1_turn', False):
            text += 'Player1'
            color = player1_color
        else:
            text += 'Player2'
            color = player2_color

        # remove old turn text if present
        try:
            if self.turntext_handle:
                self.canvas.delete(self.turntext_handle)
        except:
            pass

        self.turntext_handle = self.canvas.create_text(
            size_of_board - 5 * len(text),
            size_of_board - distance_between_dots / 8,
            font="cmr 15 bold", text=text, fill=color,
            tags=("turn",)
        )

        # Turn text should not cover dots; keep it below dots
        self.canvas.tag_raise("turn")
        self.canvas.tag_lower("turn", "dot")

    # -----------------------
    # Click handler — returns result text when game ends
    # -----------------------
    def click(self, event):
        if not getattr(self, "reset_board", False):
            grid_position = [event.x, event.y]
            logical_position, valid_input = self.convert_grid_to_logical_position(grid_position)

            if valid_input and not self.is_grid_occupied(logical_position, valid_input):
                self.update_board(valid_input, logical_position)
                self.make_edge(valid_input, logical_position)
                self.mark_box()
                # redraw grid/dots layer (without removing edges/boxes)
                self.refresh_board()

                # change turn if no point scored
                self.player1_turn = (not self.player1_turn) if not self.pointsScored else self.player1_turn
                self.pointsScored = False

                if self.is_gameover():
                    # produce a result string (used by UI)
                    player1_score = len(np.argwhere(self.board_status == -4))
                    player2_score = len(np.argwhere(self.board_status == 4))

                    if player1_score > player2_score:
                        result_text = "Winner: Player 1"
                    elif player2_score > player1_score:
                        result_text = "Winner: Player 2"
                    else:
                        result_text = "It's a tie"

                    # display gameover screen on canvas itself as well
                    self.canvas.delete("all")
                    self.canvas.create_text(size_of_board / 2, size_of_board / 3,
                                            font="cmr 60 bold", fill=player1_color if player1_score > player2_score else player2_color,
                                            text=result_text)
                    score_text = f'Player 1 : {player1_score}\nPlayer 2 : {player2_score}\n'
                    self.canvas.create_text(size_of_board / 2, 3 * size_of_board / 4,
                                            font="cmr 30 bold", fill=Green_color, text=score_text)
                    self.canvas.create_text(size_of_board / 2, 15 * size_of_board / 16,
                                            font="cmr 20 bold", fill="gray", text='Click to play again')

                    # set reset flag so next click restarts
                    self.reset_board = True

                    # return result text so UI can navigate to result screen if desired
                    return result_text
                else:
                    self.display_turn_text()
        else:
            # after gameover: click to play again
            self.canvas.delete("all")
            self.reset_game_state()
            self.reset_board = False

        # default: no game-over yet
        return None

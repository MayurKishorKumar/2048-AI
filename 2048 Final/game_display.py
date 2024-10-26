from tkinter import Frame, Label, CENTER

import game_ai
import game_functions

EDGE_LENGTH = 400
CELL_COUNT = 4
CELL_PAD = 10

UP_KEY = "'w'"
DOWN_KEY = "'s'"
LEFT_KEY = "'a'"
RIGHT_KEY = "'d'"
AI_KEY = "'r'"
AI_PLAY_KEY = "' '"

LABEL_FONT = ("Comic Sans", 60, "bold")

GAME_COLOR = "#000000"

EMPTY_COLOR = "#858585"

TILE_COLORS = {2: "#ffffff", 4: "#ffefef", 8: "#ffbebe", 16: "#ff9d9d",
               32: "#f78787", 64: "#ff7878", 128: "#ff6060",
               256: "#fb3c3c", 512: "#ff2d2d", 1024: "#fd1f1f",
               2048: "#Ff0000", 4096: "#000000", 8192: "#000000", }

LABEL_COLORS = {2: "#011c08", 4: "#011c08", 8: "#011c08", 16: "#011c08",
                32: "#011c08", 64: "#f2f2f0", 128: "#f2f2f0",
                256: "#f2f2f0", 512: "#f2f2f0", 1024: "#f2f2f0",
                2048: "#f2f2f0", 4096: "#f2f2f0", 8192: "#f2f2f0", }


class Display(Frame):
    def __init__(self):
        Frame.__init__(self)

        self.grid()
        self.master.title('2048')
        self.master.bind("<Key>", self.key_press)

        self.commands = {UP_KEY: game_functions.move_up,
                         DOWN_KEY: game_functions.move_down,
                         LEFT_KEY: game_functions.move_left,
                         RIGHT_KEY: game_functions.move_right,
                         AI_KEY: game_ai.ai_move,
                         }

        self.grid_cells = []
        self.build_grid()
        self.init_matrix()
        self.draw_grid_cells()
        self.score = 0

        self.mainloop()

    def build_grid(self):
        background = Frame(self, bg=GAME_COLOR,
                           width=EDGE_LENGTH, height=EDGE_LENGTH)
        background.grid()

        for row in range(CELL_COUNT):
            grid_row = []
            for col in range(CELL_COUNT):
                cell = Frame(background, bg=EMPTY_COLOR,
                             width=EDGE_LENGTH / CELL_COUNT,
                             height=EDGE_LENGTH / CELL_COUNT)
                cell.grid(row=row, column=col, padx=CELL_PAD,
                          pady=CELL_PAD)
                t = Label(master=cell, text="",
                          bg=EMPTY_COLOR,
                          justify=CENTER, font=LABEL_FONT, width=5, height=2)
                t.grid()
                grid_row.append(t)

            self.grid_cells.append(grid_row)

    def init_matrix(self):
        self.matrix = game_functions.initialize_game()

    def draw_grid_cells(self):
        for row in range(CELL_COUNT):
            for col in range(CELL_COUNT):
                tile_value = self.matrix[row][col]
                if not tile_value:
                    self.grid_cells[row][col].configure(
                        text="", bg=EMPTY_COLOR)
                else:
                    self.grid_cells[row][col].configure(text=str(
                        tile_value), bg=TILE_COLORS[tile_value],
                        fg=LABEL_COLORS[tile_value])
        self.update_idletasks()

    def key_press(self, event):
        valid_game = True
        key = repr(event.char)
        print(self.score)
        if key == AI_PLAY_KEY:
            move_count = 0
            while valid_game:
                self.matrix, valid_game, score = game_ai.ai_move(self.matrix, 40, 30)
                self.score += score
                if valid_game:
                    self.matrix = game_functions.add_new_tile(self.matrix)
                    self.draw_grid_cells()
                move_count += 1
        if key == AI_KEY:
            self.matrix, move_made, score = game_ai.ai_move(self.matrix, 20, 30)
            self.score += score
            if move_made:
                self.matrix = game_functions.add_new_tile(self.matrix)
                self.draw_grid_cells()
                move_made = False

        elif key in self.commands:
            self.matrix, move_made, _ = self.commands[repr(event.char)](self.matrix)
            if move_made:
                self.matrix = game_functions.add_new_tile(self.matrix)
                self.draw_grid_cells()
                move_made = False


gamegrid = Display()
while True:
    print(gamegrid.score)

# 4x4 grid
import random

COLORS = {"blue": "🟦", "red": "🟥", "green": "🟩", "yellow": "🟨", "purple": "🟪"}


class FaceGrid:
    def __init__(self, size=4):
        self.x = size
        self.y = size
        self.grid = [[0 for _ in range(size)] for _ in range(size)]

    def draw_grid(self):
        print("drawing the grid")
        for i in self.grid:
            for j in i:
                print(j, end="")
            print()

    def populate_grid(self):
        for row_num, row in enumerate(self.grid):
            for col_num, col in enumerate(row):
                random_key = random.choice(list(COLORS.keys()))
                self.grid[row_num][col_num] = COLORS[random_key]

    def set_grid(self, new_x, new_y, new_color):
        assert new_color in COLORS, "invalid color entered"
        self.grid[new_y][new_x] = COLORS[new_color]

    def check_rows(self):
        # check rows
        # isolate per row
        def check_row(row: list):
            for i in range(len(row) - 1):
                if row[i] == row[i + 1]:
                    continue
                else:
                    return False
            return True

        row_matching_dict = {}
        for i, row in enumerate(self.grid):
            row_matching = check_row(row)
            row_matching_dict[i] = row_matching
        return row_matching_dict

    def check_cols(self):

        def check_col(j):
            for i in range(len(self.grid) - 1):
                if self.grid[i][j] == self.grid[i + 1][j]:
                    continue
                else:
                    return False
            return True

        col_matching_dict = {}
        for j in range(len(self.grid[0])):
            col_matching = check_col(j)
            col_matching_dict[j] = col_matching
        return col_matching_dict

    def check_rowsandcols(self):
        return (self.check_rows(), self.check_cols())


def main():
    grid = FaceGrid(5)
    grid.populate_grid()
    grid.draw_grid()

    print(grid.check_rows())
    print(grid.check_cols())

    # done = False
    # while not done:
    #     grid.populate_grid()
    #     grid.draw_grid()
    #     d = grid.check_rows()
    #     print(d)
    #     if True in d.values():
    #         done = True

    done2 = False
    truedict = {0: True, 1: False, 2: False, 3: True}
    while not done2:
        grid.populate_grid()
        grid.draw_grid()
        row_dict = grid.check_rows()
        col_dict = grid.check_cols()

        print(row_dict, col_dict)

        if True in row_dict.values() or True in col_dict.values():
            done2 = True


main()

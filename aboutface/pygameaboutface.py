# 4x4 grid
import random

COLORS = {"blue": "🟦", "red": "🟥", "green": "🟩", "yellow": "🟨", "purple": "🟪"}


class FaceGrid:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.grid = [[0 for _ in range(self.x)] for _ in range(self.y)]

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
        def check_row_segment(k):
            for j in range(k, k + 3):
                if self.grid[i][j] == self.grid[i][j + 1]:
                    continue
                else:
                    return False
            return True

        def check_row(i):
            _tuple = []
            for k in range(self.x - 3):
                _tuple.append(check_row_segment(k))
            return _tuple

        row_matching_dict = {}
        for i in range(len(self.grid)):
            row_matching_dict[i] = check_row(i)
        return row_matching_dict

    def check_cols(self):

        def check_col_segment(k):
            for i in range(k, k + 3):
                if self.grid[i][j] == self.grid[i + 1][j]:
                    continue
                else:
                    return False
            return True

        def check_col(j):
            _tuple = []
            for k in range(self.y - 3):
                _tuple.append(check_col_segment(k))
            return _tuple

        col_matching_dict = {}
        for j in range(len(self.grid[0])):
            col_matching_dict[j] = check_col(j)
        return col_matching_dict

    def check_rowsandcols(self):
        return (self.check_rows(), self.check_cols())


def main():
    grid = FaceGrid(5, 5)
    grid.populate_grid()

    grid.draw_grid()

    # done = False
    # while not done:
    #     grid.populate_grid()
    #     grid.draw_grid()
    #     d = grid.check_rows()
    #     print(d)
    #     if True in d.values():
    #         done = True

    for i in range(4):
        grid.set_grid(1, i + 1, "red")

    grid.draw_grid()

    print(grid.check_rows())
    print(grid.check_cols())

    done2 = False
    # while not done2:
    #     grid.populate_grid()
    #     grid.draw_grid()
    #     row_dict = grid.check_rows()
    #     col_dict = grid.check_cols()

    #     print(row_dict, col_dict)

    #     if [False, True] in row_dict.values() or True in col_dict.values():
    #         done2 = True


main()

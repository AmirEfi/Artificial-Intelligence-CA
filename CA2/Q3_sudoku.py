import pygame

WIDTH = 550
background_color = (251, 247, 245)
original_grid_element_color = (52, 31, 151)
maxNums = 9      # we have 9 numbers (1,2,3,...,8,9)

grid = [
    [7, 8, 0, 4, 0, 0, 1, 2, 0],
    [6, 0, 0, 0, 7, 5, 0, 0, 9],
    [0, 0, 0, 6, 0, 1, 0, 7, 8],
    [0, 0, 7, 0, 4, 0, 2, 6, 0],
    [0, 0, 1, 0, 5, 0, 9, 3, 0],
    [9, 0, 4, 0, 6, 0, 0, 0, 5],
    [0, 7, 0, 3, 0, 0, 0, 1, 2],
    [1, 2, 0, 0, 0, 7, 4, 0, 0],
    [0, 4, 9, 2, 0, 6, 0, 0, 7]
]


def escape():
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            return


def DrawGrid():
    win = pygame.display.set_mode((WIDTH, WIDTH))
    win.fill(background_color)
    my_font = pygame.font.SysFont('Comic Sans MS', 35)

    for i in range(0, 9):
        for j in range(0, 9):
            if grid[i][j] != 0:
                value = my_font.render(str(grid[i][j]), True, original_grid_element_color)
                win.blit(value, ((j + 1) * 50 + 15, (i + 1) * 50))

    pygame.display.update()

    for i in range(0, 10):
        if i % 3 == 0:
            pygame.draw.line(win, (0, 0, 0), (50 + 50 * i, 50), (50 + 50 * i, 500), 6)
            pygame.draw.line(win, (0, 0, 0), (50, 50 + 50 * i), (500, 50 + 50 * i), 6)

        pygame.draw.line(win, (0, 0, 0), (50 + 50 * i, 50), (50 + 50 * i, 500), 2)
        pygame.draw.line(win, (0, 0, 0), (50, 50 + 50 * i), (500, 50 + 50 * i), 2)
    pygame.display.update()


def is_valid(row, col, num):
    for j in range(maxNums):     # check if the num is in the row
        if grid[row][j] == num:
            return False

    for i in range(maxNums):     # check if the num is in the column
        if grid[i][col] == num:
            return False

    if row % 3 != 0:             # find the row of the square
        remainder = row % 3
        row -= remainder

    if col % 3 != 0:             # find the column of the square
        remainder = col % 3
        col -= remainder

    square = maxNums // 3
    for i in range(square):      # check if the num is in the square
        for j in range(square):
            if grid[i + row][j + col] == num:
                return False
    return True


def solver(row, col):
    if row == maxNums - 1 and col == maxNums:
        return True
    if col == maxNums:
        row += 1
        col = 0
    if grid[row][col] > 0:
        return solver(row, col + 1)        # this place has value so go to next column

    for num in range(1, maxNums + 1):      # put 1 to the place that has no value, if it wasn't OK then put 2 then 3 and so on to 9
        if is_valid(row, col, num):        # check if the num is valid in that place or not
            grid[row][col] = num
            if solver(row, col + 1):
                return True
        grid[row][col] = 0                 # if it wasn't OK at any numbers, put 0 again in that place

    return False


def main():
    pygame.font.init()
    win = pygame.display.set_mode((WIDTH, WIDTH))
    pygame.display.set_caption("CH02")
    win.fill(background_color)

    solver(0, 0)  # my solver algorithm that starts from row and column 0

    DrawGrid()
    while True:
        escape()


main()
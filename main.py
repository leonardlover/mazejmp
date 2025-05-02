# Author: LELE
# Main file, contains game loop
# Execute as: python3 main.py <input_file_path>

import copy
import sys

import pygame
from pygame.locals import *

from parser import parse_input
from renderer import create_buttons, render_menu, render_maze
from search import dfs, bfs, ucs

# Game constants
WIDTH = 1000
HEIGHT = 618
FPS = 60

TITLE_MARGIN = 8

FONT_FAMILY = "optima"
BIG_FONT_SIZE = 48
SMALL_FONT_SIZE = 36

BACKGROUND_COLOR = "purple"
BUTTON_COLOR = pygame.Color(200, 200, 200)
FONT_COLOR = pygame.Color("black")

if __name__ == "__main__":
    # Check that file was included as command line argument
    # If more args are introduced, they are ignored
    if len(sys.argv) == 1:
        raise FileNotFoundError("no input file was introduced")

    # Read mazes and check there are some
    input_data = parse_input(sys.argv[1])

    maze_count = len(input_data)
    if maze_count == 0:
        raise ValueError("input file did not contain any mazes")

    # Initialize pygame, screen, clock and font
    pygame.init()

    window = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    big_font = pygame.font.SysFont(FONT_FAMILY, BIG_FONT_SIZE)
    small_font = pygame.font.SysFont(FONT_FAMILY, SMALL_FONT_SIZE)

    # Create text surfaces and button rectangles
    buttons = create_buttons(big_font, FONT_COLOR, WIDTH, HEIGHT)

    left_button = buttons[0][1]
    right_button = buttons[1][1]
    dfs_button = buttons[2][1]
    bfs_button = buttons[3][1]
    ucs_button = buttons[4][1]

    # This is the currently selected maze
    maze_index = 0
    selected_search = None

    # Compute solutions and print min path length to screen
    # Solutions is a list of quadruples of the best path by every search method:
    # (length, dfs_path, bfs_path, ucs_path)
    # length: integer representing length of min path, or -1 if there is none,
    # [dfs, bfs, ucs]_path: list of pairs (x, y) of
    # the cell jumps in order start -> target
    solutions = []
    for i, maze in enumerate(input_data):
        dfs_path = dfs(
            window,
            BACKGROUND_COLOR,
            buttons[2:],
            BUTTON_COLOR,
            big_font,
            small_font,
            FONT_COLOR,
            i,
            copy.deepcopy(maze),
            WIDTH,
            HEIGHT,
            TITLE_MARGIN,
            render=False
        )

        bfs_path = bfs(
            window,
            BACKGROUND_COLOR,
            buttons[2:],
            BUTTON_COLOR,
            big_font,
            small_font,
            FONT_COLOR,
            i,
            copy.deepcopy(maze),
            WIDTH,
            HEIGHT,
            TITLE_MARGIN,
            render=False
        )

        ucs_path = ucs(
            window,
            BACKGROUND_COLOR,
            buttons[2:],
            BUTTON_COLOR,
            big_font,
            small_font,
            FONT_COLOR,
            i,
            copy.deepcopy(maze),
            WIDTH,
            HEIGHT,
            TITLE_MARGIN,
            render=False
        )

        # Check that all paths are of minimum length
        assert(len(dfs_path) == len(bfs_path) and len(bfs_path) == len(ucs_path))

        length = len(dfs_path) - 1
        solutions.append((length, dfs_path, bfs_path, ucs_path))

        if length >= 0:
            print(length)
        else:
            print("No solution found")

    # Mark cells in a minimum path for future display
    # This list contains triples (dfs_grid, bfs_grid, ucs_grid)
    # Cells in path are marked as 'at-goal' and all other cells as None
    best_path_grids = []
    for maze, path in zip(input_data, solutions):
        header = maze[0]
        m, n, sx, sy, tx, ty = header

        length, dfs_path, bfs_path, ucs_path = path

        dfs_grid = [[None for _ in range(n)] for _ in range(m)]
        bfs_grid = [[None for _ in range(n)] for _ in range(m)]
        ucs_grid = [[None for _ in range(n)] for _ in range(m)]

        # Mark path
        for i, j in dfs_path:
            dfs_grid[i][j] = "at-goal"
        for i, j in bfs_path:
            bfs_grid[i][j] = "at-goal"
        for i, j in ucs_path:
            ucs_grid[i][j] = "at-goal"

        # Mark start and end
        dfs_grid[sx][sy] = "start"
        dfs_grid[tx][ty] = "target"
        bfs_grid[sx][sy] = "start"
        bfs_grid[tx][ty] = "target"
        ucs_grid[sx][sy] = "start"
        ucs_grid[tx][ty] = "target"

        # Correct for start = target
        if sx == tx and sy == ty:
            dfs_grid[sx][sy] = "at-goal"
            bfs_grid[sx][sy] = "at-goal"
            ucs_grid[sx][sy] = "at-goal"

        best_path_grids.append((dfs_grid, bfs_grid, ucs_grid))

    # Game loop
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()

                # Change current maze
                if left_button.collidepoint(pos):
                    maze_index += maze_count - 1
                    maze_index %= maze_count

                    selected_search = None
                if right_button.collidepoint(pos):
                    maze_index += maze_count + 1
                    maze_index %= maze_count

                    selected_search = None

                # Run selected algorithm
                if dfs_button.collidepoint(pos):
                    selected_search = "DFS"
                    _ = dfs(
                        window,
                        BACKGROUND_COLOR,
                        buttons[2:],
                        BUTTON_COLOR,
                        big_font,
                        small_font,
                        FONT_COLOR,
                        maze_index,
                        copy.deepcopy(input_data[maze_index]),
                        WIDTH,
                        HEIGHT,
                        TITLE_MARGIN
                    )
                if bfs_button.collidepoint(pos):
                    selected_search = "BFS"
                    _ = bfs(
                        window,
                        BACKGROUND_COLOR,
                        buttons[2:],
                        BUTTON_COLOR,
                        big_font,
                        small_font,
                        FONT_COLOR,
                        maze_index,
                        copy.deepcopy(input_data[maze_index]),
                        WIDTH,
                        HEIGHT,
                        TITLE_MARGIN
                    )
                if ucs_button.collidepoint(pos):
                    selected_search = "UCS"
                    _ = ucs(
                        window,
                        BACKGROUND_COLOR,
                        buttons[2:],
                        BUTTON_COLOR,
                        big_font,
                        small_font,
                        FONT_COLOR,
                        maze_index,
                        copy.deepcopy(input_data[maze_index]),
                        WIDTH,
                        HEIGHT,
                        TITLE_MARGIN
                    )

        # Fill screen to not get clipping
        window.fill(BACKGROUND_COLOR)

        # Draw menu
        render_menu(
            window,
            BACKGROUND_COLOR,
            buttons,
            BUTTON_COLOR,
            big_font,
            FONT_COLOR,
            maze_index,
            WIDTH,
            HEIGHT,
            TITLE_MARGIN
        )

        # Draw plain maze if no search is selected
        # or grid with best path marked, and min path length
        if selected_search is None:
            render_maze(window, small_font, FONT_COLOR, input_data[maze_index])
        else:
            header, grid, cell_type = input_data[maze_index]

            # Retrieve and display best path
            if selected_search == "DFS":
                render_maze(window, small_font, FONT_COLOR, (header, grid, best_path_grids[maze_index][0]))
            if selected_search == "BFS":
                render_maze(window, small_font, FONT_COLOR, (header, grid, best_path_grids[maze_index][1]))
            if selected_search == "UCS":
                render_maze(window, small_font, FONT_COLOR, (header, grid, best_path_grids[maze_index][2]))

        pygame.display.flip()
        clock.tick(FPS)

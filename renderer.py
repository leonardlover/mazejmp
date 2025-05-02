# Author: LELE
# Utility funcions to render buttons, the menu, and mazes

import pygame

# Constants used for scaling that look pretty
GOLDEN = 1.618
SILVER = 1.5

def create_buttons(font, font_color, width, height):
    """Creates text and buttons used in menus.

    Return a list of pairs (text, button) where text is a pygame.Surface
    of rendered text that should appear over button, a pygame.Rect.

    Buttons are: left, right, dfs, bfs, ucs.
    """

    left_text = font.render("<", True, font_color)
    right_text = font.render(">", True, font_color)
    dfs_text = font.render("DFS", True, font_color)
    bfs_text = font.render("BFS", True, font_color)
    ucs_text = font.render("UCS", True, font_color)

    left_button_width = int(GOLDEN * left_text.get_width())
    right_button_width = int(GOLDEN * right_text.get_width())
    dfs_button_width = int(SILVER * dfs_text.get_width())
    bfs_button_width = int(SILVER * bfs_text.get_width())
    ucs_button_width = int(SILVER * ucs_text.get_width())

    button_margin = (width - left_button_width - right_button_width \
        - dfs_button_width - bfs_button_width - ucs_button_width) // 4

    left_button = pygame.Rect(
        0,
        0,
        left_button_width,
        height
    )

    right_button = pygame.Rect(
        int(width - GOLDEN * right_text.get_width()),
        0,
        right_button_width,
        height
    )

    dfs_button = pygame.Rect(
        left_button_width + button_margin,
        height - int(GOLDEN * dfs_text.get_height()),
        dfs_button_width,
        int(SILVER * dfs_text.get_height())
    )

    bfs_button = pygame.Rect(
        left_button_width + dfs_button_width + 2 * button_margin,
        height - int(GOLDEN * bfs_text.get_height()),
        bfs_button_width,
        int(SILVER * bfs_text.get_height())
    )

    ucs_button = pygame.Rect(
        left_button_width + dfs_button_width + bfs_button_width + 3 * button_margin,
        height - int(GOLDEN * ucs_text.get_height()),
        ucs_button_width,
        int(SILVER * ucs_text.get_height())
    )

    return [
        (left_text, left_button),
        (right_text, right_button),
        (dfs_text, dfs_button),
        (bfs_text, bfs_button),
        (ucs_text, ucs_button),
    ]

def render_rect(window, color, text, rect):
    """Renders text over a rect.

    Inputs:
    window: game window,
    color: background color of buttons,
    text: a pygame.Surface of text to be rendered over button,
    rect: a pygame.Rect.
    """

    pygame.draw.rect(window, color, rect)
    window.blit(
        text,
        (
            rect.left + (rect.width - text.get_width()) // 2,
            rect.top + (rect.height - text.get_height()) // 2,
        )
    )

def render_buttons(window, color, assets):
    """Renders a list of buttons.

    Inputs:
    window: game window,
    color: background color of buttons,
    assets: list of pairs (text, button). Here text is a pygame.Surface
    that is supposed to be text rendered over button, a pygame.Rect.
    """

    for text, button in assets:
        render_rect(window, color, text, button)

def render_menu(window, background_color, buttons, button_color, big_font, font_color, maze_index, width, height, title_margin):
    # Draw buttons
    render_buttons(window, button_color, buttons)

    # Draw maze number on top of window
    maze_title = big_font.render(f"Maze {maze_index + 1}", True, font_color)
    window.blit(maze_title, ((width- maze_title.get_width()) / 2, title_margin))

def render_maze(window, font, font_color, maze):
    """Renders a maze on the middle of the window.

    Inputs:
    window: game window,
    font: font to render jump lengths,
    font_color: font color,
    maze: a triple (header, grid, cell_type) as elements
    of the list returned by parser.parse_input.

    Note: works well only up to jump sizes < 100
    and reasonable maze dimensions.
    """

    CELL_COLOR = pygame.Color(234, 234, 234)
    START_COLOR = pygame.Color(12, 234, 12)
    TARGET_COLOR = pygame.Color(234, 12, 12)
    AT_GOAL_COLOR = pygame.Color(234, 234, 12)

    GENERATED_COLOR = pygame.Color(12, 12, 123)
    VISITED_COLOR = pygame.Color(12, 12, 234)

    width = window.get_width()
    height = window.get_height()

    digits = [font.render(str(i), True, font_color) for i in range(10)]

    cell_margin = 2
    cell_padding = 3

    cell_size = cell_padding + max(
        max([s.get_width() for s in digits]),
        max([s.get_height() for s in digits])
    )

    cell_shift = cell_size + cell_margin

    header, grid, cell_type = maze
    m, n, sx, sy, tx, ty = header

    at_goal = (sx == tx and sy == ty)

    maze_width = n * cell_size + (n - 1) * cell_margin
    maze_height = m * cell_size + (m - 1) * cell_margin

    for i in range(m):
        for j in range(n):
            rect = pygame.Rect(
                (width - maze_width) // 2 + j * cell_shift,
                (height - maze_height) / 2 + i * cell_shift,
                cell_size,
                cell_size
            )

            cell_text = font.render(str(grid[i][j]), True, font_color)

            if cell_type[i][j] == "at-goal":
                render_rect(window, AT_GOAL_COLOR, cell_text, rect)
            elif cell_type[i][j] == "start":
                render_rect(window, START_COLOR, cell_text, rect)
            elif cell_type[i][j] == "target":
                render_rect(window, TARGET_COLOR, cell_text, rect)
            elif cell_type[i][j] == "generated":
                render_rect(window, GENERATED_COLOR, cell_text, rect)
            elif cell_type[i][j] == "visited":
                render_rect(window, VISITED_COLOR, cell_text, rect)
            else:
                render_rect(window, CELL_COLOR, cell_text, rect)

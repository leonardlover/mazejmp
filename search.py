# Author: LELE
# Includes implementations of maze search methods
# These are: DFS, BFS and UCS

from collections import deque
import heapq
import sys
import time

import pygame
from pygame.locals import *

from renderer import render_menu, render_maze

# Search rendering constants
UPDATES_PER_SECOND = 4

def initial_render(window, background_color, buttons, button_color, big_font, font_color, maze_index, width, height, title_margin):
    """Performs initial rendering after calling a search method."""

    # Fill screen to not get clipping
    window.fill(background_color)

    # Draw menu
    render_menu(
        window,
        background_color,
        buttons,
        button_color,
        big_font,
        font_color,
        maze_index,
        width,
        height,
        title_margin
    )

def render_cycle(window, small_font, font_color, header, grid, cell_type):
    """Call to render maze grid during a search."""

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
            
    # Draw maze
    render_maze(window, small_font, font_color, (header, grid, cell_type))

    # Update display
    pygame.display.flip()
    # I'm not using pygame.Clock just for simplicity
    time.sleep(1 / UPDATES_PER_SECOND)

def reconstruct_path(parent, tx, ty):
    """Reconstructs path from start to target."""

    path = [(tx, ty)]

    i, j = tx, ty
    while parent[i][j] != (-1, -1):
        path.append(parent[i][j])
        i, j = parent[i][j]

    # Reverse path to get order from start to target
    return path[::-1]

def dfs(window, background_color, buttons, button_color, big_font, small_font, font_color, maze_index, maze, width, height, title_margin, render=True):
    """Perform DFS on a maze, also visualize it.

    Will display maze grid on window coloring cells as follows:
    White: cells not yet generated,
    Green: start cell,
    Red: target cell,
    Dark blue: generated cell not yet fully visited,
    Blue: visited cell,
    Yellow: cell is start and target at the same time.

    Inputs:
    window: game screen,
    background_color: a pygame.Color for background color,
    buttons: list of (text, button) to render menu,
    big_font: font for menu,
    small_font: font for cell jump sizes,
    maze_index: index of currently selected maze,
    maze: (header, grid, cell_type) of currently selected maze,
    width: window width,
    height: window height,
    title_margin: margin of maze title,
    render: bool indicating if we're rendering or just searching.

    Output:
    path: a list of shortest path from source to target.
    This is an empty list if there is no such path.
    """

    # Perform initial render
    if render:
        initial_render(
            window,
            background_color,
            buttons,
            button_color,
            big_font,
            font_color,
            maze_index,
            width,
            height,
            title_margin
        )

    header, grid, cell_type = maze
    m, n, sx, sy, tx, ty = header

    # Orthogonal directions to move from current state
    deltas = [(1, 0), (0, -1), (-1, 0), (0, 1)]

    # Grid of DFS parent, (-1, -1) means node is either
    # source or that is was not visited
    parent = [[(-1, -1) for _ in range(n)] for _ in range(m)]

    # Grid of depth in DFS search tree
    # Used to find right parent in a shortest path
    # Again, -1 means that node was not visited
    depth = [[-1 for _ in range(n)] for _ in range(m)]

    # Exit early if start = target
    if cell_type[sx][sy] == "at-goal":
        return [(sx, sy)]

    # Start at (sx, sy) and add to stack to do DFS
    stack = [(sx, sy)]
    cell_type[sx][sy] = "generated"
    depth[sx][sy] = 0

    while len(stack) > 0:
        # Rendering stuff
        if render:
            render_cycle(
                window,
                small_font,
                font_color,
                header,
                grid,
                cell_type
            )

        # Expand top state of stack
        i, j = stack[-1]
        stack.pop()

        for di, dj in deltas:
            ii = i + di * grid[i][j]
            jj = j + dj * grid[i][j]

            # Out of bounds
            if ii < 0 or ii >= m or jj < 0 or jj >= n:
                continue

            # If child not visited nor generated, generate it.
            # Must also do this for target, since to get a shortest path
            # we must first finish the entire DFS to figure out this path.
            # If child has already been generated, find out if this new path
            # is one of shorter length, in that case, update parent and depth.
            # Unfortunately we must also do this for visited states, in the case
            # that a shorter path exists, we must traverse it again to update
            # the depth of its children.
            if cell_type[ii][jj] is None or cell_type[ii][jj] == "target":
                stack.append((ii, jj))
                parent[ii][jj] = (i, j)
                depth[ii][jj] = depth[i][j] + 1
                cell_type[ii][jj] = "generated"
            elif cell_type[ii][jj] == "generated":
                if depth[ii][jj] > depth[i][j] + 1:
                    parent[ii][jj] = (i, j)
                    depth[ii][jj] = depth[i][j] + 1
            else:
                if depth[ii][jj] > depth[i][j] + 1:
                    stack.append((ii, jj))
                    parent[ii][jj] = (i, j)
                    depth[ii][jj] = depth[i][j] + 1
                    cell_type[ii][jj] = "generated"

        # Mark current node as visited
        cell_type[i][j] = "visited"

    # Check if target was visited, if not return empty path
    if cell_type[tx][ty] != "visited":
        return []

    return reconstruct_path(parent, tx, ty)

def bfs(window, background_color, buttons, button_color, big_font, small_font, font_color, maze_index, maze, width, height, title_margin, render=True):
    """Perform BFS on a maze, also visualize it.

    Will display maze grid on window coloring cells as follows:
    White: cells not yet generated,
    Green: start cell,
    Red: target cell,
    Dark blue: generated cell not yet fully visited,
    Blue: visited cell.

    Inputs:
    window: game screen,
    background_color: a pygame.Color for background color,
    buttons: list of (text, button) to render menu,
    big_font: font for menu,
    small_font: font for cell jump sizes,
    maze_index: index of currently selected maze,
    maze: (header, grid, cell_type) of currently selected maze,
    width: window width,
    height: window height,
    title_margin: margin of maze title,
    render: bool indicating if we're rendering or just searching.

    Output:
    path: a list of shortest path from source to target.
    This is an empty list if there is no such path.
    """

    # Perform initial render
    if render:
        initial_render(
            window,
            background_color,
            buttons,
            button_color,
            big_font,
            font_color,
            maze_index,
            width,
            height,
            title_margin
        )

    header, grid, cell_type = maze
    m, n, sx, sy, tx, ty = header

    # Orthogonal directions to move from current state
    deltas = [(1, 0), (0, -1), (-1, 0), (0, 1)]

    # Grid of BFS parent, (-1, -1) means node is either
    # source or that is was not visited
    parent = [[(-1, -1) for _ in range(n)] for _ in range(m)]

    # Exit early if start = target
    if cell_type[sx][sy] == "at-goal":
        return [(sx, sy)]

    # Start at (sx, sy) and add to queue to do BFS
    # Here a deque is used since Python does not have a strict queue
    # (at least not for this use case)
    # Elements will be pushed to the queue from
    # the left and popped through the right
    queue = deque([(sx, sy)])
    cell_type[sx][sy] = "generated"

    while len(queue) > 0:
        # Rendering stuff
        if render:
            render_cycle(
                window,
                small_font,
                font_color,
                header,
                grid,
                cell_type
            )

        # Expand front state of queue
        i, j = queue.pop()

        for di, dj in deltas:
            ii = i + di * grid[i][j]
            jj = j + dj * grid[i][j]

            # Out of bounds
            if ii < 0 or ii >= m or jj < 0 or jj >= n:
                continue

            # If child is target, exit early since a shortest path has been found
            if cell_type[ii][jj] == "target":
                # Mark parent of target as current state
                parent[ii][jj] = (i, j)

                return reconstruct_path(parent, tx, ty)

            # If child not visited nor generated, generate it.
            if cell_type[ii][jj] is None:
                queue.appendleft((ii, jj))
                parent[ii][jj] = (i, j)
                cell_type[ii][jj] = "generated"

        # Mark current node as visited
        cell_type[i][j] = "visited"

    # If this point is reached, it means that target was never reached
    # This is checked by the following assertion
    assert(parent[tx][ty] == (-1, -1))

    # Now an empty path must be returned
    return []

def ucs(window, background_color, buttons, button_color, big_font, small_font, font_color, maze_index, maze, width, height, title_margin, render=True):
    """Perform UCS on a maze, also visualize it.

    Will display maze grid on window coloring cells as follows:
    White: cells not yet generated,
    Green: start cell,
    Red: target cell,
    Dark blue: generated cell not yet fully visited,
    Blue: visited cell.

    Inputs:
    window: game screen,
    background_color: a pygame.Color for background color,
    buttons: list of (text, button) to render menu,
    big_font: font for menu,
    small_font: font for cell jump sizes,
    maze_index: index of currently selected maze,
    maze: (header, grid, cell_type) of currently selected maze,
    width: window width,
    height: window height,
    title_margin: margin of maze title,
    render: bool indicating if we're rendering or just searching.

    Output:
    path: a list of shortest path from source to target.
    This is an empty list if there is no such path.
    """

    # Perform initial render
    if render:
        initial_render(
            window,
            background_color,
            buttons,
            button_color,
            big_font,
            font_color,
            maze_index,
            width,
            height,
            title_margin
        )

    header, grid, cell_type = maze
    m, n, sx, sy, tx, ty = header

    # Orthogonal directions to move from current state
    deltas = [(1, 0), (0, -1), (-1, 0), (0, 1)]

    # Grid of UCS parent, (-1, -1) means node is either
    # source or that is was not visited
    parent = [[(-1, -1) for _ in range(n)] for _ in range(m)]

    # Grid of shortest distances from start, -1 means that
    # cell is not reachable from it
    distance = [[-1 for _ in range(n)] for _ in range(m)]

    # Exit early if start = target
    if cell_type[sx][sy] == "at-goal":
        return [(sx, sy)]

    # Start at (sx, sy) and add to priority queue to do UCS.
    # Idea is to retrieve element of least path cost, so we must order
    # entries of the queue by path cost (this is good since Python's
    # heapq is a min heap by default), now to break ties and try to
    # make less long jumps we order also by jump length.
    # So elements of heap are quadruples (path_length, jump_size, i, j)
    priority_queue = [(0, grid[sx][sy], sx, sy)]
    distance[sx][sy] = 0
    cell_type[sx][sy] = "generated"

    while len(priority_queue) > 0:
        # Retrieve generated node with min path length
        path_length, _, i, j = heapq.heappop(priority_queue)

        # Do not explore already visited states.
        # Equivalent to having removed a state with higher path length.
        # This is done before rendering to get a smoother animation.
        if cell_type[i][j] == "visited":
            continue

        # Rendering stuff
        if render:
            render_cycle(
                window,
                small_font,
                font_color,
                header,
                grid,
                cell_type
            )

        # Exit early if the state we're visiting is the target
        if i == tx and j == ty:
            return reconstruct_path(parent, tx, ty)

        for di, dj in deltas:
            ii = i + di * grid[i][j]
            jj = j + dj * grid[i][j]

            # Out of bounds
            if ii < 0 or ii >= m or jj < 0 or jj >= n:
                continue

            # If child not visited nor generated, generate it.
            # If child was already generated, we must check if a better
            # path length exists with this path. If so, remove it from heap
            # and add it again with new min-so-far path length.
            # Since this is very expensive, what we'll do is just to add it
            # again to the heap with this min-so-far length, but when exploring
            # a new state we must check first if it was already visited.
            # This assures that sub-optimal paths are not considered with low overhead.
            if cell_type[ii][jj] != "visited" and cell_type[ii][jj] != "generated":
                heapq.heappush(priority_queue, (path_length + 1, grid[ii][jj], ii, jj))
                parent[ii][jj] = (i, j)
                distance[ii][jj] = distance[i][j] + 1
                cell_type[ii][jj] = "generated"
            elif cell_type[ii][jj] == "generated":
                if distance[ii][jj] > distance[i][j] + 1:
                    heapq.heappush(priority_queue, (path_length + 1, grid[ii][jj], ii, jj))
                    distance[ii][jj] = distance[i][j] + 1

        # Mark current node as visited
        cell_type[i][j] = "visited"

    # If this point is reached, it means that target was never reached
    # This is checked by the following assertion
    assert(parent[tx][ty] == (-1, -1))

    # Now an empty path must be returned
    return []

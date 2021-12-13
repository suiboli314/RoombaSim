import numpy as np
import unittest
from Maze import Maze
from MazeRoomGen import DungeonRooms


class GeneratorsTest(unittest.TestCase):

    def test_dungeon_rooms_grid(self):
        """ test Dungeon Rooms maze-creation mazes a reasonably sane maze """
        g = np.ones((7, 7), dtype=np.int8)
        g[1] = [1, 1, 1, 1, 1, 1, 1]
        g[2] = [1, 1, 1, 1, 1, 1, 1]
        g[3] = [1, 1, 0, 0, 0, 1, 1]
        g[4] = [1, 1, 0, 0, 0, 1, 1]
        g[5] = [1, 1, 0, 0, 0, 1, 1]

        m = Maze()
        m.generator = DungeonRooms(4, 4, grid=g)
        m.generate()

        assert boundary_is_solid(m.grid)
        assert all_passages_open(m.grid)

    def test_dungeon_reconnect_maze(self):
        """ test Dungeon Rooms maze-creation mazes a reasonably sane maze when reconnecting a maze """
        g = np.ones((7, 7), dtype=np.int8)
        g[1] = [1, 0, 0, 0, 1, 0, 1]
        g[2] = [1, 0, 1, 1, 1, 0, 1]
        g[3] = [1, 0, 0, 0, 1, 0, 1]
        g[4] = [1, 0, 0, 0, 1, 0, 1]
        g[5] = [1, 0, 0, 0, 1, 0, 1]

        m = Maze()
        m.generator = DungeonRooms(4, 4, grid=g)
        m.generator.reconnect_maze()

        assert boundary_is_solid(m.generator.grid)
        assert all_passages_open(m.generator.grid)

    def test_dungeon_rooms_random_rooms(self):
        """ test Dungeon Rooms maze-creation mazes a reasonably sane maze when generating some random rooms """
        m = Maze()
        m.generator = DungeonRooms(4, 4, rooms=[[(1, 1), (3, 3)]], hunt_order='random')
        m.generate()

        assert boundary_is_solid(m.grid)
        assert all_passages_open(m.grid)

    def test_dungeon_rooms_serpentine_rooms(self):
        """ test DungeonRooms mazes are reasonably when generating some random rooms in a serpentine fashion """
        m = Maze()
        m.generator = DungeonRooms(7, 7,
                                   rooms=[[(1, 1), (4, 3)], [(2, 6), (8, 9)], [(5, 8), (6, 13)]],
                                   hunt_order='serpentine')
        m.generate()

        assert boundary_is_solid(m.grid)
        assert all_passages_open(m.grid)
        print()
        print(m)


def boundary_is_solid(grid):
    """ Helper method to test of the maze is sane.
    Algorithms should generate a maze with a solid boundary of walls.

    Args:
        grid (np.array): maze array
    Returns:
        boolean: is the maze boundary solid?
    """
    # first row
    for c in grid[0]:
        if c == 0:
            return False

    # other rows
    for row in grid[1: -1]:
        if row[0] == 0 or row[-1] == 0:
            return False

    # last row
    for c in grid[grid.shape[0] - 1]:
        if c == 0:
            return False

    return True


def all_passages_open(grid):
    """ Helper method to test of the maze is sane
    All the (odd, odd) grid cells in a maze should be passages.

    Args:
        grid (np.array): maze array
    Returns:
        booean: Are all the odd/odd grid cells open?
    """
    H, W = grid.shape

    for r in range(1, H, 2):
        for c in range(1, W, 2):
            if grid[r, c] == 1:
                return False

    return True


def all_corners_complete(grid):
    """ Helper method to test of the maze is sane
    All the (even, even) grid cells in a maze should be walls.

    Args:
        grid (np.array): maze array
    Returns:
        boolean: Are all the grid corners solid?
    """
    H, W = grid.shape

    for r in range(2, H, 2):
        for c in range(2, W, 2):
            if grid[r, c] == 0:
                return False

    return True

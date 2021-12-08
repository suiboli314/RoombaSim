from random import randrange


class Maze:
    """
    This is a master object meant to hold a rectangular, 2D maze.
    This object includes the methods used to generate and solve the maze,
    as well as the start and end points.
    """

    def __init__(self, seed=None):
        self.generator = None
        self.grid = None
        self.start = None
        self.end = []
        # self.transmuters = []
        self.solver = None
        self.solutions = None
        self.prune = True
        Maze.set_seed(seed)

    @staticmethod
    def set_seed(seed):
        """ helper method to set the random seeds for all the random seed for all the random libraries we are using

        Args:
            seed (int): random seed number
        Returns:
            None
        """
        if seed is not None:
            import random
            random.seed(seed)
            import numpy as np
            np.random.seed(seed)

    @staticmethod
    def get_distance(cell1, cell2):
        """ Returns manhattan distances between two given cells

        Args:
            cell1 (tuple): one of two cells
            cell2 (tuple): the other cell
        Returns:
            int: manhattan distances between two cells
        """
        return abs(cell1[0] - cell2[0]) + abs(cell1[1] - cell2[1])

    def generate(self):
        """ public method to generate a new maze, and handle some clean-up

        Returns:
            None
        """
        assert not (self.generator is None), 'No maze-generation algorithm has been set.'

        self.grid = self.generator.generate()
        self.start = None
        self.end = []
        self.solutions = None

    def generate_entrances(self, no_end=3, at_least_distance=2):
        """ Generate maze entrances. Entrances can be on the walls, or inside the maze.

        Args:
            no_end (int): How many end of the maze?
            at_least_distance (int): start and end doesn't allow within this distance
        Returns:
            None
        """

        H, W = self.grid.shape

        # Generate a Start
        if not self.start:
            self.start = (randrange(1, H, at_least_distance), randrange(1, W, at_least_distance))

        # cells already used
        usedCells = set()
        usedCells.add(self.start)
        usedCells.update(self.GetNeighbours(self.start, at_least_distance))

        for i in range(no_end):
            timeout = 20
            while True:
                # Generate a end
                end = (randrange(1, H, at_least_distance), randrange(1, W, at_least_distance))
                # verify end
                if end not in usedCells:
                    # valid end, then add it and
                    # its neighbours into usedCells
                    usedCells.add(end)
                    usedCells.update(self.GetNeighbours(end, at_least_distance))
                    # add valid end to maze, break timeout loop
                    self.end.append(end)
                    break
                # timed out
                assert timeout > 0, "_generate_inner_entrances timeout"

    def solve(self):
        """ public method to solve a new maze, if possible

        Returns:
            None
        """
        assert not (self.solver is None), 'No maze-solving algorithm has been set.'
        assert not (self.start is None) and not (self.end is None), \
            'Start and end times must be set first.'

        self.solutions = self.solver.solve(self.grid, self.start, self.end)

    def tostring(self, entrances=False, solutions=False):
        """ Display the maze entrances/solutions IF they already exist.
        Return a string representation of the maze.

        Args:
            entrances (bool): Do you want to show the entrances of the maze?
            solutions (bool): Do you want to show the solution to the maze?
        Returns:
            str: string representation of the maze
        """
        if self.grid is None:
            return ''

        # build the walls of the grid
        txt = []
        for row in self.grid:
            txt.append(''.join(['#' if cell else ' ' for cell in row]))

        # if extant, insert the solution path
        if solutions and self.solutions:
            for r, c in self.solutions[0]:
                txt[r] = txt[r][:c] + '+' + txt[r][c + 1:]

        # insert the start and end points
        if entrances and self.start and self.end:
            r, c = self.start
            txt[r] = txt[r][:c] + 'S' + txt[r][c + 1:]

            for end in self.end:
                r, c = end
                txt[r] = txt[r][:c] + 'E' + txt[r][c + 1:]

        return '\n'.join(txt)

    def __str__(self):
        """ Display maze walls, entrances, and solutions, if available

        Returns:
            str: string representation of the maze
        """
        return self.tostring(True, True)

    def __repr__(self):
        """ Display maze walls, entrances, and solutions, if available

        Returns:
            str: string representation of the maze
        """
        return self.__str__()

    def GetNeighbours(self, cell, distance=1):
        """ Generate a list of valid steps in range
        of distance around the given cell

        Args:
            cell (tuple): given cell
            distance (int): distance of the given cell to the furthest cell
        Returns:
            list: valid nearby cells in range
        """
        r, c = cell
        neighbours = []
        for i in range(1, distance + 1):
            nearby = (r + i, c)
            if self.validate_step(nearby):
                neighbours.append(nearby)
            nearby = (r - i, c)
            if self.validate_step(nearby):
                neighbours.append(nearby)
            nearby = (r, c + i)
            if self.validate_step(nearby):
                neighbours.append(nearby)
            nearby = (r, c - i)
            if self.validate_step(nearby):
                neighbours.append(nearby)

        return neighbours

    def validate_cell(self, cell):
        """ Validate a given cell is inside maze
        Args:
            cell (tuple): cell
        Returns:
             bool: returns true if cell is inside maze
        """
        return 0 < cell[0] < self.grid.shape[0] and 0 < cell[1] < self.grid.shape[1]

    def validate_step(self, cell):
        """ Validate a given cell is walkable
        Args:
            cell (tuple):
        Returns:
             bool: returns true if cell is not obstacle inside maze
        """
        return self.validate_cell(cell) and not self.grid[cell[0]][cell[1]]

    # def transmute(self):
    #     """ Transmute an existing maze grid
    #
    #     Returns:
    #       None
    #     """
    #     assert not (self.grid is None), 'No maze grid yet exists to transmute.'
    #
    #     for transmuter in self.transmuters:
    #         transmuter.transmute(self.grid, self.start, self.end)

    # def generate_monte_carlo(self, repeat, entrances=3, difficulty=1.0, reducer=len):
    #     """ Use the Monte Carlo method to generate a maze of defined difficulty.
    #
    #     This method assumes the generator and solver algorithms are already set.
    #
    #     1. Generate a maze.
    #     2. For each maze, generate a series of entrances.
    #     3. To eliminate boring entrance choices, select only the entrances
    #         that yield the longest solution to a given maze.
    #     4. Repeat steps 1 through 3 for several mazes.
    #     5. Order the mazes based on a reduction function applied to their maximal
    #         solutions. By default, this reducer will return the solution length.
    #     6. Based on the 'difficulty' parameter, select one of the mazes.
    #
    #     Args:
    #         repeat (int): How many mazes do you want to generate?
    #         entrances (int): How many different entrance combinations do you want to try?
    #         difficulty (float): How difficult do you want the final maze to be (zero to one).
    #         reducer (function): How do you want to determine solution difficulty (default is length).
    #     Returns:
    #       None
    #     """
    #     assert (difficulty >= 0.0 and difficulty <= 1.0), 'Maze difficulty must be between 0 to 1.'
    #
    #     # generate different mazes
    #     mazes = []
    #     for _ in range(repeat):
    #         self.generate()
    #         this_maze = []
    #
    #         # for each maze, generate different entrances, and solve
    #         for _ in range(entrances):
    #             self.generate_entrances()
    #             self.solve()
    #             this_maze.append({'grid': self.grid,
    #                               'start': self.start,
    #                               'end': self.end,
    #                               'solutions': self.solutions})
    #
    #         # for each maze, find the longest solution
    #         mazes.append(max(this_maze, key=lambda k: len(k['solutions'])))
    #
    #     # sort the mazes by the length of their solution
    #     mazes = sorted(mazes, key=lambda k: reducer(k['solutions'][0]))
    #
    #     # based on optional parameter, choose the maze of the correct difficulty
    #     pos = int((len(mazes) - 1) * difficulty)
    #
    #     # save final results of Monte Carlo Simulations to this object
    #     self.grid = mazes[pos]['grid']
    #     self.start = mazes[pos]['start']
    #     self.end = mazes[pos]['end']
    #     self.solutions = mazes[pos]['solutions']

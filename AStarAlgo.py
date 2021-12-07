# If the code is not Cython-compiled, we need to add some imports.
from cython import compiled
import sys
from heapq import heappop, heappush, heapify

if not compiled:
    from MazeSolver import MazeSolver


class AStarAlgo(MazeSolver):
    """ The Algorithm

    1) create a solution for each starting position
    2) loop through each solution, and find the neighbors of the last element
    3) a solution reaches the end or a dead end when we mark it by appending a None.
    4) clean-up solutions

    Results

    Find all unique solutions. Works against imperfect mazes.
    """

    def _solve(self):
        """ A* search solutions to the maze

        Returns:
            list: valid maze solutions
        """
        sol = []

        tmp = self.start
        for end in self.end:
            cost, tmpSol = self._AStar(tmp, end)
            # store current end, use it as start for the next route
            tmp = end
            # increment current cost to total cost
            self.cost += cost
            # remove the end, to avoid duplicate add it again
            tmpSol.pop()
            # append current path to final solution
            sol += tmpSol

        sol.append(tmp)
        return [sol]

    def _AStar(self, start, end):
        """ A* search solutions to the maze

        Args:
            start (tuple): origin start or the last end
            end (tuple): one of self.end to reach
        Returns:
            int, list: the number of explored cells, valid maze solutions
        """
        counter = 0

        # dict: {cell, path}
        visited = {}

        # min heap of f
        # pop min for iterate
        heap = []
        heapify(heap)

        visited[start] = [start]
        heappush(heap, (AStarAlgo._get_distance(start, end),
                        start))

        while len(heap) != 0:
            counter += 1

            g, cell = heappop(heap)
            path = visited.get(cell)
            r, c = cell

            cell = (r - 1, c)
            if self._validate_next(cell, end, visited, heap, path) == 0:
                return counter, visited.get(cell)

            cell = (r + 1, c)
            if self._validate_next(cell, end, visited, heap, path) == 0:
                return counter, visited.get(cell)

            cell = (r, c - 1)
            if self._validate_next(cell, end, visited, heap, path) == 0:
                return counter, visited.get(cell)

            cell = (r, c + 1)
            if self._validate_next(cell, end, visited, heap, path) == 0:
                return counter, visited.get(cell)

    def _validate_next(self, cell, end, visited, heap, path):
        """ Verify if a given cell is valid in maze
        and if appends the cell to the path

        Args:
            cell (tuple): cell to be verified
            visited (dict): a set contains all visited cells
            path (list): a path that may reach the end
        Returns:
            None
        """
        r, c = cell
        h = sys.maxsize
        if 0 < r < self.grid.shape[0] and 0 < c < self.grid.shape[1]:
            if visited.get(cell) is None and not self.grid[r][c]:
                newPath = list(path)
                newPath.append(cell)
                visited[cell] = newPath
                g = len(newPath)
                h = AStarAlgo._get_distance(cell, end)
                f = g + h
                heappush(heap, (f, cell))
        return h

    @staticmethod
    def _get_distance(cell1, cell2):
        """ Calculate manhattan distance distance between given two cells

        Args:
            cell1 (tuple): a cell
            cell2 (tuple): a cell
        Returns:
            int: manhattan distance
        """
        return abs(cell1[0] - cell2[0]) + abs(cell1[1] - cell2[1])

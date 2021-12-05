# If the code is not Cython-compiled, we need to add some imports.
from cython import compiled
import queue

if not compiled:
    from MazeSolver import MazeSolver


class BFSAlgo(MazeSolver):
    """ The Algorithm

    1) create a solution for each starting position
    2) loop through each solution, and find the neighbors of the last element
    3) a solution reaches the end or a dead end when we mark it by appending a None.
    4) clean-up solutions

    Results

    Find all unique solutions. Works against imperfect mazes.
    """

    def _solve(self):
        """ breadth-first search solutions to the maze

        Returns:
            list: valid maze solutions

        """
        tmp = self.start
        for end in self.end:
            self._bfs_uninformed(tmp, end)
            tmp = end

    def _bfs_uninformed(self, start, end):
        """ breadth-first search solutions to the maze

        Args:
            start (tuple): origin start or the last end
            end (tuple): one of self.end to reach
        Returns:
            int, list: the number of explored cells, valid maze solutions
        """
        counter = 0

        # maintain a queue of paths
        q = queue.Queue()
        # visited cells
        visited = set()

        q.put([start])

        while len(q) != 0:
            counter += 1
            # get the first path from the queue
            path = q.get()
            # get the last node from the path
            cell = path[-1]
            # path found
            if cell == end:
                return counter, path
            # enumerate all adjacent nodes, construct a
            # new path and push it into the queue
            r, c = cell
            self._validate_next((r - 1, c), visited, q, path)
            self._validate_next((r + 1, c), visited, q, path)
            self._validate_next((r, c - 1), visited, q, path)
            self._validate_next((r, c + 1), visited, q, path)

    def _validate_next(self, cell, visited, q, path):
        """ Verify if a given cell is valid in maze
        and if appends the cell to the path

        Args:
            cell (tuple): cell to be verified
            visited (set): a set contains all visited cells
            q (queue): a queue maintains all possible paths
            path (list): a path that may reach the end
        Returns:
            None
        """
        r, c = cell
        if 0 < r < self.grid.shape[0] and 0 < c < self.grid.shape[1]:
            if cell not in visited and not self.grid[r][c]:
                visited.add(cell)
                q.put(list(path).append(cell))

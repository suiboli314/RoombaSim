# If the code is not Cython-compiled, we need to add some imports.
from cython import compiled
from collections import deque

if not compiled:
    from MazeSolver import MazeSolver


class BFSAlgo(MazeSolver):
    """ Search the shallowest nodes in the search tree first.

    Caveat: Solutions is a list but currently have only one solution.
    """
    def _solve(self):
        """ breadth-first search solutions to the maze

        Returns:
            list: valid maze solutions
        """
        sol = []

        tmp = self.start
        for end in self.end:
            cost, tmpSol = self._bfs_uninformed(tmp, end)
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
        q = deque()
        # visited cells
        visited = set()

        q.append([start])
        visited.add(start)

        while len(q) != 0:
            counter += 1
            # get first path from queue
            path = q.popleft()
            # get last node from path
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
            q (deque): a queue maintains all possible paths
            path (list): a path that may reach the end
        Returns:
            None
        """
        r, c = cell
        if 0 < r < self.grid.shape[0] and 0 < c < self.grid.shape[1]:
            if cell not in visited and not self.grid[r][c]:
                visited.add(cell)
                newPath = list(path)
                newPath.append(cell)
                q.append(newPath)

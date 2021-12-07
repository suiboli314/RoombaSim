# If the code is not Cython-compiled, we need to add some imports.
from cython import compiled
from collections import deque
from heapq import heappop, heappush, heapify

if not compiled:
    from MazeSolver import MazeSolver


class GreedyAlgo(MazeSolver):
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
        sol = []

        tmp = self.start
        heap = GreedyAlgo.UpdateHeap(tmp, self.end)

        while len(heap) != 0:
            end = heappop(heap)[1]
            cost, tmpSol = self._bfs_uninformed(tmp, end)
            # store current end, use it as start for the next route
            tmp = end
            # increment current cost to total cost
            self.cost += cost
            # remove the end, to avoid duplicate add it again
            tmpSol.pop()
            # append current path to final solution
            sol += tmpSol

            # Todo replace heap(update heap value each loop) with findMin

        sol.append(tmp)
        return [sol]

    @staticmethod
    def UpdateHeap(start, ends):
        """
        Args:
            start (tuple): start cell to calculate distance
            ends (list): list of ends
        Return:
            heap: heapified list
        """
        heap = []
        heapify(heap)
        for end in ends:
            node = (GreedyAlgo._get_distance(start, end), end)
            heappush(heap, node)

        return heap

    @staticmethod
    def _get_distance(cell1, cell2):
        """ Calculate manhattan distance distance between given two cells

        Args:
            cell1 (tuple): a cell
            cell2 (tuple): a cell
        Returns:
            int: manhattan distance
        """
        return abs(cell1[0] - cell2[0]) + abs(cell1[1]-cell2[1])

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

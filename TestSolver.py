import unittest
from enum import Enum
from MazeRoomGen import DungeonRooms
from Maze import Maze
from BFSAlgo import BFSAlgo
from DFSAlgo import DFSAlgo
from GreedyAlgo import GreedyAlgo
from AStarAlgo import AStarAlgo


class Algo(Enum):
    BFS = 1
    DFS = 2
    Greedy = 3
    Astar = 4


class TestSolver(unittest.TestCase):

    @staticmethod
    def duplicates_in_solution(solution):
        """ No cell should appear twice in the same maze solution.

        Args:
            solution (list): path from start to finish
        Returns:
            bool: Does the same cell appear in the solution more than once?
        """
        for i in range(len(solution[:-1])):
            if solution[i] in solution[i + 1:]:
                return True
        return False

    @staticmethod
    def one_away(cell1, cell2):
        """ Is one cell exactly one move from another?

        Args:
            cell1 (tuple): Maze position to compare
            cell2 (tuple): Maze position to compare
        Returns:
            bool: As the two cells next to each other?
        """
        r1, c1 = cell1
        r2, c2 = cell2

        if r1 == r2 and abs(c1 - c2) == 1:
            return True
        elif c1 == c2 and abs(r1 - r2) == 1:
            return True

        return False

    @staticmethod
    def solution_is_sane(solution):
        """ verify that each cell in a solution path is next to the previous cell

        Args:
            solution (list): path from start to finish
        Returns:
            bool: Does the solution seem sane and feasible?
        """
        assert len(solution) > 0

        for i in range(1, len(solution)):
            if not TestSolver.one_away(solution[i - 1], solution[i]):
                print("\n{}\nsolution prev {}, curr {}: {}".format(solution, solution[i - 1], i, solution[i]))
                return False

        return True

    @staticmethod
    def create_maze_with_varied_goals(no_end=3):
        """ Create a maze with entrances inside/outside

        Args:
            no_end (int): How many end of the maze?
        Returns:
            Maze: a small, test maze grid with entrance and exit initialized
        """
        m = Maze()
        m.generator = DungeonRooms(7, 7,
                                   rooms=[[(1, 1), (4, 3)], [(2, 6), (6, 8)], [(5, 8), (6, 13)]],
                                   hunt_order='serpentine')
        m.generate()
        m.generate_entrances(no_end)

        return m

    @staticmethod
    def _solve(maze, algo):
        """ Solve maze with given algorithm, and validate solutions
        Args:
            maze (Maze): maze with solution to be validated and printed
            algo (Algo): Algorithm to solve maze
        Returns:
             None
        """
        if algo == Algo.BFS:
            maze.solver = BFSAlgo()
        elif algo == Algo.DFS:
            maze.solver = DFSAlgo()
        elif algo == Algo.Greedy:
            maze.solver = GreedyAlgo()
        elif algo == Algo.Astar:
            maze.solver = AStarAlgo()

        maze.solve()
        TestSolver.validate(maze)

    @staticmethod
    def validate(maze):
        """ verify solutions of given maze
        Args:
            maze (Maze): maze with solution to be validated
        Returns:
             None
        """
        for sol in maze.solutions:
            assert TestSolver.one_away(maze.start, sol[1])
            assert TestSolver.solution_is_sane(sol)

    @staticmethod
    def print_maze_solution(maze, algo):
        """ verify solutions of given maze and print maze with first solution
        Args:
            maze (Maze): maze with solution to be validated and printed
            algo (Algo): Algorithm used for solutions
        Returns:
             None
        """
        print("\n{}\n1st sol efficiency: {}\nsols: {}\nsteps in algorithm: {}\n{}"
              .format(algo, len(maze.solutions[0]), maze.solutions, maze.solver.cost, maze))

    @staticmethod
    def test_BFS():
        """ Test BFS """
        m = TestSolver.create_maze_with_varied_goals(3)
        TestSolver._solve(m, Algo.BFS)
        TestSolver.print_maze_solution(m, Algo.BFS)

    @staticmethod
    def test_DFS():
        """ Test DFS """
        m = TestSolver.create_maze_with_varied_goals(3)
        TestSolver._solve(m, Algo.DFS)
        TestSolver.print_maze_solution(m, Algo.DFS)

    @staticmethod
    def test_Greedy():
        """ Test Greedy """
        m = TestSolver.create_maze_with_varied_goals(3)
        TestSolver._solve(m, Algo.Greedy)
        TestSolver.print_maze_solution(m, Algo.Greedy)

    @staticmethod
    def test_AStar():
        """ Test A* """
        m = TestSolver.create_maze_with_varied_goals(3)
        TestSolver._solve(m, Algo.Astar)
        TestSolver.print_maze_solution(m, Algo.Astar)

    @staticmethod
    def test_a_maze_print():
        """ Test a maze throughout BFS, DFS, Greedy, and A*, and print result"""
        m = TestSolver.create_maze_with_varied_goals(4)

        for algo in Algo:
            TestSolver._solve(m, algo)
            TestSolver.print_maze_solution(m, algo)
            m.solutions = []

    @staticmethod
    def test_a_maze():
        """ Test a maze throughout BFS, DFS, Greedy, and A*

        Returns:
            list: list of efficiency of each algorithm solution
        """
        m = TestSolver.create_maze_with_varied_goals(4)
        cost = []

        for algo in Algo:
            TestSolver._solve(m, algo)
            cost.append(len(m.solutions[0]))
            m.solutions = []

        return cost

    @staticmethod
    def test_benchmark(no_of_test=30):
        """ Test mazes throughout BFS, DFS, Greedy, and A*
         for a given number of time

        Args:
            no_of_test (int): number of test to be done in benchmark
        Returns:
            list: table of efficiency of each algorithm solution
        """
        costTable = []

        while no_of_test != 0:
            costTable.append(TestSolver.test_a_maze())
            no_of_test -= 1

        print()
        for row in costTable:
            print(row)

        return costTable


if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)

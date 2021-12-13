""" Inspired from code sample provided by Wu, Jingjing """
import matplotlib.pyplot as plt
import pandas as pd
from TestSolver import TestSolver


def draw_graph(no_of_tests=5):
    """ Run TestSolver and benchmark efficiency of solution
    among algorithms. Plot graph based on the result.

    Args:
        no_of_tests (int): number of tests to be done for a graph, default is 5
    Returns:
        None
    """
    result = TestSolver.test_benchmark(no_of_tests)
    df = pd.DataFrame(result,
                      index=["Maze {}".format(i + 1) for i in range(len(result))],
                      columns=["BFS", "DFS", 'Greedy', "A*"])

    print(df)

    # Transpose dataframe to print properly
    df.T.plot(kind='bar', stacked=False,
              title='Benchmark')
    plt.show()


if __name__ == '__main__':
    draw_graph()

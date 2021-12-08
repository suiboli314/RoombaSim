import matplotlib.pyplot as plt
import pandas as pd
from TestSolver import TestSolver


def draw_graph():
    result = TestSolver.test_benchmark(5)
    df = pd.DataFrame(result,
                      index=["Maze {}".format(i + 1) for i in range(len(result))],
                      columns=["BFS", "DFS", 'Greedy', "A*"])

    print(df)
    df.T.plot(kind='bar', stacked=False,
              title='Benchmark')

    plt.show()


if __name__ == '__main__':
    draw_graph()

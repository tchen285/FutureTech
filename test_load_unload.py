from collections import deque
import copy
from os.path import join, expanduser


class FindLoadUnloadPath:
    def __init__(self, matrix):
        self.start_matrix_tuple = tuple(map(tuple, matrix))
        self.cols = len(matrix[0])
        self.rows = len(matrix)
        self.queue = deque()
        self.queue.append(matrix)
        self.visited = set()  # Initialize the visited set
        matrix_tuple = tuple(map(tuple, matrix))
        self.visited.add(matrix_tuple)
        self.matrix_parent = {tuple(map(tuple, matrix)): None}
        self.move_descriptions = []
        self.total_cost = 0
        self.goal_matrix_tuple = None
        self.idle_starts = []
        self.idle_matrix_tuple = []
        self.idle_ends = []
        self.idle_descriptions = []
        self.unload_set = set()  # store the container coordinates that need to unload
        self.unload_descriptions = []

        # self.unload_set.add((1, 0))
        # self.unload_set.add((1, 1))
        # self.unload_set.add((1, 3))
        # self.unload_set.add((1, 2))

        # self.unload_set.add((6, 3))
        self.unload_set.add((0, 0))
        self.unload_set.add((1, 0))
        self.unload_set.add((1, 1))

        self.unload_sequence = []  # store the unload sequence

    def solve_load_unload(self):
        while self.queue and len(self.unload_set) != 0:
            level_size = len(self.queue)
            for _ in range(level_size):
                popped_matrix = self.queue.popleft()
                print("\n$$$$$新pop出来的矩阵:", popped_matrix)  # 可以正常输出矩阵, 无限循环

                for col in range(self.cols):
                    if popped_matrix[-1][col] == 0 or (popped_matrix[-1][col] is None and any(
                            popped_matrix[i][col] == 0 for i in range(self.rows - 1, -1, -1))):
                        continue

                    current_matrix = copy.deepcopy(popped_matrix)
                    if self.solve_current_column(current_matrix, popped_matrix, col):
                        break

        print(self.unload_sequence)
        print(self.unload_set)
        # print(self.queue)

    def solve_current_column(self, matrix, original_matrix, col):
        for row1 in range(self.rows):
            # 这里打印两次是因为, 最上面是0, 然后下一次在输出同样的内容才是非0
            print("\n*****打印当前矩阵: ", matrix)
            print("打印正在处理的column:", col)
            print("%%%%打印当前matrix的parent: ", self.matrix_parent[tuple(map(tuple, matrix))])
            if (row1, col) in self.unload_set:
                # print("打印当前matrix的parent:", self.matrix_parent[tuple(tuple(row) for row in matrix_copy)])
                print("找到一个目标点")
                self.unload_sequence.append((row1, col))
                self.unload_set.remove((row1, col))
                matrix[row1][col] = 0
                matrix_tuple = tuple(tuple(row) for row in matrix)

                self.matrix_parent[matrix_tuple] = tuple(map(tuple, original_matrix))
                self.visited.add(matrix_tuple)
                self.queue.clear()
                self.queue.append(copy.deepcopy(matrix))
                # 后续这里要增加距离, 目前只是看能不能把sequence输出来
                # if len(self.unload_set) == 0:
                #     return True
                return True
            if matrix[row1][col] != 0 and matrix[row1][col] != None:
                print("进入正常的span Tree")
                weight = matrix[row1][col]
                matrix[row1][col] = 0

                for col2 in range(self.cols):
                    if col2 == col:
                        continue
                    for row2 in reversed(range(self.rows)):
                        if matrix[row2][col2] != 0:
                            continue
                        if matrix[row2][col2] == 0:
                            matrix[row2][col2] = weight
                            if tuple(map(tuple, matrix)) in self.visited:
                                matrix[row2][col2] = 0
                                break

                            self.matrix_parent[tuple(map(tuple, matrix))] = tuple(map(tuple, original_matrix))

                            matrix_tuple = tuple(tuple(row) for row in matrix)

                            self.visited.add(matrix_tuple)
                            self.queue.append(copy.deepcopy(matrix))
                            matrix[row2][col2] = 0
                            break  # Exit the inner loop
        return False


def main():
    # matrix = [
    #     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #     [0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0],
    #     [0, 0, 0, 6, 4, 0, 0, 0, 0, 0, 0, 0],
    #     [None, 8, 9, None, 10, 11, 0, 0, 0, 0, 0, 0]
    # ]
    # matrix = [
    #
    #     [0, 0, 0, 0, 0, 0],
    #     [0, 0, 0, 2, 0, 0],
    #     [0, 0, 0, 6, 4, 0],
    #     [None, 8, 9, None, 10, 11]
    # ]

    matrix = [
        [4, 0, 0, 0],
        [6, 10, 0, 0]
    ]

    # matrix = [ # passed time cost test,
    #     [0, 0, 0, 6],
    #     [None, 10, 4, None]
    # ]

    # matrix = [ # passed time cost test,
    #     [0, 0, 3, 1],
    #     [5, 9, 1, 1]
    # ]

    # ShipCase 1 ---- Regular Balance ------ Unload 99 only
    # matrix = [
    #     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #     [None, 99, 100, 0, 0, 0, 0, 0, 0, 0, 0, None]
    # ]

    # ShipCase 2 ------Regular Balance ------- Load a new container 431 weight only
    # matrix = [
    #     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #     [40, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #     [None, 50, 0, 0, 0, 0, 0, 0, 0, 0, 0, None],
    #     [None, None, None, 120, 0, 0, 0, 0, 35, None, None, None]
    # ]

    # ShipCase 3 ------ Balance ------- Unload 500, and load 532 and 6317
    # matrix = [
    #     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #     [9041, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #     [10001, 500, 600, 100, 0, 0, 0, 0, 0, 0, 0, 0]
    # ]

    # ShipCase 4 ------- Balance ------ Unload 1100, load 2543
    # matrix = [
    #     [0, 0, 0, 0, 3044, 0, 0, 0, 0, 0, 0, 0],
    #     [0, 0, 0, 0, 1100, 0, 0, 0, 0, 0, 0, 0],
    #     [0, 0, 0, 0, 2020, 0, 0, 0, 0, 0, 0, 0],
    #     [0, 0, 0, 0, 10000, 0, 0, 0, 0, 0, 0, 0],
    #     [0, 0, 0, 0, 2011, 0, 0, 0, 0, 0, 0, 0],
    #     [0, 0, 0, 0, 2007, 0, 0, 0, 0, 0, 0, 0],
    #     [None, 0, 0, 0, 2000, 0, 0, 0, 0, 0, 0, None],
    #     [None, None, None, None, None, None, None, None, None, None, None, None]
    # ]

    # ShipCase 5 ------- Balance
    # Unload right 4 and unload left 4, and input for comment for left 4, load 153 and 2321
    # matrix = [
    #     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #     [None, 96, 8, 4, 4, 1, 0, 0, 0, 0, 0, None]
    # ]

    load_unload_path_finder = FindLoadUnloadPath(matrix)
    load_unload_path_finder.solve_load_unload()


if __name__ == "__main__":
    main()

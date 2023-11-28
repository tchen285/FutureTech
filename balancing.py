import queue
from collections import deque
import copy
import sys

class FindBalancingPath:
    def __init__(self, matrix):
        self.matrix = matrix
        self.cols = len(matrix[0])
        self.rows = len(matrix)
        self.queue = deque()
        # self.queue.append((matrix, []))  # 每个节点保存当前矩阵和移动的路径
        self.queue.append(matrix)
        self.visited = set()  # Initialize the visited set
        self.matrix_parent = {}
        self.matrix_coordinates = {} # 以self.matrix_coordinates[matrix] = (col, row1)形式存放.
        self.matrix_parent[tuple(map(tuple, matrix))] = None
        # for col in range(self.cols):
        #     for row in range(self.rows):
        #         if self.matrix[row][col] != 0:
        #             self.matrix_coordinates[tuple(map(tuple, matrix))] = (col, row)
        #         break
        #     break
        self.level = 0

    def solve_balancing(self):
        while self.queue:
            level_size = len(self.queue)
            self.level += 1
            # 查看visited内容
            print("Visited Elements:")
            for visited_elem in self.visited:
                print(visited_elem)
                print()


            for _ in range(level_size):
                popped_matrix = self.queue.popleft()
                # 输出根矩阵的父节点, 是None
                print("$$$$\n打印根节点矩阵以及根节点的父节点")
                print(tuple(map(tuple, popped_matrix))) # 目前输出正确
                print(self.matrix_parent[tuple(map(tuple, popped_matrix))]) # 目前输出正确
                print("$$$$")

                if self.is_balanced(popped_matrix):
                    print("\n\nFOUND SOLUTION!!!\n\n")
                    for row in popped_matrix:
                        print(row)
                    print(self.level)
                    sys.exit()  # End the entire program

                matrix_tuple = tuple(tuple(row) for row in popped_matrix)
                if matrix_tuple in self.visited:
                    continue
                # self.visited.add(matrix_tuple)

                for col in range(self.cols):
                    if popped_matrix[-1][col] == 0:
                        continue

                    current_matrix = copy.deepcopy(popped_matrix)
                    self.solve_current_column(current_matrix, popped_matrix, col)

                print("Queue Size:", len(self.queue))
                print("Queue Elements:")
                for elem in self.queue:
                    print(elem)
                    print()


    def solve_current_column(self, matrix, original_matrix, col):
        for row1 in range(self.rows):
            if matrix[row1][col] != 0:
                weight = matrix[row1][col]
                self.matrix_coordinates[tuple(map(tuple, matrix))] = (col, row1)
                print("$$$$first weight's start coordinate: (col, row)")
                print(self.matrix_coordinates[tuple(map(tuple, matrix))]) # 目前输出正确
                print("$$$$")

                print("Original Matrix:")
                print(original_matrix)
                print("Current Matrix:")
                print(matrix)

                print("!!!ROW:")
                print(row1)
                print("!!!COLUMN:")
                print(col)
                print("!!! WEIGHT:")
                print(weight)

                matrix[row1][col] = 0

                for col2 in range(self.cols):
                    if col2 == col:
                        continue
                    for row2 in reversed(range(self.rows)):
                        if matrix[0][col2] != 0:
                            continue
                        if matrix[row2][col2] == 0:
                            matrix[row2][col2] = weight
                            self.matrix_coordinates[tuple(map(tuple, matrix))] = (col2, row2)
                            print("$$$$\n应该会按照顺序输出(1, 0), (2, 1), (3, 1)")
                            print(self.matrix_coordinates[tuple(map(tuple, matrix))]) # 目前输出正确
                            self.matrix_parent[tuple(map(tuple, matrix))] = tuple(map(tuple, original_matrix))
                            print("应该会按顺序输出根节点下面的三个矩阵")
                            print(matrix) # 目前输出正确
                            print("应该都输出根矩阵((6, 0, 0, 0), (10, 4, 0, 0))")
                            print(self.matrix_parent[tuple(map(tuple, matrix))]) # 目前输出正确
                            print("测试再往上走一层, 测试根节点对应的坐标, 下面是根节点的父节点")
                            pa = self.matrix_parent[tuple(map(tuple, matrix))]
                            print(self.matrix_coordinates[tuple(map(tuple, pa))]) # 目前输出正确
                            print(self.matrix_parent[tuple(map(tuple, pa))]) # 目前输出正确
                            # test = ((0, 6, 0, 0), (10, 4, 0, 0))
                            # print(self.matrix_parent[test])
                            print("$$$$")

                            print("\n--------------")
                            print(matrix[0])
                            print(matrix[1])
                            print("--------------")

                            if self.is_balanced(matrix):
                                for row in matrix:
                                    print(row)
                                print(self.level)
                                # 打印result的父矩阵
                                print(self.matrix_parent[tuple(map(tuple, matrix))]) # 到目前为止是对的
                                # 打印result对应的坐标, 也就是箱子移动到的位置(col, row)
                                print(self.matrix_coordinates[tuple(map(tuple, matrix))]) # 到目前为止是对的
                                # new_matrix是result的父矩阵
                                new_matrix = self.matrix_parent[tuple(map(tuple, matrix))]
                                print(new_matrix)
                                print(self.matrix_coordinates[new_matrix])
                                print(self.matrix_parent[new_matrix])
                                # test_matrix = ((0, 6, 0, 0), (10, 4, 0, 0))
                                # print(self.matrix_parent[test_matrix])
                                # print(self.matrix_parent[tuple(map(tuple, new_matrix))])
                                print("哈哈哈哈")
                                current = tuple(map(tuple, matrix))
                                print(current)
                                while current:
                                    # print(self.matrix_coordinates[current])
                                    print(self.matrix_parent[current])
                                    current = self.matrix_parent[current]
                                sys.exit()  # End the entire program

                            matrix_tuple = tuple(tuple(row) for row in matrix)
                            if matrix_tuple in self.visited:
                                continue

                            self.visited.add(matrix_tuple)

                            self.queue.append(copy.deepcopy(matrix))

                            print("Queue Size:", len(self.queue))
                            print("Queue Elements:")
                            for elem in self.queue:
                                print(elem)
                                print()

                            matrix[row2][col2] = 0
                            break  # Exit the inner loop

                break  # Exit the outer loop

    def is_balanced(self, matrix):
        left_sum = sum(matrix[i][j] for i in range(self.rows) for j in range(self.cols // 2))
        right_sum = sum(matrix[i][j] for i in range(self.rows) for j in range(self.cols // 2, self.cols))
        print("\n\nFOUND SOLUTION!!!")
        print("计算左右的值")
        print(left_sum)
        print(right_sum)
        balancing_score = min(left_sum, right_sum) / max(left_sum, right_sum)
        print(balancing_score)
        threshold = 0.9  # Adjust this threshold as needed

        return balancing_score > threshold


def main():
    # matrix = [
    #     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    #     [1, 0, 0, 0, 0, 0, 0, 0, 0, 10],
    #     [25, 30, 20, 20, 0, 0, 15, 10, 101, 50],
    #     [101, 101, 5, 101, 25, 20, 51, 101, 101, 29]
    # ]

    # matrix = [
    #     [3, 3, 0, 0],
    #     [10, 4, 0, 0]
    # ]

    # matrix = [
    #     [0, 0, 0, 0],
    #     [10, 2, 14, 2]
    # ]

    matrix = [
        [6, 0, 0, 0],
        [10, 4, 0, 0]
    ]

    balancing_path_finder = FindBalancingPath(matrix)
    balancing_path_finder.solve_balancing()

if __name__ == "__main__":
    main()
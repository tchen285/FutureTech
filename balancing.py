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
                if self.is_balanced(popped_matrix):
                    print("\n\nFOUND SOLUTION!!!\n\n")
                    for row in popped_matrix:
                        print(row)
                    print(self.level)
                    sys.exit()  # End the entire program
                matrix_tuple = tuple(tuple(row) for row in popped_matrix)
                if matrix_tuple in self.visited:
                    continue
                self.visited.add(matrix_tuple)

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
                print(matrix)

                for col2 in range(self.cols):
                    if col2 == col:
                        continue
                    for row2 in reversed(range(self.rows)):
                        if matrix[0][col2] != 0:
                            continue
                        if matrix[row2][col2] == 0:
                            matrix[row2][col2] = weight

                            print("\n--------------")
                            print(matrix[0])
                            print(matrix[1])
                            print("--------------")

                            if self.is_balanced(matrix):
                                print("\n\nFOUND SOLUTION!!!\n\n")
                                for row in matrix:
                                    print(row)
                                print(self.level)
                                sys.exit()  # End the entire program

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
    matrix = [
        [6, 0, 0, 0],
        [10, 4, 0, 0]
    ]

    balancing_path_finder = FindBalancingPath(matrix)
    balancing_path_finder.solve_balancing()

if __name__ == "__main__":
    main()

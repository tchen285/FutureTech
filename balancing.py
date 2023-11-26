import queue
from collections import deque
import copy

class FindBalancingPath:
    def __init__(self, matrix):
        self.matrix = matrix
        self.cols = len(matrix[0])
        self.rows = len(matrix)
        self.queue = deque()
        # self.queue.append((matrix, []))  # 每个节点保存当前矩阵和移动的路径
        self.queue.append(matrix)
        self.visited = set()  # Initialize the visited set

    def solve_balancing(self):
        while self.queue:
            level_size = len(self.queue)
            for _ in range(level_size):
                popped_matrix = self.queue.popleft()
                current_matrix = [row[:] for row in popped_matrix]

                matrix_tuple = tuple(tuple(row) for row in current_matrix)
                if matrix_tuple in self.visited:
                    continue
                self.visited.add(matrix_tuple)
                # self.solve_current_column(current_matrix, popped_matrix, 0)
                for col in range(self.cols):
                    if current_matrix[-1][col] == 0:
                        continue
                    self.solve_current_column(current_matrix, popped_matrix, col)
                    current_matrix = [row[:] for row in popped_matrix]

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
                                print("FOUND SOLUTION!!!\n\n")

                            matrix_tuple = tuple(tuple(row) for row in matrix)
                            if matrix_tuple in self.visited:
                                continue

                            self.visited.add(matrix_tuple)
                            # Append a copy of the matrix to the queue
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

        # print("Left Sum:", left_sum)
        # print("Right Sum:", right_sum)

        balancing_score = min(left_sum, right_sum) / max(left_sum, right_sum)
        return balancing_score > 0.9

    def make_move(self, matrix, row, col, move_row, move_col):
        new_matrix = [row[:] for row in matrix]  # 创建矩阵的副本，以防修改原始矩阵

        if 0 <= row + move_row < self.rows and 0 <= col + move_col < self.cols:
            new_matrix[row][col], new_matrix[row + move_row][col + move_col] = new_matrix[row + move_row][
                col + move_col], new_matrix[row][col]
            return new_matrix
        else:
            return None


def main():
    # matrix = [
    #     [6, 0, 0, 0],
    #     [10, 4, 0, 0]
    # ]
    matrix = [
        [6, 0, 0, 0],
        [10, 4, 0, 0]
    ]

    balancing_path_finder = FindBalancingPath(matrix)
    balancing_path_finder.solve_balancing()

if __name__ == "__main__":
    main()

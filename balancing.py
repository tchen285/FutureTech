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
            popped_matrix = self.queue.popleft()
            current_matrix = popped_matrix

            matrix_tuple = tuple(tuple(row) for row in current_matrix)
            if matrix_tuple in self.visited:
                continue
            self.visited.add(matrix_tuple)

            for col1 in range(self.cols):
                if current_matrix[-1][col1] == 0:
                    continue
                for row1 in range(self.rows):
                    if current_matrix[row1][col1] != 0:
                        weight = current_matrix[row1][col1]
                        current_matrix[row1][col1] = 0
                        for col2 in range(self.cols):
                            for row2 in reversed(range(self.rows)):
                                if current_matrix[row2][col2] == 0 and col2 != col1:
                                    current_matrix[row2][col2] = weight
                                    print("\n--------------")
                                    print(current_matrix[0])
                                    print(current_matrix[1])
                                    print("--------------\n")
                                    matrix_tuple = tuple(tuple(row) for row in current_matrix)
                                    if matrix_tuple in self.visited:
                                        continue
                                    self.visited.add(matrix_tuple)

                                    # Append a copy of the matrix to the queue
                                    self.queue.append(copy.deepcopy(current_matrix))

                                    print("Queue Size:", len(self.queue))
                                    print("Queue Elements:")
                                    for elem in self.queue:
                                        print(elem)

                                    current_matrix[row2][col2] = 0
                                    break  # 只跳出当前循环


    def is_balanced(self, matrix):
        left_sum = sum(matrix[i][j] for i in range(self.rows) for j in range(self.cols // 2))
        right_sum = sum(matrix[i][j] for i in range(self.rows) for j in range(self.cols // 2, self.cols))

        print("Left Sum:", left_sum)
        print("Right Sum:", right_sum)

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
    matrix = [
        [6, 0, 0, 0],
        [10, 4, 0, 0]
    ]

    balancing_path_finder = FindBalancingPath(matrix)
    balancing_path_finder.solve_balancing()

if __name__ == "__main__":
    main()

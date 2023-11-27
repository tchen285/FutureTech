import copy
import sys
from collections import deque

class FindBalancingPath:
    def __init__(self, matrix):
        self.matrix = matrix
        self.cols = len(matrix[0])
        self.rows = len(matrix)
        self.queue = deque()
        self.queue.append((matrix, None))  # (matrix, parent_matrix)) 初始化为None
        self.visited = set()  # Initialize the visited set
        self.level = 0

    def solve_balancing(self):
        while self.queue:
            level_size = len(self.queue)
            self.level += 1

            for _ in range(level_size):
                popped_matrix, parent_matrix = self.queue.popleft()

                # 检查是否初始矩阵已经balance
                if self.is_balanced(popped_matrix):
                    print("\n\nFOUND SOLUTION!!!\n\n")
                    self.print_solution(popped_matrix, parent_matrix)
                    sys.exit()  # End the entire program

                # 把当前matrix放入visited里
                matrix_tuple = tuple(tuple(row) for row in popped_matrix)
                if matrix_tuple in self.visited:
                    continue
                self.visited.add(matrix_tuple)

                # 遇到非0列, 放入solve_current_column中解决
                for col in range(self.cols):
                    if popped_matrix[-1][col] == 0:
                        continue

                    current_matrix = copy.deepcopy(popped_matrix)
                    self.solve_current_column(current_matrix, col)

                print("Queue Size:", len(self.queue))
                print("Queue Elements:")


    def solve_current_column(self, matrix, col):
        parent = copy.deepcopy(matrix)
        for row1 in range(self.rows):
            if matrix[row1][col] != 0:
                weight = matrix[row1][col]

                matrix[row1][col] = 0

                for col2 in range(self.cols):
                    if col2 == col:
                        continue
                    for row2 in reversed(range(self.rows)):
                        if matrix[row2][col2] == 0:
                            matrix[row2][col2] = weight

                            if self.is_balanced(matrix):
                                print("\n\nFOUND SOLUTION!!!\n\n")
                                self.print_solution(matrix, parent)

                                sys.exit()  # End the entire program

                            matrix_tuple = tuple(tuple(row) for row in matrix)
                            if matrix_tuple in self.visited:
                                continue
                            self.queue.append((copy.deepcopy(matrix), parent))

                            print("Queue Size:", len(self.queue))
                            print("Queue Elements:")
                            for elem, elem_path in self.queue:
                                print(elem)
                                print(elem_path)
                                print()

                            matrix[row2][col2] = 0
                            break  # Exit the inner loop

                break  # Exit the outer loop

    def is_balanced(self, matrix):
        left_sum = sum(matrix[i][j] for i in range(self.rows) for j in range(self.cols // 2))
        right_sum = sum(matrix[i][j] for i in range(self.rows) for j in range(self.cols // 2, self.cols))
        balancing_score = min(left_sum, right_sum) / max(left_sum, right_sum)
        threshold = 0.9  # Adjust this threshold as needed

        return balancing_score > threshold

    def print_solution(self, matrix, parent):
        print("FOUND SOLUTION!!!")
        for row in matrix:
            print(row)
        print("Path:")
        print(parent)

def main():
    matrix = [
        [6, 0, 0, 0],
        [10, 4, 0, 0]
    ]

    balancing_path_finder = FindBalancingPath(matrix)
    balancing_path_finder.solve_balancing()

if __name__ == "__main__":
    main()

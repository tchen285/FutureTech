import copy
import sys
from collections import deque

class FindBalancingPath:
    def __init__(self, matrix):
        self.matrix = matrix
        self.cols = len(matrix[0])
        self.rows = len(matrix)
        self.queue = deque()
        self.queue.append((matrix, []))  # Each node saves the current matrix and the path taken
        self.visited = set()  # Initialize the visited set
        self.level = 0

    def solve_balancing(self):
        while self.queue:
            level_size = len(self.queue)
            self.level += 1

            for _ in range(level_size):
                popped_matrix, path = self.queue.popleft()
                if self.is_balanced(popped_matrix):
                    print("\n\nFOUND SOLUTION!!!\n\n")
                    self.print_solution(popped_matrix, path)
                    sys.exit()  # End the entire program

                matrix_tuple = tuple(tuple(row) for row in popped_matrix)
                if matrix_tuple in self.visited:
                    continue
                self.visited.add(matrix_tuple)

                for col in range(self.cols):
                    if popped_matrix[-1][col] == 0:
                        continue

                    current_matrix = copy.deepcopy(popped_matrix)
                    for row in range(self.rows):
                        if current_matrix[row][col] != 0:
                            path.append((col, row))
                            break
                    self.solve_current_column(current_matrix, path, col)

                print("Queue Size:", len(self.queue))
                print("Queue Elements:")
                for elem, elem_path in self.queue:
                    print(elem)
                    print(elem_path)
                    print()

    def solve_current_column(self, matrix, path, col):
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
                                self.print_solution(matrix, path + [(col2, row2)])

                                sys.exit()  # End the entire program

                            matrix_tuple = tuple(tuple(row) for row in matrix)
                            if matrix_tuple in self.visited:
                                continue
                            path.append((col2, row2))
                            self.queue.append((copy.deepcopy(matrix), path))

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

    def print_solution(self, matrix, path):
        print("FOUND SOLUTION!!!")
        for row in matrix:
            print(row)
        print("Path:")
        print(path)

def main():
    matrix = [
        [6, 0, 0, 0],
        [10, 4, 0, 0]
    ]

    balancing_path_finder = FindBalancingPath(matrix)
    balancing_path_finder.solve_balancing()

if __name__ == "__main__":
    main()

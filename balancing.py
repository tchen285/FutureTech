from collections import deque


class FindBalancingPath:
    def __init__(self, matrix):
        self.matrix = matrix
        self.cols = len(matrix[0])
        self.rows = len(matrix)
        self.queue = deque()
        self.queue.append((matrix, []))  # 每个节点保存当前矩阵和移动的路径
        self.visited = set()  # Initialize the visited set

    def solve_balancing(self):
        while self.queue:
            current_matrix, current_path = self.queue.popleft()

            print("Current Matrix:")
            for row in current_matrix:
                print(row)

            if self.is_balanced(current_matrix):
                print("Balancing path found:")
                for move in current_path:
                    print(move)
                return

            visited_hash = hash(str(current_matrix))  # 使用哈希值来避免重复访问相同状态
            if visited_hash in self.visited:
                continue
            self.visited.add(visited_hash)

            for row in range(self.rows):
                for col in range(self.cols):
                    for move_row in [-1, 0, 1]:
                        for move_col in [-1, 0, 1]:
                            if move_row == 0 and move_col == 0:
                                continue  # Skip the case where there is no movement

                            new_matrix = self.make_move(current_matrix, row, col, move_row, move_col)
                            if new_matrix:
                                new_path = current_path + [(row, col, move_row, move_col)]
                                self.queue.append((new_matrix, new_path))

        print("No balancing path found.")

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

from collections import deque
import copy
import sys


class FindBalancingPath:
    def __init__(self, matrix):
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

    def solve_balancing(self):
        while self.queue:
            level_size = len(self.queue)
            print("\n@@@@@@")
            print("开始新一轮pop queue:")
            print("Queue Size:", len(self.queue))
            print("Queue Elements:")
            for elem in self.queue:
                print(elem)
            print("visited elements:")
            for visited_elem in self.visited:
                print(visited_elem)
                print()
            print("@@@@@@\n")

            for _ in range(level_size):
                popped_matrix = self.queue.popleft()
                # 输出根矩阵的父节点, 是None
                print("$$$$\n打印根节点矩阵以及根节点的父节点")
                print(tuple(map(tuple, popped_matrix)))  # 目前输出正确
                print(self.matrix_parent[tuple(map(tuple, popped_matrix))])  # 根节点的父节点是None, 目前输出正确
                print("$$$$")

                if self.is_balanced(popped_matrix):
                    print("\n\nFOUND SOLUTION!!!\n\n")
                    for row in popped_matrix:
                        print(row)
                    sys.exit()  # End the entire program

                # matrix_tuple = tuple(tuple(row) for row in popped_matrix)
                # if matrix_tuple in self.visited:
                #     continue
                # self.visited.add(matrix_tuple)

                # 从第一列开始检查, 跳过全是0的列
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
        print("当前处理的矩阵:")
        print(matrix)
        print("当前处理的列:")
        print(col)
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

                for col2 in range(self.cols):
                    if col2 == col:
                        continue
                    for row2 in reversed(range(self.rows)):
                        if matrix[0][col2] != 0:
                            continue
                        if matrix[row2][col2] == 0:
                            matrix[row2][col2] = weight
                            # tuple_matrix = tuple(map(tuple, matrix))
                            # if tuple_matrix in queue:
                            #     continue
                            if tuple(map(tuple, matrix)) in self.visited:
                                continue
                            self.matrix_parent[tuple(map(tuple, matrix))] = tuple(map(tuple, original_matrix))

                            print("\n--------------")
                            print(matrix[0])
                            print(matrix[1])
                            print("--------------")

                            if self.is_balanced(matrix):
                                for row in matrix:
                                    print(row)

                                # 打印result的父矩阵
                                print(self.matrix_parent[tuple(map(tuple, matrix))])  # 到目前为止是对的
                                # new_matrix是result的父矩阵
                                new_matrix = self.matrix_parent[tuple(map(tuple, matrix))]
                                print(new_matrix)
                                print(self.matrix_parent[new_matrix])
                                print("哈哈哈哈")
                                current = tuple(map(tuple, matrix))
                                print(current)
                                while self.matrix_parent[current]:
                                    move_description = self.interpret_move(self.matrix_parent[current], current)
                                    # print(move_description)

                                    current = self.matrix_parent[current]
                                for description in reversed(self.move_descriptions):
                                    print(description)
                                print("\nTotal time cost: ", self.total_cost, " minutes.")

                                sys.exit()  # End the entire program

                            matrix_tuple = tuple(tuple(row) for row in matrix)
                            if matrix_tuple in self.visited:
                                print("Found Duplicate")
                                continue  # 这里这种情况是无限循环的根源

                            self.visited.add(matrix_tuple)

                            print("Visited Elements:")
                            for visited_elem in self.visited:
                                print(visited_elem)
                                print()

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
        print("计算左右的值")
        print(left_sum)
        print(right_sum)
        balancing_score = min(left_sum, right_sum) / max(left_sum, right_sum)
        print(balancing_score)
        threshold = 0.9  # Adjust this threshold as needed

        return balancing_score > threshold

    def interpret_move(self, parent_tuple, current_tuple):
        moves = []
        start_row, start_col, end_row, end_col = 0, 0, 0, 0
        for i1 in range(len(current_tuple)):
            for j1 in range(len(current_tuple[0])):
                if parent_tuple[i1][j1] != 0 and current_tuple[i1][j1] == 0:
                    moves.append((i1, j1))
                    start_row, start_col = i1, j1
                    height = self.rows - start_row

        for i2 in range(len(current_tuple)):
            for j2 in range(len(current_tuple[0])):
                if parent_tuple[i2][j2] == 0 and current_tuple[i2][j2] != 0:
                    moves.append((i2, j2))
                    end_row, end_col = i2, j2
                    height = max(height, self.rows - end_row)

        if abs(start_col - end_col) == 1:
            distance = abs(moves[0][0] - moves[1][0]) + abs(moves[0][1] - moves[1][1])
        else:
            distance = self.find_moving_distance(parent_tuple, current_tuple, start_col, end_col)
        print("这一轮的移动距离: ", distance)
        self.total_cost += distance

        move_description = f"\nMove the container at {moves[0]} to {moves[1]}. It takes {distance} minutes."
        self.move_descriptions.append(move_description)

    def find_moving_distance(self, start_tuple, end_tuple, start_col, end_col):
        mid_height, start_height, end_height = 0, 0, 0
        start = start_col
        end = end_col
        print("\n\n这一轮起点列与终点列: ", start, end) # 输出正确
        for row in range(self.rows):
            if start_tuple[row][start] != 0:
                start_height = self.rows - row
                break
        print("start_height: ", start_height)

        for row in range(self.rows):
            if end_tuple[row][end] != 0:
                end_height = self.rows - row
                break
        print("end_height: ", end_height)

        for column in range(min(start, end) + 1, max(start, end)):
            print("列: ", column)
            for row in range(self.rows):
                if start_tuple[row][column] != 0:
                    mid_height = max(mid_height, self.rows - row)
                    break
        print("mid_height: ", mid_height)

        if mid_height < max(start_height, end_height):
            return abs(start - end) + abs(start_height - end_height)
        return mid_height - start_height + 2 + mid_height - end_height + abs(start - end)


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

    # matrix = [ # passed time cost test
    #     [3, 3, 0, 0],
    #     [10, 4, 0, 0]
    # ]

    # matrix = [ # passed time cost test
    #     [0, 0, 3, 0],
    #     [10, 4, 3, 0]
    # ]

    # matrix = [ # passed time cost test
    #     [0, 0, 0, 0],
    #     [10, 2, 14, 2]
    # ]

    # matrix = [ # passed time cost test
    #     [6, 0, 0, 0],
    #     [10, 4, 0, 0]
    # ]

    # matrix = [ # passed time cost test
    #     [0, 0, 3, 1],
    #     [5, 9, 1, 1]
    # ]
    #
    matrix = [ # passed time cost test
        [0, 2, 3, 0],
        [1, 1, 2, 7]
    ]

    balancing_path_finder = FindBalancingPath(matrix)
    balancing_path_finder.solve_balancing()


if __name__ == "__main__":
    main()
from collections import deque
import copy


class FindLoadUnloadPath:
    def __init__(self, matrix, container_data, container_weight):
        self.matrix = matrix
        self.container_data = container_data
        self.container_weight = container_weight
        self.unload_set = set()
        self.load_list = []
        self.start_matrix_tuple = tuple(map(tuple, matrix))
        self.cols = len(matrix[0])
        self.rows = len(matrix)
        self.queue = deque()
        self.queue.append(matrix)
        self.visited = set()  # Initialize the visited set
        matrix_tuple = tuple(map(tuple, matrix))
        self.visited.add(matrix_tuple)
        self.matrix_parent = {tuple(map(tuple, matrix)): None}
        self.unload_set = set()  # store the container coordinates that need to unload
        self.unload_descriptions = []

        self.total_cost = 0 # the critical output of cost

        self.unload_sequence = []  # store the unload sequence
        self.load_list = []  # store the load containers
        self.final_matrix = None
        self.unload_load_description = []
        self.idle_description = []
        self.total_description = [] # the critical output of description
        self.idle_start = None  # To deal with when the crane is in idle movement
        self.idle_end = None

    def solve_load_unload(self):
        while self.queue:
            if not self.unload_set and not self.load_list:
                break
            level_size = len(self.queue)
            for _ in range(level_size):
                popped_matrix = self.queue.popleft()

                if not self.unload_set:
                    popped_matrix_copy = copy.deepcopy(popped_matrix)
                    while self.load_list:
                        curr_matrix = self.load_a_container(popped_matrix_copy)
                        self.matrix_parent[tuple(map(tuple, curr_matrix))] = tuple(map(tuple, popped_matrix_copy))
                        popped_matrix_copy = copy.deepcopy(curr_matrix)
                    self.final_matrix = copy.deepcopy(curr_matrix)
                    break

                for col in range(self.cols):
                    if popped_matrix[-1][col] == 0:
                        continue
                    if popped_matrix[-1][col] is None:
                        find_a_container = False
                        for r in range(self.rows):
                            if popped_matrix[r][col] != 0 or popped_matrix[r][col] is not None:
                                find_a_container = True
                        if find_a_container is False:
                            continue
                    current_matrix = copy.deepcopy(popped_matrix)
                    if self.solve_current_column(current_matrix, popped_matrix, col):
                        break
                break

        self.interpret_final_matrix(self.final_matrix)
        reversed_array = self.unload_load_description[::-1]
        keyword = "Move"
        for i in range(len(reversed_array)):
            if keyword in reversed_array[i]:
                idle_dist = abs(self.idle_start[0] - self.idle_end[0]) + abs(self.idle_start[1] - self.idle_end[1])
                idle_desc = f"Move the crane from {self.idle_start} to {self.idle_end}.\nThis step takes {idle_dist}."
                self.total_description.append(reversed_array[i])
                self.total_description.append(idle_desc)
                self.total_cost += idle_dist
                continue
            self.total_description.append(reversed_array[i])

        print()

        # The software should print self.total_description step by step
        for row in self.total_description:
            print(row)

        print("\ntotal cost is: ", self.total_cost)
        print("********shishishishishih ", self.container_data[(1, 2)])  # 成功!!!
        print("))))))))测试unload Sequence", self.unload_sequence)
        return self.unload_sequence, self.total_description, self.total_cost



    def solve_current_column(self, matrix, original_matrix, col):
        for row1 in range(self.rows):
            if (row1, col) in self.unload_set:
                self.unload_sequence.append(self.container_data[(8 - row1, col + 1)])
                self.unload_set.remove((row1, col))
                matrix[row1][col] = 0
                matrix_tuple = tuple(map(tuple, matrix))
                self.matrix_parent[matrix_tuple] = tuple(map(tuple, original_matrix))
                if self.load_list:
                    matrix = self.load_a_container(matrix)

                matrix_tuple = tuple(tuple(row) for row in matrix)

                # self.matrix_parent[matrix_tuple] = tuple(map(tuple, original_matrix))
                self.visited.add(matrix_tuple)
                self.queue.clear()
                self.queue.append(copy.deepcopy(matrix))
                if not self.unload_set:
                    self.final_matrix = matrix

                return True

            if matrix[row1][col] != 0 and matrix[row1][col] is not None:
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
                                for row in matrix:
                                    print(row)
                                matrix[row2][col2] = 0
                                break

                            self.matrix_parent[tuple(map(tuple, matrix))] = tuple(map(tuple, original_matrix))
                            matrix_tuple = tuple(tuple(row) for row in matrix)
                            self.visited.add(matrix_tuple)
                            self.queue.append(copy.deepcopy(matrix))
                            matrix[row2][col2] = 0
                            break  # Exit the inner loop
                break
        return False


    def load_a_container(self, matrix):
        original_matrix = copy.deepcopy(matrix)
        curr_matrix = copy.deepcopy(matrix)
        curr_weight = self.load_list.pop(0)
        min_dist = float("inf")
        min_dist_coordinates = None

        for col in range(self.cols):
            for row in reversed(range(self.rows)):
                if curr_matrix[row][col] == 0:
                    current_dist = row + col
                    if current_dist < min_dist:
                        min_dist = current_dist
                        min_dist_coordinates = (row, col)
                        break
            break

        if min_dist_coordinates is not None:
            row, col = min_dist_coordinates
            curr_matrix[row][col] = curr_weight

        curr_matrix_tuple = tuple(map(tuple, curr_matrix))
        self.matrix_parent[curr_matrix_tuple] = tuple(map(tuple, original_matrix))
        return curr_matrix

    def interpret_move(self, parent_tuple, current_tuple):
        moves = []
        start_row, start_col, end_row, end_col = 0, 0, 0, 0
        for i1 in range(len(current_tuple)):
            for j1 in range(len(current_tuple[0])):
                if parent_tuple[i1][j1] != 0 and parent_tuple[i1][j1] is not None and current_tuple[i1][j1] == 0:
                    moves.append((i1, j1))
                    start_row, start_col = i1, j1
                    height = self.rows - start_row

        for i2 in range(len(current_tuple)):
            for j2 in range(len(current_tuple[0])):
                if parent_tuple[i2][j2] == 0 and current_tuple[i2][j2] != 0 and current_tuple[i2][j2] is not None:
                    moves.append((i2, j2))
                    end_row, end_col = i2, j2
                    height = max(height, self.rows - end_row)

        # if abs(start_col - end_col) == 1:
        #     distance = abs(moves[0][0] - moves[1][0]) + abs(moves[0][1] - moves[1][1])
        # else:
        #     distance = self.find_moving_distance(parent_tuple, current_tuple, start_col, end_col)
        distance = abs(moves[0][0] - moves[1][0]) + abs(moves[0][1] - moves[1][1])
        # self.total_cost += distance
        return moves[0], moves[1], distance

        # move_description = f"\nMove container at {moves[0]} to {moves[1]}. It takes {distance} minutes."

    def find_moving_distance(self, start_tuple, end_tuple, start_col, end_col):
        mid_height, start_height, end_height = 0, 0, 0
        start = start_col
        end = end_col
        for row in range(self.rows):
            if start_tuple[row][start] != 0:
                start_height = row
                break

        for row in range(self.rows):
            if end_tuple[row][end] != 0:
                end_height = row
                break

        for column in range(min(start, end) + 1, max(start, end)):
            for row in range(self.rows):
                if start_tuple[row][column] != 0:
                    mid_height = max(mid_height, row)
                    break

        if mid_height < max(start_height, end_height):
            return abs(start - end) + abs(start_height - end_height)
        return mid_height - start_height + 2 + mid_height - end_height + abs(start - end)

    def interpret_unloading(self, parent_tuple, current_tuple):
        for row in range(self.rows):
            for col in range(self.cols):
                if parent_tuple[row][col] != 0 and current_tuple[row][col] == 0:
                    cost = row + col + 3
                    return row, col, cost

    def interpret_loading(self, parent_tuple, current_tuple):
        for row in range(self.rows):
            for col in range(self.cols):
                if parent_tuple[row][col] == 0 and current_tuple[row][col] != 0:
                    cost = row + col + 3
                    return row, col, cost

    def interpret_final_matrix(self, final_matrix):
        current_matrix = copy.deepcopy(final_matrix)
        current_matrix_tuple = tuple(map(tuple, current_matrix))
        while self.matrix_parent[current_matrix_tuple]:
            parent_matrix_tuple = self.matrix_parent[current_matrix_tuple]
            parent_weight, current_weight = 0, 0
            for row in range(self.rows):
                for col in range(self.cols):
                    if parent_matrix_tuple[row][col] is not None:
                        parent_weight += parent_matrix_tuple[row][col]
                    if current_matrix_tuple[row][col] is not None:
                        current_weight += current_matrix_tuple[row][col]

            if parent_weight > current_weight:
                # 执行卸船
                row, col, cost = self.interpret_unloading(parent_matrix_tuple, current_matrix_tuple)
                self.idle_end = (row, col)
                # idle_distance = abs(critical_end[0] - row) + abs(critical_end[1] - col)
                # print(f"Move the crane from [{critical_end}] to [{row},{col}].\nThis step takes {idle_distance} minutes")
                description = f"Retrieve {self.container_data[(8 - row, col + 1)]} ({self.container_weight[self.container_data[(8 - row, col + 1)]]}kg) located at [{8 - row},{col + 1}] and place it onto the truck.\nThis step takes {cost} minutes."
                self.unload_load_description.append(description)
                self.total_cost += cost

            if parent_weight == current_weight:
                # 执行船内移动
                start_coordinate, end_coordinate, cost = self.interpret_move(parent_matrix_tuple, current_matrix_tuple)
                description = f"Move {self.container_data[(8 - start_coordinate, end_coordinate + 1)]} ({self.container_weight[self.container_data[(8 - start_coordinate, end_coordinate + 1)]]}kg) located at [{8 - start_coordinate}] to [{end_coordinate + 1}].\nThis step takes {cost} minutes."
                self.unload_load_description.append(description)
                self.idle_start = end_coordinate
                self.total_cost += cost


            if parent_weight < current_weight:
                # 执行装船
                row, col, cost = self.interpret_loading(parent_matrix_tuple, current_matrix_tuple)
                description = f"Take the loading container from truck and place it at [{8 - row},{col + 1}].\nThis step takes {cost} minutes."
                self.unload_load_description.append(description)
                self.total_cost += cost

            current_matrix_tuple = self.matrix_parent[current_matrix_tuple]
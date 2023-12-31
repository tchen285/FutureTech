from collections import deque
from os.path import join, expanduser
import copy
import re
from datetime import datetime

class FindBalancingPath:
    def __init__(self, matrix, file_name, container_data, container_weight):
        self.container_data = container_data
        self.container_weight = container_weight
        self.start_matrix_tuple = tuple(map(tuple, matrix))
        self.matrix = matrix
        self.file_name = file_name
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
        self.is_sift = False
        self.goal_matrix_tuple = None
        self.idle_starts = []
        self.idle_matrix_tuple = []
        self.idle_ends = []
        self.idle_descriptions = []
        self.description_list = []
        self.swap_tuple_list = []

    def solve_balancing(self):
        total_sum = sum(
            self.start_matrix_tuple[i][j] if self.start_matrix_tuple[i][j] is not None else 0
            for i in range(self.rows) for j in range(self.cols)
        )
        max_element = max(
            self.start_matrix_tuple[i][j] if self.start_matrix_tuple[i][j] is not None else float('-inf')
            for i in range(self.rows) for j in range(self.cols)
        )

        if 0.9 * max_element > (total_sum - max_element):
            self.is_sift = True
            self.sift(self.matrix)

            for swap_tuple in reversed(self.swap_tuple_list):
                self.replace_coordinates(swap_tuple[0], swap_tuple[1])
            return

        while self.queue:
            level_size = len(self.queue)
            for _ in range(level_size):
                popped_matrix = self.queue.popleft()

                if self.is_balanced(popped_matrix):
                    return

                for col in range(self.cols):
                    # if popped_matrix[-1][col] == 0 or (popped_matrix[-1][col] is None and any(
                    #         popped_matrix[i][col] == 0 for i in range(self.rows - 1, -1, -1))):
                    #     continue
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
                        for swap_tuple in reversed(self.swap_tuple_list):
                            self.replace_coordinates(swap_tuple[0], swap_tuple[1])
                        return

    def solve_current_column(self, matrix, original_matrix, col):
        for row1 in range(self.rows):
            if matrix[row1][col] != 0 and matrix[row1][col] != None:
                weight = matrix[row1][col]
                matrix[row1][col] = 0

                for col2 in range(self.cols):
                    if col2 == col:
                        continue
                    for row2 in reversed(range(self.rows)):
                        if matrix[0][col2] != 0:
                            continue
                        if matrix[row2][col2] == 0:
                            matrix[row2][col2] = weight
                            if tuple(map(tuple, matrix)) in self.visited:
                                matrix[row2][col2] = 0
                                break
                            self.matrix_parent[tuple(map(tuple, matrix))] = tuple(map(tuple, original_matrix))

                            if self.is_balanced(matrix):
                                self.goal_matrix_tuple = tuple(map(tuple, matrix))
                                self.matrix_parent[tuple(map(tuple, matrix))]
                                current = tuple(map(tuple, matrix))

                                while self.matrix_parent[current]:
                                    self.interpret_move(self.matrix_parent[current], current)
                                    current = self.matrix_parent[current]

                                i = 1
                                while self.idle_matrix_tuple[-i] != self.goal_matrix_tuple and self.idle_matrix_tuple[
                                    -i] != self.start_matrix_tuple:
                                    idle_start = self.idle_starts[-i]

                                    idle_matrix_tuple = self.idle_matrix_tuple[-i]

                                    idle_end = self.idle_ends[-(i + 1)]

                                    idle_distance = self.find_idle_distance(idle_start, idle_matrix_tuple, idle_end)

                                    idle_description = f"\nMove crane from {idle_start} to {idle_end}. It takes {idle_distance} minutes."
                                    self.idle_descriptions.append(idle_description)
                                    self.total_cost += idle_distance
                                    i += 1

                                index1, index2 = 0, 0
                                while index1 != len(self.move_descriptions) and index2 != len(self.idle_descriptions):
                                    print(self.move_descriptions[-(index1 + 1)])
                                    self.description_list.append(self.move_descriptions[-(index1 + 1)])
                                    print(self.idle_descriptions[index2])
                                    self.description_list.append(self.idle_descriptions[index2])
                                    index1 += 1
                                    index2 += 1
                                print(self.move_descriptions[0])
                                self.description_list.append(self.move_descriptions[0])
                                print("\nTotal time cost: ", self.total_cost, " minutes.")
                                return True

                            matrix_tuple = tuple(tuple(row) for row in matrix)
                            if matrix_tuple in self.visited:
                                continue

                            self.visited.add(matrix_tuple)
                            self.queue.append(copy.deepcopy(matrix))
                            matrix[row2][col2] = 0
                            break  # Exit the inner loop
                break  # Exit the outer loop
        return False

    def is_balanced(self, matrix):
        left_sum = sum(
            matrix[i][j] if matrix[i][j] is not None else 0 for i in range(self.rows) for j in range(self.cols // 2))
        right_sum = sum(matrix[i][j] if matrix[i][j] is not None else 0 for i in range(self.rows) for j in
                        range(self.cols // 2, self.cols))

        # Ensure that denominator is not zero
        max_sum = max(left_sum, right_sum)
        balancing_score = min(left_sum, right_sum) / max_sum if max_sum != 0 else 0
        threshold = 0.9  # Adjust this threshold as needed
        return balancing_score > threshold

    def interpret_move(self, parent_tuple, current_tuple):
        moves = []
        start_row, start_col, end_row, end_col = 0, 0, 0, 0
        for i1 in range(len(current_tuple)):
            for j1 in range(len(current_tuple[0])):
                if parent_tuple[i1][j1] != 0 and parent_tuple[i1][j1] != None and current_tuple[i1][j1] == 0:
                    moves.append((self.rows - i1, j1 + 1))
                    start_row, start_col = i1, j1
                    height = self.rows - start_row

        for i2 in range(len(current_tuple)):
            for j2 in range(len(current_tuple[0])):
                if parent_tuple[i2][j2] == 0 and current_tuple[i2][j2] != 0 and current_tuple[i2][j2] != None:
                    moves.append((self.rows - i2, j2 + 1))
                    end_row, end_col = i2, j2
                    height = max(height, self.rows - end_row)


        if abs(start_col - end_col) == 1:
            distance = abs(moves[0][0] - moves[1][0]) + abs(moves[0][1] - moves[1][1])
        else:
            distance = self.find_moving_distance(parent_tuple, current_tuple, start_col, end_col)
        self.total_cost += distance
        print("Print moves0 and moves1:*******")
        print(moves[0])
        print(moves[1])
        self.swap_tuple_list.append((moves[0], moves[1]))

        move_description = f"\nMove {self.container_data[moves[0]]} ({self.container_weight[self.container_data[moves[0]]]}kg) at {moves[0]} to {moves[1]}. It takes {distance} minutes."
        # move_description = f"\nMove container at {moves[0]} to {moves[1]}. It takes {distance} minutes."
        self.move_descriptions.append(move_description)
        self.idle_ends.append(moves[0])
        self.idle_starts.append(moves[1])
        self.idle_matrix_tuple.append(current_tuple)


    def find_moving_distance(self, start_tuple, end_tuple, start_col, end_col):
        mid_height, start_height, end_height = 0, 0, 0
        start = start_col
        end = end_col
        for row in range(self.rows):
            if start_tuple[row][start] != 0:
                start_height = self.rows - row
                break

        for row in range(self.rows):
            if end_tuple[row][end] != 0:
                end_height = self.rows - row
                break

        for column in range(min(start, end) + 1, max(start, end)):
            for row in range(self.rows):
                if start_tuple[row][column] != 0:
                    mid_height = max(mid_height, self.rows - row)
                    break

        if mid_height < max(start_height, end_height):
            return abs(start - end) + abs(start_height - end_height)
        return mid_height - start_height + 2 + mid_height - end_height + abs(start - end)

    def find_idle_distance(self, idle_start, idle_matrix_tuple, idle_end):
        start_height = self.rows - idle_start[0]
        end_height = self.rows - idle_end[0]
        mid_height = 0
        for col in range(min(idle_start[1], idle_end[1]) + 1, max(idle_start[1], idle_end[1])):
            for row in range(self.rows):
                if idle_matrix_tuple[row][col] != 0:
                    height = self.rows - row
                    mid_height = max(height, mid_height)

        if start_height == end_height and mid_height < start_height:
            return abs(idle_start[1] - idle_end[1]) + 2

        if mid_height < max(start_height, end_height):
            return abs(idle_start[0] - idle_end[0]) + abs(idle_start[1] - idle_end[1])

        return mid_height - start_height + 2 + mid_height - end_height + abs(idle_start[1] - idle_end[1])

    def replace_coordinates(self, coordinates1, coordinates2):
        desktop_path = join(expanduser("~"), "Desktop")
        filename = self.file_name
        file_path = join(desktop_path, filename)

        with open(file_path, 'r') as file:
            lines = file.readlines()

        old_coordinates_str1 = '[{:02d},{:02d}]'.format(*coordinates1)
        old_coordinates_str2 = '[{:02d},{:02d}]'.format(*coordinates2)

        for i in range(len(lines)):
            # Assuming [01, 01] and [02, 02] are present in each line
            lines[i] = lines[i].replace(old_coordinates_str1, 'TEMP_SWAP')
            lines[i] = lines[i].replace(old_coordinates_str2, old_coordinates_str1)
            lines[i] = lines[i].replace('TEMP_SWAP', old_coordinates_str2)

        # Write the modified content back to the file
        with open(file_path, 'w') as file:
            file.writelines(lines)


    def sift(self, matrix):
        start_matrix = matrix
        target_matrix = self.find_sift_target_matrix(start_matrix)

        while self.queue:
            level_size = len(self.queue)
            for _ in range(level_size):
                popped_matrix = self.queue.popleft()
                if popped_matrix == target_matrix:
                    return

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
                    if self.solve_sift_current_column(current_matrix, popped_matrix, target_matrix, col):
                        return


    def solve_sift_current_column(self, matrix, original_matrix, target_matrix, col):
        for row1 in range(self.rows):
            if matrix[row1][col] != 0 and matrix[row1][col] != None:
                weight = matrix[row1][col]
                matrix[row1][col] = 0

                for col2 in range(self.cols):
                    if col2 == col:
                        continue
                    for row2 in reversed(range(self.rows)):
                        if matrix[0][col2] != 0:
                            continue
                        if matrix[row2][col2] == 0:
                            matrix[row2][col2] = weight
                            if tuple(map(tuple, matrix)) in self.visited:
                                matrix[row2][col2] = 0
                                break
                            self.matrix_parent[tuple(map(tuple, matrix))] = tuple(map(tuple, original_matrix))

                            if matrix == target_matrix:
                                self.goal_matrix_tuple = tuple(map(tuple, matrix))
                                self.matrix_parent[tuple(map(tuple, matrix))]
                                current = tuple(map(tuple, matrix))

                                while self.matrix_parent[current]:
                                    self.interpret_move(self.matrix_parent[current], current)
                                    current = self.matrix_parent[current]

                                i = 1
                                while self.idle_matrix_tuple[-i] != self.goal_matrix_tuple and self.idle_matrix_tuple[
                                    -i] != self.start_matrix_tuple:
                                    idle_start = self.idle_starts[-i]

                                    idle_matrix_tuple = self.idle_matrix_tuple[-i]

                                    idle_end = self.idle_ends[-(i + 1)]

                                    idle_distance = self.find_idle_distance(idle_start, idle_matrix_tuple, idle_end)

                                    idle_description = f"\nMove crane from {idle_start} to {idle_end}. It takes {idle_distance} minutes."
                                    self.idle_descriptions.append(idle_description)
                                    self.total_cost += idle_distance
                                    i += 1

                                index1, index2 = 0, 0
                                while index1 != len(self.move_descriptions) and index2 != len(self.idle_descriptions):
                                    print(self.move_descriptions[-(index1 + 1)])
                                    self.description_list.append(self.move_descriptions[-(index1 + 1)])
                                    print(self.idle_descriptions[index2])
                                    self.description_list.append(self.idle_descriptions[index2])
                                    index1 += 1
                                    index2 += 1
                                print(self.move_descriptions[0])
                                self.description_list.append(self.move_descriptions[0])
                                print("\nTotal time cost: ", self.total_cost, " minutes.")
                                self.write_sift_log()
                                return True

                            matrix_tuple = tuple(tuple(row) for row in matrix)
                            if matrix_tuple in self.visited:
                                continue  

                            self.visited.add(matrix_tuple)
                            self.queue.append(copy.deepcopy(matrix))
                            matrix[row2][col2] = 0
                            break  # Exit the inner loop
                break  # Exit the outer loop
        return False


    def find_sift_target_matrix(self, matrix):
        start_matrix = matrix
        list = [element for row in start_matrix for element in row if element is not None and element != 0]
        list.sort(reverse=True)
        print(list)
        target_matrix = [[None if element is None else 0 for element in row] for row in start_matrix]
        print(target_matrix)
        column_list = [5, 6, 4, 7, 3, 8, 2, 9, 1, 10, 0, 11]

        if target_matrix[7][5] is not None:
            row = 7
        if target_matrix[7][5] is None:
            row = 6

        while list:
            col = column_list.pop(0)
            target_matrix[row][col] = list.pop(0)

        # print target_matrix
        for row in target_matrix:
            print(row)

        return target_matrix

    def write_sift_log(self):
        current_time = datetime.now().strftime("%m/%d/%Y: %H:%M")

        # Log the information to the log file
        with open('log.txt', 'a') as log_file:
            log_file.write(f"{current_time} Can't use balance, use SIFT process.\n")

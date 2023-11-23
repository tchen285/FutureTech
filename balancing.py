class FindBalancingPath:
    def __init__(self, matrix):
        self.matrix = matrix
        self.cols = len(matrix[0])
        self.rows = len(matrix)

def main():
    matrix = [
        [6, 0, 0, 0],
        [10, 4, 0, 0]
    ]

    path_finder = FindBalancingPath(matrix)

    print(matrix)

if __name__ == "__main__":
    main()
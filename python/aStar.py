import math
import heapq

class Cell:
    def __init__(self):
        self.parent_i = 0        # Parent cell's row index
        self.parent_j = 0        # Parent cell's column index
        self.f = float('inf')    # Total cost of the cell (g + h)
        self.g = float('inf')    # Cost from start to this cell
        self.h = 0               # Heuristic cost from this cell to destination

class AStar:
    def __init__(self, num_rows, num_cols):
        self.rows = num_rows
        self.cols = num_cols

    def is_valid(self, row, col):
        return (row >= 0) and (row < self.rows) and (col >= 0) and (col < self.cols)

    def is_unblocked(self, grid, row, col):
        return grid[row][col] == 1

    def is_destination(self, row, col, dest):
        return row == dest[0] and col == dest[1]

    def calculate_h_value(self, row, col, dest):
        # Euclidean distance 
        return ((row - dest[0]) ** 2 + (col - dest[1]) ** 2) ** 0.5

    def trace_path(self, cell_details, dest):
        path = []
        row = dest[0]
        col = dest[1]

        # Trace the path from destination to source using parent cells
        while not (cell_details[row][col].parent_i == row and cell_details[row][col].parent_j == col):
            path.append((row, col))
            temp_row = cell_details[row][col].parent_i
            temp_col = cell_details[row][col].parent_j
            row = temp_row
            col = temp_col

        # Add the source cell to the path
        path.append((row, col))
        # Reverse the path to get the path from source to destination
        path.reverse()

        return path

    def a_star_search(self, grid, src, dest):
        # Check if the source and destination are valid
        if not self.is_valid(src[0], src[1]) or not self.is_valid(dest[0], dest[1]):
            print("Source or destination is invalid")
            return []

        # Check if the source and destination are unblocked
        if not self.is_unblocked(grid, src[0], src[1]) or not self.is_unblocked(grid, dest[0], dest[1]):
            print("Source or the destination is blocked")
            return []

        # Check if we are already at the destination
        if self.is_destination(src[0], src[1], dest):
            print("We are already at the destination")
            return []

        # Initialize the closed list (visited cells)
        closed_list = [[False for _ in range(self.cols)] for _ in range(self.rows)]
        # Initialize the details of each cell
        cell_details = [[Cell() for _ in range(self.cols)] for _ in range(self.rows)]

        # Initialize the start cell details
        i, j = src
        cell_details[i][j].f = 0
        cell_details[i][j].g = 0
        cell_details[i][j].h = 0
        cell_details[i][j].parent_i = i
        cell_details[i][j].parent_j = j

        # Initialize the open list (cells to be visited) with the start cell
        open_list = []
        heapq.heappush(open_list, (0.0, i, j))

        # Directions (4 cardinal and 4 diagonal directions)
        directions = [
            (0, 1), (0, -1), (1, 0), (-1, 0),   # Cardinal moves: Right, Left, Down, Up
            (1, 1), (1, -1), (-1, 1), (-1, -1)  # Diagonal moves: Down-Right, Down-Left, Up-Right, Up-Left
        ]

        # Main loop of A* search algorithm
        while open_list:
            # Pop the cell with the smallest f value from the open list
            p = heapq.heappop(open_list)
            i, j = p[1], p[2]
            closed_list[i][j] = True

            # For each direction, check the successors
            for dir in directions:
                new_i = i + dir[0]
                new_j = j + dir[1]

                # If the successor is valid, unblocked, and not visited
                if self.is_valid(new_i, new_j) and self.is_unblocked(grid, new_i, new_j) and not closed_list[new_i][new_j]:
                    # If the successor is the destination
                    if self.is_destination(new_i, new_j, dest):
                        # Set the parent of the destination cell
                        cell_details[new_i][new_j].parent_i = i
                        cell_details[new_i][new_j].parent_j = j
                        print("The destination cell is found")
                        # Trace and return the path from source to destination
                        return self.trace_path(cell_details, dest)

                    else:
                        # Calculate the new f, g, and h values
                        g_new = cell_details[i][j].g + 1.0
                        h_new = self.calculate_h_value(new_i, new_j, dest)
                        f_new = g_new + h_new

                        # If the cell is not in the open list or the new f value is smaller
                        if cell_details[new_i][new_j].f == float('inf') or cell_details[new_i][new_j].f > f_new:
                            # Add the cell to the open list
                            heapq.heappush(open_list, (f_new, new_i, new_j))
                            # Update the cell details
                            cell_details[new_i][new_j].f = f_new
                            cell_details[new_i][new_j].g = g_new
                            cell_details[new_i][new_j].h = h_new
                            cell_details[new_i][new_j].parent_i = i
                            cell_details[new_i][new_j].parent_j = j

        # If the destination is not found after visiting all cells
        print("Failed to find the destination cell")
        return []

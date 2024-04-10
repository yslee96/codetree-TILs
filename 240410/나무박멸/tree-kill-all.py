import sys
from collections import defaultdict
input = sys.stdin.readline

board_size, num_years, kill_dist, left_cnt = map(int, input().split())
board = [list(map(int, input().split())) for _ in range(board_size)]
is_available = [[0 for _ in range(board_size)] for _ in range(board_size)]
adj_dirs = [(-1,0), (1,0), (0,1), (0,-1)]
diag_dirs = [(-1,-1), (-1,1), (1,1), (1, -1)]

def get_adj_trees(row, col, size):
    tree_cnt = 0
    for dr, dc in adj_dirs:
        n_row, n_col = row + dr, col + dc
        if n_row < 0 or n_row>= size or n_col < 0 or n_col>=size:
            continue
        if board[n_row][n_col] > 0:
            tree_cnt += 1
    return tree_cnt

def tree_grow(size):
    cur_board = [[board[i][j] for j in range(size)] for i in range(size)]
    for i in range(size):
        for j in range(size):
            if cur_board[i][j] > 0:
                adj_trees = get_adj_trees(i,j, size)
                board[i][j] += adj_trees

def tree_produce(size, year):
    cur_board = [[board[i][j] for j in range(size)] for i in range(size)]
    produce_result = defaultdict(int)

    for i in range(size):
        for j in range(size):
            if cur_board[i][j] > 0:
                tree_cnt = 0
                places = []
                for dr, dc in adj_dirs:
                    n_row, n_col = i + dr, j + dc
                    if n_row < 0 or n_row >= size or n_col < 0 or n_col >= size:
                        continue
                    if cur_board[n_row][n_col] == 0 and is_available[n_row][n_col] <= year:
                        tree_cnt += 1
                        places.append((n_row,n_col))

                for row, col in places:
                    produce_result[(row,col)] += cur_board[i][j] // tree_cnt

    for row,col in list(produce_result.keys()):
        board[row][col] += produce_result[(row,col)]

def remove_trees(size, row, col, dist, year):
    board[row][col] = 0
    is_available[row][col] = year+left_cnt+1

    for dr, dc in diag_dirs:
        for dist in range(1, dist+1):
            n_row, n_col = row + dr*dist, col + dc*dist
            if n_row < 0 or n_row >= size or n_col < 0 or n_col >= size or board[n_row][n_col] == -1:
                break
            if board[n_row][n_col] >= 0:
                board[n_row][n_col] = 0
                is_available[n_row][n_col] = year+left_cnt+1

def count_extinct_trees(size, row, col, dist):
    total = board[row][col]
    for dr, dc in diag_dirs:
        for dist in range(1, dist+1):
            n_row, n_col = row + dr*dist, col + dc*dist
            if n_row < 0 or n_row >= size or n_col < 0 or n_col >= size or board[n_row][n_col] == -1:
                break
            if board[n_row][n_col] > 0:
                total += board[n_row][n_col]

    return total

def tree_extinct(size, k, year):
    extinct_trees_pq = []
    for i in range(size):
        for j in range(size):
            if board[i][j] > 0:
                extinct_trees = count_extinct_trees(size, i,j, k)
                extinct_trees_pq.append([-extinct_trees, i, j])

    if not extinct_trees_pq:
        return 0

    extinct_trees_pq.sort()
    total_extinct, row, col = extinct_trees_pq[0]
    remove_trees(size,row,col,k, year)

    return total_extinct * -1

sum_extincts = 0
for year in range(num_years):
    tree_grow(board_size)
    tree_produce(board_size, year)
    sum_extincts += tree_extinct(board_size, kill_dist, year)

print(sum_extincts)
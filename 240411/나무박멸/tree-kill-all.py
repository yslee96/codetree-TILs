# 첫 번째 줄에 격자의 크기 n, 박멸이 진행되는 년 수 m, 제초제의 확산 범위 k, 제초제가 남아있는 년 수 c가 공백을 사이에 두고 주어집니다.
#
# 이후 n개의 줄에 걸쳐 각 칸의 나무의 그루 수, 벽의 정보가 주어집니다. 총 나무의 그루 수는 1 이상 100 이하의 수로, 빈 칸은 0, 벽은 -1으로 주어지게 됩니다

# 5 ≤ n ≤ 20
# 1 ≤ m ≤ 1000
# 1 ≤ k ≤ 20
# 1 ≤ c ≤ 10
#
# 5 1 2 1
# 0 0 0 0 0
# 0 30 23 0 0
# 0 0 -1 0 0
# 0 0 17 46 77
# 0 0 0 12 0
#
# 179
import sys
from collections import defaultdict
input = sys.stdin.readline

# DATA
#
# board (나무 개수, 벽)
# is_available (제초제 여부, 현재 turn 과 일치 하는지로 판단)
# move_dirs(인접 4칸, 대각선 4칸)
#

board_size, num_years, kill_dist, left_cnt = map(int, input().split())
board = [list(map(int, input().split())) for _ in range(board_size)]
is_available = [[0 for _ in range(board_size)] for _ in range(board_size)]
adj_dirs = [(-1,0), (1,0), (0,1), (0,-1)]
diag_dirs = [(-1,-1), (-1,1), (1,1), (1, -1)]

# (1) 성장
# - 모든 나무 동시에
# - 인접한 4칸 중 나무가 있는 칸의 개수 만큼 나무 수 ++
#
# : 완탐하면서 나무 있으면 4방향 조사해서 더해주기

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

# (2) 번식
# - 모든 나무 동시에
# - 인접한 4개 칸 중 빈 칸에서 번식 가능
# - 번식하는 칸의 나무 그루 수 // 번식 가능한 칸의 수(1~4) 만큼 번식
#
# : 완탐하고 나무마다 파악해서 별도의 dict에 번식할 좌표 : 나무 수 로 정리
#   탐색 끝난 다음 board 업데이트

def tree_produce(size, cur_year):
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
                    if cur_board[n_row][n_col] == 0 and is_available[n_row][n_col] <= cur_year:
                        tree_cnt += 1
                        places.append((n_row,n_col))

                if tree_cnt == 0:
                    continue

                for row, col in places:
                    produce_result[(row,col)] += cur_board[i][j] // tree_cnt

    for row,col in list(produce_result.keys()):
        board[row][col] += produce_result[(row,col)]

# (3) 박멸
# - 가장 많이 박멸되는 칸에 제초제 투하
# - 나무 있는 칸에 뿌리면 4개의 대각선 방향으로 k만큼 전파
# - 벽 있거나 나무 없으면 전파 안됨
# - c년 만큼 제초제 남아있음(c+1)년에 다시 빈칸 됨
# - 기존 제초제에 또 뿌려지면 그 시점에서 다시 c년
#
# : 나무 있는 칸마다 4방향 대각선  k만큼 탐색
#   (나무수, (행,열)) list 정렬 제일 앞에 값 찾기
# 제초제
# - k 만큼 대각선
# - 벽 있으면 전파 x
# : 제초제 뿌린 후 나무 수 0으로 업데이트, is_available 현재 턴 + c+1로 바꾸기
#   is_available은 나무 번식할 때 확인


def remove_trees(size, row, col, dist, cur_year):
    board[row][col] = 0
    is_available[row][col] = year+left_cnt+1

    for dr, dc in diag_dirs:
        for dist in range(1, dist+1):
            n_row, n_col = row + dr*dist, col + dc*dist
            if n_row < 0 or n_row >= size or n_col < 0 or n_col >= size or board[n_row][n_col] == -1:
                break
            if board[n_row][n_col] >= 0:
                board[n_row][n_col] = 0
                is_available[n_row][n_col] = cur_year+left_cnt+1

def count_extinct_trees(size, row, col, dist):
    total = board[row][col]
    for dr, dc in diag_dirs:
        for dist in range(1, dist+1):
            n_row, n_col = row + dr*dist, col + dc*dist
            if n_row < 0 or n_row >= size or n_col < 0 or n_col >= size or board[n_row][n_col] <= 0:
                break
            total += board[n_row][n_col]

    return total

def tree_extinct(size, k, cur_year):
    extinct_trees_pq = []
    for i in range(size):
        for j in range(size):
            if board[i][j] > 0:
                extinct_trees = count_extinct_trees(size, i,j, k)
                extinct_trees_pq.append([-extinct_trees, i, j])

    extinct_trees_pq.sort()
    total_extinct, row, col = extinct_trees_pq[0]
    remove_trees(size,row,col,k, cur_year)
    return total_extinct * -1

sum_extincts = 0
for year in range(num_years):
    tree_grow(board_size)
    tree_produce(board_size, year)
    sum_extincts += tree_extinct(board_size, kill_dist, year)

print(sum_extincts)
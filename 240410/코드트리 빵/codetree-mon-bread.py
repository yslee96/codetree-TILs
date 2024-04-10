import sys
from collections import deque

input = sys.stdin.readline

max_size, num_people = map(int, input().split())
board = [list(map(int,input().split())) for _ in range(max_size)]
stores = [[0,0]]+ [list(map(int,input().split())) for _ in range(num_people)]
people_loc = dict()
is_arrived = [False for _ in range(num_people+1)]
basecamps = [[-1,-1]]


for i in range(max_size):
    for j in range(max_size):
        if board[i][j]:
            basecamps.append([i+1,j+1])

time = arrived = 0
visited = [[False for _ in range(max_size+1)] for _ in range(max_size+1)]

def enter_basecamp(person_num):
    # t<=m 일때 t번 사람 basecamp
    # 거리는 bfs로 측정
    if person_num > num_people:
        return

    q = deque()
    min_dist = float('inf')
    target_row, target_col = stores[person_num]
    cur_visited = [[visited[i][j] for j in range(max_size+1)] for i in range(max_size+1)]
    
    for idx, basecamp in enumerate(basecamps[1:]):
        b_row, b_col = basecamp
        if cur_visited[b_row][b_col]: continue
        q.append([0,b_row,b_col,idx+1])
        results = []

    while q:
        cur_dist, cur_row, cur_col, b_idx = q.popleft()

        if cur_row == target_row and cur_col == target_col and cur_dist <= min_dist:
            min_dist = cur_dist
            results.append(basecamps[b_idx] + [b_idx])
            continue
        
        for offset in [(0,1), (1,0), (0,-1), (-1,0)]:
            n_row = cur_row + offset[0]
            n_col = cur_col + offset[1]
            if n_row <= 0 or n_row>max_size or n_col<=0 or n_col>max_size: continue
            if cur_visited[n_row][n_col]: continue
            q.append([cur_dist+1, n_row, n_col, b_idx])
            if n_row == target_row and n_col == target_col: continue
            cur_visited[n_row][n_col] = True

    results.sort(key=lambda x: (x[0],x[1]))
    basecamp_num = results[0][-1]    
    basecamp_row, basecamp_col = basecamps[basecamp_num]
    people_loc[person_num] = [basecamp_row, basecamp_col]
    visited[basecamp_row][basecamp_col] = True

def move_people():
    # 편의점 좌표에서 사람 좌표(상하좌우)에 대해 bfs
    for person_num, person_loc in list(people_loc.items()):
        if is_arrived[person_num]: continue
        q = deque()
        store_loc = stores[person_num]
        target_row, target_col = person_loc
        goals = [(target_row-1,target_col), (target_row+1, target_col), (target_row, target_col-1), (target_row, target_col+1)]
        cur_visited = [[visited[i][j] for j in range(max_size+1)] for i in range(max_size+1)]
        min_dist = float('inf')
        q.append([0] + store_loc)
        results = []
        
        while q:
            cur_dist, cur_row, cur_col = q.popleft()
            if (cur_row,cur_col) in goals and cur_dist <= min_dist:
                min_dist = cur_dist
                results.append([cur_row,cur_col])
                continue
            
            for n_row, n_col in [(cur_row-1, cur_col), (cur_row+1, cur_col), (cur_row, cur_col-1), (cur_row, cur_col+1)]:
                if n_row <= 0 or n_row > max_size or n_col <=0 or n_col>max_size: continue
                if cur_visited[n_row][n_col]: continue
                q.append([cur_dist+1, n_row, n_col])
                if (n_row, n_col) in goals: continue
                cur_visited[n_row][n_col] = True
        
        results.sort()
        next_loc = results[0]
        people_loc[person_num] = next_loc

def check_arrived():
    global arrived
    for person_num, person_loc in list(people_loc.items()):
        if is_arrived[person_num]: continue
        if person_loc == stores[person_num]:
            arrived +=1
            is_arrived[person_num] = True


while arrived < num_people:
    time+=1
    move_people()
    check_arrived()
    enter_basecamp(time)

print(time)
from collections import defaultdict, deque
from heapq import heappush, heappop

board_size, num_turns, num_santas, rudolph_power, santa_power = map(int, input().split())
rudolph_row, rudolph_col = map(int, input().split())

rudolph_dirs = [(-1,0),(0,1),(1,0),(0,-1), (-1,-1), (-1,1), (1,1), (1,-1)]
santa_dirs = [(-1,0),(0,1),(1,0),(0,-1)]

santa_locs = defaultdict()
santa_scores = defaultdict(int)
santa_status = defaultdict(int)
santa_exists = [[0 for _ in range(board_size+1)] for _ in range(board_size+1)]

for _ in range(num_santas):
    num, row, col = map(int, input().split())
    santa_locs[num] = [(row, col)]
    santa_exists[row][col] = num

def find_dir(cur_row, cur_col, n_row, n_col):
    if cur_row == n_row or cur_col == n_col:
        if cur_row > n_row:
            return 0
        elif cur_col < n_col:
            return 1
        elif cur_row < n_row:
            return 2
        else:
            return 3
    else:
        if cur_row > n_row and cur_col > n_col:
            return 4
        elif cur_row > n_row and cur_col < n_col:
            return 5
        elif cur_row < n_row and cur_col < n_col:
            return 6
        else:
            return 7

def rudolph_move(trun, row, col):
    global santa_exists
    pq = []
    for santa_num,santa_loc in santa_locs.items():
        if santa_status[santa_num] != turn:
            continue
        dist = (row-santa_loc[0][0])**2 + (col-santa_loc[0][1])**2
        heappush(pq, (dist, (-santa_loc[0][0], -santa_loc[0][1])))
    if not pq:
        return row, col
    dist, n_loc = heappop(pq)
    t_row, t_col = -n_loc[0], -n_loc[1]
    move_dir = find_dir(row, col, t_row, t_col)
    print(move_dir)

    if row + rudolph_dirs[move_dir][0] == t_row and col + rudolph_dirs[move_dir][1] == t_col:
        santa_num = santa_exists[t_row][t_col]
        cur_row, cur_col = t_row, t_col
        santa_exists[cur_row][cur_col] = 0
        is_first = True
        while santa_num > 0:
            if is_first:
                santa_scores[santa_num] += rudolph_power
            steps = rudolph_power if is_first else 1
            n_row = cur_row + rudolph_dirs[move_dir][0] * steps
            n_col = cur_col + rudolph_dirs[move_dir][1] * steps
            if n_row <= 0 or n_row > board_size or n_col <= 0 or n_col > board_size:
                santa_status[santa_num] = -1
                santa_locs[santa_num] = [(-1,-1)]
                break
            santa_status[santa_num] = turn + 2 if is_first else turn
            if is_first:
                is_first = False
            santa_num_at_arrival = santa_exists[n_row][n_col]
            cur_row, cur_col = n_row, n_col
            santa_exists[cur_row][cur_col] = santa_num
            santa_locs[santa_num] = [(cur_row, cur_col)]
            santa_num = santa_num_at_arrival

    return row + rudolph_dirs[move_dir][0], col + rudolph_dirs[move_dir][1]

def santa_move(turn, t_row, t_col):
    for num in range(1, num_santas+1):
        if santa_status[num] != turn: 
            continue
        cur_row, cur_col = santa_locs[num][0]
        cur_dist = (t_row-cur_row)**2 + (t_col-cur_col)**2
        #방향 찾기
        is_moved = False
        move_dir = -1
        for idx, dir_info in enumerate(santa_dirs):
            n_row, n_col = cur_row + dir_info[0], cur_col + dir_info[1]
            if n_row <= 0 or n_row > board_size or n_col <= 0 or n_col > board_size:
                continue
            if santa_exists[n_row][n_col] > 0 :
                continue
            n_dist = (t_row-n_row)**2 + (t_col-n_col)**2
            if n_dist < cur_dist:
                cur_dist = n_dist
                move_dir = idx
                is_moved = True
        
        if not is_moved:
            continue

        n_row = cur_row + santa_dirs[move_dir][0]
        n_col = cur_col + santa_dirs[move_dir][1]
        santa_exists[cur_row][cur_col] = 0
        santa_locs[num] = [(n_row, n_col)]
        cur_row, cur_col = n_row, n_col
        santa_exists[cur_row][cur_col] = num

        if cur_row == t_row and cur_col == t_col:
            #산타->루돌프 충돌
            santa_num = num
            santa_exists[cur_row][cur_col] = 0
            move_dir = (move_dir+2) % 4
            while santa_num > 0:
                if santa_num == num:
                    santa_scores[santa_num] += santa_power
                steps = 1 if santa_num != num else santa_power
                n_row = cur_row + santa_dirs[move_dir][0] * steps
                n_col = cur_col + santa_dirs[move_dir][1] * steps
                if n_row <= 0 or n_row > board_size or n_col <= 0 or n_col > board_size:
                    santa_status[santa_num] = -1
                    santa_locs[santa_num] = [(-1,-1)]
                    break
                santa_status[santa_num] = turn + 2 if santa_num == num else turn
                santa_num_at_arrival = santa_exists[n_row][n_col]
                cur_row, cur_col = n_row, n_col
                santa_exists[cur_row][cur_col] = santa_num
                santa_locs[santa_num] = [(cur_row, cur_col)]
                santa_num = santa_num_at_arrival

def finish_turn(turn):
    is_done = True
    for num in range(1, num_santas+1):
        if santa_status[num]== -1:
            continue
        is_done = False
        santa_scores[num] += 1
        
        if santa_status[num] == turn:
            santa_status[num] +=1

    return is_done

#print(santa_locs)
for turn in range(num_turns):
    #print("turn: ", turn)
    new_rudolph_row, new_rudolph_col = rudolph_move(turn, rudolph_row, rudolph_col)
    santa_move(turn, new_rudolph_row, new_rudolph_col)
    is_done = finish_turn(turn)
    #print(new_rudolph_row,new_rudolph_col)
    #print(santa_locs)
    if is_done:
        break
    rudolph_row, rudolph_col = new_rudolph_row, new_rudolph_col
print("scores: ",santa_scores)
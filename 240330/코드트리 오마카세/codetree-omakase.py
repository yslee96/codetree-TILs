from heapq import heappop, heappush

pq = []
wait_sushies = {}
guest_loc = {}
sushi_per_guest = {}
eaten_sushies = {}
num_guests, num_sushies = 0, 0

def make_sushi(time, sushi_loc, guest_name):
    global num_sushies
    num_sushies +=1
    cur_guest_loc = guest_loc.get(guest_name, -1)
    if cur_guest_loc >=0:
        heappush(pq, ( time + (cur_guest_loc - sushi_loc) % belt_size, guest_name ))
    else:
        if guest_name not in wait_sushies:
            wait_sushies[guest_name] = [] 
        heappush(wait_sushies[guest_name], (sushi_loc-time)%belt_size)

def enter_guest(time, cur_guest_loc, guest_name, suchi_cnt):
    global num_guests
    num_guests +=1
    guest_loc[guest_name] = cur_guest_loc
    sushi_per_guest[guest_name] = suchi_cnt
    
    if guest_name not in wait_sushies:
        return

    while wait_sushies[guest_name]:
        sushi_loc = heappop(wait_sushies[guest_name])
        cur_sushi_loc = (sushi_loc + time) % belt_size
        heappush(pq, (time + (cur_guest_loc - cur_sushi_loc) % belt_size, guest_name) )

def take_picture(time):
    global num_guests, num_sushies
    while pq and pq[0][0] <= time:
        _, guest_name = heappop(pq)
        if guest_name not in eaten_sushies:
            eaten_sushies[guest_name] = 0
        eaten_sushies[guest_name] +=1
        num_sushies -=1
        if eaten_sushies[guest_name] == sushi_per_guest[guest_name]:
            num_guests -=1
            guest_loc[guest_name] = -1

            
    print(num_guests, num_sushies)
    
belt_size, num_cmds = map(int, input().split())
for _ in range(num_cmds):
    cmd = list(input().strip().split())
    if cmd[0] == "100":
        make_sushi(int(cmd[1]), int(cmd[2]), cmd[3])
    elif cmd[0] == "200":
        enter_guest(int(cmd[1]), int(cmd[2]), cmd[3], int(cmd[4]))
    else:
        take_picture(int(cmd[-1]))
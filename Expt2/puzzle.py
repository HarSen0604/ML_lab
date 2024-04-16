import heapq

class Node:
    def __init__(self, state, depth, misplaced_tiles, parent):
        self.state = state
        self.depth = depth
        self.misplaced_tiles = misplaced_tiles
        self.parent = parent
        self.total_cost = depth + misplaced_tiles

    def __lt__(self, other):
        return self.total_cost < other.total_cost

def get_neighbors(current_node, final_state):
    neighbors = []
    dx = [-1, 1, 0, 0]
    dy = [0, 0, -1, 1]

    for i in range(4):
        new_x, new_y = -1, -1
        for j in range(len(current_node.state)):
            for k in range(len(current_node.state[j])):
                if current_node.state[j][k] == 0:
                    new_x = j + dx[i]
                    new_y = k + dy[i]
                    break

        if is_valid_move(new_x, new_y, len(current_node.state), len(current_node.state[0])):
            new_state = copy_state(current_node.state)
            swap(new_state, new_x, new_y, current_node.state)
            neighbor = Node(new_state, current_node.depth + 1, count_misplaced_tiles(new_state, final_state), current_node)
            neighbors.append(neighbor)

    return neighbors

def is_valid_move(x, y, num_rows, num_cols):
    return 0 <= x < num_rows and 0 <= y < num_cols

def copy_state(state):
    new_state = [row[:] for row in state]
    return new_state

def swap(state, x, y, current_state):
    temp = state[x][y]
    state[x][y] = 0
    for i in range(len(current_state)):
        for j in range(len(current_state[i])):
            if current_state[i][j] == 0:
                state[i][j] = temp
                return

def print_state(state):
    for row in state:
        print(" ".join(map(str, row)))
    print()

def print_solution(goal_node):
    path = []
    current_node = goal_node
    while current_node:
        path.append(current_node)
        current_node = current_node.parent

    step = 0
    while path:
        current_node = path.pop()
        print(f"Step {step}:")
        print_state(current_node.state)
        step += 1

def count_misplaced_tiles(state, final_state):
    count = 0
    for i in range(len(state)):
        for j in range(len(state[i])):
            if state[i][j] != 0 and state[i][j] != final_state[i][j]:
                count += 1
    return count

def solve_puzzle(initial_state, final_state):
    open_set = []
    closed_set = set()

    initial_node = Node(initial_state, 0, count_misplaced_tiles(initial_state, final_state), None)
    heapq.heappush(open_set, initial_node)

    while open_set:
        current_node = heapq.heappop(open_set)
        closed_set.add(str(current_node.state))

        if current_node.state == final_state:
            print_solution(current_node)
            return

        neighbors = get_neighbors(current_node, final_state)
        for neighbor in neighbors:
            if str(neighbor.state) not in closed_set:
                heapq.heappush(open_set, neighbor)

    print("No solution found!")

if __name__ == "__main__":
    initial_state = [
        [2, 8, 3],
        [1, 6, 4],
        [7, 0, 5]
    ]

    final_state = [
        [1, 2, 3],
        [8, 0, 4],
        [7, 6, 5]
    ]

    solve_puzzle(initial_state, final_state)

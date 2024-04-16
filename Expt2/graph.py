class Node:
    def __init__(self, label, heuristic):
        self.label = label
        self.heuristic = heuristic
        self.cost = float('inf')
        self.visited = False
        self.parent = None
        self.neighbors = []

    def add_neighbor(self, edge):
        self.neighbors.append(edge)


class Edge:
    def __init__(self, target, cost):
        self.target = target
        self.cost = cost


def a_star(start, goal):
    open_list = [start]
    closed_list = []

    start.cost = 0

    while open_list:
        current = find_lowest_cost(open_list)
        open_list.remove(current)
        closed_list.append(current)

        if current == goal:
            return current.cost

        for neighbor_edge in current.neighbors:
            neighbor = neighbor_edge.target
            tentative_cost = current.cost + neighbor_edge.cost

            if neighbor not in closed_list:
                if neighbor not in open_list or tentative_cost < neighbor.cost:
                    neighbor.cost = tentative_cost
                    neighbor.parent = current
                    if neighbor not in open_list:
                        open_list.append(neighbor)

    return -1  # No path found


def find_lowest_cost(nodes):
    lowest_cost_node = None
    lowest_cost = float('inf')

    for node in nodes:
        if node.cost + node.heuristic < lowest_cost:
            lowest_cost = node.cost + node.heuristic
            lowest_cost_node = node

    return lowest_cost_node


def get_path(start, goal):
    path = []
    current = goal

    while current:
        path.append(current)
        current = current.parent

    path.reverse()
    return path


def main():
    num_vertices = int(input("Enter the number of vertices: "))
    nodes = []

    for i in range(num_vertices):
        label, heuristic = input(f"Enter vertex details (label heuristic) for vertex {i + 1}: ").split()
        heuristic = float(heuristic)
        nodes.append(Node(label, heuristic))

    num_edges = int(input("Enter the number of edges: "))

    for i in range(num_edges):
        source_label, target_label, cost = input(f"Enter edge details (source destination cost) for edge {i + 1}: ").split()
        cost = float(cost)

        source = get_node_by_label(nodes, source_label)
        target = get_node_by_label(nodes, target_label)

        if source and target:
            source.add_neighbor(Edge(target, cost))
        else:
            print("Invalid vertex label. Please try again.")
            i -= 1  # Decrement i to re-enter the current edge

    start_label = input("Enter the start vertex label: ")
    goal_label = input("Enter the goal vertex label: ")

    start = get_node_by_label(nodes, start_label)
    goal = get_node_by_label(nodes, goal_label)

    if start and goal:
        shortest_path_cost = a_star(start, goal)

        if shortest_path_cost != -1:
            print("Shortest path cost:", shortest_path_cost)
            path = get_path(start, goal)
            print("Path:", end=" ")
            for node in path:
                print(node.label, end=" ")
            print()
        else:
            print("No path found")
    else:
        print("Invalid start or goal vertex label")


def get_node_by_label(nodes, label):
    for node in nodes:
        if node.label == label:
            return node
    return None


if __name__ == "__main__":
    main()


'''
Enter the number of vertices: 4
Enter vertex details (label heuristic) for vertex 1: A 5
Enter vertex details (label heuristic) for vertex 2: B 3
Enter vertex details (label heuristic) for vertex 3: C 2
Enter vertex details (label heuristic) for vertex 4: D 0
Enter the number of edges: 4
Enter edge details (source destination cost) for edge 1: A B 2
Enter edge details (source destination cost) for edge 2: B C 1
Enter edge details (source destination cost) for edge 3: B D 4
Enter edge details (source destination cost) for edge 4: C D 1
Enter the start vertex label: A
Enter the goal vertex label: D
'''
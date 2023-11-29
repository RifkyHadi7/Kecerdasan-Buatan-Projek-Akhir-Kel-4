import heapq

def astar(graph, start, goal):
    # Priority queue to store nodes and their f-values
    open_set = [(0, start)]
    # Set to keep track of visited nodes
    closed_set = set()
    # Dictionary to store g-values (cost from start to current node)
    g_values = {node: float('inf') for node in graph}
    g_values[start] = 0
    h_values = {node: float('inf') for node in graph}
    h_values[start] = 0
    # Dictionary to store parent nodes for constructing the path
    parents = {start: None}

    while open_set:
        # Get the node with the minimum f-value
        current_cost, current_node = heapq.heappop(open_set)

        if current_node == goal:
            # Reconstruct the path
            path = []
            while current_node is not None:
                path.insert(0, current_node)
                current_node = parents[current_node]
            return path

        # Skip if the node has already been visited
        if current_node in closed_set:
            continue

        # Add the current node to the closed set
        closed_set.add(current_node)

        # Explore neighbors
        for neighbor in graph[current_node]:
            # Calculate tentative g-value
            tentative_g = g_values[current_node] + graph[current_node][neighbor]

            if tentative_g < g_values[neighbor]:
                # Update g-value, set parent, and calculate f-value
                g_values[neighbor] = tentative_g
                parents[neighbor] = current_node
                h_values[neighbor] = heuristic(neighbor, goal, graph)
                f_value = tentative_g + heuristic(neighbor, goal, graph)
                # Add the neighbor to the open set
                heapq.heappush(open_set, (f_value, neighbor))

    # If the goal is not reached, return an empty path
    return []


def heuristic(node, goal, graph):
    # Assuming graph is represented as a dictionary of dictionaries,
    # where graph[node1][node2] gives the weight of the edge between node1 and node2.

    # Check if there is an edge between the current node and the goal node
    if goal in graph[node]:
        return graph[node][goal]
    else:
        # If there is no direct edge, find the minimum edge weight to any neighbor of the current node
        neighbors = graph[node].keys()
        if not neighbors:
            # If the current node has no neighbors, return a large value
            return float('inf')
        else:
            return min(graph[node][neighbor] for neighbor in neighbors)

# Example usage:
graph = {
    '20': {'14': 100, '13': 100, '21': 70},
    '14': {'20': 100, '13': 250},
    '13': {'14': 250, '20': 100, '21': 170, '30': 70, '12': 180, '15': 400},
    '12': {'13': 180, '15': 350},
    '15': {'12': 350, '13': 400, '34': 70},
    '21': {'20': 70, '13': 170, '30': 210},
    '30': {'13': 70, '21': 210, '35': 80},
    '34': {'15': 70, '17': 110},
    '35': {'30': 80, '17': 160},
    '17': {'34': 110, '35': 160},
}

start_node = input("Masukkan titik awal: ")
goal_node = input("Masukkan titik tujuan: ")

path = astar(graph, start_node, goal_node)
if path:
    print(f"Optimal path from {start_node} to {goal_node}: {path}")
    total_cost = sum(graph[path[i]][path[i+1]] for i in range(len(path)-1))
    print(f"Total cost: {total_cost}")
else:
    print(f"No path from {start_node} to {goal_node}")

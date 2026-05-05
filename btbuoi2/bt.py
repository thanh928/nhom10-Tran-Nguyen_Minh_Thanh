from typing import List, Tuple, Dict, Optional
import heapq
from math import inf

import numpy as np
import matplotlib.pyplot as plt


WALKABLE_COSTS = {
    0: 1,  # empty
    2: 3,  # mud
    3: 5,  # rock
}
OBSTACLE = 1
PATH_MARK = 8


def create_node(
    position: Tuple[int, int],
    g: float = inf,
    h: float = 0.0,
    parent: Optional[Dict] = None,
) -> Dict:
    return {
        "position": position,
        "g": g,
        "h": h,
        "f": g + h,
        "parent": parent,
    }


def calculate_heuristic(pos1: Tuple[int, int], pos2: Tuple[int, int]) -> float:
    x1, y1 = pos1
    x2, y2 = pos2
    # Manhattan distance (4-directional movement)
    return abs(x2 - x1) + abs(y2 - y1)


def get_valid_neighbors(
    grid: np.ndarray, position: Tuple[int, int]
) -> List[Tuple[int, int]]:
    x, y = position
    rows, cols = grid.shape
    possible_moves = [
        (x + 1, y),
        (x - 1, y),
        (x, y + 1),
        (x, y - 1),
    ]
    neighbors: List[Tuple[int, int]] = []
    for nx, ny in possible_moves:
        if 0 <= nx < rows and 0 <= ny < cols and grid[nx, ny] != OBSTACLE:
            neighbors.append((nx, ny))
    return neighbors


def movement_cost(grid: np.ndarray, position: Tuple[int, int]) -> float:
    cell_value = int(grid[position[0], position[1]])
    if cell_value in WALKABLE_COSTS:
        return WALKABLE_COSTS[cell_value]
    # Treat unknown values as non-walkable
    return inf


def reconstruct_path(goal_node: Dict) -> List[Tuple[int, int]]:
    path = []
    current = goal_node
    while current is not None:
        path.append(current["position"])
        current = current["parent"]
    return path[::-1]


def find_path(
    grid: np.ndarray, start: Tuple[int, int], goal: Tuple[int, int]
) -> List[Tuple[int, int]]:
    if grid[start[0], start[1]] == OBSTACLE or grid[goal[0], goal[1]] == OBSTACLE:
        return []

    start_node = create_node(position=start, g=0, h=calculate_heuristic(start, goal))
    # Priority queue ordered by f = g + h
    open_list = [(start_node["f"], start)]
    open_dict = {start: start_node}
    closed_set = set()

    while open_list:
        current_f, current_pos = heapq.heappop(open_list)
        if current_pos not in open_dict:
            continue
        current_node = open_dict[current_pos]
        if current_f != current_node["f"]:
            continue

        if current_pos == goal:
            return reconstruct_path(current_node)

        closed_set.add(current_pos)

        for neighbor_pos in get_valid_neighbors(grid, current_pos):
            if neighbor_pos in closed_set:
                continue

            step_cost = movement_cost(grid, neighbor_pos)
            if step_cost == inf:
                continue
            tentative_g = current_node["g"] + step_cost

            if neighbor_pos not in open_dict:
                neighbor = create_node(
                    position=neighbor_pos,
                    g=tentative_g,
h=calculate_heuristic(neighbor_pos, goal),
                    parent=current_node,
                )
                open_dict[neighbor_pos] = neighbor
                heapq.heappush(open_list, (neighbor["f"], neighbor_pos))
            elif tentative_g < open_dict[neighbor_pos]["g"]:
                neighbor = open_dict[neighbor_pos]
                neighbor["g"] = tentative_g
                neighbor["f"] = tentative_g + neighbor["h"]
                neighbor["parent"] = current_node
                heapq.heappush(open_list, (neighbor["f"], neighbor_pos))

    return []


def visualize_path(grid: np.ndarray, path: List[Tuple[int, int]]) -> None:
    grid_copy = np.copy(grid)
    for x, y in path:
        grid_copy[x][y] = PATH_MARK

    render_map = {
        0: "0",
        1: "1",
        2: "2",
        3: "3",
        PATH_MARK: "*",
    }

    for row in grid_copy:
        print("".join(render_map.get(int(cell), "?") for cell in row))


def plot_grid(grid: np.ndarray, path: List[Tuple[int, int]]) -> None:
    fig, ax = plt.subplots()
    ax.imshow(grid, cmap="Greys", interpolation="none")

    if path:
        path_x = [p[1] for p in path]
        path_y = [p[0] for p in path]
        ax.plot(
            path_x,
            path_y,
            color="red",
            marker="o",
            markersize=6,
            linewidth=2,
            label="Path",
        )
        start = path[0]
        goal = path[-1]
        ax.plot(start[1], start[0], color="green", marker="s", markersize=8, label="Start")
        ax.plot(goal[1], goal[0], color="blue", marker="s", markersize=8, label="Goal")

    ax.legend()
    plt.show()


def main() -> None:
    # 0: empty (cost=1), 1: obstacle, 2: mud (cost=3), 3: rock (cost=5)
    grid = np.zeros((20, 20), dtype=int)

    # Obstacles
    grid[5:15, 10] = 1  # vertical wall
    grid[5, 5:15] = 1  # horizontal wall

    # Higher-cost terrains
    grid[12:16, 3:8] = 2  # mud zone
    grid[2:6, 14:18] = 3  # rock zone

    start_pos = (2, 2)
    goal_pos = (18, 18)

    path = find_path(grid, start_pos, goal_pos)
    if path:
        total_cost = sum(movement_cost(grid, pos) for pos in path[1:])
        print(f"Path found with {len(path)} steps. Total cost = {total_cost}")
        visualize_path(grid, path)
        plot_grid(grid, path)
    else:
        print("No path found!")


if __name__ == "__main__":
    main()
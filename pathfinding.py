from heapq import heappush, heappop

SQRT2 = 1.41421356237 

class PathFinding:
    def __init__(self, game):
        self.game = game
        self.map = game.map.mini_map
        self.dirs = [(-1, 0), (0, -1), (1, 0), (0, 1),
                     (-1, -1), (1, -1), (1, 1), (-1, 1)]

    def get_path(self, start, goal):
        visited = self.a_star(start, goal)
        if goal not in visited:
            return start
        path = [goal]
        step = visited[goal]
        while step != start:
            path.append(step)
            step = visited[step]
        path.reverse()
        return path[1] if len(path) > 1 else start

    def a_star(self, start, goal):
        open_set = []
        heappush(open_set, (0, start))
        came_from = {}
        g_score = {start: 0}

        while open_set:
            _, current = heappop(open_set)
            if current == goal:
                break

            for neighbor, cost in self.get_neighbors(current):
                tentative_g = g_score[current] + cost
                if neighbor not in g_score or tentative_g < g_score[neighbor]:
                    g_score[neighbor] = tentative_g
                    f_score = tentative_g + self.heuristic(neighbor, goal)
                    heappush(open_set, (f_score, neighbor))
                    came_from[neighbor] = current
        return came_from

    def get_neighbors(self, pos):
        x, y = pos
        result = []
        world = self.game.map.world_map
        npc = self.game.object_handler.npc_positions

        for dx, dy in self.dirs:
            nx, ny = x + dx, y + dy
            if (nx, ny) in world or (nx, ny) in npc:
                continue

            if dx != 0 and dy != 0:
                if (x + dx, y) in world or (x, y + dy) in world:
                    continue
                cost = SQRT2
            else:
                cost = 1
            result.append(((nx, ny), cost))
        return result

    def heuristic(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

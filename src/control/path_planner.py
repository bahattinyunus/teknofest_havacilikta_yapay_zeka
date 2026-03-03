import numpy as np
import heapq

class PathPlanner:
    def __init__(self, grid_size=(50, 50), resolution=1.0, inflation_radius=2.0):
        """
        grid_size: (rows, cols)
        resolution: meters per cell
        inflation_radius: meters
        """
        self.grid_size = grid_size
        self.resolution = resolution
        self.inflation_radius = inflation_radius
        self.grid = np.zeros(grid_size) # 0: free, 1: obstacle
        
    def add_obstacle(self, x, y, radius=1.0):
        # Convert world coordinates to grid coordinates
        row = int(y / self.resolution + self.grid_size[0] / 2)
        col = int(x / self.resolution + self.grid_size[1] / 2)
        
        # Inflate obstacle for safety
        total_radius = radius + self.inflation_radius
        r_cells = int(total_radius / self.resolution)
        
        for i in range(max(0, row - r_cells), min(self.grid_size[0], row + r_cells + 1)):
            for j in range(max(0, col - r_cells), min(self.grid_size[1], col + r_cells + 1)):
                dist = np.sqrt((i - row)**2 + (j - col)**2) * self.resolution
                if dist <= total_radius:
                    self.grid[i, j] = 1

    def plan(self, start_world, goal_world):
        start = (int(start_world[1] / self.resolution + self.grid_size[0] / 2),
                 int(start_world[0] / self.resolution + self.grid_size[1] / 2))
        goal = (int(goal_world[1] / self.resolution + self.grid_size[0] / 2),
                int(goal_world[0] / self.resolution + self.grid_size[1] / 2))
        
        # Bounds check
        start = (max(0, min(self.grid_size[0]-1, start[0])), max(0, min(self.grid_size[1]-1, start[1])))
        goal = (max(0, min(self.grid_size[0]-1, goal[0])), max(0, min(self.grid_size[1]-1, goal[1])))

        path = self._a_star(start, goal)
        
        if path:
            # Path Smoothing
            smoothed_path = self._smooth_path(path)
            
            # Convert back to world coords
            world_path = []
            for p in smoothed_path:
                wx = (p[1] - self.grid_size[1] / 2) * self.resolution
                wy = (p[0] - self.grid_size[0] / 2) * self.resolution
                world_path.append((wx, wy))
            return world_path
        return None

    def _smooth_path(self, path):
        if len(path) < 3: return path
        smoothed = [path[0]]
        for i in range(1, len(path) - 1):
            # Simple averaging for smoothing
            prev = np.array(path[i-1])
            curr = np.array(path[i])
            nxt = np.array(path[i+1])
            new_pt = (prev + curr + nxt) / 3.0
            smoothed.append(tuple(new_pt))
        smoothed.append(path[-1])
        return smoothed

    def _a_star(self, start, goal):
        def heuristic(a, b):
            return np.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)

        close_set = set()
        came_from = {}
        gscore = {start: 0}
        fscore = {start: heuristic(start, goal)}
        oheap = []

        heapq.heappush(oheap, (fscore[start], start))
 
        while oheap:
            current = heapq.heappop(oheap)[1]

            if current == goal:
                data = []
                while current in came_from:
                    data.append(current)
                    current = came_from[current]
                return data[::-1]

            close_set.add(current)
            for i, j in [(0,1),(0,-1),(1,0),(-1,0),(1,1),(1,-1),(-1,1),(-1,-1)]:
                neighbor = current[0] + i, current[1] + j            
                
                if not (0 <= neighbor[0] < self.grid_size[0] and 0 <= neighbor[1] < self.grid_size[1]):
                    continue

                if self.grid[neighbor[0], neighbor[1]] == 1:
                    continue

                tentative_g_score = gscore[current] + heuristic(current, neighbor)
 
                if neighbor in close_set and tentative_g_score >= gscore.get(neighbor, 0):
                    continue
 
                if tentative_g_score < gscore.get(neighbor, 0) or neighbor not in [i[1] for i in oheap]:
                    came_from[neighbor] = current
                    gscore[neighbor] = tentative_g_score
                    fscore[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                    heapq.heappush(oheap, (fscore[neighbor], neighbor))
                
        return False

import numpy as np
import heapq

class PathPlanner:
    def __init__(self, grid_size=(50, 50), resolution=1.0):
        """
        grid_size: (rows, cols)
        resolution: meters per cell
        """
        self.grid_size = grid_size
        self.resolution = resolution
        self.grid = np.zeros(grid_size) # 0: free, 1: obstacle
        
    def add_obstacle(self, x, y, radius=1.0):
        # Convert world coordinates to grid coordinates
        # Simplified: (0,0) is center of grid
        row = int(y / self.resolution + self.grid_size[0] / 2)
        col = int(x / self.resolution + self.grid_size[1] / 2)
        
        r_cells = int(radius / self.resolution)
        
        for i in range(max(0, row - r_cells), min(self.grid_size[0], row + r_cells + 1)):
            for j in range(max(0, col - r_cells), min(self.grid_size[1], col + r_cells + 1)):
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
            # Convert back to world coords
            world_path = []
            for p in path:
                wx = (p[1] - self.grid_size[1] / 2) * self.resolution
                wy = (p[0] - self.grid_size[0] / 2) * self.resolution
                world_path.append((wx, wy))
            return world_path
        return None

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
                tentative_g_score = gscore[current] + heuristic(current, neighbor)
                
                if 0 <= neighbor[0] < self.grid_size[0]:
                    if 0 <= neighbor[1] < self.grid_size[1]:                
                        if self.grid[neighbor[0], neighbor[1]] == 1:
                            continue
                    else:
                        continue
                else:
                    continue
 
                if neighbor in close_set and tentative_g_score >= gscore.get(neighbor, 0):
                    continue
 
                if  tentative_g_score < gscore.get(neighbor, 0) or neighbor not in [i[1]for i in oheap]:
                    came_from[neighbor] = current
                    gscore[neighbor] = tentative_g_score
                    fscore[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                    heapq.heappush(oheap, (fscore[neighbor], neighbor))
                
        return False

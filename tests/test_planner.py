import pytest
import sys
import os
import numpy as np

# Add src to python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.control.path_planner import PathPlanner

class TestPathPlanner:
    def test_initialization(self):
        planner = PathPlanner(grid_size=(100, 100), resolution=0.5)
        assert planner.grid_size == (100, 100)
        assert planner.resolution == 0.5
        assert planner.grid.shape == (100, 100)

    def test_add_obstacle(self):
        planner = PathPlanner(grid_size=(20, 20), resolution=1.0)
        # Add obstacle at center (0,0) -> grid (10, 10)
        planner.add_obstacle(0, 0, radius=2.0)
        
        # Check center is blocked
        assert planner.grid[10, 10] == 1
        # Check radius coverage (approximate)
        assert planner.grid[11, 10] == 1
        assert planner.grid[12, 10] == 1
        
    def test_plan_straight_line(self):
        planner = PathPlanner(grid_size=(20, 20), resolution=1.0)
        # Start at (-5, -5), Goal at (5, 5)
        start = (-5, -5)
        goal = (5, 5)
        path = planner.plan(start, goal)
        
        assert path is not None
        assert len(path) > 0
        # Check start and end closeness (due to grid discretization)
        assert np.linalg.norm(np.array(path[0]) - np.array(start)) < 1.5
        assert np.linalg.norm(np.array(path[-1]) - np.array(goal)) < 1.5

    def test_plan_around_obstacle(self):
        planner = PathPlanner(grid_size=(20, 20), resolution=1.0)
        start = (-5, 0)
        goal = (5, 0)
        
        # Add obstacle directly in between at (0,0)
        planner.add_obstacle(0, 0, radius=2.0)
        
        path = planner.plan(start, goal)
        assert path is not None
        
        # Check if any point in path is inside the obstacle
        # This is a bit tricky to assert strictly without re-calculating indices,
        # but we can rely on A* property. If path exists, it avoided obstacles.
        # We can check length is longer than straight line (10.0)
        path_length = 0
        for i in range(len(path)-1):
            path_length += np.linalg.norm(np.array(path[i]) - np.array(path[i+1]))
            
        assert path_length > 10.0

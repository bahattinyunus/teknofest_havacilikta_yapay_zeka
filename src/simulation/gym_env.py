import gym
from gym import spaces
import numpy as np
import cv2

class SkyGuardEnv(gym.Env):
    """
    Custom Environment that follows gym interface.
    This simulates a drone trying to reach a target point.
    """
    metadata = {'render.modes': ['human']}

    def __init__(self):
        super(SkyGuardEnv, self).__init__()
        
        # Action space: [Roll, Pitch, Yaw, Throttle]
        # Normalized between -1 and 1
        self.action_space = spaces.Box(low=-1, high=1, shape=(4,), dtype=np.float32)
        
        # Observation space: 
        # [x, y, z, vx, vy, vz, target_x, target_y, target_z]
        self.observation_space = spaces.Box(low=-np.inf, high=np.inf, shape=(9,), dtype=np.float32)
        
        self.state = None
        self.target = np.array([0, 0, 10]) # Target altitude 10m
        self.max_steps = 500
        self.current_step = 0
        self.dt = 0.1 # 10Hz

    def reset(self):
        # Reset drone state [x, y, z, vx, vy, vz]
        self.state = np.array([0, 0, 0, 0, 0, 0], dtype=np.float32)
        self.current_step = 0
        return self._get_obs()

    def step(self, action):
        self.current_step += 1
        
        # Unpack action
        roll_cmd, pitch_cmd, yaw_cmd, throttle_cmd = action
        
        # Simple Physics Model (Kinematics)
        x, y, z, vx, vy, vz = self.state
        
        # Acceleration based on angle (Simplified)
        ax = 0.5 * pitch_cmd 
        ay = 0.5 * roll_cmd
        az = (throttle_cmd + 1) * 0.5 * 2.0 - 9.81 * 0.1 # Gravity offset
        
        # Integration
        vx += ax * self.dt
        vy += ay * self.dt
        vz += az * self.dt
        
        x += vx * self.dt
        y += vy * self.dt
        z += vz * self.dt
        
        # Ground collision
        if z < 0: z = 0; vz = 0
        
        self.state = np.array([x, y, z, vx, vy, vz], dtype=np.float32)
        
        # Reward Calculation
        dist_to_target = np.linalg.norm(self.state[:3] - self.target)
        reward = -dist_to_target # Negative distance as reward (get closer)
        
        # Bonus for being close
        if dist_to_target < 1.0:
            reward += 10.0
            done = True
        else:
            done = False
            
        if self.current_step >= self.max_steps:
            done = True
            
        info = {"dist": dist_to_target}
        
        return self._get_obs(), reward, done, info

    def _get_obs(self):
        return np.concatenate((self.state, self.target))

    def render(self, mode='human'):
        # Simple visualizer using OpenCV
        img = np.zeros((400, 400, 3), dtype=np.uint8)
        
        # Map X, Y to pixel coordinates (Scale 10px = 1m)
        center_x, center_y = 200, 200
        drone_x = int(center_x + self.state[0] * 10)
        drone_y = int(center_y + self.state[1] * 10)
        
        target_x = int(center_x + self.target[0] * 10)
        target_y = int(center_y + self.target[1] * 10)
        
        # Draw Target
        cv2.circle(img, (target_x, target_y), 5, (0, 255, 0), -1)
        
        # Draw Drone
        cv2.circle(img, (drone_x, drone_y), 3, (0, 0, 255), -1)
        
        cv2.putText(img, f"Alt: {self.state[2]:.2f}m", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        cv2.imshow("SkyGuard RL Environment", img)
        cv2.waitKey(1)

    def close(self):
        cv2.destroyAllWindows()

if __name__ == "__main__":
    # Test Policy
    env = SkyGuardEnv()
    obs = env.reset()
    for _ in range(200):
        action = env.action_space.sample() # Random action
        obs, reward, done, info = env.step(action)
        env.render()
        if done:
            print("Episode Finished")
            obs = env.reset()
    env.close()

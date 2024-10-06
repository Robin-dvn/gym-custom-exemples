import gymnasium as gym
from gymnasium import spaces
import numpy as np
import pygame

class GridWorld(gym.Env):
    metadata = {"render_mode":["human"],"render_fps":4}

    def __init__(self,size=5, render_mode=None):
        self.window_size = 512
        assert render_mode is None or render_mode in self.metadata["render_mode"]
        self.render_mode = render_mode

        self.size = size
        self.observation_space = spaces.Dict(
            {
                "agent": spaces.Box(0,size-1,shape=(2,),dtype=int),
                "target": spaces.Box(0,size-1,shape=(2,),dtype=int)
            }
        )

        self.action_space = spaces.Discrete(4)

        self._action_to_direction = {
            0 : np.array([1,0]),
            1 : np.array([0,1]),
            2 : np.array([-1,0]),
            3 : np.array([0,-1])
        }

        self.window = None
        self.clock = None
    


    def _get_obs(self):
        return  {"agent" : self._agent_location, "target": self._target_location}
    
    def _get_info(self):
        return 2
    

    def reset(self, seed):
        super().reset(seed=seed)


        self._agent_location =  self.np_random.integers(0, self.size, size=2, dtype=int)

        self._target_location =  self._agent_location
        while np.array_equal(self._target_location, self._agent_location):
            self._target_location = self.np_random.integers(
                0, self.size, size=2, dtype=int
            )

        if self.render_mode == "human":
            self._render_frame()

        obs = self._get_obs()
        info = self._get_info()

        return obs, info
    
    def step(self,action):

        direction = self._action_to_direction(action)

        self._agent_location += direction

        terminated = np.array_equal(self._agent_location, self._target_location)
        reward = 1 if terminated else 0  # Binary sparse rewards

        obs = self._get_obs()
        info = self._get_info()

        if self.render_mode == "human":
            self._render_frame()

        return obs,reward,terminated,False,info

    def close(self):
        if self.window is not None:
            pygame.display.quit()
            pygame.quit()

    def render(self):
        if self.render_mode == "rgb_array":
            return self._render_frame()

    def _render_frame(self):
        if self.window is None and self.render_mode == "human":
            pygame.init()
            pygame.display.init()
            self.window = pygame.display.set_mode(
                (self.window_size, self.window_size)
            )

        if self.clock is None and self.render_mode == "human":
            self.clock = pygame.time.Clock()

        canvas = pygame.Surface((self.window_size, self.window_size))
        canvas.fill((255, 255, 255))
        pix_square_size = (
            self.window_size / self.size
        )  # The size of a single grid square in pixels

        # First we draw the target
        pygame.draw.rect(
            canvas,
            (255, 0, 0),
            pygame.Rect(
                pix_square_size * self._target_location,
                (pix_square_size, pix_square_size),
            ),
        )
        # Now we draw the agent
        pygame.draw.circle(
            canvas,
            (0, 0, 255),
            (self._agent_location + 0.5) * pix_square_size,
            pix_square_size / 3,
        )

        # Finally, add some gridlines
        for x in range(self.size + 1):
            pygame.draw.line(
                canvas,
                0,
                (0, pix_square_size * x),
                (self.window_size, pix_square_size * x),
                width=3,
            )
            pygame.draw.line(
                canvas,
                0,
                (pix_square_size * x, 0),
                (pix_square_size * x, self.window_size),
                width=3,
            )

        if self.render_mode == "human":
            # The following line copies our drawings from `canvas` to the visible window
            self.window.blit(canvas, canvas.get_rect())
            pygame.event.pump()
            pygame.display.update()

            # We need to ensure that human-rendering occurs at the predefined framerate.
            # The following line will automatically add a delay to keep the framerate stable.
            self.clock.tick(self.metadata["render_fps"])
        else:  # rgb_array
            return np.transpose(
                np.array(pygame.surfarray.pixels3d(canvas)), axes=(1, 0, 2)
            )
import gymnasium as gym
import numpy as np
import pygame

from gymnasium import spaces

class GymWalk(gym.Env):
    metadata = {"render_modes": ["human","rgb_array"],"render_fps":1}

    def __init__(self,render_mode=None):
        self.window_size = 512
        self.observation_space = spaces.Discrete(7,start=0)
        self.action_space = spaces.Discrete(2)

        self._action_to_direction = {
            0: -1,
            1: 1,
        }

        assert render_mode is None or render_mode in self.metadata["render_modes"]
        self.render_mode = render_mode

        self.window = None
        self.clock = None
    
    def _get_obs(self):
        return self.agent_location
    def _get_info(self):
        return {"info":2}
    
    def reset(self,seed = None,options = None):
        super().reset(seed=seed)

        self.agent_location = self.np_random.integers(1,5,dtype=int)
        
        observation = self._get_obs()
        info = self._get_info()

        if self.render_mode == "human":
            self._render_frame()
        
        
        return observation, info
    
    def step(self, action):
        direction = self._action_to_direction[action]
        self.agent_location =self.agent_location+ direction
        terminated = False


        if self.agent_location == 0 or self.agent_location == 6:
            terminated = True
        
        reward = 0
        if terminated:
            if self.agent_location == 6:
                reward = 1
            else:
                reward = -1
        
        observation = self._get_obs()
        info = self._get_info()

        if self.render_mode == "human":
            self._render_frame()

        return observation, reward,terminated,False,info
    
    def render(self):
        if self.render_mode == "rgb_array":
            return self.render_frame()
    
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
            self.window_size / 7
        )  # The size of a single grid square in pixels

        # First we draw the target
        pygame.draw.rect(
            canvas,
            (255, 0, 255),
            pygame.Rect(6*pix_square_size,0,pix_square_size,pix_square_size),
        )
        pygame.draw.rect(
            canvas,
            (255, 0, 0),
            pygame.Rect(0,0,pix_square_size,pix_square_size),
        )
        pygame.draw.circle(
            canvas,
            (0, 0, 255),
            (self.agent_location * pix_square_size + pix_square_size/2,pix_square_size/2),
            pix_square_size / 3,

        )

            # Finally, add some gridlines
        for x in range(8):
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

    def close(self):
        if self.window is not None:
            pygame.display.quit()
            pygame.quit()
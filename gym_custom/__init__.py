from gymnasium.envs.registration import register

register(
     id="GymWalk-v0",
     entry_point="gym_custom.envs:GymWalk",
     max_episode_steps=300,
)
register(
     id="GymWalk19-v0",
     entry_point="gym_custom.envs:GymWalk19",
     max_episode_steps=300,
)
register(
    id="GridWorld-v0",
    entry_point="gym_custom.envs:GridWorld",
    max_episode_steps=1000

)
from setuptools import setup

setup(
    name="gym_custom",
    version="0.0.4.4.9",
    packages=['gym_custom', 'gym_custom.envs'],
    install_requires=["gymnasium", "pygame"],
)
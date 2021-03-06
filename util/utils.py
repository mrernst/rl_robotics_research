#!/usr/bin/python
# _____________________________________________________________________________

# ----------------
# import libraries
# ----------------

# standard libraries
# -----
import torch
import numpy as np

import gym
from gym import Wrapper
from collections import OrderedDict

# utilities
# -----
from env.mujoco.maze_env_utils import construct_maze

# custom functions
# -----

# TODO this should be configureable and thus be part of the config?
class SubgoalActionSpace(object):
    def __init__(self, dim):
        limits = np.array(
            [-10, -10, -0.5, 
            #[-4, -4, -0.5, 
            -1, -1, -1, -1,
            -0.5, -0.3, -0.5, -0.3, -0.5, -0.3, -0.5, -0.3])
        self.shape = (dim,1)
        self.low = limits[:dim]
        self.high = -self.low

    def sample(self):
        return (self.high - self.low) * np.random.sample(self.high.shape) + self.low

class Subgoal(object):
    def __init__(self, dim=15):
        self.action_space = SubgoalActionSpace(dim)
        self.action_dim = self.action_space.shape[0]


def _is_update(episode, freq, ignore=0, rem=0):
    if episode!=ignore and episode%freq==rem:
        return True
    return False


def get_obs_array(state, combined=False):
    try:
        if combined:
            np.concatenate([state[k] for k in state.keys()])
        else:
            state = state['observation']
    except:
        pass
    
    return state



def visualize_goalspace(grid, state_encoder, state_trajectory, goal_trajectory):
    # this function is planned take a grid within the 2D or 3D position space of the environment
    # (may be different for a different environment) and uses the state encoder network to encode
    # and then visualizes the grid using a pacmap with euclidean distance encoded with color
    # could also draw the path taken in the subgoal space
    fig = None
    return fig


# def visualize_eval_trajectories(env_name, overlay=True):
#     maze_structure = construct_maze(env_name)
#     size = 2,4,8 for v2, v1, v0
#     pass

def visualize_endpoints():
    pass

def draw_2d_env_map():
    pass
    
    
def _compose_alpha(img_in, img_layer, opacity):
    """Calculate alpha composition ratio between two images.
    """
    
    comp_alpha = np.minimum(img_in[:, :, 3], img_layer[:, :, 3]) * opacity
    new_alpha = img_in[:, :, 3] + (1.0 - img_in[:, :, 3]) * comp_alpha
    np.seterr(divide='ignore', invalid='ignore')
    ratio = comp_alpha / new_alpha
    ratio[ratio == np.nan] = 0.0
    return ratio

def darken(img_in, img_layer, opacity):
    """
    Apply darken only blending mode of a layer on an image.
    """
        
    img_in_norm = img_in / 255.0
    img_layer_norm = img_layer / 255.0
    
    ratio = _compose_alpha(img_in_norm, img_layer_norm, opacity)
    
    comp = np.minimum(img_in_norm[:, :, :3], img_layer_norm[:, :, :3])
    
    ratio_rs = np.reshape(np.repeat(ratio, 3), [comp.shape[0], comp.shape[1], comp.shape[2]])
    img_out = comp * ratio_rs + img_in_norm[:, :, :3] * (1.0 - ratio_rs)
    img_out = np.nan_to_num(np.dstack((img_out, img_in_norm[:, :, 3])))  # add alpha channel and replace nans
    return img_out * 255.0

# wrapper to make standard environments 'goal-based' by providing a 
# fake goal in order to test the flat agent
class MakeGoalBased(Wrapper):
    def __init__(self, env):
        super(MakeGoalBased, self).__init__(env)
        ob_space = env.observation_space
        self.goal_space = gym.spaces.Box(low=np.array([0,0]), high=np.array([1,1]))
        self.observation_space = gym.spaces.Dict(OrderedDict({
            'observation': ob_space,
            'desired_goal': self.goal_space,
            'achieved_goal': self.goal_space,
        }))
        self._max_episode_steps = self.env._max_episode_steps
    def step(self, action):
        #print(action, action.shape)
        observation, reward, done, info = self.env.step(action)
        out = {'observation': observation,
               'desired_goal': np.array([0,0]),
               'achieved_goal': np.array([0,0])}
        return out, reward, done, info
    
    def reset(self):
        observation = self.env.reset()
    
        out = {'observation': observation,
               'desired_goal': np.array([0,0]),
               'achieved_goal': np.array([0,0])}
        return out


# custom classes
# -----


# ----------------
# main program
# ----------------

if __name__ == "__main__":
    pass


# _____________________________________________________________________________

# Stick to 80 characters per line
# Use PEP8 Style
# Comment your code

# -----------------
# top-level comment
# -----------------

# medium level comment
# -----

# low level comment

import gym
import random
from transformer import transform_code
from reward import heuristic_reward
from test_cases import test_cases

class CodeEnv(gym.Env):
    def __init__(self, functions, test_cases):
        self.action_space = ['optimize_loop', 'simplify_string', 'use_builtins', 'memoize']
        self.functions = [f for f in functions if f.split("def ")[1].split("(")[0] in test_cases]
        self.test_cases = test_cases
        self.current_code = None
        self.func_name = None
        self.steps = 0
        self.max_steps = 10

    def reset(self):
        self.current_code = random.choice(self.functions)
        self.func_name = self.current_code.split("def ")[1].split("(")[0]
        self.steps = 0
        return self.current_code

    def step(self, action):
        new_code = transform_code(self.current_code, action)
        reward = heuristic_reward(new_code, self.func_name, self.test_cases[self.func_name])
        self.current_code = new_code
        self.steps += 1
        done = reward > 8 or self.steps >= self.max_steps
        return new_code, reward, done, {}

if __name__ == "__main__":
    from data import get_all_functions
    env = CodeEnv(get_all_functions(), test_cases)
    state = env.reset()
    print(f"Initial code:\n{state}")
    new_state, reward, done, _ = env.step('optimize_loop')
    print(f"New code:\n{new_state}\nReward: {reward}\nDone: {done}")
import torch
import matplotlib.pyplot as plt
from transformer import transform_code
from reward import heuristic_reward
from policy import Policy, encode_state
from data import get_all_functions
from test_cases import test_cases

def plot_learning_curve(rewards):
    plt.plot(rewards)
    plt.xlabel("Episode")
    plt.ylabel("Reward")
    plt.title("Learning Curve")
    plt.savefig("learning_curve.png")
    plt.close()

def evaluate_example(code, policy, func_name, test_inputs):
    state = encode_state(code)
    probs = policy(state)
    action_idx = torch.argmax(probs).item()
    action = ['optimize_loop', 'simplify_string', 'use_builtins', 'memoize'][action_idx]
    optimized_code = transform_code(code, action)
    original_reward = heuristic_reward(code, func_name, test_inputs)
    optimized_reward = heuristic_reward(optimized_code, func_name, test_inputs)
    return code, optimized_code, original_reward, optimized_reward, action

rewards = torch.load("rewards.pt").tolist()
plot_learning_curve(rewards)

functions = get_all_functions()
sample_code = next(f for f in functions if "sum_squares" in f)
func_name = sample_code.split("def ")[1].split("(")[0]
policy = Policy(input_dim=4, action_dim=4)
policy.load_state_dict(torch.load("policy.pth"))
policy.eval()

original, optimized, orig_reward, opt_reward, action = evaluate_example(sample_code, policy, func_name, test_cases[func_name])
print(f"Action: {action}")
print(f"Original:\n{original}\nReward: {orig_reward:.2f}")
print(f"Optimized:\n{optimized}\nReward: {opt_reward:.2f}")
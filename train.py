import torch
import torch.optim as optim
from environment import CodeEnv
from policy import Policy, encode_state
from data import get_all_functions
from test_cases import test_cases

def compute_returns(rewards, gamma=0.99):
    returns = []
    R = 0
    for r in reversed(rewards):
        R = r + gamma * R
        returns.insert(0, R)
    return returns

env = CodeEnv(get_all_functions(), test_cases)
policy = Policy(input_dim=4, action_dim=len(env.action_space))
optimizer = optim.Adam(policy.parameters(), lr=0.01)
rewards_log = []

for episode in range(100):
    state = env.reset()
    log_probs = []
    rewards = []
    done = False
    while not done:
        state_vec = encode_state(state)
        probs = policy(state_vec)
        action_idx = torch.multinomial(probs, 1).item()
        action = env.action_space[action_idx]
        next_state, reward, done, _ = env.step(action)
        log_probs.append(torch.log(probs[action_idx]))
        rewards.append(reward)
        state = next_state
    returns = compute_returns(rewards)
    baseline = sum(rewards) / len(rewards) if rewards else 0
    loss = sum([-log_prob * (ret - baseline) for log_prob, ret in zip(log_probs, returns)])
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    total_reward = sum(rewards)
    rewards_log.append(total_reward)
    print(f"Episode {episode}: Reward = {total_reward}")

torch.save(policy.state_dict(), "policy.pth")
torch.save(torch.tensor(rewards_log), "rewards.pt")
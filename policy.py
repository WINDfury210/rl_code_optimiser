import torch
import torch.nn as nn
import ast

def encode_state(code):
    tree = ast.parse(code)
    loop_count = sum(1 for node in ast.walk(tree) if isinstance(node, ast.For))
    if_count = sum(1 for node in ast.walk(tree) if isinstance(node, ast.If))
    call_count = sum(1 for node in ast.walk(tree) if isinstance(node, ast.Call))
    return torch.tensor([len(code), loop_count, if_count, call_count], dtype=torch.float32)

class Policy(nn.Module):
    def __init__(self, input_dim, action_dim):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(input_dim, 64),
            nn.ReLU(),
            nn.Linear(64, action_dim)
        )

    def forward(self, state):
        logits = self.net(state)
        return torch.softmax(logits, dim=-1)

if __name__ == "__main__":
    policy = Policy(input_dim=4, action_dim=4)
    sample_code = """
def sum_squares(n):
    total = 0
    for i in range(n):
        total += i ** 2
    return total
"""
    state = encode_state(sample_code)
    probs = policy(state)
    print(f"State: {state.tolist()}")
    print(f"Action probabilities: {probs.tolist()}")
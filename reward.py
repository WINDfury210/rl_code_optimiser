import timeit
import ast
from test_cases import test_cases

def heuristic_reward(code, func_name, test_inputs):
    """
    Calculate heuristic reward for optimized code based on runtime, code length, and correctness.
    Args:
        code (str): The optimized code string.
        func_name (str): Name of the function (e.g., 'sum_squares').
        test_inputs (list): List of (input, expected_output) tuples from test_cases.py.
    Returns:
        float: Normalized reward in [0, 10].
    """
    try:
        ast.parse(code)

        exec(code, globals())
        for input_val, expected in test_inputs:

            input_str = str(input_val)
            if isinstance(input_val, list):
                input_str = f"{input_val}"
            result = eval(f"{func_name}({input_str})")
            if result != expected:
                return 0


        input_val = test_inputs[0][0]
        input_str = str(input_val)
        if isinstance(input_val, list):
            input_str = f"{input_val}"
        runtime = timeit.timeit(
            f"{func_name}({input_str})",
            setup=f"from __main__ import {func_name}",
            number=1000
        )
        runtime_reward = min(5.0, 1.0 / (runtime + 1e-5))

        code_length = len(code)

        length_reward = min(3.0, 100.0 / (code_length + 1))


        correctness_reward = 2.0

        total_reward = 0.6 * runtime_reward + 0.3 * length_reward + 0.1 * correctness_reward
        return min(10.0, total_reward)

    except Exception as e:
        return 0

if __name__ == "__main__":

    test_code = """
def sum_squares(n):
    total = 0
    for i in range(n):
        total += i ** 2
    return total
"""
    optimized_code = """
def sum_squares(n):
    total = sum(i ** 2 for i in range(n))
    return total
"""
    func_name = "sum_squares"
    reward_original = heuristic_reward(test_code, func_name, test_cases[func_name])
    reward_optimized = heuristic_reward(optimized_code, func_name, test_cases[func_name])
    print(f"Original code reward: {reward_original:.2f}")
    print(f"Optimized code reward: {reward_optimized:.2f}")
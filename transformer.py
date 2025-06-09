import ast
from ast import NodeTransformer, parse, unparse, fix_missing_locations

class CodeTransformer(NodeTransformer):
    def __init__(self, action):
        self.action = action

    def visit_FunctionDef(self, node):
        if self.action == "memoize":
            if any(isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == node.name for n in ast.walk(node)):
                node.decorator_list.append(ast.Call(
                    func=ast.Name(id='cache', ctx=ast.Load()),
                    args=[], keywords=[]
                ))
                return fix_missing_locations(node)
        return self.generic_visit(node)

    def visit_For(self, node):
        if self.action == "simplify_loop":
            if len(node.body) == 1 and isinstance(node.body[0], ast.AugAssign):
                target = node.body[0].target
                value = node.body[0].value
                comp = ast.GeneratorExp(
                    elt=value,
                    generators=[ast.comprehension(target=node.target, iter=node.iter, ifs=[])]
                )
                return ast.Assign(
                    targets=[target],
                    value=ast.Call(func=ast.Name(id='sum', ctx=ast.Load()), args=[comp], keywords=[])
                )
            elif len(node.body) == 1 and isinstance(node.body[0], ast.Expr) and isinstance(node.body[0].value, ast.Call):
                call = node.body[0].value
                if isinstance(call.func, ast.Attribute) and call.func.attr == 'append':
                    target = call.func.value
                    comp = ast.ListComp(
                        elt=call.args[0],
                        generators=[ast.comprehension(target=node.target, iter=node.iter, ifs=node.ifs)]
                    )
                    return ast.Assign(targets=[target], value=comp)
        return self.generic_visit(node)

    def visit_Assign(self, node):
        if self.action == "optimize_string":
            if isinstance(node.value, ast.BinOp) and isinstance(node.value.op, ast.Add):
                if isinstance(node.value.left, ast.Str) and isinstance(node.value.right, ast.Str):
                    return ast.Assign(
                        targets=node.targets,
                        value=ast.Call(
                            func=ast.Attribute(value=ast.Str(s=""), ctx=ast.Load(), attr='join'),
                            args=[ast.List(elts=[node.value.left, node.value.right], ctx=ast.Load())],
                            keywords=[]
                        )
                    )
            elif isinstance(node.value, ast.BinOp) and isinstance(node.value.op, ast.Add) and isinstance(node.value.left, ast.Name):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        return ast.Assign(
                            targets=[target],
                            value=ast.Subscript(
                                value=node.value.right,
                                slice=ast.Slice(lower=None, upper=None, step=ast.Constant(value=-1)),
                                ctx=ast.Load()
                            )
                        )
        elif self.action == "inline_builtins":
            if isinstance(node.value, ast.BinOp) and isinstance(node.value.op, ast.Mult):
                if isinstance(node.value.left, ast.Constant) and node.value.left.value == 3.14:
                    return ast.Assign(
                        targets=node.targets,
                        value=ast.BinOp(
                            left=ast.Name(id='math.pi', ctx=ast.Load()),
                            op=node.value.op,
                            right=node.value.right
                        )
                    )
        return self.generic_visit(node)

def transform_code(code, action):
    try:
        tree = parse(code)
        transformer = CodeTransformer(action)
        new_tree = transformer.visit(tree)
        fix_missing_locations(new_tree)
        optimized_code = unparse(new_tree)
        if action == "memoize":
            optimized_code = "from functools import cache\n" + optimized_code
        if action == "inline_builtins" and "math.pi" in optimized_code:
            optimized_code = "import math\n" + optimized_code
        return optimized_code
    except Exception as e:
        return code

if __name__ == "__main__":
    test_codes = [
        """
def sum_squares(n):
    total = 0
    for i in range(n):
        total += i ** 2
    return total
""",
        """
def concat_words(words):
    result = ""
    for word in words:
        result += word + " "
    return result.strip()
""",
        """
def fibonacci(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fibonacci(n-1) + fibonacci(n-2)
""",
        """
def circle_area(radius):
    return 3.14 * radius * radius
""",
        """
def reverse_string(s):
    result = ""
    for char in s:
        result = char + result
    return result
"""
    ]

    actions = ["simplify_loop", "optimize_string", "memoize", "inline_builtins", "optimize_string"]
    for code, action in zip(test_codes, actions):
        print(f"\nAction: {action}")
        print("Original:\n", code)
        print("Optimized:\n", transform_code(code, action))
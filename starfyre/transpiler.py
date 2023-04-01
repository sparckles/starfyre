import ast
import inspect

class PythonToJsTranspiler(ast.NodeVisitor):
    def __init__(self):
        self.js_code = []

    def visit_FunctionDef(self, node):
        function_name = node.name
        parameters = [arg.arg for arg in node.args.args]
        param_list = ", ".join(parameters)

        self.js_code.append(f"function {function_name}({param_list}) {{")
        self.generic_visit(node)
        self.js_code.append("}\n")

    def visit_Assign(self, node):
        targets_code = " = ".join([ast.unparse(t) for t in node.targets])
        value_code = ast.unparse(node.value)
        self.js_code.append(f"  {targets_code} = {value_code};")

    def visit_Return(self, node):
        value_code = ast.unparse(node.value) if node.value else ""
        self.js_code.append(f"  return {value_code};")

    def visit_Expr(self, node):
        if isinstance(node.value, ast.Call):
            self.visit_Call(node.value)

    def visit_Call(self, node):
        if isinstance(node.func, ast.Name) and node.func.id == "print":
            args_code = ", ".join([ast.unparse(arg) for arg in node.args])
            self.js_code.append(f"  console.log({args_code});")
        else:
            func_code = ast.unparse(node.func)
            args_code = ", ".join([ast.unparse(arg) for arg in node.args])
            self.js_code.append(f"  {func_code}({args_code});")




def transpile(python_code: str) -> str:
    tree = ast.parse(python_code)
    transpiler = PythonToJsTranspiler()
    transpiler.visit(tree)
    return "".join(transpiler.js_code)

def transpile_to_js(python_code):
    code = inspect.getsource(python_code)
    return transpile(code)

def main():
    python_code = '''
def greet(name):
    print("Hello, " + name)

def add(a, b):
    result = a + b
    return result
'''

    js_code = transpile(python_code)
    print(js_code)

if __name__ == "__main__":
    main()


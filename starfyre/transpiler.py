import libcst as cst
import inspect


class PythonToJsTranspiler(cst.CSTTransformer):
    def __init__(self):
        self.js_code = []

    def visit_FunctionDef(self, node: cst.FunctionDef) -> None:
        function_name = node.name.value
        parameters = [param.name.value for param in node.params.params]
        param_list = ", ".join(parameters)

        self.js_code.append(f"function {function_name}({param_list}) {{")
        for stmt in node.body.body:
            if isinstance(stmt, cst.SimpleStatementLine):
                for component in stmt.body:
                    if isinstance(component, cst.Assign):
                        self.visit_Assign(component)
                    elif isinstance(component, cst.Return):
                        self.visit_Return(component)
                    elif isinstance(component, cst.Expr):
                        self.visit_Expr(component)
            elif isinstance(stmt, cst.BaseCompoundStatement):
                # Add handling for other compound statements as needed
                pass
        self.js_code.append("}")

    def visit_Assign(self, node: cst.Assign) -> None:
        targets_code = " = ".join([t.target.to_code() for t in node.targets])
        value_code = node.value.to_code()
        self.js_code.append(f"{targets_code} = {value_code};")

    def visit_Return(self, node: cst.Return) -> None:
        value_code = node.value.to_code() if node.value else ""
        self.js_code.append(f"return {value_code};")

    def visit_Expr(self, node: cst.Expr) -> None:
        if isinstance(node.value, cst.Call):
            if isinstance(node.value.func, cst.Name) and node.value.func.value == "print":
                self.visit_Print(node.value)

    def visit_Print(self, node: cst.Call) -> None:
        args_code = ", ".join([arg.to_code() for arg in node.args])
        self.js_code.append(f"console.log({args_code});")

    def transpile(self, python_code: str) -> str:
        tree = cst.parse_module(python_code)
        modified_tree = self.visit_Module(tree)
        return "\n".join(self.js_code)

def transpile_to_js(python_code):
    """
    Transpiles python code to javascript
    """
    python_code = inspect.getsource(python_code)
    transpiler = PythonToJsTranspiler()
    js_code = transpiler.transpile(python_code)

    return js_code
        

def main():
    python_code = '''
def greet(name):
    print("Hello, " + name)

def add(a, b):
    result = a + b
    return result
'''

    transpiler = PythonToJsTranspiler()
    js_code = transpiler.transpile(python_code)
    print(js_code)

if __name__ == "__main__":
    main()

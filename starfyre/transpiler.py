import inspect

def transpile_to_js(python_code):
    """
    Transpiles python code to javascript
    """
    python_code = inspect.getsource(python_code).split("\n")
    js_code = []
    js_line = ""

    # based on the assumption of just simple functions
    for line in python_code:
        js_line = line

        if line.startswith("def "):
            js_line = line.replace("def ", "function ")
            js_line = js_line.replace(":", "{")
            print("Appending js line", js_line)
        elif "js." in line:
            js_line = line.replace("js.", "")
        elif "print" in line:
            js_line = line.replace("print", "console.log")
        
        print("Appending js line", js_line)
        js_code.append(js_line)


    js_code.append("}")
    print("This is the js code", js_code, python_code)

    # add a missing } at the end of the function in js code

    return "\n".join(js_code)
        


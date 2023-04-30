import inspect

from starfyre.dom_methods import render, render_root
from .compiler import compile
from starfyre.component import Component
from .transpiler import transpile

# import js

# for exports

# from .component import Component
# from .dom_methods import render
from .parser import RootParser

# from .store import create_signal


def create_component(pyml="", css="", js="", client_side_python=""):
    if client_side_python:
        new_js = transpile(client_side_python) + js
        js = new_js

    local_variables = inspect.currentframe().f_back.f_back.f_locals.copy()
    global_variables = inspect.currentframe().f_back.f_back.f_globals.copy()

    parser = RootParser(local_variables, global_variables, css, js)
    pyml = pyml.strip("\n").strip()
    parser.feed(pyml)
    parser.close()
    pyml_root = parser.get_root()

    if pyml_root is None:
        return Component("div", {}, [], {}, {}, uuid="store", js=js)

    return pyml_root


# __all__ = [
#     "render",
#     "js",
#     "create_component",
#     "Component",
#     "create_signal",
#     "sum_as_string",
# ]

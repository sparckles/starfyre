import inspect
from starfyre.dom_methods import render, render_root
from .compiler import compile

from starfyre.component import Component
from .transpiler import transpile

from .parser import ComponentParser


def create_component(pyml="", css="", js="", client_side_python="", component_name=""):
    if client_side_python:
        new_js = transpile(client_side_python) + js
        js = new_js

    local_variables = inspect.currentframe().f_back.f_back.f_locals.copy()
    global_variables = inspect.currentframe().f_back.f_back.f_globals.copy()

    parser = ComponentParser(local_variables, global_variables, css, js, component_name)
    pyml = pyml.strip("\n").strip()
    parser.feed(pyml)
    parser.close()
    pyml_root = parser.get_root()

    if pyml_root is None:
        return Component("div", {}, [], {}, {}, uuid="store", js=js, original_name="div")

    return pyml_root


__all__ = [
    "create_component",
    "render",
    "render_root",
    "compile",
    "transpile",
    "Component",
]

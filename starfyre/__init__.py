import inspect

from starfyre.component import Component
from starfyre.dom_methods import render, render_root

from .compiler import compile
from .parser import ComponentParser
from .transpiler import transpile


def create_component(pyxide="", css="", js="", client_side_python="", component_name=""):
    if client_side_python:
        new_js = transpile(client_side_python) + js
        js = new_js

    local_variables = inspect.currentframe().f_back.f_back.f_locals.copy()
    global_variables = inspect.currentframe().f_back.f_back.f_globals.copy()

    parser = ComponentParser(local_variables, global_variables, css, js, component_name)
    pyxide = pyxide.strip("\n").strip()
    parser.feed(pyxide)
    parser.close()
    pyxide_root = parser.get_root()

    if pyxide_root is None:
        return Component(
            tag="div",
            props={},
            children=[],
            event_listeners={},
            state={},
            uuid="store",
            js=js,
            original_name="div",
        )

    return pyxide_root


__all__ = [
    "create_component",
    "render",
    "render_root",
    "compile",
    "transpile",
    "Component",
]

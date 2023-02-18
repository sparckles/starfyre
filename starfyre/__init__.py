import inspect

import js

from starfyre.starfyre import sum_as_string

from .component import Component
from .dom_methods import render
from .parser import RootParser
from .store import create_signal


def extract_functions(obj):
    functions = {}
    for key, value in obj.items():
        if callable(value):
            functions[key] = value

    return functions


def return_event_listensers(event_listener_names, local_functions, global_functions):
    event_listeners = {}
    for event_listener_name in event_listener_names:
        if event_listener_name in local_functions:
            event_listeners[event_listener_name] = local_functions[event_listener_name]
        elif event_listener_name in global_functions:
            event_listeners[event_listener_name] = global_functions[event_listener_name]
        else:
            pass
    return event_listeners


def return_state(possible_state_names, local_functions, global_functions):
    states = {}
    for possible_state_name in possible_state_names:
        if possible_state_name in local_functions:
            states[possible_state_name] = local_functions[possible_state_name]
        elif possible_state_name in global_functions:
            states[possible_state_name] = global_functions[possible_state_name]
        else:
            pass
    return states


def create_component(jsx):
    locals_variables = inspect.currentframe().f_back.f_locals.copy()
    global_variables = inspect.currentframe().f_back.f_globals.copy()

    parser = RootParser(locals_variables, global_variables)
    jsx = jsx.strip("\n").strip()
    parser.feed(jsx)
    parser.close()
    pytml_root = parser.get_root()
    print("This is the pytml root root", pytml_root)
    return pytml_root


__all__ = [
    "render",
    "js",
    "create_component",
    "Component",
    "create_signal",
    "sum_as_string",
]

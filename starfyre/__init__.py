import inspect
import re

from .parser import Parser
from .component import Component
from .dom_methods import render
from .store import create_signal

import js
from starfyre.starfyre import sum_as_string, DomNode


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
    globals = inspect.currentframe().f_back.f_globals.copy()
    locals = inspect.currentframe().f_back.f_locals
    local_functions = extract_functions(locals)
    global_functions = extract_functions(globals)

    # extract event listeners name from jsx

    event_listeners_names = re.findall(r"on\w+=\{(\w+)}", jsx)
    event_listeners = return_event_listensers(
        event_listeners_names, local_functions, global_functions
    )

    jsx_variables = re.findall(r"\{(\w+)\}", jsx)
    possible_states = [
        el for el in jsx_variables if el not in event_listeners
    ]  # this can be props or states
    state = return_state(possible_states, local_functions, global_functions)

    # print(inspect.getframeinfo(inspect.currentframe().f_back))
    print("These are the locals", local_functions)
    print("These are the global_functions", global_functions)

    parser = Parser(state)
    jsx = jsx.strip("\n").strip()
    parser.feed(jsx)
    parser.close()

    pytml_tree = parser.parse()
    pytml_root = pytml_tree[0]
    pytml_root.event_listeners = event_listeners
    pytml_root.state = state
    new_root = Component("div", {}, [pytml_root], {}, {})
    dom_node = DomNode("hello", {}, [pytml_root], {}, {})
    print("This is the dom node ", dom_node)
    return new_root


__all__ = [
    "render",
    "js",
    "create_component",
    "Component",
    "create_signal",
    "sum_as_string",
]

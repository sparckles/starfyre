import js
from .parser import Parser
from .component import Component
from .dom_methods import render
from .store import create_signal


def create_component(jsx, event_listeners=None, state=None):
    parser = Parser(state)
    parser.feed(jsx)
    parser.close()

    pytml_tree = parser.parse()
    pytml_root = pytml_tree[0]
    pytml_root.event_listeners = event_listeners
    pytml_root.state = state
    new_root = Component("div", {}, [pytml_root], {}, {})
    return new_root


__all__ = ["render", "js", "create_component", "Component", "create_signal"]

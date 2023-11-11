# import uuid

import js
import math
import random

# from .dom_methods import render

store = {}
observers = {}
# dict[uuid.UUID, list[Component]] = 
#

def render(component):
    ...


def create_signal(initial_state=None):
    """Create a signal to be used in a component."""
    global store
    id = random.randint(0, 100000)

    def use_signal(element=None):
        """Get the state and manage observers."""
        nonlocal id
        if element:
            observers.setdefault(id, []).append(element)
        return store.get(id, initial_state)

    def set_signal(state):
        """Set a new state and trigger re-render for observers."""
        # need to fix this
        # we need to maintain a global tree indexed by uuids after the hydration process
        # after the hydration process, we need to update the tree with the new state
        # then we need to re-render the tree

        

        nonlocal id
        store[id] = state
        for component_id in observers.get(id, []):
            component = js.document.getElementById(component_id)

            if component and component.parentComponent:
                parentDom = component.parentComponent
                # 
                parentDom.removeChild(component)
            else:
                parentDom = js.document.getElementById("root")
                parentDom.innerHTML = ""

            render(component)

    def get_signal():
        """Get the current state without affecting the observer list."""
        nonlocal id
        return store.get(id, initial_state)

    return [use_signal, set_signal, get_signal]

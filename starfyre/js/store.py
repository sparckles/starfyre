import uuid

import js

from starfyre.component import Component

from .dom_methods import render

store = {}
observers: dict[uuid.UUID, list[Component]] = {}


def create_signal(initial_state=None):
    """Create a signal to be used in a component."""
    global store
    id = uuid.uuid4()

    def getState(element):
        print("This is the type", type(element))
        if id in observers:
            observers[id].append(element)
        else:
            observers[id] = [element]

        return store.get(id, initial_state)

    def setState(state):
        store[id] = state
        for component in observers[id]:
            print("observer component", component)
            if component and component.parentDom:
                parentDom = component.parentDom
                parentDom.removeChild(component.dom)
            else:
                parentDom = js.document.getElementById("root")
                parentDom.innerHTML = ""

            print("rendering", component)
            # should be done in batching
            render(component)

    return [getState, setState]

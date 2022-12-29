import uuid
from .dom_methods import render
import js

store = {}
observers = {}


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
            print("component", component)
            if component.parentDom:
                parentDom = component.parentDom
                parentDom.removeChild(component.dom)
            else:
                parentDom = js.document.getElementById("root")
                parentDom.innerHTML = ""

            print("rendering", component)
            render(component, parentDom)

    return [getState, setState]

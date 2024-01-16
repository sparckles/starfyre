# import uuid

import random

import js


store = GLOBAL_STORE
observers = GLOBAL_OBSERVERS

reverse_store = GLOBAL_OBSERVERS  # maps dom id: uuid
clientDomIdMap = GLOBAL_CLIENT_DOM_ID_MAP



def evaluate_data(component, dom_id):
    # we will need to extend this
    data = component.data
    new_data = data
    print("Original data", data)
    if "signal" in data:
        store_id = reverse_store.get(dom_id)
        signal_value = store.get(store_id)
        print("This is the component signal", component.signal)
        temp_data = data.replace(component.signal, str(signal_value))
        print("This is the temp data", temp_data)
        new_data = eval(f"{temp_data.strip().strip(';')}")
        print("This is the new data", new_data)

    return new_data


def hydrate(component):
    # this will take the component and then find the dom element
    # and then convert the tree to the html
    # component is then tree
    # and pareneComponent is the parent node
    # we need to remove the html of the parent component
    # and then add the new html based on the component tree
    #
    for child in component.children:
        id = child.uuid
        domElement = js.document.querySelector(f"[data-pyxide-id='{id}']")
        if domElement is None:
            continue

        data = evaluate_data(child, id)
        domElement.innerText = data
        hydrate(child)


def create_signal(initial_state=None):
    """Create a signal to be used in a component."""
    global store, reverse_store
    signal_id = random.randint(0, 100000)

    def use_signal(dom_id=None):  # this will be the dom id
        """Get the state and manage observers."""
        nonlocal signal_id
        if dom_id:
            observers.setdefault(signal_id, []).append(dom_id)
            reverse_store[dom_id] = signal_id

        return store.get(signal_id, initial_state)

    def set_signal(initial_state=None):
        # need to fix this
        # we need to maintain a global tree indexed by uuids after the hydration process
        # after the hydration process, we need to update the tree with the new state
        # then we need to re-render the tree

        nonlocal signal_id
        store[signal_id] = initial_state
        for component_id in observers.get(signal_id, []):
            component = js.document.querySelector(f"[data-pyxide-id='{component_id}']")
            component = clientDomIdMap.get(component_id)
            if component is None:
                continue
            print("component", component, "new state", initial_state)
            print("clientDomIdMap", clientDomIdMap)

            js.console.log(
                "This is the component",
                component,
                str(dir(component)),
                component.children,
            )
            component.re_render()
            hydrate(component)
            print("hydration ended")

    def get_signal(*args, **kwargs):
        # args and kwargs are not used but a hack as the ids are being
        # passed as arguments currently
        # will be fixed once the serialization and deserialization is done
        """Get the current state without affecting the observer list."""
        nonlocal signal_id
        return store.get(signal_id, initial_state)

    return [use_signal, set_signal, get_signal]

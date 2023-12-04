# import uuid

import random

import js

# from .dom_methods import render

store = {}
observers = {}

reverse_store = {}  # maps dom id: uuid
# dict[uuid.UUID, list[Component]] =
#


def render(component, parentElement=None):  # this is domElement
    # the best fix will be to serialize the dom tree and then de serialize it
    # on the client
    # and then find from a dict to re render
    #

    # but for now, we will just find the id of the component by
    # document.getElementById
    # and then get the current state
    # put it as a inner text and then re render the children
    #

    if parentElement is None:
        parentElement = js.document.querySelector("[data-pyxide-id=root]")
        if parentElement is None:
            parentElement = js.document.createElement("div")
            parentElement.id = "root"
            js.document.body.appendChild(parentElement)

    if component:
        # find all the names in "{}" and print them
        # need to sort this again
        # matches = re.findall(r"{(.*?)}", data)
        # for match in matches:
        # if match in state:
        # function = state[match]
        # function = partial(function, component)
        # data = component.data.replace(f"{{{ match }}}", str(function()))
        # dom = js.document.createTextNode(data)

        dom_id = component.id

        parentElement.appendChild(component)
        # print("Text Node", component)
        js.console.log(component, component.children)
        if component.children:
            for child in component.children:
                render(child, component.element)

        if dom_id in reverse_store:
            id = reverse_store[dom_id]
            state = store.get(id)
            if state:
                component.innerText = state
    # Add event listeners
    # def isListener(name):
    # return name.startswith("on")
    # def isAttribute(name):
    # return not isListener(name) and name != "children"

    # set attributes

    # for name in props:
    #     if isAttribute(name):
    #         dom.setAttribute(name, props[name])

    # Render children
    # children = component.children
    # childElements.forEach(childElement => render(childElement, dom));
    # for childElement in children:
    # childElement.parentDom = dom
    # render(childElement)

    # // Append to parent
    # need to apply batch updates here
    # also create a tree of dom nodes in the first place
    # if parentElement.contains(dom):
    # parentElement.replaceChild(dom, parentElement.childNodes[0])
    # else:
    # parentElement.appendChild(dom)


# the render is the wrong implementation


def create_signal(initial_state=None):
    """Create a signal to be used in a component."""
    global store, reverse_store
    id = random.randint(0, 100000)

    def use_signal(element=None):  # this will be the dom id
        """Get the state and manage observers."""
        nonlocal id
        if element:
            observers.setdefault(id, []).append(element)
            reverse_store[element] = id

        return store.get(id, initial_state)

    def set_signal(state):
        """Set a new state and trigger re-render for observers."""
        """The render process works in a wrong way at this point but works for now."""
        """We need to update the value in the state"""
        # need to fix this
        # we need to maintain a global tree indexed by uuids after the hydration process
        # after the hydration process, we need to update the tree with the new state
        # then we need to re-render the tree

        nonlocal id
        store[id] = state
        for component_id in observers.get(id, []):
            component = js.document.querySelector(f"[data-pyxide-id='{component_id}']")
            js.console.log(
                "This is the component",
                component,
                str(dir(component)),
                component.children,
            )

            render(component, component.parentElement)

    def get_signal(*args, **kwargs):
        # args and kwargs are not used but a hack as the ids are being
        # passed as arguments currently
        # will be fixed once the serialization and deserialization is done
        """Get the current state without affecting the observer list."""
        nonlocal id
        return store.get(id, initial_state)

    return [use_signal, set_signal, get_signal]

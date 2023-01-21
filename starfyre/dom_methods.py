import js
from .component import Component
from pyodide import create_proxy
from functools import partial
import re
from starfyre.starfyre import DomNode


def render(element: Component, parentDom: js.Element):
    element.parentDom = parentDom
    dom_node = DomNode(element.tag, element.props, element.children, element.event_listeners, element.state or {})
    dom_node.set_parent_element(parentDom)
    print(dom_node)

    tag = element.tag
    props = element.props
    state = element.state
    data = element.data
    print(data)

    # Create DOM element
    if element.is_text_component:
        # find all the names in "{}" and print them
        matches = re.findall(r"{(.*?)}", data)
        for match in matches:
            if match in state:
                print(match, state[match])
                function = state[match]
                function = partial(function, element)
                
                data = element.data.replace(
                    f"{{{ match }}}", str(function())
                )

        dom = js.document.createTextNode(data)
        print("Text Node", element)
    else:
        dom = js.document.createElement(tag)

    element.dom = dom

    # Add event listeners
    isListener = lambda name: name.startswith("on")
    isAttribute = lambda name: not isListener(name) and name != "children"

    # set event listeners
    for event_name, action in props.items():
        if isListener(event_name):
            eventType = event_name.lower()[2:]
            action = action.replace("{", "").replace("}", "")

            if action in element.event_listeners:
                event_listener = element.event_listeners[action]
                dom.addEventListener(eventType, create_proxy(event_listener))

    # set attributes

    for name in props:
        if isAttribute(name):
            dom.setAttribute(name, props[name])

    # Render children
    children = element.children
    # childElements.forEach(childElement => render(childElement, dom));
    for childElement in children:
        render(childElement, dom)

    # // Append to parent
    if parentDom.contains(dom):
        parentDom.replaceChild(dom, parentDom.childNodes[0])
    else:
        parentDom.appendChild(dom)

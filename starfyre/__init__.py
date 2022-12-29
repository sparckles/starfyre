import js
from .parser import Parser
from .component import Component, Instance



def render(element: Component, parentDom: js.Element):
    tag = element.tag
    props = element.props

    # Create DOM element
    if element.is_text_component:
        dom = js.document.createTextNode(element.data)
        print("Text Node", element)
    else:
        dom = js.document.createElement(tag)


    # Add event listeners
    isListener = lambda name: name.startswith("on")
    isAttribute = lambda name: not isListener(name) and name != "children"

    # set event listeners
    for event_name, action in props.items():
        if isListener(event_name):
            eventType = event_name.lower()[2:]
            from pyodide import create_proxy
            print(element.event_listeners)
            action = action.replace("{", "").replace("}", "")
            event_listener = element.event_listeners[action]

            # dom.addEventListener(eventType, props[name])
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
    if parentDom.hasChild(dom):
        parentDom.replaceChild(dom, parentDom.childNodes[0])
    else:
        parentDom.appendChild(dom)


def create_component(jsx, event_listeners):
    parser = Parser()
    parser.feed(jsx)
    parser.close()
    pytml_tree = parser.parse()
    pytml_root = pytml_tree[0]
    pytml_root.event_listeners = event_listeners
    return pytml_root


__all__ = ["render", "js", "create_component"]

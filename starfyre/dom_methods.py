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
class Parser(HTMLParser):
    def __init__(self, state):
        super().__init__()
        self.stack = []
        self.state = state # this is initialized for every component

    def handle_starttag(self, tag, attrs):
        props = {}
        for attr in attrs:
            props[attr[0]] = attr[1]

        # instead of creating a new component, we check if the tag is a global component
        # then we check the uuid of the global component
        # if the uuid is not in the stack, we create a new component
        # if the uuid is in the stack, we use the component from the stack
        # we are using a hack for now

        if tag in components:
            component = components[tag][0]
        else:
            component = Component(tag, props, [], {}, self.state)

        components[tag].append(component)
        # instead of assiging tags we assign uuids
        self.stack.append(Component(tag, props, [], {}, self.state))

    def handle_endtag(self, tag):
        children = []
        while self.stack:
            node = self.stack[-1]
            # instead of comparing tags we compare uuids
            if isinstance(node, Component) and node.tag == tag:

                break

            self.stack.pop()
            children.append(node)

        children = children[::-1]
        if self.stack:
            self.stack[-1].children = children

        print("Encountered an end tag :", self.stack)

    def handle_data(self, data):
        print(data)
        self.stack.append(Component("TEXT_NODE", {}, [], {}, self.state, data=data))

    def parse(self):
        return self.stack
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

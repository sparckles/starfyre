import js
from .parser import Parser
from .component import Component, Instance

# from .globals import fyre_tree


# def create_element_tree(node):
#     if type(node) == str:
#         return js.document.createTextNode(node)

#     element = js.document.createElement(node.tag)

#     if node.props:
#         for key, value in node.props.items():
#             element.setAttribute(key, value)

#     if node.children:
#         for child in node.children:
#             next_element = create_element_tree(child)
#             if type(next_element) == str:
#                 element.innerHTML += next_element
#             else:
#                 element.appendChild(next_element)

#     return element

root_instance = None


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
    def hello(*args):
        print("Hello")

    for name in props:
        if isListener(name):
            eventType = name.lower()[2:]

            from pyodide import create_proxy

            # dom.addEventListener(eventType, props[name])
            dom.addEventListener(eventType, create_proxy(hello))

    # set attributes

    # Object.keys(props).filter(isAttribute).forEach(name => {
    # dom[name] = props[name];
    # });
    for name in props:
        if isAttribute(name):
            dom.setAttribute(name, props[name])

    # Render children
    children = element.children
    # childElements.forEach(childElement => render(childElement, dom));
    for childElement in children:
        render(childElement, dom)

    # // Append to parent
    parentDom.appendChild(dom)


def create_component(jsx):
    parser = Parser()
    parser.feed(jsx)
    parser.close()
    pytml_tree = parser.parse()
    pytml_root = pytml_tree[0]
    return pytml_root


# def render_root(element: str):
#     div = js.document.createElement("div")
#     div.setAttribute("id", "root")
#     parser = Parser()
#     parser.feed(element)
#     parser.close()

#     pytml_tree = parser.parse()
#     pytml_root = pytml_tree[0]
#     print("This is the pytml root", pytml_root)
#     print(pytml_tree)
#     print(element)
#     fyre_tree.root = FyreNode(pytml_root)
#     fyre_tree.build_tree()

#     js.document.body.prepend(fyre_tree.root.data[0])
#     js.document.body.prepend(div)


def main():
    root = Component(
        "div",
        {"id": "root"},
        [
            Component("TEXT_NODE", {}, [], {}, data="Hello, World!"),
            Component("p", {}, [Component("TEXT_NODE", {}, [], {}, "bruhh")], {}),
        ],
        {},
    )

    # fyre_tree = FyreTree(FyreNode(root))
    # fyre_tree.build_tree()
    # print("FyreTree:")
    # print(fyre_tree)
    # js.document.body.prepend(fyre_tree.root.data[0])
    # root.children[0].data = "Hello, World!!!!"
    # root.set_state("id", "root", fyre_tree)
    # print("FyreTree:")
    # print(fyre_tree)


__all__ = ["render", "js", "main"]

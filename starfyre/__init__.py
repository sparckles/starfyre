import js
from starfyre.fyre_tree import Component, FyreNode, FyreTree
from .parser import Node, Parser


def create_element_tree(node):
    if type(node) == str:
        return js.document.createTextNode(node)

    element = js.document.createElement(node.tag)

    if node.props:
        for key, value in node.props.items():
            element.setAttribute(key, value)

    if node.children:
        for child in node.children:
            next_element = create_element_tree(child)
            if type(next_element) == str:
                element.innerHTML += next_element
            else:
                element.appendChild(next_element)

    return element


def render(element: str, container: js.Element):
    parser = Parser()
    parser.feed(element)
    parser.close()

    pytml_tree = parser.parse()
    pytml_root = pytml_tree[0]

    element = create_element_tree(pytml_root)  # this is essentially the dom tree
    container.appendChild(element)

    js.document.body.prepend(container)


def render_root(element: str):
    div = js.document.createElement("div")
    div.setAttribute("id", "root")
    parser = Parser()
    parser.feed(element)
    parser.close()

    pytml_tree = parser.parse()
    pytml_root = pytml_tree[0]

    element = create_element_tree(pytml_root)
    if type(element) == str:
        div.innerHTML = element
    else:
        div.appendChild(element)

    js.document.body.prepend(div)


def main():
    root = Component(
        "div",
        {"id": "root"},
        [
            Component("TEXT_NODE", {}, [], data="Hello, World!"),
            Component("p", {}, [Component("TEXT_NODE", {}, [], "bruhh")]),
        ],
    )

    fyre_tree = FyreTree(FyreNode(root))
    fyre_tree.build_tree()
    print("FyreTree:")
    print(fyre_tree)
    root.render(fyre_tree)
    print("FyreTree:")
    print(fyre_tree)


__all__ = ["render", "render_root", "js", "main"]

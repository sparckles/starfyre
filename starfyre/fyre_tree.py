from typing import Union
import js
from .component import Component


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


class FyreNode:
    def __create_dom_element(self, vdom_component: Component):
        if vdom_component.is_text_component:
            return js.document.createTextNode(vdom_component.data)

        element = js.document.createElement(vdom_component.tag)
        return element

    def __init__(self, component: Component, parent=None):
        self.parent = parent
        self.children = []

        dom_element = self.__create_dom_element(component)
        self.data = (dom_element, component)

    def __repr__(self):
        return f"{ self.data[0], self.data[1].tag, self.data[1].data }"

    def __str__(self):
        return f"{ self.data[0], self.data[1].tag, self.data[1].data }"


class FyreTree:
    """Class to hold a DOM tree for a given HTML document."""

    def __init__(self, root: FyreNode):
        """Initialize the tree with the root element."""
        self.root = root
        self.current = root

    def build_tree(self):
        """Build the tree from the root element."""
        self.__build_tree(self.root)

    def __build_tree(self, node: FyreNode):
        """Build the tree from a given node."""
        if node.data[1].children:
            for child in node.data[1].children:
                child_node = FyreNode(child, node)
                if child_node.data[1].children:
                    self.__build_tree(child_node)

                node.data[0].appendChild(child_node.data[0])
                node.children.append(child_node)
                self.__build_tree(child_node)

    def find_component(self, component: Component):
        """Find a component in the tree."""
        return self.__find_component(self.root, component)

    def __find_component(self, node: FyreNode, component: Component):
        """Find a component in the tree from a given node."""
        if node.data[1] == component:
            return node

        for child in node.children:
            found = self.__find_component(child, component)
            if found:
                return found

    def rebuild_tree_from_component(self, component: Component):
        """Rebuild the tree from a given component."""
        node = self.find_component(component)
        print("Rebuilding tree from component")
        self.__rebuild_tree_from_node(node)

    def __rebuild_tree_from_node(self, node: FyreNode):
        """Rebuild the tree from a given node."""
        if node.parent:
            # need to remove the children from the parent of vdom and realdom
            node.parent.children = []
            node.data[0].childNodes = []

            # node.parent.data[0].innerHTML = ""
            print("Yeh backchodi")
            self.__build_tree(node.parent)
        else:
            self.root = node
            node.data[0].innerHTML = ""
            self.__build_tree(node)

    def __str__(self):
        """Return a string representation of the tree."""
        return self.__str_node(self.root)

    def __str_node(self, node: FyreNode):
        return (
            f"{node} -> {[self.__str_node(child) for child in node.children]}"
        )

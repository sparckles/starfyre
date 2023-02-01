from html.parser import HTMLParser
from uuid import uuid4

from .component import Component
from .global_components import components


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

    def handle_data(self, data):
        self.stack.append(Component("TEXT_NODE", {}, [], {}, self.state, data=data))

    def parse(self):
        return self.stack


class RootParser(HTMLParser):
    def __init__(self, state, components):
        super().__init__()
        self.stack = []
        self.state = state # this is initialized for every component
        self.components = components


    def handle_starttag(self, tag, attrs):
        props = {}
        for attr in attrs:
            props[attr[0]] = attr[1]

        # instead of creating a new component, we check if the tag is a global component
        # then we check the uuid of the global component
        # if the uuid is not in the stack, we create a new component
        # if the uuid is in the stack, we use the component from the stack
        # we are using a hack for now

        if tag in self.components:
            print(tag, self.components[tag])
            # the parser is not case sensitive, which is a problem
            # we are using the local variable components
            # but if we can find a way to make the parser case sensitive
            # we can use the global variable components and not have to pass them in the local variable
            component = self.components[tag]
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


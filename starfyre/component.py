from dataclasses import dataclass
from html.parser import HTMLParser
from uuid import uuid4

import js


class Parser(HTMLParser):
    stack = []

    def handle_starttag(self, tag, attrs):
        props = {}
        for attr in attrs:
            props[attr[0]] = attr[1]

        self.stack.append(Component(tag, props, [], {}, {}))

    def handle_endtag(self, tag):
        children = []
        while self.stack:
            node = self.stack[-1]
            if isinstance(node, Component) and node.tag == tag:
                break

            self.stack.pop()
            children.append(node)

        children = children[::-1]
        if self.stack:
            self.stack[-1].children = children

    def handle_data(self, data):
        self.stack.append(Component("TEXT_NODE", {}, [], {}, {}, data=data))

    def parse(self):
        return self.stack


@dataclass
class Component:
    tag: str
    props: dict
    children: list
    event_listeners: dict
    state: dict
    original_data: str = ""
    data: str = ""
    parentDom: js.Element = None
    dom: js.Element = None
    uuid = uuid4()
    # on any property change, rebuild the tree

    def render(self):
        pass

    @property
    def is_text_component(self):
        return self.tag == "TEXT_NODE"

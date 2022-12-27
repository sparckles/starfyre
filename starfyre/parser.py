from html.parser import HTMLParser
from dataclasses import dataclass


@dataclass
class Node:
    tag: str
    props: dict
    children: list


class Parser(HTMLParser):
    stack = []

    def handle_starttag(self, tag, attrs):
        props = {}
        for attr in attrs:
            props[attr[0]] = attr[1]

        self.stack.append(Node(tag, props, []))

    def handle_endtag(self, tag):

        children = []
        while self.stack:
            node = self.stack[-1]
            if type(node) == Node and node.tag == tag:
                break

            self.stack.pop()
            children.append(node)

        children = children[::-1]
        if self.stack:
            self.stack[-1].children = children

        print("Encountered an end tag :", self.stack)

    def handle_data(self, data):
        self.stack.append(data)

    def parse(self):
        return self.stack


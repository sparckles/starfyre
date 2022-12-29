from abc import abstractmethod
import js
from dataclasses import dataclass # fyre_tree will be a global variable


@dataclass
class Component:
    tag: str
    props: dict
    children: list
    data: str = ""
    event_listeners = {}
    # on any property change, rebuild the tree

    def render(self, fyre_tree):
        self.tag = "h1"
        fyre_tree.rebuild_tree_from_component(self)

    @property
    def is_text_component(self):
        return self.tag == "TEXT_NODE"


@dataclass
class Instance:
    # an element that has already been rendered to the dom
    dom: js.Element
    component: Component
    children: list

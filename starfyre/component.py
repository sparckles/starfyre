from dataclasses import dataclass


@dataclass
class Component:
    tag: str
    props: dict
    children: list
    data: str = ""

    def render(self, fyre_tree):
        self.tag = "p"
        fyre_tree.rebuild_tree_from_component(self)

    @property
    def is_text_component(self):
        return self.tag == "TEXT_NODE"

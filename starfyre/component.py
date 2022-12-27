from dataclasses import dataclass # fyre_tree will be a global variable


@dataclass
class Component:
    tag: str
    props: dict
    children: list
    state: dict
    data: str = ""
    # on any property change, rebuild the tree

    def render(self, fyre_tree):
        self.tag = "h1"
        fyre_tree.rebuild_tree_from_component(self)

    def set_state(self, key, state, fyre_tree):
        self.state[key] = state
        fyre_tree.rebuild_tree_from_component(self)

    @property
    def is_text_component(self):
        return self.tag == "TEXT_NODE"

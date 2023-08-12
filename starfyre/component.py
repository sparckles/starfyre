from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass
class Component:
    tag: str
    props: dict = field(default_factory=dict)
    children: list = field(default_factory=list)
    event_listeners: dict = field(default_factory=dict)
    state: dict = field(default_factory=dict)
    uuid: Any = None
    signal: str = ""
    original_data: str = ""
    data: str = ""
    parentComponent: Optional[Any] = None

    # this should be replaced by a Dom Node class
    html: str = ""
    css: str = ""
    js: str = ""
    # on any property change, rebuild the tree

    def render(self):
        pass

    @property
    def is_text_component(self):
        return self.tag == "TEXT_NODE"
    
    def __repr__(self):
        return f"<{self.tag}> {self.data} </{self.tag}>"

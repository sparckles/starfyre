from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass
class Component:
    tag: str
    props: dict
    children: list
    event_listeners: dict
    state: dict
    uuid: Any
    signal: str = ""
    original_data: str = ""
    data: str = ""
    parentComponent: Optional[Any] = None
    html: str = ""
    css: str = ""
    js: str = ""
    original_name: str = ""
    # on any property change, rebuild the tree
    
    
    def __post_init__(self):
        self.original_name = self.tag
   

    def render(self):
        pass

    @property
    def is_text_component(self):
        return self.tag == "TEXT_NODE"

    @property
    def is_slot_component(self):
        return self.tag == "slot"
    
    def __repr__(self):
        return f"<{self.tag}> {self.data} {self.children} </{self.tag}>"

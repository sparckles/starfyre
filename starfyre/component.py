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
    is_slot_element: bool = False       #True for element that should be rendered into <slot> on the final html 
    is_custom: bool = False             #True for root node of custom component "<store> or <parent>"
    # on any property change, rebuild the tree
    

    def render(self):
        pass

    @property
    def is_text_component(self):
        return self.tag == "TEXT_NODE"
    
    def __repr__(self):
        return f"<{self.tag}> {self.data} {self.children} </{self.tag}>"

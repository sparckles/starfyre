from dataclasses import dataclass
from html.parser import HTMLParser
from typing import Any, Optional
from uuid import uuid4

# import js


@dataclass
class Component:
    tag: str
    props: dict
    children: list
    event_listeners: dict
    state: dict
    uuid: Any 
    original_data: str = ""
    data: str = ""
    parentComponent: Optional[ Any ] = None
    html: str = ""
    css: str = ""
    js: str = ""
    signal: str = ""
    # on any property change, rebuild the tree


    def render(self):
        pass

    @property
    def is_text_component(self):
        return self.tag == "TEXT_NODE"

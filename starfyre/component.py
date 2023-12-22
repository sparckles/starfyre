from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class Component:
    tag: str
    props: dict
    children: list
    event_listeners: dict
    uuid: Any
    signal: str = ""
    original_data: str = ""
    data: str = ""
    parentComponent: Optional[Any] = None
    # html,css, and js are debug properties. Not needed for rendering
    html: str = ""
    # this should not be a part of the rendering
    css: str = ""
    # this should not be a part of the rendering
    js: str = ""
    client_side_python: str = ""
    original_name: str = ""
    # on any property change, rebuild the tree

    @property
    def is_text_component(self):
        return self.tag == "TEXT_NODE"

    @property
    def is_slot_component(self):
        return self.tag == "slot"

    def __repr__(self):
        return f"<{self.tag}> {self.data} {self.children} </{self.tag}>"

    def to_json(self):
        return {
            "tag": self.tag,
            "props": self.props,
            "children": self.children,
            "event_listeners": self.event_listeners,
            "uuid": self.uuid,
            "signal": self.signal,
            "original_data": self.original_data,
            "data": self.data,
            "parentComponent": self.parentComponent,
            "html": self.html,
            "original_name": self.original_name,
        }

    # not including the css, js and client_side_python as they are not needed for re rendering

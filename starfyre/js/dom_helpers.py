from starfyre import js



def is_listener(name):
    return name.startswith("on")


def is_attribute(name):
    return not is_listener(name) and name != "children"


class Component:
    def __init__(
        self,
        tag: str,
        props: dict,
        children: list,
        event_listeners: dict,
        uuid: str,
        signal: str = "",
        original_data: str = "",
        data: str = "",
        parentComponent=None,
        html: str = "",
        css: str = "",
        js: str = "",
        client_side_python: str = "",
        original_name: str = "",
    ):
        self.tag = tag
        self.props = props
        self.children = children
        self.event_listeners = event_listeners
        self.uuid = uuid
        self.signal = signal
        self.original_data = data
        self.data = data
        self.parentComponent = parentComponent
        self.html = html
        self.css = css
        self.js = js
        self.client_side_python = client_side_python
        self.original_name = original_name

    @property
    def is_text_component(self):
        return self.tag == "TEXT_NODE"

    @property
    def is_slot_component(self):
        return self.tag == "slot"

    def __repr__(self):
        return f"<{self.tag}> {self.data} {self.children} </{self.tag}>"

    def re_render_helper(self, component):
        # this will rebuild the tree
        ...

        if self == component:
            print("This is the true component", component)

        for child in component.children:
            if isinstance(child, Component):
                self.re_render_helper(child)

    def re_render(self):
        print("This is the re render function")
        return self.re_render_helper(self)


def parse_component_data(data):
    if isinstance(data, dict):
        # Check if this dictionary represents a Component
        if "tag" in data and "props" in data:
            # Parse children if present
            children = data.get("children", [])
            parsed_children = [parse_component_data(child) for child in children]

            # Handle special cases like parentComponent
            if "parentComponent" in data and data["parentComponent"] is not None:
                data["parentComponent"] = parse_component_data(data["parentComponent"])

            # Create a Component instance, passing the parsed children
            data["children"] = parsed_children
            component = Component(**data)
            dom_id = component.uuid

            # need to find a way to add this component to a global dom store
            # and make it accessible to the render function
            print("This is the dom id", clientDomIdMap)
            clientDomIdMap[dom_id] = component
            return component
        else:
            # Handle other dict structures (e.g., props)
            return {k: parse_component_data(v) for k, v in data.items()}
    elif isinstance(data, list):
        # Handle lists (e.g., a list of children)
        return [parse_component_data(item) for item in data]
    else:
        # Return the item as is for basic types (int, str, etc.)
        return data


def rebuild_tree():
    print("This is the rebuild tree function")
    # this is present globally
    # TODO: need to work on this
    # js.window maybe
    STARFYRE_ROOT_NODE = getattr(js.window, "STARFYRE_ROOT_NODE")
    tree_node = STARFYRE_ROOT_NODE
    # print("This is the tree node", tree_node)
    print("This is the tree node", type(tree_node))
    json_data = json.loads(tree_node)
    tree = parse_component_data(json_data)
    print("Successfully loaded json data", json_data)
    print(tree)


rebuild_tree()

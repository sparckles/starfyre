import re
from html.parser import HTMLParser

from .component import Component


def extract_functions(obj):
    functions = {}
    for key, value in obj.items():
        if callable(value):
            functions[key] = value

    return functions


class RootParser(HTMLParser):
    generic_tags = ["div", "p", "b", "span", "i", "button"]

    def __init__(self, component_local_variables, component_global_variables):
        super().__init__()
        self.stack: list[tuple[Component, int]] = []
        self.children = []
        self.current_depth = 0

        # these are the event handlers and the props
        self.local_variables = component_local_variables
        self.global_variables = component_global_variables
        self.components = self.extract_components(component_local_variables)
        print("These are the self components", self.components)
        # populate the dict with the components

    def extract_components(self, local_functions):
        components = {}
        for key, value in local_functions.items():
            if isinstance(value, Component):
                components[key] = value

        return components

    def is_event_listener(self, name):
        return name.startswith("on")

    def is_state(self, function):
        return "create_signal" in str(function)

    def handle_starttag(self, tag, attrs):
        # logic should be to just create an empty component on start
        # and fill the contents on the end tag
        props = {}
        state = {}
        event_listeners = {}
        self.current_depth += 1

        for attr in attrs:
            print("These are the new parse attributes", attr)
            if attr[1].startswith("{") and attr[1].endswith("}"):
                attr_value = attr[1].strip("{").strip("}").strip(" ")
                if self.is_event_listener(attr[0]):
                    event_handler = None
                    if attr_value in self.global_variables:
                        event_handler = self.global_variables[attr_value]

                    # we are giving the priority to local functions
                    if attr_value in self.local_variables:
                        event_handler = self.local_variables[attr_value]

                    if event_handler is None:
                        print("Event handler not found")

                    event_listeners[attr[0]] = event_handler
                    # these are functions, so we will replace them with the actual function
                else:
                    # here we need to check if these are functions
                    # or state objects or just regular text
                    if attr_value in self.local_variables and self.is_state(
                        self.local_variables[attr_value]
                    ):
                        state[attr[0]] = self.local_variables[attr_value]
                        props[attr[0]] = self.local_variables[attr_value]()
            else:
                props[attr[0]] = attr[1]

        if tag not in self.generic_tags and tag in self.components:
            component = self.components[tag]
            tag = component.tag
            component.props = {**component.props, **props}
            component.state = {**component.state, **state}
            component.event_listeners = {**component.event_listeners, **event_listeners}
            self.stack.append((component, self.current_depth))
            printable_stack = [element[0].tag for element in self.stack]
            print(
                "Encountered a start tag :",
                tag,
                printable_stack,
                "Current depth",
                self.current_depth,
            )

            return

        # see if the attribute value is a state component
        # if it is, we use the state component

        # instead of creating a new component, we check if the tag is a global component
        # then we check the uuid of the global component
        # if the uuid is not in the stack, we create a new component
        # if the uuid is in the stack, we use the component from the stack
        # we are using a hack for now

        # if the component has already been called
        # and then we evaluate -> it will be in the store but with the wrong name
        # but we don't care about the name
        # we can just replace it with the new name
        # but the issue will be the new props that we can pass
        # lets not worry about that for now

        component = Component(tag, props, [], event_listeners, state)

        # instead of assiging tags we assign uuids
        self.stack.append((component, self.current_depth))
        printable_stack = [element[0].tag for element in self.stack]
        print(
            "Encountered a start tag :",
            tag,
            printable_stack,
            "Current depth",
            self.current_depth,
        )

    def handle_endtag(self, tag):
        # we need to check if the tag is a default component or a custom component
        # if it is a custom component, we get the element from the custom components dict
        if tag not in self.generic_tags and tag in self.components:
            component = self.components[tag]
            tag = component.tag

        print(
            "Encountered an end tag :",
            tag,
            "Current depth",
            self.current_depth,
            "Stack",
            self.stack,
            "Children",
            self.children,
        )
        parent_node, parent_depth = self.stack[
            -1
        ]  # based on the assumption that the stack is not empty
        # need to check the if this is always true

        while len(self.children) > 0:
            child, child_depth = self.children[0]
            print("These are the children", child, child_depth)
            if child_depth == parent_depth + 1:
                self.children.pop(0)
                self.stack[-1][0].children.insert(0, child)
                print("Added child", child.tag, "to parent", parent_node.tag)
            else:
                break  # we have reached the end of the children

        self.stack.pop()
        self.current_depth = parent_depth
        self.children.insert(0, (parent_node, parent_depth))

    def handle_data(self, data):
        data = data.strip().strip("\n").strip(" ")
        matches = re.findall(r"{(.*?)}", data)

        state = {}
        print("These are the matches in the text data", matches, data)

        for match in matches:
            # match can be a sentece so we will split it
            current_data = None
            if match in self.local_variables:
                current_data = self.local_variables[match]
            elif match in self.global_variables:
                current_data = self.global_variables[match]
            else:
                raise Exception("Variable not found")

            if not self.is_state(current_data) and not callable(current_data):
                data = data.replace(match, current_data)
            elif self.is_state(current_data):
                state[match] = current_data

        if data == "":
            return

        # matches can be of 4 types
        # 1. {{variable}} 2. {{function()}} 3. Props = these are all just local and global variables
        # 4. State

        # TODO handle state in text node

        self.current_depth += 1
        # this should never be in the parent stack
        # a text node is a child node as soon as it is created
        print("Encountered some text data :", data, "Current depth", self.current_depth)
        self.children.append(
            (
                Component("TEXT_NODE", {}, [], {}, state=state, data=data),
                self.current_depth,
            )
        )
        self.current_depth -= 1

    def get_stack(self):
        return self.stack

    def get_root(self):
        return self.children[0][0]

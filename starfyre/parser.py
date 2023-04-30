import re
from html.parser import HTMLParser
from uuid import uuid4

from starfyre.transpiler import transpile

from .component import Component


def extract_functions(obj):
    functions = {}
    for key, value in obj.items():
        if callable(value):
            functions[key] = value

    return functions


class RootParser(HTMLParser):
    generic_tags = ["div", "p", "b", "span", "i", "button"]

    def __init__(self, component_local_variables, component_global_variables, css, js):
        super().__init__()
        self.stack: list[tuple[Component, int]] = []
        self.children = []
        self.current_depth = 0
        self.css = css
        self.js = js

        # these are the event handlers and the props
        self.local_variables = component_local_variables
        self.global_variables = component_global_variables

        self.components = self.extract_components(
            {**self.local_variables, **self.global_variables}
        )
        # populate the dict with the components

    def extract_components(self, local_functions):
        components = {}
        for key, value in local_functions.items():
            if isinstance(value, Component):
                components[key] = value

        return components

    def is_event_listener(self, name):
        return name.startswith("on")

    def handle_starttag(self, tag, attrs):
        # logic should be to just create an empty component on start
        # and fill the contents on the end tag
        props = {}
        state = {}
        event_listeners = {}
        self.current_depth += 1

        for attr in attrs:
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

            return

        component = Component(
            tag,
            props,
            [],
            event_listeners,
            state,
            js=self.js,
            css=self.css,
            uuid=uuid4(),
        )

        # instead of assiging tags we assign uuids
        self.stack.append((component, self.current_depth))
        [(element[0].tag, element[1]) for element in self.stack]

    def handle_endtag(self, tag):
        # we need to check if the tag is a default component or a custom component
        # if it is a custom component, we get the element from the custom components dict
        if tag not in self.generic_tags and tag in self.components:
            component = self.components[tag]
            tag = component.tag

        # need to check the if this is always true
        parent_node, parent_depth = self.stack[
            -1
        ]  # based on the assumption that the stack is not empty

        while len(self.children) > 0:
            child, child_depth = self.children[0]
            if child_depth == parent_depth + 1:
                self.children.pop(0)
                self.stack[-1][0].children.insert(0, child)
            else:
                break  # we have reached the end of the children

        self.stack.pop()
        self.current_depth -= 1

        if parent_node.tag != "style" and parent_node.tag != "script":
            self.children.insert(0, (parent_node, parent_depth))

    def is_signal(self, str):
        if not str:
            return False
        return "signal" in str

    def inject_uuid(self, signal, uuid):
        return signal.replace("()", f"('{uuid}')")

    def handle_data(self, data):
        # this is doing too much
        # lexing
        # parsing

        data = data.strip().strip("\n").strip(" ")
        # regex to find all the elements that are wrapped in {}

        matches = re.findall(r"{(.*?)}", data)

        state = {}

        parent_node, parent_depth = self.stack[-1]
        uuid = uuid4()
        component_signal = ""

        for match in matches:
            # match can be a sentece so we will split it
            current_data = None
            if match in self.local_variables:
                current_data = self.local_variables[match]
            elif match in self.global_variables:
                current_data = self.global_variables[match]
            else:
                # we need to handle a case where the eval result is a signal object
                if self.is_signal(match):
                    new_js = transpile(match)
                    new_js = self.inject_uuid(new_js, uuid)
                    component_signal = new_js.strip("{").strip("}").strip(";")
                    print("new js", new_js)
                    # inject uuid in the signal function call

                    current_data = new_js

                else:
                    eval_result = eval(
                        match, self.local_variables, self.global_variables
                    )
                    if isinstance(eval_result, Component):
                        self.stack[-1][0].children.append(eval_result)
                        return
                    elif isinstance(eval_result, str):
                        current_data = eval_result
                    elif isinstance(eval_result, list):
                        current_data = " ".join([str(i) for i in eval_result])
                    else:
                        # we need to handle a case where the eval result is a state object

                        raise Exception("Variable not found")

            if not self.is_signal(current_data) and not callable(current_data):
                print("current data", current_data)
                if matches:
                    data = data.replace("{", "").replace("}", "")
                data = data.replace(match, str(current_data))

        if data == "":
            return

        # matches can be of 4 types
        # 1. {{variable}} 2. {{function()}} 3. Props = these are all just local and global variables
        # 4. State

        # TODO handle state in text node

        # this should never be in the parent stack
        # a text node is a child node as soon as it is created

        # add a parent component
        # on the wrapper div component

        wrapper_div_component = Component(
            "div",
            {},
            [],
            {},
            state=state,
            data=data,
            css=self.css,
            js=self.js,
            signal="",
            uuid=uuid,
        )

        wrapper_div_component.children.append(
            Component(
                "TEXT_NODE",
                {},
                [],
                {},
                state=state,
                data=data,
                css=self.css,
                js=self.js,
                signal=component_signal,
                uuid=uuid,
            )
        )

        parent_node.children.insert(0, wrapper_div_component)

        print(
            "parent node",
            parent_node.tag,
            parent_node.children,
            "for the text node ",
            data,
        )

    def get_stack(self):
        return self.stack

    def get_root(self):
        if len(self.children) != 0:
            return self.children[0][0]
        return Component(
            "div", {}, [], {}, state={}, data="", css=self.css, js=self.js, uuid=uuid4()
        )

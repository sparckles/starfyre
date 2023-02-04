import inspect
import re

from html.parser import HTMLParser
from uuid import uuid4

from .component import Component
from .global_components import components, new_global_components

def extract_functions(obj):
    functions = {}
    for key, value in obj.items():
        if callable(value):
            functions[key] = value

    return functions



class Parser(HTMLParser):
    def __init__(self, state):
        super().__init__()
        self.stack = []
        self.state = state # this is initialized for every component

    def handle_starttag(self, tag, attrs):
        props = {}
        for attr in attrs:
            props[attr[0]] = attr[1]

        # instead of creating a new component, we check if the tag is a global component
        # then we check the uuid of the global component
        # if the uuid is not in the stack, we create a new component
        # if the uuid is in the stack, we use the component from the stack
        # we are using a hack for now

        if tag in components:
            component = components[tag][0]
        else:
            component = Component(tag, props, [], {}, self.state)

        components[tag].append(component)
        # instead of assiging tags we assign uuids
        self.stack.append(component)

    def handle_endtag(self, tag):
        children = []
        while self.stack:
            node = self.stack[-1]
            # instead of comparing tags we compare uuids
            if isinstance(node, Component) and node.tag == tag:

                break

            self.stack.pop()
            children.append(node)

        children = children[::-1]
        if self.stack:
            self.stack[-1].children = children

    def handle_data(self, data):
        self.stack.append(Component("TEXT_NODE", {}, [], {}, self.state, data=data))

    def parse(self):
        return self.stack


class RootParser(HTMLParser):
    generic_tags = ["div", "p", "b", "span", "i", "button"]
    def __init__(self, component_local_variables, component_global_variables):
        super().__init__()
        self.stack = []
        self.local_variables = component_local_variables
        self.global_variables = component_global_variables
        self.components = self.extract_components(component_local_variables)
        print("These are the self components", self.components, new_global_components)
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
        

        for attr in attrs:
            print("These are the new parse attributes", attr)
            if self.is_event_listener(attr[0]):
                event_handler = None
                if attr[1] in self.global_variables:
                    event_handler = self.global_variables[attr[1]]

                # we are giving the priority to local functions
                if attr[1] in self.local_variables:
                    event_handler = self.local_variables[attr[1]]
                    
                if event_handler is None:
                    print("Event handler not found")

                event_listeners[attr[0]] = event_handler
                # these are functions, so we will replace them with the actual function
            else:
                # here we need to check if these are functions 
                # or state objects or just regular text
                if attr[1] in self.local_variables and self.is_state(self.local_variables[attr[1]]):
                    state[attr[0]] = self.local_variables[attr[1]]
                    props[attr[0]] = self.local_variables[attr[1]]()
                else:
                    props[attr[0]] = attr[1]

        if tag not in self.generic_tags and tag in self.components:
            component = self.components[tag]
            tag = component.tag
            component.props = {**component.props, **props}
            component.state = {**component.state, **state}
            component.event_listeners = {**component.event_listeners, **event_listeners}
            self.stack.append(component)
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
        self.stack.append(component)

    def handle_endtag(self, tag):
        unresolved_tag = tag
        if tag not in self.generic_tags and tag in self.components:
            component = self.components[tag]
            tag = component.tag

        children = []
        while self.stack:
            node = self.stack[-1]
            # instead of comparing tags we compare uuids
            # can also compare the values of the last component for robustness
            # but we don't need to do that for now
            if isinstance(node, Component) and node.tag == tag:
                break

            self.stack.pop()
            children.append(node)

        children = children[::-1]
        if self.stack:
            print("These are the children", children)
            self.stack[-1].children.extend(children)

        if unresolved_tag == 'display':
            print("These are the self This is the display component", self.stack[-1], self.stack, children)

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


        # matches can be of 4 types
        # 1. {{variable}} 2. {{function()}} 3. Props = these are all just local and global variables
        # 4. State

        # TODO handle state in text node

        self.stack.append(Component("TEXT_NODE", {}, [], {}, state=state, data=data))

    def parse(self):
        return self.stack



        





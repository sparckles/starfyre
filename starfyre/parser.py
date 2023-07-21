import re
from html.parser import HTMLParser
from uuid import uuid4

from starfyre.transpiler import transpile

from .component import Component
from .exceptions import UnknownTagError


def extract_functions(obj):
    functions = {}
    for key, value in obj.items():
        if callable(value):
            functions[key] = value

    return functions


class ComponentParser(HTMLParser):
    # this is the grammar for the parser
    # we need cover all the grammar rules

    def __init__(self, component_local_variables, component_global_variables, css, js, component_name):
        super().__init__()             
        self.stack: list[Component] = [] 
        self.current_depth = 0
        self.css = css
        self.js = js
        self.root_node = None

        # these are the event handlers and the props
        self.local_variables = component_local_variables
        self.global_variables = component_global_variables

        self.components = self.extract_components(
            {**self.local_variables, **self.global_variables}
        )
        # populate the dict with the components
        self.component_name = component_name

    generic_tags = {
        "html", "div", "p", "b", "span", "i", "button", "head", "link", "meta", "style", "title",
        "body", "section", "nav", "main", "hgroup", "h1", "h2", "h3", "h4", "h5", "h6",
        "header", "footer", "aside", "article", "address", "blockquote", "dd", "dl", "dt",
        "figcaption", "figure", "hr", "li", "ol", "ul", "menu", "pre", "a", "abbr", "bdi",
        "bdo", "br", "cite", "code", "data", "em", "mark", "q", "s", "small", "strong", "sub",
        "sup", "time", "u", "area", "audio", "img", "map", "track", "video", "embed", "iframe",
        "picture", "object", "portal", "svg", "math", "canvas", "script", "noscript", "caption",
        "col", "colgroup", "table", "tbody", "td", "tfoot", "th", "thead", "tr", "datalist",
        "fieldlist", "form", "input", "label", "legend", "meter", "optgroup", "option", "output",
        "progress", "select", "textarea", "details", "dialog", "summary"
    }
              

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

        # extracting the attributes found in the tags
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

        # if the tag is not found in the generic tags but found in custom components
        if tag not in self.generic_tags and tag in self.components:
            component = self.components[tag]
            tag = component.tag
            component.props = {**component.props, **props}
            component.state = {**component.state, **state}

            component.event_listeners = {**component.event_listeners, **event_listeners}
            self.stack.append(component)

            return

        # if the tag is not found in the generic tags and custom components
        if tag not in self.generic_tags and tag not in self.components:
            raise UnknownTagError(f'Unknown tag: "{tag}". Please review line {self.lineno} in your "{self.component_name}" component in the pyml code.')

        if self.root_node is None:
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
            self.root_node = component
        else:
            component = Component(
                tag,
                props,
                [],
                event_listeners,
                state,
                js="",
                css="",
                uuid=uuid4(),
            )

        # instead of assiging tags we assign uuids        
        
        self.stack.append(component)
        

    def handle_endtag(self, tag):
        # if the tag is not found in the generic tags and custom components
        if tag not in self.generic_tags and tag not in self.components:             
            raise UnknownTagError(f'Unknown tag: "{tag}". Please review line {self.lineno} in your "{self.component_name}" component in the pyml code.')

        # we need to check if the tag is a default component or a custom component
        # if it is a custom component, we get the element from the custom components dict          

        if tag not in self.generic_tags and tag in self.components:
            component = self.components[tag]
            tag = component.tag
        
        endtag_node = self.stack.pop()  
        self.current_depth -= 1
        if endtag_node.tag != "style" and endtag_node.tag != "script":
            if len(self.stack) > 0:
                parent_node = self.stack[-1]      #this is last item/"top element" of stack
                parent_node.children.append(endtag_node)
            else:
                self.root_node = endtag_node
      

        print("test end")    

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

        # this is a very minimal version of lexing
        # we should ideally be writing a separate layer for lexing
        data = data.strip().strip("\n").strip(" ")
        # regex to find all the elements that are wrapped in {}

        matches = re.findall(r"{(.*?)}", data)

        # parsing starts here
        state = {}
        parent_node = self.stack[-1]         
        
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
                        self.stack[-1].children.append(eval_result)
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
            css="",
            js="",
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
                css="",
                js="",
                signal=component_signal,
                uuid=uuid,
            )
        )
        
        parent_node.children.append(wrapper_div_component) 

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
        if self.root_node is not None:
            return self.root_node
        return Component(
            "div", {}, [], {}, state={}, data="", css=self.css, js=self.js, uuid=uuid4()
        )

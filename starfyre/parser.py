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
    """
    The ComponentParser is a custom HTML parser designed to parse custom components written in a specific format (resembling HTML). When parsing HTML-like structures, one of the most critical elements to handle is the hierarchy of tags: parent-child relationships.

    The self.stack attribute maintains a collection of components that are currently "open". When you encounter a start tag, you add to the stack. When you find an end tag, you pop off the stack. This allows you to maintain the nested structure inherent to HTML and similar languages.

    The self.current_children list comes into play when dealing with custom components that can be nested inside other components. This list holds the currently parsed children for a custom component, which may not directly belong to the last item in the stack but instead belong to a custom component tag within that stack item.

    Here's why self.current_children is necessary:

    Slots and Custom Components: In the handle_endtag method, there's logic that looks for a slot component. This slot seems to be a placeholder where child components get injected. If there's a slot in the component being processed, then the current children (from self.current_children) get placed into that slot. If there's no slot, the children simply get appended to the component.

    Handling custom components: If you encounter a tag that's not a generic HTML tag but is one of your custom components, the parser needs to know what child components belong to it. Instead of immediately adding children to the stack's top component, they are kept in self.current_children until it's clear where they should go.

    End Tag Handling: When the end tag of a custom component is encountered, the parser checks if this custom component has any "reserved slots" for its children. If such slots are found, the children from self.current_children are placed inside those slots. Otherwise, the parser checks the parent of the current custom component (using the stack) and appends the children to it.

    In summary, the self.current_children list is a temporary storage for child components while the parser is determining their final parent component. This is crucial when dealing with custom component logic, which may dictate where and how child components are placed within their parent component.


    TODO: All of this can be achieved using a single stack(*batman's spider sense*), but I am not sure how to do it. I will try to do it later.
    """

    def __init__(
        self,
        component_local_variables,
        component_global_variables,
        css,
        js,
        component_name,
    ):
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
        self.current_children = []

    generic_tags = {
        "html", "div", "p", "b", "span", "i", "button", "head", "link", "meta", "style", "title", "body", "section", "nav",
        "main", "hgroup", "h1", "h2", "h3", "h4", "h5", "h6", "header", "footer", "aside", "article", "address", "blockquote",
        "dd", "dl", "dt", "figcaption", "figure", "hr", "li", "ol", "ul", "menu", "pre", "a", "abbr", "bdi", "bdo", "br",
        "cite", "code", "data", "em", "mark", "q", "s", "small", "strong", "sub", "sup", "time", "u", "area", "audio", "img",
        "map", "track", "video", "embed", "iframe", "picture", "object", "portal", "svg", "math", "canvas", "script",
        "noscript", "caption", "col", "colgroup", "table", "tbody", "td", "tfoot", "th", "thead", "tr", "datalist",
        "fieldlist", "form", "input", "label", "legend", "meter", "optgroup", "option", "output", "progress", "select",
        "textarea", "details", "dialog", "summary", "slot"
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
            component.original_name = tag
            component.props = {**component.props, **props}
            component.state = {**component.state, **state}

            component.event_listeners = {
                **component.event_listeners,
                **event_listeners,
            }
            self.stack.append(component)
            print("This is the stack", self.stack)
            if self.root_node is None:
                self.root_node = component
            return

        # if the tag is not found in the generic tags and custom components
        if tag not in self.generic_tags and tag not in self.components:
            raise UnknownTagError(
                f'Unknown tag: "{tag}". Please review line {self.lineno} in your "{self.component_name}" component in the pyml code.'
            )

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
                original_name=tag,
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
                original_name=tag,
            )

        # instead of assiging tags we assign uuids

        self.stack.append(component)

    def handle_endtag(self, tag):
        # if the tag is not found in the generic tags and custom components
        if tag not in self.generic_tags and tag not in self.components:
            raise UnknownTagError(
                f'Unknown tag: "{tag}". Please review line {self.lineno} in your "{self.component_name}" component in the pyml code.'
            )

        endtag_node = self.stack.pop()
        self.current_depth -= 1

        if endtag_node.tag != "style" and endtag_node.tag != "script":
            # basically finding and replacing the slot with
            # the actual content
            new_children = []
            is_slot_used = False

            # TODO: this linear search of children is the reason of why neasted slot is not working
            for child_component in endtag_node.children:
                if (
                    child_component.is_slot_component
                ):  # We check each child in the entag_node list for the slot components
                    new_children.extend(self.current_children)
                    is_slot_used = True
                else:
                    new_children.append(child_component)

            if not is_slot_used and len(self.current_children) > 0:
                # If there arent slot tag on the template.fyre and
                # the current_children is not empty, means that the user forget
                # to add the slot tag, so we add the content to the end and let the user knows
                new_children.extend(self.current_children)
                print(
                    "Appending at the end of the stack as slot position not specified."
                )

            if endtag_node.original_name != endtag_node.tag:
                # if the tag is not found in the generic tags but found in custom components
                # we need to replace the tag with the actual component
                # and add the children to the component
                # @suelen can you come up with a better explanation for this?
                endtag_node.children = new_children
                self.current_children = []

            if len(self.stack) > 0:
                parent_node = self.stack[
                    -1
                ]  # this is last item/"top element" of stack
                if parent_node.original_name != parent_node.tag:
                    self.current_children.append(endtag_node)
                else:
                    parent_node.children.append(endtag_node)
            else:
                self.root_node = endtag_node
                self.root_node.children.extend(self.current_children)
                self.current_children = []

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
                        # TODO: replace with one of the children stack
                        self.children.append(
                            eval_result
                        )  # TODO: Check with sanskar - this is a bug, we don't have self.children
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
            original_name="div",
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
                original_name="TEXT_NODE",
            )
        )

        # We need to check if the wrapped text component should go to the "self.current_children"
        # or to parent_node children list.
        # If the text node is child of a custom tag e.g <parent></parent>,
        # that text node should go to self.current_children list, "what will be the replacement for the slot".
        # If we don't check that, the text node will be added straight to the parent_node.children
        # and consequently placed in the wrong order on the final HTML.

        if parent_node.original_name != parent_node.tag:
            self.current_children.append(wrapper_div_component)
        else:
            parent_node.children.append(wrapper_div_component)

    def get_stack(self):
        return self.stack

    def get_root(self):
        if self.root_node is not None:
            return self.root_node
        return Component(
            "div",
            {},
            [],
            {},
            state={},
            data="",
            css=self.css,
            js=self.js,
            uuid=uuid4(),
            original_name="div",
        )

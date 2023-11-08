import re
from functools import partial
from uuid import uuid4
import inspect

from .component import Component
from .transpiler import transpile_to_js


def assign_event_listeners(event_listener_name, event_listener):
    # component.dom.addEventListener(event_type, create_proxy(event_listener))
    # here we will add f strings in micropython
    # js_event_listener = transpile_to_js(event_listener)
    python_event_listener = inspect.getsource( event_listener )
    # replace  onclick with py_click
    event_listener_name = event_listener_name.replace("on", "py_")

    html = f" {event_listener_name}='{event_listener.__name__}()' "

    return html, python_event_listener


# Add event listeners
def is_listener(name):
    return name.startswith("on")


def is_attribute(name):
    return not is_listener(name) and name != "children"


def render_helper(component: Component) -> tuple[str, str, str, str]:
    parentElement = component.parentComponent
    html = "\n"
    css = ""
    js = "\n"
    client_side_python = ""

    if parentElement is None:
        parentElement = Component(
            tag="div",
            props={"id": "root"},
            children=[],
            event_listeners={},
            state={},
            uuid=uuid4(),
            original_name="div",
        )
        component.parentComponent = parentElement

    tag = component.tag
    props = component.props
    state = component.state
    data = component.data
    event_listeners = component.event_listeners

    # Create DOM element
    if component.is_text_component:
        # find all the names in "{}" and print them
        matches = re.findall(r"{(.*?)}", data)
        for match in matches:
            if match in state:
                function = state[match]
                function = partial(function, component)
                data = component.data.replace(f"{{{ match }}}", str(function()))
            else:
                print("No match found for", match, component, "This is the state", state)

        component.parentComponent.uuid = component.uuid
        html += f"{data}\n"
        component.html = html

        if component.signal:
            js += f"""
                component = document.getElementById('{component.uuid}');
                addDomIdToMap('{component.uuid}', "{ component.signal }");
                if (component) {{
                   component.innerText = `${{{ component.signal }}}`;
                }}
            """

        return html, css, js, client_side_python

    if component.css:
        css += f"{ component.css }\n"

    if component.js:
        js += f"{component.js}\n"

    html += f"<{tag} id='{component.uuid}' "

    # this is not when the component is a text component
    prop_string = ""
    for name in props:
        if is_attribute(name):
            prop_string += f" {name}='{props[name]}' "

    for name, function in event_listeners.items():
        if is_listener(name):
            new_html, new_js = assign_event_listeners(name, function)
            js += new_js
            html += new_html

    if html.endswith(">"):
        html.removesuffix(">")

    if not component.is_text_component:
        html += f"{prop_string} >"

    # Render children
    children = component.children
    # childElements.forEach(childElement => render(childElement, dom));

    for childElement in children:
        childElement.parentElement = component
        new_html, new_css, new_js, client_side_python = render_helper(childElement)
        html += new_html
        css += new_css
        js += new_js

    html += f"</{tag}>\n"

    component.html = html

    return html, css, js, client_side_python




def hydrate(component: Component) -> str:

    html, css, js, client_side_python = render_helper(component)
    final_html = f"<style>{css}</style><div id='root'>{html}</div><script>{js}</script><script type='mpy'>{client_side_python}</script>"
    return final_html


# this is a client side render and should be rendered
# on the client side
# we need to a have a client.py file where we will store
# all the client side code and the store.py code
# def render(component: Component):
    # parentElement = component.parentDom
    # if parentElement is None:
        # parentElement = js.document.createElement("div")
        # parentElement.id = "root"
        # js.document.body.appendChild(parentElement)

    # component.parentDom = parentElement
    # we will add rust later
    # dom_node = DomNode(element.tag, element.props, element.children, element.event_listeners, element.state or {})
    # dom_node.set_parent_element(parentDom)
    # print(dom_node)

    # tag = component.tag
    # props = component.props
    # state = component.state
    # data = component.data
    # print(data)

    # Create DOM element
    # if component.is_text_component:
        # find all the names in "{}" and print them
        # matches = re.findall(r"{(.*?)}", data)
        # for match in matches:
            # if match in state:
                # function = state[match]
                # function = partial(function, component)
                # data = component.data.replace(f"{{{ match }}}", str(function()))
        # dom = js.document.createTextNode(data)
        # print("Text Node", component)
    # else:
        # dom = js.document.createElement(tag)

    # component.dom = dom

    # Add event listeners
    # def isListener(name):
        # return name.startswith("on")
    # def isAttribute(name):
        # return not isListener(name) and name != "children"

    # assign_event_listeners(component, component.event_listeners)
    # set attributes

    # for name in props:
        # if isAttribute(name):
            # dom.setAttribute(name, props[name])

    # Render children
    # children = component.children
    # childElements.forEach(childElement => render(childElement, dom));
    # for childElement in children:
        # childElement.parentDom = dom
        # render(childElement)

    # // Append to parent
    # need to apply batch updates here
    # also create a tree of dom nodes in the first place
    # if parentElement.contains(dom):
        # parentElement.replaceChild(dom, parentElement.childNodes[0])
    # else:
        # parentElement.appendChild(dom)

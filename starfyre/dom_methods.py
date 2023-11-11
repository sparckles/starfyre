import re
from functools import partial
from uuid import uuid4
import inspect

from .component import Component
from .transpiler import transpile_to_js


def assign_event_listeners(event_listener_name, event_listener):
    # js_event_listener = transpile_to_js(event_listener)
    # python_event_listener = inspect.getsource( event_listener )
    # replace  onclick with py_click
    event_listener_name = event_listener_name.replace("on", "py_")

    html = f" {event_listener_name}='{event_listener}' "

    return html
 # , python_event_listener


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
            print("This is the signal", component.signal)
            js += f"""
                component = document.getElementById('{component.uuid}');
                addDomIdToMap('{component.uuid}', "{ component.signal }");
                if (component) {{
                   component.innerText = `${{{ component.signal }}}`;
                }}
            """
            
            client_side_python += f"""
                import js

                component = js.document.getElementById('{component.uuid}');
                js.addDomIdToMap('{component.uuid}', "{ component.signal }");
                if (component) {{
                   component.innerText = `${{{ component.signal }}}`;
                }}
            """
            print("This is the client side python", client_side_python)


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
        print("This is the name", name, "This is the function", function)
        if is_listener(name):
            new_html = assign_event_listeners(name, function)
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
        new_html, new_css, new_js, new_client_side_python = render_helper(childElement)
        html += new_html
        css += new_css
        js += new_js
        client_side_python += new_client_side_python

    html += f"</{tag}>\n"

    component.html = html

    return html, css, js, client_side_python




def hydrate(component: Component) -> str:
    html, css, js, client_side_python = render_helper(component)
    print("This is the client side python", client_side_python)

    final_html = f"<style>{css}</style><div id='root'>{html}</div><script>{js}</script><script type='mpy'>{client_side_python}</script>"
    return final_html


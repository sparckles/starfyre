import re
from functools import partial
from uuid import uuid4

from .transpiler import transpile_to_js


# # import js
# from pyodide import create_proxy


from .component import Component


def assign_event_listeners(event_listener_name, event_listener):
    # component.dom.addEventListener(event_type, create_proxy(event_listener))
    js_event_listener = transpile_to_js(event_listener)
    html = f" {event_listener_name}='{event_listener.__name__}()' "

    return html, js_event_listener


# there should be two renders


# render page and render component
def render_helper(component: Component) -> tuple[str, str, str]:
    # Add event listeners
    def is_listener(name):
        return name.startswith("on")

    def is_attribute(name):
        return not is_listener(name) and name != "children"

    parentElement = component.parentComponent
    html = "\n"
    css = "\n"
    js = "\n"
    if parentElement is None:
        # instead of creating an element with js
        # we need to create a div string

        parentElement = Component("div", {"id": "root"}, [], {}, {}, uuid=uuid4())
        component.parentComponent = parentElement

        # ??
        # cannot use js
        # js.document.body.appendChild(parentElement)

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
                print("No match found for", match)

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

        return html, css, js

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
        new_html, new_css, new_js = render_helper(childElement)
        html += new_html
        css += new_css
        js += new_js

    html += f"</{tag}>\n"

    component.html = html
    return html, css, js
    # // Append to parent
    # need to apply batch updates here
    # also create a tree of dom nodes in the first place
    # if parentElement.contains(dom):
    #     parentElement.replaceChild(dom, parentElement.childNodes[0])
    # else:
    #     parentElement.appendChild(dom)


def render(component: Component) -> str:
    html, css, js = render_helper(component)
    final_html = f"<style>{css}</style>{html}<script>{js}</script>"
    return final_html


def render_root(component: Component) -> str:
    html, css, js = render_helper(component)
    final_html = f"<style>{css}</style><div id='root'>{html}</div><script>{js}</script>"
    return final_html

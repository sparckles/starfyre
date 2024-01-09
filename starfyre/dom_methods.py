import json
from uuid import UUID, uuid4

from .component import Component


def assign_event_listeners(id, event_listener_name, event_listener):
    # js_event_listener = transpile_to_js(event_listener)
    # python_event_listener = inspect.getsource( event_listener )
    # replace  onclick with py_click
    event_listener_name = event_listener_name.replace("on", "")
    event_listener = event_listener.strip("()")

    client_side_python = f"""
element = js.document.querySelector("[data-pyxide-id='{id}']");
element.addEventListener('{event_listener_name}', {event_listener});
    """

    html = f"{event_listener_name}='{event_listener}' "

    return html, client_side_python


# , python_event_listener


# Add event listeners
def is_listener(name):
    return name.startswith("on")


def is_attribute(name):
    return not is_listener(name) and name != "children"


def assign_initial_signal_population(component: Component):
    return f"""
component = js.document.querySelector("[data-pyxide-id='{component.uuid}']");
if (component):
   component.innerText = {component.data}
            """


def hydration_helper(component: Component) -> tuple[str, str, str, str]:
    # this should be renamed to hydration_helper
    # actually instead of rendering here, we should just populate the  html with the initail value
    # and then the client side python should populate the html with the new value
    # and attach the event listeners, signal, etc
    # logically we should have an initial value and then the data part should be attached
    # as is
    # on hydration, the inital value should be filled in the html, which we are already doing
    # and then everything else should be attached on the client side

    parentElement = component.parentComponent
    html = "\n"
    css = ""
    js = "\n"
    client_side_python = component.client_side_python

    if parentElement is None:
        parentElement = Component(
            tag="div",
            props={"id": "root"},
            children=[],
            event_listeners={},
            uuid=uuid4(),
            original_name="div",
        )
        component.parentComponent = parentElement

    tag = component.tag
    props = component.props
    data = component.data
    event_listeners = component.event_listeners

    # Create DOM element
    if component.is_text_component:
        component.parentComponent.uuid = component.uuid
        html += f"{data}\n"
        component.html = html

        # matches = re.findall(r"{(.*?)}", data)
        # print("This is the matches", matches)
        # we need to do a better way of managing the signals
        if component.signal:
            # TODO: this part should be moved to the client
            client_side_python += assign_initial_signal_population(component)
        return html, css, js, client_side_python

    if component.css:
        css += f"{ component.css }\n"

    if component.js:
        js += f"{component.js}\n"

    html += f"<{tag} data-pyxide-id='{component.uuid}' "

    # this is not when the component is a text component
    prop_string = ""
    for name in props:
        if is_attribute(name):
            prop_string += f" {name}='{props[name]}' "

    for name, function in event_listeners.items():
        print("This is the name", name, "This is the function", function)
        if is_listener(name):
            new_html, new_client_side_python = assign_event_listeners(
                component.uuid, name, function
            )
            html += new_html
            client_side_python += new_client_side_python

    if html.endswith(">"):
        html.removesuffix(">")

    if not component.is_text_component:
        html += f"{prop_string} >"

    # Render children
    children = component.children

    for childElement in children:
        childElement.parentElement = component
        new_html, new_css, new_js, new_client_side_python = hydration_helper(
            childElement
        )
        html += new_html
        css += new_css
        js += new_js
        client_side_python += new_client_side_python

    html += f"</{tag}>\n"

    component.html = html

    return html, css, js, client_side_python


class ComponentEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Component):
            return obj.to_json()

        if isinstance(obj, UUID):
            return str(obj)
        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)


def hydrate(component: Component) -> str:
    html, css, js, client_side_python = hydration_helper(component)
    tree = json.dumps(component, cls=ComponentEncoder)

    final_html = f"""<!DOCTYPE html>
    <meta charset='UTF-8'>
    <script>window["STARFYRE_ROOT_NODE"]=`{tree}`</script>
    <script type='mpy' src='./dom_helpers.py'></script>
    <script type='mpy' config='pyscript.toml'>{client_side_python}</script>
    <style>{css}</style>
    <div data-pyxide-id='root'>{html}</div>
    <script>{js}</script>"""
    return final_html

import re
from functools import partial


# # import js
# from pyodide import create_proxy


from .component import Component


# def assign_event_listeners(component: Component, event_listeners):
#     for event_listener_name, event_listener in event_listeners.items():
#         event_type = event_listener_name.lower()[2:]
#         print(
#             "Assigning event listeners to the component",
#             component,
#             event_type,
#             event_listener,
#         )
#         component.dom.addEventListener(event_type, create_proxy(event_listener))

    

def render(component: Component) -> str:
    parentElement = component.parentComponent
    html = ""
    if parentElement is None:
        # instead of creating an element with js
        # we need to create a div string

        parentElement = Component("div", {"id": "root"}, [], {}, {})
        component.parentComponent = parentElement

        # ?? 
        # cannot use js
        # js.document.body.appendChild(parentElement)

    # we will add rust later
    # dom_node = DomNode(element.tag, element.props, element.children, element.event_listeners, element.state or {})
    # dom_node.set_parent_element(parentDom)
    # print(dom_node)

    tag = component.tag
    props = component.props
    state = component.state
    data = component.data

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

        html += f"{data}"
        component.html = html
    else:
        html += f"<{tag}>"


    # Add event listeners
    def isListener(name):
        return name.startswith("on")
    def isAttribute(name):
        return not isListener(name) and name != "children"

    # TODO: add event listeners
    # assign_event_listeners(component, component.event_listeners)
    # set attributes


    prop_string = ""
    for name in props:
        if isAttribute(name):
            prop_string += f" {name}='{props[name]}' "

    html = html.replace(">", f"{prop_string}>")
            

    # Render children
    children = component.children
    # childElements.forEach(childElement => render(childElement, dom));
    for childElement in children:
        childElement.parentElement = component
        html += render(childElement)

    # Close tag
    if not component.is_text_component:
        html += f"</{tag}>"

    component.html = html

    return html
    # // Append to parent
    # need to apply batch updates here
    # also create a tree of dom nodes in the first place
    # if parentElement.contains(dom):
    #     parentElement.replaceChild(dom, parentElement.childNodes[0])
    # else:
    #     parentElement.appendChild(dom)



def render_root(component: Component) -> str:
    html = render(component)
    return "<div id='root'>" + html + "</div>"


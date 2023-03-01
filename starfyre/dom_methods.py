import re
from functools import partial
import glob
import os
from pathlib import Path

import js
from pyodide import create_proxy
import pyodide


from .component import Component


def assign_event_listeners(component: Component, event_listeners):
    for event_listener_name, event_listener in event_listeners.items():
        event_type = event_listener_name.lower()[2:]
        print(
            "Assigning event listeners to the component",
            component,
            event_type,
            event_listener,
        )
        component.dom.addEventListener(event_type, create_proxy(event_listener))


def pre_render():
    """The purpose of this function is to get a list of all the files with .fyre extension in the current folder
    """
    current_file = Path(".")
    parent = current_file.absolute()
    print("This is the parent", parent)

    print("This is parents parent", parent.parent)

    # https://www.youtube.com/watch?v=B5bToFdBxdw

    # walk in the pyodide folder


    # for elem in pyodide.readdir(root):
    #     print("This is the pyodide eleme", elem)



    all_fire_files = glob.glob("/lib/**/*.fyre", recursive=True)

    # for rood, dir, files in os.walk("/lib", topdown=True, onerror=None, followlinks=True):
    # # # get all the files in the parent directory
    # # files = glob.glob(str(parent) + "/*.fyre")
    #     print("Walking the directory", rood, dir, files)

    #     for file in files:
    #         if file.endswith(".fyre"):
    #             print("This is the file ", file)

    print("This is the all fire files", all_fire_files)
    





def render(component: Component):
    print("Calling the pre  render")
    pre_render()
    parentElement = component.parentDom
    if parentElement is None:
        parentElement = js.document.createElement("div")
        parentElement.id = "root"
        js.document.body.appendChild(parentElement)

    component.parentDom = parentElement
    # we will add rust later
    # dom_node = DomNode(element.tag, element.props, element.children, element.event_listeners, element.state or {})
    # dom_node.set_parent_element(parentDom)
    # print(dom_node)

    tag = component.tag
    props = component.props
    state = component.state
    data = component.data
    print(data)

    # Create DOM element
    if component.is_text_component:
        # find all the names in "{}" and print them
        matches = re.findall(r"{(.*?)}", data)
        for match in matches:
            if match in state:
                function = state[match]
                function = partial(function, component)
                data = component.data.replace(f"{{{ match }}}", str(function()))
        dom = js.document.createTextNode(data)
        print("Text Node", component)
    else:
        dom = js.document.createElement(tag)

    component.dom = dom

    # Add event listeners
    def isListener(name):
        return name.startswith("on")
    def isAttribute(name):
        return not isListener(name) and name != "children"

    assign_event_listeners(component, component.event_listeners)
    # set attributes

    for name in props:
        if isAttribute(name):
            dom.setAttribute(name, props[name])

    # Render children
    children = component.children
    # childElements.forEach(childElement => render(childElement, dom));
    for childElement in children:
        childElement.parentDom = dom
        render(childElement)

    # // Append to parent
    # need to apply batch updates here
    # also create a tree of dom nodes in the first place
    if parentElement.contains(dom):
        parentElement.replaceChild(dom, parentElement.childNodes[0])
    else:
        parentElement.appendChild(dom)

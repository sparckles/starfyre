def assign_event_listeners(component, event_listeners):
    for event_listener_name, event_listener in event_listeners.items():
        event_type = event_listener_name.lower()[2:]
        print(
            "Assigning event listeners to the component",
            component,
            event_type,
            event_listener,
        )
        # component.dom.addEventListener(event_type, create_proxy(event_listener))


# def render(component: Component):
# parentElement = component.parentComponent
# if parentElement is None:
# parentElement = js.document.createElement("div")
# parentElement.id = "root"
# js.document.body.appendChild(parentElement)

# component.parentComponent = parentElement
# we will add rust later
# dom_node = DomNode(element.tag, element.props, element.children, element.event_listeners, element.state or {})
# dom_node.set_parent_element(parentComponent)
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
# childElement.parentComponent = dom
# render(childElement)

# // Append to parent
# need to apply batch updates here
# also create a tree of dom nodes in the first place
# if parentElement.contains(dom):
# parentElement.replaceChild(dom, parentElement.childNodes[0])
# else:
# parentElement.appendChild(dom)

from starfyre import get_all_fyre_files, compile, render, create_component, render_root


print(get_all_fyre_files(__file__))
compile(__file__)

# render should generate an html file per route
# then we should focus on routing
# then interactivity 
# first event handlers
# then state management

state = "123"
html = """
<div>
    <p>Hello {state} 2</p>
    <span>Hello {state} 3</span>
</div>
"""

component = create_component(html)
print("This is the component", component)
print(render(component))
print(render_root(component))



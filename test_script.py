from starfyre import get_all_fyre_files, compile, render, create_component, render_root


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


# main script

# compile all the files
# and then find the init.py file
# then render root
# then store it in a dist/index.html folder

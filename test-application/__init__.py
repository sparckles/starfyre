from .parent import parent

def mocked_request():
  return "fetched on the server"

def handle_on_click():
  js.alert("click rendered on client")
  print("handles on click")
  

from starfyre import create_component, render

def fx_app():
    # not nesting the code to preserve the frames
    component = create_component("""
  <parent hello='world'>
      <p onclick={handle_on_click}>{[ mocked_request() for i in range(4)]}</p>
  </parent>


        """,
"""
  body {
    background-color: red;
  }

""",
"""
  alert("Just in case you need to do something special")
"""
    )

    return render(component)


app=fx_app()
    
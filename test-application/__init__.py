from starfyre import create_component, render

from .parent import parent

def mocked_request():
  return "fetch_request"


def fx_app():
    # not nesting the code to preserve the frames
    component = create_component("""
  <parent hello='world'>
      <p>{[ mocked_request() for i in range(4)]}</p>
  </parent>

        """)

    return render(component)


app=fx_app()
    
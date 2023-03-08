from starfyre import create_component, render

from .parent import parent


def fx_app():
    return render(create_component("""
  <parent hello='world'>
      <p>This is a nested child</p>
  </parent>

        """))


app=fx_app()
    
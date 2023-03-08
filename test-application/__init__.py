from starfyre import create_component, render

from .parent import parent


def app():
    return render(create_component("""
  <parent hello='world'>
      <p>This is a nested child</p>
  </parent>

        """))

app()
    

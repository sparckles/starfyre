from starfyre import create_component, render

from .counter import Counter as counter
from .display import Display as display


def app():
    return render(create_component("""
  <counter hello='world'>
      <display>
          <p>This is a nested child</p>
      </display>
  </counter>

        """))
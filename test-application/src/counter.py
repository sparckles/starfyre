from starfyre import create_component
from .state import set_state, get_state


def hello(component, *args):
    set_state(get_state(component) + 1)
    print(component.tag)
    print("get_state", get_state(component))


def print_mouse_over(component, *args):
    print("mouse moved over")


def Counter():
    # create a global store
    return create_component(
        """<div class="main-content"><p onMouseOver={print_mouse_over}>Count {get_state}</p></div>
        """
    )

from starfyre import create_component
from .state import get_state, set_state


def set(component, *args):
    set_state(get_state(component) + 1)
    print(component.tag)
    print("get_state", get_state(component))


def Display():
    return create_component(
        """<button onClick={set}>
            +
        </button>
        """
    )




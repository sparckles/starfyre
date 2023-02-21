from starfyre import create_component
from .state import get_state, set_state


def set(component, *args):
    print("set", component, args)
    set_state(get_state(component) + 1)
    print("Hello world")


def Display():
    return create_component(
        """
        <div>
        <button onClick={set}>
            +
        </button>
        </div>
        """
    )




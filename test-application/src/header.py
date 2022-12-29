from starfyre import create_component


def hello(*args):
    print("div clicked")


def print_mouse_over(*args):
    print("mouse moved over")


def Body():
    # create a global store
    return create_component(
        """<div class="main-content" onClick={foo} onMouseOver={bar}>
            Hello 👋 from Starfyre
            </div>
            """,
        {"foo": hello, "bar": print_mouse_over},
    )

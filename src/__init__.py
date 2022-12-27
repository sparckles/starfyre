import starfyre
from .header import Body

from .state_store import createSignal


def main():
    [state, setState] = createSignal(0)

    div = f"<div>{Body()}</div>"
    starfyre.render_root(div)
    starfyre.main()

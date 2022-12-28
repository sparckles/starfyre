import starfyre
from .header import Body


from pyodide import create_proxy
import js

def print_hello():
    print("hello")

from .state_store import createSignal

def print_hello(*args):
    print("hello")

def main():
    [state, setState] = createSignal(0)
    js.document.getElementById("root").addEventListener("click", create_proxy(print_hello))

    # div = f"<div>{Body()}</div>"
    # starfyre.render_root(div)
    # starfyre.main()

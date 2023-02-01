import starfyre

from .counter import Counter
from .display import Display


def main():
    counter = Counter()
    display = Display()
    print("This is an innovation")
    # will fix this create_root_component
    # create_root_component will be a combination of create component and render
    print("Final not counter", starfyre.create_root_component(
        """<Counter><Display></Display></Counter>"""
    ))
    counter.children.append(display)
    print("Final counter", counter)
    starfyre.render(counter, starfyre.js.document.getElementById("root"))
    print(starfyre.sum_as_string(1, 2))

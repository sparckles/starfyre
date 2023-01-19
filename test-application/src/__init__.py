import starfyre

from .counter import Counter
from .display import Display


def main():
    counter = Counter()
    display = Display()
    counter.children.append(display)
    starfyre.render(counter, starfyre.js.document.getElementById("root"))
    print(starfyre.sum_as_string(1, 2))

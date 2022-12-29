import starfyre

from .counter import Counter
from .display import Display


def main():
    counter = Counter()
    display = Display()
    counter.children.append(display)
    # display.children.append(counter)
    print("bccc")
    # print(display)
    starfyre.render(counter, starfyre.js.document.getElementById("root"))

from starfyre import create_component, render

from .counter import Counter
from .display import Display


def main():
    counter = Counter()
    display = Display()

    render(
        create_component("""
            <counter hello='world'>
                <display>
                    <p>This is a nested child</p>
                </display>
            </counter>
        """)
    )


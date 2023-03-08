from starfyre import create_component, render

from src.counter import counter
from src.display import display

counter = counter()
display = display()

print("Hello bklo")
print(counter, display)


def test_script():
    return create_component("""
<Test>
    <counter hello='world'>
        <display>
            <p>This is a nested child</p>
        </display>
    </counter>
</Test>
        """)
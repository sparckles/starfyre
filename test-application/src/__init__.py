import starfyre
from .header import Body


def main():
    component = Body()
    starfyre.render(component, starfyre.js.document.getElementById("root"))

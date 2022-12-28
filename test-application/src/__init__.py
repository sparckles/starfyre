import starfyre
import js
from .header import Body
from pyodide import create_proxy




def main():
    body = Body()
    compoent = starfyre.create_component(body)
    print(compoent)
    starfyre.render(compoent, js.document.getElementById("root"))

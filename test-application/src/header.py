from pyodide import create_proxy
import pickle

def hello():
    return "alert('HelloWorld!');"


def Body():
# , create_proxy(hello)
    return """<div class="main-content" onClick={foo}>
            Hello 👋 from Starfyre
            </div>
            """

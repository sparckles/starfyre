
<img alt="Starfyre Logo" src="https://user-images.githubusercontent.com/29942790/221331176-609e156a-3896-4c1a-9386-7bf595dfb879.png" width="350" />

# Starfyre ⭐🔥

## Introduction:

Starfyre is a library that allows you to build reactive frontends using only Python. It is built using pyodide and wasm, which enables it to run natively in the browser. With Starfyre, you can create interactive, real-time applications with minimal effort. Simply define your frontend as a collection of observables and reactive functions, and let Starfyre handle the rest.

Please note that Starfyre is still very naive and may be buggy, as it was developed in just five days. However, it is under active development and we welcome contributions to improve it. Whether you are a seasoned web developer or new to frontend development, we hope that you will find Starfyre to be a useful tool. Its intuitive API and simple, declarative style make it easy to get started, and its powerful features allow you to build sophisticated applications.


## Installation:

The easiest way to get started is to clone `create-starfyre-app` repo. Hosted at [create-starfyre-app](https://github.com/sansyrox/create-starfyre-app)

## Sample Usage


src/__init__.py
```python
from starfyre import create_component, render

from .component import Component


def main():
    component = Component()
    render(create_component(<component></component>))
```

src/component.py
```python

from starfyre import create_component, create_signal

[get_component_state, set_state] = create_signal(0)


def updateCounter(component, *args):
    set_state(get_component_state(component) + 1)


def Component():
    return create_component("""<div onClick={updateCounter}>
        This is the component state
        <button>Click Here to increment</button> {get_component_state}
        </div>""",
    )

```

## Developing Locally

1. `make in-dev`

For more flexibility, see `make help`

## Feedback

Feel free to open an issue and let me know what you think of it. 

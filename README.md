<p align="center">
  <img alt="Starfyre Logo" src="https://user-images.githubusercontent.com/29942790/221331176-609e156a-3896-4c1a-9386-7bf595dfb879.png" width="350" />
</p>

[![Discord](https://img.shields.io/discord/1080951642070978651?label=discord&logo=discord&logoColor=white&style=for-the-badge&color=blue)](https://discord.gg/ThQcpvJMZ6)
[![Downloads](https://static.pepy.tech/badge/starfyre)](https://pepy.tech/project/starfyre)


# Starfyre ⭐🔥

## Introduction:

Starfyre is a library that allows you to build reactive frontends using only Python. With Starfyre, you can create interactive, real-time applications with minimal effort. Simply define your frontend as a collection of observables and reactive functions, and let Starfyre handle the rest.



## 📦 Installation:

```
pip install starfyre
```

A sample project is hosted on [GitHub](https://github.com/sansyrox/first-starfyre-app/).

## 🚀 Sample App

To create an application

```bash
python3 -m starfyre --create="my-app"
```


`my-app/src/__init__.fyre`
```python

from .parent import parent
from .store import store

def mocked_request():
  return "fetched on the server"


async def handle_on_click(e):
  alert("click rendered on client")
  if 1==1:
    print("Hello world")

  current_value = get_parent_signal()
  set_parent_signal(current_value + 1)
  a = await fetch('https://jsonplaceholder.typicode.com/todos/1')
  print(await a.text())
  print("handles on click")
  

<style>
  body {
    background-color: red;
  }
</style>

<pyxide>
  <store>
    <parent hello='world'>
        <span onclick={handle_on_click}>
          {[ mocked_request() for i in range(4)]}
        </span>
    </parent>
  </store>
</pyxide>


<script>
// this is the optional section 
// for third party scripts and custom js
</script>

```


## 🚀 Sample CLI usage

```bash
Usage: python -m starfyre [OPTIONS]

  Command-line interface to compile and build a Starfyre project.

  Args:

      path (str): Path to the project directory.

      build (bool): Whether to start the build package.

      create (str): Name of the project to create.

      serve (bool): Whether to serve the project.

Options:
  --path TEXT    Path to the project. Requires --build.
  --build        Compile and build package. Requires --path.
  --create TEXT  Create a new project. Requires a project name.
  --serve        Serve the project. Requires --path.
  --help         Show this message and exit.
```

## 🗒️ How to contribute

### 🏁 Get started
Please read the code of conduct and go through CONTRIBUTING.md before contributing to Starfyre. Feel free to open an issue for any clarifications or suggestions.

If you're feeling curious. You can take a look at a more detailed architecture here.

If you still need help to get started, feel free to reach out on our community discord.


## ⚙️  Developing Locally

Python version 3.10

1. Fork this [repo](https://github.com/sparckles/starfyre)
2. Clone this repo - `git clone https://github.com/sparckles/starfyre`
3. Go in to the starfyre directory - `cd starfyre`
4. Download poetry `curl -sSL https://install.python-poetry.org/ | python3 -`
5. Install the dependencies `poetry install`
6. Activate poetry virtual environment `poetry shell`
7. Run the script `./build.sh`. This command will run the build process in starfyre against the test application in `test-application` directory.
  - The `build.sh` file is a simple script that runs two commands sequentially.
    - `python -m starfyre --build=True --path="test_application/"`
        - The `path` variable here is the path to our application.
        - The `build` directory is basically a python package that contains all the compiled files. We use the `--build` flag to run that package.

8. You can find a small test application in the `test_application` directory.
9. Navigate to `cd test_application/dist`.
10. Open `index.html` in your browser to see the output.


## Feedback

Feel free to open an issue and let me know what you think of it. 

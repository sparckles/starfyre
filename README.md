<p align="center">
  <img alt="Starfyre Logo" src="https://user-images.githubusercontent.com/29942790/221331176-609e156a-3896-4c1a-9386-7bf595dfb879.png" width="350" />
</p>

[![Discord](https://img.shields.io/discord/1080951642070978651?label=discord&logo=discord&logoColor=white&style=for-the-badge&color=blue)](https://discord.gg/ThQcpvJMZ6)
[![Downloads](https://static.pepy.tech/badge/starfyre)](https://pepy.tech/project/starfyre)


# Starfyre ⭐🔥

## Introduction:

Starfyre is a library that allows you to build reactive frontends using only Python. With Starfyre, you can create interactive, real-time applications with minimal effort. Simply define your frontend as a collection of observables and reactive functions, and let Starfyre handle the rest. Starfyre is based on Pyscript for client side functions and uses the concept of `pyxides` when structuring code.

- pyxide - translates to a container. Every component is a container. It can contain other components or HTML elements.




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

It will use the [create-starfyre-app](https://github.com/sparckles/create-starfyre-app) as the template to create a new project.


### A simple component
`my-app/pages/__init__.fyre`

```python
import "../styles/index.css"

def message():
  return "World"

---client
import js

def handle_click():
  js.console.log("Hello World")
---

<pyxide>
  <div onclick={handle_click()}>
    Hello, {message()}
  </div>
</pyxide>

```

### Using Components
<details>
<summary>Click to expand</summary>

`my-app/pages/__init__.fyre`

```python
import "../styles/index.css"
from @.components.custom_component import custom_component
# @ is the alias for the source directory. e.g. my-app in our case

<pyxide>
 <custom_component></custom_component>
</pyxide>
```

`my-app/src/components/custom_component.fyre`

```python

<pyxide>
  <div> This is a custom component </div>
</pyxide>
```
</details>

### State Management

<details>
<summary>Click to expand</summary>

Signals are super early at this moment. You need to have the word "signal" when declaring a variable. e.g. get_signal, set_signal, use_signal. And use_signal and get_signal can't be evaluated on the client, i.e. can't have `{use_signal()+1}`. This will be fixed with a better serialization.

`my-app/pages/__init__.fyre`

```python

---client

[get_signal, set_signal, use_signal] = create_signal("Hello World")

def handle_click():
  set_signal("Goodbye World")
---

<pyxide>
  <div onclick={handle_click}>
    {use_signal()}
  </div>
</pyxide>

```
</details>

### Routing
<details>
<summary>File based Routing</summary>

Starfyre supports file based routing.

```bash
my-app
├── pages
│   ├── __init__.fyre
│   ├── about.fyre
│   └── nav.fyre
```

</details>

### Styling
<details>
<summary>Click to expand</summary>

Starfyre supports CSS and file based css.

```python
import "../styles/index.css"

<style>
.component {
/* CSS here */
}

</style>

<pyxide>
  <div class="component"> Hello World </div>
</pyxide>
```
</details>

### Dependencies

You need to have a `starfyre_config.toml` file in your project root directory. This file is used to specify the dependencies for your project. The dependencies are specified in the following format:

```toml

pyxide_packages = [] # for client side packages
server_packages = [] # for server side packages

[js_modules]
is_odd = "https://cdn.jsdelivr.net/npm/is-odd@3.0.1/+esm"
Fireworks = "https://cdn.jsdelivr.net/npm/fireworks-js@2.10.7/+esm"
```

You can specify the dependencies using the following commands:

```bash
python3 -m starfyre --add-pyxide-package="package-name"
python3 -m starfyre --add-server-package="package-name"
python3 -m starfyre --add-js-module="module-name" --as="alias"
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

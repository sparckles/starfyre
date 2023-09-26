
<p align="center">
  <img alt="Starfyre Logo" src="https://user-images.githubusercontent.com/29942790/221331176-609e156a-3896-4c1a-9386-7bf595dfb879.png" width="350" />
</p>

[![Discord](https://img.shields.io/discord/1080951642070978651?label=discord&logo=discord&logoColor=white&style=for-the-badge&color=blue)](https://discord.gg/ThQcpvJMZ6)

# Starfyre ⭐🔥

## Introduction:

Starfyre is a library that allows you to build reactive frontends using only Python. It is built using pyodide and wasm, which enables it to run natively in the browser. With Starfyre, you can create interactive, real-time applications with minimal effort. Simply define your frontend as a collection of observables and reactive functions, and let Starfyre handle the rest.

Please note that Starfyre is still very naive and may be buggy, as it was developed in just five days. However, it is under active development and we welcome contributions to improve it. Whether you are a seasoned web developer or new to frontend development, we hope that you will find Starfyre to be a useful tool. Its intuitive API and simple, declarative style make it easy to get started, and its powerful features allow you to build sophisticated applications.

## 📚 Documentation
**[Compiler](compiler.md)**: Learn about the compiler and its functionality.

**[ComponentParser](component_parser.md)**: Understand how the Component Parser works and its usage.

**[File-Based Router](file_based_router.md)**: Explore the file-based routing feature and use it.

**[Exceptions](exceptions.md)**: Explore all possible errors that might occur while developing with Starfyre


## 💥 What's new?! 
### 🔥 Command Line Interface (CLI) Improvement

With the recent enhancements to the Starfyre CLI, the process of building and compiling Starfyre projects has been streamlined and made more intuitive. The CLI commands have been refined to provide a simpler and more consistent experience for developers. Let's take a look at the changes that have been introduced:

#### New Compile and Build Command
```bash
python3 starfyre --build --path="test-application"
```

**🔥 File-Based Router**:
```
test-application
├───pages
    ├───home.fyre
    ├───about.fyre
```
A new file-based routing feature has been introduced! Learn how to define routes using individual files in the pages directory [here](file_based_router.md).

## 📦 Installation:

```
pip install starfyre
```

A sample project is hosted on [GitHub](https://github.com/sansyrox/first-starfyre-app/).

## 🚀 Sample App


src/__init__.fyre
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

Options:
  --path TEXT      Path to the project
  --build BOOLEAN  Compile and build package
  --help           Show this message and exit.
```

## 🗒️ How to contribute

### 🏁 Get started
Please read the code of conduct and go through `CONTRIBUTING.md` before contributing to Starfyre. Feel free to open an issue for any clarifications or suggestions.

If you're feeling curious. You can take a look at a more detailed architecture here.

If you still need help to get started, feel free to reach out on our community discord.


## ⚙️  Developing Locally

Python version 3.10

1. Fork this [repo](https://github.com/sparckles/starfyre)
2. Clone this repo - `git clone https://github.com/sparckles/starfyre`
3. Go in to the starfyre directory - `cd starfyre`
4. Download poetry `curl -sSL https://install.python-poetry.org/ | python3 -`
5. Install the dependencies `poetry install`
6. Activate poetry virtual enviromente `poetry shell`
7. Run the script `./build.sh`. This command will run the build process in starfyre against the test application in `test-application` directory.
  - The `build.sh` file is a simple script that runs two commands sequentially.
    - `python -m starfyre --dev=True --path="test-application/"`
    - `python -m starfyre --build=True --path="test-application/"`
        - The `path` variable here is the path to our application.
        - The `dev` flag here is used to start the compilation and create the `build` directory. 
        - The `build` directory is basically a python package that contains all the compiled files. We use the `--build` flag to run that package.

8. You can find a small test application in the `test-application` directory.
9. Navigate to `cd test-application/dist`.
10. Open `index.html` in your browser to see the output, run `explorer.exe index.html`.

## Running the sample app with Docker

#### Ideally, we should not be needing this. But if you are having trouble running the sample app locally, you can try this.

1. Build the image `docker build --tag starfyre .`
2. Run the container `docker run -v ./test-application:/app/test-application/ starfyre`
3. Check the `test-application` directory for `build` and `dist` directories that contain the outputs
4. If you would like to develop interactively inside the container, run `docker run -it -v ./test-application:/app/test-application/ starfyre bash`

## Feedback

Feel free to open an issue and let me know what you think of it. 

## Running Locally

`npx docsify-cli serve docs`

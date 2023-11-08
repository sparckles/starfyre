# Understanding Starfyre

To delve into the inner workings of Starfyre, we first need to grasp the fundamental aspects of a Starfyre application.

## Application Creation
```
Start
|
V
Create .fyre files
|
V
Run build command (python -m starfyre --path="path/to/app" --build)
|
V
End
```

- The journey begins by creating a Starfyre application.
- An application comprises several `.fyre` files.
- Once the application is set, it's time to build it using the command `python -m starfyre --path="path/to/app" --build`, which is predefined in `starfyre/__main__.py`.

## Build Process
```
Start
|
V
Build creates a build directory
|
V
.fyre files are transmuted into Python files (starfyre/compiler.py & def transpile_to_python())
|
V
End
```

Building the application results in the creation of a `build` directory within the application directory. This directory houses a fresh package (see `def main()` and `def create_main_file()`).

Now, our new package is essentially `test-application/build`. Interestingly, you can manually run the build directory too, using `python -m test-application/build`.

In this build process, all the `.fyre` files are transmuted into Python files, courtesy of `starfyre/compiler.py` and the `def transpile_to_python()` function.

## Python Files in the Build Directory
```
Start
|
V
For each file, create a function named fx_<file_name>
|
V
create_component function transforms pyxide, css, js, and client_side_python into a Component or a Node
|
V
client_side_python transpiles into js
|
V
ComponentParser parses pyxide, css, js, creating a Component or a Node, duplicating global and local variables
|
V
ComponentParser parses pyxide and constructs a tree out of html, returns a Component
|
V
End
```

The build directory hosts all the Python files born out of the conversion process.

Each file features a function named `fx_<file_name>`, corresponding to the file's component name. The `fx_<file_name>` function invokes the `create_component` function (defined in `starfyre/__init__.py`). This function transforms the `pyxide`, `css`, `js`, and `client_side_python` strings into a Component or a Node in our Tree.

Firstly, `client_side_python` undergoes transpilation into `js` (Refer to line 13 of `starfyre/__init__.py`).

Secondly, the `ComponentParser` steps in, parsing the `pyxide`, `css`, `js` strings and transforming them into a Component or a Node in our Tree. Additionally, it also takes care of duplicating the global and local variables of the Python file, which is crucial for copying the imports and the variables associated with the component.

The `ComponentParser` further parses the `pyxide`, constructs a tree out of the provided `html`, and returns a `Component` (`starfyre/component.py`), the root of the tree.

## Insight into the Build Directory
```
Start
|
V
In __init__.py, function fx_app() calls hydrate() function
|
V
hydrate() converts Component into the final html
|
V
End
```

Returning to the previously generated build directory, two distinguishing features are noted in the `__init__.py` file. It always contains a function named `fx_app()`, which in turn calls upon the `hydrate()` function.

The `hydrate` function takes on the task of converting the `Component` into the final, fully generated `html`.

The `fx_` functions are dynamically generated via the `python_transpiled_string` function in the `starfyre/compiler.py`.

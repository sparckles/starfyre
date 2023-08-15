from starfyre import compile
from pathlib import Path
from starfyre.file_router import FileRouter

import sys
import os
import shutil
import subprocess
import click
import importlib.resources as pkg_resources

def write_js_file(path):
    dist_path = Path(path) / "dist"
    dist_path.mkdir(exist_ok=True)
    js_store = pkg_resources.path("starfyre.js", "store.js")
    shutil.copy(str(js_store), path + "/dist/store.js")

def build_routes_output(generated_routes, path):
    write_js_file(path)

    output_file_path = path + "/build/__main__.py"
    init_file_path = path + "/build/__init__.py"
    user_routes = generated_routes[:]
    user_routes.insert(0, 'app')
    
    # create empty __init__.py file
    with open(init_file_path, "w"):
        pass

    with open(output_file_path, "w") as f:
        f.write(
            f'''from starfyre import create_component, render_root
from starfyre.exceptions import IndexFileConflictError

import os
import sys
from pathlib import Path
import importlib

def generate_pages(generated_routes, path):
    """
    Generate HTML pages for each route in the provided list of routes.

    Parameters:
    - generated_routes (list): List of generated routes.
    - path (str): Path to the project directory.

    This function generates HTML pages for each route provided in the `generated_routes` list.
    It imports the necessary components for each route, renders them using Starfyre,
    and writes the rendered content to corresponding HTML files.
    """

    out_dir = Path(path + "/dist").resolve()
    root = Path(out_dir / "..").resolve()

    # get the user defined project name
    app_name = (str(root).split('/'))[-1]

    for route_name in generated_routes:
        print(f'route name is = {{route_name}}')
        
        if route_name.lower() == 'app':
            component_key = 'app'  # For the 'app' component in `build/pages/__init__.py`
        else:
            component_key = route_name
        
        if route_name == 'app':
            module_name = f"{{Path(app_name)}}.build.pages"
        else:
            module_name= f"{{Path(app_name)}}.build.pages.{{route_name}}"
        
        try:
            module = importlib.import_module(module_name)
            if component_key == 'app':
                component = getattr(module, component_key, f"{{component_key}} does not exist")
            else:
                component = getattr(module, f'rendered_{{component_key}}')
            result = str(component)
        except ModuleNotFoundError:
            print(f"Error: Could not import module '{{module_name}}'.")
            continue

        # write to component file
        if route_name == 'app':
            route_name = 'index'  # rename to index
        with open(out_dir / f"{{route_name}}.html", "w") as html_file:
            html_file.write("<script src='store.js'></script>")
            html_file.write(result)

if __name__ == '__main__':
    generate_pages(generated_routes={user_routes}, path="{path}")
    ''')

@click.command()
@click.option("--path", help="Path to the project")
@click.option("--build", is_flag=True, help="Compile and build package")
def main(path, build):
    """
    Command-line interface to compile and build a Starfyre project.

    Args:

        path (str): Path to the project directory.\n
        build (bool): Whether to start the build package.
    """
    if not path:
        click.echo(
            "Error: Please provide a valid path using the --path flag.\nUse --help for more details")
        return

    # Convert path to absolute path
    absolute_path = Path(path).resolve()
    print(f'Absoulte path = {absolute_path}')

    if build:
        # Compile and build project
        init_file_path = absolute_path / "__init__.py"
        # Note: The routes specified in the pages folder will have generated code in the build directory.
        compile(init_file_path.resolve())

        # At this point, the project has been compiled and the build directory has been created.
        # Now, initialize the Router object and use it to handle file-based routing.
        # Basically, get all the file names from the "pages" directory
        file_router = FileRouter(absolute_path / "pages")
        routes = file_router.populate_router()

        # We have to create the main file.
        # The main file will be used to generate the HTML output for all routes found by the FileRouter, index route inclusively.
        build_routes_output(generated_routes=routes, path=str(absolute_path))

        # Start/run project
        subprocess.run(
            [sys.executable, "-m", "build"],
            cwd=path,
            # stdout=subprocess.PIPE,
            stderr=None,
        )


if __name__ == "__main__":
    main()

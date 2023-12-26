import importlib
import os
import importlib.resources as pkg_resources
import shutil
from pathlib import Path

from starfyre.dom_methods import hydrate
import toml

"""
This module defines functions to build the distribution package for a Starfyre project.
"""


def write_js_file(path: Path):
    dist_path = Path(path) / "dist"
    print("This is the dist path", dist_path)
    dist_path.mkdir(exist_ok=True)

    with pkg_resources.path("starfyre.js", "store.js") as js_store:
        store_path = dist_path / "store.js"
        print("This is the store path", store_path)
        print("This is the js store path", js_store)
        shutil.copy(str(js_store), str(store_path))


def write_python_client_file(path: Path):
    dist_path = Path(path) / "dist"
    dist_path.mkdir(exist_ok=True)
    with pkg_resources.path(
        "starfyre.js", "dom_methods.py"
    ) as dom_methods, pkg_resources.path("starfyre.js", "store.py") as store_py:
        dom_methods_path = dist_path / "dom_methods.py"
        shutil.copy(str(dom_methods), str(dom_methods_path))
        store_path = dist_path / "store.py"
        shutil.copy(str(store_py), str(store_path))


def generate_html_pages(file_routes, project_dir: Path):
    """
    Generate HTML pages for each route in the provided list of routes.

    Parameters:
    - file_routes (list): List of file routes
    - project_dir (Path): Path to the project directory.

    This function generates HTML pages for each route provided in the `file_routes` list.
    It imports the necessary components for each route, renders them using Starfyre,
    and writes the rendered content to corresponding HTML files.
    """

    dist_dir = project_dir / "dist"
    dist_dir.mkdir(exist_ok=True)  # Ensure that the dist directory exists

    for route_name in file_routes:
        print(f"Generating HTML for route: {route_name}")

        # Determine the module and component names
        module_name = (
            "build.pages"
            if route_name.lower() == "app"
            else f"build.pages.{route_name}"
        )
        component_name = "app" if route_name.lower() == "app" else route_name

        try:
            # Importing the module and getting the component
            module = importlib.import_module(module_name)
            page = getattr(module, component_name, None)
            if not page:
                raise AttributeError(
                    f"Component '{component_name}' does not exist in '{module_name}'"
                )

            print("Rendering page:", page)

            # Assuming 'hydrate' is a function that you have defined elsewhere
            rendered_page = hydrate(page)

        except ImportError as e:
            print(f"Import error: {e}")
            print("Available modules:", os.listdir("build/pages"))
            print("Current directory:", os.getcwd())
            continue
        except AttributeError as e:
            print(f"Attribute error: {e}")
            continue

        # Write the rendered content to an HTML file
        output_file_name = (
            "index.html" if route_name.lower() == "app" else f"{route_name}.html"
        )
        with open(dist_dir / output_file_name, "w") as html_file:
            html_file.write("<script src='store.js'></script>")
            # html_file.write(
            #     "<script type='module' src='https://pyscript.net/releases/2023.11.1/core.js'></script>"
            # )
            html_file.write(
                "<script type='module' src='https://cdn.jsdelivr.net/npm/@pyscript/core/dist/core.js'></script>"
            )
            html_file.write("<script type='mpy' src='./store.py'></script>")
            html_file.write("<script type='mpy' src='./dom_methods.py'></script>")
            html_file.write(rendered_page)

    # Change back to the original directory
    os.chdir(project_dir)


def copy_public_files(project_dir: Path):
    """
    Copy files from the public directory to the dist directory.

    Parameters:
    - project_dir (str): Path to the project directory.
    """
    public_dir = (project_dir / "public").resolve()
    dist_dir = (project_dir / "dist").resolve()

    dist_dir.mkdir(exist_ok=True)

    for file in public_dir.iterdir():
        destination_path = dist_dir / file.name
        if file.is_file():
            if destination_path.exists():
                destination_path.unlink()
            shutil.copy(file, destination_path)
        elif file.is_dir():
            if destination_path.exists():
                shutil.rmtree(destination_path)
            shutil.copytree(file, destination_path)


def copy_starfyre_config(project_dir: Path):
    """
    Copy the pyscript config file to the dist directory.

    Parameters:
    - project_dir (str): Path to the project directory.
    """
    dist_dir = (project_dir / "starfyre_config.toml").resolve()
    pyscript_config_path = (project_dir / "dist" / "pyscript.toml").resolve()

    with open(dist_dir, "r") as f:
        data = toml.load(f)

    pyscript_data = {}
    pyscript_data["packages"] = data["pyxide_packages"]

    js_modules_main = {}
    for js_module in data["js_modules"]:
        url = data["js_modules"][js_module]
        js_modules_main[url] = js_module

    pyscript_data["js_modules"] = {"main": js_modules_main}

    with open(pyscript_config_path, "w") as f:
        toml.dump(pyscript_data, f)


def create_dist(file_routes, project_dir_path):
    """
    create_dist creates the final dist of the project. i.e. the html, css , js and the py(script) files.

    Args:
    - file_routes (list): List of file base routes.
    - project_dir_path (str): Path to the project directory.
    """
    print("This is the project dir path", project_dir_path)
    print("These are the file routes", file_routes)
    write_js_file(project_dir_path)
    print("JS file written")
    write_python_client_file(project_dir_path)
    print("Python files written")

    # first step is to transfer everything from the public folder to the dist folder
    copy_starfyre_config(project_dir_path)
    copy_public_files(project_dir_path)
    generate_html_pages(file_routes=file_routes, project_dir=project_dir_path)

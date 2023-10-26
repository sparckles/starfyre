import importlib
import importlib.resources as pkg_resources
import shutil
from pathlib import Path

"""
This module defines functions to build the distribution package for a Starfyre project.
"""


def write_js_file(path: Path):
    dist_path = Path(path) / "dist"
    dist_path.mkdir(exist_ok=True)
    js_store = pkg_resources.path("starfyre.js", "store.js")
    store_path = dist_path / "store.js"
    shutil.copy(str(js_store), str(store_path))


def generate_html_pages(file_routes, project_dir: Path):
    """
    Generate HTML pages for each route in the provided list of routes.

    Parameters:
    - file_routes (list): List of file routes
    - project_dir (str): Path to the project directory.

    This function generates HTML pages for each route provided in the `file_routes` list.
    It imports the necessary components for each route, renders them using Starfyre,
    and writes the rendered content to corresponding HTML files.
    """

    dist_dir = Path(project_dir / "dist").resolve()

    for route_name in file_routes:
        print(f"route name is = {route_name}")

        if route_name.lower() == "app":
            component_key = (
                "app"  # For the 'app' component in `build/pages/__init__.py`
            )
        else:
            component_key = route_name

        if route_name == "app":
            module_name = "build.pages"
        else:
            module_name = f"build.pages.{route_name}"

        try:
            module = importlib.import_module(module_name)
            if component_key == "app":
                component = getattr(
                    module, component_key, f"{component_key} does not exist"
                )
            else:
                component = getattr(module, f"rendered_{component_key}")
            result = str(component)
        except ModuleNotFoundError:
            raise ImportError(
                f"Error: Unable to import the module '{module_name}'. Please address your import statements."
            )

        # write to component file
        if route_name == "app":
            route_name = "index"  # rename to index
        with open(dist_dir / f"{route_name}.html", "w") as html_file:
            html_file.write("<script src='store.js'></script>")
            # TODO: add pyscript here
            # also find a way to add various files
            html_file.write(result)

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




def create_dist(file_routes, project_dir_path):
    """
    create_dist creates the final dist of the project. i.e. the html, css , js and the py(script) files.

    Args:
    - file_routes (list): List of file base routes.
    - project_dir_path (str): Path to the project directory.
    """
    write_js_file(project_dir_path)

    # first step is to transfer everything from the public folder to the dist folder
    copy_public_files(project_dir_path)
    generate_html_pages(file_routes=file_routes, project_dir=project_dir_path)

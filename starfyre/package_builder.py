from pathlib import Path
import importlib.resources as pkg_resources
import shutil

"""
This module defines functions to build the distribution package for a Starfyre project.
"""


def get_build_main_file_content(user_routes, path):
    """
    Template for the main execution script to generate HTML pages for generated routes.

    This module defines the template for the main execution script that generates HTML pages
    for each route in the provided list of generated routes. The script imports the necessary
    components for each route, renders them using Starfyre, and writes the rendered content
    to corresponding HTML files.

    The template contains placeholders for variables that will be dynamically substituted when
    the script is used. The placeholders include the generated routes list and the path to the
    project directory.
    """

    return f"""import os
import sys
from pathlib import Path
import importlib


def generate_pages(generated_routes, path):
    '''
    Generate HTML pages for each route in the provided list of routes.

    Parameters:
    - generated_routes (list): List of generated routes.
    - path (str): Path to the project directory.

    This function generates HTML pages for each route provided in the `generated_routes` list.
    It imports the necessary components for each route, renders them using Starfyre,
    and writes the rendered content to corresponding HTML files.
    '''

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
            raise ImportError(f"Error: Unable to import the module '{{module_name}}'. Please address your import statements.")
            

        # write to component file
        if route_name == 'app':
            route_name = 'index'  # rename to index
        with open(out_dir / f"{{route_name}}.html", "w") as html_file:
            html_file.write("<script src='store.js'></script>")
            html_file.write(result)



if __name__ == '__main__':
    generate_pages(generated_routes={user_routes}, path="{path}")
    """


def write_js_file(path):
    dist_path = Path(path) / "dist"
    dist_path.mkdir(exist_ok=True)
    js_store = pkg_resources.path("starfyre.js", "store.js")
    shutil.copy(str(js_store), path + "/dist/store.js")


def prepare_html_and_main(generated_routes, path):
    """
    Build the HTML output files for each generated route and create the main execution file.

    Parameters:
    - generated_routes (list): List of generated route names.
    - path (str): Path to the project directory.

    This function gets the HTML output for each generated route based on the provided `generated_routes` list.
    It also creates the main execution file (__main__.py) that orchestrates rendering and writing HTML content to files.
    The rendered HTML content is generated by importing and utilizing the corresponding components for each route in the __main__ file.

    Args:
        generated_routes (list): A list of route names that have been generated.
        path (str): The path to the project directory.
    """
    write_js_file(path)

    main_file_path = path + "/build/__main__.py"
    init_file_path = path + "/build/__init__.py"
    main_file_content = get_build_main_file_content(
        user_routes=generated_routes, path=path
    )

    # create empty __init__.py file
    Path(init_file_path).touch()

    with open(main_file_path, "w") as f:
        f.write(main_file_content)
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

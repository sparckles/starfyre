from starfyre import create_component, render

import os
import sys
from pathlib import Path
import importlib


class FileRouter:
    """
    A router that handles file-based routing.

    This router parses the specified pages directory to automatically generate routes based on
    the file names. Each file in the pages directory is treated as a separate route. 

    Parameters:
        pages_directory (str): The path to the directory containing the pages files.
    Example:
        pages_directory = "test-application/pages"
        file_router = FileRouter(pages_directory)
    """

    def __init__(self, pages_directory):
        self.pages_directory = pages_directory


    def generate_routes(self):
        """
        Generate routes and create corresponding HTML files.

        This method generates routes based on the file names in the specified pages directory. Each file in the
        pages directory with a ".fyre" extension is considered a separate route. The route names are derived from
        the file names by removing the ".fyre" extension and converting the names to lowercase.

        The generated route names are stored in a list, and corresponding HTML files are created in the specified
        "dist" directory. The HTML files are created by transpiling the components using the `_build_output` method.

        Note:
        - This method should be called after initializing the `FileRouter` object.
        - The `_build_output` method is responsible for generating the HTML files.

        Example:
            pages_directory = "test_app/pages"
            router = FileRouter(pages_directory)
            router.generate_routes()  # This generates the routes and corresponding HTML files.

        Raises:
            FileNotFoundError: If the specified pages directory does not exist.
        """
        routes = []
        dist_dir = Path(self.pages_directory / ".." / "dist").resolve()
        if not dist_dir.exists():
            dist_dir.mkdir()

        # get file names in the "pages" directory
        for file_name in os.listdir(self.pages_directory):
            if file_name.endswith(".fyre"):
                route_name = file_name.replace(".fyre", "").lower()
                routes.append(route_name)
                # print(f'Found fyre file: New route will be = {route_name}')
                # print(f'file path for route is = {dist_dir}/{route_name}.html')

        # read the contents from the generated python files
        self._build_output(generated_routes=routes, out_dir=dist_dir)


    def _build_output(self, generated_routes, out_dir):
        """
        Transpile the output of `render(component)` to route HTML files.

        This method takes a list of generated routes and an output directory and transpiles the components
        using `render(component)`. The resulting components are then written to corresponding HTML files
        in the output directory.

        Parameters:
            generated_routes (list): A list of route names (strings) generated from the pages directory.
            out_dir (str): The path to the output directory where the HTML files will be written.

        Example:
            pages_directory = "test_app/pages"
            router = FileRouter(pages_directory)
            router.generate_routes()  # This generates the `generated_routes` list.
            out_directory = "test_app/dist"
            router._build_output(generated_routes, out_directory)
        """
        print(f'Generated routes: {generated_routes}')

        root = Path(out_dir / "..").resolve()
        app_name = (str(root).split('/'))[-1] # get the user defined project name

        for route_name in generated_routes:
            # Get the module name dynamically based on the route_name
            module_name = f"{Path(app_name)}.build.{route_name}"
            
            try:
                module = importlib.import_module(module_name)
            except ModuleNotFoundError:
                print(f"Error: Could not import module '{module_name}'.")
                continue

            component = module.__dict__[route_name]
            result = str(render(component))

            # write to component file
            with open(out_dir / f"{route_name}.html", "w") as html_file:
                html_file.write(result)

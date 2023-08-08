from starfyre import create_component, render_root
from starfyre.exceptions import IndexFileConflictError

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
            file_router = FileRouter(pages_directory)
            file_router.generate_routes()  # This generates the routes and corresponding HTML files.

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
                if route_name.lower() == 'index':
                    raise IndexFileConflictError()
                routes.append(route_name)

        return routes

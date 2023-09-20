from starfyre import create_component, render_root
from starfyre.exceptions import IndexFileConflictError

import os
import sys
from pathlib import Path
import importlib


class FileRouter:
    def __init__(self, pages_directory):
        """
        A router that handles file-based routing.

        This router parses the specified pages directory to automatically generate routes based on
        the file names. Each file in the pages directory is treated as a separate route. 

        Parameters:
            pages_directory (str): The path to the directory containing the pages files.
        Example:
            pages_directory = "test_application/pages"
            file_router = FileRouter(pages_directory)
            Initialize the FileRouter with the specified pages directory.

        Args:
            pages_directory (str): The path to the directory containing the pages files.
        """
        self.pages_directory = pages_directory

    def populate_router(self):
        """
        Collect route names from files in the specified pages directory.

        This method collects route names based on the file names in the specified pages directory.
        Each file in the pages directory with a ".fyre" extension is considered a separate route.
        The route names are derived from the file names by removing the ".fyre" extension and
        converting the names to lowercase.

        The generated route names are stored in a list, and corresponding HTML files are created
        in the specified "dist" directory.

        Returns:
            list: A list of generated route names.

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
                if route_name == '__init__':
                    routes.insert(0, 'app')
                    continue # do no add '__init__' as a route found rather use 'app'
                if route_name.lower() == 'index':
                    raise IndexFileConflictError()
                routes.append(route_name)

        return routes

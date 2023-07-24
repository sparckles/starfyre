import os
from pathlib import Path

class Router:
    """
    A router that handles file-based routing.

    This router parses the specified pages directory to automatically generate routes based on
    the file names. Each file in the pages directory is treated as a separate route, and the
    component name is derived from the file name. The routes and their corresponding component
    names are stored in a dictionary.

    Parameters:
        pages_directory (str): The path to the directory containing the pages files.
    Example:
        pages_directory = "test_app/pages"
        file_router = FileBasedRouter(pages_directory)
    """

    def __init__(self, pages_directory):
        super().__init__()
        self.pages_directory = pages_directory
        self.generate_routes()
        print(f'Number of files in "pages" directory is: {len(os.listdir(self.pages_directory))}')

    def generate_routes(self):
        """
        Parse the "pages" directory to generate routes.

        This method iterates through each file in the pages directory and adds a new route
        to the routes dictionary. The route is derived from the file name, and the component
        name is derived from the file name by converting it to title case.

        Example:
            If there is a file named "home.fyre" in the test-application/pages directory, the router will
            add a route "/home.html".

        Note:
            This method is automatically called when the Router is initialized.
        """
        for file_name in os.listdir(self.pages_directory):
            if file_name.endswith(".fyre"):
                route_name = file_name.replace(".fyre", "").lower()
                route_path = f"/{route_name}"
                print(f'Found file: {file_name} and we have generated this path: {route_path} with name: {route_name}')
                
                # use this to generate the respective html files in the app's ./pages folder
                print(f' dir: {self.pages_directory}')
                root_directory = Path(self.pages_directory ) / ".." / "dist/pages"
                if not root_directory.exists():
                    root_directory.mkdir()

                html_file_path = root_directory / f'{route_name}.html'
                print(f'File path for {route_name} is = {html_file_path}')
                html_file_path.touch()




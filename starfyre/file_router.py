from starfyre import compile

import os
from pathlib import Path


class FileRouter:
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
        self.pages_directory = pages_directory


    def generate_routes(self):
        """
        Generate route
        """
        routes = []
        print(f'Router: Absolute Path = {self.pages_directory}')
        dist_dir = Path(self.pages_directory / ".." / "dist").resolve()
        print(f'Directory to write to: {dist_dir}')
        if not dist_dir.exists():
            dist_dir.mkdir()

        # get file names in the "pages" directory
        for file_name in os.listdir(self.pages_directory):
            if file_name.endswith(".fyre"):
                route_name = file_name.replace(".fyre", "").lower()
                routes.append(route_name)
                print(f'Found fyre file: New route will be = {route_name}')
                print(f'file path for route is = {dist_dir}/{route_name}.html')

        # read the contents from the generated python files
        _generate_output(self, generated_routes=routes, out_dir=dist_dir)


def _generate_output(self, generated_routes, out_dir):
    """
    Send the output of `render_root(component)` to route html file
    """
    # build_dir = Path(self.pages_directory / ".." / "build").resolve()

    # # print(f'build directory = {build_dir}')
    # import_lines = []
    # separator_line = '\n\n# ---------- functions call ---------\n\n'
    # body_lines = []
    # export_section = ''

    # for file_ in os.listdir(build_dir):
    #     file_name = file_.replace(".py", "")
       
    #     if file_name in generated_routes:
    #         print(f'Generated python file: {file_} is defined as a route')
           
    #         # # create a build/route_generator.py file
    #         # route_gen_file_path = build_dir / "route_generator.py"
    #         # print(f"Route generator file:{route_gen_file_path}")

    #         import_lines.append(f'from .{file_name} import {file_name}')
    #         body_lines.append(f'{file_name}')

    #         # form file content
    #         import_section = "\n".join(import_lines)
    #         initial_body = 'def create_routes():'
    #         for func in body_lines:
    #             initial_body +=f"""
    # {func}"""        

    #         initial_body += """
    # return
    #         """ 
    #         main_content = import_section + separator_line + initial_body
    #         main_content += '\n\nrouter=create_routes()'
    #         print(main_content)
    pass
import os
import subprocess
import sys
from pathlib import Path

import click

from starfyre import compile
from starfyre.dist_builder import create_dist
from starfyre.file_router import FileRouter


@click.command()
@click.option("--path", help="Path to the project. Requires --build.")
@click.option(
    "--build", is_flag=True, help="Compile and build package. Requires --path."
)
@click.option("--create", help="Create a new project. Requires a project name.")
@click.option("--serve", is_flag=True, help="Serve the project. Requires --path.")
def main(path, build, create, serve):
    """
    Command-line interface to compile and build a Starfyre project.

    Args:

        path (str): Path to the project directory.\n
        build (bool): Whether to start the build package.\n
        create (str): Name of the project to create.\n
        serve (bool): Whether to serve the project.\n
    """
    # Convert path to absolute path
    if path and build:
        absolute_path = Path(path).resolve()
        print(f"Absolute path of the project = {absolute_path}")

        sys.path.append(str(absolute_path))

        # Compile and build project
        init_file_path = absolute_path / "__init__.py"
        project_directory = Path(os.path.dirname(init_file_path.resolve()))
        # Note: The routes specified in the pages folder will have generated code in the build directory.
        compile(project_directory)

        # At this point, the project has been compiled and the build directory has been created.
        # Now, initialize the Router object and use it to handle file-based routing.
        # Basically, get all the file names from the "pages" directory
        file_router = FileRouter(absolute_path / "pages")
        file_routes = file_router.populate_router()

        # We have to create the main file.
        # The main file will be used to generate the HTML output for all routes found by the FileRouter, index route inclusively.
        create_dist(file_routes=file_routes, project_dir_path=absolute_path)

    if create:
        subprocess.run(
            [
                "git",
                "clone",
                "git@github.com:sparckles/create-starfyre-app.git",
                create,
            ],
            stdout=subprocess.PIPE,
            stderr=None,
        )

    if path and serve:
        path = Path(path).resolve() / "dist"
        print("Serving the project at http://localhost:8000")
        result = subprocess.run(
            [sys.executable, "-m", "http.server", "--directory", path],
            cwd=path,
            stdout=subprocess.PIPE,
            stderr=None,
        )

        print(result.stdout.decode("utf-8"))


if __name__ == "__main__":
    main()

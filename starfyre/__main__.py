from starfyre import compile
from pathlib import Path
import sys
import os
import shutil
import subprocess
import click
import importlib.resources as pkg_resources


def write_js_file(path):
    dist_path = Path(path) / "dist"
    dist_path.mkdir(exist_ok=True)
    js_store = pkg_resources.path("starfyre.js", "store.js")
    shutil.copy(str(js_store), path + "/dist/store.js")


def create_main_file(path):
    """
    Creates a main file in the build directory.
    
    This file will be used to run the project.
    Every starfyre build will have an `__init__.py` file in the build directory.
    And the `__init__.py` file will have a component that will render the root component. It will be named `app`.

    You can have a look at the `test-application/build/__init__.py` file to see what it looks like.

    The main file is also responsible for adding the `store.js` file to the `index.html` file.
    """
    output_file_path = path + "/build/__main__.py"
    write_js_file(path)

    with open(output_file_path, "w") as f:
        f.write(
            """
from . import app
import os
from pathlib import Path


if __name__ == '__main__':
    path_ = os.path.dirname(os.path.abspath(__file__))
    directory = Path(path_ ) / ".." / "dist"
    if not directory.exists():
        directory.mkdir()

    with open(f"{directory}/index.html", "w") as f:
        f.write("<script src='store.js'></script>")
        f.write(app)
"""
        )


@click.command()
@click.option("--path", help="Path to the project")
@click.option("--build", is_flag=True, help="Compile and build package")
def main(path, build):
    """
    Command-line interface to compile and build a Starfyre project.

    Args:

        path (str): Path to the project directory.\n
        build (bool): Whether to start the build package.
    """
    if not path:
        click.echo(
            "Error: Please provide a valid path using the --path flag.\nUse --help for more details")
        return

    # Convert path to absolute path
    absolute_path = Path(path).resolve()

    if build:
        # Compile and build project
        init_file_path = absolute_path / "__init__.py"
      
        compile(init_file_path.resolve())
        # At this point, the project has been compiled and the build directory has been created.
        # But there is no main file in the build directory.
        create_main_file(str(absolute_path))

        # Start/run project
        subprocess.run(
            [sys.executable, "-m", "build"],
            cwd=path,
            stdout=subprocess.PIPE,
            stderr=None,
        )


if __name__ == "__main__":
    main()

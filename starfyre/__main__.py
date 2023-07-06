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
        create_main_file(str(absolute_path))

        # Start/run project
        subprocess.run(
            [sys.executable, "-m", "build"],
            cwd=path,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )


if __name__ == "__main__":
    main()

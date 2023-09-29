import subprocess
import sys
from pathlib import Path

import click

from starfyre import compile
from starfyre.package_builder import prepare_html_and_main
from starfyre.file_router import FileRouter


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
            "Error: Please provide a valid path using the --path flag.\nUse --help for more details"
        )
        return

    # Convert path to absolute path
    absolute_path = Path(path).resolve()
    print(f"Absolute path of the project = {absolute_path}")

    if build:
        # Compile and build project
        init_file_path = absolute_path / "__init__.py"
        # Note: The routes specified in the pages folder will have generated code in the build directory.
        compile(init_file_path.resolve())

        # At this point, the project has been compiled and the build directory has been created.
        # Now, initialize the Router object and use it to handle file-based routing.
        # Basically, get all the file names from the "pages" directory
        file_router = FileRouter(absolute_path / "pages")
        routes = file_router.populate_router()

        # We have to create the main file.
        # The main file will be used to generate the HTML output for all routes found by the FileRouter, index route inclusively.
        prepare_html_and_main(generated_routes=routes, path=str(absolute_path))

        # Start/run project
        result = subprocess.run(
            [sys.executable, "-m", "build"],
            cwd=path,
            stdout=subprocess.PIPE,
            stderr=None,
        )

        print(result.stdout.decode("utf-8"))


if __name__ == "__main__":
    main()

import toml
import os
import subprocess
import sys
from pathlib import Path
import requests

import click

from starfyre import compile
from starfyre.dist_builder import create_dist
from starfyre.file_router import FileRouter


def get_latest_version(package_name):
    url = f"https://registry.npmjs.org/{package_name}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data["dist-tags"]["latest"]
    else:
        return None


def construct_cdn_link(package_name, version):
    return f"https://cdn.jsdelivr.net/npm/{package_name}@{version}/+esm"


@click.command()
@click.option("--path", help="Path to the project. Requires --build.")
@click.option(
    "--build", is_flag=True, help="Compile and build package. Requires --path."
)
@click.option("--create", help="Create a new project. Requires a project name.")
@click.option("--serve", is_flag=True, help="Serve the project. Requires --path.")
@click.option("--add-server-dep", help="Add a Python server dependency to the project.")
@click.option("--add-pyxide-dep", help="Add a Pyxide dependency to the project.")
@click.option("--add-js-dep", help="Add a JS dependency to the project.")
@click.option("--as", "as_", help="Name of the JS dependency.")
def main(path, build, create, serve, add_server_dep, add_pyxide_dep, add_js_dep, as_):
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
        print("File routes populated", file_routes)

        # We have to create the main file.
        # The main file will be used to generate the HTML output for all routes found by the FileRouter, index route inclusively.
        create_dist(file_routes=file_routes, project_dir_path=absolute_path)
        print("Dist created")

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

    if add_server_dep:
        with open("starfyre_config.toml", "r") as f:
            # data = json.load(f)
            data = toml.load(f)

            if add_server_dep not in data["server_packages"]:
                data["server_packages"].append(add_server_dep)
            else:
                print(f"{add_server_dep} already exists in pyscript.json")
                return

        with open("starfyre_config.toml", "w") as f:
            toml.dump(data, f)

    if add_pyxide_dep:
        with open("starfyre_config.toml", "r") as f:
            # data = json.load(f)
            data = toml.load(f)

            if add_pyxide_dep not in data["pyxide_packages"]:
                data["pyxide_packages"].append(add_pyxide_dep)
            else:
                print(f"{add_pyxide_dep} already exists in pyscript.json")
                return

        with open("starfyre_config.toml", "w") as f:
            toml.dump(data, f)

    if add_js_dep:
        with open("starfyre_config.toml", "r") as f:
            data = toml.load(f)

        if add_js_dep in data["js_modules"]:
            print(f"{add_js_dep} already exists in starfyre_config.toml")
            return

        version = get_latest_version(add_js_dep)

        dependency_name = add_js_dep if not as_ else as_

        if version:
            cdn_link = construct_cdn_link(add_js_dep, version)
            data["js_modules"][dependency_name] = cdn_link
            with open("starfyre_config.toml", "w") as f:
                toml.dump(data, f)
                print(f"Added {cdn_link} to starfyre_config.toml")
        else:
            print("Failed to fetch the latest version for the package.")


if __name__ == "__main__":
    main()

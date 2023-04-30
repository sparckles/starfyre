from starfyre import compile
from pathlib import Path
import sys
import os
import shutil
import subprocess
import click

def create_main_file(path):
    print("This is the main path", path)
    output_file_path = path + "/build/__main__.py"
    store_path = path + "/build/store.js"
    dist_path = Path(path) / "dist"

    dist_path.mkdir(exist_ok=True)

    
    shutil.copy(store_path, path + "/dist/store.js")

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
@click.option("--path", default=".", help="Path to the project")
@click.option("--dev", default=False, help="Run in development mode")
@click.option("--build", default=False, help="Build the project")
def main(path, dev, build):
    red = "\033[1;31m"
    reset = "\033[0;0m"
    if dev:
        path_ = path + "/__init__.py"
        # get absolute path
        path = os.path.abspath(path_)
        compile(path)
        create_main_file(os.path.dirname(path))
    if build:
        print(red, "This is the path", path, reset)
        print("Building the project :", path)

        subprocess.run([sys.executable , "-m", "build"], cwd=path, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


    

if __name__ == "__main__":
    main()


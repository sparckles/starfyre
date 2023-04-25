from starfyre import compile
import sys
import os

def create_main_file(path):
    output_file_path = path + "/build/__main__.py"
    with open(output_file_path, "w") as f:
        f.write(
"""

from . import app
import os


if __name__ == '__main__':
    path_ = os.path.dirname(os.path.abspath(__file__))

    with open(f"{path_}/index.html", "w") as f:
        f.write(app)
"""
        )

def main():
    path = sys.argv[1] + "/__init__.py"
    # get absolute path
    path = os.path.abspath(path)
    compile(path)
    # this is a hack or not?!
    create_main_file(os.path.dirname(path))

    # after compilation, 
    # there will a new folder called `path`/build
    # create a new file called `path`/build/__main__.py

    

if __name__ == "__main__":
    main()


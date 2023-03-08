from . import app
import os

from .parent import parent

if __name__ == '__main__':
    path_ = os.path.dirname(os.path.abspath(__file__))

    print("These are the contents", app)
    # with open(f"{path_}/index.html", "w") as f:
    #     f.write(app())



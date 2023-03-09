from . import app
import os


if __name__ == '__main__':
    path_ = os.path.dirname(os.path.abspath(__file__))

    with open(f"{path_}/index.html", "w") as f:
        f.write(app)



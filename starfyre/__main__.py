from starfyre import compile
import sys
import os

def main():
    path = sys.argv[1] + "/__init__.py"
    # get absolute path
    path = os.path.abspath(path)
    compile(path)
    

if __name__ == "__main__":
    main()


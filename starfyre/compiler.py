import os
import re
import shutil
from pathlib import Path

from starfyre.exceptions import IndexFileConflictError, InitFyreMissingError

DIRECTORIES_TO_IGNORE = ["__pycache__", "build", "dist", "venv", ".git", ".vscode"]


def get_fyre_files(project_dir):
    fyre_files = []
    directories = []

    def traverse_directory(directory):
        for entry in os.listdir(directory):
            full_path = os.path.join(directory, entry)
            relative_path = os.path.relpath(full_path, project_dir)
            if os.path.isfile(full_path) and entry.endswith(".fyre"):
                # Construct the relative path
                if relative_path.lower() == "pages/index.fyre":
                    raise IndexFileConflictError()
                fyre_files.append(relative_path)
            elif (
                os.path.isdir(full_path) and relative_path not in DIRECTORIES_TO_IGNORE
            ):
                directories.append(relative_path)
                traverse_directory(full_path)

    traverse_directory(project_dir)

    return fyre_files, directories


def resolve_css_import(css_file_name, working_directory):
    """Read a css file and save it's content to a list"""
    print("This is the working directory", working_directory, css_file_name)
    css_content = []
    # we should be checking if the css files
    # are http/s
    # or have some path

    if css_file_name.startswith("."):
        # extract the path like ./ or ../ or ../../
        path = Path(css_file_name)
        import_path = working_directory / path
        import_path = import_path.resolve()
    elif css_file_name.startswith("/"):
        import_path = css_file_name
    else:
        raise Exception("Unable to understand the import path")

    with open(import_path, "r") as import_file:
        for line in import_file.readlines():
            css_content.append(line)

    return css_content


def check_absolute_import_line(line):
    """
    Check if the given line starts with an absolute fyre import statement from the specified project directory.
    e.g. from @.pages import index

    Args:
        line (str): The line to check.

    Returns:
        bool: True if the line starts with the specified import statement, False otherwise.
    """
    pattern = r"^from\s+@\."
    match = re.match(pattern, line)
    return match is not None


def get_line_type(line):
    line_starts = {
        "<style": "css",
        "<pyxide": "pyxide",
        "<script": "js",
        "---client": "client",
    }
    for start, line_type in line_starts.items():
        if line.startswith(start):
            return line_type

    return None


def parse(fyre_file_name, project_dir):
    def remove_empty_lines_from_end(lines):
        while lines and lines[-1] == "\n":
            lines.pop()
        while lines and lines[0] == "\n":
            lines.pop(0)
        if lines == []:
            return [""]
        return lines

    current_line_type = "python"
    python_lines = []
    css_lines = []
    pyxide_lines = []
    js_lines = []
    client_side_python = []
    # regex pattern to match if a line is a css import, e.g. import "style.css"
    css_import_pattern = re.compile(r"^import\s[\"\'](.*?\.css)[\"\']")
    with open(fyre_file_name, "r") as fyre_file:
        for line in fyre_file.readlines():
            css_import_match = css_import_pattern.search(line)

            # check for fyre import styles
            has_fyre_import = check_absolute_import_line(line=line)

            # If the line is a fyre import statement, modify it to ensure proper resolution
            if has_fyre_import:
                # Split the line into module part and imported component
                line = line.replace("@", "build")

            if line.startswith("<style"):
                current_line_type = "css"
                continue
            elif line.startswith("<pyxide"):
                current_line_type = "pyxide"
                continue
            elif line.startswith("<script"):
                current_line_type = "js"
                continue
            elif line.startswith("---client"):
                current_line_type = "client"  # this is a hack
                continue
            elif css_import_match:
                css_import = css_import_match.group(1)
                project_dir = Path(os.path.dirname(fyre_file_name))
                css_content = resolve_css_import(css_import, project_dir)
                css_lines += css_content
                continue
            elif (
                "</style>" in line
                or "</pyxide>" in line
                or "</script>" in line
                or "---" in line
            ):
                current_line_type = "python"
                continue
            if current_line_type == "python":
                python_lines.append(line)
            elif current_line_type == "css":
                css_lines.append(line)
            elif current_line_type == "pyxide":
                pyxide_lines.append(line)
            elif current_line_type == "js":
                js_lines.append(line)
            elif current_line_type == "client":
                client_side_python.append(line)

    return (
        remove_empty_lines_from_end(python_lines),
        remove_empty_lines_from_end(css_lines),
        remove_empty_lines_from_end(pyxide_lines),
        remove_empty_lines_from_end(js_lines),
        remove_empty_lines_from_end(client_side_python),
    )


def python_transpiled_string(
    pyxide_lines, css_lines, js_lines, client_side_python, file_name
):
    file_name = file_name.replace(".py", "").split("/")[-1]
    pyxide_lines = "".join(pyxide_lines)
    css_lines = "".join(css_lines)
    js_lines = "".join(js_lines)
    client_side_python = "".join(client_side_python)

    root_name = None

    if "__init__" in file_name:
        root_name = "app"
    else:
        root_name = file_name

    return f'''
from starfyre import create_component

def fx_{root_name}():
    # not nesting the code to preserve the frames
    component = create_component("""
{pyxide_lines}
""", css="""
{css_lines}
""", js="""
{js_lines}
""", client_side_python="""
{client_side_python}
""",
component_name="""{root_name}"""
)
    return component

{root_name}=fx_{root_name}()
'''


def transpile_to_python(
    python_lines,
    css_lines,
    pyxide_lines,
    js_lines,
    client_side_python,
    output_file_name,
) -> str:
    """
    Transpiles a fyre file into an ( IR ) python file.

    This function is responsible for:
    - parsing the fyre file into python, css, pyxide, js and client side python

    """
    final_python_lines = ["".join(python_lines)]

    main_content = python_transpiled_string(
        pyxide_lines, css_lines, js_lines, client_side_python, output_file_name
    )

    final_python_lines.append(main_content)

    return "".join(final_python_lines)


def compile(project_dir: Path):
    """
    Compiles a fyre project into a python project.
    This function is responsible for:
    - finding all fyre files in the project
    - transpiling each fyre file into a python file.
        - "transpiling" is used a bit loosely here. What we're really doing is slicing up the fyre file into different components and then inserting them into a python file.
        - We have two functions important for us in python files `create_component` and `hydrate`.
        - The `init.py` file will have a component that will hydrate and the rest of the files will have components that will be rendered inside the root component.
    """

    build_dir = project_dir / "build"
    build_dir.mkdir(exist_ok=True)
    build_init_file = build_dir / "__init__.py"
    build_init_file.touch(exist_ok=True)

    fyre_files, directories = get_fyre_files(project_dir)

    # build_dir = project_dir / "build" / "pages"  # create build pages dir
    # build_dir.mkdir(exist_ok=True)
    for directory in directories:
        build_dir = project_dir / "build" / directory

        # the styles directory is a special case
        # all the files in the styles directory should be copied to the build directory
        # we will need a global styles directory
        # maybe a better way to do this is to have a global styles directory in the public directory
        if directory == "styles":
            build_dir = project_dir / "build" / "styles"
            if build_dir.exists():
                shutil.rmtree(build_dir)
            shutil.copytree(project_dir / "styles", build_dir)
            continue

        if directory != "public" or directory != "__pycache__" or directory != "build":
            build_dir.mkdir(exist_ok=True)

    # check if pages/__init__.fyre exist else stop compilation
    if "pages/__init__.fyre" not in fyre_files:
        raise InitFyreMissingError()

    for fyre_file in fyre_files:
        python_file_name = fyre_file.replace(".fyre", ".py")
        # TODO: need to fix the parse function
        # we need to find a way to not automatically color the functions
        python_lines, css_lines, pyxide_lines, js_lines, client_side_python = parse(
            fyre_file_name=project_dir / fyre_file, project_dir=project_dir
        )
        output_file_name = project_dir / "build" / python_file_name
        python_contents = transpile_to_python(
            python_lines,
            css_lines,
            pyxide_lines,
            js_lines,
            client_side_python,
            python_file_name,
        )

        with open(output_file_name, "w") as output_file:
            output_file.write(python_contents)

    print("Compilation successful")

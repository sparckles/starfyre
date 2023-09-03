from starfyre.exceptions import InitFyreMissingError, IndexFileConflictError

import os
import re
from pathlib import Path


def get_fyre_files(project_dir):
    fyre_files = []
    for entry in os.listdir(project_dir):
        if entry.endswith(".fyre"):
            fyre_files.append(entry)
        # check inside the 'pages' folder
        if entry == 'pages':
            for file_ in os.listdir(project_dir / "pages"):
                if file_.endswith(".fyre"):
                    # check for the invalid 'index.fyre'
                    if file_.lower() == 'index.fyre':
                        raise IndexFileConflictError()
                    fyre_files.append(f'pages/{file_}')
    return fyre_files


def resolve_css_import(css_file_name, working_directory):
    """Read a css file and save it's content to a list"""
    css_content = []

    if css_file_name.startswith("."):
        css_file_name = css_file_name.replace(".", str(working_directory), 1)

    with open(css_file_name, "r") as import_file:
        for line in import_file.readlines():
            css_content.append(line)

    return css_content


def check_import_line(line, project_dir):
    
    """
    Check if the given line starts with an fyre import statement from the specified project directory.

    Args:
        line (str): The line to check.
        project_dir (str): The project directory name.

    Returns:
        bool: True if the line starts with the specified import statement, False otherwise.
    """
    project_dir_name = str(project_dir).split("/")[-1]
    pattern = rf'^from\s+{project_dir_name}\.' # checks is we have a line like 'from {project_dir}.'
    match = re.match(pattern, line)
    return match is not None


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
    pyml_lines = []
    js_lines = []
    client_side_python = []

    # regex pattern to match if a line is a css import, e.g. import "style.css"
    css_import_pattern = re.compile(r"^import\s[\"\'](.*?\.css)[\"\']")

    with open(fyre_file_name, "r") as fyre_file:
        for line in fyre_file.readlines():
            css_import_match = css_import_pattern.search(line)

            # check for fyre import styles
            has_fyre_import = check_import_line(line=line, project_dir=project_dir)

            # If the line is a fyre import statement, modify it to ensure proper resolution
            if has_fyre_import:
                # Split the line into module part and imported component
                module_part, imported_component = line.split(" import ")

                # Extract the file name to import from the module part
                file_to_import = module_part.split(".")[-1]

                # Get the name of the project directory
                project_dir_name = str(project_dir).split("/")[-1]

                # Modify the line to use the resolved import path
                line = f'from test_application.build.{file_to_import} import {imported_component}'

            if line.startswith("<style"):
                current_line_type = "css"
                continue
            elif line.startswith("<pyml"):
                current_line_type = "pyml"
                continue
            elif line.startswith("<script"):
                current_line_type = "js"
                continue
            elif line.startswith("--client"):
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
                or "</pyml>" in line
                or "</script>" in line
                or "--" in line
            ):
                current_line_type = "python"
                continue

            if current_line_type == "python":
                python_lines.append(line)
            elif current_line_type == "css":
                css_lines.append(line)
            elif current_line_type == "pyml":
                pyml_lines.append(line)
            elif current_line_type == "js":
                js_lines.append(line)
            elif current_line_type == "client":
                client_side_python.append(line)

    return (
        remove_empty_lines_from_end(python_lines),
        remove_empty_lines_from_end(css_lines),
        remove_empty_lines_from_end(pyml_lines),
        remove_empty_lines_from_end(js_lines),
        remove_empty_lines_from_end(client_side_python),
    )


def python_transpiled_string(
    pyml_lines, css_lines, js_lines, client_side_python, file_name
):
    file_name = file_name.replace(".py", "").split("/")[-1]
    pyml_lines = "".join(pyml_lines)
    css_lines = "".join(css_lines)
    js_lines = "".join(js_lines)
    client_side_python = "".join(client_side_python)

    root_name = None

    if "__init__" in file_name:
        root_name = "app"
    else:
        root_name = file_name

    if root_name == "app":
        return f'''
from starfyre import create_component, render_root

def fx_{root_name}():
    # not nesting the code to preserve the frames
    component = create_component("""
{pyml_lines}
""", css="""
{css_lines}
""", js="""
{js_lines}
""", client_side_python="""
{client_side_python}
""",
component_name="""{root_name}"""
)
    return render_root(component)

{root_name}=fx_{root_name}()
'''
    else:
        return f'''
from starfyre import create_component, render_root

def fx_{root_name}():
    component = create_component("""
{pyml_lines}
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
rendered_{root_name} = render_root({root_name})
'''


def transpile_to_python(
    python_lines,
    css_lines,
    pyml_lines,
    js_lines,
    client_side_python,
    output_file_name,
    project_dir,
):
    """
    Transpiles a fyre file into a python file.

    This function is responsible for:
    - parsing the fyre file into python, css, pyml, js and client side python

    """
    final_python_lines = ["".join(python_lines)]

    main_content = python_transpiled_string(
        pyml_lines, css_lines, js_lines, client_side_python, output_file_name
    )

    final_python_lines.append(main_content)

    output_file_name = project_dir / "build" / output_file_name

    with open(output_file_name, "w") as output_file:
        # result of the transpiled
        output_file.write("".join(final_python_lines))


def compile(entry_file_name):
    """
    Compiles a fyre project into a python project.
    This function is responsible for:
    - finding all fyre files in the project
    - transpiling each fyre file into a python file.
        - "transpiling" is used a bit loosely here. What we're really doing is slicing up the fyre file into different components and then inserting them into a python file.
        - We have two functions important for us in python files `create_component` and `render_root`. 
        - The `init.py` file will have a component that will render root and the rest of the files will have components that will be rendered inside the root component.
    """
    project_dir = Path(os.path.dirname(entry_file_name))

    build_dir = project_dir / "build"
    build_dir.mkdir(exist_ok=True)

    build_dir = project_dir / "build" / "pages"  # create build pages dir
    build_dir.mkdir(exist_ok=True)

    fyre_files = get_fyre_files(project_dir)

    # check if pages/__init__.fyre exist else stop compilation
    if 'pages/__init__.fyre' not in fyre_files:
        raise InitFyreMissingError()

    for fyre_file in fyre_files:
        python_file_name = fyre_file.replace(".fyre", ".py")
        python_lines, css_lines, pyml_lines, js_lines, client_side_python = parse(
            fyre_file_name=project_dir / fyre_file, project_dir=project_dir
        )
        transpile_to_python(
            python_lines,
            css_lines,
            pyml_lines,
            js_lines,
            client_side_python,
            python_file_name,
            project_dir,
        )

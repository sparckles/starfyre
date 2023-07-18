import os
import re
from pathlib import Path


def get_fyre_files(project_dir):
    fyre_files = []
    for file in os.listdir(project_dir):
        if file.endswith(".fyre"):
            fyre_files.append(file)
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


def parse(fyre_file_name): 
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
from starfyre import create_component

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

    file_name = output_file_name.split("/")[-1]                 #getting the file itself "without the path"
    output_file_name = project_dir / "build" / file_name

    with open(output_file_name, "w") as output_file:
        output_file.write("".join(final_python_lines))          #result of the transpiled


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

    fyre_files = get_fyre_files(project_dir) 

    for fyre_file in fyre_files:
        python_file_name = fyre_file.replace(".fyre", ".py")
        python_lines, css_lines, pyml_lines, js_lines, client_side_python = parse(
            project_dir / fyre_file
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

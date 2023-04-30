import os
from pathlib import Path


def get_fyre_files(project_dir):
    fyre_files = []
    for file in os.listdir(project_dir):
        if file.endswith(".fyre"):
            fyre_files.append(file)
    return fyre_files


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

    with open(fyre_file_name, "r") as fyre_file:
        for line in fyre_file.readlines():
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
"""
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
"""
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
    final_python_lines = ["".join(python_lines)]

    main_content = python_transpiled_string(
        pyml_lines, css_lines, js_lines, client_side_python, output_file_name
    )

    final_python_lines.append(main_content)

    file_name = output_file_name.split("/")[-1]
    output_file_name = project_dir / "build" / file_name

    with open(output_file_name, "w") as output_file:
        output_file.write("".join(final_python_lines))


def compile(entry_file_name):
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

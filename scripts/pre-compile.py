import pathlib

current_working_path = pathlib.Path(__file__).parent
application_path = current_working_path.parent / "test_application"

def get_function_template(function_lines, file_name):
    function_template = ""
    if "__init__" not in file_name:
        function_template = f"""
def {function_name}():
    return create_component(\"\"\"
    {function_lines}
    \"\"\")
        """
    else:
        function_template = f"""
def main():
    return render(
        create_component(\"\"\"
        {function_lines}
        \"\"\")
    )
    """
    return function_template


# traverse the directory and list the files with a .fyre extension
fyre_files = []
for file in application_path.glob("**/*.fyre"):
    fyre_files.append(file)

for file in fyre_files:
    print("Compiling", file)
    # compile the file
    file_name = file.name.strip("fyre").strip(".")
    new_file_name = file.parent / (file_name + ".py")

    # find all the lines till <pyml> tag
    with open(file, "r") as old_file, new_file_name.open("w") as new_file:
        lines = old_file.readlines()
        new_lines = []

        for line in lines:
            if line.strip() == "<pyml>":
                break
            new_lines.append(line)

        function_lines = []
        
        append=False
        for line in lines:
            if line.strip() == "<pyml>":
                append=True
                continue
            if line.strip() == "</pyml>":
                append=False
                continue

            if append:
                function_lines.append(line)

        function_name = file_name.lower()
        function_lines = "".join(function_lines)
        template = get_function_template(function_lines, file_name)
        new_lines.append(template)
        new_file.writelines(new_lines)


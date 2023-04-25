use std::path::Path;
use std::{collections::HashMap, io::BufRead};
use std::{fs::File, io::Write};

fn python_transpiled_string(
    pyml_lines: &str,
    css_lines: &str,
    js_lines: &str,
    file_name: &str,
) -> String {
    let file_name = file_name.replace(".py", "");

    let python_short_name = file_name.split("/").last().unwrap();
    let root_name = if python_short_name.contains("__init__") {
        "app"
    } else {
        &python_short_name
    };

    println!(
        "This is the file_name and root_name {} {}",
        file_name, root_name
    );

    if root_name == "app" {
        return format!(
            "
from starfyre import create_component, render

def fx_{0}():
    # not nesting the code to preserve the frames
    component = create_component(\"\"\"
{1}
        \"\"\",
\"\"\"
{2}
\"\"\",
\"\"\"
{3}
\"\"\"
    )

    return render(component)


{0}=fx_{0}()
    ",
            root_name, pyml_lines, css_lines, js_lines
        );
    } else {
        return format!(
            "
from starfyre import create_component

def fx_{0}():
    component = create_component(\"\"\"
{1}
        \"\"\",
\"\"\"
{2}
\"\"\",
\"\"\"
{3}
\"\"\"
    )
    return component


{0}=fx_{0}()
    ",
            root_name, pyml_lines, css_lines, js_lines
        );
    }
}

pub fn transpile_to_python(
    python_lines: Vec<String>,
    pyml_lines: Vec<String>,
    css_lines: Vec<String>,
    js_lines: Vec<String>,
    output_file: &str,
    output_directory: &Path,
) {
    let mut final_output = vec![];
    final_output.push(python_lines.join("\n"));

    let main_content = python_transpiled_string(
        &pyml_lines.join("\n"),
        &css_lines.join("\n"),
        &js_lines.join("\n"),
        output_file,
    );
    final_output.push(main_content);

    let file_name = output_file.split("/").last().unwrap();
    let output_file_path = output_directory.join(file_name);

    println!("Output file path {:?}", output_file_path);
    let mut write_buffer = File::create(output_file_path).unwrap();
    println!(
        "Written python files {:?} {:?}",
        &output_file, &final_output
    );
    write_buffer
        .write_all(final_output.join("\n").as_bytes())
        .unwrap();
}

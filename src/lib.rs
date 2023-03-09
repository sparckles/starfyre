use pyo3::{
    prelude::*,
    types::{PyDict, PyList},
};
use std::path::Path;
use std::{collections::HashMap, io::BufRead};
use std::{fs::File, io::Write};
use walkdir::WalkDir;

/// Formats the sum of two numbers as string.
#[pyfunction]
fn sum_as_string(a: usize, b: usize) -> PyResult<String> {
    Ok((a + b).to_string())
}

#[pyfunction]
fn get_all_fyre_files(file_name: &str) -> Vec<String> {
    // get all the files in the directory of the file that end with .fyre
    let path = Path::new(file_name);
    let directory = path.parent().unwrap();
    println!("This is the file name {:?}", directory);

    let mut filenames = Vec::new();

    for entry in WalkDir::new(directory)
        .into_iter()
        .filter_map(Result::ok)
        .filter(|e| !e.file_type().is_dir())
    {
        let f_name = String::from(entry.file_name().to_string_lossy());
        let absoltue_name = String::from(entry.path().to_string_lossy());

        if f_name.ends_with(".fyre") {
            filenames.push(absoltue_name);
        }
    }

    filenames
}

fn get_function_template(pyml_lines: &str, file_name: &str, root_name: &str) -> String {
    let file_name = file_name.replace(".py", "");

    if file_name.contains("__init__") {
        return format!(
            "
from starfyre import create_component, render

def fx_{0}():
    # not nesting the code to preserve the frames
    component = create_component(\"\"\"
{1}
        \"\"\")

    return render(component)


{0}=fx_{0}()
    ",
            root_name, pyml_lines
        );
    } else {
        return format!(
            "
from starfyre import create_component

def fx_{0}():
    component = create_component(\"\"\"
{1}
        \"\"\")

    return component


{0}=fx_{0}()
    ",
            root_name, pyml_lines
        );
    }
}

#[pyfunction]
fn compile(file_name: &str) {
    // get all the files in the directory of the file that end with .fyre
    let fyre_files = get_all_fyre_files(file_name);

    for fyre_file in fyre_files {
        let python_file = fyre_file.replace(".fyre", ".py");

        let fyre_file_pointer = File::open(fyre_file).unwrap();
        let fyre_file_reader = std::io::BufReader::new(fyre_file_pointer);
        let mut python_lines: Vec<String> = vec![];
        let mut pyml_lines = vec![];

        let mut python_flag = true;
        let mut root_name = String::from("");

        for line in fyre_file_reader.lines() {
            let copy_line = line.unwrap().clone();
            let is_pyml_line = copy_line.clone().trim().starts_with("<");
            if !python_flag || is_pyml_line {
                python_flag = false;
                let copy_line = copy_line.clone();
                if root_name == "" && is_pyml_line {
                    let root_name_temp = copy_line.clone();
                    // .split_once(' ').unwrap();
                    let split: Vec<&str> = root_name_temp.split(' ').into_iter().collect();
                    if !split.is_empty() && split[0] != "" {
                        // check for trim
                        root_name = split[0].replace("<", "").replace(">", "").to_string();
                        continue;
                    }
                };

                if copy_line.trim().starts_with(&format!("<{0}", root_name))
                    || copy_line.trim().starts_with(&format!("</{0}", root_name))
                {
                    continue;
                }

                pyml_lines.push(copy_line);
            } else if python_flag {
                python_lines.push(copy_line.to_string());
            }
        }

        let template = get_function_template(&pyml_lines.join("\n"), &python_file, &root_name);

        println!("Written python files {:?} {:?}", &python_file, &template);
        python_lines.push(template);

        let mut write_buffer = File::create(python_file).unwrap();
        write_buffer
            .write_all(python_lines.join("\n").as_bytes())
            .unwrap();
    }
}
/// A Python module implemented in Rust.
#[pymodule]
fn starfyre(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(sum_as_string, m)?)?;
    m.add_function(wrap_pyfunction!(get_all_fyre_files, m)?)?;
    m.add_function(wrap_pyfunction!(compile, m)?)?;
    Ok(())
}

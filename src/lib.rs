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
            println!("{}", absoltue_name);
            filenames.push(absoltue_name);
        }
    }

    filenames
}

fn get_function_template(pyml_lines: &str, file_name: &str) -> String {
    let file_name = file_name.strip_suffix(".py").unwrap();
    let mut function_template = "";

    if file_name.contains("__init__") {
        return format!(
            "
def {0}():
    return render(create_component(\"\"\"
{1}
        \"\"\"))",
            file_name, pyml_lines
        );
    } else {
        return format!(
            "
def {0}():
    return create_component(\"\"\"
{1}
        \"\"\")",
            file_name, pyml_lines
        );
    }
}

#[pyfunction]
fn compile(file_name: &str) {
    // get all the files in the directory of the file that end with .fyre
    let fyre_files = get_all_fyre_files(file_name);

    for fyre_file in fyre_files {
        let python_file = fyre_file.replace(".fyre", ".py");
        println!("This is the python file {}", python_file);

        let fyre_file_pointer = File::open(fyre_file).unwrap();
        let fyre_file_reader = std::io::BufReader::new(fyre_file_pointer);
        let mut python_lines = vec![];
        let mut pyml_lines = vec![];

        let mut python_flag = true;

        for line in fyre_file_reader.lines() {
            let copy_line = line.unwrap().clone();
            if !python_flag || copy_line.clone().trim().starts_with("<") {
                python_flag = false;
                pyml_lines.push(copy_line)
            } else if python_flag {
                python_lines.push(copy_line.clone());
            }
        }

        let file_name_short = Path::new(&file_name).file_name().unwrap().to_string_lossy();
        let template = get_function_template(&pyml_lines.join("\n"), &file_name_short);
        python_lines.push(template);
        println!("Written python files {:?}", &python_file);

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

mod parser;
mod scanner;
mod transpiler;

use pyo3::{
    prelude::*,
    types::{PyDict, PyList},
};
use std::path::Path;

use scanner::get_all_fyre_files;

/// Formats the sum of two numbers as string.
#[pyfunction]
fn sum_as_string(a: usize, b: usize) -> PyResult<String> {
    Ok((a + b).to_string())
}

#[pyfunction]
fn compile(entry_file_name: &str) {
    // entry file name is the file that is passed in from the command line
    // also the `__init__.fyre` file of the target application

    // get all the files in the directory of the file that end with .fyre
    // traverse all the files and then transpile them from .fyre to .py
    // try creating a directory that

    let entry_file_path = Path::new(entry_file_name);
    let project_directory = entry_file_path.parent().unwrap();

    // create a new directory called `build` in the project directory
    let build_directory = project_directory.join("build");
    let build_directory_path = build_directory.as_path();
    std::fs::create_dir_all(&build_directory).unwrap();

    // get all the fyre files in the project directory
    let fyre_files = get_all_fyre_files(project_directory);

    for fyre_file in fyre_files {
        let python_file = fyre_file.replace(".fyre", ".py");

        let (python_lines, css_lines, pyml_lines, js_lines) = parser::parse_fyre_file(&fyre_file);

        // here the transpiler is transpiling from pyml to python
        // we will also have another transpiler from python to js
        // akin to how we have two parsers - one is html parser
        // the other one is fyre file parser
        transpiler::transpile_to_python(
            python_lines,
            pyml_lines,
            css_lines,
            js_lines,
            &python_file,
            build_directory_path,
        );
    }
}
/// A Python module implemented in Rust.
#[pymodule]
fn starfyre(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(sum_as_string, m)?)?;
    m.add_function(wrap_pyfunction!(compile, m)?)?;
    Ok(())
}

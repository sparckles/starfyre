mod parser;
mod scanner;
mod transpiler;

use pyo3::{
    prelude::*,
    types::{PyDict, PyList},
};
use std::{collections::HashMap, io::BufRead};
use std::{fs::File, io::Write};

use scanner::get_all_fyre_files;

/// Formats the sum of two numbers as string.
#[pyfunction]
fn sum_as_string(a: usize, b: usize) -> PyResult<String> {
    Ok((a + b).to_string())
}

#[pyfunction]
fn compile(file_name: &str) {
    // get all the files in the directory of the file that end with .fyre
    let fyre_files = get_all_fyre_files(file_name);
    // root name should be file name

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

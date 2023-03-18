use std::{collections::HashMap, io::BufRead};
use std::{fs::File, io::Write};

pub fn parse_fyre_file(file: &str) -> (Vec<String>, Vec<String>, Vec<String>, Vec<String>) {
    let fyre_file_pointer = File::open(file).unwrap();
    let fyre_file_reader = std::io::BufReader::new(fyre_file_pointer);

    let possible_line_types = ["python", "css", "pyml", "js"].iter();
    let mut current_line_type = "python";
    let mut python_lines = vec![];
    let mut css_lines = vec![];
    let mut pyml_lines = vec![];
    let mut js_lines = vec![];

    for line in fyre_file_reader.lines() {
        let line = line.unwrap().clone();
        if line.starts_with("<style") {
            current_line_type = "css";
            continue;
        } else if line.starts_with("<pyml") {
            current_line_type = "pyml";
            continue;
        } else if line.starts_with("<script") {
            current_line_type = "js";
            continue;
        } else if line.ends_with("/pyml>")
            || line.ends_with("/style>")
            || line.ends_with("/script>")
        {
            // for tags like /pyml> , /style>, /script>
            continue;
        }

        println!(
            "Current line type and line {:?} {:?}",
            &current_line_type, &line
        );

        match current_line_type {
            "python" => {
                python_lines.push(line.to_string());
            }
            "css" => {
                css_lines.push(line.to_string());
            }
            "pyml" => {
                pyml_lines.push(line.to_string());
            }
            "js" => {
                js_lines.push(line.to_string());
            }
            _ => {}
        }
    }

    return (python_lines, css_lines, pyml_lines, js_lines);
}

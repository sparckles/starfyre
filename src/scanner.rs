use std::path::Path;
use walkdir::WalkDir;

pub fn get_all_fyre_files(project_directory_path: &Path) -> Vec<String> {
    // get all the files in the directory of the file that end with .fyre

    let mut filenames = Vec::new();

    for entry in WalkDir::new(project_directory_path)
        .into_iter()
        .filter_map(Result::ok)
        .filter(|e| !e.file_type().is_dir())
    {
        let f_name = String::from(entry.file_name().to_string_lossy());
        let absolute_name = String::from(entry.path().to_string_lossy());

        if f_name.ends_with(".fyre") {
            filenames.push(absolute_name);
        }
    }

    filenames
}

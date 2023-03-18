use std::path::Path;
use walkdir::WalkDir;

pub fn get_all_fyre_files(file_name: &str) -> Vec<String> {
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

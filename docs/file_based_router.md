# File-Based Routing in Starfyre

### Introduction
This document provides an overview of the file-based routing feature. This feature enables developers to implement navigation capabilities in their applications through the use of structured file-based routes.

### Feature Overview
The file-based routing feature in Starfyre allows developers to define and manage routes for their applications using individual files. Each file corresponds to a route, and the routing system automatically generates routes based on the filenames within a specified directory.

## Implementation Details

###  Pages Directory Structure
To utilize the file-based routing feature, developers need to create a pages directory within their Starfyre application project. This directory serves as the location for storing the route-defining files.

### File Router (FileRouter class)
The `FileRouter` class is responsible for collecting route names from files within the pages directory. This class parses each file name and generates a list of route names based on those filenames.

Here is a simplified structure of the `FileRouter` class:

```python
class FileRouter:
    def __init__(self, pages_directory):
        # Constructor details...

    def populate_router(self):
        # Method details...

```

### Route Generation
When the FileRouter is initialized and the `populate_router` method is called, the router scans the files in the pages directory. Files with the `.fyre` extension are considered routes. The route names are derived from these filenames, with the .fyre extension removed and converted to lowercase. The router also handles special cases like avoiding the `__init__` route and checking for conflicts with the `index` route.

### HTML Output and Main File Generation
A function called `prepare_html_and_main` takes the list of generated route names and generates HTML output files for each route. Additionally, it creates the main execution file `(build/__main__.py)` that orchestrates rendering and writing HTML content to files. This main file imports and uses corresponding components for each route to render the HTML content.

### Usage Example
Here's an example of how you can use the file-based routing feature within your Starfyre application:

- Create a `pages` directory within your project.
- Define separate `.fyre` files within the `pages` directory, each representing a route.

### Conclusion
The file-based routing feature in Starfyre provides a convenient and structured way to implement navigation capabilities within your applications. By organizing routes as separate files, developers can efficiently manage navigation logic and enhance the user experience of their applications.

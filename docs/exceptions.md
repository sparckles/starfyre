# Exception Classes

### Introduction
This document provides an overview of newly introduced errors within the Starfyre framework.

### InitFyreMissingError
This exception class is raised when the `pages/__init__.fyre` file is missing in the project directory. It ensures that the `__init__.fyre` file is present to maintain the project's structure.

### IndexFileConflictError
Raised when a `.fyre` file named `index.fyre` is found in the pages folder. This conflicts with the code generation process, as `__init__.fyre` is transpiled into `index.html`. This exception prevents conflicts and ensures smooth code generation.

### UnknownTagError
As part of this improvement, an `UnknownTagError` exception class has been introduced. This exception is raised when an unknown tag is encountered during parsing. It helps identify which component had the unknown tag, making debugging and troubleshooting easier.
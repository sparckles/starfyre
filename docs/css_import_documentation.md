# CSS Import implementation

### Introduction
This document describes the usage of importing CSS resources as separate files into Starfyre projects.


### Feature Description
The app now supports a way to provide CSS styling via external file. To do that, use the syntax:
`import <relative or absolute path to CSS file>`
If relative path is used, it must start from `.` and the css file should be placed in the (same folder as the template, and both should be inside the application folder.)


### Usage Example
An example is located in the test-project `test-application` folder under Starfyre’s [repo](https://github.com/sparckles/starfyre/tree/main/test-application)

```python
import "./css_file_test.css"
```
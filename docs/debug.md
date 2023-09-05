# Debugger Setup

### Introduction

This document is intended for developers who want to setup a debugger for this project in VS Code.

### ⚙️ Follow The Steps:

1. Open project
2. Run
	- `poetry shell`
	- `poetry env info`

	check output:
		Virtualenv
		Python:         3.10.6
		Implementation: CPython
		Path:           /home/suelenk/.cache/pypoetry/virtualenvs/starfyre--dCuxLEF-py3.10
		Executable:     /home/suelenk/.cache/pypoetry/virtualenvs/starfyre--dCuxLEF-py3.10/bin/python
		Valid:          True

		System
		Platform:   linux
		OS:         posix
		Python:     3.10.6
		Path:       /usr
		Executable: /usr/bin/python3.10

3. Copy `file-path` output from `Executable`
4. In VSCode press `Ctrl + Shift + P`
    - Type `Python env` in the search box 
    - Select `Python: Create Environment`
	- Select `venv`
    - Click on `+ Enter Interpreter path`
    - Enter file-path output from step #3 to python executable and press enter
5. In VSCode top menu:
    - Click on `Run` -> `Add Configuration` -> `Python file` - (it should open launch.json file-name)
6. Paste into the file:
```
{
    // Use IntelliSense to learn about possible attributes.
    // Hover to view descriptions of existing attributes.
    // For more information, visit: https://go.microsoft.com/fwlink/?linkid=830387
    "version": "0.2.0",
    "configurations": [
        
        
        {
            "name": "Python: Module",
            "type": "python",
            "request": "launch",
            "module": "starfyre",
            "justMyCode": true,
            "args": ["--path",
            "test-application/",
            "--build"
            ],
            "stopOnEntry": false,
            "console": "integratedTerminal",
        }
    ]
}
```
7. In VSCode menu test with:
    - Click on `Run` -> `Run Without Debugging` "or press `Ctrl + F5`" - to check that the output has no errors

8. To debugg it, In VSCode menu:
    - Add break point on the lines you want to debbug
    - Click on `Run` -> `Start Debugging` "or press `F5`"
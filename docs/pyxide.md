# Pyxide Language Specification

Pyxide blends Python with a JSX-like syntax, offering seamless integration of both scripting and markup.

## Table of Contents
- Structure
- Python Functionality
- Styling
- Pyxide Markup
- JavaScript Integration
- Importing CSS and JS Libraries
- Structure

A Pyxide file contains:

1.Python imports, functions, and library integrations.
2. Styling via the <style> block or CSS imports.
3. Pyxide markup inside the <pyxide> block.
4. (Optional) JavaScript in the <script> block or JS library imports.

### Python Functionality

Declare Python functions and import modules as in regular Python.

```

from .parent import parent
from .store import store

def mocked_request():
  return "fetched on the server"

async def handle_on_click(e):
  # async code here

```

### Styling

Define styles with the <style> block, or import them from external files.

```
<style>
  body {
    background-color: red;
  }
</style>

```

### CSS Imports:
```
import 'path/to/style.css'
```

### Components:

```
<store>
  <parent hello='world'>
    ...
  </parent>
</store>
```
### Event Handling and Looping

```
<span onclick={handle_on_click}>
    {[ mocked_request() for i in range(4)]}
</span>
```

JavaScript Integration
Include custom JS in the <script> section.

```
<script>
// custom JS here
</script>
```

### Importing CSS and JS Libraries

Pyxide supports the importing of external CSS stylesheets and JS libraries directly from the Python code.

More documentation coming soon.



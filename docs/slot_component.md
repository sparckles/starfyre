# <SLOT> Component Implementation

### Introduction
This document provides an overview of component re-usage thought special tag `<slot>`.  

### Feature Description
This feature allows Starfyre developers to redefine parts of a Component for their application using a special tag `<slot>`. It provides a better design and flexibility to the app.

## Implementation Details

### Component Definition
Every Component in Starfyre is defined in a separate `.fyre file`. It allows developers to specify the position on the pyml source code to insert a custom content when using a defined component in another `.fyre template` (as part of a different page/component.)
To mark such placeholder, `<slot></slot> tag` should be inserted into the component definition.
Example of a component definition:

```python
user_component.fyre

<pyml>
  <div>
    <slot></slot>
    Hello    
    <p>World</p>
  </div>
</pyml>
```

### Component Usage
When there are a `<user_component>` inside another `.fyre template`, everything between open and close tags `<user_component></user_component>` are considered it’s “children content”, for example:

```python
__init__.fyre

from .user_component import user_component

<pyml>
  <user_component>
      <div>I will replace slot</div>
      I will replace slot too
  </user_component>
<pyml>
```
When the result HTML for the Application is rendered, this “children content” will be inserted instead of the `<slot></slot> tag` in the same position as it was defined.

Here is a HTML file result:

```python
index.html

<script src='store.js'></script><style>

</style><div id='root'>
<div id='74ac46f6-0816-43e1-91c8-5496293a8e72'  >
<div id='5194ec83-cb78-4162-874d-35a039f59a01'  >
<div id='b0c0e539-1d0f-41ad-84b1-445d9d9aa7b3'  >
I will replace slot
</div>
</div>

<div id='d16eb6a2-0df3-4278-a9cb-39c2c253ffe0'  >
I will replace slot too
</div>

<div id='60b7c7cb-32ad-4898-9dd0-9b7e3694034f'  >
Hello
</div>

<p id='0f4ab321-ef7c-4290-8765-50e8016c6333'  >
<div id='8c145b6c-25c7-439d-83d0-c907e0bb4c20'  >
World
</div>
</p>
</div>
</div><script>

```

In case of there are no `<slot></slot> tag` specified on the component definition, the “child content” will be appended to the end of the Component's definition, (it will be the last content before closing the root tag) and a warning message will be printed to the program’s output.

See example:

```python
user_component.fyre "there are no <slot> especified here"

<pyml>
  <div>
    Hello    
    <p>World</p>
  </div>
</pyml>
```
This is the output with custom component content being added to the end on the html file.

```python

<script src='store.js'></script><style>

</style><div id='root'>
<div id='91e9507b-0892-419a-9fee-d603c9ed743f'  >
<div id='af88c8fc-4fe9-433a-8ef6-460bc08240f2'  >
Hello
</div>

<p id='fcebb4f2-f5dd-4066-b4f2-6631fee46c93'  >
<div id='996b939b-1e37-4832-918d-54f8556f9255'  >
World
</div>
</p>

<div id='0d606409-e5ce-406b-adb4-a76ad4505e56'  >
<div id='b66def9a-861f-422c-a633-b5545dd987a4'  >
I will replace slot
</div>
</div>

<div id='eab718c7-d1bf-4756-9274-d7a78148065f'  >
I will replace slot too
</div>
</div>
</div><script>

```

If a Component has no child content, no warning message is generated.

### Known Limitations
`<slot></slot> tag` should be a direct child of root element in the Component’s definition.

### Conclusion
This feature allows the developer to re-use custom Starfyre Components, providing runtime flexibility. More features, such as flexible positioning, default values will be added in next releases.

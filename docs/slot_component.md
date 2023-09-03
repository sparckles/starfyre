# <SLOT> Component Implementation

### Introduction
This document provides an overview of component re-usage thought special `<slot>`.  

### Feature Description
This feature allows Starfyre developers to redefine parts of a Component for their application using a special tag `<slot>`. It provides a better design and flexibility to the app.

## Implementation Details

### Component Definition
Every Component in Starfyre is defined in a separate `.fyre file`. It allows developers to specify the position on the pyml source code to insert a custom content when using a defined component in another `.fyre template` (as part of a different page/component.)
To mark such placeholder, `<slot></slot> tag` should be inserted into the component definition.

### Component Usage
When there are a `<user_component>` inside another `.fyre template`, everything between open and closed tags is considered it’s “child content”, for example:

```python
<user_component>
    <div>HTML child content</div>
    Text child content
</user_component>
```
When the result HTML for the Application is rendered, this “child content” will be inserted instead of the `<slot></slot> tag` in the same position as it was defined.

Here is a HTML file result:

```python

<script src='store.js'></script><style>


</style><div id='root'>
<div id='3cbf3ee9-52ae-448d-9b71-735797434cff'  >
<div id='f0a8cc67-4530-476e-bb2c-30126b54c4d7'  >
Before the slot
</div>

<div id='ea417e22-c456-420c-8ddc-9dc47ac033c9'  >
<div id='2d392f01-ac23-4067-9cb3-53bc82c70d9e'  >
HTML child content
</div>
</div>

<div id='c405ad08-1a97-4b79-935c-fa0fdeae950c'  >
Text child content
</div>

<p id='a3209a50-3157-4605-ae15-b218a52db41c'  >
<div id='65041c6d-6106-4b6e-aecd-9d306397ba6e'  >
After the slot
</div>
</p>
</div>
</div><script>

```

In case of there are no `<slot></slot> tag` defined, the “child content” will be appended to the end of the Component's definition, (it will be the last thing before closing the root tag) and a warning message will be printed to the program’s output.

See example:

```python

<script src='store.js'></script><style>


</style><div id='root'>
<div id='92616af9-06ac-4337-afb5-c12bacb24b59'  >
<div id='a9477267-5c16-4ee4-be5b-ae7babc32926'  >
Hello
</div>

<p id='c8950fce-dc49-4606-907d-7f413b9bf939'  >
<div id='f1d2236e-74c2-4677-9096-a95989ee6b03'  >
World
</div>
</p>

<div id='bb79b3ea-e31a-4352-8ed9-e6591b385d28'  >
<div id='4e2aa740-acd8-4954-a73b-07e92a289cbf'  >
HTML child content
</div>
</div>

<div id='f03ce8dc-5358-4c9a-a6ce-bc3b4ed8ca40'  >
Text child content
</div>
</div>
</div><script>

```

If a Component has no child content, no warning message is generated.

"put an exemplo here"

Usage Examples
```python
<pyml>
    <span>  
       <h1> THIS IS MY FIRST HTML NODE </h1>
        {ssr_request()}
       <slot></slot>
        <p> THIS IS MY SECOND HTML NODE </p>        
        <div>
        This won't be re-rendered
      </div>      
    </span>
</pyml>
```


Known Limitations
`<slot></slot> tag` should be a direct child of root element in the Component’s definition.

Conclusion
This feature allows a developer to re-use custom Starfyre Components, providing runtime flexibility. More features, such as flexible positioning, default values will be added in next releases.

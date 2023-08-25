# Introduction

This document reflect the accomplished tasks during the MLH 12 weeks Summer Fellowship.
These issues were closed by [Suelen Karbivnychhy](https://github.com/SuelenKarbivnychyy)

## Issue

Issue number: [#44](https://github.com/sparckles/starfyre/issues/44) Add a way to import css files instead of having single file css.

## Problem Description

No way to specify external css files to be used in Starfyre components. Only inline css is supported. 

## Solution

To address this issue the following steps were taken:

- Alter logic of parsing lines in `compiler.py parse method`. If line in file matches regular expression of css import statement - add that line to `resolve_css_import method`. 
- The `resolve_css_import method` reads the file and append the css content to respective list `(local css_lines variable inside parse method)`.

Details of the solution can be found in [PR#56](https://github.com/sparckles/starfyre/pull/56) 

## Testing

- See `css_file_test.css` and the css import statement in `parent.fyre file` under `test-application project folder`
- To run generation locally, use the command `./build.sh` from project folder.

test-application/parent.py

```python
import requests
import "./css_file_test.css"


def ssr_request():
  text = "Hello"
  if text != "":
    return text + " from Server Side"
  else:
    return "No response"

<pyml>
    <span>    
      <div>
        <h1> Hello World </h1>
      <div>    
    </span>
</pyml>

```
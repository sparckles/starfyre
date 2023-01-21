use pyo3::{
    prelude::*,
    types::{PyDict, PyList},
};
use std::collections::HashMap;

/// Formats the sum of two numbers as string.
#[pyfunction]
fn sum_as_string(a: usize, b: usize) -> PyResult<String> {
    Ok((a + b).to_string())
}

#[pyclass]
pub struct DomNode {
    tag: String,
    props: Py<PyDict>,
    children: Py<PyList>,
    state: Py<PyDict>,
    event_listeners: Py<PyDict>,
    original_data: String,
    data: String,
    parent_element: Option<Py<PyAny>>,
    dom_pointer: Option<Py<PyAny>>,
}

#[pymethods]
impl DomNode {
    #[new]
    pub fn new(
        tag: String,
        props: Py<PyDict>,
        children: Py<PyList>,
        event_listeners: Py<PyDict>,
        state: Py<PyDict>,
    ) -> DomNode {
        DomNode {
            tag,
            props,
            children,
            event_listeners,
            state,
            original_data: "".to_string(),
            data: "".to_string(),
            parent_element: None,
            dom_pointer: None,
        }
    }

    pub fn is_text_node(&self) -> bool {
        self.tag == "TEXT_NODE"
    }

    pub fn set_parent_element(&mut self, parent_element: Py<PyAny>) {
        self.parent_element = Some(parent_element);
    }
}

pub struct DomTree {
    pub root: DomNode,
}

/// A Python module implemented in Rust.
#[pymodule]
fn starfyre(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(sum_as_string, m)?)?;
    m.add_class::<DomNode>()?;
    Ok(())
}

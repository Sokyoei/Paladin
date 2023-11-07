use pyo3::prelude::*;

#[pyfunction]
fn hello() {
    println!("hello")
}

#[pymodule]
#[pyo3(name = "ahri_rust")]
fn ahri_rust(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(hello, m)?)?;
    Ok(())
}

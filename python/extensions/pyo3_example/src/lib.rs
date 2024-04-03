use pyo3::prelude::*;

#[pyfunction]
fn hello() {
    println!("hello")
}

#[pymodule]
#[pyo3(name = "pyo3_example")]
fn pyo3_example(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(hello, m)?)?;
    Ok(())
}

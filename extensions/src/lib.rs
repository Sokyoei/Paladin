use pyo3::prelude::*;

#[pymodule]
mod _rust {
    use pyo3::prelude::*;

    #[pyfunction]
    fn hello_rust() -> PyResult<()> {
        println!("Hello Rust!");
        Ok(())
    }

    #[pyfunction]
    fn sum_as_string(a: usize, b: usize) -> PyResult<String> {
        Ok((a + b).to_string())
    }
}

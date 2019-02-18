
mod main;

use pyo3::prelude::*;
use pyo3::wrap_pyfunction;


#[pyfunction]
fn cosine(original_phrases: Vec<String>, compared_phrases: Vec<String>, thread_count: usize) -> PyResult<f32> {

	Ok(main::run(original_phrases, compared_phrases, thread_count))

}

#[pymodule]
fn similarity_rs(_py: Python, m: &PyModule) -> PyResult<()> {
	m.add_wrapped(wrap_pyfunction!(cosine))?;

	Ok(())
}

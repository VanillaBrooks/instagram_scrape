
mod main;

#[no_mangle]
pub unsafe extern "C" fn similarity(
	original_phrases: Vec<String>,
	compared_phrases: Vec<String>,
	thread_count: usize) -> f32 {

	main::run(original_phrases, compared_phrases, thread_count)

}

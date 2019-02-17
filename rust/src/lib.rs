
mod main;


#[no_mangle]
pub unsafe extern "C" fn cos_similarity(
	original_phrases: Vec<String>,
	compared_phrases: Vec<String>,
	thread_count: usize) -> f32 { // funct start

	main::run(original_phrases, compared_phrases, thread_count)

}

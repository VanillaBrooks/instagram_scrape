use hashbrown::HashMap;
use parking_lot::RwLock;
use std::sync::Arc;
use rayon;
use std::sync::mpsc;


fn cosine_sim(orginal_user_vec: Vec<Vec<u32>>, second_user_vec: Vec<Vec<u32>>) -> f32 {
	let user_2_magnitudes: Vec<f32> = second_user_vec.iter().map(|v| magnitude(v)).collect::<Vec<_>>();
	let user_1_magnitudes: Vec<f32> = orginal_user_vec.iter().map(|v| magnitude(v)).collect::<Vec<_>>();
	let length = orginal_user_vec.len().pow(2);
	let len_orig = orginal_user_vec.len() as f32;

	let mut total : f32 = 0.0;

	for i in 0..orginal_user_vec.len(){
		let curr_vec = &orginal_user_vec[i];
		let curr_mag = &user_1_magnitudes[i];

		for j in 0..second_user_vec.len(){
			let k = dot_product(&curr_vec, &second_user_vec[j])  / (curr_mag * user_2_magnitudes[j]);//.acos() * 180.0 / std::f32::consts::PI;
			println!{"currnet is {}", k}
			total += k;
		}
	}
	println!{"total is {} length is {}", total, length}
	//total = total / length as f32;
	total = total / len_orig;

	return total
}

fn magnitude(vector: &Vec<u32>) -> f32 {

	let mag : u32 = vector.iter()
					.map(|x| x.pow(2)).sum();
	let mag = (mag as f32).sqrt();

	return mag
}

fn dot_product(vec_1: &Vec<u32>, vec_2: &Vec<u32>) -> f32{
	let mut run_sum = 0;

	for i in 0..vec_1.len(){
		run_sum+= vec_1[i] * vec_2[i];
	}
	return run_sum as f32
}

fn _hashmap_count(vector_to_compare: Vec<String>, indexer_lock: Arc<RwLock<HashMap<String, usize>>>) -> () {

	println!{"after indexer read and counts"}

	let mut write = false;

	for sentence in vector_to_compare {
		for word in sentence.split(" "){
			println!{"word is {}", word}
			{
				let indexer =  indexer_lock.read();
				println!{"got indexer lock"}
				match indexer.get(word){
					Some(_) => continue, // we are not counting matches like this
					None => write = true
				}
				println!{"after match"}
			}

			if write{
				println!{"in write"}
				write = false;
				println!{"ready to acquire the write lock"}
				let mut indexer_write = indexer_lock.write();
				println!{"got indexer_write lock"}
				match indexer_write.get(word){
					Some(_) => continue, // it was already  inserted into the hashmap
					None => {
						let length = indexer_write.len().clone();
						indexer_write.insert(word.to_string(), length);
						println!{"added to hashmap"}
					}
				}
			}
		}
	}
	return ()
}

fn _vector_count(sentence: &String, hashmap_mutex: &Arc<RwLock<HashMap<String, usize>>>, trans: mpsc::Sender<Vec<usize>>) {
	let hashmap = hashmap_mutex.read();
	let mut counts : Vec<usize> = vec![0; hashmap.len()];

	for word in sentence.split(" "){
		counts[hashmap.get(word).unwrap().clone() as usize] += 1
	}

	trans.send(counts).unwrap()

}

fn thread_hashmap_counter(passed_vector: &Vec<String>, hashmap_mutex: &Arc<RwLock<HashMap<String, usize>>>, thread_count:usize){
	let num_chunks = passed_vector.len() / thread_count + 1;
	println!{"vector size is {} thread count is {}", passed_vector.len(), thread_count}

	rayon::scope( |t| {
		println!{"inside scope"}
		for chunk_to_compare in passed_vector.chunks(num_chunks){
			println!{"chunk is {:?}", chunk_to_compare}
			let index_clone = Arc::clone(hashmap_mutex);

			t.spawn( move |_| {
				_hashmap_count(chunk_to_compare.to_vec(), index_clone);
			});

		}

	});

}

fn thread_vector_count(vector: &Vec<String>, hashmap_mutex:&Arc<RwLock<HashMap<String, usize>>>){
	let (tx, rx) = mpsc::channel();
	rayon::scope(|t| {
		for sentence in vector{

			let hashmap_clone = Arc::clone(hashmap_mutex);
			let tx_copy = mpsc::Sender::clone(&tx);

			t.spawn( move |_|{
				_vector_count(sentence, &hashmap_clone, tx_copy);
			});
		}

	});



}

fn threading (original_phrases: Vec<String>,  phrases_to_compare: Vec<String>, thread_count: usize)-> () {
	let map : HashMap<String, usize>= HashMap::new();
	let hashmap_index = Arc::new(RwLock::new(map));

	thread_hashmap_counter(&original_phrases, &hashmap_index, thread_count);
	thread_hashmap_counter(&phrases_to_compare, &hashmap_index, thread_count);

	let orig = thread_vector_count(&original_phrases, &hashmap_index);
	let cmp  = thread_vector_count(&phrases_to_compare, &hashmap_index);


}

fn main() {
	let phrases_1 : Vec<String> = vec!["sample".to_string(), "phrase".to_string()];
	let phrases_2 : Vec<String> = vec!["sample".to_string(), "here".to_string(), "asdads".to_string(), "asdasfhg".to_string(),"sample".to_string(), "here".to_string(), "asdads".to_string(), "asdasfhg".to_string(),"sample".to_string(), "here".to_string(), "asdads".to_string(), "asdasfhg".to_string(),"sample".to_string(), "here".to_string(), "asdads".to_string(), "asdasfhg".to_string(),"sample".to_string(), "here".to_string(), "asdads".to_string(), "asdasfhg".to_string(),"sample".to_string(), "here".to_string(), "asdads".to_string(), "asdasfhg".to_string(),"sample".to_string(), "here".to_string(), "asdads".to_string(), "asdasfhg".to_string() ];

	threading(phrases_1, phrases_2, 5);
}

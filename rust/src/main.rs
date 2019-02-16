use hashbrown::HashMap;
use parking_lot::RwLock;
use std::sync::Arc;
use rayon;
use std::sync::mpsc;


fn cosine_sim(orginal_user_vec: Vec<Vec<usize>>, second_user_vec: Vec<Vec<usize>>) -> f32 {
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
			//println!{"currnet is {}", k}
			total += k;
		}
	}
	//println!{"total is {} length is {}", total, length}
	//total = total / length as f32;
	total = total / len_orig;

	return total
}

fn magnitude(vector: &Vec<usize>) -> f32 {

	let mag : usize = vector.iter()
					.map(|x| x.pow(2)).sum();
	let mag = (mag as f32).sqrt();

	return mag
}

fn dot_product(vec_1: &Vec<usize>, vec_2: &Vec<usize>) -> f32{
	let mut run_sum = 0;

	for i in 0..vec_1.len(){
		run_sum+= vec_1[i] * vec_2[i];
	}
	return run_sum as f32
}

fn _hashmap_count(vector_to_compare: Vec<String>, indexer_lock: Arc<RwLock<HashMap<String, usize>>>) -> () {

	let mut write;

	for sentence in vector_to_compare {
		for word in sentence.split(" "){
			{
				let indexer =  indexer_lock.read();
				match indexer.get(word){
					Some(_) => continue, // we are not counting matches like this
					None => write = true
				}
			}

			if write == true{
				write = false;
				let mut indexer_write = indexer_lock.write();
				match indexer_write.get(word){
					Some(_) => continue, // it was already  inserted into the hashmap
					None => {
						let length = indexer_write.len().clone();
						indexer_write.insert(word.to_string(), length);
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

fn thread_hashmap_counter(passed_vector: &Vec<String>, hashmap_mutex: &Arc<RwLock<HashMap<String, usize>>>, thread_count:usize) {
	let num_chunks = passed_vector.len() / thread_count + 1;

	rayon::scope( |t| {
		for chunk_to_compare in passed_vector.chunks(num_chunks){
			let index_clone = Arc::clone(hashmap_mutex);

			t.spawn( move |_| {
				_hashmap_count(chunk_to_compare.to_vec(), index_clone);
			});

		}

	});
}

fn thread_vector_count(vector: &Vec<String>, hashmap_mutex:&Arc<RwLock<HashMap<String, usize>>>) ->Vec<Vec<usize>>{
	let (tx, rx) = mpsc::channel();

	rayon::scope( move |t| {
		for sentence in vector{

			let hashmap_clone = Arc::clone(hashmap_mutex);
			let tx_copy = mpsc::Sender::clone(&tx);

			t.spawn( move |_| {
				_vector_count(sentence, &hashmap_clone, tx_copy);
			});
		}

	});

	//
	// TODO : change this to .iter().collect()
	//
	let mut results : Vec<Vec<usize>> = vec![];
	for value in rx{
		results.push(value);
	}

	return results;
}

pub fn threading (original_phrases: Vec<String>,  phrases_to_compare: Vec<String>, thread_count: usize)-> (Vec<Vec<usize>>, Vec<Vec<usize>>) {
	let map : HashMap<String, usize>= HashMap::new();
	let hashmap_index = Arc::new(RwLock::new(map));

	thread_hashmap_counter(&original_phrases, &hashmap_index, thread_count);
	thread_hashmap_counter(&phrases_to_compare, &hashmap_index, thread_count);

	let orig = thread_vector_count(&original_phrases, &hashmap_index);
	let cmp  = thread_vector_count(&phrases_to_compare, &hashmap_index);

	return (orig, cmp)
}

fn run(phrases_1: Vec<String>, phrases_2: Vec<String>, thread_count: u32)->f32 {
	let (vec_1, vec_2) = threading(phrases_1, phrases_2, thread_count);
	let sim = cosine_sim(vec_1, vec_2);
	return sim
}

fn main(){
	// add tests here


}

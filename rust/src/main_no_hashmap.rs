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


fn cmp(original: &String, indexer: &mut Vec<String>) -> Vec<u32> {
	let mut counts  : Vec<u32> = vec![0; indexer.len()];

	for word in original.split(" "){
		match indexer.iter().position(|y| *y == word){
			Some(x) => counts[x] += 1,
			None => {
				counts.push(1);
				indexer.push(word.to_string());
			},
		}
	}

	return counts

}

fn count_occurances(original: Vec<String>, compare: Vec<String>) -> (Vec<Vec<u32>>, Vec<Vec<u32>>) {
	let mut indexer    : Vec<String> = Vec::new();

	let mut orig_count : Vec<Vec<u32>> = Vec::new();
	for phrase in original{
		orig_count.push(cmp(&phrase, &mut indexer));
	}

	let mut comp_count : Vec<Vec<u32>> = Vec::new();
	for phrase in compare{
		comp_count.push(cmp(&phrase, &mut indexer));
	}

	for row in &mut orig_count{
		row.append(&mut vec![0; indexer.len() - row.len()]);

	}

	for  row in &mut comp_count{
		row.append(&mut vec![0; indexer.len() - row.len()]);
	}

	(orig_count, comp_count)

}

fn main() {
	let phrases_1 : Vec<String> = vec!["sample".to_string(), "phrase".to_string()];
	let phrases_2 : Vec<String> = vec!["sample".to_string(), "here".to_string()];
	println!{"{:?}", phrases_1}

	let (v1, v2) = count_occurances(phrases_1, phrases_2);
	println!{"v1 {:?} v2 {:?}", v1, v2}
	let similarities = cosine_sim(v1, v2);
	println!{"{:?}", similarities }

}

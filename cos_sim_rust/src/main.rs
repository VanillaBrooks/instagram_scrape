use hashbrown::HashMap;
use parking_lot::RwLock;
use std::sync::Arc;
use std::thread;
use rayon;


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


fn cmp(original: &String, indexer_lock: &Arc<RwLock<HashMap<String, usize>>>) -> Vec<u32> {
    let mut indexer = indexer_lock.read();
    // initialize a vector full of zeroes up until the current length of the hashmap
    

    let size;
    {
        let indexer = indexer_lock.read();
        size = indexer.len().clone();
    }

    let mut counts  : Vec<u32> = vec![0; size];
    let mut need_reader_flag = true;


    println!{"after indexer read and counts"}

    let mut write = false;
    for word in original.split(" "){
        println!{"word is {}", word}
        {
            let indexer=  indexer_lock.read();
            println!{"got indexer lock"}
            match indexer.get(word){
                Some(x) =>counts[*x] +=1,
                None => write = true
            }
            println!{"after match"}
        }

        if write{
            println!{"in write"}
            write = false;
            let mut indexer_write = indexer_lock.write();
            println!{"got indexer_write lock"}
            let length = indexer_write.len().clone();
            indexer_write.insert(word.to_string(), length);
        }
        

    }

    return counts

}

fn count_occurances<'a>(original_lock: Arc<RwLock<Vec<String>>>, compare: Vec<String>,  indexer_lock: Arc<RwLock<HashMap<String, usize>>>) -> (Vec<Vec<u32>>, Vec<Vec<u32>>) {
    let original = original_lock.read();
    println!{"starting a count_occurances function"}
    

    let mut orig_count : Vec<Vec<u32>> = Vec::new();

    for phrase in original.iter(){
        orig_count.push(cmp(&phrase, &indexer_lock));
    }
    println!{"finished original.iter()"}

    let mut comp_count : Vec<Vec<u32>> = Vec::new();
    for phrase in compare{
        comp_count.push(cmp(&phrase, &indexer_lock));
    }

//    for row in &mut orig_count{
 //       row.append(&mut vec![0; indexer.len() - row.len()]);
//
//    }
//
//    for  row in &mut comp_count{
//        row.append(&mut vec![0; indexer.len() - row.len()]);
//~    }

    (orig_count, comp_count)

}

fn threading (original_phrases: Vec<String>,  phrases_to_compare: Vec<String>, thread_count: usize)-> () {
    let map : HashMap<String, usize>= HashMap::new();
    let indexer = Arc::new(RwLock::new(map));
    let original_phrases_lock = Arc::new(RwLock::new(original_phrases));


    let num_chunks = phrases_to_compare.len() / thread_count;
    let num_chunks = 15;

    rayon::scope( |t| {
        for chunk_to_compare in phrases_to_compare.chunks(num_chunks){
            println!{"chunk is {:?}", chunk_to_compare}
            let index_clone = Arc::clone(&indexer);
            let original_phrases_clone =  Arc::clone(&original_phrases_lock);

            t.spawn( move |_| {
                count_occurances(original_phrases_clone, chunk_to_compare.to_vec(), index_clone);
            });

        }
    });

}

fn main() {
    let phrases_1 : Vec<String> = vec!["sample".to_string(), "phrase".to_string()];
    let phrases_2 : Vec<String> = vec!["sample".to_string(), "here".to_string(), "asdads".to_string(), "asdasfhg".to_string(),"sample".to_string(), "here".to_string(), "asdads".to_string(), "asdasfhg".to_string(),"sample".to_string(), "here".to_string(), "asdads".to_string(), "asdasfhg".to_string(),"sample".to_string(), "here".to_string(), "asdads".to_string(), "asdasfhg".to_string(),"sample".to_string(), "here".to_string(), "asdads".to_string(), "asdasfhg".to_string(),"sample".to_string(), "here".to_string(), "asdads".to_string(), "asdasfhg".to_string(),"sample".to_string(), "here".to_string(), "asdads".to_string(), "asdasfhg".to_string() ];

    threading(phrases_1, phrases_2, 5);
}

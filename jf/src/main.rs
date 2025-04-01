use std::{io::{self, Write}, collections::{HashMap, HashSet}};

// use alloc::collections;
use tinyjson::JsonValue;

// collection tree: dl.ndl.go.jp/api/collection/all
const CATS: &[&'static str] = &["A00003",
"A00004",
"A00005",
"A00006",
"A00007",
"A00008"];
// const CATS: &[&'static str] = &["A00001", "A00026", "A00027"];
// const CATS: &[&'static str] = &["A00016",
// "A00105",
// "A00117",
// "A00160",
// "A00116",
// "A00115",
// "A00106",
// "A00147",
// "A00174",
// "A00187",
// "A00020",
// "A00176",
// "A00075",
// "A00104",
// "A00146",
// "A00077",
// "A00161",
// "A00018",
// "A00081",
// "A00056",
// "A00057",
// "A00113",
// "A00058",
// "A00059",
// "A00060",
// "A00061",
// "A00062",
// "A00063",
// "A00064",
// "A00065",
// "A00066",
// "A00067",
// "A00068",
// "A00069",
// "A00070",
// "A00071",
// "A00072",
// "A00073",
// "A00074",
// "A00177",
// "A00178",
// "A00179",
// "A00076",
// "A00108",
// "A00175"];

fn main() {
    // let args: Vec<String> = std::env::args().collect();
    // if args.len() < 2 {
    //     panic!("Usage: {} TODO", args[0]);
    // }

    let mut stdout = io::stdout().lock();
    let mut stderr = io::stderr().lock();

    let symbol_internet = JsonValue::from(String::from("internet"));
    let symbol_collections: HashSet<_> = CATS.into_iter().map(|&s| String::from(s)).collect();
    
    let mut seen = HashSet::new();

    // read line from stdio
    for line in io::stdin().lines() {
        let line = line.expect("Ok");
        if !line.trim().is_empty() {
            if let Ok(v) = line.parse() {
                let v: tinyjson::JsonValue = v;
                if v.query().child("permission").child("rule").find() != Some(&symbol_internet) {
                    continue;
                }
                if let Some(collections) =  v.query().child("collections").get::<Vec<JsonValue>>(){
                    if !collections.into_iter().any(|c| symbol_collections.contains(c.get::<String>().unwrap())) {
                        continue;
                    }
                }
                let pid: usize = v.query().child("pid").get::<String>().unwrap().strip_prefix("info:ndljp/pid/").unwrap().parse().unwrap();
                if seen.contains(&pid) {
                    continue
                }
                writeln!(stdout, "{}", line).unwrap();
                seen.insert(pid);
            }
            else {
                writeln!(stderr, "{}", line).unwrap();
            }
        }
    }

    // let input = std::fs::File::open(&args[1]).unwrap();
    // let output1 = std::fs::File::create(&args[2]).unwrap();
    // let output2 = std::fs::File::create(&args[3]).unwrap();

    // // read lines from the zstd compressed file
    // for line in zstd::Decoder::new(input).lines() {
    //     if
    // }
    // zstd::stream::
    // zstd::stream::copy_decode(file, std::io::stdout()).unwrap();
}

// use std::io;

// // This function use the convenient `copy_encode` method
// fn compress(level: i32) {
//     zstd::stream::copy_encode(io::stdin(), io::stdout(), level).unwrap();
// }

// // This function does the same thing, directly using an `Encoder`:
// fn compress_manually(level: i32) {
//     let mut encoder = zstd::stream::Encoder::new(io::stdout(), level).unwrap();
//     io::copy(&mut io::stdin(), &mut encoder).unwrap();
//     encoder.finish().unwrap();
// }

// fn decompress() {
//     zstd::stream::copy_decode(io::stdin(), io::stdout()).unwrap();
// }

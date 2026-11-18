use std::env;
use std::error::Error;
use std::fs;
use std::num::ParseIntError;

fn main() -> Result<(), Box<dyn Error>> {
    let input_filename = env::args().nth(1).expect("at least one argument");
    let input = fs::read_to_string(&input_filename)?;
    println!("part1: {:?}", run_part_1(&input));
    println!("part2: {:?}", run_part_2(&input));
    Ok(())
}

fn run_part_1(input: &str) -> Result<String, ParseIntError> {
    let triangles = parse_input(input)?;
    Ok(triangles
        .iter()
        .fold(0 as usize, |acc, sides| {
            acc + (is_valid_triangle(sides) as usize)
        })
        .to_string())
}

fn run_part_2(input: &str) -> Result<String, ParseIntError> {
    let data = parse_input(input)?;
    let mut triangles = Vec::new();
    for c in 0..3 {
        for (r, _) in data.iter().enumerate().step_by(3) {
            triangles.push(vec![data[r + 0][c], data[r + 1][c], data[r + 2][c]]);
        }
    }
    Ok(triangles
        .iter()
        .fold(0 as usize, |acc, sides| {
            acc + (is_valid_triangle(sides) as usize)
        })
        .to_string())
}

fn is_valid_triangle(sides: &Vec<usize>) -> bool {
    if sides.is_empty() {
        return false;
    }
    let sum: usize = sides.iter().sum();
    for side in sides {
        let remaining = sum - *side;
        if remaining <= *side {
            return false;
        }
    }
    return true;
}

fn parse_input(input: &str) -> Result<Vec<Vec<usize>>, ParseIntError> {
    input
        .split_terminator('\n')
        .map(|line| {
            line.split_whitespace()
                .map(|value| value.parse::<usize>())
                .collect()
        })
        .collect()
}

#[cfg(test)]
mod tests {
    use super::*;
    use rstest::rstest;

    #[rstest]
    #[case("5 10 25\n", Ok("0".to_string()))]
    #[case("3 4 5\n", Ok("1".to_string()))]
    #[case("5 10 25\n3 4 5\n", Ok("1".to_string()))]
    #[case("5 10 25\n3 4 5\n3 4 5\n3 4 5\n3 4 5\n3 4 5\n3 4 5\n", Ok("6".to_string()))]
    #[case("\n", Ok("0".to_string()))]
    #[case("1 1 1\n", Ok("1".to_string()))]
    #[case("1 2 1\n", Ok("0".to_string()))]
    fn part_1_examples(#[case] input: &str, #[case] expected: Result<String, ParseIntError>) {
        assert_eq!(run_part_1(input), expected)
    }

    #[rstest]
    #[case("1 1 5\n1 2 10\n1 1 25\n", Ok("1".to_string()))]
    fn part_2_examples(#[case] input: &str, #[case] expected: Result<String, ParseIntError>) {
        assert_eq!(run_part_2(input), expected)
    }
}

use std::fs;
use std::env;
use std::collections::HashSet;
use std::error::Error;
use std::ops::Add;
use std::ops::AddAssign;
use std::str::FromStr;

fn main() -> Result<(), Box<dyn Error>> {
    let input_filepath = env::args().nth(1)
        .expect("ERROR: input filepath arg should be given");
    let input: String = fs::read_to_string(&input_filepath)?;
    println!("part1: {}", run_part1(&input)?);
    println!("part2: {}", run_part2(&input)?);
    Ok(())
}

type Location = (i32, i32);

fn manhattan(location: Location) -> u32 {
    (location.0.abs() + location.1.abs()).try_into().expect("valid integers")
}

#[derive(Clone, Copy)]
enum Turn {
    L,
    R,
}

struct Instruction {
    t: Turn,
    d: u32,
}

impl FromStr for Instruction {
    type Err = &'static str;

    fn from_str(text: &str) -> Result<Self, Self::Err> {
        let distance: u32 = text[1..].parse().unwrap();
        if let Some(c) = text.chars().nth(0) {
            match c {
                'L' => Ok(Instruction{t: Turn::L, d: distance}),
                'R' => Ok(Instruction{t: Turn::R, d: distance}),
                _ => Err("turn must be L or R"),
            }
        } else {
            Err("instruction cannot be empty")
        }
    }
}

#[derive(Clone, Copy)]
enum Compass {
    N,
    S,
    E,
    W,
}

impl Add<Compass> for Location {
    type Output = Location;

    fn add(self, direction: Compass) -> Self::Output {
        match direction {
            Compass::N => (self.0, self.1 + 1),
            Compass::S => (self.0, self.1 - 1),
            Compass::W => (self.0 - 1, self.1),
            Compass::E => (self.0 + 1, self.1),
        }
    }
}

impl Add<Turn> for Compass {
    type Output = Compass;

    fn add(self, turn: Turn) -> Self::Output {
        match (self, turn) {
            (Compass::W, Turn::R) | (Compass::E, Turn::L) => Compass::N,
            (Compass::W, Turn::L) | (Compass::E, Turn::R) => Compass::S,
            (Compass::N, Turn::R) | (Compass::S, Turn::L) => Compass::E,
            (Compass::N, Turn::L) | (Compass::S, Turn::R) => Compass::W,
        }
    }
}

impl AddAssign<Compass> for Location {
    fn add_assign(&mut self, direction: Compass) {
        *self = *self + direction;
    }
}

impl AddAssign<Turn> for Compass {
    fn add_assign(&mut self, turn: Turn) {
        *self = *self + turn;
    }
}

struct CityVec {
    loc: Location,
    f: Compass,
    v: HashSet<Location>
}

impl CityVec {
    fn new() -> Self {
        Self::new_at((0, 0))
    }

    fn new_at(location: Location) -> Self {
        let mut visited: HashSet<Location> = HashSet::new();
        visited.insert(location);
        return Self{loc: location, f: Compass::N, v: visited}
    }

    fn then(&mut self, instr: &Instruction) -> Option<Location> {
        let mut revisited_location = None;
        let d: i32 = instr.d.try_into().expect("parsing integers works");
        self.f += instr.t;
        for _ in 0..d {
            self.loc += self.f;
            if self.v.contains(&self.loc) {
                match revisited_location {
                    Some(_) => (),
                    None => { revisited_location = Some(self.loc); },
                }
            } else {
                self.v.insert(self.loc);
            }
        }
        revisited_location
    }

    fn manhattan(&self) -> u32 {
        manhattan(self.loc)
    }
}


fn run_part1(input: &str) -> Result<String, String> {
    let instructions = input.split_whitespace()
        .map(|word| word.trim_matches(&[',']).parse::<Instruction>())
        .collect::<Result<Vec<Instruction>, _>>()?;

    let mut location = CityVec::new();
    for instruction in instructions {
        let _ = location.then(&instruction);
    }
    Ok(location.manhattan().to_string())
}

fn run_part2(input: &str) -> Result<String, String> {
    let instructions = input.split_whitespace()
        .map(|word| word.trim_matches(&[',']).parse::<Instruction>())
        .collect::<Result<Vec<Instruction>, _>>()?;

    let mut location = CityVec::new();
    for instruction in instructions {
        match location.then(&instruction) {
            Some(location) => {
                return Ok(manhattan(location).to_string())
            },
            None => (),
        }
    }
    Ok(location.manhattan().to_string())
}


#[cfg(test)]
mod tests {
    use rstest::rstest;
    use super::*;

    #[rstest]
    #[case("R2, L3", Ok("5".to_string()))]
    #[case("R2, R2, R2", Ok("2".to_string()))]
    #[case("R5, L5, R5, R3", Ok("12".to_string()))]
    fn part1_examples(#[case] input: &str, #[case] expected: Result<String, String>) {
        assert_eq!(run_part1(input), expected);
    }

    #[rstest]
    #[case("R8, R4, R4, R8", Ok("4".to_string()))]
    fn part2_examples(#[case] input: &str, #[case] expected: Result<String, String>) {
        assert_eq!(run_part2(&input), expected);
    }
}

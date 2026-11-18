use std::cmp::min;
use std::convert::TryFrom;
use std::error::Error;
use std::{env, fs};

fn main() -> Result<(), Box<dyn Error>> {
    let filename = env::args().nth(1).expect("valid string");
    let input = fs::read_to_string(&filename)?;
    println!("part1: {}", run_part_1(&input)?);
    println!("part2: {}", run_part_2(&input)?);
    Ok(())
}

fn run_part_1(input: &str) -> Result<String, String> {
    let kp = Keypad::phone();
    run_any_part(input, kp)
}

fn run_part_2(input: &str) -> Result<String, String> {
    let kp = Keypad::fuckshit();
    run_any_part(input, kp)
}

fn run_any_part(input: &str, mut keypad: Keypad) -> Result<String, String> {
    let instructions: Vec<Vec<Movement>> = parse_instructions(&input);
    let digits: Vec<char> = instructions
        .iter()
        .map(|movements| {
            movements.iter().for_each(|movement| {
                keypad.adjust(*movement);
            });
            keypad
                .digit()
                .expect("keypad has some key at the current position")
        })
        .collect();
    Ok(String::from_iter(digits))
}

#[derive(Debug)]
struct Keypad {
    row: usize,
    col: usize,
    grid: Vec<Vec<Option<char>>>,
    size: usize,
}

impl Keypad {
    fn phone() -> Self {
        Self::new(vec![
            vec![Some('1'), Some('2'), Some('3')],
            vec![Some('4'), Some('5'), Some('6')],
            vec![Some('7'), Some('8'), Some('9')],
        ])
    }

    fn fuckshit() -> Self {
        let mut keypad = Self::new(vec![
            vec![None, None, Some('1'), None, None],
            vec![None, Some('2'), Some('3'), Some('4'), None],
            vec![Some('5'), Some('6'), Some('7'), Some('8'), Some('9')],
            vec![None, Some('A'), Some('B'), Some('C'), None],
            vec![None, None, Some('D'), None, None],
        ]);
        keypad.col = 0;
        keypad
    }

    fn new(grid: Vec<Vec<Option<char>>>) -> Self {
        let size = grid.len();
        let mid = (size - 1) / 2;
        Self {
            row: mid,
            col: mid,
            grid: grid,
            size: size,
        }
    }

    fn digit(&self) -> Option<char> {
        self.grid[self.row][self.col]
    }

    fn adjust(&mut self, movement: Movement) {
        let (orig_row, orig_col) = (self.row, self.col);
        let (dv, dh): (i32, i32) = match movement {
            Movement::Down => (1, 0),
            Movement::Up => (-1, 0),
            Movement::Left => (0, -1),
            Movement::Right => (0, 1),
        };
        self.row = self.clamp(self.row, dv);
        self.col = self.clamp(self.col, dh);
        if self.digit().is_none() {
            self.row = orig_row;
            self.col = orig_col;
        }
    }

    fn clamp(&self, value: usize, delta: i32) -> usize {
        if delta < 0 && value <= 0 {
            value
        } else {
            min(((value as i32) + delta) as usize, self.size - 1)
        }
    }
}

#[derive(Copy, Clone, Debug)]
enum Movement {
    Left,
    Right,
    Up,
    Down,
}

impl TryFrom<char> for Movement {
    type Error = String;

    fn try_from(c: char) -> Result<Self, Self::Error> {
        match c.to_ascii_uppercase() {
            'L' => Ok(Movement::Left),
            'R' => Ok(Movement::Right),
            'U' => Ok(Movement::Up),
            'D' => Ok(Movement::Down),
            _ => Err(format!(
                "{c} is not a valid movement. Must be L, R, U, or D"
            )),
        }
    }
}

fn parse_instructions(input: &str) -> Vec<Vec<Movement>> {
    input
        .split_terminator('\n')
        .map(|line| {
            line.chars()
                .map(|c| Movement::try_from(c).expect("valid input instruction data"))
                .collect()
        })
        .collect()
}

#[cfg(test)]
mod tests {
    use super::*;
    use rstest::rstest;

    #[rstest]
    #[case("ULL\nRRDDD\nLURDL\nUUUUD\n", Ok("1985".to_string()))]
    fn part_1_examples(#[case] input: &str, #[case] expected: Result<String, String>) {
        assert_eq!(run_part_1(input), expected)
    }

    #[rstest]
    #[case("ULL\nRRDDD\nLURDL\nUUUUD\n", Ok("5DB3".to_string()))]
    fn part_2_examples(#[case] input: &str, #[case] expected: Result<String, String>) {
        assert_eq!(run_part_2(input), expected)
    }
}

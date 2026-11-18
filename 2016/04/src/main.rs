use std::{collections::HashMap, env, error::Error, fmt, fs};
use regex::Regex;

fn main() -> Result<(), Box<dyn Error>> {
    let input_filename = env::args().nth(1).expect("valid first argument");
    let input = fs::read_to_string(input_filename)?;
    println!("part1: {}", run_part_1(&input)?);
    println!("part2: {}", run_part_2(&input)?);
    Ok(())
}

fn run_part_1(input: &str) -> Result<String, String> {
    let mut total = 0;
    for room in get_valid_rooms(&input) {
        total += room.sector_id;
    }
    Ok(total.to_string())
}

fn run_part_2(input: &str) -> Result<String, String> {
    for room in get_valid_rooms(&input) {
        let name: String = room.decode();
        if name.contains("north") {
            return Ok(format!("{:?}({})", room, room.decode()));
        }
    }
    return Err(String::from("North pole room not found!"));
}

fn parse_rooms(input: &str) -> Vec<Room> {
    let mut rooms = Vec::new();
    for line in input.split_terminator('\n') {
        rooms.push(Room::from(line).expect("valid room input"))
    }
    rooms
}

fn get_valid_rooms(input: &str) -> Vec<Room> {
    let mut rooms = Vec::new();
    for room in parse_rooms(&input) {
        if room.is_valid() {
            rooms.push(room);
        }
    }
    rooms
}

#[derive(Debug, Clone, PartialEq)]
struct RoomParseError {
    room_text: String,
}

impl RoomParseError {
    fn new(room_text: &str) -> Self {
        Self { room_text: room_text.to_string()}
    }
}

impl fmt::Display for RoomParseError {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(
            f,
            "Failed to parse {} as a room",
            self.room_text,
        )
    }
}

impl Error for RoomParseError {}

#[derive(PartialEq, Debug)]
struct Room {
    name: String,
    sector_id: u32,
    checksum: String,
}

impl Room {
    fn new(
        name: &str,
        sector_id: u32,
        checksum: &str,
    ) -> Self {
        Room { name: name.to_string(), sector_id: sector_id, checksum: checksum.to_string() }
    }

    fn from(text: &str) -> Result<Self, RoomParseError> {
        let regex = Regex::new(r"([a-z-]+)-(\d+)\[([a-z]{5})\]").or(
            Err(RoomParseError::new(&format!("oh no: {}", text)))
        )?;
        match regex.captures(text) {
            None => Err(RoomParseError::new(text)),
            Some(m) => {
                let name = m
                    .get(1)
                    .ok_or(RoomParseError::new(&format!("name: {}", format!("{:?}", m))))?
                    .as_str();
                let sector_id = m
                    .get(2)
                    .ok_or(RoomParseError::new(&format!("sector_id1: {}", format!("{:?}", m))))?
                    .as_str()
                    .parse()
                    .or(Err(RoomParseError::new(&format!("sector_id2: {}", format!("{:?}", m)))))?;
                let checksum = m
                    .get(3)
                    .ok_or(RoomParseError::new(&format!("checksum: {}", format!("{:?}", m))))?
                    .as_str();
                Ok(Room {
                    name: name.to_string(),
                    sector_id: sector_id,
                    checksum: checksum.to_string(),
                })
            }
        }
    }

    fn is_valid(&self) -> bool {
        self.checksum == self.calculate_checksum()
    }

    fn calculate_checksum(&self) -> String {
        let mut data = self.analyze();
        data.sort_by_key(|md| { (-(md.count as i32), md.letter) });

        let most_common = data[..5].to_vec();
        String::from_iter(most_common.iter().map(|md| md.letter))
    }

    fn analyze(&self) -> Vec<Metadata> {
        let mut data: HashMap<char, Metadata> = HashMap::new();
        let chars = self.name.chars().filter(|c| *c != '-');
        for (i, c) in chars.enumerate() {
            match data.get_mut(&c) {
                None => { data.insert(c, Metadata::new(c, i)); },
                Some(md) => md.incr(),
            }
        }
        Vec::from_iter(data.into_values())
    }

    fn decode(&self) -> String {
        let offset = 'a' as u8;
        let rot = (self.sector_id % 26) as u8;
        let mut result: String = String::new();
        for c in self.name.chars() {
            result.push(match c {
                '-' => ' ',
                _ => {
                    let orig = (c as u8) - offset;
                    let new = (orig + rot) % 26 + offset;
                    new as char
                }
            });
        }
        result
    }
}

#[derive(Clone)]
struct Metadata {
    letter: char,
    index: usize,
    count: u32,
}

impl Metadata {
    fn new(letter: char, index: usize) -> Self {
        Metadata { letter: letter, index: index, count: 1 }
    }

    fn incr(&mut self) {
        self.count += 1;
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use rstest::rstest;

    #[rstest]
    #[case("aaaaa-bbb-z-y-x-123[abxyz]", Ok(Room::new("aaaaa-bbb-z-y-x-", 123, "abxyz")))]
    #[case("a-b-c-d-e-f-g-h-987[abcde]", Ok(Room::new("a-b-c-d-e-f-g-h-", 987, "abcde")))]
    #[case("not-a-real-room-404[oarel]", Ok(Room::new("not-a-real-room-", 404, "oarel")))]
    #[case("totally-real-room-200[decoy]", Ok(Room::new("totally-real-room-", 200, "decoy")))]
    fn test_room_parsing(#[case] text: &str, #[case] expected: Result<Room, RoomParseError>) {
        assert_eq!(Room::from(text), expected)
    }

    #[rstest]
    #[case(Room::new("aaaaa-bbb-z-y-x-", 123, "abxyz"), true)]
    #[case(Room::new("a-b-c-d-e-f-g-h-", 987, "abcde"), true)]
    #[case(Room::new("not-a-real-room-", 404, "oarel"), true)]
    #[case(Room::new("totally-real-room-", 200, "decoy"), false)]
    fn test_is_room_valid(#[case] room: Room, #[case] expected: bool) {
        assert_eq!(room.is_valid(), expected)
    }

    #[rstest]
    #[
        case(
            "aaaaa-bbb-z-y-x-123[abxyz]\na-b-c-d-e-f-g-h-987[abcde]\nnot-a-real-room-404[oarel]\ntotally-real-room-200[decoy]\n",
            Ok("1514".to_string())
        )
    ]
    fn part_1_examples(#[case] input: &str, #[case] expected: Result<String, String>) {
        assert_eq!(run_part_1(input), expected)
    }
}
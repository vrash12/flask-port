use wasm_bindgen::prelude::*;

// Enum to define the ranks of the pieces
#[wasm_bindgen]
#[derive(Clone, Copy)]
pub enum Rank {
    FiveStarGeneral,
    FourStarGeneral,
    ThreeStarGeneral,
    TwoStarGeneral,
    OneStarGeneral,
    Colonel,
    LieutenantColonel,
    Major,
    Captain,
    FirstLieutenant,
    SecondLieutenant,
    Sergeant,
    Spy,
    Private,
    Flag,
}

// Struct to define each game piece
#[wasm_bindgen]
pub struct GamePiece {
    name: String,
    rank: Rank,
    position: usize,
}

#[wasm_bindgen]
impl GamePiece {
    // Constructor to create a new piece
    pub fn new(name: &str, rank: Rank, position: usize) -> GamePiece {
        GamePiece {
            name: name.to_string(),
            rank,
            position,
        }
    }

    // Method to get the name of the piece
    pub fn get_name(&self) -> String {
        self.name.clone()
    }

    // Method to get the rank of the piece
    pub fn get_rank(&self) -> Rank {
        self.rank
    }

    // Method to get the position of the piece
    pub fn get_position(&self) -> usize {
        self.position
    }

    // Move the piece to a new position
    pub fn move_to(&mut self, new_position: usize) {
        self.position = new_position;
    }

    // Method to determine if a move is valid (you can extend this with your own rules)
    pub fn is_move_valid(&self, new_position: usize) -> bool {
        // For now, we assume all moves are valid. You can add game-specific rules here
        true
    }

    // Method to determine the outcome of a battle between two pieces
    pub fn battle(&self, other: &GamePiece) -> String {
        match (self.rank, other.rank) {
            // Spy wins against generals
            (Rank::Spy, Rank::FiveStarGeneral | Rank::FourStarGeneral | Rank::ThreeStarGeneral | Rank::TwoStarGeneral | Rank::OneStarGeneral | Rank::Colonel | Rank::LieutenantColonel | Rank::Major | Rank::Captain | Rank::FirstLieutenant | Rank::SecondLieutenant) => "Spy Wins".to_string(),
            
            // Private wins against the Spy
            (Rank::Private, Rank::Spy) => "Private Wins".to_string(),
            
            // Attacker wins against the Flag
            (_, Rank::Flag) => "Attacker Wins".to_string(),
            
            // Flag loses to any other piece
            (Rank::Flag, _) => "Flag is Defeated".to_string(),
            
            // Rank comparison for other pieces
            _ if (self.rank as i32) > (other.rank as i32) => "Attacker Wins".to_string(),
            _ if (self.rank as i32) < (other.rank as i32) => "Defender Wins".to_string(),
            
            // Draw (both pieces are of the same rank)
            _ => "Draw".to_string(),
        }
    }
}

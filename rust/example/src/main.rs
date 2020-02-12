use std::error::Error;

fn main() -> Result<(), Box<dyn Error>> {
    rlbot::run_bot(MyBot { player_index: 0 })
}

struct MyBot {
    player_index: usize,
}

impl rlbot::Bot for MyBot {
    fn set_player_index(&mut self, index: usize) {
        self.player_index = index;
    }

    fn tick(&mut self, packet: &rlbot::GameTickPacket) -> rlbot::ControllerState {
        get_input(self.player_index, packet).unwrap_or_default()
    }
}

fn get_input(player_index: usize, packet: &rlbot::GameTickPacket,) -> Option<rlbot::ControllerState> {
    Some(rlbot::ControllerState {
        throttle: 1.0,
        ..Default::default()
    })
}
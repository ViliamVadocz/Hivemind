// use rlbot::ffi;

fn main() -> Result<(), Box<dyn std::error::Error>> {
    rlbot::run_bot(MyBot {
        index: 0
    })
}

struct MyBot {
    index: usize
}

impl rlbot::Bot for MyBot {
    fn set_player_index(&mut self, index: usize) {
        self.index = index;
    }

    fn tick(&mut self, packet: &rlbot::GameTickPacket) -> rlbot::ControllerState {
        let ctrl = rlbot::ControllerState::default();
        ctrl
    }
}
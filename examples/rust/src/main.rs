use std::error::Error;

fn main() -> Result<(), Box<dyn Error>> {
    rlbot::run_bot(
        MyBot {
            player_index: 0,
            last_time: 0.0,
            delta_time: 0.0,
            timer: 0.0
        }
    )
}

struct MyBot {
    player_index: usize,
    last_time: f32,
    delta_time: f32,
    timer: f32
}

impl rlbot::Bot for MyBot {
    fn set_player_index(&mut self, index: usize) {
        self.player_index = index;
    }

    fn tick(&mut self, packet: &rlbot::GameTickPacket) -> rlbot::ControllerState {
        let game_time = packet.game_info.seconds_elapsed;
        self.delta_time = game_time - self.last_time;
        self.last_time = game_time;
        self.timer += self.delta_time;

        if self.timer > 1.0 {
            println!("Running!");
            self.timer = 0.0;
        }

        rlbot::ControllerState {
            throttle: 1.0,
            steer: 1.0,
            ..Default::default()
        }
        // get_input(self.player_index, packet).unwrap_or_default()
    }
}

fn get_input(player_index: usize, packet: &rlbot::GameTickPacket,) -> Option<rlbot::ControllerState> {
    Some(rlbot::ControllerState {
        throttle: 1.0,
        ..Default::default()
    })
}
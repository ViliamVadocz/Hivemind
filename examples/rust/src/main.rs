use std::error::Error;

fn main() -> Result<(), Box<dyn Error>> {
    rlbot::run_hive(
        MyHivemind {
            drone_indices: vec![],
            last_time: 0.0,
            delta_time: 0.0,
            timer: 0.0
        }
    )
}

struct MyHivemind {
    drone_indices: Vec<usize>,
    last_time: f32,
    delta_time: f32,
    timer: f32
}

impl rlbot::Hivemind for MyHivemind {
    fn set_drone_indices(&mut self, indices: Vec<usize>) {
        self.drone_indices = indices;
    }

    fn tick(&mut self, packet: &rlbot::GameTickPacket) -> Vec<(usize, rlbot::ControllerState)> {
        let game_time = packet.game_info.seconds_elapsed;
        self.delta_time = game_time - self.last_time;
        self.last_time = game_time;
        self.timer += self.delta_time;

        if self.timer > 1.0 {
            println!("Running!");
            self.timer = 0.0;
        }

        let mut inputs: Vec<(usize, rlbot::ControllerState)> = vec![];
        for &index in self.drone_indices.iter() {
            inputs.push(
                (
                    index,
                    rlbot::ControllerState {
                        throttle: 1.0,
                        steer: 1.0,
                        ..Default::default()
                    }
                )
            );
        }
        
        inputs
    }
}
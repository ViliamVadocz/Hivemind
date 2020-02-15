use crate::{
    game::{GameTickPacket, ControllerState},
    framework::parse_framework_args,
    init_with_options
};
use std::error::Error;


pub trait Hivemind {
    fn set_drone_indices(&mut self, indices: Vec<usize>);
    fn tick(&mut self, packet: &GameTickPacket) -> Vec<ControllerState>;
}

pub fn run_hive<H: Hivemind>(mut hive: H) -> Result<(), Box<dyn Error>> {
    let args = parse_framework_args()
    .map_err(|_| Box::<dyn Error>::from("could not parse framework arguments"))?
    .ok_or_else(|| Box::<dyn Error>::from("not launched by framework"))?;

    let drone_indices = args.drone_indices;

    let rlbot = init_with_options(args.into())?;

    hive.set_drone_indices(drone_indices as Vec<usize>);

    let mut packets = rlbot.packeteer();
    loop {
        let packet = packets.next()?;
        let inputs = hive.tick(&packet);

        match inputs.len().cmp(drone_indices.len()) {
            Ordering::Equal => {
                for i in 0..drone_indices.len() {
                    drone = drone_indices[i];
                    input = inputs[i]
                    rlbot.update_player_input(drone, &input)
                }
            },
            Ordering::Less => return Box::<dyn Error>::from("too few inputs for drones"),
            Ordering::More => return Box::<dyn Error>::from("too many inputs for drones")
        }
    }
}

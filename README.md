# Hivemind

Hivemind bots for [RLBot](rlbot.org).

This repo is for experimentation and examples.
A proper pull request to the framework will be made once everything is working as intended.

Currently supported languages:

- Python
- Rust

***

## Python

To get started with your own hivemind in Python you will need these four things:

- a bot configuration file
- an appearance configuration file
- a dummy `DroneAgent`
- a `PythonHivemind` (subclass of `BotHelperProcess`)

### Bot Configuration File

The bot configuration file must have the file ending `.cfg` and look something like this (see `config.cfg` in the examples):

```toml
[Locations]
# Path to loadout config. Can use relative path from here.
looks_config = ./appearance.cfg

# Path to python file. Can use relative path from here.
python_file = ./hive.py

# Name of the bot in-game
name = Drone
```

`python_file` points to a file containing the dummy `DroneAgent`.

### Appearance configuration file

The appearance file is just a normal appearance file. See [the rlbot wiki](https://github.com/RLBot/RLBot/wiki/Bot-Customization) for more info.

### Dummy DroneAgent

RLBot needs an agent to request the hivemind (subclass of `BotHelperRequest`). This is done using a `BaseIndependentAgent`. I abstracted away all the hassle of making a request with `DroneAgent`. All you need now is just to subclass it like this:

```python
class Drone(DroneAgent):
    # Relative path to the hivemind file.
    hive_path = './some/relative/path.py'
    # Bots with the same key will be part of the same hivemind.
    hive_key = 'my_unique_hivemind_key'
    # Name of your hivemind that shows up in the console.
    hive_name = 'Terrible Name'
```

- `hive_path` points towards the main hivemind file containing a `PythonHivemind` subclass. This can be the same file that the `DroneAgent` is in, in which case you can just point to `__file__`.
- `hive_key` matches up agents with the same key into one hivemind. Your key should be unique so that when two hiveminds meet there is no confusion over which bot is whose.
- `hive_name` determines the name that shows up in the console when you use the `self.logger`. ![image](console.png)

### The Hivemind

This is where all your bot logic goes. The `PythonHivemind` is a subclass of `BotHelperProcess`. When the drones request a hivemind, a process is created with the unique key if one doesn't already exist with that key. This process is your hivemind and it has control over the drones that requested it.

Here's a basic template for what a hivemind looks like:

```python
class MyVeryOwnHivemind(PythonHivemind):

    def initialize_hive(self, packet: GameTickPacket) -> None:
        pass

    def get_outputs(self, packet: GameTickPacket) -> Dict[int, PlayerInput]:
        return {index: PlayerInput() for index in self.drone_indices}
```

You will notice that is not unlike a standard Python bot. Instead of `initialize_agent` and `get_output` methods we have `initialize_hive` and `get_outputs` methods.

The `initialize_hive` method is for any code that you want to run before any `get_outputs` calls. It differs from `initialize_agent` in that you also get access to the packet. This is done because it is convenient to have when initializing objects. I recommend you use the method initializing objects for each of your drones, the ball, and other cars.

`get_outputs` gets called every time a new packet arrives (Does not use a rate limiter). It differs from `get_output` in the expected return. Since `get_output` only determines the controls for one car, it only returns a single controller state. A hivemind controls more bots, so we use a dictionary, where the keys are drone indices, and the values are `PlayerInput`s. `PlayerInput` is basically the same as `SimpleControllerState` for our use case.

**`self.drone_indices` is a set of bot indices which your hivemind controls.**

Normally, a `BotHelperProcess` would have to use `GameInterface` methods to access things like ball prediction or rendering. These methods have been wrapped similar to normal Python bot methods.

Without wrapper:

```python
# In initialization:
self.ball_prediction = BallPrediction()
# In main loop:
self.game_interface.update_ball_prediction(self.ball_prediction)
```

With wrapper:

```python
self.ball_prediction = self.get_ball_prediction_struct
```

***

## Rust

You will need:

- a bot configuration file
- an appearance configuration file
- a dummy `DroneAgent`
- a `SubprocessHivemind` (subclass of `BotHelperProcess`)
- an executable to control the hivemind.

### Bot Configuration File

The bot configuration file must have the file ending `.cfg` and look something like this (see `config.cfg` in the examples):

```toml
[Locations]
# Path to loadout config. Can use relative path from here.
looks_config = ./appearance.cfg

# Path to python file. Can use relative path from here.
python_file = ./hive.py

# Name of the bot in-game
name = Drone
```

Note that unlike when running a normal Rust bot, you do not specify the path to the executable in the config file.

### Appearance configuration file

The appearance file is just a normal appearance file. See [the rlbot wiki](https://github.com/RLBot/RLBot/wiki/Bot-Customization) for more info.

### Dummy Drone Agent

RLBot needs an agent to request the hivemind (subclass of `BotHelperRequest`). This is done using a `BaseIndependentAgent`. I abstracted away all the hassle of making a request with `DroneAgent`. All you need now is just to subclass it like this:

```python
class Drone(DroneAgent):
    # Relative path to the hivemind file.
    hive_path = './some/relative/path.py'
    # Bots with the same key will be part of the same hivemind.
    hive_key = 'my_unique_hivemind_key'
    # Name of your hivemind that shows up in the console.
    hive_name = 'Terrible Name'
```

- `hive_path` points towards the main hivemind file containing a `SubprocessHivemind` subclass. This can be the same file that the `DroneAgent` is in, in which case you can just point to `__file__`.
- `hive_key` matches up agents with the same key into one hivemind. Your key should be unique so that when two hiveminds meet there is no confusion over which bot is whose.
- `hive_name` determines the name that shows up in the console when you use the `self.logger`. ![image](console.png)

### The Hivemind

The `SubprocessHivemind` is a subclass of `BotHelperProcess`. When the drones request a hivemind, a process is created with the unique key if one doesn't already exist with that key. Once it collects all the indices, it launches your executable with the drone indices as arguments.

You need to specify the path to the executable by setting `exec_path`.

TODO: Make relatives path work

```python
class MyOwnRustHivemind(SubprocessHivemind):
    # Path to the executable.
    exec_path = str(
        Path(__file__).parent.parent / 'target' / 'debug' / 'example.exe')
```

### The Executable

If you have made a Rust bot before, the framework is very similar:

```rust
use std::error::Error;

fn main() -> Result<(), Box<dyn Error>> {
    rlbot::run_hive(MyHivemind { drone_indices: vec![] })
}

struct MyHivemind {
    drone_indices: Vec<usize>
}

impl rlbot::Hivemind for MyHivemind {
    fn set_drone_indices(&mut self, indices: Vec<usize>) {
        self.drone_indices = indices;
    }

    fn tick(&mut self, packet: &rlbot::GameTickPacket) -> Vec<rlbot::ControllerState> {

        let mut inputs: Vec<rlbot::ControllerState> = vec![];
        for _index in self.drone_indices.iter() {
            inputs.push(
                rlbot::ControllerState {
                    throttle: 1.0,
                    ..Default::default()
                }
            );
        }

        inputs
    }
}
```

Important differences from the normal Rust bot framework:

- `run_hive` instead of `run_bot`. It also expects a struct which implements the `Hivemind` trait.
- instead of `set_player_index` there is `set_drone_indices` which gives you a `Vec<usize>`.
- `tick` expects a return of `Vec<ControllerState>` instead of just one `ControllerState`. The first input will be sent to the first index in drone_indices, and so forth.

Otherwise it is pretty much the same as a normal Rust bot.

***

## Other Languages

TODO

***

## Help

If you have further questions ask me on Discord `@Calculated_Will#4544`.

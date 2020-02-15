# Hivemind

Hivemind bots for [RLBot](rlbot.org).

This repo is for experimentation and examples.
A proper pull request to the framework will be made once everything is working as intended.

## Python

To get started with your own hivemind in Python you will need these four things:

- a bot configuration file
- an appearance configuration file
- a dummy `DroneAgent`
- a `Hivemind` (subclass of `BotHelperProcess`)

### Bot configuration file

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

## Rust

TODO

## Other Languages

TODO

## Help

If you have further questions ask me on Discord `@Calculated_Will#4544`.

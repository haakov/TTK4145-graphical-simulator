# TTK4145-graphical-simulator

A _crude_ graphical alternative to TTK4145's elevator simulator. Written in Python 3 using [Pyglet](https://bitbucket.org/pyglet/pyglet/wiki/Home).

### TODO: 
* Stop and Obstruction buttons for single elevators
* Manual motor override
* Command line arguments
* User-specified amount of elevators and floors


## Usage

```
$ git clone https://github.com/haakov/TTK4145-graphical-simulator
$ cd TTK4145-graphical-simulator
$ pip3 install pyglet
$ python3 main.py
```

The simulator will now listen for connections on ports 15657, 15658 and 15659.

Stop: Enter
Obstruction: Backspace
(These two work on all three elevators simultaneously)

### Elevator 1

Reset: F1

| Floor | Hall up | Hall down | Cab |
|-------|---------|-----------|-----|
| 3     |         | 2         | 3   |
| 2     | Q       | W         | E   |
| 1     | A       | S         | D   |
| 0     | Z       |           | C   |

### Elevator 2

Reset: F2

| Floor | Hall up | Hall down | Cab |
|-------|---------|-----------|-----|
| 3     |         | 5         | 6   |
| 2     | R       | T         | Y   |
| 1     | F       | G         | H   |
| 0     | V       |           | N   |

### Elevator 3

Reset: F3

| Floor | Hall up | Hall down | Cab |
|-------|---------|-----------|-----|
| 3     |         | 8         | 9   |
| 2     | U       | I         | O   |
| 1     | J       | K         | L   |
| 0     | M       |           | .   |

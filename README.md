# So You Think You Can Program An Elevator

Many of us ride elevators every day. We feel like we understand how they work, how they decide where to go. If you were asked to put it into words, you might say that an elevator goes wherever it's told, and in doing so goes as far in one direction as it can before turning around. Sounds simple, right? Can you put it into code?

In this challenge, you are asked to implement the business logic for a simplified elevator model in Python. We'll ignore a lot of what goes into a real world elevator, like physics, maintenance overrides, and optimizations for traffic patterns. All you are asked to do is to decide whether the elevator should go up, go down, or stop.

How does the challenge work? The simulator and test harness are laid out in this document, followed by several examples. All of this can be run in an actual Python interpreter using Python's built-in `doctest` functionality, which extracts the code in this document and runs it.

A naive implementation of the business logic is provided in the `elevator.py` file in this project. If you run `doctest` using the provided implementation, several examples fail to produce the expected output. Your challenge is to fix that implementation until all of the examples pass.

Open a pull request with your solution. Good luck! Have fun!

## Test Harness

Like all elevators, ours can go up and down. We define constants for these. The elevator also happens to be in a building with six floors.

    >>> UP = 1
    >>> DOWN = 2
    >>> FLOOR_COUNT = 6

We will make an `Elevator` class that simulates an elevator. It will delegate to another class which contains the elevator business logic, i.e. deciding what the elevator should do. Your challenge is to implement this business logic class.

### User actions

A user can interact with the elevator in two ways. She can call the elevator by pressing the up or down  button on any floor, and she can select a destination floor by pressing the button for that floor on the panel in the elevator. Both of these actions are passed straight through to the logic delegate.

    >>> class Elevator(object):
    ...     def call(self, floor, direction):
    ...         self._logic_delegate.on_called(floor, direction)
    ... 
    ...     def select_floor(self, floor):
    ...         self._logic_delegate.on_floor_selected(floor)

### Elevator actions

The logic delegate can respond by setting the elevator to move up, move down, or stop. It can also read the current floor and movement direction of the elevator. These actions are accessed through `Callbacks`, a mediator provided by the `Elevator` class to the logic delegate.

    >>> class Elevator(Elevator):
    ...     def __init__(self, logic_delegate, starting_floor=1):
    ...         self._current_floor = starting_floor
    ...         print "%s..." % starting_floor,
    ...         self._motor_direction = None
    ...         self._logic_delegate = logic_delegate
    ...         self._logic_delegate.callbacks = self.Callbacks(self)
    ... 
    ...     class Callbacks(object):
    ...         def __init__(self, outer):
    ...             self._outer = outer
    ... 
    ...         @property
    ...         def current_floor(self):
    ...             return self._outer._current_floor
    ... 
    ...         @property
    ...         def motor_direction(self):
    ...             return self._outer._motor_direction
    ... 
    ...         @motor_direction.setter
    ...         def motor_direction(self, direction):
    ...             self._outer._motor_direction = direction

### Simulation

The simulation runs in steps. Each time step consists of the elevator moving a single floor, or pausing at a floor. Either way, the business logic delegate gets notified. Along the way, we print out the movements of the elevator so that we can keep track of it. We also define a few helper methods that advance the simulation to points of interest, for ease of testing.

    >>> class Elevator(Elevator):
    ...     def step(self):
    ...        delta = 0
    ...        if self._motor_direction == UP: delta = 1
    ...        elif self._motor_direction == DOWN: delta = -1
    ... 
    ...        if delta:
    ...            self._current_floor = self._current_floor + delta
    ...            print "%s..." % self._current_floor,
    ...            self._logic_delegate.on_floor_changed()
    ...        else:
    ...            self._logic_delegate.on_ready()
    ... 
    ...        assert self._current_floor >= 1
    ...        assert self._current_floor <= FLOOR_COUNT
    ...     
    ...     def run_until_stopped(self):
    ...         self.step()
    ...         while self._motor_direction is not None: self.step()
    ...     
    ...     def run_until_floor(self, floor):
    ...         for i in range(100):
    ...             self.step()
    ...             if self._current_floor == floor: break
    ...         else: assert False

That's it for the framework.

## Business Logic

As for the business logic, an example implementation is provided in the `elevator.py` file in this project.

    >>> from elevator import ElevatorLogic

As provided, it doesn't pass the tests in this document. Your challenge is to fix it so that it does. To run the tests, run this in your shell:

    python -m doctest -v README.md

With the correct business logic, here's how the elevator should behave:

## Fuzz testing

No amount of legal moves should compel the elevator to enter an illegal state. Here, we run a bunch of random requests against the simulator to make sure that no asserts are triggered.

    >>> import random
    >>> e = Elevator(ElevatorLogic())
    1...
    >>> try: print '-',  # doctest:+ELLIPSIS
    ... finally:
    ...     for i in range(100000):  
    ...         r = random.randrange(6)
    ...         if r == 0: e.call(
    ...             random.randrange(FLOOR_COUNT) + 1,
    ...             random.choice((UP, DOWN)))
    ...         elif r == 1: e.select_floor(random.randrange(FLOOR_COUNT) + 1)
    ...         else: e.step()
    - ...


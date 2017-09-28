UP = 1
DOWN = 2
FLOOR_COUNT = 6

class ElevatorLogic(object):
    """
    An incorrect implementation. Can you make it pass all the tests?

    Fix the methods below to implement the correct logic for elevators.
    The tests are integrated into `README.md`. To run the tests:
    $ python -m doctest -v README.md

    To learn when each method is called, read its docstring.
    To interact with the world, you can get the current floor from the
    `current_floor` property of the `callbacks` object, and you can move the
    elevator by setting the `motor_direction` property. See below for how this is done.
    """

    def __init__(self):
        # Feel free to add any instance variables you want.
        self.destination_floor = None
        self.callbacks = None
        self.queue = [] # adding a queue to handle more than 1 request

    def on_called(self, floor, direction):
        """
        This is called when somebody presses the up or down button to call the elevator.
        This could happen at any time, whether or not the elevator is moving.
        The elevator could be requested at any floor at any time, going in either direction.

        floor: the floor that the elevator is being called to
        direction: the direction the caller wants to go, up or down
        """
        self.destination_floor = floor
        # Append an Object containing the request and direction
        self.queue.append({ "floor": floor, "direction": direction })

    def on_floor_selected(self, floor):
        """
        This is called when somebody on the elevator chooses a floor.
        This could happen at any time, whether or not the elevator is moving.
        Any floor could be requested at any time.

        floor: the floor that was requested
        """
        # Append an Object containing the request and direction will be nothing
        # compare next request on the queue with the requested and determine if it should be ignored
        if len(self.queue) != 0: 
            next_in_queue = self.queue[0]
            if next_in_queue["floor"] < floor:
                self.queue.append({ "floor": floor, "direction": 0 })
            # Otherwise ignore the 

    def on_floor_changed(self):
        """
        This lets you know that the elevator has moved one floor up or down.
        You should decide whether or not you want to stop the elevator.
        """
        current_floor = self.callbacks.current_floor
        current_direction = self.callbacks.motor_direction
        for request in self.queue:
            requested_floor = request["floor"]
            requested_direction = request["direction"]
            if current_floor == requested_floor and \
                (requested_direction == current_direction or \
                requested_direction == 0):
                self.queue.remove(request)
                self.callbacks.motor_direction = None

    def on_ready(self):
        """
        This is called when the elevator is ready to go.
        Maybe passengers have embarked and disembarked. The doors are closed,
        time to actually move, if necessary.
        """
        # get the first floor in the queue and keep moving on that direction
        if len(self.queue) == 0:
            return

        destination = self.queue[0]
        if destination["floor"] > self.callbacks.current_floor:
            self.callbacks.motor_direction = UP
        elif destination["floor"] < self.callbacks.current_floor:
            self.callbacks.motor_direction = DOWN


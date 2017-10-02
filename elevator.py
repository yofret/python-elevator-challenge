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
        self.last_direction = None

    def on_called(self, floor, direction):
        """
        This is called when somebody presses the up or down button to call the elevator.
        This could happen at any time, whether or not the elevator is moving.
        The elevator could be requested at any floor at any time, going in either direction.

        floor: the floor that the elevator is being called to
        direction: the direction the caller wants to go, up or down
        """
        # Append an Object containing the request and direction
        if floor == 1 and direction == DOWN or floor == FLOOR_COUNT and direction == UP:
            return
        if not self.is_valid_floor(floor):
            return

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
        
        # Ignore all request in opposite direction
        if floor < self.callbacks.current_floor and self.last_direction == UP or \
        floor > self.callbacks.current_floor and self.last_direction == DOWN or \
        floor == self.callbacks.current_floor or \
        not self.is_valid_floor(floor):
            return

        if floor > self.callbacks.current_floor:
            self.last_direction = UP
        elif floor < self.callbacks.current_floor:
            self.last_direction = DOWN
        else:
            return

        # If Floor is already requested
        for request in self.queue:
            if floor == request["floor"]:
                return
            
        self.queue.insert(0,{ "floor": floor, "direction": 0 })
        # print(self.queue, self.last_direction)

    def on_floor_changed(self):
        """
        This lets you know that the elevator has moved one floor up or down.
        You should decide whether or not you want to stop the elevator.
        """

        current_floor = self.callbacks.current_floor
        for request in self.queue:
            if request["floor"] == current_floor:
                should_stop = self.elevator_should_stop(request)
                # print(should_stop, request)
                if should_stop:
                    self.queue.remove(request)
                    self.callbacks.motor_direction = None
                    # If there is no more floors put direction to none
                    if len(self.queue) == 0:
                        self.last_direction = None

    def on_ready(self):
        """
        This is called when the elevator is ready to go.
        Maybe passengers have embarked and disembarked. The doors are closed,
        time to actually move, if necessary.
        """
        # get the first floor in the queue and keep moving on that direction
        if len(self.queue) == 0:
            self.last_direction = None
            return
        
        # print(self.queue)

        destination = self.queue[0]
        if destination["floor"] > self.callbacks.current_floor:
            self.callbacks.motor_direction = UP
            self.last_direction = UP
        elif destination["floor"] < self.callbacks.current_floor:
            self.callbacks.motor_direction = DOWN
            self.last_direction = DOWN
        else:
            # Inverse direction
            self.inverse_direction()


    def elevator_should_stop(self, request):
        requested_direction = request["direction"]

        is_same_direction = requested_direction == self.callbacks.motor_direction
        is_stop_request = requested_direction == 0
        has_further_request = self.has_further_request()

        return is_same_direction or is_stop_request or not has_further_request

    def has_further_request(self):
        if self.last_direction == UP:
            for request in self.queue:
                if request["floor"] > self.callbacks.current_floor:
                    return True
            return False
        elif self.last_direction == DOWN:
            for request in self.queue:
                if request["floor"] < self.callbacks.current_floor:
                    return True
            return False
    
    def last_request(self):
        if len(self.queue) == 1:
            return True
        return False
    
    def is_valid_floor(self, floor):
        if(floor >= 1 or floor <= FLOOR_COUNT):
            return True
        return False

    def inverse_direction(self):
        if self.last_direction == UP:
            self.last_direction = DOWN
        elif self.last_direction == DOWN:
            self.last_direction = UP
        else:
            self.last_direction = None

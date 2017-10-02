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
        if floor == self.callbacks.current_floor and self.callbacks.motor_direction == None:
            return

        if self.floor_is_upcoming(floor):
            self.queue.insert(0, { "floor": floor, "direction": direction })
        else:
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
        has_request = filter(lambda request: request["floor"] == floor, self.queue)
        if floor < self.callbacks.current_floor and self.last_direction == UP or \
        floor > self.callbacks.current_floor and self.last_direction == DOWN or \
            len(has_request) > 0:
            return

        if floor > self.callbacks.current_floor:
            self.last_direction = UP
        elif floor < self.callbacks.current_floor:
            self.last_direction = DOWN
        else:
            return
            
        self.queue.insert(0,{ "floor": floor, "direction": 0 })

    def on_floor_changed(self):
        """
        This lets you know that the elevator has moved one floor up or down.
        You should decide whether or not you want to stop the elevator.
        """
        current_floor = self.callbacks.current_floor

        # print(current_floor, self.callbacks.motor_direction)
        loop_queue = filter(lambda request: request["floor"] == current_floor, self.queue)
        completed = []

        for request in loop_queue:
            if self.elevator_should_stop(request):
                self.callbacks.motor_direction = None
                completed.append(request)
                direction = request["direction"]

        for completed_request in completed:
             self.queue.remove(completed_request)

        if len(self.queue) == 0:
            self.last_direction = direction

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

        destination = self.queue[0]

        if destination["floor"] > self.callbacks.current_floor:
            self.callbacks.motor_direction = UP
            self.last_direction = UP
        elif destination["floor"] < self.callbacks.current_floor:
            self.callbacks.motor_direction = DOWN
            self.last_direction = DOWN
        else:
            # Inverse direction
            self.last_direction = self.inverse_direction()
            self.queue = filter(lambda request: request["floor"] != self.callbacks.current_floor, self.queue)

    def elevator_should_stop(self, request):
        return self.is_valid_stop(request) or not self.has_further_request()
    
    def is_valid_stop(self, request):
        requested_direction = request["direction"]

        is_same_direction = requested_direction == self.callbacks.motor_direction
        is_stop_request = requested_direction == 0
        # has_further_request = self.has_further_request()

        return is_same_direction or is_stop_request

    def has_further_request(self):
        for request in self.queue:
            if self.is_valid_stop(request) or self.floor_is_upcoming(request["floor"]):
                return True
        return False
    
    def floor_is_upcoming(self, floor):
        if self.last_direction == UP:
            return floor > self.callbacks.current_floor
        elif self.last_direction == DOWN:
            return floor < self.callbacks.current_floor

    def is_edge_floor(self, floor):
        if floor == 1 or floor == FLOOR_COUNT:
            return True
        return False 

    def inverse_direction(self):
        if self.last_direction == UP:
            return DOWN
        elif self.last_direction == DOWN:
            return UP
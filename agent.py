from field import Field

class Agent:
    def __init__(self, field = Field()) -> None:
        self.position, self.goal = field.start, field.goal
        self.field = field
        self.unsafe = list()
        self.path = list()

    # Returns a list of actions which the agent can take
    def actions(self) -> list:
        x, y = self.position
        moves = [
            ((x + 1, y), "DOWN"),
            ((x - 1, y), "UP"),
            ((x, y + 1), "RIGHT"),
            ((x, y - 1), "LEFT")
        ]
        actions = dict()
        for move in moves:
            if 0 <= move[0][0] < self.field.length and 0 <= move[0][1] < self.field.length and move not in self.unsafe:
                actions[move[1]] = move[0]
        return actions
    
    # Return True if agent has reached goal, else return False
    def check_goal(self):
        if self.position == self.goal:
            return True
        return False
    
    # Return True if agent hit mine, else return False
    def check_mine(self):
        if self.position in self.field.mines:
            return True
        return False
    
    # Move agent to coordinate
    def move(self, coordinate) -> None:
        self.position = coordinate

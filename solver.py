from field import Field
from agent import Agent
from random import choices
from time import time
from copy import deepcopy

LENGTH = 10
MINES = 25
START = (0, 0)
GOAL = (9, 9)
PROB = 0.9 # Probability that agent will select the most optimal move
MAX_RESETS = 5000 # Reset limit when searching for solution

def main():
    # Check that start and goal variables are valid:
    for x, y in [START, GOAL]:
        if 0 <= x < LENGTH and 0 <= y < LENGTH:
            pass
        else:
            print("Invalid start or goal coordinates. Check global variables.")
            return 1
    # Create field with mines
    game = Field(length=LENGTH, mines=MINES, start=START, goal=GOAL)
    # Create reference field with no mines, for marking
    reference = Field(length=LENGTH, mines=0, start=START, goal=GOAL)
    # Create agent object
    agent = Agent(game)
    try:
        # Search for path via reinforcement learning
        result = search(agent, reference)
    except EOFError:
        print("Search terminated.")
    if result:
        print("Solution found! Game ended.")
        return 0
    else:
        print(f"Hidden Minefield:\n{agent.field}")
        print("No solution found!")
    
def search(agent, reference):
    solution = None
    # Save start time
    start = time()
    last_update = start
    # Initialise counts
    resets = 0
    longest_path = 0
    cost = agent.field.length ** 2
    # Lowest theoretically possible cost
    lowest_cost = abs(GOAL[0] - START[0]) + abs(GOAL[1] - START[1])
    # End loop if limit is exceeded
    while resets < MAX_RESETS:
        # Mark current position of the agent on the reference field
        reference.mark_field(agent.position, 1)
        # Add current position to path
        agent.path.append(agent.position)

        # Obtain list of all possible actions from current position
        actions = agent.actions()
        options = list()
        # Remove actions which agent has already explored
        for action in actions:
            if actions[action] not in agent.path:
                options.append(actions[action])

        # With PROB probability, select the most optimal move from the list of moves in options. Else, select a random move.
        rand = choices([True, False], [PROB, 1 - PROB])[0]
        if rand == True and options:
            move = informed_action(agent, options)
        elif options:
            move = choices(options)[0]

        # Move agent to new position
        agent.move(move)

        # If agent has reached the goal state
        if agent.check_goal():
            # Obtain cost of state
            new_cost = reference.count_marker(1)
            print(f"\nNew solution found after {elapsed:.4f} seconds and {resets} resets (cost = {new_cost}):\n{reference}\n")
            # Save solution if cost is lowest seen
            if new_cost < cost:
                cost = new_cost
                solution = deepcopy(reference)
                if cost == lowest_cost:
                    break
            print(reference)
            # Reset agent and reference field
            reset(agent, reference)
            resets += 1

        # If agent encountered mine or dead end
        if agent.check_mine() or not options:
            # Add move to unsafe list
            agent.unsafe.append(move)
            # Add move to reference field
            reference.map[move[0]][move[1]] = "X"
            reference.mines.append(move)
            reset(agent, reference)
            resets += 1
            # Update elapsed time
        elapsed = time() - start
        path_length = reference.count_marker(1)
        
        # Update terminal every second or if new longest path found
        if path_length > longest_path or time() - last_update > 1:
            last_update = time()
            longest_path = path_length
            print(f"Searching...\nCurrent position: {agent.position}\nActions: {options}\nPath: {agent.path}    (Enter ctrl D to terminate search)\n{reference}")
    
    # If solution exists, return True, else return False
    if solution:
        print(f"Most optimal solution (Cost={cost}) found after {(time() - start):.4f} seconds and {resets} resets:\n{solution}")
        return True
    print(f"\nNo path found after {elapsed:.4f} seconds.")
    print(f"Resets: {resets}")
    return False

# Given a list of actions, return the most optimal action.
def informed_action(agent, actions):
    cost = agent.field.length * 2
    goal_x, goal_y = agent.goal
    best = actions[0]
    for action in actions:
        x, y = action
        new_cost = abs(goal_x - x) + abs(goal_y - y)
        if new_cost < cost:
            cost = new_cost
            best = action
        elif new_cost == cost:
            best = choices([action, best])[0]
    return best

# Function to reset agent and reference field
def reset(agent, reference):
    # Reset game field
    agent.field.reset()
    # Reset reference field
    reference.reset()
    # Move agent to start
    agent.move(START)
    # Reset path
    agent.path = list()

if __name__ == "__main__":
    main()
from field import Field
from agent import Agent
from random import choices
from time import time

LENGTH = 10
MINES = 20
START = (0, 0)
GOAL = (9, 9)
PROB = 0.7 # Probability that agent will select the most optimal move
MAX_RESETS = 30000 # Reset limit when searching for solution

def main():
    # Create field with mines
    game = Field(length=LENGTH, mines=MINES, start=START, goal=GOAL)
    # Create reference field with no mines, for marking
    reference = Field(length=LENGTH, mines=0, start=START, goal=GOAL)
    # Create agent object
    agent = Agent(game)
    # Search for path via reinforcement learning
    try:
        result = search(agent, reference)
    except EOFError:
        print("Search terminated.")
    print(f"Hidden Minefield:\n{agent.field}")
    if result:
        print("Goal reached! Game ended.")
        return 0
    else:
        print(f"Agent's map:\n{reference}")
    
def search(agent, reference):
    # Save start time
    start = time()
    last_update = start
    # Initialise counts
    resets = 0
    longest_path = 0
    # End loop if time limit is exceeded
    while resets < MAX_RESETS:
        # Mark the current position of the agent on the reference field as H
        reference.mark_field(agent.position, "H")
        # Add current position to path
        agent.path.append(agent.position)
        # Obtain list of all possible actions from current position
        actions = agent.actions()
        options = list()
        # Remove actions which agent has previously already explored
        for action in actions:
            if action not in agent.path:
                options.append(actions[action])
        # With PROB probability, select the most optimal move from the list of moves in options. Else, select a random move.
        rand = choices([True, False], [PROB, 1 - PROB])[0]
        if rand == True and options:
            move = informed_action(agent, options)
        elif options:
            move = choices(options)[0]
        # Before moving, mark the current position as 1 before moving to the next position
        reference.mark_field(agent.position, 1)
        # Move agent to new position
        agent.move(move)
        # If agent has reached the goal state, return 0
        if agent.check_goal():
            elapsed = time() - start
            print(f"\nSolution found after {elapsed:.4f} seconds and {resets} resets:")
            print(reference)
            return True
        # If agent encountered mine or is stuck in a dead end
        elif agent.check_mine() == 1 or not options:
            # Add move to unsafe list
            agent.unsafe.append(move)
            # Add move to reference field
            reference.map[move[0]][move[1]] = "X"
            reference.mines.append(move)
            # Reset game field
            agent.field.reset()
            # Reset reference field
            reference.reset()
            # Move agent to start
            agent.move(START)
            # Add to reset count
            resets += 1
            # Reset path
            agent.path.clear()
        elapsed = time() - start
        path_length = reference.count_marker(1)
        # Update terminal every second or if new longest path found
        if path_length > longest_path or time() - last_update > 1:
            last_update = time()
            longest_path = path_length
            print(f"Searching...    (Enter ctrl D to terminate search)\n{reference}")
    print(f"\nNo path found after {round(elapsed)} seconds.")
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

if __name__ == "__main__":
    main()
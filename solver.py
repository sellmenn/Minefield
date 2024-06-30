from field import Field
from agent import Agent
from random import choices
from time import time
from copy import deepcopy

LENGTH = 10
MINES = 20
START = (0, 0)
GOAL = (9, 9)
PROB = 0.9 # Probability that agent will select the most optimal move
MAX_RESETS = 500 # Reset limit when searching for solution


def main():
    # Check that start and goal variables are valid:
    for x, y in [START, GOAL]:
        if not 0 <= x < LENGTH or not 0 <= y < LENGTH:
            print("Invalid start or goal coordinates. Check global variables.")
            return 1
    # Create field with mines
    game = Field(length=LENGTH, mines=MINES, start=START, goal=GOAL)
    # Create reference field with no mines, for marking
    reference = Field(length=LENGTH, mines=0, start=START, goal=GOAL)
    # Create agent object
    agent = Agent(game)
    # Search for path using reinforcement learning
    result = search(agent, reference)
    if result:
        print("Solution found! Game ended.\n")
        return 0
    print(f"Hidden Minefield:\n{agent.field}\nNo solution found!")
    

def search(agent, reference):
    solution = None
    # Save start time
    start = time()
    last_update = start
    # Initialise variables
    resets = 0
    longest_path = 0
    cost = agent.field.length ** 2
    # Save lowest theoretically possible cost
    lowest_cost = abs(GOAL[0] - START[0]) + abs(GOAL[1] - START[1])

    # While limit is not exceeded
    while resets < MAX_RESETS:
        # Mark current position of the agent on reference field
        reference.mark_field(agent.position, 1)
        # Add current position to path
        agent.path.append(agent.position)

        # Obtain list of all possible actions for current position
        actions_dict = agent.actions()
        actions = list()
        for key in actions_dict:
            actions.append(actions_dict[key])
        # If unable to leave start, break from loop
        if agent.position == START and not actions:
            break

        # With PROB probability, select the most optimal move from the list of moves in options. Else, select a random move.
        rand = choices([True, False], [PROB, 1 - PROB])[0]
        if rand == True and actions:
            move = informed_action(agent, actions)
        elif actions:
            move = choices(actions)[0]

        # Move agent to new position
        agent.move(move)

        # If agent has reached the goal state
        if agent.check_goal():
            # Obtain cost of state
            new_cost = reference.count_marker(1)
            print(f"\nNew solution found(cost = {new_cost}):\n{reference}\n")
            # Save solution if cost is lowest so far
            if new_cost < cost:
                cost = new_cost
                solution = deepcopy(reference)
                # Break if cost is lowest theoretically possible
                if cost == lowest_cost:
                    break
            # Reset agent and reference field
            reset(agent, reference)
            resets += 1

        # If agent encountered mine or dead end
        if agent.check_mine() or not actions:
            # Add move to unsafe list
            agent.unsafe.append(move)
            # Add move to reference field
            reference.map[move[0]][move[1]] = "X"
            reference.mines.append(move)
            reset(agent, reference)
            resets += 1
        
        # Update terminal every second
        if time() - last_update > 1:
            last_update = time()
            print(f"Searching...\nCurrent position: {agent.position}\nActions: {actions}\n{reference}")
    
    # Update elapsed time
    elapsed = time() - start
    # If solution exists, return True, else return False
    if solution:
        print(f"Hidden Minefield:\n{agent.field}")
        print(f"Most optimal solution (Cost={cost}) found after {elapsed:.4f} seconds and {resets} resets:\n{solution}")
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
    agent.field.reset()
    reference.reset()
    agent.move(START)
    agent.path.clear()

if __name__ == "__main__":
    main()
# MINEFIELD

Minefield is a popular team-building game in which players have to navigate a physical space without touching 'mines' that have been planted in the area. Players accomplish this blindfolded, guided only by the voices of their teammates.
---

## HOW TO RUN

Ensure all modules in requirements.txt have been installed. Simply use pip3 install -r requirements.txt in your terminal.
Type python3 solver.py in your terminal and press Enter.
The program defaults to a field with sides of 10 units, containing 20 mines.
For configuration, modify the global variables in solver.py. Ensure that START and GOAL are coordinates within the field.

## PROJECT DESCRIPTION

In this project's adaptation of Minefield, an AI agent must navigate a 'minefield', represented as a grid of coordinates, without prior knowledge of where the mines are placed. Each time the agent encounters a coordinate with a mine, it restarts from its original position. The agent wins if it reaches the goal coordinate without encountering any mines in a single attempt.

The purpose of this project was to experiment with reinforcement learning. Hence, the code was designed around such an approach instead of conventional breadth-first search. To guide the agent through the minefield, a simple heuristic was used to measure the utility of each move. If X and Y represent the coordinates of the goal, and x and y represent the current position, the utility of the position is calculated as abs(X - x) + abs(Y - y). A smaller utility score indicates a more optimal move.

Occasionally, a minefield may be generated with no possible solution. The agent's progress can be monitored in the terminal.

The project includes three files:

* agent.py - contains the Agent class.
* field.py - contains the Field class.
* solver.py - contains the code to search for a solution path through the minefield.

### Agent Class

The Agent class includes instance methods to simulate an agent navigating a minefield. It takes a single Field object as an argument.

* The unsafe attribute, initialized as an empty list, stores coordinates of known mines.
* The actions instance method returns a list of possible moves for the agent, excluding actions that encounter known mines.
* The check_goal and check_mine instance methods return True if the agent's coordinate matches the goal or a mine respectively on the field; otherwise, False.

### Field Class

The Field class includes instance methods to simulate a minefield. It accepts four optional arguments: length, mines, start, and goal.

* The length attribute determines the dimensions of the square minefield.
* The mines attribute determines the number of mines in the minefield.
* The start and goal attributes determine the starting and goal coordinates for the board.

During initialization of a Field object, when create_field() is called:

An empty table represented by lists is generated and stored in the map attribute, with empty coordinates represented as 0.
Mines, represented by 'X', are stored in the map attribute, as well as in the mines attribute.
When mark_field(coordinate, marker) is called:

The provided coordinate is marked with the marker in the corresponding position within the map attribute.
In this project's implementation, an agent's path is represented by 1s.
When reset_field() is called:

Within the map attribute, any coordinate that contains neither 0 nor 'X' is reset to 0 by calling the unmark_field function.

### solver.py

#### search(agent, reference)

The backbone of solving the problem, this function takes two arguments: the agent and a separate Field object reference. It's worth noting that the agent doesn't always choose the most optimal path based on the heuristic. In edge-case scenarios, an action resulting in a smaller utility may lead to a dead end. Therefore, with a probability determined by the global variable PROB, the agent may randomly select an action.

* The function checks if the agent's current position is a goal state. If so, the function returns.
* It obtains a list of possible actions that can be taken, excluding known mines and coordinates already on the agent's path.
* With a probability determined by the global variable PROB, the function selects the most optimal action from the list; otherwise, it randomly selects an action.
* If the agent is stuck in a dead-end or encounters a mine, it marks the coordinate as unsafe. The coordinate is added to the agent's unsafe attribute and marked on the reference Field object. The agent's position and its associated Field object are reset.

#### informed_action(agent, actions)
This function takes two arguments: the agent and a list of actions that can be taken. To guide the agent through the minefield, a simple heuristic was used to calculate the utility score for each move. If X and Y represent the coordinates of the goal, and x and y represent the coordinates of a given position, the utility of this position is given by abs(X - x) + abs(Y - y). A smaller utility score indicates a more optimal move.

For each action, a utility score is calculated.
* If the current utility score is smaller than previously recorded scores, its associated move is saved.
* If the current utility score matches the current saved score, there's a 50% chance that this action overwrites the previously saved one.
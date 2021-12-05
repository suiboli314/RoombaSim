import numpy as np

def path_planning(start_location, end_location):
    # create new Matrix
    rewards_new = np.copy(rewards)
    # Get the ending state
    ending_state = location_to_state[end_location]
    # set the trash with highest point
    rewards_new[ending_state, ending_state] = 100
    print(rewards_new)

    # Initializing Q Values table
    Q = np.array(np.zeros([9, 9]))
    print(Q)

    # Q-Learning process 1000 times
    for i in range(1000):
        # Pick up a state randomly
        current_state = np.random.randint(0, 9)
        playable_actions = []
        # Iterate through rewards_new matrix and get actions > 0
        for j in range(9):
            if rewards_new[current_state, j] != 0:
                playable_actions.append(j)
        # Pick an action randomly from the list of playable actions
        next_state = np.random.choice(playable_actions)
        # Get the temporal difference
        TD = rewards_new[current_state, next_state] + gamma * Q[next_state, np.argmax(Q[next_state,])] - Q[
            current_state, next_state]
        # Update the Q Value table using Bellman equation
        Q[current_state, next_state] += alpha * TD

    print(Q)
    # Initialize start_location and next_location
    route = [start_location]
    next_location = start_location

    while (next_location != end_location):
        starting_state = location_to_state[start_location]
        # Fetch the highest value in Q value table for starting state
        next_state = np.argmax(Q[starting_state,])
        next_location = state_to_location[next_state]
        route.append(next_location)
        # Update the starting location for the next iteration
        start_location = next_location

    return route


if __name__ == '__main__':
    # Initialize parameters
    gamma = 0.8  # Discount factor (0.8-0.99)
    alpha = 0.9  # Learning rate

    # Define the states
    location_to_state = {
        'S1': 0,
        'S2': 1,
        'S3': 2,
        'S4': 3,
        'S5': 4,
        'S6': 5,
        'S7': 6,
        'S8': 7,
        'S9': 8
    }

    # Define the rewards
    rewards = np.array([[0, 0, 0, 5, 0, 0, 0, 0, 0],
                        [0, 0, 5, 0, 5, 0, 0, 0, 0],
                        [0, 5, 0, 0, 0, 5, 0, 0, 0],
                        [5, 0, 0, 0, 5, 0, 0, 0, 0],
                        [0, 5, 0, 5, 0, 5, 0, 5, 0],
                        [0, 0, 5, 0, 5, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 5, 0],
                        [0, 0, 0, 0, 5, 0, 5, 0, 5],
                        [0, 0, 0, 0, 0, 0, 0, 5, 0]])

    # Maps indices to locations
    state_to_location = dict((state, location) for location, state in location_to_state.items())

    # Define the actions
    actions = [0, 1, 2, 3, 4, 5, 6, 7, 8]

    print(path_planning('S2', 'S9'))

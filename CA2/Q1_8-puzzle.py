import sys


# Heuristic function (Manhattan distance)
def heuristic(state, goal_st):
    distance = 0

    for count in range(9):      # find i and j of goal and minus with i and j of state for each number between 0 to 8
        i_goal = 0
        j_goal = 0
        i_state = 0
        j_state = 0

        for i in range(3):
            for j in range(3):
                if state[i][j] == count:
                    i_state = i
                    j_state = j

                if goal_st[i][j] == count:
                    i_goal = i
                    j_goal = j

        distance += (abs(i_goal - i_state) + abs(j_goal - j_state))

    return distance


# Successor function
def successors(state):
    successor = []
    empty_i, empty_j = None, None
    for i in range(3):
        for j in range(3):
            if state[i][j] == 0:
                empty_i, empty_j = i, j

    moves = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    for move in moves:
        new_i, new_j = empty_i + move[0], empty_j + move[1]
        if 0 <= new_i < 3 and 0 <= new_j < 3:
            new_state = [row[:] for row in state]
            new_state[empty_i][empty_j] = new_state[new_i][new_j]
            new_state[new_i][new_j] = 0
            successor.append(new_state)

    return successor


# Goal test function
def is_goal(state, goal_st):
    return state == goal_st


# Print puzzle 
def print_puzzle(state):
    for row in state:
        print(row)


# Recursive Best-First Search
def rbfs(state, goal_st, f_lim):
    outcome = None
    if is_goal(state, goal_st):
        return state, None

    suc = successors(state)
    if suc is None:                      # if it has no child, then return None means there is no answer
        return None, sys.maxsize

    hue_children = []
    for child in suc:                    # calculate heuristic of children
        hue_children.append([heuristic(child, goal_st), child])

    for i in range(len(hue_children)):
        hue_children.sort(key=lambda x: x[0])  # sort by heuristics

        best_f = hue_children[0][0]            # assign best_f with first element of hue_children

        if best_f > f_lim:                     # if best_f is greater than f_limit, then return None
            return None, best_f

        alter_f = hue_children[1][0]           # assign alter_f with second element of hue_children

        # call rbfs recursively
        outcome, hue_children[0][0] = rbfs(hue_children[0][1], goal_st, min(f_lim, alter_f))

        if outcome is not None:                # if result found, then break and return it
            break

    return outcome, None


# Example input
initial_state = [[1, 2, 3], [0, 4, 6], [7, 5, 8]]
goal_state = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
f_limit = heuristic(initial_state, goal_state)
result = rbfs(initial_state, goal_state, f_limit)


print("Initial state:")
print_puzzle(initial_state)

if result[0] is not None:
    print("Goal state reached:")
    print_puzzle(result[0])
else:
    print("Goal state could not be reached.")

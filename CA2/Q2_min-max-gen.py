import math


def inputFun(n):       # get input
    print("Enter the order of Snooker scores: ", end="")
    values = [int(num) for num in input().split(" ", n-1)]
    return values


# min-max algorithm recursively
def min_max(depth, nodeIndex, maxTurn, minTurn, values, targetDepth):

    if depth == targetDepth:
        return values[nodeIndex]

    if minTurn:
        return min(min_max(depth + 1, nodeIndex * 2, True, False, values, targetDepth),
                   min_max(depth + 1, nodeIndex * 2 + 1, True, False, values, targetDepth))

    elif maxTurn:
        return max(min_max(depth + 1, nodeIndex * 2, False, True, values, targetDepth),
                   min_max(depth + 1, nodeIndex * 2 + 1, False, True, values, targetDepth))

    else:
        return None


# min-max algorithm with pruning
def min_maxWithPru(depth, nodeIndex, maxPlayer, minPlayer, values, alpha, beta, targetDepth, nodePruned):

    if depth == targetDepth:
        return values[nodeIndex]

    if minPlayer:
        best = float('inf')

        for i in range(0, targetDepth - 1):

            curr_value = min_maxWithPru(depth + 1, nodeIndex * 2 + i, True, False, values, alpha, beta, targetDepth,
                                        nodePruned)
            best = min(best, curr_value)
            beta = min(beta, best)

            if beta <= alpha:         # pruning happens here
                print('Pruning node {0} in depth {1}: '.format(nodeIndex, depth), end="")
                print('with child in node {0} in depth {1}.'.format(nodeIndex * 2 + 1, depth + 1))
                nodePruned.append(1)  # it counts number of pruning
                break

        return best


    elif maxPlayer:
        best = float('-inf')

        for i in range(0, targetDepth - 1):

            curr_value = min_maxWithPru(depth + 1, nodeIndex * 2 + i, False, True, values, alpha, beta, targetDepth,
                                        nodePruned)
            best = max(best, curr_value)
            alpha = max(alpha, best)

            if beta <= alpha:         # pruning happens here
                print('Pruning node {0} in depth {1}: '.format(nodeIndex, depth), end="")
                print('with child in node {0} in depth {1}.'.format(nodeIndex * 2 + 1, depth + 1))
                nodePruned.append(1)  # it counts number of pruning
                break

        return best


    else:
        return None


def genetic(values, depth):

    if min_max(0, 0, True, False, values, depth) >= 6:  # if min-max algorithm finds value more than 6, it is in optimal state
        return values

    values = sorted(values)                             # first sort values
    middle = len(values) // 2                           # then find the middle of values
    firstHalf = values[:middle]                         # put first half of values in a list
    secondHalf = values[middle:]                        # put second half of values in a list
    secondHalf = sorted(secondHalf, reverse=True)       # sort second half of values descending

    # put max value in second half with min value in first half next to each other (this state is optimal)
    j = 0
    for i in range(middle):
        values[j] = firstHalf[i]
        values[j + 1] = secondHalf[i]
        j += 2

    return values


# Main
# scores_Snk = [2, 4, 7, 6, 1, 0, 5, 3]                   # example of input scores based on Snooker Game

scores_Snk = inputFun(8)                                  # get scores of Snooker as input

treeDepth = math.floor(math.log(len(scores_Snk), 2))      # find the depth of the tree

print("Min-Max without Pruning:")                         # Part A.1
optimal = min_max(0, 0, True, False, scores_Snk, treeDepth)
print("The optimal value without pruning is: ", optimal)
print("=============================================")

print("Min-Max with Pruning:")                            # Part A.2
numOfPruning = []
optimalPru = min_maxWithPru(0, 0, True, False, scores_Snk, -10000, 10000, treeDepth, numOfPruning)
print("The optimal value with pruning is: ", optimalPru)
print("The total number of pruning is: ", sum(numOfPruning))
print("=============================================")

print("Optimization of the tree:")                        # Part B
scores_Snk = genetic(scores_Snk, treeDepth)
print("The optimal tree is: ", scores_Snk)
mostOpt = min_max(0, 0, True, False, scores_Snk, treeDepth)
print("The optimal value with the optimal tree is: ", mostOpt)
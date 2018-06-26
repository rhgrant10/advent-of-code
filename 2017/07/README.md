Recursive Circus
================

## Part 2

For this problem we use depth first tree traversal. The catch is we can't easily use recursion since we have to return an answer from an arbitrarily deep node. Instead, we use an iterative approach.

For each node we track the cumulative weights of its children. Once we have collected all the weights, we check for any imbalance. The trick is to use the gathered list of child weights as a way to track which children have been visited.

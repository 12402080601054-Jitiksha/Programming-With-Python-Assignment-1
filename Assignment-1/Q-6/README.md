# Q6 - Python Module Dependency Resolver

## Problem Description
The Python Module Dependency Resolver determines a valid loading order for a set of Python modules based on their import dependencies.

If module `A` imports module `B`, then module `B` must be loaded before module `A`.

The program:
* Builds a dependency graph.
* Ignores duplicate import edges.
* Uses topological sorting to determine the loading order.
* Uses a min heap to select the lexicographically smallest available module.
* Detects circular dependencies using DFS.
* Prints `CYCLE` and one detected cycle when a circular dependency exists.

---

## Input Format
```text
n e
module_1
module_2
...
module_n
module_a module_b
...
```
*Here, `module_a module_b` means that `module_a` imports `module_b`.*

## Output Format
For a valid dependency graph:
```text
module1 module2 module3 ...
```

If a cycle exists:
```text
CYCLE
module1 module2 ... module1
```

---

## Sample Input & Output

### Sample Input
```text
4 3
core
db
ui
auth
ui auth
auth db
db core
```

### Sample Output
```text
core db auth ui
```

---

## Algorithm
1. Create an adjacency-list graph.
2. Reverse each import relationship so that a dependency points to the module that depends on it.
3. Use a set to ignore duplicate edges.
4. Calculate the indegree of every module.
5. Insert all modules with indegree `0` into a min heap.
6. Repeatedly remove the lexicographically smallest module from the heap.
7. Reduce the indegree of its dependent modules.
8. Add newly available modules to the heap.
9. If all modules are processed, print the loading order.
10. Otherwise, use DFS to find and display one cycle.

---

## Data Structures
* **Dictionary:** Used for managing the graph structure and tracking indegrees.
* **Set:** Used for duplicate edge detection.
* **Min Heap:** Used to maintain lexicographical ordering of modules with an indegree of 0.
* **Lists:** Used for managing adjacency lists and recording traversal paths.
* **Dictionary:** Used to track DFS states during cycle detection.

---

## Complexity
* **Time Complexity:** \(O((n + e) \log n)\)
* **Space Complexity:** O(n + e)

---

## How to Run
Make sure Python 3.10 or later is installed.

Run the file using your terminal:
```bash
python 12402080601054_Assignment1_Q6.py
```
Enter the inputs manually or redirect from a text file according to the specified format.

---

## Testing Scenarios
The program has been validated against the following test suites:
1. Standard sample test case.
2. Graph structures containing explicit cycles.
3. Inputs containing duplicate dependency edges.
4. Independent node structures with zero overall dependencies.
5. Multiple concurrent branches having a zero-indegree.
6. Boundary configurations consisting of only a single module.
7. Graceful management of invalid or malformed input types.

---

## Learning Outcomes
Completing this script reinforces core concepts in computer science and data structure design:
* Directed Graph representations.
* **Kahn's Algorithm** paired with Priority Queues for customized topological sorting.
* State-based Depth First Search (DFS) for cycle retrieval.
* Utilizing `heapq` and tracking custom ordering criteria.
* Robust error handling and stream input parsing.

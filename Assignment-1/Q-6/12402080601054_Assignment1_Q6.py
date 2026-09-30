# Python Module Dependency Resolver
# Assignment 1 - Question 6
# Python 3.10+

import heapq
import sys


class DependencyResolver:
    """Resolves Python module dependencies."""

    def __init__(self, modules):
        self.modules = modules
        self.graph = {module: [] for module in modules}
        self.edge_set = set()
        self.indegree = {module: 0 for module in modules}

    def add_dependency(self, module_a, module_b):
        """
        module_a imports module_b.

        Therefore module_b must be loaded before module_a.
        Graph edge:
            module_b -> module_a
        """

        edge = (module_b, module_a)

        # Ignore duplicate edges
        if edge in self.edge_set:
            return

        self.edge_set.add(edge)
        self.graph[module_b].append(module_a)
        self.indegree[module_a] += 1

    def topological_sort(self):
        """
        Returns lexicographically smallest valid loading order.
        Returns None if a cycle exists.
        """

        # Work on a copy because indegree is modified.
        indegree = self.indegree.copy()

        # Min heap for lexicographically smallest module.
        heap = []

        for module in self.modules:
            if indegree[module] == 0:
                heapq.heappush(heap, module)

        order = []

        while heap:
            current = heapq.heappop(heap)
            order.append(current)

            for dependent in self.graph[current]:
                indegree[dependent] -= 1

                if indegree[dependent] == 0:
                    heapq.heappush(heap, dependent)

        if len(order) != len(self.modules):
            return None

        return order

    def find_cycle(self):
        """
        Finds one cycle using DFS.

        Returns the modules involved in the cycle.
        """

        # 0 = unvisited
        # 1 = currently visiting
        # 2 = completely processed
        state = {module: 0 for module in self.modules}

        # Stores the current DFS path.
        path = []

        # Stores the position of each module in the path.
        path_position = {}

        sys.setrecursionlimit(
            max(1_000_000, len(self.modules) + 100)
        )

        def dfs(current):

            state[current] = 1
            path_position[current] = len(path)
            path.append(current)

            for neighbor in self.graph[current]:

                # Found a back edge -> cycle
                if state[neighbor] == 1:

                    start = path_position[neighbor]

                    return path[start:] + [neighbor]

                # Continue DFS
                if state[neighbor] == 0:

                    result = dfs(neighbor)

                    if result is not None:
                        return result

            # Current module is completely processed.
            path.pop()
            path_position.pop(current, None)
            state[current] = 2

            return None

        for module in self.modules:

            if state[module] == 0:

                result = dfs(module)

                if result is not None:
                    return result

        return []

    def resolve(self):
        """Resolves dependencies and returns the required output."""

        order = self.topological_sort()

        if order is not None:
            return " ".join(order)

        cycle = self.find_cycle()

        if cycle:
            return "CYCLE\n" + " ".join(cycle)

        return "CYCLE"


def main():

    try:
        # Read n and e
        first_line = input().strip().split()

        if len(first_line) != 2:
            raise ValueError(
                "First line must contain n and e."
            )

        n = int(first_line[0])
        e = int(first_line[1])

        if n < 1:
            raise ValueError(
                "Number of modules must be at least 1."
            )

        if e < 0:
            raise ValueError(
                "Number of edges cannot be negative."
            )

        modules = []

        # Read module names
        for _ in range(n):

            module = input().strip()

            if not module:
                raise ValueError(
                    "Module name cannot be empty."
                )

            if module in modules:
                raise ValueError(
                    f"Duplicate module name: {module}"
                )

            if len(module) > 50:
                raise ValueError(
                    "Module name is too long."
                )

            modules.append(module)

        module_set = set(modules)

        resolver = DependencyResolver(modules)

        # Read dependencies
        for _ in range(e):

            parts = input().strip().split()

            if len(parts) != 2:
                raise ValueError(
                    "Each dependency must contain two module names."
                )

            module_a = parts[0]
            module_b = parts[1]

            if module_a not in module_set:
                raise ValueError(
                    f"Unknown module: {module_a}"
                )

            if module_b not in module_set:
                raise ValueError(
                    f"Unknown module: {module_b}"
                )

            resolver.add_dependency(
                module_a,
                module_b
            )

        print(resolver.resolve())

    except ValueError as error:
        print(f"INVALID {error}")

    except EOFError:
        print("INVALID")


if __name__ == "__main__":
    main()